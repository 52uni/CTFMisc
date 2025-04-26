import hashlib
import string

prefix = "NdYpTGA"
md5_value = "823c6f55577c412bca496010bcea0d4e"
char=string.ascii_lowercase+string.digits

for c1 in char:
    for c2 in char:
        for c3 in char:
            for c4 in char:
                guess = prefix + str(c1) + str(c2) + str(c3) + str(c4)
                print(guess)
                guess_md5 = hashlib.md5(guess.encode()).hexdigest()
                if guess_md5 == md5_value:
                    print(f"Found the solution: {guess}")
                    exit(0)
print("Failed to solve PoW.")
