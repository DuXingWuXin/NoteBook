import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
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
    birthday_table = ttk.Treeview(
        master=table_frame,
        columns=['ID', '行', '姓名', '出生日期', '类型'],
        show='headings',  # 隐藏首列
        yscrollcommand=vertical_scrollbar.set,
    )
    birthday_table.heading('ID', text='ID')
    birthday_table.heading('行', text='行')
    birthday_table.heading('姓名', text='姓名')
    birthday_table.heading('出生日期', text='出生日期')
    birthday_table.heading('类型', text='类型')
    birthday_table.column('ID', stretch=False)
    birthday_table.column('行', anchor=tk.CENTER)
    birthday_table.column('姓名', anchor=tk.CENTER)
    birthday_table.column('出生日期', anchor=tk.CENTER)
    birthday_table.column('类型', anchor=tk.CENTER)
    birthday_table.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # 配置滚动条与Treeview绑定
    vertical_scrollbar.config(command=birthday_table.yview)
    vertical_scrollbar.pack(side="right", fill="y")

    def on_resize(event):
        width = event.width
        scrollbar_width = vertical_scrollbar.winfo_width() if vertical_scrollbar.winfo_width() > 0 else 10
        width = width - scrollbar_width
        
        column_ratios = [0.0, 0.05, 0.3, 0.3, 0.3]
    
        # 计算每列的宽度
        for i, col in enumerate(birthday_table["columns"]):
            column_width = int(width * column_ratios[i])
            birthday_table.column(col, width=column_width, minwidth=column_width)

    # 绑定窗口大小变化事件
    table_frame.bind("<Configure>", on_resize)

    # 添加按钮
    tk.Button(button_frame, text="删除", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: delete_button_event(birthday_table)).pack(side="right", padx=3)
    tk.Button(button_frame, text="添加", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: insert_button_event(win, birthday_table)).pack(side="right", padx=3)
    tk.Button(button_frame, text="编辑", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: edit_button_event(win, birthday_table)).pack(side="right", padx=3)
    tk.Button(button_frame, text="搜索", bd=0, highlightthickness=0, relief="flat", font=("楷体", 13), command=lambda: search_button_event(search_entry, birthday_table)).pack(side="right", padx=3)

    # 添加搜索框
    search_entry = tk.Entry(button_frame, width=10)
    def on_entry_click(event):
        """处理Entry框单击事件"""
        if search_entry.get() == "姓名":
            search_entry.delete(0, "end")  # 删除文本框内容
            search_entry.configure(foreground='black')  # 设置正常文本颜色

    def on_focus_out(event):
        """处理Entry框焦点离开事件"""
        if search_entry.get() == "":
            search_entry.insert(0, "姓名")  # 插入默认文本
            search_entry.configure(foreground='grey')  # 设置灰色文本

    search_entry.bind('<FocusIn>', on_entry_click)
    search_entry.bind('<FocusOut>', on_focus_out)
    search_entry.configure(foreground='grey')
    search_entry.pack(side="right", padx=3)
    search_entry.insert(0, "姓名")

    display_data(birthday_table, db.searchAll_birthdays())




def display_data(table, data):
    table.delete(*table.get_children())
    for index, row in enumerate(data, start=1):
        date_type = "阳历" if row[3] == 0 else "阴历"
        table.insert('', tk.END, values=(row[0], index, row[1], row[2], date_type))

def search_button_event(search_entry, table):
    search_name = search_entry.get()
    if search_name == "":
        data = db.searchAll_birthdays()
    else:
        data = db.searchByName_birthdays(search_name)
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

    tk.Label(insert_dialog, text="姓名:").pack(pady=5)
    name_entry = ttk.Entry(insert_dialog)
    name_entry.pack(pady=5)

    def on_entry_click(event):
        """处理Entry框单击事件"""
        if birthday_entry.get() == "YYYY-MM-DD":
            birthday_entry.delete(0, "end")  # 删除文本框内容
            birthday_entry.configure(foreground='black')  # 设置正常文本颜色

    def on_focus_out(event):
        """处理Entry框焦点离开事件"""
        if birthday_entry.get() == "":
            birthday_entry.insert(0, "YYYY-MM-DD")  # 插入默认文本
            birthday_entry.configure(foreground='grey')  # 设置灰色文本

    tk.Label(insert_dialog, text="出生年月:").pack(pady=5)
    birthday_entry = ttk.Entry(insert_dialog)
    birthday_entry.insert(0, "YYYY-MM-DD")
    birthday_entry.bind('<FocusIn>', on_entry_click)
    birthday_entry.bind('<FocusOut>', on_focus_out)
    birthday_entry.configure(foreground='grey')  # 设置默认文本颜色为灰色
    birthday_entry.pack(pady=5)

    tk.Label(insert_dialog, text="日期类型:").pack(pady=5)
    date_type_combobox = ttk.Combobox(insert_dialog, values=["阳历", "阴历"], state='readonly')
    date_type_combobox.pack(pady=5)

    def insert():
        name = name_entry.get()
        birthday = birthday_entry.get()
        date_type = date_type_combobox.get()

       # 验证日期格式
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("错误", "出生年月格式错误，应为YYYY-MM-DD！")
            return

        # 验证日期类型
        if date_type == "阳历":
            is_lunar = False
        elif date_type == "阴历":
            is_lunar = True

        new_values = (name, birthday, is_lunar)
        db.insert_birthdays(new_values)

        messagebox.showinfo("添加成功", "添加成功")

        display_data(table, db.searchAll_birthdays())
        
        insert_dialog.destroy()

    tk.Button(insert_dialog, text="添加", command=insert).pack(pady=10)


def delete_button_event(table):
    selected_item = table.selection()
    if selected_item:
        confirm = messagebox.askyesno("确认删除", "确定要删除选中的行吗？")
        if confirm:
            for item in selected_item:
                item_id = table.item(item)['values'][0]
                db.delete_birthdays(item_id)

            messagebox.showinfo("删除成功", "所选行已成功删除")

            display_data(table, db.searchAll_birthdays())
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

        tk.Label(edit_dialog, text="姓名:").pack(pady=5)
        name_entry = ttk.Entry(edit_dialog)
        name_entry.pack(pady=5)
        name_entry.insert(0, old_values[2])

        tk.Label(edit_dialog, text="出生年月:").pack(pady=5)
        birthday_entry = ttk.Entry(edit_dialog)
        birthday_entry.pack(pady=5)
        birthday_entry.insert(0, old_values[3])

        tk.Label(edit_dialog, text="日期类型:").pack(pady=5)
        date_type_combobox = ttk.Combobox(edit_dialog, values=["阳历", "阴历"], state='readonly')
        date_type_combobox.pack(pady=5)
        date_type_combobox.set(old_values[4])

        def edit():
            name = name_entry.get()
            birthday = birthday_entry.get()
            date_type = date_type_combobox.get()

            # 验证日期格式
            try:
                datetime.strptime(birthday, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("错误", "出生年月格式错误，应为YYYY-MM-DD！")
                return

            # 验证日期类型
            if date_type == "阳历":
                is_lunar = False
            elif date_type == "阴历":
                is_lunar = True

            new_values = (name, birthday, is_lunar, old_values[0])
            db.update_birthdays(new_values)

            messagebox.showinfo("编辑成功", "编辑成功")

            display_data(table, db.searchAll_birthdays())

            edit_dialog.destroy()

        tk.Button(edit_dialog, text="保存", command=edit).pack(pady=10)
    else:
        messagebox.showwarning("未选择行", "请先选择要编辑的行")