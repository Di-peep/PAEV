import rsa


def elgamal_sign():
    msg = str('secret').encode("utf-8")
    pubkey, privkey = rsa.newkeys(512)
    signature = rsa.sign(msg, privkey, 'SHA-1')
    return pubkey, signature


def check_sign(pubkey, signature):
    msg = str('secret').encode("utf-8")
    try:
        rsa.verify(msg, signature, pubkey)
        return True
    except rsa.pkcs1.VerificationError:
        print('-! Невалідний підпис бюлетеня')
        return False


if __name__ == '__main__':
    s = elgamal_sign()
    print("This is an illusion =(")
