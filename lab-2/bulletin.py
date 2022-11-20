import rsa


class Bulletin:
    def __init__(self, voter_fake_id: int, choice: bytes):
        self.choice = choice
        self.voter_fake_id = voter_fake_id

        self.cvk_sign = 'sign'
        self.cvk_pubkey = 'cvk_pubkey'
