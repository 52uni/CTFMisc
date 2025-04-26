import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox

from core.GIFTools import GIFSeparator
from core.barcode_parser import BarcodeParser
from core.file_handler import FileHandler
from core.flag_analyzer import FlagDecryptor
from core.image_dimension_restoration import CTFImageFixer
from core.lsb_decrypt import LSBDecrypter
from core.qr_code_parser import QRCodeParser
from core.tools_manager import ToolsManager


class MainUI:
    def __init__(self, root):
        """
        初始化主界面
        :param root: 主窗口对象
        """
        self.root = root
        self.root.title("CTFMisc-by-UniMao")
        self.root.geometry("1200x800")
        self.root.configure(bg='white')

        # 核心模块实例化
        self.file_handler = FileHandler()
        self.qr_code_parser = QRCodeParser()
        self.bar_code_parser = BarcodeParser()
        self.tools_manager = ToolsManager()
        self.GIF_Separator = GIFSeparator()
        self.decrypt_lsb = LSBDecrypter()
        self.DimensionRestorer_Image = CTFImageFixer()

        # 设置全局样式
        self.set_global_style()

        # 创建主布局
        self.create_main_layout()

    def set_global_style(self):
        """设置全局样式"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='white', foreground='black', font=('黑体', 10))
        style.configure('TButton', background='#0078D4', foreground='white', font=('黑体', 10, 'bold'))
        style.map('TButton', background=[('active', '#005EB8')])

    def create_main_layout(self):
        """创建主界面布局"""
        # 左侧：工具栏和文件加载框
        left_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 文件加载框
        load_frame = ttk.Frame(left_frame, padding="10", relief="groove", borderwidth=2, style='TFrame')
        load_frame.pack(fill=tk.X, pady=10)

        # 文件图标
        img = self.file_handler.get_file_icon()
        file_icon_label = ttk.Label(load_frame, image=img, background='white')
        file_icon_label.image = img
        file_icon_label.pack(side=tk.LEFT, padx=10)

        # 文件路径显示
        file_info_frame = ttk.Frame(load_frame, style='TFrame')
        file_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(file_info_frame, text="当前文件:", font=('黑体', 10, 'bold')).pack(anchor=tk.W)
        self.file_path_label = ttk.Label(file_info_frame, text="未选择文件", font=('Arial', 10), foreground='gray')
        self.file_path_label.pack(anchor=tk.W, pady=5)

        # 加载文件按钮
        load_file_button = ttk.Button(load_frame, text="选择文件", command=self.load_file, style='TButton')
        load_file_button.pack(side=tk.RIGHT, padx=10)

        # 输出框
        output_label = ttk.Label(left_frame, text="输出:", font=('Arial', 10, 'bold'))
        output_label.pack(anchor=tk.W, pady=5)
        self.output_box = scrolledtext.ScrolledText(left_frame, height=20, wrap=tk.WORD, state=tk.DISABLED,
                                                    font=('黑体', 10))
        self.output_box.pack(fill=tk.BOTH, expand=True, pady=5)

        # 功能按钮
        button_frame = ttk.Frame(left_frame, padding="5", style='TFrame')
        button_frame.pack(fill=tk.X, pady=10)

        get_flag_button = ttk.Button(button_frame, text="一键获取 Flag", command=self.get_flag, style='TButton')
        get_flag_button.pack(side=tk.LEFT, padx=5)

        # decrypt_button = ttk.Button(button_frame, text="智能解密", command=self.smart_decrypt, style='TButton')
        # decrypt_button.pack(side=tk.LEFT, padx=5)

        # 右侧：工具树
        right_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 创建工具树
        self.tool_tree = self.create_tool_tree(right_frame)
        self.tool_tree.pack(fill=tk.BOTH, expand=True)

        # 自动展开所有节点
        self.expand_all_nodes(self.tool_tree)

    def create_tool_tree(self, parent):
        """
        创建工具树
        :param parent: 父容器
        :return: Tool Tree 对象
        """
        tool_tree = ttk.Treeview(parent, columns=("description"), show="tree")
        tool_tree.heading("#0", text="工具名称", anchor=tk.W)
        tool_tree.column("#0", width=200, anchor=tk.W)
        tool_tree.heading("description", text="描述", anchor=tk.W)
        tool_tree.column("description", width=400, anchor=tk.W)

        # 插入工具数据
        tools_data = self.tools_manager.load_tools_from_json()
        for category_data in tools_data:
            category_name = category_data["category"]
            category_id = tool_tree.insert("", "end", text=category_name, open=True)
            for tool in category_data["tools"]:
                tool_name = tool["name"]
                tool_desc = tool.get("description", "无描述")
                tool_tree.insert(category_id, "end", text=tool_name, values=(tool_desc,), tags=("tool",))

        # 绑定双击事件
        tool_tree.tag_bind("tool", "<Double-1>", self.on_tool_double_click)

        return tool_tree

    def expand_all_nodes(self, tree, parent=""):
        """
        递归展开 Treeview 中的所有节点
        :param tree: Treeview 对象
        :param parent: 当前父节点 ID
        """
        children = tree.get_children(parent)
        for child in children:
            tree.item(child, open=True)
            self.expand_all_nodes(tree, child)

    def on_tool_double_click(self, event):
        """
        处理工具双击事件
        """
        try:
            tree = event.widget
            item = tree.selection()[0]
            tool_name = tree.item(item, "text")

            # 获取工具类型并执行
            tool_config = self.tools_manager.get_tool_config(tool_name)
            if not tool_config:
                messagebox.showerror("错误", f"未找到工具 {tool_name} 的配置！")
                return

            tool_type = tool_config.get("type", "command")
            if tool_type == "image_analysis":
                if tool_name == "二维码解析":
                    self.update_output("正在解析二维码，请稍候...")
                    threading.Thread(target=self.parse_qr_code).start()
                else:
                    self.update_output("正在解析条形码,请稍后...")
                    threading.Thread(target=self.parse_bar_code).start()

            elif tool_type == "GIF":
                if tool_name == "GIF分离":
                    self.update_output("GIF正在分离，请稍候...")
                    threading.Thread(target=self.Separator_GIF()).start()

            elif tool_type == "DR":
                if tool_name == "图片宽高恢复":
                    self.update_output("图片宽高正在恢复，请稍候...")
                    threading.Thread(target=self.Image_DR()).start()

            elif tool_type == "Lsb":
                if tool_name == "Lsb隐写查看":
                    self.update_output("lsb隐写查看中，请稍候...")
                    threading.Thread(target=self.Decrypt_Lsb()).start()

            elif tool_type == "command":
                output = self.tools_manager.run_command(tool_config.get("cmd", ""))
                self.update_output(output)

            elif tool_type == "open_eve_file":
                file_path = tool_config.get("cmd")
                if file_path:
                    self.tools_manager.open_eve_file(file_path)
                    self.update_output(f"正在打开 {tool_name} 的EVE文件...")
                else:
                    messagebox.showerror("错误", f"工具 {tool_name} 的EVE文件路径未配置！")
                # 这里需要实现打开eve文件的具体逻辑

            else:
                messagebox.showwarning("警告", f"未知工具类型: {tool_type}")
        except IndexError:
            messagebox.showerror("错误", "未选择任何工具！")

    def Separator_GIF(self):
        """分离 GIF 为单帧图片"""
        if not self.file_handler.file_path:
            self.update_output("未选择有效的GIF图片文件！")
            return
    #
        try:
            result = self.GIF_Separator.separate(self.file_handler.file_path)
            self.update_output(result)
        except Exception as e:
            self.update_output(f"解析失败: {e}")

    def Decrypt_Lsb(self):
        """分离 GIF 为单帧图片"""
        if not self.file_handler.file_path:
            self.update_output("未选择有效的GIF图片文件！")
            return
    #
        try:
            result = self.decrypt_lsb.decrypt_block_lsb(self.file_handler.file_path)
            self.update_output(result)
        except Exception as e:
            self.update_output(f"解析失败: {e}")

    def Image_DR(self):
        """分离 GIF 为单帧图片"""
        if not self.file_handler.file_path:
            self.update_output("未选择有效的GIF图片文件！")
            return
    #
        try:
            result = self.DimensionRestorer_Image.auto_fix(self.file_handler.file_path)
            self.update_output(result)
        except Exception as e:
            self.update_output(f"解析失败: {e}")

    def parse_qr_code(self):
        """解析二维码文件"""
        if not self.file_handler.file_path:
            self.update_output("未选择有效的二维码图片文件！")
            return

        try:
            result = self.qr_code_parser.parse(self.file_handler.file_path)
            self.update_output(result)
        except Exception as e:
            self.update_output(f"二维码解析失败: {e}")

    def parse_bar_code(self):
        """解析条形码"""
        if not self.file_handler.file_path:
            self.update_output("未选择有效的条形码图片文件！")
            return

        try:
            result = self.bar_code_parser.parse(self.file_handler.file_path)
            self.update_output(result)
        except Exception as e:
            self.update_output(f"条形码解析失败: {e}")

    def load_file(self):
        """加载文件"""
        file_path = filedialog.askopenfilename(title="选择文件")
        if not file_path:
            return

        try:
            self.file_handler.load_file(file_path)
            self.file_path_label.config(text=os.path.basename(file_path), foreground='black')
            self.update_output(f"文件已加载：{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"文件加载失败: {e}")


    def get_flag(self):
        """一键获取 Flag"""
        try:
            flag = FlagDecryptor.get_flag(self.file_handler.file_content)
            self.update_output(flag)
        except Exception as e:
            messagebox.showwarning("警告", str(e))

    def smart_decrypt(self):
        """智能解密"""
        try:
            decrypted_text = FlagDecryptor.smart_decrypt(self.file_handler.file_content)
            self.update_output(decrypted_text)
        except Exception as e:
            messagebox.showwarning("警告", str(e))

    def update_output(self, text):
        """更新输出框内容"""
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)
        self.output_box.config(state=tk.DISABLED)