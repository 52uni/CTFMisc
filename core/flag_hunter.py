# import re
# from PIL import Image
# import pytesseract
#
# class FlagHunter:
#     def __init__(self):
#         """初始化 FlagHunter"""
#         self.patterns = [
#             r"flag\{.*?\}",  # 标准 flag 格式
#             r"[0-9a-fA-F]{32}"  # 常见 MD5 格式
#         ]
#
#     def extract_from_text(self, content):
#         """从文本内容中提取 flag"""
#         flags = []
#         for pattern in self.patterns:
#             matches = re.findall(pattern, content)
#             if matches:
#                 flags.extend(matches)
#         return flags
#
#     def extract_from_image(self, image_path):
#         """从图片中提取 flag（OCR）"""
#         try:
#             img = Image.open(image_path)
#             text = pytesseract.image_to_string(img)
#             return self.extract_from_text(text)
#         except Exception as e:
#             print(f"图片处理失败: {e}")
#             return []
#
#     def hunt_flag(self, file_path):
#         """根据文件类型提取 flag"""
#         try:
#             if file_path.lower().endswith(('.txt', '.log')):
#                 with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#                     content = f.read()
#                 return self.extract_from_text(content)
#
#             elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
#                 return self.extract_from_image(file_path)
#
#             else:
#                 print(f"不支持的文件类型: {file_path}")
#                 return []
#         except Exception as e:
#             print(f"文件处理失败: {e}")
#             return []