from random import randint, choice

import rsa

from bulletin import Bulletin


class Voter:
    def __init__(self, id, full_name, age):
        self.id = id
        self.name = full_name
        self.age = age

        self.fake_id = randint(100_000, 990_000)
        self.public_key, self.__private_key = rsa.newkeys(1024)

    def create_sets_bulletins(self, candidates, *, amount=3):
        set_bulletins = []
        for _ in range(amount):
            set_bulletins.append(tuple(Bulletin(self.fake_id, self.encrypt_choice(c)) for c in candidates))

        return self.__private_key, set_bulletins

    def encrypt_choice(self, candidate):
        return rsa.encrypt(candidate.encode('utf8'), self.public_key)

    def voting(self, pair_bulletin, cvk_public_key):
        bulletin = choice(pair_bulletin)
        candidate = rsa.decrypt(bulletin.choice, self.__private_key).decode('utf8')
        candidate = rsa.encrypt(candidate.encode('utf8'), cvk_public_key)
        bulletin.choice = candidate
        return bulletin
