from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession
import sys, time, pickle, multiprocessing, datetime
#session = WolframLanguageSession()
session = WolframLanguageSession('D:/Program Files/Mathematica/12.0/WolframKernel.exe')
words = open(sys.argv[1], 'r').read().strip().split('\n')
name = sys.argv[2]
clues = dict()
clues = pickle.load( open( "cluesMaster.pkl", "rb" ) )

# defnquery = 'WordDefinition["{}"]'.format('hello')
# defn = session.evaluate(wlexpr(defnquery))
# if defn[0] == 'UnknownWord': print('dne')
# print(defn)
length = len(words)
pool_size = 4

def extract_word(n, word):
    t0 = time.time()
    word = word.lower()
    if session.evaluate(wlexpr('DictionaryWordQ["{}"]'.format(word))): 
        cluequery = 'Entity["Word", "{}"]["NYTCrosswordPuzzleClues"]'.format(word)
        clue = session.evaluate(wlexpr(cluequery))
        if not (clue[0] == 'NotAvailable' or clue[0] == 'UnknownEntity'): 
            clues.update({word: clue})
            #print('{} in {:.2f}s   \t| {:.2f}%'.format(word, time.time() - t0, n/length * 100))
    return time.time() - t0
backup_time = 500
display_time = 10
t = t1 = t2 = time.time()
runningtime = count = 0
for n, word in enumerate(words):
    if word in clues: continue
    if time.time() - t1 >= backup_time: 
        pickle.dump(clues, open('clues{}.pkl'.format(name),'wb'))
        t1 = time.time()
        print('Backed up @ {}\t Uptime: {:.2f}s'.format(datetime.datetime.now(), time.time() - t))
    if time.time() - t2 >= display_time:
        t2 = time.time()
        print('ETA: {} \t | {:.2f}% Completed'.format(str(datetime.timedelta(seconds= runningtime/count * (length - n))), n/length * 100))
    runningtime += extract_word(n, word)
    count += 1
