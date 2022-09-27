
def serialize_crossword_info(crossword):
    return {
        "type": "game.start",
        "id": crossword.id,
        "language": crossword.language.language,
        "board": crossword.board,
        "solved": crossword.solved,
        "width": crossword.width,
        "height": crossword.height,
        "total_blocks": crossword.total_blocks,
        "indices": crossword.indices,
        "clues": crossword.clues
    }


def serialize_crossword_error(err):
    return {
        "type": "game.error",
        "id": err.id,
        "message": err.msg
    }
