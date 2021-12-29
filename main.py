import random
from public_key import PublicKey
from curves import Generator, Point, Curve
from tx import TxIn, Script, TxOut, Tx
from ecdsa import Signature, sign
from sha256 import sha256
from bitcoin import BITCOIN

secret_key = random.randrange(1, BITCOIN.gen.n)
assert 1 <= secret_key < BITCOIN.gen.n

public_key = secret_key * BITCOIN.gen.G
address = PublicKey.from_point(public_key).address(net='test', compressed=True)

print("Our first Bitcoin identity:")
print("1. secret key: ", secret_key)
print("2. public key: ", (public_key.x, public_key.y))
print("3. Bitcoin address: ", address)

secret_key2 = random.randrange(1, BITCOIN.gen.n)
assert 1 <= secret_key2 < BITCOIN.gen.n
public_key2 = secret_key2 * BITCOIN.gen.G
address2 = PublicKey.from_point(public_key2).address(net='test', compressed=True)

print("Our second Bitcoin identity:")
print("1. secret key: ", secret_key2)
print("2. public key: ", (public_key2.x, public_key2.y))
print("3. Bitcoin address: ", address2)

tx_in = TxIn(
    prev_tx = bytes.fromhex('5541463879b28a408166555ec5350f3db7a98d4b80ee8e6483ccffc860ed2b2e'),
    prev_index = 0,
    script_sig = None
)

tx_out1 = TxOut(amount = 3000)
tx_out2 = TxOut(amount = 4550)

out1_pkb_hash = PublicKey.from_point(public_key2).encode(compressed=True, hash160=True)
out1_script = Script([118, 169, out1_pkb_hash, 136, 172])
print(out1_script.encode().hex())

out2_pkb_hash = PublicKey.from_point(public_key).encode(compressed=True, hash160=True)
out2_script = Script([118, 169, out2_pkb_hash, 136, 172])
print(out2_script.encode().hex())

tx_out1.script_pubkey = out1_script
tx_out2.script_pubkey = out2_script

tx = Tx(
    version = 1,
    tx_ins = [tx_in],
    tx_outs = [tx_out1, tx_out2],
)

source_script = Script([118, 169, out2_pkb_hash, 136, 172])
print("recall out2_pkb_hash is just raw bytes of the hash of public_key: ", out2_pkb_hash.hex())

tx_in.prev_tx_script_pubkey = source_script

message = tx.encode(sig_index = 0)

random.seed(int.from_bytes(sha256(message), 'big')) # see note below
sig = sign(secret_key, message)
sig_bytes = sig.encode()

sig_bytes_and_type = sig_bytes + b'\x01'
pubkey_bytes = PublicKey.from_point(public_key).encode(compressed=True, hash160=False)
script_sig = Script([sig_bytes_and_type, pubkey_bytes])
tx_in.script_sig = script_sig

print("Transaction size in bytes: ", len(tx.encode()))
print(tx)
print(tx.encode().hex())