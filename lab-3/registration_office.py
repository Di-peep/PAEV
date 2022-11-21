from random import randint

from voter import Voter


class BR:
    """Registration office"""

    def __init__(self):
        self.voters_registration = {}

    def get_all_registration_numbers(self):
        """Returns a list of all issued registration numbers."""
        return list(self.voters_registration.keys())

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
