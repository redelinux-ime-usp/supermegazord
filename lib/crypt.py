from Crypto.Cipher import AES
import hashlib
import base64

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

def encrypt(string, key):
	cipher = AES.new(hashlib.sha256(key).digest())
	b64encoded = pad(base64.b64encode(string))
	return base64.b64encode(cipher.encrypt(b64encoded))

def decrypt(data, key):
	cipher = AES.new(hashlib.sha256(key).digest())
	b64encoded = cipher.decrypt(base64.b64decode(data))
	return base64.b64decode(b64encoded.rstrip(PADDING))
