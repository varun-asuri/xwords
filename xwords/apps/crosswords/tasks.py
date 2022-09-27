from celery import shared_task
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery.exceptions import SoftTimeLimitExceeded

from .models import Crossword, Dictionary
from ...crosswords.handler import create_board, get_clues, string_to_board


def send_through_socket(crossword, event_type):
    print("sending {}".format(event_type))
    async_to_sync(get_channel_layer().group_send)(
        crossword.channels_group_name, {"type": event_type}
    )


def board_match(board_a, board_b):
    for i in range(len(board_a)):
        if board_a[i] == "-" or board_b[i] == "-":
            continue
        if board_a[i] != board_b[i]:
            return False
    return True


@shared_task(soft_time_limit=60)
def create_crossword(crossword_id):
    print("Running crossword creation task")
    try:
        crossword = Crossword.objects.get(id=crossword_id)
    except Crossword.DoesNotExist:
        return -1
    try:
        cached = crossword.language.crosswords.filter(
            width=crossword.width,
            height=crossword.height,
            total_blocks=crossword.total_blocks,
            optional_words=crossword.optional_words,
        )
        for puzzle in cached:
            if settings.NO_CACHE: continue
            if board_match(puzzle.solved, crossword.board) and puzzle.solved:
                print(puzzle.solved)
                crossword.board = puzzle.board
                print(crossword.board)
                crossword.solved = puzzle.solved
                crossword.valid = True
#                crossword.clues = puzzle.clues
                final_board = string_to_board(puzzle.solved, crossword.width, crossword.height)
                print(len(final_board))
                print(len(final_board[0]))
                across, down = get_clues(crossword.width, crossword.height, final_board, crossword.language)
                crossword.clues = {
                    "across": across,
                    "down": down
                }
                crossword.indices = puzzle.indices
                crossword.is_copy = True
                crossword.save(update_fields=['board', 'solved', 'valid', 'clues', 'indices', 'is_copy'])
                send_through_socket(crossword, "game.start")
                return 0

        if not crossword.solved:
            print("Running solver code")
            err, ret = create_board(
                crossword.height,
                crossword.width,
                crossword.total_blocks,
                crossword.board,
                crossword.language,
                crossword.optional_words
            )

            if err:
                msg = ret
                crossword.errors.create(
                    msg=msg
                )
                send_through_socket(crossword, "game.error")
                print("Error message: " + msg)
                return -1

            print("Created board")
            print(ret)
            unsolved, solved, across, down = ret

            crossword.board = unsolved
            crossword.solved = solved
            crossword.valid = True

            crossword.clues = {
                "across": across,
                "down": down
            }
            crossword.indices = list(sorted(set([*across.keys()] + [*down.keys()])))
            crossword.is_copy = False

            crossword.save(update_fields=['board', 'solved', 'valid', 'clues', 'indices', 'is_copy'])

        print("Sending crossword through socket")
        send_through_socket(crossword, "game.start")
        return 0
    except SoftTimeLimitExceeded:
        crossword.errors.create(
            msg="Timed out when creating crossword"
        )
        send_through_socket(crossword, "game.error")


@shared_task
def delete_crossword_copies():
    Crossword.objects.filter(is_copy=True).delete()
