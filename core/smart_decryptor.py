from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class SmartDecryptor:
    def __init__(self):
        """初始化 SmartDecryptor"""
        self.config = {
            "aes": {
                "key": "0123456789abcdef",
                "iv": "0123456789abcdef"
            },
            "base64": {},
            "custom": {}
        }

    def decrypt_aes(self, cipher_text, key, iv):
        """AES 解密"""
        cipher = Cipher(
            algorithms.AES(key.encode()),
            modes.CBC(iv.encode()),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(cipher_text) + decryptor.finalize()
        return plaintext.decode().strip()

    def decrypt_base64(self, cipher_text):
        """Base64 解密"""
        return b64decode(cipher_text).decode()

    def decrypt_custom(self, cipher_text):
        """自定义解密逻辑（示例：反转字符串）"""
        return cipher_text[::-1]

    def decrypt(self, cipher_text, method="base64"):
        """根据指定方法解密密文"""
        method_config = self.config.get(method, {})
        if not method_config:
            raise ValueError(f"未找到解密方法: {method}")

        if method == "aes":
            return self.decrypt_aes(cipher_text, method_config["key"], method_config["iv"])
        elif method == "base64":
            return self.decrypt_base64(cipher_text)
        elif method == "custom":
            return self.decrypt_custom(cipher_text)
        else:
            raise NotImplementedError(f"未实现解密方法: {method}")