from random import randint

import rsa
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

import data
from bulletin import Bulletin
from voter import Voter


class CVK:
    """Central Election Committee"""
    def __init__(self):
        self.candidates = data.candidates
        self.candidates_codes = self.init_candidates_codes()
        self.voters_registration = {}
        self.code_parts = {}
        self.voting_statistic = self.init_voting_statistic()
        self.public_key, self.__private_key = rsa.newkeys(1024)

    def init_voting_statistic(self) -> dict:
        return {candidate: 0 for candidate in self.candidates}

    def init_candidates_codes(self) -> dict:
        code_generator = self.generate_candidates_code()
        return {next(code_generator): candidate for candidate in self.candidates}

    def get_registration(self, voter: Voter) -> int:
        """
        Processes the voter's application, invokes data verification, and
        returns the generated registration number.
        """
        if self.check_voter_rights(voter):
            register_number = randint(100_000, 999_000)
            self.voters_registration[register_number] = voter.id
            return register_number

    def check_voter_rights(self, voter: Voter) -> bool:
        if voter.age < 18:
            print(f'-! Виборець {voter.name} занадто молодий: {voter.age} років.')
            return False

        if voter.id in self.voters_registration.values():
            print(f'-! Виборець {voter.name} уже має реєстровий номер.')
            return False

        return True

    def get_statistic(self, statistic: dict):
        for code in statistic:
            res = int(rsa.decrypt(statistic[code], self.__private_key))
            self.code_parts[code] = self.code_parts.get(code, 1) * res

    def counting(self):
        res = {}
        for code in list(self.code_parts.values()):
            res[code] = res.get(code, 0) + 1

        return res

    @staticmethod
    def generate_candidates_code():
        start_index = 256
        while True:
            yield start_index * 2
            start_index += start_index // 2


class VK:
    def __init__(self):
        self.voters_statistic = dict()

    def get_bulletin(self, bulletin: Bulletin):
        if bulletin.register_code in self.voters_statistic.keys():
            print(f"-! Виборець {bulletin.register_code} уже надсилав свій бюлетень..")
        elif self.check_sign(bulletin):
            self.voters_statistic[bulletin.register_code] = bulletin.choice

    @staticmethod
    def check_sign(bulletin: Bulletin) -> bool:
        msg = str(bulletin.register_code).encode("utf-8")
        hash_obj = SHA256.new(msg)
        pubkey = bulletin.pubkey
        verifier = DSS.new(pubkey, 'fips-186-3')
        try:
            verifier.verify(hash_obj, bulletin.sign)
            return True
        except ValueError:
            print("The message is not authentic.")
            return False
