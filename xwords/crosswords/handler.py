from .solver import display, setup_poss, setup_start, set_partial_lookup, score_word
from .solver import get_blocked_board, place_words
from django.db.models.functions import Length
from django.conf import settings
import time
import random


def board_to_string(board):
    return ''.join([''.join(row) for row in board])


def string_to_board(string, w, h):
    assert(w * h == len(string))
    board = []
    for i in range(h):
        board.append([j for j in string[i*w:(i+1)*w]])
    return board


def get_words(dictionary, lengths, optional_words):
    words = dictionary.words.annotate(text_len=Length('word')).filter(text_len__in=list(lengths))
    # Sort words by how often their letters appear
    occurs = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
    buckets = {i: [] for i in lengths}
    for worditem in words:
        word = worditem.word
        for letter in word:
            if letter not in occurs:
                continue
            occurs[letter] += 1
        length = len(word)
        if length in buckets:
            buckets[length].append(word)
        else:
            buckets[length] = [word]

    print("Sorting: " + str(time.time()))
    for key in buckets:
        bucket = buckets[key]
        bucket = sorted(bucket, key=lambda word: -float("inf") if word in optional_words else score_word(word, occurs) * random.uniform(1 - settings.DETERMINISTIC_RATE, 1 + settings.DETERMINISTIC_RATE))
        buckets[key] = bucket

    return buckets


def get_clues(w, h, board, dictionary):
    across = {}
    curr_idx = None
    for row in range(h):
        curr_word = ""
        for col in range(w):
            if board[row][col] == "#":
                if curr_word:
                    clue = random.choice(dictionary.words.get(word=curr_word.strip()).definitions.all_definitions())
                    curr_word = ""
                    assert(curr_idx is not None)
                    across[curr_idx] = clue
            else:
                if len(curr_word) == 0:
                    curr_idx = w * row + col
                curr_word += board[row][col]
        if curr_word:
            clue = random.choice(dictionary.words.get(word=curr_word).definitions.all_definitions())
            curr_word = ""
            across[curr_idx] = clue

    down = {}
    curr_idx = None
    for col in range(w):
        curr_word = ""
        for row in range(h):
            if board[row][col] == "#":
                if curr_word:
                    clue = random.choice(dictionary.words.get(word=curr_word).definitions.all_definitions())
                    curr_word = ""
                    assert(curr_idx is not None)
                    down[curr_idx] = clue
            else:
                if len(curr_word) == 0:
                    idx = w * row + col
                    curr_idx = idx
                curr_word += board[row][col]
        if curr_word:
            clue = random.choice(dictionary.words.get(word=curr_word).definitions.all_definitions())
            curr_word = ""
            down[curr_idx] = clue

    return across, down


def create_board(height, width, total_blocks, board, dictionary, optional_words):
    blocked_board = get_blocked_board(width, height, total_blocks, board)
    print("Optional words: " + str(optional_words))
    if not blocked_board:
        return True, "Couldn't make valid blocked board"
    blocked_board_copy = [row.copy() for row in blocked_board]
    board = [i.copy() for i in blocked_board]
    print("Blocked board:")
    print(display(board))
    print()

    print("SETTING UP START DICT: " + str(time.time()))
    needed_lengths = setup_start(board)
    print("GETTING WORDS: " + str(time.time()))
    words = get_words(dictionary, needed_lengths, optional_words)
    print("SETTING UP PARTIAL LOOKUP: " + str(time.time()))
    set_partial_lookup(words, dictionary)
    print("GETTING INITIAL POSSES: " + str(time.time()))
    poss, used = setup_poss(board, words)
    print("DONE SETTING UP: " + str(time.time()))
    if not poss:
        return True, "Can't even start putting words on board"

    final_board = place_words(board, poss, used, set(optional_words))
    print("Final board:")
    print(display(final_board))
    print()
    if not final_board:
        return True, "Couldn't place words"

    across, down = get_clues(width, height, final_board, dictionary)

    blocked_board_copy = board_to_string(blocked_board_copy)
    final_board = board_to_string(final_board)
    return False, [blocked_board_copy, final_board, across, down]
