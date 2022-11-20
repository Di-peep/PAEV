import rsa

from voter import Voter
import data


class CVK:
    def __init__(self):
        self.candidates = data.candidates
        self.voting_statistic = self.init_voting_statistic()
        self.voters_statistic = {}
        self.public_key, self.__private_key = rsa.newkeys(1024)

    def init_voting_statistic(self):
        return {candidate: 0 for candidate in self.candidates}

    def choose_bulletin_from_set(self, set_bulletin, key):
        for i in range(len(set_bulletin) - 1):
            if self.__check_set_bulletin(set_bulletin[i], key):
                return set_bulletin[-1]

    def __check_set_bulletin(self, sb, k):
        choice = [rsa.decrypt(b.choice, k).decode('utf8') for b in sb]
        if choice == self.candidates:
            return True
        return False

    def get_bulletin(self, bulletin):
        candidate = rsa.decrypt(bulletin.choice, self.__private_key).decode('utf8')
        self.voting_statistic[candidate] += 1
        self.voters_statistic[bulletin.voter_fake_id] = candidate


def voting():
    cvk = CVK()
    print(f"Кандидати: {cvk.candidates}")
    for voter_data in data.voters:
        voter = Voter(**voter_data)
        key, set_bulletin = voter.create_sets_bulletins(cvk.candidates)
        set_bulletin = cvk.choose_bulletin_from_set(set_bulletin, key)
        bulletin = voter.voting(set_bulletin, cvk.public_key)
        cvk.get_bulletin(bulletin)

    print(f"Результати голосування: {cvk.voting_statistic}\n")

    print(f"Перелік бюлетенів:")
    for b in cvk.voters_statistic.items():
        print(f"Бюлетень: {b[0]} - {b[1]}")


if __name__ == '__main__':
    voting()
