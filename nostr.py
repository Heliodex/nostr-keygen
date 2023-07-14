import secrets
import secp256k1Crypto
import bech32
from multiprocessing import Process # This can of worms can't be closed now
# import threading
import socket

port = 7654

class PublicKey:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw_bytes = raw_bytes

        self.bech32 = bech32.bech32_encode("npub", bech32.convertbits(self.raw_bytes, 8, 5), "BECH32")

        self.hex = self.raw_bytes.hex()


class PrivateKey:
    def __init__(self) -> None:
        raw_secret = secrets.token_bytes(32)

        self.public_key = PublicKey(secp256k1Crypto.PrivateKey(
            raw_secret).pubkey.serialize()[1:])
        
        self.bech32 = bech32.bech32_encode(
            "nsec", bech32.convertbits(raw_secret, 8, 5), "BECH32")

        self.hex = raw_secret.hex()

threads = 48

def printKey(iter: int, priv: PrivateKey, pubBech: str, pubHex: str, rank: int):
    text = (
        f"RANK {rank}: {iter} iterations" +
        f"\n\tPrivate Key:     {priv.bech32}" +
        f"\n\tPrivate Key Hex: {priv.hex}" +
        f"\n\tPublic Key:      {pubBech}" +
        f"\n\tPublic Key Hex:  {pubHex}" +
        "\n"
    )
    print(text)

    # send to server, on specified port
    if port:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", port))
        sock.sendall(text.encode())
        sock.close()


def check(string: str):
    for i in range(len(string), 0, -1):
        if string.count(string[0]) == len(string):
            break
        string = string[:i]
    return len(string)


def generate(n):
    try:
        for i in range(n, 10**20, threads):
            priv = PrivateKey()
            key = priv.public_key
            bech = key.bech32
            hex = key.hex

            if i % 10000 == 0:
                print(i)

            rank = check(bech[5:]) + check(hex)
            if rank > 8:
                printKey(i, priv, bech, hex, rank)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
	for i in range(threads):
		t = Process(target=generate, args=(i,))
		t.start()
		# t = threading.Thread(target=generate, args=(i,))
		# t.start()
