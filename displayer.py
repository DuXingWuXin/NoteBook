import os
import sys
import tkinter as tk
from tkinter import ttk
import database as db
import birthday_win as bir_win
import account_win as acc_win



# 获取当前目录
def get_executable_path():
    # 可执行文件
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # 代码
    else:
        return os.path.dirname(os.path.abspath(__file__))



if __name__ == '__main__':

    db.createTable_database()

    root_width = 700
    root_height = 500
    menu_width = int(root_width * 0.2)

    base_path = get_executable_path()
    logo_ico_path = os.path.join(base_path, 'resources', 'logo.ico')
    logo_img_path = os.path.join(base_path, 'resources', 'logo.png')
    birthday_img_path = os.path.join(base_path, 'resources', 'birthday.png')
    account_img_path = os.path.join(base_path, 'resources', 'account.png')

    # 窗口
    root = tk.Tk()
    root.title('记事本')
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    x = int((screenwidth - root_width) / 2)
    y = int((screenheight - root_height) / 2)
    root.geometry('{}x{}+{}+{}'.format(root_width, root_height, x, y))  # 大小以及位置
    root.minsize(root_width, root_height)
    root.iconbitmap(logo_ico_path)

    # 样式
    style = ttk.Style()
    style.configure('Treeview.Heading', font=('楷体', 13))  # 设置表头字体
    style.configure('Treeview', font=('楷体', 13))  # 设置表格内容字体
    style.configure('TButton', font=('楷体', 13))  # 设置按钮字体

    logo_img = tk.PhotoImage(file=logo_img_path)
    birthday_button_img = tk.PhotoImage(file=birthday_img_path)
    account_button_img = tk.PhotoImage(file=account_img_path)

    # 创建左边的菜单栏
    menu_frame = tk.Frame(root, background="white", width=menu_width)
    menu_frame.pack(side="left", fill="y")

    # 创建右边的主内容区
    content_frame = tk.Frame(root)
    content_frame.pack(side="right", fill="both", expand=True)

    tk.Label(content_frame, image=logo_img).pack(expand=True)

    # 添加菜单项按钮
    birthday_button = tk.Button(menu_frame, image=birthday_button_img, bd=0, highlightthickness=0, relief="flat", command=lambda: bir_win.update_content(content_frame, "生日", root))
    birthday_button.pack(side="top", pady=10)

    account_button = tk.Button(menu_frame, image=account_button_img, bd=0, highlightthickness=0, relief="flat", command=lambda: acc_win.update_content(content_frame, "账号", root))
    account_button.pack(side="top", pady=10)

    root.mainloop()
