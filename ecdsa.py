import random

from dataclasses import dataclass
from curves import Point, inv
from sha256 import sha256
from bitcoin import BITCOIN

@dataclass
class Signature:
    r: int
    s: int

    def encode(self) -> bytes:
        """ return the DER encoding of this signature """

        def dern(n):
            nb = n.to_bytes(32, byteorder='big')
            nb = nb.lstrip(b'\x00') # strip leading zeros
            nb = (b'\x00' if nb[0] >= 0x80 else b'') + nb # preprend 0x00 if first byte >= 0x80
            return nb

        rb = dern(self.r)
        sb = dern(self.s)
        content = b''.join([bytes([0x02, len(rb)]), rb, bytes([0x02, len(sb)]), sb])
        frame = b''.join([bytes([0x30, len(content)]), content])
        return frame

def sign(secret_key: int, message: bytes) -> Signature:
    n = BITCOIN.gen.n

    z = int.from_bytes(sha256(sha256(message)), 'big')

    sk = random.randrange(1, n)
    P = sk * BITCOIN.gen.G

    r = P.x
    s = inv(sk, n) * (z + secret_key * r) % n
    if s > n / 2:
        s = n - s

    sig = Signature(r, s)
    return sig

def verify(public_key: Point, message: bytes, sig: Signature) -> bool:
    # just a stub for reference on how a signature would be verified in terms of the API
    # we don't need to verify any signatures to craft a transaction, but we would if we were mining
    pass