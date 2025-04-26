import os


class FileHandler:
    def __init__(self):
        self.file_path = None
        self.file_content = None

    def load_file(self, file_path):
        """加载文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError("文件不存在！")

        with open(file_path, 'rb') as file:
            content = file.read()

        try:
            self.file_content = content.decode('utf-8')
        except UnicodeDecodeError:
            self.file_content = content  # 存储二进制内容

        self.file_path = file_path

    # def decrypt(self):
    #     """智能解密"""
    #     if isinstance(self.file_content, str):
    #         return f"解密结果: {self.file_content[::-1]}"
    #     else:
    #         raise ValueError("当前文件为二进制文件，无法进行解密操作！")

    @staticmethod
    def get_file_icon():
        """加载文件图标"""
        # 这里可以使用 PIL 或其他库加载图标
        from PIL import Image, ImageTk
        img = Image.open(os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "file_icon.png"))
        img = img.resize((32, 32))
        return ImageTk.PhotoImage(img)