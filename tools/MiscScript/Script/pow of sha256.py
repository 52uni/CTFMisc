import hashlib
import itertools

prefix = "NdYpTGA"
sha256_value = "79283cb6eb54a99d5dcb0a134f49a4138a34f68a800055ecd56fd7ceab04b4df"

for c1, c2, c3, c4 in itertools.product("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", repeat=4):
    guess = prefix + c1 + c2 + c3 + c4
    guess_sha256 = hashlib.sha256(guess.encode()).hexdigest()
    print(guess)
    if guess_sha256 == sha256_value:
        print(f"Found the solution: {guess}")
        exit(0)
print("Failed to solve PoW.")
