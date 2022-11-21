from random import randint, choice

from Crypto.Hash import SHA256
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from elgamal.elgamal import Elgamal

from bulletin import Bulletin


class Voter:
    def __init__(self, id, full_name, age):
        self.id = id
        self.name = full_name
        self.age = age

        self.register_number = 0
        self.fake_id = randint(100_000, 999_000)

    def make_choice(self, candidates: list, cvk_key) -> Bulletin:
        my_choice = choice(candidates).encode("utf-8")
        my_choice = Elgamal.encrypt(my_choice, cvk_key)
        bulletin = Bulletin(
            register_code=self.register_number,
            voter_fake_id=self.fake_id,
            choice=my_choice
        )
        self.make_sign(bulletin)
        return bulletin

    def make_sign(self, bulletin: Bulletin):
        key = DSA.generate(2048)
        hash_obj = SHA256.new(str(self.register_number).encode("utf-8"))
        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(hash_obj)
        bulletin.sign_key = key.publickey().export_key()
        bulletin.sign = signature
