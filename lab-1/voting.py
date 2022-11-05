import random

from voters import voters
from bulletin import Bulletin, rsa


class CVK:
    def __init__(self, candidates=None, voters=None):
        self.public_key, self.__private_key = rsa.newkeys(1024)
        self.candidates = candidates or self.generate_candidates()
        self.voting_statistic = self.init_voting_statistic()
        self.voters = voters or self.init_voters()
        self.voters_statistic = []

    @staticmethod
    def generate_candidates():
        return ['candidate_1', 'candidate_2']

    @staticmethod
    def init_voters():
        return voters

    @staticmethod
    def check_voter_rights(voter):
        if voter['age'] > 18:
            return True
        return False

    def init_voting_statistic(self):
        return {candidate: 0 for candidate in self.candidates}

    def generate_bulletin(self, voter):
        if voter in self.voters_statistic:
            print(f'- Виборець {voter["full_name"]} уже голосував.')
            return

        if self.check_voter_rights(voter):
            bull = Bulletin(self.public_key)
            self.voters_statistic.append(voter)
            return bull

    def get_bulletin(self, voter, bulletin: Bulletin):
        if not self.__check_sign(voter, bulletin):
            return

        choice = rsa.decrypt(bulletin.choice, self.__private_key).decode('utf8')
        self.voting_statistic[choice] += 1
        return choice

    @staticmethod
    def __check_sign(voter, bulletin):
        voter_id = bytes(voter['id'])
        signature = bulletin.sign
        pubkey = bulletin.public_key
        try:
            rsa.verify(voter_id, signature, pubkey)
            return True
        except rsa.pkcs1.VerificationError:
            print('-! Невалідний підпис бюлетеня')
            return False


def voting():
    cvk = CVK()
    print(f"Список кандидатів: {cvk.candidates}\n")

    for voter in voters:
        bulletin = cvk.generate_bulletin(voter)
        if bulletin:
            bulletin.make_choice(random.choice(cvk.candidates))
            bulletin.create_sign(voter['id'])
            cvk.get_bulletin(voter, bulletin)
            print(f"+ Виборець {voter['full_name']} зробив свій вибір.\n")
        else:
            print(f"- Виборець {voter['full_name']} не може голосувати у цьому голосуванні.\n")

    print(f"Результати голосування: {cvk.voting_statistic}")


if __name__ == '__main__':
    voting()
