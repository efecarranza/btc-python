from dataclasses import dataclass
from typing import List, Union
from sha256 import sha256

def encode_int(i, nbytes, encoding='little'):
    return i.to_bytes(nbytes, encoding)

def encode_varint(i):
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + encode_int(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + encode_int(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + encode_int(i, 8)
    else:
        raise ValueError("Integer too large: %d" % (i, ))

@dataclass
class Script:
    cmds: List[Union[int, bytes]]

    def encode(self):
        out = []
        for cmd in self.cmds:
            if isinstance(cmd, int):
                out += [encode_int(cmd, 1)]
            elif isinstance(cmd, bytes):
                length = len(cmd)
                assert length < 75
                out += [encode_int(length, 1), cmd]

        ret = b''.join(out)
        return encode_varint(len(ret)) + ret

@dataclass
class TxIn:
    prev_tx: bytes
    prev_index: int
    script_sig: Script = None
    sequence: int = 0xffffffff

    def encode(self, script_override=None):
        out = []
        out += [self.prev_tx[::-1]]
        out += [encode_int(self.prev_index, 4)]

        if script_override is None:
            out += [self.script_sig.encode()]
        elif script_override is True:
            out += [self.prev_tx_script_pubkey.encode()]
        elif script_override is False:
            out += [Script([]).encode()]
        else:
            raise ValueError("script_override must be one of None|True|False")

        out += [encode_int(self.sequence, 4)]
        return b''.join(out)

@dataclass
class TxOut:
    amount: int
    script_pubkey: Script = None

    def encode(self):
        out = []
        out += [encode_int(self.amount, 8)]
        out += [self.script_pubkey.encode()]
        return b''.join(out)

@dataclass
class Tx:
    version: int
    tx_ins: List[TxIn]
    tx_outs: List[TxOut]
    locktime: int = 0

    def tx_id(self) -> str:
        return sha256(sha256(self.encode()))[::-1].hex()

    def encode(self, sig_index=-1) -> bytes:
        out = []
        out += [encode_int(self.version, 4)]
        out += [encode_varint(len(self.tx_ins))]
        if sig_index == -1:
            out += [tx_in.encode() for tx_in in self.tx_ins]
        else:
            out += [tx_in.encode(script_override=(sig_index == i))
                    for i, tx_in in enumerate(self.tx_ins)]
        out += [encode_varint(len(self.tx_outs))]
        out += [tx_out.encode() for tx_out in self.tx_outs]
        out += [encode_int(self.locktime, 4)]
        out += [encode_int(1, 4) if sig_index != -1 else b''] # 1 = SIGHASH_ALL
        return b''.join(out)
