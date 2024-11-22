import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Kết nối SQLite
conn = sqlite3.connect("personal_expenses.db")
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL
)
""")
conn.commit()

# Hàm thêm giao dịch
def add_transaction():
    date = entry_date.get()
    description = entry_desc.get()
    amount = entry_amount.get()
    category = category_var.get()
    
    if not (date and description and amount and category):
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
        return
    
    try:
        amount = float(amount)
        cursor.execute("INSERT INTO expenses (date, description, amount, category) VALUES (?, ?, ?, ?)",
                       (date, description, amount, category))
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm giao dịch thành công!")
        clear_entries()
        load_transactions()
    except ValueError:
        messagebox.showerror("Lỗi", "Số tiền phải là một giá trị số hợp lệ!")

# Hàm xóa dữ liệu nhập
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    category_var.set("")

# Hàm tải dữ liệu lên bảng
def load_transactions():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    for row in rows:
        # Định dạng lại số tiền với dấu phân cách
        formatted_row = list(row)
        formatted_row[3] = f"{row[3]:,}"  # Định dạng số tiền tại cột 3 (Số tiền)
        tree.insert("", tk.END, values=formatted_row)
    calculate_balance()


# Hàm tính tổng số dư
def calculate_balance():
    cursor.execute("SELECT SUM(CASE WHEN category='Income' THEN amount ELSE -amount END) FROM expenses")
    balance = cursor.fetchone()[0]
    if balance:
        lbl_balance.config(text=f"Số dư hiện tại: {balance:,.2f} VND")
    else:
        lbl_balance.config(text="Số dư hiện tại: 0.00 VND")

# Hàm xóa một giao dịch
def delete_transaction():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn giao dịch để xóa!")
        return
    transaction_id = tree.item(selected_item)["values"][0]
    cursor.execute("DELETE FROM expenses WHERE id = ?", (transaction_id,))
    conn.commit()
    messagebox.showinfo("Thành công", "Đã xóa giao dịch!")
    load_transactions()

# Giao diện Tkinter
root = tk.Tk()
root.title("Quản Lý Chi Tiêu Cá Nhân")
root.geometry("800x600")

# Frame nhập liệu
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Ngày (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(frame_input, width=20)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5)
entry_desc = tk.Entry(frame_input, width=20)
entry_desc.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Số tiền:").grid(row=2, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_input, width=20)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Loại:").grid(row=3, column=0, padx=5, pady=5)
category_var = tk.StringVar()
ttk.Combobox(frame_input, textvariable=category_var, values=["Income", "Expense"], width=18).grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Thêm Giao Dịch", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=10)

# Bảng hiển thị dữ liệu
frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack()

columns = ("ID", "Ngày", "Mô tả", "Số tiền", "Loại")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100 if col == "ID" else 150)
tree.pack()

# Nút xóa giao dịch
tk.Button(root, text="Xóa Giao Dịch", command=delete_transaction).pack(pady=10)

# Hiển thị tổng số dư
frame_balance = tk.Frame(root, padx=10, pady=10)
frame_balance.pack()
lbl_balance = tk.Label(frame_balance, text="Số dư hiện tại: 0.00 VND", font=("Arial", 14))
lbl_balance.pack()

# Tải dữ liệu ban đầu
load_transactions()

# Chạy chương trình
root.mainloop()

# Đóng kết nối SQLite khi thoát chương trình
conn.close()
