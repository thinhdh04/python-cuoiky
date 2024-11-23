from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Hàm tạo kết nối cơ sở dữ liệu SQLite
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row  # Để có thể truy cập cột như từ điển
    return conn

# Trang chủ hiển thị danh sách công việc
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('''
        SELECT tasks.id, tasks.title, tasks.description, tasks.status, priorities.level AS priority, categories.name AS category
        FROM tasks
        JOIN priorities ON tasks.priority_id = priorities.id
        JOIN categories ON tasks.category_id = categories.id
    ''').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Thêm công việc mới
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    priority_id = request.form['priority_id']
    category_id = request.form['category_id']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tasks (title, description, status, priority_id, category_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, status, priority_id, category_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Chỉnh sửa công việc
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        priority_id = request.form['priority_id']
        category_id = request.form['category_id']
        
        conn.execute('''
            UPDATE tasks
            SET title = ?, description = ?, status = ?, priority_id = ?, category_id = ?
            WHERE id = ?
        ''', (title, description, status, priority_id, category_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    categories = conn.execute('SELECT * FROM categories').fetchall()
    priorities = conn.execute('SELECT * FROM priorities').fetchall()
    conn.close()
    
    return render_template('edit_task.html', task=task, categories=categories, priorities=priorities)

# Xóa công việc
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Cập nhật trạng thái công việc
@app.route('/update_status/<int:id>/<status>', methods=['POST'])
def update_status(id, status):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
