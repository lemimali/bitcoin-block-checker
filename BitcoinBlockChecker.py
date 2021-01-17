#!/usr/bin/python

# Program that verifies if a hash of a bitcoin block is acceptable or not.
# Program calculates the hash and checks if it matches with the hash the block creator has sent.
# It also checks if creators hash value is equal or smaller than target bits value.
# Program needs block's hash as a parameter to make the needed work. Best way to get a hash is to go to
# blockchain.com's explorer section and choose a block from there. Then copy hash value from block's info page.

import urllib.request, json, sys
from urllib.error import HTTPError
from hashlib import sha256
from binascii import unhexlify

# Converting value to little endian format.
def little_endian(line):
    array = [line[i:i + 2] for i in range(0, len(line), 2)]
    array.reverse()
    return "".join(array)

# Checking that user has given a hash.
if(len(sys.argv) < 2):
    print("Give a hash to identify what block you want to check.\nFor example: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
    sys.exit()

# Finding wanted block data in JSON format.
try:
    with urllib.request.urlopen(
            "https://blockchain.info/rawblock/" + sys.argv[1]) as url:
        data = json.loads(url.read().decode())
except HTTPError as error:
    print("Given hash value was not valid. Try again...")
    sys.exit()

# Collecting needed information from JSON object:
print("# Calculating values for Block " + str(data["height"]))
# Version number
array = bytearray(data["ver"].to_bytes(4, "big"))
version_number = little_endian(bytes(array).hex())

# Previous block hash
prev_block_hash = little_endian(data["prev_block"])

# Merkle root
mrkl_root = little_endian(data["mrkl_root"])

# Timestamp
timestamp = little_endian(hex(data["time"])[2:])

# Bits
bits = little_endian(hex(data["bits"])[2:])

# Nonce value
nonce = hex(int(0x100000000) + data["nonce"])[-8:]
nonce = little_endian(nonce)

# Calculating the hash value
# Append all parameters
all_params = version_number + prev_block_hash + mrkl_root + timestamp + bits + nonce

# Get double SHA-256 value
all_params = unhexlify(all_params)
calculated_hash = little_endian(sha256(sha256(all_params).digest()).hexdigest())
block_hash = data["hash"]

# Printing values.
print(">>> Original hash value:   " + block_hash)
print(">>> Calculated hash value: " + calculated_hash)

# Checking if the calculated hash matches with the one the block creator has sent.
print("# Checking if the calculated hash matches with the one the block creator has sent...")
if calculated_hash == block_hash:
    print(">>> Success! Hash values match!")
else:
    print(">>> Failed... Hash values don't match.")

# Checking that block creators hashs value is smaller than the target value (bits).
print("# Checking that block creators hashs value is smaller than the target value (Bits)...")
if data["hash"] <= bits:
    print(">>> Success! Block creator's hash value is smaller than bits.")
else:
    print(">>> Failed... Block creator's hash value is not smaller than bits.")
