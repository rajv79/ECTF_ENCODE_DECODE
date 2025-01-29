"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import argparse
import struct
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class Encoder:
    def __init__(self, secrets: bytes):
        """
        You **may not** change the arguments or returns of this function!

        :param secrets: Contents of the secrets file generated by
            ectf25_design.gen_secrets
        """
        # Load the json of the secrets file
        secrets = json.loads(secrets)

        # Load the example secrets for use in Encoder.encode
        # This will be a 16-byte (128-bit) hex-encoded key
        self.key = bytes.fromhex(secrets["some_secrets"])  # Convert hex to bytes
        
        
        

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts the input data using AES-128 in CFB mode.
        Prepends the IV (Initialization Vector) to the encrypted data.
        """
         # 16-byte IV for AES
        iv = os.urandom(16) 
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        # IV + encrypted data
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return iv + encrypted_data  
    
     # 16-byte IV for AES
    
    
   
    

    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """
        The frame encoder function.

        This will be called for every frame that needs to be encoded before being
        transmitted by the satellite to all listening TVs.

        You **may not** change the arguments or returns of this function!

        :param channel: 16b unsigned channel number. Channel 0 is the emergency
            broadcast that must be decodable by all channels.
        :param frame: Frame to encode. Max frame size is 64 bytes.
        :param timestamp: 64b timestamp to use for encoding. **NOTE**: This value may
            have no relation to the current timestamp, so you should not compare it
            against the current time. The timestamp is guaranteed to strictly
            monotonically increase (always go up) with subsequent calls to encode.

        :returns: The encoded frame, which will be sent to the Decoder.
        """
        # Ensure the frame size does not exceed 64 bytes
        if len(frame) > 64:
            raise ValueError("Frame size must not exceed 64 bytes.")

        # Pack the channel (4 bytes) and timestamp (8 bytes)
        header = struct.pack("<IQ", channel, timestamp)

        # Encrypt the frame (max 64 bytes)
        encrypted_frame = self.encrypt(frame)

        # Ensure the encrypted frame does not exceed 64 bytes
        if len(encrypted_frame) > 64:
            raise ValueError("Encrypted frame size must not exceed 64 bytes.")

        # Combine the header and encrypted frame
        encoded_frame = header + encrypted_frame

        return encoded_frame


def main():
    """A test main to one-shot encode a frame

    This function is only for your convenience and will not be used in the final design.

    After pip-installing, you should be able to call this with:
        python3 -m ectf25_design.encoder path/to/test.secrets 1 "frame to encode" 100
    """
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument(
        "secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file"
    )
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64b timestamp to use")
    args = parser.parse_args()

    encoder = Encoder(args.secrets_file.read())
    print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


if __name__ == "__main__":
    main()
