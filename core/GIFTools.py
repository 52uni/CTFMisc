from PIL import Image, ImageSequence
import os
import subprocess


class GIFSeparator:
    @staticmethod
    def separate(file_path):
        """分离 GIF 为单帧图片"""
        output_dir = "D:/tools/CTFMisc/output/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            gif = Image.open(file_path)
            for i, frame in enumerate(ImageSequence.Iterator(gif)):
                frame_path = os.path.join(output_dir, f"frame_{i}.png")
                frame.save(frame_path)

            # 自动打开生成的目录文件夹
            GIFSeparator.open_folder(output_dir)

            return f"GIF 分离完成，单帧图片保存至 {output_dir}"
        except Exception as e:
            return f"分离 GIF 时出错: {e}"

    @staticmethod
    def open_folder(folder_path):
        """根据系统类型打开文件夹"""
        if os.name == 'nt':  # Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # Linux
            subprocess.Popen(['xdg-open', folder_path])
        else:  # macOS
            subprocess.Popen(['open', folder_path])


# class GIFFramerateAdjuster:
#     @staticmethod
#     def adjust_framerate(file_path, new_framerate):
#         """调整 GIF 的帧率"""
#         output_dir = "D:/tools/CTFMisc/output/"
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#
#         output_path = os.path.join(output_dir, "adjusted_framerate.gif")
#         try:
#             gif = Image.open(file_path)
#             frames = []
#             durations = []
#             for frame in ImageSequence.Iterator(gif):
#                 frames.append(frame.copy())
#                 # 获取原帧持续时间
#                 duration = frame.info.get('duration', 100)
#                 # 根据新帧率计算新的持续时间
#                 new_duration = int(1000 / new_framerate)
#                 durations.append(new_duration)
#
#             frames[0].save(output_path, save_all=True, append_images=frames[1:],
#                            duration=durations, loop=0)
#
#             # 自动打开生成的目录文件夹
#             GIFSeparator.open_folder(output_dir)
#
#             return f"GIF 帧率调整完成，新文件保存至 {output_path}"
#         except Exception as e:
#             return f"调整 GIF 帧率时出错: {e}"


# class GIFMerger:
#     @staticmethod
#     def merge(frame_paths):
#         """将一系列单帧图片合并成 GIF"""
#         output_dir = "D:/tools/CTFMisc/output/"
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#
#         output_path = os.path.join(output_dir, "merged.gif")
#         try:
#             frames = []
#             for path in frame_paths:
#                 frame = Image.open(path)
#                 frames.append(frame)
#
#             frames[0].save(output_path, save_all=True, append_images=frames[1:],
#                            duration=100, loop=0)
#
#             # 自动打开生成的目录文件夹
#             GIFSeparator.open_folder(output_dir)
#
#             return f"GIF 合并完成，新文件保存至 {output_path}"
#         except Exception as e:
#             return f"合并 GIF 时出错: {e}"


# class GIFFrameExtractor:
#     @staticmethod
#     def extract_frame(file_path, frame_index):
#
#         output_dir = "D:/tools/CTFMisc/output/"
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#
#         output_path = os.path.join(output_dir, f"extracted_frame_{frame_index}.png")
#         try:
#             gif = Image.open(file_path)
#             frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
#             if 0 <= frame_index < len(frames):
#                 frames[frame_index].save(output_path)
#
#                 # 自动打开生成的目录文件夹
#                 GIFSeparator.open_folder(output_dir)
#
#                 return f"GIF 第 {frame_index} 帧提取完成，保存至 {output_path}"
#             else:
#                 return f"指定的帧索引 {frame_index} 超出范围，GIF 总帧数为 {len(frames)}"
#         except Exception as e:
#             return f"提取 GIF 帧时出错: {e}"