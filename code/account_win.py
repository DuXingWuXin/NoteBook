import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db



# 更新表格和上方按钮
def update_content(content_frame, text, win):
    
    # 清空现有内容
    for widget in content_frame.winfo_children():
        widget.destroy()

    # 创建按钮区域
    button_frame = tk.Frame(content_frame)
    button_frame.pack(fill="x", pady=5)

    # 添加说明区域
    tk.Label(button_frame, text=text, font=("楷体", 13)).pack(side="left", padx=5)

    # 创建表格区域
    table_frame = tk.Frame(content_frame)
    table_frame.pack(fill="both", expand=True)

    # 创建垂直滚动条
    vertical_scrollbar = tk.Scrollbar(table_frame, orient="vertical")

    # 添加表格
    account_table = ttk.Treeview(
        master=table_frame,
        columns=['ID', '行', 'app', '账号', '密码'],
        show='headings',  # 隐藏首列
        yscrollcommand=vertical_scrollbar.set,
    )
    account_table.heading('ID', text='ID')
    account_table.heading('行', text='行')
    account_table.heading('app', text='app')
    account_table.heading('账号', text='账号')
    account_table.heading('密码', text='密码')
    account_table.column('ID', width=0, stretch=False)
    account_table.column('行', width=20, anchor=tk.CENTER)
    account_table.column('app', width=100, anchor=tk.CENTER)
    account_table.column('账号', width=150, anchor=tk.CENTER)
    account_table.column('密码', width=150, anchor=tk.CENTER)
    account_table.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # 配置滚动条与Treeview绑定
    vertical_scrollbar.config(command=account_table.yview)
    vertical_scrollbar.pack(side="right", fill="y")

    def on_resize(event):
        width = event.width
        scrollbar_width = vertical_scrollbar.winfo_width() if vertical_scrollbar.winfo_width() > 0 else 10
        width = width - scrollbar_width
        
        column_ratios = [0.0, 0.05, 0.2, 0.35, 0.35]
    
        # 计算每列的宽度
        for i, col in enumerate(account_table["columns"]):
            column_width = int(width * column_ratios[i])
            account_table.column(col, width=column_width, minwidth=column_width)

    # 绑定窗口大小变化事件
    table_frame.bind("<Configure>", on_resize)

    # 添加按钮
    tk.Button(button_frame, text="删除", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: delete_button_event(account_table)).pack(side="right", padx=3)
    tk.Button(button_frame, text="添加", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: insert_button_event(win, account_table)).pack(side="right", padx=3)
    tk.Button(button_frame, text="编辑", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: edit_button_event(win, account_table)).pack(side="right", padx=3)
    tk.Button(button_frame, text="搜索", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: search_button_event(search_entry, account_table)).pack(side="right", padx=3)

    # 添加搜索框
    search_entry = tk.Entry(button_frame, width=10)
    def on_entry_click(event):
        """处理Entry框单击事件"""
        if search_entry.get() == "app":
            search_entry.delete(0, "end")  # 删除文本框内容
            search_entry.configure(foreground='black')  # 设置正常文本颜色

    def on_focus_out(event):
        """处理Entry框焦点离开事件"""
        if search_entry.get() == "":
            search_entry.insert(0, "app")  # 插入默认文本
            search_entry.configure(foreground='grey')  # 设置灰色文本

    search_entry.bind('<FocusIn>', on_entry_click)
    search_entry.bind('<FocusOut>', on_focus_out)
    search_entry.configure(foreground='grey')
    search_entry.pack(side="right", padx=3)
    search_entry.insert(0, "app")

    display_data(account_table, db.searchAll_accounts())




def display_data(table, data):
    table.delete(*table.get_children())
    for index, row in enumerate(data, start=1):
        table.insert('', tk.END, values=(row[0], index, row[1], row[2], row[3]))

def search_button_event(search_entry, table):
    search_name = search_entry.get()
    if search_name == "":
        data = db.searchAll_accounts()
    else:
        data = db.searchByName_accounts(search_name)
    display_data(table, data)

