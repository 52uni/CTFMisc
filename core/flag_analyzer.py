import re
import base64
from enum import Enum, auto
import logging
from collections import Counter
import struct
from io import BytesIO
from itertools import zip_longest

# 可选依赖检测
try:
    from PIL import Image, ExifTags

    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    logging.warning("Pillow未安装，图片处理功能受限")

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 枚举定义
class FileType(Enum):
    UNKNOWN = auto()
    PNG = auto()
    JPEG = auto()
    PDF = auto()
    ELF = auto()


class EncryptionType(Enum):
    PLAIN = auto()
    XOR = auto()
    BASE64 = auto()
    CAESAR = auto()
    ROT47 = auto()
    RAIL_FENCE = auto()
    BACON = auto()
    BINARY = auto()


class FlagDecryptor:
    def __init__(self, file_content):
        self.raw_bytes = self._preprocess(file_content)
        self.file_type = self._detect_file_type()
        self.encryption_pipeline = [("初始状态", self._get_debug_content())]
        self.final_flag = "未找到Flag"

    # 基础处理
    @staticmethod
    def _preprocess(content):
        """预处理：统一转换为字节"""
        if isinstance(content, str):
            return content.encode('utf-8', errors='replace')
        if isinstance(content, bytes):
            return content
        raise ValueError("仅支持字节或字符串输入")

    def _detect_file_type(self):
        """魔数检测文件类型"""
        head = self.raw_bytes[:20]
        if head.startswith(b'\x89PNG\r\n\x1a\n'): return FileType.PNG
        if head.startswith(b'\xff\xd8\xff'): return FileType.JPEG
        if head.startswith(b'%PDF-'): return FileType.PDF
        if len(head) >= 4 and head[:4] == b'\x7fELF': return FileType.ELF
        return FileType.UNKNOWN

    def _get_debug_content(self, max_len=200):
        """获取调试用内容片段"""
        return self.raw_bytes.decode('utf-8', errors='replace')[:max_len] + '...'

    # 二进制文件处理
    def _process_binary_file(self):
        """二进制文件深度处理（隐写+元数据）"""
        if self.file_type in (FileType.PNG, FileType.JPEG) and HAS_PIL:
            self.raw_bytes += self._extract_image_lsb().encode()
            self.raw_bytes += self._extract_image_metadata().encode()
        if self.file_type == FileType.PDF:
            self.raw_bytes += self._extract_pdf_comments().encode()
        if self.file_type == FileType.ELF:
            self.raw_bytes += self._extract_elf_strings().encode()
        self.encryption_pipeline.append(("二进制处理后", self._get_debug_content()))

    # 隐写提取
    def _extract_image_lsb(self, depth=1):
        """LSB隐写提取（1-3位）"""
        if not HAS_PIL: return ""
        try:
            img = Image.open(BytesIO(self.raw_bytes))
            pixels = img.getdata()
            bits = []
            for p in pixels:
                if isinstance(p, int):  # 单色图
                    bits.extend([(p >> i) & 1 for i in range(depth)])
                else:  # RGB/A
                    for c in p:
                        bits.extend([(c >> i) & 1 for i in range(depth)])
            return self._bits_to_str(bits)
        except Exception as e:
            logger.debug(f"LSB提取失败: {e}")
            return ""

    @staticmethod
    def _bits_to_str(bits):
        """二进制位转字符串"""
        return ''.join([
            chr(int(''.join(map(str, bits[i:i + 8])), 2))
            for i in range(0, len(bits), 8)
        ]) if len(bits) >= 8 else ""

    def _extract_image_metadata(self):
        """EXIF元数据提取"""
        if not HAS_PIL: return ""
        try:
            img = Image.open(BytesIO(self.raw_bytes))
            exif = img.getexif()
            if not exif: return ""
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag, '').lower() in ['usercomment', 'comment']:
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='replace')
                    if 'flag' in value.lower():
                        return value.strip()
            return ""
        except Exception as e:
            logger.debug(f"元数据解析失败: {e}")
            return ""

    def _extract_pdf_comments(self):
        """PDF注释提取"""
        try:
            pdf_text = self.raw_bytes.decode('latin-1', errors='replace')
            return '\n'.join(re.findall(r'%%[Cc]omment: (.*?)\n', pdf_text))
        except Exception as e:
            logger.debug(f"PDF解析失败: {e}")
            return ""

    def _extract_elf_strings(self):
        """ELF文件字符串提取"""
        try:
            if len(self.raw_bytes) < 0x40: return ""
            e_shoff = struct.unpack('<I', self.raw_bytes[0x28:0x2c])[0]
            e_shnum = struct.unpack('<H', self.raw_bytes[0x36:0x38])[0]
            e_shentsize = struct.unpack('<H', self.raw_bytes[0x3a:0x3c])[0]
            e_shstrndx = struct.unpack('<H', self.raw_bytes[0x3e:0x40])[0]
            sh_strtab = self.raw_bytes[e_shoff + e_shstrndx * e_shentsize:]
            return self._extract_printable(sh_strtab)
        except Exception as e:
            logger.debug(f"ELF解析失败: {e}")
            return ""

    @staticmethod
    def _extract_printable(data, min_len=4):
        """提取可打印字符串"""
        return ''.join([
            chr(b) for i, b in enumerate(data)
            if 32 <= b <= 126 and all(
                32 <= data[j] <= 126 for j in range(i, min(i + min_len, len(data)))
            )
        ])

    # 加密算法
    def _run_decryption_pipeline(self):
        """按优先级执行解密链"""
        decryptors = [
            ('base64', self._base64_decrypt),
            ('rot47', self._rot47_decrypt),
            ('xor', self._xor_decrypt),
            ('rail_fence', self._rail_fence_decrypt),
            ('bacon', self._bacon_decrypt),
            ('caesar', self._caesar_decrypt),
        ]
        for name, decryptor in decryptors:
            if decryptor():
                self.encryption_pipeline.append((f"解密: {name}", self._get_debug_content()))

    def _base64_decrypt(self):
        """智能Base64解密（支持URL安全/补等号）"""
        content = self.raw_bytes.decode(errors='replace')
        if not (('=' in content) and set(content).issubset(
                set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='))):
            return False
        try:
            self.raw_bytes = base64.b64decode(content.replace('\n', ''))
            return True
        except:
            try:
                self.raw_bytes = base64.urlsafe_b64decode(content)
                return True
            except:
                return False

    def _rot47_decrypt(self):
        """ROT47解密（ASCII 33-126）"""
        if sum(1 for b in self.raw_bytes if 33 <= b <= 126) < len(self.raw_bytes) * 0.5:
            return False
        self.raw_bytes = bytes([
            33 + ((b - 33 + 47) % 94) if 33 <= b <= 126 else b
            for b in self.raw_bytes
        ])
        return True

    def _xor_decrypt(self, max_keys=256):
        """单字节异或爆破"""
        content = self.raw_bytes.decode(errors='replace')
        for key in range(1, max_keys + 1):
            decrypted = ''.join(chr(ord(c) ^ key) for c in content)
            if self._has_flag_like(decrypted):
                self.raw_bytes = decrypted.encode()
                return True
        return False

    def _rail_fence_decrypt(self):
        """栅栏密码解密（2-5层）"""
        content = self.raw_bytes.decode(errors='replace')
        for rails in range(2, 6):
            try:
                decrypted = self._rail_fence_decode(content, rails)
                if self._has_flag_like(decrypted):
                    self.raw_bytes = decrypted.encode()
                    return True
            except:
                continue
        return False

    @staticmethod
    def _rail_fence_decode(cipher, rails):
        """栅栏密码逆向"""
        rail = [[] for _ in range(rails)]
        direction = -1
        row = 0
        for i, c in enumerate(cipher):
            if row == 0 or row == rails - 1:
                direction *= -1
            rail[row].append(c)
            row += direction
        return ''.join([c for r in rail for c in r])

    def _bacon_decrypt(self):
        """培根密码解密（A=0, B=1，5位一组）"""
        content = self.raw_bytes.decode(errors='replace').upper()
        bits = []
        for c in content:
            if c == 'A':
                bits.append('0')
            elif c == 'B':
                bits.append('1')
        if len(bits) % 5 != 0:
            return False
        binary = ''.join(bits[i:i + 5] for i in range(0, len(bits), 5))
        if len(binary) % 8 != 0:
            return False
        self.raw_bytes = bytes(int(binary[i:i + 8], 2) for i in range(0, len(binary), 8))
        return bool(binary)

    def _caesar_decrypt(self):
        """凯撒密码解密（自动移位）"""
        content = self.raw_bytes.decode(errors='replace').lower()
        freq = Counter(c for c in content if c.isalpha())
        if not freq:
            return False
        most_common = freq.most_common(1)[0][0]
        shift = (ord(most_common) - ord('e')) % 26
        decrypted = ''.join([
            chr((ord(c) - shift - 97) % 26 + 97) if c.islower() else
            chr((ord(c) - shift - 65) % 26 + 65) if c.isupper() else c
            for c in content
        ])
        if self._has_flag_like(decrypted):
            self.raw_bytes = decrypted.encode()
            return True
        return False

    # Flag提取
    _flag_patterns = [
        re.compile(r'flag\{[^}]+\}', re.IGNORECASE),
        re.compile(r'fl4g\{[^}]+\}', re.IGNORECASE),
        re.compile(r'[fF][lL][aA@4][gG]\{[^}]+\}', re.IGNORECASE),
    ]

    def _has_flag_like(self, content):
        """快速Flag特征检测"""
        return any(pattern.search(content) for pattern in self._flag_patterns)

    def _finalize_flag(self, content):
        """最终Flag格式化"""
        candidates = []
        for line in content.split('\n'):
            for pattern in self._flag_patterns:
                match = pattern.search(line)
                if match:
                    candidates.append(match.group().strip())
        if candidates:
            return f"Flag: {candidates[0]}"
        legacy = re.findall(r'\b(flag|fl4g|f1ag|FLAG)[^ ]{6,}', content, re.IGNORECASE)
        return f"疑似Flag: {legacy[0]}" if legacy else "未找到Flag"

    # 主流程
    def smart_decrypt(self):
        """全流程解密（含步骤追踪）"""
        # 1. 二进制文件预处理
        self._process_binary_file()

        # 2. 加密算法解密
        self._run_decryption_pipeline()

        # 3. 最终提取
        self.final_flag = self._finalize_flag(self.raw_bytes.decode('utf-8', errors='replace'))

        # 4. 生成报告
        return self._generate_process_report()

    def _generate_process_report(self):
        """生成带步骤的解密报告"""
        report = ["### 解密流程追踪："]
        for step, content in self.encryption_pipeline:
            report.append(f"• {step}:")
            report.append(f"  ├─ 内容片段: {content}")
            report.append(f"  └─ 完整长度: {len(self.raw_bytes)}字节")
        report.append(f"\n### 最终结果：{self.final_flag}")
        return '\n'.join(report)

    # 入口方法
    @classmethod
    def get_flag(cls, file_content):
        """统一入口（兼容字节/字符串）"""
        if not file_content:
            raise ValueError("文件内容为空")
        try:
            decryptor = cls(file_content)
            return decryptor.smart_decrypt()
        except Exception as e:
            return f"解密失败: {str(e)}"
