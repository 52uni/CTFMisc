def caesar_cipher_decrypt(ciphertext, key):
    """
    凯撒密码解密函数，接受密文和密钥，并返回解密后的明文
    """
    plaintext = ""
    for c in ciphertext:
        if c.isalpha():
            # 将字符转换为 ASCII 码，并减去密钥
            new_char = ord(c) - key
            # 处理超出字母表范围的字符
            if c.isupper():
                if new_char < ord('A'):
                    new_char += 26
                elif new_char > ord('Z'):
                    new_char -= 26
            elif c.islower():
                if new_char < ord('a'):
                    new_char += 26
                elif new_char > ord('z'):
                    new_char -= 26
            # 将 ASCII 码转换回字符，并添加到明文字符串中
            plaintext += chr(new_char)
        else:
            plaintext += c
    return plaintext


def caesar_cipher_brute_force(ciphertext):
    """
    凯撒密码暴力破解函数，接受密文，并枚举所有可能的密钥并尝试解密消息
    """
    for i in range(26):
        print(f"Key: {i}, Plaintext: {caesar_cipher_decrypt(ciphertext, i)}")
        
ciphertext = "RPQLD JDOOLD HVWGLYLVD LQ SDUWHV WUHV"
caesar_cipher_brute_force(ciphertext)
