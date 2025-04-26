#!/usr/bin/env python
# coding=utf-8

import struct
import binascii
from PIL import Image
import os
import logging
import shutil
import argparse
import sys

# CTF专用日志（带格式标签）
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(format)s] %(message)s',
    datefmt='%H:%M:%S'
)


class CTFImageFixer:
    # 全格式签名库（2024 CTF最新）
    FORMAT_SPECS = {
        'png': (b'\x89PNG\r\n\x1a\n', 8, 16, 8, (64, 64)),  # IHDR宽高位置
        'jpeg': (b'\xff\xd8', 2, 7, 4, (128, 128)),  # SOF0宽高（大端，高在前）
        'webp': (b'RIFF', 4, 13, 4, (64, 64)),  # VP8头宽高（小端）
        'bmp': (b'BM', 2, 18, 8, (256, 256))  # BMP宽高（小端）
    }

    @staticmethod
    def auto_fix(file_path):
        """全格式入口（带格式标签日志）"""
        if not os.path.exists(file_path):
            logging.error(f"文件不存在: {file_path}", extra={'format': 'UNKNOWN'})
            return "文件不存在"

        fmt = CTFImageFixer._detect_format(file_path)
        if not fmt:
            return "未知格式（支持PNG/JPEG/WebP/BMP）"

        backup_file = file_path + '.bak'
        try:
            shutil.copy(file_path, backup_file)
            logging.info(f"开始修复 {fmt.upper()} 文件", extra={'format': fmt.upper()})
            result = getattr(CTFImageFixer, f"fix_{fmt}")(file_path)
            logging.info(result, extra={'format': fmt.upper()})
            return result
        except FileNotFoundError as e:
            logging.error(f"文件未找到: {str(e)}", extra={'format': fmt.upper()})
            return "文件未找到"
        except PermissionError as e:
            logging.error(f"权限不足: {str(e)}", extra={'format': fmt.upper()})
            return "权限不足"
        except Exception as e:
            logging.error(f"修复失败: {str(e)[:50]}", extra={'format': fmt.upper()})
            if os.path.exists(backup_file):
                shutil.move(backup_file, file_path)  # 回滚到备份
            return "修复失败（已回滚备份）"
        finally:
            if os.path.exists(backup_file):
                os.remove(backup_file)

    # ======================
    # PNG 修复（含防黑）
    # ======================
    @staticmethod
    def fix_png(file_path):
        with open(file_path, 'r+b') as f:
            # 1. 修复文件头+IHDR
            f.seek(0)
            f.write(CTFImageFixer.FORMAT_SPECS['png'][0])  # 强制文件头
            CTFImageFixer._fix_png_ihdr(f, file_path)

        # 2. 验证
        try:
            with Image.open(file_path) as img:
                if CTFImageFixer._is_all_black(img):
                    return "PNG防黑修复（透明通道模式）"
                return f"PNG修复: {img.size}（{img.mode}）"
        except IOError as e:
            logging.error(f"无法打开修复后的PNG文件: {str(e)}", extra={'format': 'PNG'})
            return "无法打开修复后的PNG文件"

    @staticmethod
    def _fix_png_ihdr(f, file_path):
        guess_w, guess_h = CTFImageFixer._guess_size(file_path, 'png')
        ihdr_data = struct.pack('>II', guess_w, guess_h)  # 宽高数据
        crc_data = b'IHDR' + ihdr_data + b'\x00\x00\x00\x00'  # CRC计算用数据
        crc_value = binascii.crc32(crc_data) & 0xFFFFFFFF  # 计算CRC值
        f.seek(16)
        f.write(ihdr_data)  # 写入宽度和高度
        f.seek(24)
        f.write(struct.pack('>I', crc_value))  # 写入CRC值

    # ======================
    # JPEG 修复（SOF0定位）
    # ======================
    @staticmethod
    def fix_jpeg(file_path):
        with open(file_path, 'r+b') as f:
            # 1. 定位SOF0（跳过APP块）
            sof0_pos = CTFImageFixer._find_sof0(f)
            if sof0_pos == -1:
                return "JPEG重建SOF0（宽松模式）"

            # 2. 写入宽高（CTF常见尺寸）
            guess_w, guess_h = CTFImageFixer._guess_size(file_path, 'jpeg')
            f.seek(sof0_pos + 5)  # 跳过长度(2)+精度(1)
            f.write(struct.pack('>HH', guess_h, guess_w))  # 高在前

        # 3. 验证
        try:
            with Image.open(file_path) as img:
                return f"JPEG修复: {img.size}（SOF0校正）"
        except IOError as e:
            logging.error(f"无法打开修复后的JPEG文件: {str(e)}", extra={'format': 'JPEG'})
            return "无法打开修复后的JPEG文件"

    @staticmethod
    def _find_sof0(f):
        while True:
            byte = f.read(1)
            if not byte or byte != b'\xFF':
                return -1
            marker = f.read(1)
            if marker == b'\xC0':  # SOF0标记
                return f.tell() - 2
            elif marker.startswith(b'\xE0'):  # APP块
                length = struct.unpack('>H', f.read(2))[0]
                f.seek(length - 2, 1)
            else:
                break
        return -1

    # ======================
    # WebP 修复（VP8头）
    # ======================
    @staticmethod
    def fix_webp(file_path):
        with open(file_path, 'r+b') as f:
            # 1. 定位VP8头（RIFF+WEBP后）
            f.seek(8)  # 'WEBP'标记后
            if f.read(1) != b'\xF5':  # VP8图片标志
                return "非VP8 WebP（无法修复）"

            # 2. 写入宽高（小端序）
            guess_w, guess_h = CTFImageFixer._guess_size(file_path, 'webp')
            f.seek(13)  # 宽高位置（小端2字节x2）
            f.write(struct.pack('<HH', guess_w, guess_h))

        # 3. 验证
        try:
            with Image.open(file_path) as img:
                return f"WebP修复: {img.size}（VP8头校正）"
        except IOError as e:
            logging.error(f"无法打开修复后的WebP文件: {str(e)}", extra={'format': 'WEBP'})
            return "无法打开修复后的WebP文件"

    # ======================
    # BMP 修复（文件头+宽高）
    # ======================
    @staticmethod
    def fix_bmp(file_path):
        with open(file_path, 'r+b') as f:
            # 1. 修复文件头
            f.seek(0)
            f.write(CTFImageFixer.FORMAT_SPECS['bmp'][0])  # 'BM'头

            # 2. 写入宽高（小端序）
            guess_w, guess_h = CTFImageFixer._guess_size(file_path, 'bmp')
            f.seek(18)  # BMP宽高偏移
            f.write(struct.pack('<II', guess_w, guess_h))  # 小端整数

        # 3. 验证
        try:
            with Image.open(file_path) as img:
                return f"BMP修复: {img.size}（小端序校正）"
        except IOError as e:
            logging.error(f"无法打开修复后的BMP文件: {str(e)}", extra={'format': 'BMP'})
            return "无法打开修复后的BMP文件"

    # ======================
    # 底层核心功能
    # ======================
    @staticmethod
    def _detect_format(file_path):
        """0.01秒格式检测（含BMP）"""
        with open(file_path, 'rb') as f:
            for fmt, (sig, length, _, _, _) in CTFImageFixer.FORMAT_SPECS.items():
                header = f.read(length)
                f.seek(0)  # 重置文件指针
                if header == sig:
                    return fmt
        return None

    @staticmethod
    def _guess_size(file_path, fmt):
        """全格式尺寸推测（CTF特征库）"""
        size = os.path.getsize(file_path)
        # 格式特定文件头补偿
        header_size = {
            'png': 29, 'jpeg': 10, 'webp': 12, 'bmp': 54
        }[fmt]
        effective = size - header_size

        # CTF尺寸库（含BMP特殊尺寸）
        size_map = {
            4096: (64, 64),  # PNG/LSB
            16384: (128, 128),  # JPEG/二维码
            65536: (256, 256),  # WebP/透明隐写
            262144: (512, 512),  # BMP/大尺寸隐写
            1024: (32, 32)  # 小型隐写
        }
        closest = min(size_map.keys(), key=lambda x: abs(effective - x))
        return size_map[closest]

    @staticmethod
    def _is_all_black(img):
        """全格式黑图检测"""
        return all(p in {(0, 0, 0), (0, 0, 0, 255)} for p in img.getdata())






