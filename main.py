import random
from public_key import PublicKey
from curves import Generator, Point, Curve

bitcoin_curve = Curve(
	p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
	a=0x0000000000000000000000000000000000000000000000000000000000000000,
	b=0x0000000000000000000000000000000000000000000000000000000000000007
)

G = Point(
	bitcoin_curve,
	x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
	y=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)

bitcoin_gen = Generator(
	G=G,
	n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)

secret_key = random.randrange(1, bitcoin_gen.n)
assert 1 <= secret_key < bitcoin_gen.n

public_key = secret_key * G
address = PublicKey.from_point(public_key).address(net='test', compressed=True)

print("Our first Bitcoin identity:")
print("1. secret key: ", secret_key)
print("2. public key: ", (public_key.x, public_key.y))
print("3. Bitcoin address: ", address)
