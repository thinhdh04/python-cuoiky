from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Hàm tạo kết nối cơ sở dữ liệu SQLite
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  # Để có thể truy cập cột như từ điển
    return conn

# Hàm tạo bảng ToDo trong cơ sở dữ liệu
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Trang chủ hiển thị danh sách công việc
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Thêm công việc mới
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# Xóa công việc
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Tạo bảng nếu chưa tồn tại
    app.run(debug=True)
