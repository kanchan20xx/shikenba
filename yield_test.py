# coding at utf-8
import time
import threading


def factorize(number):
    """素因数分解
    """
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


class FactorizeThread(threading.Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

print(time.time() - start)

start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

# マルチスレッドにしても逐次実行のときとあまり変わらない。
# グローバルインタプリタロックにより、マルチコアCPUで並列実行できない。
# グローバルなロックなので、内部的には一つのスレッドしか進行できない。
print(time.time() - start)