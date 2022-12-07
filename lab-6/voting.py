import data
from election_commission import VK
from registration_office import BR
from voter import Voter


def voting():
    br = BR()
    vk = VK()

    print(f"Генерація реєстраційних номерів та токенів..\n")
    registration_numbers = br.generating_registration_numbers(len(data.voters))
    tokens = vk.generate_tokens(registration_numbers)
    br.set_tokens(tokens)

    print(f"Початок реєстрації виборців..\n")
    voters = [Voter(**voter_data) for voter_data in data.voters]
    for voter in voters:
        br.voter_registration(voter)

    print(f"\nВиборці формують бюлетені та голосують..\n")
    for voter in voters:
        try:
            bulletin = voter.make_choice(data.candidates)
            vk.get_bulletin(bulletin)
        except KeyError:
            print(f"-! Надісланий невірний токен..")

    print(f"\nПідведення підсумків:")
    print(vk.voting_result)


if __name__ == '__main__':
    voting()
