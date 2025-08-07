import tkinter
import pymysql
from tkinter.simpledialog import askstring
from tkinter import ttk, font, messagebox
import random

root = tkinter.Tk()
root.geometry('800x600')
root.title('AIRPORT MANAGEMENT SYSTEM')

d = {}
f1 = font.Font(family='Arial', size=32)
f2 = font.Font(family='Arial', size=16)

e1 = tkinter.StringVar()
e2 = tkinter.StringVar()
e3 = tkinter.StringVar()

l = list(range(2, 61))
P = ['AIR INDIA 1', 'BOEING 2', 'BRITAIN AIRLINE 3']
C = ['BUSSINESS', 'ECONOMY']

con = pymysql.connect(user='root', password='csctnr', host='localhost', database='airport', port=3306)
mc = con.cursor()

def admin():
    name = askstring('password', 'what is password')
    if name == 'abcd':
        frm.pack_forget()
        frm1.pack()
    else:
        messagebox.showerror('password', 'wrong password')

def admin1():
    for i in all_frames:
        i.pack_forget()
    frm1.pack()

def save():
    try:
        q = "insert into plane_details values(%s,%s,%s)"
        s = (combo.get(), e1.get(), e2.get())
        mc.execute(q, s)
        con.commit()
    except:
        messagebox.showerror('AIRPORT MANAGEMENT SYSTEM','INVALID DATE FORMAT')

def load1():
    frm1.pack_forget()
    pdetails.pack()
    for i in tv.get_children():
        tv.delete(i)
    mc.execute('select * from plane_details')
    rows = mc.fetchall()
    for i in rows:
        d[i[0]] = i
        tv.insert('', tkinter.END, values=i[0:])

def login():
    for i in all_frames:
        i.pack_forget()
    frm.pack()

def passenger():
    for i in all_frames:
        i.pack_forget()
    frm2.pack()

def psch():
    frm1.pack_forget()
    pschedule.pack()

def savep():
    if not l:
        messagebox.showerror("Error", "All tickets booked.")
        return
    x = random.choice(l)
    l.remove(x)
    q = "insert into passengers values(%s,%s,%s,%s)"
    s = (e3.get(), combo1.get(), combo2.get(), str(x))
    e3.set('')
    mc.execute(q, s)
    con.commit()

def tbook():
    for i in all_frames:
        i.pack_forget()
    bticket.pack()

def tdetails():
    for i in all_frames:
        i.pack_forget()
    dticket.pack()
    for i in tv1.get_children():
        tv1.delete(i)
    mc.execute('select * from passengers')
    rows = mc.fetchall()
    for i in rows:
        tv1.insert('', tkinter.END, values=i[0:])

def tcancellation():
    for i in all_frames:
        i.pack_forget()
    cticket.pack()
    lb.delete(0, tkinter.END)
    mc.execute('SELECT p_name FROM passengers')
    rows = mc.fetchall()
    for i in rows:
        lb.insert(tkinter.END, i[0])

def cancel():
    selected_index = lb.curselection()
    if selected_index:
        selected_name = lb.get(selected_index[0])
        q = 'DELETE FROM passengers WHERE p_name = %s'
        mc.execute(q, (selected_name,))
        con.commit()
        lb.delete(selected_index[0])
        messagebox.showinfo("Success", f"Ticket for {selected_name} has been cancelled.")

def prep():
    for i in all_frames:
        i.pack_forget()
    preport.pack()
    for i in tv2.get_children():  # Fixed: was tv1.get_children()
        tv2.delete(i)
    mc.execute('select * from passengers')
    rows = mc.fetchall()
    for i in rows:
        tv2.insert('', tkinter.END, values=i[0:])

# Frames
frm = tkinter.Frame(root)
frm1 = tkinter.Frame(root)
frm2 = tkinter.Frame(root)
pschedule = tkinter.Frame(root)
pdetails = tkinter.Frame(root)
bticket = tkinter.Frame(root)
cticket = tkinter.Frame(root)
dticket = tkinter.Frame(root)
preport = tkinter.Frame(root)

# Frame: Login
tkinter.Label(frm, text='LOGIN PORTAL', font=f1).pack()
tkinter.Button(frm, text='ADMIN LOGIN', command=admin, width=25, font=f2, pady=10).pack()
tkinter.Button(frm, text='PASSENGER LOGIN', command=passenger, width=25, font=f2, pady=10).pack()

