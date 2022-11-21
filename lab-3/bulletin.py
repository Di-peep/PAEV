class Bulletin:
    def __init__(
            self,
            register_code: int,
            voter_fake_id: int,
            choice: bytes
    ):
        self.choice = choice
        self.voter_fake_id = voter_fake_id
        self.register_code = register_code

        self.sign = 'sign'
        self.sign_key = 'key'
