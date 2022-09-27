import pickle, json
import testing.submission as submission
#set_globals, setup, score_word, place_words, display, set_partial_lookup, get_blocked_board
#from xwords.apps.crosswords.models import Dictionary

def str_to_board(w, h, string):
    assert(len(string) == w*h)
    return [[j for j in string[i*w:(i+1)*w]] for i in range(h)]
    

def get_words(words, w, h):
#    file = open("dctEckel.txt")
#    words = [line.strip() for line in file]
    # Sort words by how often their letters appear
    occurs = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
    buckets = {i: [] for i in range(max(h, w) + 1)}
    for word in words:
        failed = False
        for letter in word:
            if letter not in occurs:
                failed = True
                break
            occurs[letter] += 1
        if failed:
            continue
        if len(word) in buckets:
            buckets[len(word)].append(word)
        else:
            buckets[len(word)] = [word]

    for key in buckets:
        bucket = buckets[key]
        bucket = sorted(bucket, key=lambda word: submission.score_word(word, occurs))
        buckets[key] = bucket

    return buckets



def test_blocked():
#    board_str = "#-----#---#-----#---#---------##-------------#--------#-------------##---------#---#-----#---#-----#"
    board_str = "-------------------------------#------------------------------------#-------------------------------"
    w, h = 10, 10
    language = "English"

    board = str_to_board(10, 10, board_str)
    dictionary = Dictionary.objects.get(language=language)
    print(submission.display(board))
    submission.set_globals(w, h)

    words = get_words(dictionary, w, h)
    submission.set_partial_lookup(words)
    poss, used = submission.setup(board, words)

    final_board = submission.place_words(board, poss, used)
    assert(final_board is not None)

    print(submission.display(board))


def create_partial_lookup(bucket):
    lookup = {}
    letters = "abcdefghijklmnopqrstuvwxyz0123456789"
    assert (len(letters) == 36)
    for word_len in bucket:
        words = bucket[word_len]
        for letter in letters:
            for idx in range(word_len):
                restricted = {word for word in words if word[idx] == letter}
                lookup[(word_len, idx, letter)] = restricted
    return lookup


def create_lookup():
    dictionary = Dictionary.objects.get(language="English")
    words = get_words(dictionary, 30, 30)
    lookup = create_partial_lookup(words)
    with open("lookup.pkl", "wb") as out:
        pickle.dump(lookup, out)
        out.close()


def load():
    words = [line.strip().split(",")[1] for line in open("word.csv")]
    all_words = get_words(words, 30, 30)
    submission.set_partial_lookup(all_words)
    return all_words


def bruteforce(all_words):
    bruteforced = {}
#    dictionary = Dictionary.objects.get(language="English")
#    words = dictionary.words.all_words()
    for size in range(3, 31):
        w, h = size, size
        for num_blocks in range(0, w * h - 8):
#            w, h, num_blocks = 10, 10, 20
            print(size, num_blocks)
            board = '-' * (w * h)
#            board = str_to_board(w, h, '-' * (w * h))
            blocked_board = submission.get_blocked_board(w, h, num_blocks, board)
            if not blocked_board:
                print("No blocked board could be made")
                bruteforced[(w, h, num_blocks)] = (None, None)
                continue

            board = [i.copy() for i in blocked_board]
            print("Blocked board:")
            print(submission.display(board))
            print()

            submission.set_globals(w, h)
            words = {i: all_words[i].copy() for i in all_words}
            poss, used = submission.setup(board, words)

#            print(poss)

            final_board = submission.place_words(board, poss, used)
            if final_board:
                print(submission.display(final_board))
                bruteforced[(w, h, num_blocks)] = (blocked_board, final_board)
            else:
                print("Could not be solved")
                bruteforced[(w, h, num_blocks)] = (blocked_board, None)

        print(bruteforced)
        with open("bruteforced" + str(size) + ".pkl", "wb") as out:
           pickle.dump(bruteforced, out)
           out.close()


words = load()
#letters = set()
#for bucket in words:
#    for word in words[bucket]:
#        for letter in word:
#            letters.add(letter)
#print(letters)
bruteforce(words)
#test_blocked()
