from random import randint, getrandbits
from math import gcd as bltin_gcd


def coprime(a, b):
    return bltin_gcd(a, b) == 1


def isPrime(number):
    if number == 1 or number == 2 or number == 3:
        return True
    if number == 4:
        return False

    index = 3
    while number > index:
        if number % index == 0:
            return False
        else:
            index += 1

    if index == number:
        return True


def isCongruentNumber(number):
    if (number - 3) % 4 == 0:
        return True
    else:
        return False


class BBS:
    p = 0
    q = 0
    n = 0
    seed = 0
    generatedValues = []

    def __init__(self, p, q):
        self.setP(p)
        self.setQ(q)
        if self.p > 0 and self.q > 0:
            self.__setN()
            self.__setSeed()

    def setP(self, p):
        if not self.__checkParams(p):
            self.p = p

    def setQ(self, q):
        if not self.__checkParams(q):
            self.q = q

    @staticmethod
    def __checkParams(number):
        is_error = False
        if not isPrime(number):
            print(number, 'is not prime')
            is_error = True

        return is_error

    def __setN(self):
        self.n = self.p * self.q

    def __setSeed(self):
        while not coprime(self.n, self.seed) and self.seed < 1:
            self.seed = randint(0, self.n - 1)

    @staticmethod
    def decrypt(encrypted_msg, x0):
        return encrypted_msg, x0

    def __generateValue(self):
        if self.p > 0 and self.q > 0:
            x = 0
            while not coprime(self.n, x):
                x = randint(0, self.n)
            return pow(x, 2) % self.n

    def encrypt(self, msg: bytes):
        bits = self.generateBits(200)
        x0 = bits[:10]
        return msg, bits, x0

    def generateBits(self, amount):
        if self.p == self.q:
            print('p should be diffrent than q')
            return False

        if self.n == 0:
            print('N is equal 0')
            return False

        else:
            bits_array = []
            amount += 1

            for i in range(amount):
                generated_value = self.__generateValue()
                self.generatedValues.append(generated_value)

                if generated_value % 2 == 0:
                    bits_array.append(0)
                else:
                    bits_array.append(1)

            return bits_array


if __name__ == '__main__':
    bits = BBS(7, 31)
    bits = bits.generateBits(2000)
    print(bits)
