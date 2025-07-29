import datetime
from lunardate import LunarDate
import tkinter as tk
import database as db



# 存储读取到的日期
solar_birthdays = {}
lunar_birthdays = {}

# 提前提醒的天数
remind_days = 5


# 从数据库读取数据，将日期存储
def read_from_db():
    rows = db.searchAll_birthdays()

    for row in rows:
        id, name, birthday_str, is_lunar = row
        if is_lunar:
            lunar_birthdays[name] = datetime.datetime.strptime(birthday_str, '%Y-%m-%d').date()
        else:
            solar_birthdays[name] = datetime.datetime.strptime(birthday_str, '%Y-%m-%d').date()


# 检查阳历生日
def check_solar_birthdays(reminders, solar_birthdays, remind_days):
    today = datetime.date.today()
    for name, bdate in solar_birthdays.items():
        # 处理跨年：计算今年的生日日期。 如果今年生日已过，计算明年生日
        bday_this_year = datetime.date(today.year, bdate.month, bdate.day)
        delta = (bday_this_year - today).days
        if delta < 0:
            bday_next_year = datetime.date(today.year + 1, bdate.month, bdate.day)
            delta = (bday_next_year - today).days

        if delta == 0:
            reminders.append((f"今日寿星！ {name}", "blue"))
        elif delta <= remind_days:
            reminders.append((f"{delta}天后 {name}", "black"))


# 检查阴历生日
def check_lunar_birthdays(reminders, lunar_birthdays, remind_days):
    today = datetime.date.today()
    
    # 计算今天和未来几天的公历日期
    future_dates = [today + datetime.timedelta(days=i) for i in range(remind_days + 1)]
    
    # 转换为对应的农历日期
    lunar_dates = []
    for s_date in future_dates:
        try:
            lunar_date = LunarDate.fromSolarDate(s_date.year, s_date.month, s_date.day)
            lunar_dates.append((s_date, lunar_date))
        except Exception as e:
            print(f"转换日期 {s_date} 时出错: {e}")
            lunar_dates.append((s_date, None))
    
    # 检查每个农历生日
    for name, lbirth in lunar_birthdays.items():
        lunar_month_day = (lbirth.month, lbirth.day)
        
        for s_date, l_date in lunar_dates:
            if l_date and (l_date.month, l_date.day) == lunar_month_day:
                delta = (s_date - today).days
                
                if delta == 0:
                    reminders.append((f"今日寿星！ {name}", "blue"))
                else:
                    reminders.append((f"{delta}天后 {name}", "black"))

                break


# 在区域中显示最近生日的人
def check_birthdays():
    reminders = []

    check_solar_birthdays(reminders, solar_birthdays, remind_days)
    check_lunar_birthdays(reminders, lunar_birthdays, remind_days)

    return reminders


# 将窗口显示在右下角
def right_bottom_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = screen_width - width
    y = screen_height - height

    window.geometry("+%d+%d" % (x, y))


# 窗口
def show_birthdays_window(reminders):
    if reminders:
        popup = tk.Tk()
        popup.lift()
        popup.title("生日提醒")
        popup.geometry("300x300")
        label_font = ("楷书", 15)

        for reminder_text, color in reminders:
            label = tk.Label(popup, text=reminder_text, font=label_font, fg=color, anchor="center")
            label.pack(expand=True, fill="both")
        
        right_bottom_window(popup, 300, 300)
        popup.mainloop()


if __name__ == '__main__':
    read_from_db()
    reminders = check_birthdays()
    show_birthdays_window(reminders)
