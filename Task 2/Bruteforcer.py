from hashlib import sha256
import time
import threading

class Bruteforcer:
    def __init__(self):
        self.file = "hashes.txt"
        self.threadsnum = 1
        self.alph = "abcdefghijklmnopqrstuvwxyz"
        self.fileopen()

    def set_threadsnum(self, threadsnum):
        self.threadsnum = threadsnum

    def fileopen(self):
        try:
            with open(self.file, "r") as f:
                self.hashes = f.read().splitlines()
        except:
            print("ERROR! File cannot be opened!")

    def func_chunks_generators(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    def get_time(self):
        start_time = time.time()
        while True:
            if threading.active_count() == 2:
                print("Затрачено времени: ", (time.time() - start_time))
                return

    def brute(self):
        thrdchrs = list(
                self.func_chunks_generators(
                    self.alph, int(26 / int(self.threadsnum))))
        timechk = threading.Thread(target=self.get_time)
        for thrd in thrdchrs:
            x = threading.Thread(target=self.crack, args=(thrd[0], thrd[-1],))
            x.start()
        timechk.start()

    def crack(self, start='a', end='z'):
        for i in range(ord(start), ord(end)+1):
            for j in range(ord('a'), ord('z')+1):
                for k in range(ord('a'), ord('z')+1):
                    for l in range(ord('a'), ord('z')+1):
                        for m in range(ord('a'), ord('z')+1):
                            word = chr(i) + chr(j) + chr(k) + chr(l) + chr(m)
                            if len(self.hashes):
                                self.chckhash(word)
                            else:
                                return

    def chckhash(self, word):
        for hash in self.hashes:
            wordencoded = sha256(word.encode('utf-8')).hexdigest()
            if hash == wordencoded:
                print(hash, " : ", word)
                self.hashes.remove(wordencoded)
                return


if __name__ == '__main__':
    thrdin = input("Enter number of threads(default = 1, max = 26): ")
    a = Bruteforcer()
    if thrdin:
        if int(thrdin)<0:
            thrdin = 1
        elif int(thrdin)>26:
            thrdin = 26
        a.set_threadsnum(thrdin)
        a.brute()

