#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, transactions):
    """
        k - Number of trailing zeros in the binary representation (integer)
        prev_hash - the hash of the previous block (bytes)
        rand_lines - a set of "transactions," i.e., data to be included in this block (list of strings)

        Complete this function to find a nonce such that 
        sha256( prev_hash + rand_lines + nonce )
        has k trailing zeros in its *binary* representation
    """
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'

    # TODO your code to find a nonce here
    # Prepare the data to be hashed (prev_hash + all transactions)
    data = prev_hash
    for tx in transactions:
        data += tx.encode('utf-8')
    
    # Start with nonce = 0 and increment until it finds a valid one
    nonce = 0
    while True:
        # Convert nonce to bytes (little endian)
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, 'little') or b'\x00'
        
        # Compute the hash
        h = hashlib.sha256(data + nonce_bytes)
        hash_bytes = h.digest()  # Get the hash as bytes
        
        # Convert hash to binary string and check trailing zeros
        binary_hash = bin(int.from_bytes(hash_bytes, 'big'))[2:]  # [2:] to remove '0b' prefix
        
        # Pad with leading zeros to ensure full 256 bits
        binary_hash = binary_hash.zfill(256)
        
        # Check if we have at least k trailing zeros
        if binary_hash[-k:] == '0' * k:
            return nonce_bytes
        
        # Increment nonce for next attempt
        nonce += 1

    assert isinstance(nonce, bytes), 'nonce should be of type bytes'
    return nonce


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 20

    transactions = get_random_lines(filename, num_lines)
    nonce = mine_block(diff, transactions)
    print(nonce)
