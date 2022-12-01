from random import choice

import rsa
from Crypto.Hash import SHA256
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from rsa import PublicKey

from bulletin import Bulletin


class Voter:
    def __init__(self, _id, full_name, age):
        self.id = _id
        self.register_code = _id
        self.name = full_name
        self.age = age
        self.sign = 'sign'
        self.pubkey = 'key'

    def make_choice(self, candidates_code: list, cvk_pubkey: PublicKey) -> (Bulletin, Bulletin):
        my_choice = choice(candidates_code)
        first_code, second_code = self.code_split(my_choice)
        first_code = rsa.encrypt(str(first_code).encode("utf-8"), cvk_pubkey)
        second_code = rsa.encrypt(str(second_code).encode("utf-8"), cvk_pubkey)
        self.make_sign()
        first_bulletin = Bulletin(self.register_code, first_code, self.sign, self.pubkey)
        second_bulletin = Bulletin(self.register_code, second_code, self.sign, self.pubkey)
        return first_bulletin, second_bulletin

    def make_sign(self):
        key = DSA.generate(2048)
        msg = str(self.register_code).encode("utf-8")
        hash_obj = SHA256.new(msg)
        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(hash_obj)
        self.sign = signature
        self.pubkey = key.public_key()

    @staticmethod
    def code_split(value: int, start=8, step=2) -> (int, int):
        for divider in range(start, value, step):
            if value % divider == 0:
                return divider, value // divider
        else:
            return value, 1
