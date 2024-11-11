
import os
import sys

# Add the src directory to the path so we can import crypto_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from crypto_utils.key_management import generate_keys
from crypto_utils import (
    derive_shared_key,
    encrypt_data,
    decrypt_data,
    encrypt_large_file,
    reassemble_file_from_chunks,
    encrypt_chunk,
    decrypt_chunk,
    encrypt_file_to_array,
    reconstruct_file_from_array
)

def test_satellite_communication():
    # Generate keys for Satellite A and Satellite B using satellite names
    generate_keys("SatelliteA")
    generate_keys("SatelliteB")
    
    # Derive shared keys from Satellite A's private key and Satellite B's public key, and vice versa
    shared_key_A_to_B = derive_shared_key("keys/SatelliteA_private_key.pem", "keys/SatelliteB_public_key.pem")
    shared_key_B_to_A = derive_shared_key("keys/SatelliteB_private_key.pem", "keys/SatelliteA_public_key.pem")
    
    # Check that both derived keys are identical
    assert shared_key_A_to_B == shared_key_B_to_A, "Shared keys between satellites do not match!"

    # Encrypt a message from Satellite A to Satellite B
    message_from_A = b"Message from Satellite A"
    encrypted_message_from_A = encrypt_data(message_from_A, shared_key_A_to_B)
    
    # Satellite B decrypts the message
    decrypted_message_at_B = decrypt_data(encrypted_message_from_A, shared_key_B_to_A)
    assert decrypted_message_at_B == message_from_A, "Decrypted message at Satellite B does not match the original message!"

    # Encrypt a message from Satellite B to Satellite A
    message_from_B = b"Reply from Satellite B"
    encrypted_message_from_B = encrypt_data(message_from_B, shared_key_B_to_A)
    
    # Satellite A decrypts the message
    decrypted_message_at_A = decrypt_data(encrypted_message_from_B, shared_key_A_to_B)
    assert decrypted_message_at_A == message_from_B, "Decrypted message at Satellite A does not match the original message!"
    
    print("Satellite communication test passed successfully!")

def test_large_file_encryption():
    # Use a random AES key for testing large file encryption
    shared_key = os.urandom(32)

    # Prepare a large test file
    test_file = "test_large_file.txt"
    with open(test_file, "wb") as f:
        f.write(os.urandom(5 * 1024 * 1024))  # 5 MB test file

    # Encrypt and split the large file
    encrypted_chunks_dir = "encrypted_chunks"
    encrypt_large_file(test_file, shared_key, encrypted_chunks_dir, chunk_size=1024 * 512)  # 512 KB chunks

    # Reassemble and decrypt the file
    reassembled_file = "reassembled_test_large_file.txt"
    reassemble_file_from_chunks(reassembled_file, encrypted_chunks_dir, shared_key)

    # Verify that the reassembled file matches the original
    with open(test_file, "rb") as original, open(reassembled_file, "rb") as reassembled:
        assert original.read() == reassembled.read(), "Reassembled file does not match the original file!"

    # Clean up files
    os.remove(test_file)
    os.remove(reassembled_file)
    for chunk_file in os.listdir(encrypted_chunks_dir):
        os.remove(os.path.join(encrypted_chunks_dir, chunk_file))
    os.rmdir(encrypted_chunks_dir)

    print("Large file encryption test passed successfully!")

def test_non_chunked_encryption():
    # Use a random AES key for testing
    shared_key = os.urandom(32)

    # Prepare a test file
    test_file = "test_file.txt"
    with open(test_file, "wb") as f:
        f.write(b"This is a test file content for non-chunked encryption.")

    # Read file data and encrypt without chunking
    with open(test_file, "rb") as f:
        data = f.read()
    encrypted_data = encrypt_data(data, shared_key)

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, shared_key)

    # Verify that decrypted data matches original
    assert decrypted_data == data, "Decrypted data does not match the original content!"

    # Clean up files
    os.remove(test_file)

    print("Non-chunked encryption test passed successfully!")

def test_individual_chunk_encryption():
    # Use a random AES key for testing chunk encryption
    shared_key = os.urandom(32)

    # Prepare individual chunks as byte arrays
    chunk1 = b"This is the first chunk of data."
    chunk2 = b"This is the second chunk of data."

    # Encrypt each chunk individually
    encrypted_chunk1 = encrypt_chunk(chunk1, shared_key)
    encrypted_chunk2 = encrypt_chunk(chunk2, shared_key)

    # Decrypt each chunk individually
    decrypted_chunk1 = decrypt_chunk(*encrypted_chunk1, shared_key)
    decrypted_chunk2 = decrypt_chunk(*encrypted_chunk2, shared_key)

    # Verify that decrypted chunks match the original chunks
    assert decrypted_chunk1 == chunk1, "Decrypted chunk1 does not match the original chunk1!"
    assert decrypted_chunk2 == chunk2, "Decrypted chunk2 does not match the original chunk2!"

    print("Individual chunk encryption test passed successfully!")

def test_array_encryption_and_reconstruction():
    # Use a random AES key for testing
    shared_key = os.urandom(32)

    # Prepare a test file
    test_file = "test_array_file.txt"
    with open(test_file, "wb") as f:
        f.write(b"This is a large test file for array encryption and reconstruction.")

    # Encrypt the file into an array of chunks
    encrypted_chunks = encrypt_file_to_array(test_file, shared_key, chunk_size=16)  # Small chunk size for test

    # Reconstruct the file from the encrypted chunks
    reconstructed_file = "reconstructed_array_file.txt"
    reconstruct_file_from_array(encrypted_chunks, reconstructed_file, shared_key)

    # Verify that the reconstructed file matches the original
    with open(test_file, "rb") as original, open(reconstructed_file, "rb") as reconstructed:
        assert original.read() == reconstructed.read(), "Reconstructed file does not match the original file!"

    # Clean up files
    os.remove(test_file)
    os.remove(reconstructed_file)

    print("Array encryption and reconstruction test passed successfully!")

# Run the tests
if __name__ == "__main__":
    test_satellite_communication()
    test_large_file_encryption()
    test_non_chunked_encryption()
    test_individual_chunk_encryption()
    test_array_encryption_and_reconstruction()
