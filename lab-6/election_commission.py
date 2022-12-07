from elgamal.elgamal import Elgamal

from voter import bbs
from bulletin import Bulletin


class VK:
    def __init__(self):
        self.voters_info = {}
        self.voting_result = {}
        self.public_key, self.__private_key = Elgamal.newkeys(64)

    def generate_tokens(self, registration_code_list: [int]) -> dict:
        tokens = {}
        for reg_code in registration_code_list:
            token = {
                "pubkey": self.public_key,
                "reg_code": reg_code
            }
            self.voters_info[reg_code] = dict()
            self.voters_info[reg_code]['token'] = token

            tokens[reg_code] = token

        return tokens

    def get_bulletin(self, bulletin: Bulletin):
        voter_choice = self.decrypting_bulletin(bulletin)
        self.voting_result[voter_choice] = self.voting_result.get(voter_choice, 0) + 1

    def decrypting_bulletin(self, bulletin: Bulletin):
        first_decrypt = Elgamal.decrypt(bulletin.choice, self.__private_key).decode("utf-8")
        second_decrypt, _ = bbs.decrypt(first_decrypt, bulletin.first_bit_gen_value)
        return first_decrypt
