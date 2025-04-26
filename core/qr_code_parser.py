from pyzbar.pyzbar import decode
from PIL import Image


class QRCodeParser:
    @staticmethod
    def parse(file_path):
        """解析二维码文件"""
        decoded_objects = decode(Image.open(file_path))

        if decoded_objects:
            qr_data = "\n".join([obj.data.decode("utf-8") for obj in decoded_objects])
            return f"二维码解析完成:\n{qr_data}"
        else:
            return "未能从图片中解析出二维码内容！"