import data
from election_commission import CVK, VK
from voter import Voter


def voting():
    cvk = CVK()
    vkf = VK()
    vks = VK()
    voters = [Voter(**voter_data) for voter_data in data.voters]

    print(f"Список кандидатів та їх кодів: {cvk.candidates_codes}\n")
    print(f"Видача реєстреційних номерів для виборців...")
    for voter in voters:
        voter_register_code = cvk.get_registration(voter)
        if voter_register_code:
            voter.register_code = voter_register_code

    print(f"\nПочаток голосування...")
    candidates_codes = list(cvk.candidates_codes.keys())
    for voter in voters:
        bulletin1, bulletin2 = voter.make_choice(candidates_codes, cvk.public_key)
        vkf.get_bulletin(bulletin1)
        vks.get_bulletin(bulletin2)

    print(f"\nПублікація результатів ВК-1 та ВК-2:")
    print(f"ВК-1:", vkf.voters_statistic)
    print(f"ВК-2:", vks.voters_statistic)

    print(f"\nПередача результатів до ЦВК..")
    cvk.get_statistic(vkf.voters_statistic)
    cvk.get_statistic(vks.voters_statistic)

    print(f"\nСписок виданих кодів та їх голос:")
    print(cvk.code_parts)

    print(f"Результати виборів:")
    print(cvk.candidates_codes)
    print(cvk.counting())


if __name__ == '__main__':
    voting()
