import random

from elgamal.elgamal import Elgamal

from bbs import BBS
from bulletin import Bulletin


bbs = BBS(7, 31)


class Voter:
    def __init__(self, _id, full_name, age):
        self.id = _id
        self.name = full_name
        self.age = age

        self.register_code: int = 0
        self.token: dict = {}

    def make_choice(self, candidates: list):
        my_choice = random.choice(candidates)
        my_encrypted_choice, _, x0 = bbs.encrypt(my_choice.encode('utf-8'))
        message = Elgamal.encrypt(my_encrypted_choice, self.token["pubkey"])
        bulletin = Bulletin(
            choice=message,
            first_bit_gen_value=x0,
            voter_id=self.register_code
        )
        return bulletin
