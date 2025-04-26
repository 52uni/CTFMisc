from pyzbar.pyzbar import decode
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BarcodeParser:
    @staticmethod  # 保持静态方法
    def parse(file_path, allowed_types=None):
        """线程安全的解析方法（已修复调用问题）"""

        """
        解析条形码文件（支持UPC/EAN/Code128等20+种格式）

        :param file_path: 图片文件路径（支持PNG/JPEG/BMP）
        :param allowed_types: 允许的条形码类型列表（如['UPC-A', 'EAN-13']），None表示所有类型
        :return: 解析结果字符串（含类型和数据）或错误信息
        """
        try:
            # 1. 验证文件类型
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                return "错误：仅支持PNG/JPEG/BMP格式图片"

            # 2. 解析图片
            img = Image.open(file_path)
            decoded = decode(img)

            # 3. 过滤无效结果
            results = []
            for obj in decoded:
                barcode_type = obj.type
                barcode_data = obj.data.decode('utf-8', errors='replace')

                # 类型过滤
                if allowed_types and barcode_type not in allowed_types:
                    logger.info(f"跳过不允许的类型: {barcode_type}")
                    continue

                # 数据校验（针对常见条形码的长度校验）
                if BarcodeParser._validate_barcode(barcode_type, barcode_data):
                    results.append(f"类型: {barcode_type}, 数据: {barcode_data}")
                else:
                    logger.warning(f"无效数据: {barcode_type}({barcode_data})")

            # 4. 结果输出
            if results:
                return "\n".join([f"✅ {res}" for res in results])
            return "未检测到有效条形码（支持类型: UPC-A/EAN-13/Code128等20+种）"

        except FileNotFoundError:
            return "错误：文件不存在"
        except Exception as e:
            logger.error(f"解析失败: {str(e)}")
            return f"解析失败: {str(e)[:50]}..."

    @staticmethod
    def _validate_barcode(barcode_type, data):
        """常见条形码数据格式校验（CTF场景优化）"""
        validators = {
            'UPC-A': lambda d: len(d) == 12 and d.isdigit(),
            'EAN-13': lambda d: len(d) == 13 and d.isdigit(),
            'CODE128': lambda d: len(d) <= 8192,  # 标准最大长度
            'CODABAR': lambda d: set(d).issubset({'0123456789-$:/.+abcdABCD'}),
            'PDF417': lambda d: len(d) <= 1850,  # 典型长度
        }
        validator = validators.get(barcode_type, lambda _: True)
        return validator(data.strip())
