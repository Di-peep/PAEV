import data
from voter import Voter


def voting():
    print(f"Формуємо список виборців...\n")
    voters = [Voter(**voter_data) for voter_data in data.voters]

    print(f"Виборці отримують бюлетені...\n")
    for voter in voters:
        voter.make_choice(candidates=data.candidates)

    list_first_pubkeys = [voter.first_pubkey for voter in voters][::-1]
    list_second_pubkeys = [(voter.second_pubkey, voter.position) for voter in voters][::-1]

    print(f"Процес кодувань бюлетенів...\n")
    for voter in voters:
        voter.first_encoding(list_first_pubkeys)
        voter.second_encoding(list_second_pubkeys)

    print(f"Формуємо список бюлетенів...\n")
    list_bulletins = [voter.bulletin for voter in voters]

    print(f"Процес декодувань бюлетенів: перше коло...\n")
    for voter in voters:
        for bulletin in list_bulletins:
            voter.second_decoding(bulletin)

    print(f"Процес декодувань бюлетенів: друге коло...\n")
    elgamal_pubkey_list = [voter.elgamal_pubkey for voter in voters]
    for i, voter in enumerate(voters):
        for bulletin in list_bulletins:
            voter.first_decoding(bulletin, elgamal_pubkey_list[i-1])

    print(f"Підрахунок результатів:\n")
    res = {c['_id']: 0 for c in data.candidates}
    for b in list_bulletins:
        res[int(b.choice.decode())] += 1

    print(f"Результати:\n")
    for c in data.candidates:
        print(f"{c['name']} - {res[c['_id']]} голосів.")


if __name__ == '__main__':
    voting()