def insert_button_event(win, table):
    # 创建添加对话框
    insert_dialog = tk.Toplevel(win)
    insert_dialog.title("添加")
    dialog_width = 300
    dialog_height = 250

    # 获取主窗口位置和尺寸
    main_x = win.winfo_x()
    main_y = win.winfo_y()
    main_width = win.winfo_width()
    main_height = win.winfo_height()

    # 计算弹窗位置，使其位于主窗口中央
    dialog_x = main_x + (main_width - dialog_width) // 2
    dialog_y = main_y + (main_height - dialog_height) // 2
    insert_dialog.geometry(f'{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}')

    tk.Label(insert_dialog, text="app:").pack(pady=5)
    app_entry = ttk.Entry(insert_dialog)
    app_entry.pack(pady=5)

    tk.Label(insert_dialog, text="账号:").pack(pady=5)
    account_entry = ttk.Entry(insert_dialog)
    account_entry.pack(pady=5)

    tk.Label(insert_dialog, text="密码:").pack(pady=5)
    password_entry = ttk.Entry(insert_dialog)
    password_entry.pack(pady=5)


    def insert():
        app = app_entry.get()
        account = account_entry.get()
        password = password_entry.get()

        new_values = (app, account, password)
        db.insert_accounts(new_values)

        messagebox.showinfo("添加成功", "添加成功")

        display_data(table, db.searchAll_accounts())
        
        insert_dialog.destroy()

    tk.Button(insert_dialog, text="添加", command=insert).pack(pady=10)


def delete_button_event(table):
    selected_item = table.selection()
    if selected_item:
        confirm = messagebox.askyesno("确认删除", "确定要删除选中的行吗？")
        if confirm:
            for item in selected_item:
                item_id = table.item(item)['values'][0]
                db.delete_accounts(item_id)

            messagebox.showinfo("删除成功", "所选行已成功删除")

            display_data(table, db.searchAll_accounts())
    else:
        messagebox.showwarning("未选择行", "请先选择要删除的行")


def edit_button_event(win, table):
    selected_item = table.selection()
    if selected_item:
        item = table.item(selected_item)
        old_values = item['values']

        # 创建编辑对话框
        edit_dialog = tk.Toplevel(win)
        edit_dialog.title("修改")
        dialog_width = 300
        dialog_height = 250

        # 获取主窗口位置和尺寸
        main_x = win.winfo_x()
        main_y = win.winfo_y()
        main_width = win.winfo_width()
        main_height = win.winfo_height()

        # 计算弹窗位置，使其位于主窗口中央
        dialog_x = main_x + (main_width - dialog_width) // 2
        dialog_y = main_y + (main_height - dialog_height) // 2
        edit_dialog.geometry(f'{dialog_width}x{dialog_height}+{dialog_x}+{dialog_y}')

        tk.Label(edit_dialog, text="app:").pack(pady=5)
        app_entry = ttk.Entry(edit_dialog)
        app_entry.pack(pady=5)
        app_entry.insert(0, old_values[2])

        tk.Label(edit_dialog, text="账号:").pack(pady=5)
        account_entry = ttk.Entry(edit_dialog)
        account_entry.pack(pady=5)
        account_entry.insert(0, old_values[3])

        tk.Label(edit_dialog, text="密码:").pack(pady=5)
        password_entry = ttk.Entry(edit_dialog)
        password_entry.pack(pady=5)
        password_entry.insert(0, old_values[4])

        def edit():
            app = app_entry.get()
            account = account_entry.get()
            password = password_entry.get()

            new_values = (app, account, password, old_values[0])
            db.update_accounts(new_values)

            messagebox.showinfo("编辑成功", "编辑成功")

            display_data(table, db.searchAll_accounts())

            edit_dialog.destroy()

        tk.Button(edit_dialog, text="保存", command=edit).pack(pady=10)
    else:
        messagebox.showwarning("未选择行", "请先选择要编辑的行")