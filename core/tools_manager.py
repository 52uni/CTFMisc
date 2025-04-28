import json
import subprocess
import os
import webbrowser
from tkinter import messagebox


class ToolsManager:
    def __init__(self):
        self.tools_data = self.load_tools_from_json()

    @staticmethod
    def load_tools_from_json():
        """从 JSON 文件加载工具数据"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, "tools_config.json")

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("未找到工具配置文件 tools_config.json！")
        except json.JSONDecodeError:
            raise ValueError("工具配置文件格式错误，请检查 JSON 格式！")

    def get_tool_config(self, tool_name):
        """获取工具配置"""
        for category_data in self.tools_data:
            for tool in category_data["tools"]:
                if tool["name"] == tool_name:
                    return tool
        return None

    @staticmethod
    def run_command(cmd):
        """运行命令行工具"""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout or result.stderr

    @staticmethod
    def open_eve_file(file_path):
        try:
            # 去除路径中的引号
            file_path = file_path.strip('"')
            if os.path.isabs(file_path):
                full_path = file_path
            else:
                project_root = os.getcwd()
                full_path = os.path.join(project_root, file_path)

            if os.name == 'nt':
                os.startfile(full_path)
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', full_path])
        except Exception as e:
            messagebox.showerror("错误", f"打开EVE文件 {full_path} 时出错: {e}")


    @staticmethod
    def open_html_file(file_path):
        try:
            webbrowser.open_new_tab(file_path)
        except Exception as e:
            messagebox.showerror("错误", f"在浏览器中打开HTML文件 {file_path} 时出错: {e}")