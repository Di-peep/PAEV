from random import randint

from voter import Voter


class BR:
    """Registration office"""

    def __init__(self):
        self.voters_info = {}

    @staticmethod
    def generating_registration_numbers(length: int) -> [int]:
        """Returns a list of all generated registration numbers."""
        return list(randint(1000, 9999) for _ in range(length))

    def set_tokens(self, tokens: dict):
        for rid, token in tokens.items():
            self.voters_info[rid] = {}
            self.voters_info[rid]['token'] = token

    def voter_registration(self, voter: Voter):
        """Voter register function in the system."""
        if self.check_voter_rights(voter):
            for rid, voter_info in self.voters_info.items():
                if len(voter_info) > 1:
                    continue

                voter.register_code = rid
                voter.token = voter_info['token']
                self.voters_info[rid]['name'] = voter.name
                self.voters_info[rid]['age'] = voter.age
                return

    def check_voter_rights(self, voter: Voter) -> bool:
        if voter.age < 18:
            print(f'-! Виборець {voter.name} занадто молодий: {voter.age} років.')
            return False

        if voter.register_code in self.voters_info:
            print(f'-! Виборець {voter.name} уже має реєстровий номер.')
            return False

        return True
