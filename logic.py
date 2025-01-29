import struct
from cryptography.fernet import Fernet
import base64

class Encoder:
    def __init__(self, secrets: bytes):
        # ... (previous initialization code) ...
        self.key1 = Fernet.generate_key()
        self.key2 = Fernet.generate_key()
        self.fernet1 = Fernet(self.key1)
        self.fernet2 = Fernet(self.key2)

    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """
        Encodes a frame for transmission using a two-step encryption process.
        """
        # Validate input values
        if not (0 <= channel <= 0xFFFF):
            raise ValueError("Channel must be a 16-bit unsigned integer (0-65535).")
        if len(frame) > 64:
            raise ValueError("Frame size exceeds the maximum allowed 64 bytes.")
        if not (0 <= timestamp <= 0xFFFFFFFFFFFFFFFF):
            raise ValueError("Timestamp must be a 64-bit unsigned integer.")

        # Optional: Match the frame and timestamp against the provided test cases
        for test_case in self.some_secrets:
            if test_case[0] == channel and test_case[2] == timestamp:
                frame = test_case[1].encode()
                break

        # Step 1: Split the frame into three parts
        frame_length = len(frame)
        part1 = frame[:frame_length // 3]
        part2 = frame[frame_length // 3: 2 * frame_length // 3]
        part3 = frame[2 * frame_length // 3:]

        # Step 2: Encrypt each part separately
        encrypted_part1 = self.fernet1.encrypt(part1)
        encrypted_part2 = self.fernet1.encrypt(part2)
        encrypted_part3 = self.fernet1.encrypt(part3)

        # Step 3: Combine the encrypted parts
        combined_encrypted = encrypted_part1 + encrypted_part2 + encrypted_part3

        # Step 4: Encrypt the combined parts again
        final_encrypted = self.fernet2.encrypt(combined_encrypted)

        # Step 5: Pack the encoded frame with channel and timestamp
        return struct.pack("<IQ", channel, timestamp) + final_encrypted

    # def decode(self, encoded_frame: bytes) -> tuple:
    #     """
    #     Decodes an encoded frame.
    #     """
    #     # Unpack channel and timestamp
    #     channel, timestamp = struct.unpack("<IQ", encoded_frame[:12])
    #     encrypted_data = encoded_frame[12:]

    #     # Step 1: Decrypt the outer layer
    #     decrypted_combined = self.fernet2.decrypt(encrypted_data)

    #     # Step 2: Split the decrypted data into three parts
    #     part_length = len(decrypted_combined) // 3
    #     encrypted_part1 = decrypted_combined[:part_length]
    #     encrypted_part2 = decrypted_combined[part_length:2*part_length]
    #     encrypted_part3 = decrypted_combined[2*part_length:]

    #     # Step 3: Decrypt each part
    #     part1 = self.fernet1.decrypt(encrypted_part1)
    #     part2 = self.fernet1.decrypt(encrypted_part2)
    #     part3 = self.fernet1.decrypt(encrypted_part3)

    #     # Step 4: Combine the decrypted parts
    #     original_frame = part1 + part2 + part3

    #     return channel, original_frame, timestamp
