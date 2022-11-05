import rsa


class Bulletin:
    def __init__(self, cvk_public_key):
        self.choice = 'choice'
        self.cvk_pubkey = cvk_public_key
        self.public_key, self.__private_key = rsa.newkeys(1024)
        self.sign = 'sign'

    def create_sign(self, voter_id: int):
        self.sign = rsa.sign(bytes(voter_id), self.__private_key, 'SHA-1')

    def make_choice(self, candidate: str):
        self.choice = rsa.encrypt(candidate.encode('utf8'), self.cvk_pubkey)
