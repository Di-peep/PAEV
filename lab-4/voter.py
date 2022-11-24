from random import choice
import rsa

import elgamal
from bulletin import Bulletin


class Voter:
    def __init__(self, _id, full_name, age, n):
        self.id = _id
        self.name = full_name
        self.age = age
        self.position = n

        self.bulletin = Bulletin()
        self.elgamal_pubkey, self.signature = elgamal.elgamal_sign()
        self.first_pubkey, self._first_privkey = rsa.newkeys(128*n)
        self.second_pubkey, self._second_privkey = rsa.newkeys(640*n)

    def make_choice(self, candidates: dict):
        my_choice = str(choice(candidates)['_id']).encode("utf-8")
        self.bulletin.choice = my_choice

    def first_encoding(self, list_of_pubkeys: list):
        for pubkey in list_of_pubkeys:
            self.bulletin.choice = rsa.encrypt(self.bulletin.choice, pubkey)

    def second_encoding(self, list_of_pubkeys: [tuple]):
        for pubkey, pos in list_of_pubkeys:
            self.bulletin.choice += str(pos).encode("utf-8")
            self.bulletin.choice = rsa.encrypt(self.bulletin.choice, pubkey)

    def second_decoding(self, bulletin: Bulletin):
        decrypted = rsa.decrypt(bulletin.choice, self._second_privkey)
        bulletin.choice = decrypted[:-1]

    def first_decoding(self, bulletin: Bulletin, pubkey):
        if bulletin.sign == 'sign' or elgamal.check_sign(pubkey, bulletin.sign):
            decrypted = rsa.decrypt(bulletin.choice, self._first_privkey)
            bulletin.choice = decrypted
            bulletin.sign = self.signature
        else:
            print(f"-! Невалідний підпис.")