# Frame: Admin
tkinter.Label(frm1, text='ADMIN PORTAL', font=f1).pack()
tkinter.Button(frm1, text='EDIT PLANE DETAILS', width=25, font=f2, command=psch).pack()
tkinter.Button(frm1, text='PASSENGERS REPORT', width=25, font=f2, pady=10, command=prep).pack()
tkinter.Button(frm1, text='PLANE DETAILS', width=25, font=f2, pady=10, command=load1).pack()
tkinter.Button(frm1, text='LOGIN PORTAL', width=25, font=f2, pady=10, command=login).pack()

# Frame: Passenger
tkinter.Label(frm2, text='PASSENGER PORTAL', font=f1).pack()
tkinter.Button(frm2, text='TICKET BOOKING', width=25, font=f2, pady=10, command=tbook).pack()
tkinter.Button(frm2, text='TICKET CANCELLATION', width=25, font=f2, pady=10, command=tcancellation).pack()
tkinter.Button(frm2, text='TICKET DETAILS', width=25, font=f2, pady=10, command=tdetails).pack()
tkinter.Button(frm2, text='LOGIN PORTAL', width=25, font=f2, pady=10, command=login).pack()

# Frame: Plane Schedule
tkinter.Label(pschedule, text='AIRPLANE MODEL', font=f2).pack()
combo = ttk.Combobox(pschedule, value=P)
combo.pack()
tkinter.Label(pschedule, text='REPORTING TIME', font=f2, pady=10).pack()
tkinter.Entry(pschedule, width=25, textvariable=e1).pack()
tkinter.Label(pschedule, text='DEPARTURE TIME', font=f2, pady=10).pack()
tkinter.Entry(pschedule, width=25, textvariable=e2).pack()
tkinter.Button(pschedule, text='save', font=f2, command=save, width=25, pady=10).pack()
tkinter.Button(pschedule, text='ADMIN PORTAL', font=f2, command=admin1, width=25).pack()

# Plane Details Treeview
ts = ttk.Style()
ts.configure('Treeview.Heading', font=('Arial', 12, 'bold'))
ts.configure('Treeview', font=('Arial', 12))
tv = ttk.Treeview(pdetails, columns=('c1', 'c2', 'c3'), show='headings')
tv.heading('c1', text='PLANE MODEL')
tv.heading('c2', text='REPORT TIMING')
tv.heading('c3', text='DEPARTURE')
tkinter.Button(pdetails, text='ADMIN PORTAL', font=f2, command=admin1, width=25).pack(side=tkinter.BOTTOM)
tv.pack()

# Ticket Booking
tkinter.Label(bticket, text='NAME', font=f2).pack()
tkinter.Entry(bticket, width=25, textvariable=e3).pack()
tkinter.Label(bticket, text='PLANE MODEL', font=f2, pady=10).pack()
combo1 = ttk.Combobox(bticket, value=P)
combo1.pack()
tkinter.Label(bticket, text='CLASS', font=f2, pady=10).pack()
combo2 = ttk.Combobox(bticket, value=C)
combo2.pack()
tkinter.Button(bticket, text='save', font=f2, command=savep, width=25, pady=10).pack()
tkinter.Button(bticket, text='PASSENGER PORTAL', font=f2, command=passenger, width=25).pack()

# Ticket Details
tv1 = ttk.Treeview(dticket, columns=('d1', 'd2', 'd3', 'd4'), show='headings')
tv1.heading('d1', text='NAME')
tv1.heading('d2', text='PLANE MODEL')
tv1.heading('d3', text='CLASS')
tv1.heading('d4', text='TICKET NO')
tv1.pack()
tkinter.Button(dticket, text='PASSENGER PORTAL', font=f2, command=passenger, width=25).pack()

# Ticket Cancellation
lb = tkinter.Listbox(cticket)
lb.pack()
tkinter.Button(cticket, text='CANCEL', font=f2, command=cancel, width=25).pack()
tkinter.Button(cticket, text='PASSENGER PORTAL', font=f2, command=passenger, width=25).pack()

# Passenger Report
tv2 = ttk.Treeview(preport, columns=('D1', 'D2', 'D3', 'D4'), show='headings')
tv2.heading('D1', text='NAME')
tv2.heading('D2', text='PLANE MODEL')
tv2.heading('D3', text='CLASS')
tv2.heading('D4', text='TICKET NO')
tv2.pack()
tkinter.Button(preport, text='ADMIN PORTAL', font=f2, command=admin1, width=25).pack()

# All frames list
all_frames = [frm, frm1, frm2, pschedule, pdetails, bticket, cticket, dticket, preport]

# Start from login frame
frm.pack()

root.mainloop()