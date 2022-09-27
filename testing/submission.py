import sys
import re
import time
import pickle

NOT_BLOCK = '*'
EMPTY = '-'
BLOCK = '#'
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
w, h, ROTATE180, LOCATIONS, ROWS, COLS, START_DICT, START_DICT_INV, CHECK_ALLOWED, PARTIAL_LOOKUP = None, None, None, None, None, None, {}, {}, {}, {}
currdepth = 0
global start_time
start_time = None
BLOCK_TIME_LIMIT = 40
TIME_LIMIT = 60

def set_globals(width, height):
    global w, h, ROTATE180, LOCATIONS, ROWS, COLS
    w, h = width, height
    ROTATE180 = {(j % h, j // h): (h - (j % h) - 1, w - (j // h) - 1) for j in range(w * h)}
    LOCATIONS = [(j % h, j // h) for j in range(w * h)]
    ROWS = [[(j, k) for k in range(w)] for j in range(h)]
    COLS = [[(k, j) for k in range(h)] for j in range(w)]


def add_seeds(board, seeds, left):
    for seed in seeds:
        start, dir, word = seed
        curr = start
        word = word.lower()
        for i, curr in enumerate(getrange(start, dir, len(word))):
            if word[i] == BLOCK:
                if get(board, curr) != BLOCK:
                    put(board, curr, BLOCK)
                    left -= 1
            else:
                put(board, curr, word[i])
            opp = ROTATE180[curr]
            if word[i] == BLOCK:
                if get(board, opp) != BLOCK:
                    put(board, opp, BLOCK)
                    left -= 1
            elif word[i] == EMPTY:
                put(board, opp, NOT_BLOCK)

    return board, left


def count(board, char):
    count = 0
    for i in board:
        for j in i:
            if j == char:
                count += 1
    return count


def opp(pos):
    return (pos[0] * -1, pos[1] * -1)


def addmult(a, b, mult=1):
    return (a[0] + b[0] * mult, a[1] + b[1] * mult)


def add(a, b):
    return addmult(a, b)


def getrange(start, diff, num):
    assert (diff[0] == 0 or diff[1] == 0)
    return [addmult(start, diff, i) for i in range(num)]


def get(board, loc):
    if not inbounds(loc):
        return None
    return board[loc[0]][loc[1]]


def put(board, loc, val):
    board[loc[0]][loc[1]] = val


def inbounds(loc):
    return loc[0] >= 0 and loc[1] >= 0 and loc[0] < h and loc[1] < w


def display(board):
    return '.\n' + '\n'.join([''.join(i) for i in board]).strip()


def num_direction(board, start, dir):
    curr = (start[0], start[1])
    count = 0
    while True:
        curr = add(curr, dir)
        if not inbounds(curr):
            break
        if get(board, curr) == BLOCK:
            break
        count += 1

    return count


def check_pos_valid(board, loc):
    # Check if it's cutting off a horizontal location
    left = num_direction(board, loc, (0, -1))
    right = num_direction(board, loc, (0, 1))
    if left + right + 1 < 3:
        return False

    # Check if it's cutting off a vertical location
    up = num_direction(board, loc, (-1, 0))
    down = num_direction(board, loc, (1, 0))
    if up + down + 1 < 3:
        return False

    return True


def get_invalids(board):
    invalids = []
    for loc in LOCATIONS:
        if get(board, loc) == BLOCK:
            continue
        if not check_pos_valid(board, loc):
            invalids.append(loc)

    return invalids


def iterative_valid(board, left):
    invalids = get_invalids(board)
    changed = set()

    if not invalids:
        return board, changed

    for invalid in invalids:
        if left < 0:
            return None, changed

        opp = ROTATE180[invalid]
        for pos in [invalid, opp]:
            if get(board, pos) == EMPTY:
                put(board, pos, BLOCK)
                changed.add(pos)
                left -= 1
            elif get(board, pos) != BLOCK:
                return None, changed

    newboard, newchanged = iterative_valid(board, left)
    return newboard, changed.union(newchanged)


def get_groups(board):
    # BFS gang
    not_blocks = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if get(board, (i, j)) != BLOCK:
                not_blocks.add((i, j))

    assert (len(not_blocks) == len(board) * len(board[0]) - count(board, BLOCK))

    groups = []
    while not_blocks:
        start = not_blocks.pop()
        queue = [start]
        groups.append(set())
        while queue:
            node = queue.pop()
            for dir in DIRECTIONS:
                neighbor = add(node, dir)
                if not inbounds(neighbor) or get(board, neighbor) == BLOCK or neighbor not in not_blocks:
                    continue
                queue.append(neighbor)
                not_blocks.remove(neighbor)
                groups[-1].add(neighbor)

    return groups


def fill(board, area, char):
    for loc in area:
        put(board, loc, char)
    return board


def get_breakup(board, loc):
    left = num_direction(board, loc, (-1, 0))
    right = num_direction(board, loc, (1, 0))
    up = num_direction(board, loc, (0, -1))
    down = num_direction(board, loc, (0, 1))

    #    return (up*down + left*right) / 5 + up + down + left + right
    heuristic = 0
    for s in [left, right, up, down]:
        if s <= 2:
            heuristic -= s * 25
#            print("HI")
    return left * right + up * down


start = time.time()


def recur(board, left, depth=0):
    global start_time
    if time.time() - start_time > BLOCK_TIME_LIMIT:
        return None
    valid, changed = iterative_valid(board, left)
    left -= len(changed)
    if valid is None:
        # Undo any changes that were made before returning
        fill(board, changed, EMPTY)
        return None
    board = valid

    # Check if there are any walls, and if so try to fix them
    groups = get_groups(board)
    if len(groups) > 1:
        fill(board, changed, EMPTY)
        return None
        toRemove = []
        for group in groups:
            temp = group.pop()
            toFill = ROTATE180[temp] not in group
            group.add(temp)
            if toFill:
                if len(group) > left:
                    # Undo any changes
                    fill(board, changed, EMPTY)
                    return None
                fill(board, group, BLOCK)
                left -= len(group)
                changed = changed.union(group)
                toRemove.append(group)
        for group in toRemove:
            groups.remove(group)

        groups = sorted(groups, key=lambda g: len(g))
        lengths = [len(group) for group in groups]
        total = sum(lengths)
        tryout = []
        for i in range(len(lengths)):
            # If you have enough blocks to place such that you can try leaving that area empty
            if total - lengths[i] < left:
                tryout.append(i)

        if len(tryout) == 0:
            fill(board, changed, EMPTY)
            return None

        # Try filling in all the other groups
        for i in tryout:
            for ind, group in enumerate(groups):
                if i != ind:
                    board = fill(board, group, BLOCK)
            new_board = recur(board, left - (total - lengths[i]), depth + 1)
            if new_board:
                return new_board
            for ind, group in enumerate(groups):
                if i != ind:
                    board = fill(board, group, EMPTY)

        fill(board, changed, EMPTY)
        return None

    if left == 0:
        return board

    locations = LOCATIONS[:len(LOCATIONS) // 2 + 1]
    locations = list(reversed(sorted(locations, key=lambda loc: get_breakup(board, loc))))
    # Only go through half of the locations
    for loc in locations:

        if loc[0] == w // 2 and loc[1] == h // 2 and w % 2 == 1 and h % 2 == 1:
            continue

        opp = ROTATE180[loc]

        if get(board, loc) != EMPTY or get(board, opp) != EMPTY:
            continue

        put(board, loc, BLOCK)
        put(board, opp, BLOCK)

        new_board = recur(board, left - 2, depth + 1)
        if new_board:
            return new_board

        put(board, loc, EMPTY)
        put(board, opp, EMPTY)

    # Undo any changes that were made before returning
    fill(board, changed, EMPTY)
    return None


def get_blocked_board(w, h, blocking, initial):
    set_globals(w, h)
    left = blocking
    board = [[i for i in initial[idx*w:(idx+1)*w]] for idx in range(h)]
#    print("Seeded board:")
#    print(board)
#    print(display(board))
#    print()

    left -= count(board, BLOCK)
    if w % 2 == 1 and h % 2 == 1:
        loc = (h // 2, w // 2)
        if left % 2 == 1:
            put(board, loc, BLOCK)
            left -= 1
        elif get(board, loc) == EMPTY:
            put(board, loc, NOT_BLOCK)

    global start_time
    start_time = time.time()
    final_board = recur(board, left)
    if not final_board:
        return None
    final_board = [[EMPTY if j == NOT_BLOCK else j for j in i] for i in final_board]
    return final_board


def score_word(word, occurs):
    score = 0
    for letter in word:
        if letter not in occurs:
            continue
        score += occurs[letter]
    return -score


def set_start_lookup(board):
    global START_DICT, START_DICT_INV
    START_DICT, START_DICT_INV = {}, {}
    for row in ROWS:
        prev_block = True
        prev_start = None
        for pos in row:
            if get(board, pos) == BLOCK:
                prev_block = True
            else:
                if prev_block:
                    prev_start = pos
                    prev_block = False
                    START_DICT[(prev_start, (0, 1))] = []
                START_DICT_INV[(pos, (0, 1))] = prev_start
                START_DICT[(prev_start, (0, 1))].append(pos)

    for col in COLS:
        prev_block = True
        prev_start = None
        for pos in col:
            if get(board, pos) == BLOCK:
                prev_block = True
            else:
                if prev_block:
                    prev_start = pos
                    prev_block = False
                    START_DICT[(prev_start, (1, 0))] = []
                START_DICT_INV[(pos, (1, 0))] = prev_start
                START_DICT[(prev_start, (1, 0))].append(pos)


def set_partial_lookup(bucket):
    letters = "abcdefghijklmnopqrstuvwxyz"
    assert (len(letters) == 26)
    for word_len in bucket:
        words = bucket[word_len]
        for letter in letters:
            for idx in range(word_len):
                restricted = {word for word in words if word[idx] == letter}
                PARTIAL_LOOKUP[(word_len, idx, letter)] = restricted


def check_allowed(board, word, curr_word):
    if (word, curr_word) in CHECK_ALLOWED:
        return CHECK_ALLOWED[(word, curr_word)]
    if len(word) != len(curr_word):
        print(display(board))
        print(word, curr_word, len(word), len(curr_word))
    assert (len(word) == len(curr_word))
    for i in range(len(curr_word)):
        if curr_word[i] != EMPTY and word[i] != EMPTY and curr_word[i] != word[i]:
#            print(word, curr_word)
            CHECK_ALLOWED[(word, curr_word)] = False
            CHECK_ALLOWED[(curr_word, word)] = False
            return False
    CHECK_ALLOWED[(word, curr_word)] = True
    CHECK_ALLOWED[(curr_word, word)] = True
    return True


def intersect(seq1, seq2):
    for val in seq1:
        if val in seq2:
            return val
    return None


def filter_possible_words(board, poss, used, prev_placed=None):
    delete = []
    for start in poss.keys():
        seq = START_DICT[start]
        word = ''.join([get(board, pos) for pos in seq])
        if EMPTY not in word:
            if word not in poss[start]:
#                print("WORD NOT IN POSS[START]")
                return False, poss, used
            if word in used:
#                print("WORD IN USED")
                return False, poss, used
            used.add(word)
            delete.append(start)
        else:
            words = poss[start]
            words2 = None

            if prev_placed is not None:
                prev_start, prev_word = prev_placed
                prev_seq = START_DICT[prev_start]
                intersection = intersect(prev_seq, seq)
                if intersection is None:
                    continue
                idx = seq.index(intersection)
                letter = get(board, intersection)
                length = len(seq)
                words = [w for w in words if w in PARTIAL_LOOKUP[(length, idx, letter)]]
                poss[start] = words
                continue

            prevlen = len(words)
#            print(prevlen)
#            print(start, START_DICT[start], word)
            words = [w for w in words if check_allowed(board, w, word)]
#            print(len(words))
            poss[start] = words

        if len(poss[start]) == 0:
#            print("LEN POSS IS 0")
            return False, poss, used

    for key in delete:
        seq = START_DICT[key]
        word = ''.join([get(board, pos) for pos in seq])
        del poss[key]

#    print("ITS ALL GUCCI")
    return True, poss, used


def place(board, loc, word, dir):
    for i, pos in enumerate(getrange(loc, dir, len(word))):
        put(board, pos, word[i])
    return board


bestdepth = 0


def place_words(board, poss, used, last_placed=None, depth=0):
    global start_time
    if depth == 0:
        start_time = time.time()
    if time.time() - start_time > TIME_LIMIT:
        return None
    global currdepth, bestdepth
    currdepth = depth

    if depth > bestdepth:
        bestdepth = depth

    poss_copy = [(k, poss[k].copy()) for k in poss]

    valid, poss, used = filter_possible_words(board, poss, used, last_placed)
    if not valid:
        for k, v in poss_copy:
            poss[k] = v
        return None

    if len(poss) == 0:
        return board

    # Decide maxkey
    maxkey = min(poss, key=lambda k: len(poss[k]))
    loc, dir = maxkey
    words = poss[maxkey]
    del poss[maxkey]

    word_len = num_direction(board, loc, dir) + 1
    for word in words:
        if word in used:
            continue

        prev = []
        # Place word on board
        pos = loc
        for i, pos in enumerate(getrange(loc, dir, len(word))):
            prev.append(get(board, pos))
            put(board, pos, word[i])

        currdepth = depth

        newboard = place_words(board, poss, used | {word}, (maxkey, word), depth + 1)
        if newboard is not None:
            return newboard

        currdepth = depth

        # Unplace word from board
        pos = loc
        for i, pos in enumerate(getrange(loc, dir, len(word))):
            put(board, pos, prev[i])

    for k, v in poss_copy:
        poss[k] = v

    return None


def setup(board, words):
    set_start_lookup(board)
#    set_partial_lookup(words)
#    print("PRINTING STUFF", board)
#    print(len(words))
#    print(START_DICT)
    poss = {key: words[num_direction(board, key[0], key[1]) + 1].copy() for key in START_DICT}
#    print(poss[((0, 0), (0, 1))])
    valid, poss, used = filter_possible_words(board, poss, set())
    if not valid:
#        print("Words are being weird?")
        return None, None
    return poss, used
