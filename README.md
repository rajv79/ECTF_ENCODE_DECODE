
## Encryption Algorithm
The encoder uses AES-256 (Advanced Encryption Standard) in CFB (Cipher Feedback) mode for encryption. AES-256 is a widely recognized and secure symmetric encryption algorithm. The key size is 256 bits (32 bytes), and the initialization vector (IV) is 16 bytes.

## Key Features of AES-256 CFB:
Symmetric Encryption: The same key is used for both 2 time encryption .

## CFB Mode: This mode turns the block cipher into a stream cipher, allowing encryption of data in smaller chunks without padding.

## IV (Initialization Vector): A random 16-byte IV is generated for each encryption operation to ensure that the same plaintext produces different ciphertexts each time.

## Encryption Process
The encoder follows these steps to encrypt the frame:

Input Validation:

The frame input is checked to ensure it does not exceed 64 bytes.

The Channel ID is packed into 4 bytes, and the Timestamp is packed into 8 bytes.

## Encryption:

The frame is encrypted using AES-256 in CFB mode.

A 16-byte IV is generated for each encryption operation.

The IV is prepended to the encrypted data to allow decryption.

Size Constraints:

The encrypted frame is checked to ensure it does not exceed 64 bytes.

The final encoded frame consists of:

Header: 4 bytes (Channel ID) + 8 bytes (Timestamp).

Encrypted Frame: Up to 64 bytes.

## Output:

The encoded frame is returned as a byte string.


## ------------------------------------------------------------------

## How to Test the Encoder

python3 encoder.py secrets_vivek.json <channel> "<frame>" <timestamp>

secrets_vivek.json: Path to the secrets_vivek file.

<channel>: Channel ID (e.g., 2).

"<frame>": Frame content as a string (e.g., "vivek raj").

<timestamp>: Timestamp (e.g., 3)


## Example :

python3 encoder.py secrets_vivek.json 2 "vivek raj" 3


## output :
b'\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00O\x07p\xee\x1d\x01\x11GO.9j\xad\x80\x1c:T\xd8\x97\xefF\xedI\xdeB'
