from tkinter import *

# Tạo cửa sổ chính
win = Tk()
win.geometry("312x324")
win.resizable(0, 0)
win.title("Máy Tính")

# Khởi tạo biến toàn cục cho biểu thức
bieu_thuc = ""

# Các hàm
def btn_click(item):
    global bieu_thuc
    bieu_thuc += str(item)
    input_text.set(bieu_thuc)

def xoa():  # Hàm để xóa trường nhập liệu
    global bieu_thuc
    bieu_thuc = ""
    input_text.set("")

def bang():  # Hàm để tính toán biểu thức hiện tại
    global bieu_thuc
    try:
        ket_qua = str(eval(bieu_thuc))
        input_text.set(ket_qua)
        bieu_thuc = ""
    except:
        input_text.set("Lỗi!")
        bieu_thuc = ""

# Khởi tạo trường nhập liệu
input_text = StringVar()
khung_nhap = Frame(win, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=2)
khung_nhap.pack(side=TOP)

# Đặt màu nền của ô nhập liệu thành màu trắng
truong_nhap = Entry(khung_nhap, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#fff", fg="#000", bd=0, justify=RIGHT)
truong_nhap.grid(row=0, column=0)
truong_nhap.pack(ipady=10)

# Tạo khung cho các nút bấm
khung_nut = Frame(win, width=312, height=272.5, bg="grey")
khung_nut.pack()

# Đặt màu sắc cho các nút
mau_nut_so = "#4CAF50"  # Màu xanh cho các nút số
mau_nut_phep_toan = "#FF9800"  # Màu cam cho các nút phép toán
mau_nut_chuc_nang = "#f44336"  # Màu đỏ cho nút chức năng

# Dòng đầu tiên
Button(khung_nut, text="C", fg="white", width=32, height=3, bd=0, bg=mau_nut_chuc_nang, cursor="hand2", command=xoa).grid(row=0, column=0, columnspan=3, padx=1, pady=1)
Button(khung_nut, text="/", fg="white", width=10, height=3, bd=0, bg=mau_nut_phep_toan, cursor="hand2", command=lambda: btn_click("/")).grid(row=0, column=3, padx=1, pady=1)

# Dòng thứ hai
Button(khung_nut, text="7", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(7)).grid(row=1, column=0, padx=1, pady=1)
Button(khung_nut, text="8", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(8)).grid(row=1, column=1, padx=1, pady=1)
Button(khung_nut, text="9", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(9)).grid(row=1, column=2, padx=1, pady=1)
Button(khung_nut, text="*", fg="white", width=10, height=3, bd=0, bg=mau_nut_phep_toan, cursor="hand2", command=lambda: btn_click("*")).grid(row=1, column=3, padx=1, pady=1)

# Dòng thứ ba
Button(khung_nut, text="4", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(4)).grid(row=2, column=0, padx=1, pady=1)
Button(khung_nut, text="5", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(5)).grid(row=2, column=1, padx=1, pady=1)
Button(khung_nut, text="6", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(6)).grid(row=2, column=2, padx=1, pady=1)
Button(khung_nut, text="-", fg="white", width=10, height=3, bd=0, bg=mau_nut_phep_toan, cursor="hand2", command=lambda: btn_click("-")).grid(row=2, column=3, padx=1, pady=1)

# Dòng thứ tư
Button(khung_nut, text="1", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(1)).grid(row=3, column=0, padx=1, pady=1)
Button(khung_nut, text="2", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(2)).grid(row=3, column=1, padx=1, pady=1)
Button(khung_nut, text="3", fg="white", width=10, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(3)).grid(row=3, column=2, padx=1, pady=1)
Button(khung_nut, text="+", fg="white", width=10, height=3, bd=0, bg=mau_nut_phep_toan, cursor="hand2", command=lambda: btn_click("+")).grid(row=3, column=3, padx=1, pady=1)

# Dòng cuối cùng
Button(khung_nut, text="0", fg="white", width=21, height=3, bd=0, bg=mau_nut_so, cursor="hand2", command=lambda: btn_click(0)).grid(row=4, column=0, columnspan=2, padx=1, pady=1)
Button(khung_nut, text=".", fg="white", width=10, height=3, bd=0, bg=mau_nut_phep_toan, cursor="hand2", command=lambda: btn_click(".")).grid(row=4, column=2, padx=1, pady=1)
Button(khung_nut, text="=", fg="white", width=10, height=3, bd=0, bg="#009688", cursor="hand2", command=bang).grid(row=4, column=3, padx=1, pady=1)

# Vòng lặp chính để hiển thị cửa sổ
win.mainloop()
