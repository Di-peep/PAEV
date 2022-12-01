class Bulletin:
    def __init__(self, register_code: int, choice, sign, pubkey):
        self.register_code = register_code
        self.choice = choice
        self.sign = sign
        self.pubkey = pubkey
