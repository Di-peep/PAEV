from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from elgamal.elgamal import Elgamal

import data
from bulletin import Bulletin
from registration_office import BR
from voter import Voter


class CVK:
    """Central Election Committee"""

    def __init__(self):
        self.candidates = data.candidates
        self.registration_list = []
        self.voters_statistic = {}
        self.voting_statistic = self.init_voting_statistic()
        self.public_key, self.__private_key = Elgamal.newkeys(64)

    def init_voting_statistic(self):
        return {candidate: 0 for candidate in self.candidates}

    def get_registration_list(self, reg_list: list):
        self.registration_list = reg_list

    def get_bulletin(self, bulletin: Bulletin):
        if self.check_bulletin(bulletin):
            candidate = Elgamal.decrypt(bulletin.choice, self.__private_key).decode("utf-8")
            voter_fid = bulletin.voter_fake_id
            register_number = bulletin.register_code

            self.voting_statistic[candidate] += 1
            self.voters_statistic[voter_fid] = candidate
            self.registration_list.remove(register_number)

    def check_bulletin(self, bulletin: Bulletin) -> bool:
        if bulletin.register_code not in self.registration_list:
            print(f"-! Надісланий бюлетень {bulletin.register_code} має недійсний реєстраційний номер.")
            return False

        if not self.check_sign(bulletin.sign, bulletin.register_code, bulletin.sign_key):
            print(f"-! Надісланий бюлетень {bulletin.register_code} має недійсний підпис.")
            return False

        return True

    def check_sign(self, signature, msg, pub_key) -> bool:
        try:
            hash_obj = SHA256.new(str(msg).encode("utf-8"))
            verifier = DSS.new(pub_key, 'fips-186-3')
            verifier.verify(hash_obj, signature)
        except ValueError:
            return False
        finally:
            return True


def voting():
    br = BR()
    cvk = CVK()
    voters = [Voter(**voter_data) for voter_data in data.voters]

    print(f"Список кандидатів: {cvk.candidates}\n")
    print(f"Видача реєстреційних номерів для виборців...")
    for voter in voters:
        voter_register_number = br.get_registration(voter)
        voter.register_number = voter_register_number

    print(f"\nПередача списку реєстраційних номерів до ЦВК...\n")
    cvk.get_registration_list(br.get_all_registration_numbers())

    print(f"Початок голосування...")
    for voter in voters:
        bulletin = voter.make_choice(cvk.candidates, cvk.public_key)
        cvk.get_bulletin(bulletin)

    print(f"\nРезультати голосування: {cvk.voting_statistic}\n")
    print(f"Перелік бюлетенів:")
    for b in cvk.voters_statistic.items():
        print(f"Бюлетень: {b[0]} - {b[1]}")


if __name__ == '__main__':
    voting()
