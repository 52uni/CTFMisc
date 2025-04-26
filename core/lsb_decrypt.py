import struct
import binascii
from PIL import Image
import os
import logging

# CTF专用日志（带格式标签）
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(format)s] %(message)s',
    datefmt='%H:%M:%S'
)


class LSBDecrypter:
    @staticmethod
    def _load_image(file_path):
        """加载图片，返回图片对象或 None"""
        try:
            if not os.path.exists(file_path):
                logging.error(f"文件 {file_path} 不存在。", extra={'format': 'UNKNOWN'})
                return None

            with open(file_path, 'rb') as f:
                header = f.read(8)

            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                fmt = 'png'
            elif header.startswith((b'\xff\xd8', b'\xff\xd9')):
                fmt = 'jpeg'
            elif header.startswith(b'RIFF') and header[8:12] == b'WEBP':
                fmt = 'webp'
            elif header.startswith(b'BM'):
                fmt = 'bmp'
            else:
                logging.error(f"未知文件类型: {header[:8].hex()}", extra={'format': 'UNKNOWN'})
                return None

            image = Image.open(file_path)
            logging.info(f"成功加载 {fmt.upper()} 文件: {file_path}", extra={'format': fmt.upper()})
            return image

        except FileNotFoundError:
            logging.error(f"文件 {file_path} 未找到。", extra={'format': 'UNKNOWN'})
        except Exception as e:
            logging.error(f"加载图片时出现未知错误: {str(e)}", extra={'format': 'UNKNOWN'})
        return None

    @staticmethod
    def _binary_to_text(binary_message):
        """将二进制字符串转换为文本消息"""
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            if len(byte) == 8:
                char = chr(int(byte, 2))
                if char.isprintable():
                    message += char
                else:
                    break  # 停止在第一个不可打印字符处
        return message.strip()

    @staticmethod
    def decrypt(file_path):
        """对 LSB 隐写图片进行解密"""
        image = LSBDecrypter._load_image(file_path)
        if not image:
            return "无法解密，图片未成功加载。"
        width, height = image.size
        pixels = image.load()
        binary_message = ""
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y][:3]  # Ensure we only get R, G, B channels
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)
        return LSBDecrypter._binary_to_text(binary_message)

    @staticmethod
    def check_file_header(file_path):
        """检查文件头是否正确"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(10)
                header_hex = binascii.hexlify(header).decode()
                if file_path.lower().endswith('.png'):
                    return LSBDecrypter._check_png_header(header_hex)
                elif file_path.lower().endswith(('.jpg', '.jpeg')):
                    return LSBDecrypter._check_jpeg_header(header_hex)
                elif file_path.lower().endswith('.webp'):
                    return LSBDecrypter._check_webp_header(header_hex)
                elif file_path.lower().endswith('.bmp'):
                    return LSBDecrypter._check_bmp_header(header_hex)
                return "未知文件类型，无法检查文件头。"
        except FileNotFoundError:
            logging.error(f"文件 {file_path} 未找到。", extra={'format': 'UNKNOWN'})
            return f"错误: 文件 {file_path} 未找到。"
        except Exception as e:
            logging.error(f"检查文件头时出现未知错误: {str(e)}", extra={'format': 'UNKNOWN'})
            return f"错误: 检查文件头时出现未知错误 {e}。"

    @staticmethod
    def _check_png_header(header_hex):
        """检查 PNG 文件头"""
        if header_hex.startswith('89504e47'):
            return "PNG 文件头正常。"
        return "PNG 文件头异常。"

    @staticmethod
    def _check_jpeg_header(header_hex):
        """检查 JPEG 文件头"""
        if header_hex.startswith('ffd8'):
            return "JPEG 文件头正常。"
        return "JPEG 文件头异常。"

    @staticmethod
    def _check_webp_header(header_hex):
        """检查 WebP 文件头"""
        if header_hex.startswith('52494646'):
            return "WebP 文件头正常。"
        return "WebP 文件头异常。"

    @staticmethod
    def _check_bmp_header(header_hex):
        """检查 BMP 文件头"""
        if header_hex.startswith('424d'):
            return "BMP 文件头正常。"
        return "BMP 文件头异常。"

    @staticmethod
    def decrypt_block_lsb(file_path, block_size=10):
        """分块进行 LSB 解密"""
        image = LSBDecrypter._load_image(file_path)
        if not image:
            return "无法进行分块解密，图片未成功加载。"
        width, height = image.size
        pixels = image.load()
        all_messages = []
        for block_y in range(0, height, block_size):
            for block_x in range(0, width, block_size):
                binary_message = ""
                for y in range(block_y, min(block_y + block_size, height)):
                    for x in range(block_x, min(block_x + block_size, width)):
                        r, g, b = pixels[x, y][:3]  # Ensure we only get R, G, B channels
                        binary_message += str(r & 1)
                        binary_message += str(g & 1)
                        binary_message += str(b & 1)
                message = LSBDecrypter._binary_to_text(binary_message)
                all_messages.append(message)
        return ''.join(all_messages)

    @staticmethod
    def fix_file_header(file_path, correct_header):
        """修复文件头"""
        try:
            with open(file_path, 'rb+') as f:
                f.seek(0)
                f.write(binascii.unhexlify(correct_header))
            return "文件头修复成功"
        except FileNotFoundError:
            logging.error(f"文件 {file_path} 未找到。", extra={'format': 'UNKNOWN'})
            return f"错误: 文件 {file_path} 未找到。"
        except Exception as e:
            logging.error(f"文件头修复失败: {str(e)}", extra={'format': 'UNKNOWN'})
            return f"文件头修复失败: {e}"





