import sqlite3
import os
import sys


# 获取当前目录
def get_executable_path():
    # 可执行文件
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # 代码
    else:
        return os.path.dirname(os.path.abspath(__file__))
    
# 拼接为数据库文件路径
def database_path():
    base_path = get_executable_path()
    return os.path.join(base_path, 'database.db')
    
# 上下文管理器，自动管理连接和游标
class SQLiteConnection:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    
def createTable_database():
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS birthdays (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            birthday DATE NOT NULL,
                            is_lunar BOOLEAN NOT NULL
                            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            application TEXT NOT NULL,
                            account TEXT NOT NULL,
                            password TEXT
                            )''')

def searchAll_birthdays():
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('SELECT * FROM birthdays')
        data = cursor.fetchall()
    return data

def searchByName_birthdays(name):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('SELECT * FROM birthdays WHERE name LIKE ?', ('%' + name + '%',))
        data = cursor.fetchall()
    return data

def insert_birthdays(values):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('INSERT INTO birthdays (name, birthday, is_lunar) VALUES (?, ?, ?)', values)


def delete_birthdays(id):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('DELETE FROM birthdays WHERE id=?', (id,))


def update_birthdays(values):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('UPDATE birthdays SET name=?, birthday=?, is_lunar=? WHERE id=?', values)



def searchAll_accounts():
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('SELECT * FROM accounts')
        data = cursor.fetchall()
    return data

def searchByName_accounts(name):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('SELECT * FROM accounts WHERE application LIKE ?', ('%' + name + '%',))
        data = cursor.fetchall()
    return data

def insert_accounts(values):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('INSERT INTO accounts (application, account, password) VALUES (?, ?, ?)', values)


def delete_accounts(id):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('DELETE FROM accounts WHERE id=?', (id,))


def update_accounts(values):
    with SQLiteConnection(database_path()) as cursor:
        cursor.execute('UPDATE accounts SET application=?, account=?, password=? WHERE id=?', values)