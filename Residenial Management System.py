
# --------------- IMPORT MODULES ---------------
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox as m_box
import sqlite3 as db
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont
import time
from pynput.mouse import Controller
import threading
import os
from tkcalendar import *
from datetime import datetime, date
import os
import re
import random
import smtplib
import clipboard

# import datetime
# from PIL import Image, ImageFilter, ImageDraw, ImageFont

# --------------- MAIN SCREEN ---------------

root = Tk()
root.title("Dark Town")
root.iconbitmap("Icon.ico")
root.configure(background="#242936")
# root.configure(background="#ffffff")
root.wm_attributes('-fullscreen','true')

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  # <-- move focus to this widget

global dark_color
dark_color = "#0c0d15"

stl = ttk.Style()
stl.configure("Treeview",
    background="#fff")
stl.map("Treeview",
    foreground=[('selected', '#fff')],
    background=[('selected', dark_color)])

tree_view_frame = Frame(root, bg=dark_color)
tree_view_frame.place(rely=0.314, relx=0.3485)

tv = ttk.Treeview(tree_view_frame, height=20, selectmode="extended",
                    column=('cia', 'Name', 'Surname', 'Age', 'Address', 'Booking Unit', 'Contact', 'CNIC', 'Date/Time'))
telling_no_data = StringVar(root)

telling_no_data_label = Label(tv, fg="gray45", bg="#ffffff",textvar=telling_no_data, font=("Calibri", 13))
check_login = False
# check_login = True

local_font = Font(family="Maiandra GD", weight="bold", size=13)

# --------------- BACKEND -------------------
conn = db.connect("Dark Town Database.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS DATA
    (
        cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Name Text,
        Surname Text,
        Age Text,
        Address Text,
        BookingUnit Text,
        Contact Text,
        CNIC Text,
        Time Text
    )''')
cur.execute('''CREATE TABLE IF NOT EXISTS SETTINGUP
    (
        cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        AdminName Text,
        AdminAddress Text,
        Email Text,
        LoginUsername Text,
        LoginPassword Text,
        AdminContact Text,
        AdminCNIC Text,
        Time Text
    )''')

# --------------- FUNCTIONS --------------- #

def submit(*args):
    SEARCH.set("")

    conn = db.connect("Dark Town Database.db")
    cur = conn.cursor()
    name = name_value.get()
    s_name = surname_value.get()
    age = age_value.get()
    ad = address_value.get()
    b_u = booking_unit_value.get()
    c_v = contact_value.get()
    c_num = cnic_value.get()
    time = getdate()
    c_v = c_v.replace(" ","")
    c_num = c_num.replace(" ","")
    
    if name == '' or s_name == '' or ad == '' or b_u =='' or c_v == '' or c_num == '' or age == '':
        m_box.showerror("Error", "Fill up the feild(s).")

    else:
        try:
            age = int(age)
            c_num = int(c_num)
            c_v = int(c_v)

        except ValueError:
            m_box.showerror('Error', 'Age, Contact and CNIC number must be only in numerals.')

        else:
            c_v = str(c_v)
            c_num = str(c_num)
            name = name.replace(" ","")
            s_name = s_name.replace(" ","")

            check_exists = cur.execute("""SELECT EXISTS (SELECT 1 
                                                 FROM DATA 
                                                 WHERE CNIC=?)""", (c_num, )).fetchone()[0]

            if name.isdigit() >= name.isalpha():
                m_box.showerror('Error', 'Username must be in letters.')

            elif s_name.isdigit() >= s_name.isalpha():
                m_box.showerror('Error', 'Surname must be in letters.')

            elif len(name.replace(" ",""))<3 or len(name.replace(" ",""))>15:
                m_box.showerror('Error', 'Username has at least 3-15 characters.')

            elif len(s_name.replace(" ",""))<3 or len(s_name.replace(" ",""))>14:
                m_box.showerror('Error', 'Surname has at least 3-14 characters.')

            elif age < 18:
                m_box.showerror('Error', 'Age must above than 18.')

            elif age >= 101:
                m_box.showerror('Error', 'Age limit exceed.')

            elif len(ad.replace(" ",""))<6 or len(ad.replace(" ",""))>25:
                m_box.showerror('Error', 'Address has at least 6-25 characters.')

            elif len(b_u.replace(" ",""))<3 or len(b_u.replace(" ",""))>8:
                m_box.showerror('Error', 'Booking unit has at least 3-8 characters.')

            elif len(c_v)<8 or len(c_v)>14:
                m_box.showerror("Error", "Contact has at least 8-14 digits.")
            
            elif check_exists:
                m_box.showerror("Error", "CNIC number already exists.")

            elif len(c_num)<10 or len(c_num)>16:
                m_box.showerror("Error", "CNIC number has at least 10-16 digits.")

            else:
                name = name_value.get()
                s_name = surname_value.get()
                c_v = "+92-"+c_v

                telling_no_data_label.place_forget()
                print(f"{name} | {s_name} | {age} | {ad} | {c_v} | {c_num} | {time}")
                tv.delete(*tv.get_children())
                sqlite_insert_query = """INSERT INTO DATA(name, surname, age, address, bookingunit, contact, cnic, Time) 
                                        VALUES (?,?,?,?,?,?,?,?)"""

                cur.execute(sqlite_insert_query, (name, s_name, age, ad, b_u, c_v, c_num, time))
                cur.execute(f'''CREATE TABLE IF NOT EXISTS {name.replace(" ", "")+c_num.replace(" ", "")} 
                    (
                        cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Amount Text,
                        Date Text,
                        ReceiverName,
                        ReceiverCNIC,
                        Time Text
                    )''')

                cur.execute("SELECT * FROM `DATA` ORDER BY `cia` ASC")
                fetch = cur.fetchall()
                for data in fetch:
                    tv.insert('', 'end',
                                values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
                conn.commit()
                conn.close()

                m_box.showinfo('Added', 'Data has been added.')

                name_value.set("")
                surname_value.set("")
                age_value.set("")
                address_value.set("")
                booking_unit_value.set("")
                contact_value.set("")
                cnic_value.set("")

cur.close()
conn.commit()
conn.close()

def getdate():
    return time.asctime(time.localtime(time.time()))

# def generate_num_send_email(otp):
    conn = db.connect("Dark Town Database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM SETTINGUP ORDER BY `cia` ASC")
    fetch = cur.fetchall()
    for data in fetch:
        getting_email = data[3]
    conn.commit()
    cur.close()
    conn.close()

    otp=""
    for i in range(4):
        otp+=str(random.randint(1,9))
    # print (otp)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("youremail", "yourpassword")
    server.sendmail(f"youremail", getting_email, f"Subject:Your Verification Code\n\n{otp}")
    server.close()


def clear(*args):
    clear_button.config(text="Clear")

    search.configure(state=NORMAL, bg="#ffffff")
    
    btn_search.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
    btn_search.bind("<Enter>", search_button_hover)
    btn_search.bind("<Leave>", search_button_left)
    
    btn_reset.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
    btn_reset.bind("<Enter>", reset_button_hover)
    btn_reset.bind("<Leave>", reset_button_left)    

    name_value.set("")
    surname_value.set("")
    age_value.set("")
    address_value.set("")
    booking_unit_value.set("")
    contact_value.set("")
    cnic_value.set("")
    
    update.config(state=DISABLED, bg=dark_color, cursor="X_cursor")
    update.bind("<Enter>", "")
    update.bind("<Leave>", "")

    def sub_hover(event):
        submit_button.config(
            font=buttons_font,
            bg='#ffffff',
            fg='#00e5ff'
        )

    def sub_left(event):
        submit_button.config(
            font=buttons_font,
            bg='#00e5ff',
            fg='#ffffff'
        )

    submit_button.config(state=NORMAL, bg="#00e5ff", cursor="hand2")
    submit_button.bind("<Enter>", sub_hover)
    submit_button.bind("<Leave>", sub_left)

def selectedRows(event):
    SEARCH.set("")

    for i in tv.get_children():
        curItem = tv.focus()
        contents = (tv.item(curItem))
        selecteditem = contents['values']
        if (len(selecteditem)) == 0:
            print("Clicked Treeview panel")
        else:
            print("Clicked on record")
            search.configure(state=DISABLED)
            btn_search.configure(state=DISABLED, bg=dark_color, cursor="X_cursor")
            btn_search.bind("<Enter>", "")
            btn_search.bind("<Leave>", "")
            
            btn_reset.configure(state=DISABLED, bg=dark_color, cursor="X_cursor")
            btn_reset.bind("<Enter>", "")
            btn_reset.bind("<Leave>", "")

            curItem = tv.focus()
            contents = (tv.item(curItem))
            selecteditem = contents['values']
            name_value.set("")
            surname_value.set("")
            age_value.set("")
            address_value.set("")
            contact_value.set("")
            cnic_value.set("")

            name_value.set(selecteditem[1])
            surname_value.set(selecteditem[2])
            age_value.set(selecteditem[3])
            address_value.set(selecteditem[4])
            booking_unit_value.set(selecteditem[5])
            contact_value.set(selecteditem[6].replace("+92-",""))
            cnic_value.set(selecteditem[7])

            def more_buttons_hover_update(event):
                update.configure(font=buttons_font, fg="#00e5ff", bg="#ffffff")

            def more_buttons_left_update(event):
                update.configure(font=buttons_font, bg="#00e5ff", fg="#ffffff")

            update.config(state=NORMAL, bg="#00e5ff", cursor="hand2")
            update.bind("<Enter>", more_buttons_hover_update)
            update.bind("<Leave>", more_buttons_left_update)

            clear_button.config(text="Cancel")

            submit_button.config(state=DISABLED, bg=dark_color, cursor="X_cursor")
            submit_button.bind("<Enter>", "")
            submit_button.bind("<Leave>", "")

            root.bind("<Control-U>", Update)
            root.bind("<Control-u>", Update)

def Update(*args):
    global cia
    curItem = tv.focus()
    contents = (tv.item(curItem))
    selecteditem = contents['values']
    cia = selecteditem[0]
    conn = db.connect("Dark Town Database.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS DATA
        (
            cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Name Text,
            Surname Text,
            Age Text,
            Address Text,
            BookingUnit Text,
            Contact Text,
            CNIC Text,
            Time Text
        )''')
    name = name_value.get()
    s_name = surname_value.get()
    age = age_value.get()
    ad = address_value.get()
    b_u = booking_unit_entry.get()
    c_v = contact_value.get()
    c_num = cnic_value.get()
    time = getdate()
    c_v = c_v.replace(" ","")
    c_num = c_num.replace(" ","")

    if name == '' or s_name == '' or ad == '' or c_v == '' or c_num == '' or age == '':
        m_box.showerror("Error", "Fill up the field(s).")
    else:
        try:
            age = int(age)
            c_num = int(c_num)
            c_v = int(c_v)

        except ValueError:
            m_box.showerror('Error', 'Age, Contact and CNIC number must be only in numerals.')

        else:
            c_v = str(c_v)
            c_num = str(c_num)
            name = name.replace(" ","")
            s_name = s_name.replace(" ","")

            if name.isdigit() >= name.isalpha():
                m_box.showerror('Error', 'Username must be in letters.')

            elif s_name.isdigit() >= s_name.isalpha():
                m_box.showerror('Error', 'Surname must be in letters.')

            elif len(name.replace(" ",""))<3 or len(name.replace(" ",""))>15:
                m_box.showerror('Error', 'Username has at least 3-15 characters.')

            elif len(s_name.replace(" ",""))<3 or len(s_name.replace(" ",""))>14:
                m_box.showerror('Error', 'Surname has at least 3-14 characters.')

            elif age < 18:
                m_box.showerror('Error', 'Age must above than 18.')

            elif age >= 101:
                m_box.showerror('Error', 'Age limit exceed.')
            
            elif len(ad.replace(" ",""))<6 or len(ad.replace(" ",""))>25:
                m_box.showerror('Error', 'Address has at least 6-25 characters.')

            elif len(b_u.replace(" ",""))<3 or len(b_u.replace(" ",""))>8:
                m_box.showerror('Error', 'Booking unit has at least 3-8 characters.')

            elif len(c_v)<8 or len(c_v)>14:
                m_box.showerror("Error", "Contact has at least 8-14 digits.")
    
            elif len(c_num)<10 or len(c_num)>16:
                m_box.showerror("Error", "CNIC number has at least 10-16 digits.")

            else:
                root.bind("<Control-U>", "")
                root.bind("<Control-u>", "")

                name = name_value.get()
                s_name = surname_value.get()
                c_v = "+92-"+c_v

                search.configure(state=NORMAL, bg="#ffffff")
                
                btn_search.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
                btn_search.bind("<Enter>", search_button_hover)
                btn_search.bind("<Leave>", search_button_left)
                
                btn_reset.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
                btn_reset.bind("<Enter>", reset_button_hover)
                btn_reset.bind("<Leave>", reset_button_left)

                print(f"{name} | {s_name} | {age} | {ad} | {c_v} | {c_num} | {time}")
                tv.delete(*tv.get_children())
                cur.execute(
                    "UPDATE `DATA` SET `name` = ?, `surname` = ?, `age` = ?, `address` = ?, `bookingunit` =?, `contact` = ?, `cnic` = ?, time = ? WHERE cia = ?",
                    (
                    str(name), str(s_name), str(age), str(ad), str(b_u),
                    str(c_v), str(c_num), time, int(cia)))

                def to_show():
                    cur.execute("SELECT * FROM `DATA` ORDER BY `cia` ASC")
                    fetch = cur.fetchall()
                    for data in fetch:
                        tv.insert('', 'end',
                                    values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
                    cur.close()
                    conn.close()
                    name_value.set("")
                    surname_value.set("")
                    age_value.set("")
                    address_value.set("")
                    booking_unit_value.set("")
                    contact_value.set("")
                    cnic_value.set("")

                    root.focus()
                    # update.bind("<Return>", None)
                    m_box.showinfo('Updated', 'Record has been updated.')

                    clear_button.config(text="Clear")

                    update.config(state=DISABLED, bg=dark_color, cursor="X_cursor")
                    update.bind("<Enter>", "")
                    update.bind("<Leave>", "")
                    def sub_hover(event):
                        submit_button.config(
                            font=buttons_font,
                            bg='#ffffff',
                            fg='#00e5ff'
                        )

                    def sub_left(event):
                        submit_button.config(
                            font=buttons_font,
                            bg='#00e5ff',
                            fg='#ffffff'
                        )

                    submit_button.config(state=NORMAL, bg="#00e5ff", cursor="hand2")
                    submit_button.bind("<Enter>", sub_hover)
                    submit_button.bind("<Leave>", sub_left)

                # if name != selecteditem[1] or c_num != selecteditem[7]:
                try:
                    test = selecteditem[1].replace(" ", "")+str(selecteditem[7]).replace(" ", "")
                    print(test)
                    best = name.replace(" ", "")+c_num.replace(" ", "")
                    cur.execute(f"ALTER TABLE {test} RENAME TO {best}")
                    conn.commit()
                    to_show()
                
                except:
                    to_show()


def Delete_all(*args):
    if tv.selection():
        result = m_box.askquestion("Delete All", "Are you sure you want to delete all record?",
                                    icon="warning")
        if result == "yes":
            # telling_no_data_label.place(rely=0.1, relx=0.5, anchor=CENTER)  
            telling_no_data_label.place(rely=0.5, relx=0.5, anchor=CENTER)              
            telling_no_data.set("No Data Found")
            tv.delete(*tv.get_children())
            conn = db.connect("Dark Town Database.db")
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS DATA
                (
                    cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Name Text,
                    Surname Text,
                    Age Text,
                    Address Text,
                    BookingUnit Text,
                    Contact Text,
                    CNIC Text,
                    Time Text
                )''')
            query = "SELECT Name,CNIC FROM `DATA`"
            cur.execute(query)
            ids = cur.fetchall()
            list = []

            for rov in ids:
                rov = str(rov).replace('(', '')
                rov = str(rov).replace(')', '')
                rov = str(rov).replace(',', '')
                rov = str(rov).replace("'", '')
                rov = str(rov).replace(' ', '')
                list.append(rov)
            for i in list:
                cur.execute(f"DROP table `{i}`")
            
            cur.execute("DELETE FROM `DATA` WHERE `cia`")
            conn.commit()
            cur.close()
            conn.close()

            name_value.set("")
            surname_value.set("")
            age_value.set("")
            address_value.set("")
            booking_unit_value.set("")
            contact_value.set("")
            cnic_value.set("")

            Reset()

            update.config(state=DISABLED, bg=dark_color, cursor="X_cursor")
            update.bind("<Enter>", "")
            update.bind("<Leave>", "")

            def sub_hover(event):
                submit_button.config(
                    font=buttons_font,
                    bg='#ffffff',
                    fg='#00e5ff'
                )

            def sub_left(event):
                submit_button.config(
                    font=buttons_font,
                    bg='#00e5ff',
                    fg='#ffffff'
                )

            submit_button.config(state=NORMAL, bg="#00e5ff", cursor="hand2")
            submit_button.bind("<Enter>", sub_hover)
            submit_button.bind("<Leave>", sub_left)
            
            search.configure(state=NORMAL, bg="#ffffff")
    
            btn_search.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
            btn_search.bind("<Enter>", search_button_hover)
            btn_search.bind("<Leave>", search_button_left)
            
            btn_reset.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
            btn_reset.bind("<Enter>", reset_button_hover)
            btn_reset.bind("<Leave>", reset_button_left)

            m_box.showinfo("Info", "Records has been deleted.")
            return None
    else:
        m_box.showerror("Error", "At least select one record to delete all records.")

def Delete_selected(*args):
    if tv.selection():
        result = m_box.askquestion('Delete', 'Are you sure you want to delete this record?',
                                    icon="warning")
        if result == 'yes':
            conn = db.connect("Dark Town Database.db")
            ccur = conn.cursor()
            ccur.execute(''' SELECT COUNT(*) FROM DATA ''')
            if ccur.fetchone()[0]!=1:
                telling_no_data_label.place_forget()
            else:
                # telling_no_data_label.place(rely=0.1, relx=0.5, anchor=CENTER)        
                telling_no_data_label.place(rely=0.5, relx=0.5, anchor=CENTER)        
                telling_no_data.set("No Data Found")
            curItem = tv.focus()
            contents = (tv.item(curItem))
            selecteditem = contents['values']
            tv.delete(curItem)
            conn = db.connect("Dark Town Database.db")
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS DATA
                (
                    cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    Name Text,
                    Surname Text,
                    Age Text,
                    Address Text,
                    BookingUnit Text,
                    Contact Text,
                    CNIC Text,
                    Time Text
                )''')
            cur.execute("DELETE FROM `DATA` WHERE `cia` = %d" % selecteditem[0])
            deleting_amount_table = selecteditem[1].replace(" ","")+str(selecteditem[7]).replace(" ","")
            cur.execute(f"DROP table {deleting_amount_table}")
            conn.commit()
            cur.close()
            conn.close()

            name_value.set("")
            surname_value.set("")
            age_value.set("")
            address_value.set("")
            booking_unit_value.set("")
            contact_value.set("")
            cnic_value.set("")

            Reset()

            update.config(state=DISABLED, bg=dark_color, cursor="X_cursor")
            update.bind("<Enter>", "")
            update.bind("<Leave>", "")

            def sub_hover(event):
                submit_button.config(
                    font=buttons_font,
                    bg='#ffffff',
                    fg='#00e5ff'
                )

            def sub_left(event):
                submit_button.config(
                    font=buttons_font,
                    bg='#00e5ff',
                    fg='#ffffff'
                )

            submit_button.config(state=NORMAL, bg="#00e5ff", cursor="hand2")
            submit_button.bind("<Enter>", sub_hover)
            submit_button.bind("<Leave>", sub_left)
            
            search.configure(state=NORMAL, bg="#ffffff")

            btn_search.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
            btn_search.bind("<Enter>", search_button_hover)
            btn_search.bind("<Leave>", search_button_left)
            
            btn_reset.configure(state=NORMAL, cursor="hand2", bg="#00e5ff")
            btn_reset.bind("<Enter>", reset_button_hover)
            btn_reset.bind("<Leave>", reset_button_left)
            
            m_box.showinfo("Info", "Selected record has been deleted.")
            return None
    else:
        m_box.showerror("Error", "Select the record which you want to delete.")
        return displaydata()

def Search(*args):
    if SEARCH.get() == "":
        Reset()
    else:
        conn = db.connect("Dark Town Database.db")
        cursor = conn.cursor()
        tv.delete(*tv.get_children())
        cursor.execute("SELECT * FROM DATA ORDER BY cia ASC ")
        tv.delete(*tv.get_children())
        conn = db.connect("Dark Town Database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DATA WHERE Name LIKE ? OR Surname LIKE ? OR Age LIKE ? OR BookingUnit LIKE ? OR Contact LIKE ? OR CNIC LIKE ?",
                        (str(SEARCH.get()), str(SEARCH.get()), str(SEARCH.get()), str(SEARCH.get()),"+92-"+str(SEARCH.get().replace("+92-", "")), str(SEARCH.get())))
        fetch = cursor.fetchall()
        print(fetch)
        for data in fetch:
            tv.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
        cursor.close()
        conn.close()

def Reset(*args):
    SEARCH.set("")
    conn = db.connect("Dark Town Database.db")
    cursor = conn.cursor()
    tv.delete(*tv.get_children())
    cursor.execute("SELECT * FROM DATA ORDER BY cia ASC ")
    fetch = cursor.fetchall()
    for data in fetch:
        tv.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
    cursor.close()
    conn.close()

def displaydata():
    conn = db.connect("Dark Town Database.db")
    ccur = conn.cursor()
    ccur.execute(''' SELECT COUNT(*) FROM DATA ''')

    if ccur.fetchone()[0]>=1:
        telling_no_data_label.place_forget()
        root.update()
        tv.delete(*tv.get_children())
        conn = db.connect("Dark Town Database.db")
        cur = conn.cursor()
        query = "SELECT * FROM `DATA` ORDER BY `cia` ASC"

        cur.execute(query)
        data = cur.fetchall()
        for row in data:
            tv.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        conn.close()
    else:
        telling_no_data.set("No Data Found")
        # telling_no_data_label.place(rely=0.1, relx=0.5, anchor=CENTER)        
        telling_no_data_label.place(rely=0.5, relx=0.5, anchor=CENTER)        

        root.update()
def add_payment(*args):
    if tv.selection():
        clear()
        btn_display_payment.configure(state=DISABLED, cursor="X_cursor")
        btn_add_payment.configure(state=DISABLED, cursor="X_cursor")
        delete_selected.configure(state=DISABLED, cursor="X_cursor")
        delete_all.configure(state=DISABLED, cursor="X_cursor")

        root.focus()
        add_payment_frame = Frame(bg=dark_color, height=320, width=450, highlightbackground = "#00e5ff", highlightthickness=5)
        add_payment_frame.place(anchor=CENTER, rely=0.5, relx=0.5)

        mouse = Controller()
        mouse.position = (705, 425)
        tree_view_frame.place_forget()

        def hide_add_payment_frame():
            add_payment_frame.place_forget()
            displaydata()
            tree_view_frame.place(rely=0.314, relx=0.3485)
            btn_add_payment.configure(state=NORMAL, cursor="hand2")
            btn_display_payment.configure(state=NORMAL, cursor="hand2")
            btn_add_payment.configure(state=NORMAL, cursor="hand2")
            delete_selected.configure(state=NORMAL, cursor="hand2")
            delete_all.configure(state=NORMAL, cursor="hand2")

            btn_add_payment.focus()

        def add_payment_frame_submit(*args):
            getting_receiver_name = receiver_name_choosen.get()
            getting_receiver_cnic = value_of_receiver_cnic.get()

            # receiver_name_choosen['values']+= (getting_receiver_name,)
            # receiver_cnic_choosen['values']+= (getting_receiver_cnic,)

            # cur.execute('''INSERT INTO CHOOSE (ReceiverName, ReceiverCNIC) VALUES(?,?)''', (getting_receiver_name, getting_receiver_cnic))
            # cur.close()
            # conn.commit()
            # conn.close()

            amount = amount_value.get()
            date = show_date.cget("text")
            time = getdate()
            
            if amount == '' or date == '' or getting_receiver_name == '' or getting_receiver_cnic == '':
                m_box.showerror("Error", "Fill up the feild(s).")

            else:
                try:
                    amount = int(amount)
                    getting_receiver_cnic = int(getting_receiver_cnic)
                except ValueError:
                    m_box.showerror('Error', 'Amount and CNIC number must be only in numerals.')

                else:
                    amount = str(amount)
                    date = str(date)
                    getting_receiver_name = str(getting_receiver_name)
                    getting_receiver_cnic = str(getting_receiver_cnic)

                    if len(amount)<4 or len(amount)>10:
                        m_box.showerror('Error', 'Amount must be in 4-10 characters.')

                    # elif len(date)<4 or len(date)>14:
                    #     m_box.showerror('Error', 'Must have 4 characters of "Day", "Month", "Year".')
                    elif getting_receiver_name.isdigit() >= getting_receiver_name.isalpha():
                        m_box.showerror('Error', 'Receiver name must be in letters.')

                    elif len(getting_receiver_name)<3 or len(getting_receiver_name)>15:
                        m_box.showerror('Error', 'Receiver name must be in 3-15 characters.')

                    elif len(getting_receiver_cnic)<10 or len(getting_receiver_cnic)>16:
                        m_box.showerror('Error', 'CNIC number must be in 10-16 characters.')

                    else:
                        conn = db.connect("Dark Town Database.db")
                        cur = conn.cursor()
                        cur.execute('''CREATE TABLE  IF NOT EXISTS CHOOSE
                            (
                                "ReceiverName" TEXT,
                                "ReceiverCNIC" TEXT
                            )'''
                        )

                        # receiver_name_choosen['values']+= (getting_receiver_name,)
                        # receiver_cnic_choosen['values']+= (getting_receiver_cnic,)

                        cur.execute('''INSERT INTO CHOOSE (ReceiverName, ReceiverCNIC) VALUES(?,?)''', (getting_receiver_name, getting_receiver_cnic))
                        cur.close()
                        conn.commit()
                        conn.close()

                        conn = db.connect("Dark Town Database.db")
                        cur = conn.cursor()
                        cur.execute(f'''CREATE TABLE IF NOT EXISTS {selecteditem[1].replace(" ", "")+str(selecteditem[7]).replace(" ", "")} 
                            (
                                cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                Amount Text,
                                Date Text,
                                ReceiverName,
                                ReceiverCNIC,
                                Time Text
                            )''')

                        amount = amount_value.get()
                        date = show_date.cget("text")

                        telling_no_data_label.place_forget()
                        print(f"{amount} | {date} | {time}")
                        tv.delete(*tv.get_children())
                        sqlite_insert_query = f"""INSERT INTO {selecteditem[1].replace(" ", "")+str(selecteditem[7]).replace(" ", "")}(amount, date, ReceiverName, ReceiverCNIC,time) 
                                                VALUES (?,?,?,?,?)"""

                        cur.execute(sqlite_insert_query,(amount, date, getting_receiver_name, getting_receiver_cnic,time))

                        conn.commit()
                        cur.close()
                        conn.close()

                        # conn = db.connect("Dark Town Database.db")
                        # cur = conn.cursor()
                        # query = "SELECT * FROM `SETTINGUP` ORDER BY `cia` ASC"

                        # cur.execute(query)
                        # data = cur.fetchall()
                        # for row in data:
                        #     admin_name_for_receipt = row[1]
                        #     admin_cnic_for_receipt =row[7]
                        # conn.close()
                            
                        m_box.showinfo('Added', 'Data has been added, Please wait until "Receipt" generate.')

                        hide_add_payment_frame()

                        if not os.path.exists('All_Receipts'):
                            os.makedirs('All_Receipts')
                        folder_locating = (f"All_Receipts\\{selecteditem[1]}_{selecteditem[2]}_{selecteditem[5]}_Receipts")
                        if not os.path.exists(folder_locating):
                            os.makedirs(folder_locating)

                        im = Image.new('RGB', (600, 400), (dark_color))

                        draw = ImageDraw.Draw(im)
                        draw.rectangle((20, 20, 580, 380), fill=(dark_color), outline=("#00e5ff"),  width=3)
                        draw.rectangle((30, 30, 570, 370), fill=(dark_color), outline=("#00e5ff"), width=3)
                        head_font = ImageFont.truetype("Fonts//Algerian Regular.ttf", 42)
                        draw.text((300, 83), "DARK TOWN", ("#ffffff"), font=head_font, anchor="ms")
                        draw.line((390, 313, 540, 313), fill="#ffffff", width=2)

                        global_font_semi_bold =  ImageFont.truetype("Fonts//MavenPro-SemiBold.ttf", 20)
                        global_font_medium = ImageFont.truetype("Fonts//MavenPro-Medium.ttf", 20)
                        global_font_comfortaa =  ImageFont.truetype("Fonts//Comfortaa-Medium.ttf", 18)

                        draw.text((75, 135), "Full Name:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
                        draw.text((215, 135), f"{selecteditem[1].capitalize()}", ("#ffffff"), font=global_font_medium, anchor="ls")
                        draw.line((215, 138, 430, 138), fill="#ffffff", width=2)

                        draw.text((75, 180), "Amount:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
                        draw.text((215, 180), f"{amount}", ("#ffffff"), font=global_font_medium, anchor="ls")
                        draw.line((215, 183, 430, 183), fill="#ffffff", width=2)

                        draw.text((75, 230), "Booking Unit:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
                        draw.text((215, 230), f"{selecteditem[5]}", ("#ffffff"), font=global_font_medium, anchor="ls")
                        draw.line((215, 233, 430, 233), fill="#ffffff", width=2)

                        draw.text((75, 280), "CNIC No:", ("#ffffff"), font=global_font_semi_bold, anchor="ls")
                        draw.text((215, 280), f"{selecteditem[7]}", ("#ffffff"), font=global_font_medium, anchor="ls")
                        draw.line((215, 283, 430, 283), fill="#ffffff", width=2)

                        date_font =  ImageFont.truetype("Fonts//Comfortaa-Medium.ttf", 15)

                        draw.text((45, 355), "Date:", ("#ffffff"), font=date_font, anchor="ls")
                        draw.text((92, 355), f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}", ("#ffffff"), font=date_font, anchor="ls")

                        draw.text((465, 335), f"{value_of_receiver_name.get()}", ("#ffffff"), font=global_font_comfortaa, anchor="ms")
                        draw.text((465, 360), f"{value_of_receiver_cnic.get()}", ("#ffffff"),font=global_font_comfortaa, anchor="ms")

                        import time

                        receipt_name = f"Receipt issued at {datetime.today().strftime('%Y-%m-%d-%H')+str(time.time())}"#:%M')}"

                        # receipt_name = f"Receipt issued at {time.time()}"#:%M')}"
                        
                        locating_receipt= f"All_Receipts\\{selecteditem[1]}_{selecteditem[2]}_{selecteditem[5]}_Receipts\\{receipt_name}.png"

                        open_receipt_folder_manually = m_box.askquestion(f'Open Folder', 'Want to see "'+selecteditem[1]+'" all Receipts',
                                            icon="info")
                        if open_receipt_folder_manually == 'yes':
                            os.startfile(folder_locating)
                        im.save(locating_receipt)

                        # img = Image.open(locating_receipt)
                        # img.show()
                        os.startfile(locating_receipt)


        def show_cal(*args):
            todays_date = date.today() 
            cal = Calendar(add_payment_frame, selectmode="day", year = todays_date.year, month = todays_date.month, 
                       day = todays_date.day, foreground="#00e5ff", background="#15171f", bordercolor="#242936",normalforeground="#ffffff",normalbackground="#15171f", headersbackground=dark_color, headersforeground="#00e5ff", weekendforeground= "#00e5ff", weekendbackground= dark_color, disableddaybackground="#15171f", disableddayforeground="#00e5ff", othermonthbackground="#242936", othermonthwebackground="#242936", selectbackground="#00e5ff", selectforeground="#ffffff")
            cal.place(rely=0.35, relx=0.32, anchor=CENTER)

            def close_cal(*args):
                add_payment_close_btn.configure(state=NORMAL, cursor="hand2")
                add_payment_submit_btn.configure(state=NORMAL, cursor="hand2")
                cal.place_forget()
                add_payment_cal_btn.configure(text="Select Date", width=9,command=show_cal)
                show_date.configure(text=cal.get_date())
                add_payment_cal_btn.bind("<Return>", show_cal)    
            
            add_payment_cal_btn.bind("<Return>", close_cal)    
            add_payment_close_btn.configure(state=DISABLED, cursor="X_cursor")
            add_payment_submit_btn.configure(state=DISABLED, cursor="X_cursor")
            add_payment_cal_btn.configure(text="Close", width=6,command=close_cal)

        def add_payment_close_hover(event):
            add_payment_close_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        def add_payment_close_left(event):
            add_payment_close_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        # def add_payment_clear_hover(event):
        #     add_payment_clear_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        # def add_payment_clear_left(event):
        #     add_payment_clear_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        def add_payment_submit_hover(event):
            add_payment_submit_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        def add_payment_submit_left(event):
            add_payment_submit_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        def add_payment_cal_btn_hover(event):
            add_payment_cal_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        def add_payment_cal_btn_left(event):
            add_payment_cal_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        for i in tv.get_children():
            curItem = tv.focus()
            contents = (tv.item(curItem))
            selecteditem = contents['values']
            curItem = tv.focus()
            contents = (tv.item(curItem))
            selecteditem = contents['values']

        getting_amount_label = Label(add_payment_frame, text="GETTING AMOUNT", bg=dark_color, fg="#ffffff",
                    font=("Algerian", 25))
        getting_amount_label.place(rely=0.1, relx=0.5, anchor=CENTER)

        add_payment_frame_details_font = Font(family="Arial rounded MT", weight="bold", size=23)

        name_label_add_payment_frame = Label(add_payment_frame, text=f"From {selecteditem[1]} For Unit {selecteditem[5]}", font=("Arial rounded MT", 12, "bold"), fg="#00e5ff", bg=dark_color)
        name_label_add_payment_frame.place(rely=0.205, relx=0.5, anchor=CENTER)
        
        receiver_cnic_label = Label(add_payment_frame, text="Receiver Name", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.305, relx=0.033)#.place(rely=0.56, relx=0.033)

        ttk.Style().configure('App.TCombobox', font=("Rockwell 11"))

        value_of_receiver_name = StringVar() 
        receiver_name_choosen = ttk.Combobox(add_payment_frame, style = "App.TCombobox",width = 20, textvariable =value_of_receiver_name, font=("Rockwell 11")) 
        receiver_name_choosen.place(rely=0.357, relx=0.713, anchor=CENTER)#.place(rely=0.6, relx=0.713, anchor=CENTER) 
        receiver_name_choosen.current() 

        receiver_cnic_label = Label(add_payment_frame, text="Receiver CNIC", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.418, relx=0.033)#.place(rely=0.65, relx=0.033)

        value_of_receiver_cnic = StringVar()
        receiver_cnic_choosen = ttk.Combobox(add_payment_frame, width = 20, textvariable = value_of_receiver_cnic) 
        receiver_cnic_choosen.place(rely=0.472, relx=0.713, anchor=CENTER)#.place(rely=0.71, relx=0.713, anchor=CENTER) 
        receiver_cnic_choosen.current() 

        # ----------- AMOUNT ------------
        amount_label = Label(add_payment_frame, text="Amount", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.535, relx=0.033)#.place(rely=0.305, relx=0.033)
        amount_value = StringVar(add_payment_frame)
        amount_entry = Entry(add_payment_frame, textvariable=amount_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17, relief=FLAT)
        amount_entry.place(rely=0.588, relx=0.713, anchor=CENTER)#.place(rely=0.326, relx=0.56)

        # ----------- DATE ------------
        date_label = Label(add_payment_frame, text="Date", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10,fg="#00e5ff").place(rely=0.65, relx=0.033)#.place(rely=0.414, relx=0.033)
        date_value = StringVar(add_payment_frame)

        add_payment_cal_btn = Button(add_payment_frame, text="Select Date", command=show_cal, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff", width=9, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        add_payment_cal_btn.place(rely=0.705, relx=0.713, anchor=CENTER) #.place(rely=0.47, relx=0.713, anchor=CENTER)
        add_payment_cal_btn.bind("<Return>", show_cal)
        add_payment_cal_btn.bind("<Enter>", add_payment_cal_btn_hover)
        add_payment_cal_btn.bind("<Leave>", add_payment_cal_btn_left)

        show_date = Label(add_payment_frame, text="", bg= dark_color, fg="#00e5ff", font=("Arial rounded MT", 11))
        show_date.place(rely=0.8, relx=0.713, anchor=CENTER)


        # def add_combobox_values_for_receiver_name():
        #     conn = db.connect("Dark Town Database.db")
        #     cur = conn.cursor()
        #     cur.execute('''CREATE TABLE  IF NOT EXISTS CHOOSE
        #         (
        #             "ReceiverName" TEXT,
        #             "ReceiverCNIC" TEXT
        #         )'''
        #     )

        #     getting_receiver_name = receiver_name_choosen.get()
        #     getting_receiver_cnic = value_of_receiver_cnic.get()

        #     receiver_name_choosen['values']+= (getting_receiver_name,)
        #     receiver_cnic_choosen['values']+= (getting_receiver_cnic,)

        #     cur.execute('''INSERT INTO CHOOSE (ReceiverName, ReceiverCNIC) VALUES(?,?)''', (getting_receiver_name, getting_receiver_cnic))
        #     cur.close()
        #     conn.commit()
        #     conn.close()

        def display_combobox_values_for_receiver_name(faiz, ziaz):
            conn = db.connect("Dark Town Database.db")
            cur = conn.cursor()
            cur.execute('''CREATE TABLE  IF NOT EXISTS CHOOSE
                (
                    "ReceiverName" TEXT,
                    "ReceiverCNIC" TEXT
                )'''
            )
            query = f"SELECT {faiz} FROM `CHOOSE`"

            cur.execute(query)
            ids = cur.fetchall()
            ziaz['values'] = ids

            cur.close()
            conn.commit()
            conn.close()

        # add_to_combobox_for_receiver_name = Button(add_payment_frame, text="Submit", command=add_combobox_values_for_receiver_name, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        #  # ttk.Button(add_payment_frame, text='add', command=add_combobox_values_for_receiver_name)
        # add_to_combobox_for_receiver_name.place(relx=0.6, rely=0.9, anchor=CENTER)
        display_combobox_values_for_receiver_name("ReceiverName", receiver_name_choosen)
        display_combobox_values_for_receiver_name("ReceiverCNIC", receiver_cnic_choosen)


        # add_payment_clear_btn = Button(add_payment_frame, text="Clear", command=hide_add_payment_frame, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        # add_payment_clear_btn.place(relx=0.6, rely=0.9, anchor=CENTER)
        # add_payment_clear_btn.bind("<Enter>", add_payment_clear_hover)
        # add_payment_clear_btn.bind("<Leave>", add_payment_clear_left)

        add_payment_submit_btn = Button(add_payment_frame, text="Submit", command=add_payment_frame_submit, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        add_payment_submit_btn.place(relx=0.8, rely=0.92, anchor=CENTER)
        add_payment_submit_btn.bind("<Enter>", add_payment_submit_hover)
        add_payment_submit_btn.bind("<Leave>", add_payment_submit_left)
    
        add_payment_close_btn = Button(add_payment_frame, text="Close", command=hide_add_payment_frame, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        add_payment_close_btn.place(relx=0.6, rely=0.92, anchor=CENTER)
        add_payment_close_btn.bind("<Enter>", add_payment_close_hover)
        add_payment_close_btn.bind("<Leave>", add_payment_close_left)

    else:
        m_box.showerror("Error", "Select the record which you want to Add Payment.")

def display_payment(*args):
    if tv.selection():
        try:
            clear()
            btn_display_payment.configure(state=DISABLED, cursor="X_cursor")
            btn_add_payment.configure(state=DISABLED, cursor="X_cursor")
            delete_selected.configure(state=DISABLED, cursor="X_cursor")
            delete_all.configure(state=DISABLED, cursor="X_cursor")
            root.focus()

            display_payment_frame = Frame(root,bg=dark_color, height=500, width=630, highlightbackground = "#00e5ff", highlightthickness=5)
            display_payment_frame.place(anchor=CENTER, rely=0.5, relx=0.5)

            tree_view_frame_display_all_payment = Frame(display_payment_frame)
            tv_display_all_payment = ttk.Treeview(tree_view_frame_display_all_payment, height=12, selectmode="extended",
                                column=('cia', 'Amount', 'Date', 'Received By', 'Receiver CNIC', 'Date/Time'))
            tree_view_frame.place_forget()
            tree_view_frame_display_all_payment.place(anchor=CENTER, rely=0.52, relx=0.5)
            scroll_bar_horizontal_display_all_payment = ttk.Scrollbar(tree_view_frame_display_all_payment, orient="horizontal",command=tv_display_all_payment.xview)
            scroll_bar_vertical_display_all_payment = ttk.Scrollbar(tree_view_frame_display_all_payment, orient="vertical",command=tv_display_all_payment.yview)
            tv_display_all_payment.configure(xscrollcommand=scroll_bar_horizontal_display_all_payment.set)
            tv_display_all_payment.configure(yscrollcommand=scroll_bar_vertical_display_all_payment.set)
            scroll_bar_horizontal_display_all_payment.pack(fill=X,side=BOTTOM)
            scroll_bar_vertical_display_all_payment.pack(fill=Y,side=RIGHT)

            tv_display_all_payment.heading('Amount', text="Amount", anchor="n")
            tv_display_all_payment.heading('Date', text="Date", anchor="n")
            tv_display_all_payment.heading('Received By', text="Received By", anchor="n")
            tv_display_all_payment.heading('Receiver CNIC', text="Receiver CNIC", anchor="n")
            tv_display_all_payment.heading('Date/Time', text="Date/Time", anchor="n")

            tv_display_all_payment.column('#0', minwidth=0, width=0, anchor='n')
            tv_display_all_payment.column('#1', minwidth=0, width=0, anchor='n')
            tv_display_all_payment.column('#2', minwidth=80, width=80, anchor='n')
            tv_display_all_payment.column('#3', minwidth=75, width=75, anchor='n')
            tv_display_all_payment.column('#4', minwidth=80, width=80, anchor='n')
            tv_display_all_payment.column('#5', minwidth=80, width=80, anchor='n')
            tv_display_all_payment.column('#6', minwidth=150, width=150, anchor='n')
            # style = ttk.Style(root)
            # ttk.Style().configure(".", font=('calibri', 11))
            # ttk.Style().configure("Heading", font=('Arial Rounded MT Bold', 12), foreground="#00e5ff",background=dark_color, bd=0)
            # style.configure("Name", highlightthickness=0, bd=0, font=('Calibri', 11))  # Modify the font of the body
            
            # tv_display_all_payment.bind("<Double-Button-1>", selectedRows)
            tv_display_all_payment.pack()

            telling_no_data_display_frame = StringVar(root)
            # telling_no_data_label_display_frame.pack()
            telling_no_data_label_display_frame = Label(tv_display_all_payment, fg="gray45", bg="#ffffff",textvar=telling_no_data_display_frame, font=("Calibri", 13))
            telling_no_data_label_display_frame.place(rely=0.5, relx=0.5)
            # tree_view_frame_display_all_payment = Frame(display_payment_frame, bg="#ffffff")
            # tree_view_frame_display_all_payment.place(rely=0.314, relx=0.390553)

            mouse = Controller()
            mouse.position = (705, 425)
            tree_view_frame.place_forget()
        except Exception as e:
            raise e
            print(e)

        for i in tv.get_children():
            curItem = tv.focus()
            contents = (tv.item(curItem))
            selecteditem = contents['values']
            curItem = tv.focus()
            contents = (tv.item(curItem))
            selecteditem = contents['values']

        def hide_display_payment_frame():
            display_payment_frame.place_forget()
            tree_view_frame.place(rely=0.314, relx=0.3485)
            update_payment_frame.place_forget()
            displaydata()
            btn_display_payment.configure(state=NORMAL, cursor="hand2")
            btn_add_payment.configure(state=NORMAL, cursor="hand2")
            delete_selected.configure(state=NORMAL, cursor="hand2")
            delete_all.configure(state=NORMAL, cursor="hand2")

            btn_display_payment.focus()

        def display_all_payment():
            conn = db.connect("Dark Town Database.db")
            ccur = conn.cursor()
            ccur.execute(f''' SELECT COUNT(*) FROM {selecteditem[1].replace(" ", "")+str(selecteditem[7]).replace(" ", "")} ''')

            if ccur.fetchone()[0]>=1:
                telling_no_data_label_display_frame.place_forget()
                root.update()
                tv_display_all_payment.delete(*tv_display_all_payment.get_children())
                conn = db.connect("Dark Town Database.db")
                cur = conn.cursor()
                sub_query = selecteditem[1].replace(" ", "")+str(selecteditem[7]).replace(" ", "")
                query = f"SELECT * FROM `{sub_query}` ORDER BY `cia` ASC"

                cur.execute(query)
                data = cur.fetchall()
                for row in data:
                    tv_display_all_payment.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5]))
                conn.close()
            else:
                telling_no_data_display_frame.set("No Data Found")
                telling_no_data_label_display_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

        def selected_display_row(*args):
            for i in tv_display_all_payment.get_children():
                curItem = tv_display_all_payment.focus()
                contents = (tv_display_all_payment.item(curItem))
                selecteditem = contents['values']
                curItem = tv_display_all_payment.focus()
                contents = (tv_display_all_payment.item(curItem))
                selecteditem = contents['values']
                if (len(selecteditem)) == 0:
                    print("Clicked Treeview panel")
                else:
                    def faiz(*args):
                        amount_value = StringVar(update_payment_frame)
                        amount_value.set(selecteditem[1])

                        show_date = Label(update_payment_frame, text="", bg= dark_color, fg="#00e5ff", font=("Arial rounded MT", 11))
                        show_date.configure(text=f"{selecteditem[2]}")

                        value_of_receiver_name = StringVar() 

                        value_of_receiver_cnic = StringVar()

                        update_payment_frame.place(anchor=CENTER, rely=0.5, relx=0.5)

                        mouse = Controller()
                        mouse.position = (705, 425)
                        
                        # tree_view_frame.place_forget()

                        # def hide_add_payment_frame():
                        #     add_payment_frame.place_forget()
                        #     tree_view_frame.place(rely=0.314, relx=0.390553)
                             # displaydata()
                                    # hide_add_payment_frame()

                        def hide_update_payment_frame(*args):
                            update_payment_frame.place_forget()
                            display_payment_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


                        def update_display_payment(*args):
                            for i in tv.get_children():
                                curItem_getting_name = tv.focus()
                                contents_getting_name = (tv.item(curItem_getting_name))
                                selecteditem_getting_name = contents_getting_name['values']
                                curItem_getting_name = tv.focus()
                                contents_getting_name = (tv.item(curItem_getting_name))
                                selecteditem_getting_name = contents_getting_name['values'][1].replace(" ", "") + str(contents_getting_name['values'][7]).replace(" ", "")
                            global cia
                            curItem = tv_display_all_payment.focus()
                            contents = (tv_display_all_payment.item(curItem))
                            selecteditem = contents['values']
                            cia = selecteditem[0]
                            conn = db.connect("Dark Town Database.db")
                            cur = conn.cursor()
                            cur.execute(f'''CREATE TABLE IF NOT EXISTS {selecteditem_getting_name}
                                (
                                cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                Amount Text,
                                Date Text,
                                ReceiverName,
                                ReceiverCNIC,
                                Time Text
                                )''')
            
                            getting_receiver_name = receiver_name_choosen.get()
                            getting_receiver_cnic = value_of_receiver_cnic.get()

                            amount = amount_value.get()
                            date = show_date.cget("text")
                            time = getdate()
                            if amount == '' or date == '':
                                m_box.showerror("Error", "Fill up the field(s).")
                            else:
                                try:
                                    amount = int(amount)
                                    getting_receiver_cnic = int(getting_receiver_cnic)

                                except ValueError:
                                    m_box.showerror('Error', 'Amount and CNIC number must be only in numerals.')

                                else:
                                    amount = str(amount)
                                    date = str(date)
                                    getting_receiver_name = str(getting_receiver_name)
                                    getting_receiver_cnic = str(getting_receiver_cnic)

                                    if len(amount)<4 or len(amount)>10:
                                        m_box.showerror('Error', 'Amount must be in thousand(s).')

                                    # elif len(date)<4 or len(date)>14:
                                    #     m_box.showerror('Error', 'Must have 4 characters of "Day", "Month", "Year".')

                                    elif getting_receiver_name.isdigit() >= getting_receiver_name.isalpha():
                                        m_box.showerror('Error', 'Receiver name must be in letters.')

                                    elif len(getting_receiver_name)<3 or len(getting_receiver_name)>15:
                                        m_box.showerror('Error', 'Receiver name must be in 3-15 characters.')

                                    elif len(getting_receiver_cnic)<10 or len(getting_receiver_cnic)>16:
                                        m_box.showerror('Error', 'CNIC number must be in 10-16 characters.')

                                    else:
                                        amount = amount_value.get()
                                        date = show_date.cget("text")
                                        # fff = str(selecteditem[1]).replace(" ", "")
                                        # print(fff)
                                        print(f"{amount} | {date} | {time}")
                                        tv_display_all_payment.delete(*tv_display_all_payment.get_children())

                                        cur.execute(
                                            f"UPDATE `{selecteditem_getting_name}` SET `amount` = ?, `date` = ?, `ReceiverName` = ?, `ReceiverCNIC` = ?,time = ? WHERE cia = ?",
                                            (
                                            str(amount), str(date), str(getting_receiver_name), str(getting_receiver_cnic), time, int(cia)))
                                        conn.commit()
                                        cur.execute(f"SELECT * FROM `{selecteditem_getting_name}` ORDER BY `cia` ASC")
                                        fetch = cur.fetchall()
                                        for data in fetch:
                                            tv_display_all_payment.insert('', 'end',
                                                        values=(data[0], data[1], data[2], data[3], data[4], data[5]))
                                        cur.close()
                                        conn.close()

                                        m_box.showinfo('Updated', 'Record has been updated.')
                                        hide_update_payment_frame()
                                        display_payment_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

                                        # tree_view_frame.place(rely=0.314, relx=0.3485)
                                        # displaydata()
                        def update_payment_cal_btn_hover(event):
                            update_payment_cal_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

                        def update_payment_cal_btn_left(event):
                            update_payment_cal_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

                        def update_payment_close_btn_hover(event):
                            update_payment_close_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

                        def update_payment_close_btn_left(event):
                            update_payment_close_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

                        def update_payment_btn_hover(event):
                            update_payment_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

                        def update_payment_btn_left(event):
                            update_payment_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

                        getting_amount_label = Label(update_payment_frame, text="UPDATING", bg=dark_color, fg="#ffffff",
                                    font=("Algerian", 25))
                        getting_amount_label.place(rely=0.1, relx=0.5, anchor=CENTER)

                        add_payment_frame_details_font = Font(family="Arial rounded MT", weight="bold", size=23)

                        for i in tv.get_children():
                            curItem_getting_name = tv.focus()
                            contents_getting_name = (tv.item(curItem_getting_name))
                            selecteditem_getting_name = contents_getting_name['values']
                
                        name_label_update_payment_frame = Label(update_payment_frame, text=f"Of {selecteditem_getting_name[1]} For Unit {selecteditem_getting_name[5]}", font=("Arial rounded MT", 12, "bold"), fg="#00e5ff", bg=dark_color)
                        name_label_update_payment_frame.place(rely=0.2, relx=0.5, anchor=CENTER)

                        receiver_cnic_label = Label(update_payment_frame, text="Receiver Name", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.305, relx=0.033)#.place(rely=0.56, relx=0.033)

                        receiver_name_choosen = ttk.Combobox(update_payment_frame, width = 20, textvariable = value_of_receiver_name) 
                        receiver_name_choosen.place(rely=0.357, relx=0.713, anchor=CENTER)#.place(rely=0.6, relx=0.713, anchor=CENTER) 
                        receiver_name_choosen.current() 

                        receiver_cnic_label = Label(update_payment_frame, text="Receiver CNIC", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.418, relx=0.033)#.place(rely=0.65, relx=0.033)

                        receiver_cnic_choosen = ttk.Combobox(update_payment_frame, width = 20, textvariable = value_of_receiver_cnic) 
                        receiver_cnic_choosen.place(rely=0.472, relx=0.713, anchor=CENTER)#.place(rely=0.71, relx=0.713, anchor=CENTER) 
                        receiver_cnic_choosen.current() 

                        # ----------- AMOUNT ------------
                        amount_label = Label(update_payment_frame, text="Amount", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.535, relx=0.033)
                        amount_entry = Entry(update_payment_frame, textvariable=amount_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17, relief=FLAT)
                        amount_entry.place(rely=0.588, relx=0.713, anchor=CENTER)

                        # ----------- DATE ------------
                        # def koko():
                        #     print("gas")
                        #     todays_date = date.today() 
                        #     cal = Calendar(update_payment_frame, selectmode="day", year = todays_date.year, month = todays_date.month, 
                        #                day = todays_date.day, foreground="#00e5ff", background="#15171f", bordercolor="#242936",normalforeground="#ffffff",normalbackground="#15171f", headersbackground=dark_color, headersforeground="#00e5ff", weekendforeground= "#00e5ff", weekendbackground= dark_color, disableddaybackground="#15171f", disableddayforeground="#00e5ff", othermonthbackground="#242936", othermonthwebackground="#242936", selectbackground="#00e5ff", selectforeground="#ffffff")
                        #     cal.place(rely=0.35, relx=0.32, anchor=CENTER)
                        #     google_bol_dop_art_vart.place_forget()
                            # google_bol_dop_art_vart.place_forget()
                        def show_cal(*args):
                            todays_date = date.today() 
                            cal = Calendar(update_payment_frame, selectmode="day", year = todays_date.year, month = todays_date.month, 
                                       day = todays_date.day, foreground="#00e5ff", background="#15171f", bordercolor="#242936",normalforeground="#ffffff",normalbackground="#15171f", headersbackground=dark_color, headersforeground="#00e5ff", weekendforeground= "#00e5ff", weekendbackground= dark_color, disableddaybackground="#15171f", disableddayforeground="#00e5ff", othermonthbackground="#242936", othermonthwebackground="#242936", selectbackground="#00e5ff", selectforeground="#ffffff")
                            cal.place(rely=0.35, relx=0.32, anchor=CENTER)

                            def close_cal(*args):
                                update_payment_close_btn.configure(state=NORMAL, cursor="hand2")
                                update_payment_btn.configure(state=NORMAL, cursor="hand2")
                                cal.place_forget()
                                update_payment_cal_btn.configure(text="Select Date", width=9,command=show_cal)
                                show_date.configure(text=cal.get_date())
                                update_payment_cal_btn.bind("<Return>", show_cal)
                                
                            update_payment_close_btn.configure(state=DISABLED, cursor="X_cursor")
                            update_payment_btn.configure(state=DISABLED, cursor="X_cursor")
                            update_payment_cal_btn.configure(text="Close", width=6,command=close_cal)

                        date_label = Label(update_payment_frame, text="Date", font=local_font, width=18, height=1, pady=5, bg=dark_color, padx=10, fg="#00e5ff").place(rely=0.65, relx=0.033)
                        date_value = StringVar(update_payment_frame)

                        update_payment_cal_btn.configure(command=show_cal)
                        update_payment_cal_btn.place(rely=0.705, relx=0.713, anchor=CENTER)

                        show_date.place(rely=0.8, relx=0.713, anchor=CENTER)

                        # def add_combobox_values_for_receiver_name():
                        #     conn = db.connect("Dark Town Database.db")
                        #     cur = conn.cursor()
                        #     cur.execute('''CREATE TABLE  IF NOT EXISTS CHOOSE
                        #         (
                        #             "ReceiverName" TEXT,
                        #             "ReceiverCNIC" TEXT
                        #         )'''
                        #     )

                        #     getting_receiver_name = receiver_name_choosen.get()
                        #     getting_receiver_cnic = value_of_receiver_cnic.get()

                        #     receiver_name_choosen['values']+= (getting_receiver_name,)
                        #     receiver_cnic_choosen['values']+= (getting_receiver_cnic,)

                        #     cur.execute('''INSERT INTO CHOOSE (ReceiverName, ReceiverCNIC) VALUES(?,?)''', (getting_receiver_name, getting_receiver_cnic))
                        #     cur.close()
                        #     conn.commit()
                        #     conn.close()

                        def display_combobox_values_for_receiver_name(faiz, ziaz):
                            conn = db.connect("Dark Town Database.db")
                            cur = conn.cursor()
                            cur.execute('''CREATE TABLE  IF NOT EXISTS CHOOSE
                                (
                                    "ReceiverName" TEXT,
                                    "ReceiverCNIC" TEXT
                                )'''
                            )
                            query = f"SELECT {faiz} FROM `CHOOSE`"

                            cur.execute(query)
                            ids = cur.fetchall()
                            ziaz['values'] = ids

                            cur.close()
                            conn.commit()
                            conn.close()

                        # add_to_combobox_for_receiver_name = Button(add_payment_frame, text="Submit", command=add_combobox_values_for_receiver_name, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
                        #  # ttk.Button(add_payment_frame, text='add', command=add_combobox_values_for_receiver_name)
                        # add_to_combobox_for_receiver_name.place(relx=0.6, rely=0.9, anchor=CENTER)
                        display_combobox_values_for_receiver_name("ReceiverName", receiver_name_choosen)
                        display_combobox_values_for_receiver_name("ReceiverCNIC", receiver_cnic_choosen)

                        update_payment_btn = Button(update_payment_frame, text="Update", command=update_display_payment, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
                        update_payment_btn.place(relx=0.8, rely=0.9, anchor=CENTER)
                        update_payment_btn.bind("<Enter>", update_payment_btn_hover)
                        update_payment_btn.bind("<Leave>", update_payment_btn_left)
                        update_payment_btn.configure(state=NORMAL, cursor="hand2")
                    
                        update_payment_close_btn = Button(update_payment_frame, text="Close", command=hide_update_payment_frame, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
                        update_payment_close_btn.place(relx=0.6, rely=0.9, anchor=CENTER)
                        update_payment_close_btn.bind("<Enter>", update_payment_close_btn_hover)
                        update_payment_close_btn.bind("<Leave>", update_payment_close_btn_left)
                        update_payment_close_btn.configure(state=NORMAL, cursor="hand2")

                    def login_fun(*args):     

                        conn = db.connect("Dark Town Database.db")
                        cur = conn.cursor()
                        query = "SELECT * FROM `SETTINGUP` ORDER BY `cia` ASC"

                        cur.execute(query)

                        data = cur.fetchall()
                        for row in data:
                            admin_cia_to_display  = row[0]
                            admin_name_to_display  = row[1]
                            admin_address_to_display  = row[2]
                            admin_email_to_display  = row[3]
                            admin_login_username_to_display  = row[4]
                            admin_login_password_to_display  = row[5]
                            admin_contact_to_display  = row[6].replace("+92-", "")
                            admin_cnic_to_display  = row[7]
                        conn.close()       
                        def click_login(*args):
                            admin_login_username_value_getting = admin_login_username_value.get()
                            admin_login_password_value_getting = admin_login_password_value.get()

                            if admin_login_username_value_getting == "" or admin_login_password_value_getting == "":
                                m_box.showerror('Error', "Fill up the field(s)")

                            elif admin_login_username_value_getting != admin_login_username_to_display:
                                m_box.showerror('Error', "Worng username")
                            
                            elif admin_login_password_value_getting != admin_login_password_to_display:
                                m_box.showerror('Error', "Worng password")
                            
                            else:
                                admin_login_username_value.set("")
                                admin_login_password_value.set("")
                                faiz()
                                global check_login
                                check_login = True
                                # settings_window()
                                root.update()
                                frame_for_login.place_forget()

                        def close_login(*args):
                            admin_login_username_value.set("")
                            admin_login_password_value.set("")
                            frame_for_login.place_forget()
                            display_payment_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
                            # display_payment_frame.place
                        
                        def forgot_password_func(*args):
                            def forget_password(*args):
                                getting_code = verify_email_enter_code_value.get()

                                if getting_code == '':
                                        m_box.showerror("Error", "Enter the verification code.")
                                    
                                elif getting_code != otp:
                                    m_box.showerror("Error", "Verification code doesn't match.")
                                else:
                                    verify_email_enter_code_entry.configure(state=DISABLED, cursor="X_cursor")
                                    verify_email_frame_heading.configure(text="Verified")
                                    message_label.configure(text=f"Password is {getting_password}")
                                    def copy_password(*args):
                                        clipboard.copy(getting_password)
                                        m_box.showinfo("Copied", "Password has copied." )
                                    m_box.showinfo("Verified", "Thanks for verifying." )
                                    verify_email_button.configure(text="Copy", command=copy_password)
                                    copy_password()
                                    # new_password_frame = Frame(root, height=220, width=420, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
                                    # new_password_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

                                    # new_password_frame_heading = Label(new_password_frame, justify=LEFT, text="Verify Now",
                                    #                     bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
                                    # new_password_enter_code_label = Label(new_password_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")
                                    # new_password_message_label = Label(new_password_frame, justify=CENTER, bg=dark_color, fg="#00e5ff", font=("Ebrima", 11))

                                    # new_password_enter_code_label = Label(new_password_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")

                                    # new_password_enter_code_value = StringVar(new_password_frame)
                                    # new_password_enter_code_entry = Entry(new_password_frame, textvariable=new_password_enter_code_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                                    #                     width=17)
                                    # new_password_button = Button(new_password_frame, text="Verify", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=6, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)#, 


                                    # new_password_frame_heading.place(rely=0.23, relx=0.5, anchor=CENTER)
                                    # new_password_enter_code_label.place(rely=0.45, relx=0.05)                
                                    # new_password_enter_code_entry.place(rely=0.487, relx=0.55)
                                    # new_password_button.place(rely=0.713, relx=0.7)

                            def close_forget_password(*args):
                                verify_email_frame.place_forget()
                                # settings_window()
                                display_payment_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

                            frame_for_login.place_forget()

                            conn = db.connect("Dark Town Database.db")
                            cur = conn.cursor()
                            cur.execute("SELECT * FROM SETTINGUP ORDER BY `cia` ASC")
                            fetch = cur.fetchall()
                            for data in fetch:
                                getting_email = data[3].replace(" ","")
                                getting_password = data[5]
                            conn.commit()
                            cur.close()
                            conn.close()

                            verify_email_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

                            verify_email_frame_heading.place(rely=0.138, relx=0.5, anchor=CENTER)

                            verify_email_enter_code_label.place(rely=0.35, relx=0.0)
                            # -----------ENTER CODE------------
                            verify_email_enter_code_entry.place(rely=0.387, relx=0.5)
                            
                            verify_change_email_button.bind("<Enter>", verify_change_email_button_hover)
                            verify_change_email_button.bind("<Leave>", verify_change_email_button_left)

                            message_label.configure(text=f"We sent a verification code on,\n {getting_email} also check spams")
                            message_label.place(rely=0.65, relx=0.5, anchor=CENTER)

                            verify_email_button.place(rely=0.795, relx=0.7)
                            verify_email_button.configure(command=forget_password)

                            verify_email_close_button.place(rely=0.795, relx=0.5)
                            verify_email_close_button.configure(command=close_forget_password)
                            # generate_num_send_email()

                            otp=""
                            for i in range(4):
                                otp+=str(random.randint(1,9))
                            # print (otp)
                            server = smtplib.SMTP("smtp.gmail.com", 587)
                            server.ehlo()
                            server.starttls()
                            server.login("youremail", "yourpassword")
                            server.sendmail(f"youremail", getting_email, f"Subject:Your Verification Code\n\n{otp}")
                            server.close()
                            # verific

                        display_payment_frame.place_forget()
                        frame_for_login.place(relx=0.5, rely=0.5, anchor=CENTER)

                                # -----------ADMIN NAME------------

                        login_heading.place(rely=0.135, relx=0.5, anchor=CENTER)

                        admin_login_username_name.place(rely=0.3, relx=0.05)
                        admin_login_username_entry.place(rely=0.337, relx=0.55)

                        # -----------BRANCH ADDRESS------------
                        admin_login_password_label.place(rely=0.47, relx=0.05)
                        admin_login_password_entry.place(rely=0.512, relx=0.55)

                        login_button.place(rely=0.77, relx=0.725)
                        login_button.configure(command=click_login)
                        login_button.bind("<Return>", click_login)

                        forgot_password_login_button.place(rely=0.77, relx=0.525)
                        forgot_password_login_button.configure(command=threading.Thread(target=forgot_password_func).start)
                        forgot_password_login_button.bind("<Return>", lambda event:threading.Thread(target=forgot_password_func).start)

                        close_login_button.place(rely=0.77, relx=0.322)
                        close_login_button.configure(command=close_login)
                        close_login_button.bind("<Return>", close_login)


                    display_payment_frame.place_forget()
                    if check_login == False:
                        login_fun()
                        
                    else:
                        faiz()

        def delete_selected_display_payment_frame(*args):
            if tv_display_all_payment.selection():
                result = m_box.askquestion('Delete', 'Are you sure you want to delete this record?',
                                            icon="warning")
                if result == 'yes':
                    for i in tv.get_children():         
                        curItem_getting_name = tv.focus()
                        contents_getting_name = (tv.item(curItem_getting_name))
                        selecteditem_getting_name = contents_getting_name['values']
                        print(selecteditem_getting_name)
                        selecteditem_getting_name = contents_getting_name['values'][1].replace(" ", "")+str(contents_getting_name['values'][7]).replace(" ", "")
                        print(selecteditem_getting_name)

                    conn = db.connect("Dark Town Database.db")
                    ccur = conn.cursor()
                    # global selecteditem
                    ccur.execute(f''' SELECT COUNT(*) FROM {selecteditem_getting_name} ''')

                    if ccur.fetchone()[0]!=1:
                        telling_no_data_label_display_frame.place_forget()
                    else:
                        # telling_no_data_label.place(rely=0.1, relx=0.5, anchor=CENTER)        
                        telling_no_data_label_display_frame.place(rely=0.5, relx=0.5, anchor=CENTER)        
                        telling_no_data_display_frame.set("No Data Found")
                        display_payment_delete_btn.configure(state=DISABLED, bg="#fff", cursor="X_cursor")
                        display_payment_delete_all_btn.configure(state=DISABLED, bg="#fff", cursor="X_cursor")

                    curItem = tv_display_all_payment.focus()
                    contents = (tv_display_all_payment.item(curItem))
                    selecteditem = contents['values']
                    tv_display_all_payment.delete(curItem)
                    conn = db.connect("Dark Town Database.db")
                    cur = conn.cursor()

                    cur.execute(f"DELETE FROM `{selecteditem_getting_name}` WHERE `cia` = %d" % selecteditem[0])
                    conn.commit()
                    cur.close()
                    conn.close()
                    m_box.showinfo("Info", "Selected record has been deleted.")
                    return None
            else:
                m_box.showerror("Error", "Select the record which you want to delete.")
                # return display_payment(*args)
                # display_all_payment()

        def delete_all_display_payment_frame(*args):
            if tv_display_all_payment.selection():
                result = m_box.askquestion('Delete', 'Are you sure you want to delete all record?',
                                            icon="warning")
                if result == 'yes':
                    telling_no_data_label_display_frame.place(rely=0.5, relx=0.5, anchor=CENTER)        
                    telling_no_data_display_frame.set("No Data Found")
                    for i in tv.get_children():         
                        curItem_getting_name = tv.focus()
                        contents_getting_name = (tv.item(curItem_getting_name))
                        selecteditem_getting_name = contents_getting_name['values']
                        curItem_getting_name = tv.focus()
                        contents_getting_name = (tv.item(curItem_getting_name))
                        selecteditem_getting_name = contents_getting_name['values'][1].replace(" ", "") + str(contents_getting_name['values'][7]).replace(" ", "")

                    tv_display_all_payment.delete(*tv_display_all_payment.get_children())

                    conn = db.connect("Dark Town Database.db")
                    cur = conn.cursor()

                    cur.execute(f"DELETE FROM `{selecteditem_getting_name}` WHERE `cia`")
                    conn.commit()
                    cur.close()
                    conn.close()

                    m_box.showinfo("Info", "All records has been deleted.")
                    return None
            else:
                m_box.showerror("Error", "At least select one record to delete all records.")

        def display_payment_close_hover(event):
            display_payment_close_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        def display_payment_close_left(event):
            display_payment_close_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        def display_payment_delete_hover(event):
            display_payment_delete_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        def display_payment_delete_left(event):
            display_payment_delete_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        def display_payment_delete_all_hover(event):
            display_payment_delete_all_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        def display_payment_delete_all_left(event):
            display_payment_delete_all_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        # def display_payment_update_hover(event):
        #     display_payment_update_btn.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

        # def display_payment_update_left(event):
        #     display_payment_update_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

        getting_amount_label = Label(display_payment_frame, text="ALL PAYMENTS", bg=dark_color, fg="#ffffff",
                    font=("Algerian", 25))
        getting_amount_label.place(rely=0.09, relx=0.5, anchor=CENTER)

        display_payment_frame_details_font = Font(family="Arial rounded MT", weight="bold", size=23)

        name_label_display_payment_frame = Label(display_payment_frame, text=f"Of {selecteditem[1]} For Unit {selecteditem[5]}", font=("Arial rounded MT", 12, "bold"), fg="#00e5ff", bg=dark_color)
        name_label_display_payment_frame.place(rely=0.16, relx=0.5, anchor=CENTER)
     
        tv_display_all_payment.bind("<Double-Button-1>", selected_display_row)
        display_all_payment()

        display_payment_close_btn = Button(display_payment_frame, text="Close", command=hide_display_payment_frame, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        display_payment_close_btn.place(relx=0.515, rely=0.9, anchor=CENTER)
        display_payment_close_btn.bind("<Enter>", display_payment_close_hover)
        display_payment_close_btn.bind("<Leave>", display_payment_close_left)

        display_payment_delete_btn = Button(display_payment_frame, text="Delete", command=delete_selected_display_payment_frame, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        display_payment_delete_btn.place(relx=0.65, rely=0.9, anchor=CENTER)
        display_payment_delete_btn.bind("<Enter>", display_payment_delete_hover)
        display_payment_delete_btn.bind("<Leave>", display_payment_delete_left)

        display_payment_delete_all_btn = Button(display_payment_frame, text="Delete All", command=delete_all_display_payment_frame, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=8, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        display_payment_delete_all_btn.place(relx=0.8, rely=0.9, anchor=CENTER)
        display_payment_delete_all_btn.bind("<Enter>", display_payment_delete_all_hover)
        display_payment_delete_all_btn.bind("<Leave>", display_payment_delete_all_left)

        # display_payment_update_btn = Button(display_payment_frame, text="Update", command=update_display_payment, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        # display_payment_update_btn.place(relx=0.8, rely=0.9, anchor=CENTER)
        # display_payment_update_btn.bind("<Enter>", display_payment_update_hover)
        # display_payment_update_btn.bind("<Leave>", display_payment_update_left)

    # display_payment()
    else:
        m_box.showerror("Error", "Select the record which you want to Display Payment.")


def settings_window(*args):
    tree_view_frame.place_forget()

    def settingUp_submit(*args):
        admin_name = settingUp_admin_name_value.get()
        admin_address = settingUp_admin_address_value.get()
        admin_email = settingUp_admin_email_value.get().replace(" ","")
        admin_login_username = settingUp_admin_login_username_value.get()
        admin_login_password = settingUp_admin_login_password_value.get()
        admin_c_v = settingUp_admin_contact_value.get()
        admin_c_num = settingUp_admin_cnic_value.get()
        time = getdate()
        # admin_email = admin_email.replace(" ","")
        admin_c_v = admin_c_v.replace(" ","")
        admin_c_num = admin_c_num.replace(" ","")
        
        if admin_name == '' or admin_address == '' or admin_email == '' or admin_login_username =='' or admin_login_password == '' or admin_c_v == '' or admin_c_num == '':
            m_box.showerror("Error", "Fill up the feild(s).")

        else:
            try:
                admin_c_v = int(admin_c_v)
                admin_c_num = int(admin_c_num)

            except ValueError:
                m_box.showerror('Error', 'Contact and CNIC number must be only in numerals.')

            else:
                email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                username_regex = re.compile(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$")
                password_regex = re.compile(r"^.*(?=.{5,14})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$")
                admin_c_v = str(admin_c_v)
                admin_c_num = str(admin_c_num)
                # admin_name = admin_name.replace("\n", "")
                # s_name = s_name.replace(" ","")

                if admin_name.isdigit() >= admin_name.isalpha():
                    m_box.showerror('Error', 'Admin Name must be in letters.')

                # elif s_name.isdigit() >= s_name.isalpha():
                    # m_box.showerror('Error', 'Surname must be in letters.')

                elif len(admin_name.replace(" ",""))<3 or len(admin_name.replace(" ",""))>15:
                    m_box.showerror('Error', 'Admin Name has at least 3-15 characters.')

                # elif len(s_name.replace(" ",""))<3 or len(s_name.replace(" ",""))>14:
                    # m_box.showerror('Error', 'Surname has at least 3-14 characters.')

                # elif age < 18:
                    # m_box.showerror('Error', 'Age must above than 18.')

                # elif age >= 101:
                    # m_box.showerror('Error', 'Age limit exceed.')

                elif len(admin_address.replace(" ",""))<6 or len(admin_address.replace(" ",""))>25:
                    m_box.showerror('Error', 'Branch Address has at least 6-25 characters.')

                elif not email_regex.match(admin_email):  
                    m_box.showerror('Error', 'Invalid Email') 
                # elif len(b_u.replace(" ",""))<3 or len(b_u.replace(" ",""))>8:
                    # m_box.showerror('Error', 'Booking unit has at least 3-8 characters.')
                elif not username_regex.match(admin_login_username):
                    m_box.showerror('Error', 'Username must have 8-14 characters Uppercase, Lowercase, Numbers and Special Characters') 

                elif not password_regex.match(admin_login_password):
                    m_box.showerror('Error', 'Password must have 5-13 characters Uppercase, Lowercase, Numbers and Special Characters') 

                elif len(admin_c_v)<8 or len(admin_c_v)>14:
                    m_box.showerror("Error", "Admin  has at least 8-14 digits.")
                
                elif len(admin_c_num)<10 or len(admin_c_num)>16:
                    m_box.showerror("Error", "Admin CNIC number has at least 10-16 digits.")

                else:

                    def verify_email_func(*args):
                        verify_email_enter_code_value_get = verify_email_enter_code_value.get()
                        if verify_email_enter_code_value_get == '':
                            m_box.showerror("Error", "Enter the verification code.")
                        
                        elif verify_email_enter_code_value_get != otp:
                            m_box.showerror("Error", "Verification code doesn't match.")

                        else:
                            verify_email_enter_code_value.set("")
                            conn = db.connect("Dark Town Database.db")
                            cur = conn.cursor()
                            cur.execute('''CREATE TABLE IF NOT EXISTS SETTINGUP
                                (
                                    cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    AdminName Text,
                                    AdminAddress Text,
                                    Email Text,
                                    LoginUsername Text,
                                    LoginPassword Text,
                                    AdminContact Text,
                                    AdminCNIC Text,
                                    Time Text
                                )''')
                            # conn = db.connect("Dark Town Database.db")
                            # ccur = conn.cursor()

                            admin_name = settingUp_admin_name_value.get()
                            # s_name = surname_value.get()
                            admin_c_v = settingUp_admin_contact_value.get()
                            admin_c_v = "+92-"+admin_c_v

                            telling_no_data_label.place_forget()
                            print(f"{admin_name} | {admin_address} | {admin_email} | {admin_login_username} | {admin_login_password} | {admin_c_v} | {admin_c_num}")
                            tv.delete(*tv.get_children())
                            sqlite_insert_query = """INSERT INTO SETTINGUP(AdminName, AdminAddress, Email, LoginUsername, LoginPassword, AdminContact, AdminCNIC, Time) 
                                                    VALUES (?,?,?,?,?,?,?,?)"""

                            cur.execute(sqlite_insert_query, (admin_name, admin_address, admin_email,admin_login_username, admin_login_password, admin_c_v, admin_c_num, time))

                            cur.close()
                            conn.commit()
                            conn.close()

                            m_box.showinfo('Verified', 'You have successfully verified.')
                            verify_email_frame.place_forget()
                            settings_window_frame.place_forget()
                            root.update()
                            tree_view_frame.place(rely=0.314, relx=0.3485)
                            displaydata()
                            
                    mouse = Controller()
                    mouse.position = (680, 470)
                    
                    settings_window_frame.place_forget()    
                    # verify_email_frame = Frame(root, height=300, width=455, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
                    verify_email_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

                    # verify_email_frame_heading = Label(verify_email_frame, justify=LEFT, text="Verify Now",
                    # bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
                    verify_email_frame_heading.place(rely=0.125, relx=0.5, anchor=CENTER)

                    # -----------ENTER CODE------------

                    message_label.configure(text=f"We sent a verification code on,\n {admin_email} also check spams")
                    message_label.place(rely=0.65, relx=0.5, anchor=CENTER)
                    # verify_email_enter_code_label = Label(verify_email_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")
                    verify_email_enter_code_label.place(rely=0.35, relx=0.05)
                    # verify_email_enter_code_value = StringVar(verify_email_frame)
                    # verify_email_enter_code_entry = Entry(verify_email_frame, textvariable=verify_email_enter_code_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                                        # width=17)
                    verify_email_enter_code_entry.place(rely=0.387, relx=0.55)

                    def change_email(*args):
                        verify_email_frame.place_forget()
                        settings_window()

                    def verify_email_button_hover(event):
                        verify_email_button.configure(fg="#00e5ff", bg="#ffffff")

                    def verify_email_button_left(event):
                        verify_email_button.configure(bg="#00e5ff", fg="#ffffff")

                    verify_change_email_button = Button(verify_email_frame, text="Change Email", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=12, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3,command=change_email)
                    verify_change_email_button.place(rely=0.818, relx=0.345)
                    verify_change_email_button.bind("<Enter>", verify_change_email_button_hover)
                    verify_change_email_button.bind("<Leave>", verify_change_email_button_left)
                    verify_change_email_button.bind("<Return>",change_email)

                    verify_email_button.configure(command=verify_email_func)
                    verify_email_button.place(rely=0.818, relx=0.7)
                    verify_email_button.bind("<Return>",verify_email_func)
                    m_box.showinfo('Verify', 'Please verify email address.')

                    name_value.set("")
                    surname_value.set("")
                    age_value.set("")
                    address_value.set("")
                    booking_unit_value.set("")
                    contact_value.set("")
                    cnic_value.set("")

                    otp=""
                    for i in range(4):
                        otp+=str(random.randint(1,9))
                    # print (otp)
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.ehlo()
                    server.starttls()
                    server.login("youremail", "yourpassword")
                    server.sendmail(f"youremail", admin_email, f"Subject:Your Verification Code\n\n{otp}")
                    server.close()

    def settingUp_submit_hover(event):
        settingUp_submit_button.configure(fg="#00e5ff", bg="#ffffff")

    def settingUp_submit_left(event):
        settingUp_submit_button.configure(bg="#00e5ff", fg="#ffffff")

    mouse = Controller()
    mouse.position = (680, 470)
    settings_window_frame = Frame(root, height=450, width=500, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
    
    settingUp_heading = Label(settings_window_frame, justify=LEFT, text="SettingUp",
                    bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
    settingUp_heading.place(rely=0.07, relx=0.5, anchor=CENTER)

    # -----------ADMIN NAME------------
    settingUp_admin_name = Label(settings_window_frame, text="Admin Name", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                        fg="#00e5ff").place(rely=0.16, relx=0.05)
    settingUp_admin_name_value = StringVar(settings_window_frame)
    settingUp_admin_name_entry = Entry(settings_window_frame, textvariable=settingUp_admin_name_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                        width=17)
    settingUp_admin_name_entry.place(rely=0.187, relx=0.55)

    # -----------BRANCH ADDRESS------------
    settingUp_admin_address_label = Label(settings_window_frame, text="Branch Address", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                            fg="#00e5ff").place(rely=0.256, relx=0.05)
    settingUp_admin_address_value = StringVar(settings_window_frame)
    settingUp_admin_address_entry = Entry(settings_window_frame, textvariable=settingUp_admin_address_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                            relief=FLAT)
    settingUp_admin_address_entry.place(rely=0.282, relx=0.55)

    # -----------EMAIL------------
    settingUp_admin_email_label = Label(settings_window_frame, text="Email", font=local_font, width=18, height=1, bg=dark_color, pady=10, padx=10,
                    fg="#00e5ff").place(rely=0.353, relx=0.05)#.place(rely=0.488, relx=0.05)
    settingUp_admin_email_value = StringVar(settings_window_frame)
    settingUp_admin_email_entry = Entry(settings_window_frame, textvariable=settingUp_admin_email_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17, relief=FLAT)
    settingUp_admin_email_entry.place(rely=0.377, relx=0.55)

    # -----------LOGIN USERNAME------------
    settingUp_admin_login_username_label = Label(settings_window_frame, text="Login Username", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                        fg="#00e5ff").place(rely=0.448, relx=0.05)
    settingUp_admin_login_username_value = StringVar(settings_window_frame)
    settingUp_admin_login_username_entry = Entry(settings_window_frame, textvariable=settingUp_admin_login_username_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                        relief=FLAT)
    settingUp_admin_login_username_entry.place(rely=0.475, relx=0.55)#.place(rely=0.397, relx=0.55)

    # -----------LOGIN PASSWORD------------
    settingUp_admin_login_password_label = Label(settings_window_frame, text="Login Password", font=local_font, bg=dark_color, pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.548, relx=0.05)#.place(rely=0.838, relx=0)
    settingUp_admin_login_password_value = StringVar(settings_window_frame)
    settingUp_admin_login_password_entry = Entry(settings_window_frame, textvariable=settingUp_admin_login_password_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                        relief=FLAT)
    settingUp_admin_login_password_entry.place(rely=0.574, relx=0.55)#.place(rely=0.865, relx=0.5)

    # -----------CONTACT------------
    settingUp_admin_contact_label = Label(settings_window_frame, text="Contact", font=local_font, bg=dark_color, pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.643, relx=0.05)#.place(rely=0.608, relx=0)
    settingUp_admin_contact_value = StringVar(settings_window_frame)
    settingUp_admin_contact_entry = Entry(settings_window_frame, textvariable=settingUp_admin_contact_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                            relief=FLAT)
    settingUp_admin_contact_entry.place(rely=0.67, relx=0.55)#.place(rely=0.634, relx=0.5)

    settingUp_code_button = Label(settings_window_frame, text="+92-", relief=FLAT, bg=dark_color, fg="gray45", font=("Rockwell 11 "))
    settingUp_code_button.place(rely=0.67, relx=0.472)

    # -----------CNIC NAME------------
    settingUp_admin_cnic_num = Label(settings_window_frame, text="CNIC Number", font=local_font, bg=dark_color, pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.743, relx=0.05) #.place(rely=0.723, relx=0)
    settingUp_admin_cnic_value = StringVar(settings_window_frame)
    settingUp_admin_cnic_entry = Entry(settings_window_frame, textvariable=settingUp_admin_cnic_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                        relief=FLAT)
    settingUp_admin_cnic_entry.place(rely=0.77, relx=0.55)#.place(rely=0.75, relx=0.5)

    # -----------BUTTONS------------
    buttons_font = Font(family="Arial Rounded MT Bold", size=13)

    def threaded_settingUp_submit(*args):
        threading.Thread(target=settingUp_submit).start()

    settingUp_submit_button = Button(settings_window_frame, text="Submit", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3, command=threaded_settingUp_submit)
    settingUp_submit_button.place(rely=0.88, relx=0.7)
    settingUp_submit_button.bind("<Enter>",  settingUp_submit_hover)
    settingUp_submit_button.bind("<Leave>",  settingUp_submit_left)
    settingUp_submit_button.bind("<Return>", settingUp_submit)

    # settingUp_clear_button = Button(settings_window_frame, text="Clear", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=6, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)#,command=clear)
    # settingUp_clear_button.place(rely=0.88, relx=0.515)
    # settingUp_clear_button.bind("<Enter>", cls_hover)
    # settingUp_clear_button.bind("<Leave>", cls_left)
    # settingUp_clear_button.bind("<Return>",clear)

    def hide_settings_frame(event):
        settings_window_frame.place_forget()
        # settings_button.configure(state=NORMAL, cursor="hand2")

    # settings_button.configure(state=DISABLED, cursor="X_cursor")

    settings_window_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

def Exit(*args):
    result = m_box.askquestion('Exit', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        # exit()
    # --------------- HOVER FUNCTIONS --------------- #

def sub_hover(event):
    submit_button.config(
        font=buttons_font,
        bg='#ffffff',
        fg='#00e5ff'
    )

def sub_left(event):
    submit_button.config(
        font=buttons_font,
        bg='#00e5ff',
        fg='#ffffff'
    )

def cls_hover(event):
    clear_button.config(
        font=buttons_font,
        bg='#ffffff',
        fg='#00e5ff'
    )

def cls_left(event):
    clear_button.config(
        font=buttons_font,
        bg='#00e5ff',
        fg='#ffffff'
    )

def more_buttons_hover_delete_selected(event):
    delete_selected.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

def more_buttons_left_delete_selected(event):
    delete_selected.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def more_buttons_hover_delete_all(event):
    delete_all.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

def more_buttons_left_delete_all(event):
    delete_all.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def search_button_hover(event):
    btn_search.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

def search_button_left(event):
    btn_search.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def reset_button_hover(event):
    btn_reset.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

def reset_button_left(event):
    btn_reset.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def add_payment_hover(event):
    btn_add_payment.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

def add_payment_left(event):
    btn_add_payment.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def display_payment_hover(event):
    btn_display_payment.configure(font=more_buttons_fonts, fg="#00e5ff", bg="#ffffff")

def display_payment_left(event):
    btn_display_payment.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def verify_email_button_hover(event):
    verify_email_button.configure(fg="#00e5ff", bg="#ffffff")

def verify_email_button_left(event):
    verify_email_button.configure(bg="#00e5ff", fg="#ffffff")

def verify_change_email_button_hover(event):
    verify_change_email_button.configure(fg="#00e5ff", bg="#ffffff")

def verify_change_email_button_left(event):
    verify_change_email_button.configure(bg="#00e5ff", fg="#ffffff")

def minimize_btn_hover(event):
    minimize_btn.configure(font=more_buttons_fonts, bg="#ffffff", fg="#00e5ff")

def minimize_btn_left(event):
    minimize_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def exit_btn_hover(event):
    exit_btn.configure(font=more_buttons_fonts, fg="#ffffff", bg="Red")

def exit_btn_left(event):
    exit_btn.configure(font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff")

def when_hover(event):
    top_heading.configure(fg="#00e5ff")
    dark_logo_label.place(rely=-0.01, relx=0.31)

def when_leave(event):
    top_heading.configure(fg=dark_color)
    dark_logo_label.place_forget()

def menu_bar(*args):

    def info_button_hover(event):
        info_button.configure(font=more_buttons_fonts, fg="#ffffff", bg="#00e5ff")

    def info_button_leave(event):
        info_button.configure(font=more_buttons_fonts, bg="#ffffff", fg=dark_color)

    def about_button_hover(event):
        about_button.configure(font=more_buttons_fonts, fg="#ffffff", bg="#00e5ff")

    def about_button_leave(event):
        about_button.configure(font=more_buttons_fonts, bg="#ffffff", fg=dark_color)

    def settings_button_hover(event):
        settings_button.configure(font=more_buttons_fonts, fg="#ffffff", bg="#00e5ff")

    def settings_button_leave(event):
        settings_button.configure(font=more_buttons_fonts, bg="#ffffff", fg=dark_color)

    def hide_button_hover(event):
        hide.configure(bg="#ffffff", fg=dark_color)

    def hide_button_leave(event):
        hide.configure(fg="#ffffff", bg=dark_color)

    far = Frame(root, width=330, height=770, bg="#15171f")
    menu_buttons_fonts = Font(family="Arial rounded MT", weight="bold", size=13)
    menu_Label_fonts = Font(family="Arial rounded MT", weight="bold", size=23)

    menu_label = Label(far, text="Menu Bar", font=menu_Label_fonts, bg="#15171f", fg="#ffffff")
    menu_label.place(rely=0.032, relx=0.038)

    def info_window(*args):
        mouse = Controller()
        mouse.position = (680, 470)
        info_window_frame = Frame(root, height=480, width=500, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
        
        shortcut_keys_heading = Label(info_window_frame, justify=LEFT, text="Shortcut Keys",
                        bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
        shortcut_keys_heading.place(rely=0.07, relx=0.5, anchor=CENTER)

        command_label = Label(info_window_frame, justify=LEFT, text="Command", bg=dark_color, fg="#00e5ff", font=("Ebrima", 16, "bold"))
        command_label.place(rely=0.17, relx=0.143)

        shortcut_label = Label(info_window_frame, justify=LEFT, text="Shortcut", bg=dark_color, fg="#00e5ff", font=("Ebrima", 16, "bold"))
        shortcut_label.place(rely=0.17, relx=0.655)

        submit_command_label = Label(info_window_frame, justify=CENTER, text="Submit", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        submit_command_label.place(rely=0.25, relx=0.143)

        submit_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+S", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        submit_shortcut_label.place(rely=0.25, relx=0.655)

        clear_command_label = Label(info_window_frame, justify=CENTER, text="Clear", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        clear_command_label.place(rely=0.31, relx=0.143)

        clear_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+Shift+C", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        clear_shortcut_label.place(rely=0.31, relx=0.655)

        update_command_label = Label(info_window_frame, justify=CENTER, text="Update", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        update_command_label.place(rely=0.37, relx=0.143)

        update_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+U", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        update_shortcut_label.place(rely=0.37, relx=0.655)

        delete_command_label = Label(info_window_frame, justify=CENTER, text="Delete", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        delete_command_label.place(rely=0.43, relx=0.143)

        delete_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+D", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        delete_shortcut_label.place(rely=0.43, relx=0.655)

        delete_all_command_label = Label(info_window_frame, justify=CENTER, text="Delete all", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        delete_all_command_label.place(rely=0.49, relx=0.143)

        delete_all_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+Shift+D", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        delete_all_shortcut_label.place(rely=0.49, relx=0.655)

        search_command_label = Label(info_window_frame, justify=CENTER, text="Search", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        search_command_label.place(rely=0.55, relx=0.143)

        search_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+Shift+S", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        search_shortcut_label.place(rely=0.55, relx=0.655)

        reset_command_label = Label(info_window_frame, justify=CENTER, text="Reset", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        reset_command_label.place(rely=0.61, relx=0.143)

        reset_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+R", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        reset_shortcut_label.place(rely=0.61, relx=0.655)

        minimize_command_label = Label(info_window_frame, justify=CENTER, text="Add Payment", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        minimize_command_label.place(rely=0.67, relx=0.143)

        minimize_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+P", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        minimize_shortcut_label.place(rely=0.67, relx=0.655)

        close_command_label = Label(info_window_frame, justify=CENTER, text="Display Payment", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        close_command_label.place(rely=0.73, relx=0.143)

        close_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+Shift+P", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        close_shortcut_label.place(rely=0.73, relx=0.655)

        close_command_label = Label(info_window_frame, justify=CENTER, text="Minimize", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        close_command_label.place(rely=0.79, relx=0.143)

        close_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+M", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        close_shortcut_label.place(rely=0.79, relx=0.655)

        close_command_label = Label(info_window_frame, justify=CENTER, text="Close", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        close_command_label.place(rely=0.85, relx=0.143)

        close_shortcut_label = Label(info_window_frame, justify=CENTER, text="Escape", bg=dark_color, fg="#00e5ff", font=("Ebrima", 14))
        close_shortcut_label.place(rely=0.85, relx=0.655)

        note_label = Label(info_window_frame, justify=CENTER, text='Note: If data is not displaying click on "Reset" button.', bg=dark_color, fg="#00e5ff", font=("Ebrima", 11))
        note_label.place(rely=0.96, relx=0.5, anchor=CENTER)
        # clear_command_label = Label(info_window_frame, justify=CENTER, text="Submit", bg="red", fg="#00e5ff", font=("Ebrima", 16))
        # clear_command_label.place(rely=0.4, relx=0.143)

        # clear_shortcut_label = Label(info_window_frame, justify=CENTER, text="Ctrl+S", bg="red", fg="#00e5ff", font=("Ebrima", 16))
        # clear_shortcut_label.place(rely=0.4, relx=0.655)

        def hide_info_frame(event):
            info_window_frame.place_forget()
            info_button.configure(state=NORMAL, cursor="hand2")

        root.bind("<Button-1>", hide_info_frame)
        info_button.configure(state=DISABLED, cursor="X_cursor")

        info_window_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

    info_button = Button(far, text="Info", justify=LEFT, font=menu_buttons_fonts, bg="#ffffff", fg=dark_color,
                            height=1, width=27, bd=0, pady=6.3, activebackground=dark_color, activeforeground="#ffffff",cursor="hand2",relief=FLAT, command=info_window)
    info_button.place(rely=0.12, relx=0.038)

    info_button.bind("<Enter>", info_button_hover)
    info_button.bind("<Leave>", info_button_leave)

    def about_window(*args):
        mouse = Controller()
        mouse.position = (705, 425)
        about_window_frame = Frame(root, height=180, width=315, bg=dark_color)

        about_label = Label(about_window_frame, justify=CENTER, text="A\nB\nO\nU\nT",
                            font=("Arial rounded MT", 21, "bold"), underline=16, fg="#00e5ff",
                            bg=dark_color)  # ,width=29,padx=10, pady=8
        about_label.place(rely=0.03, relx=0.043)
        about_label2 = Label(about_window_frame, text="S\nO\nF\nT\nW\nA\nR\nE", font=("Ebrima", 12, "bold"),
                                justify=CENTER, fg="#00e5ff", bg=dark_color)  # ,width=29,padx=10, pady=8
        about_label2.place(rely=0.015, relx=0.15)

        about_label_detail = Label(about_window_frame, justify=LEFT, text="Dark Town Management\nSystem Details:",
                                    bg=dark_color,
                                    fg="#00e5ff", font=("Maiandra GD", 12, "bold"))
        about_label_detail.place(rely=0.05, relx=0.265)

        about_label_detail2 = Label(about_window_frame, justify=LEFT,
                                    text="Built on: February 20, 2020\nSize: Unknown\nRuntime version: 0.3",
                                    bg=dark_color,
                                    fg="#00e5ff", font=("ArialRoundedMT", 10, "bold"))
        about_label_detail2.place(rely=0.32, relx=0.265)
        about_window_frame.place(rely=0.5, relx=0.5, anchor=CENTER)  
        about_button.configure(state=DISABLED, cursor="X_cursor")

        def hide_about_frame(event):
            about_window_frame.place_forget()
            about_button.configure(state=NORMAL, cursor="hand2")

        root.bind("<Button-1>", hide_about_frame)

    about_button = Button(far, text="About", font=menu_buttons_fonts, bg="#ffffff", fg=dark_color, activebackground=dark_color, activeforeground="#ffffff",height=1, width=27,
                            pady=6.3, relief=FLAT, bd=0, cursor="hand2",command=about_window)
    about_button.place(rely=0.19, relx=0.038)
    # about_button.place(rely=0.12, relx=0.038)
    about_button.configure(state=NORMAL, cursor="hand2")
    about_button.bind("<Enter>", about_button_hover)
    about_button.bind("<Leave>", about_button_leave)

    def settings_window(*args):
        # try:
        buttons_font = Font(family="Arial Rounded MT Bold", size=13)

        frame_for_login = Frame(root, height=220, width=420, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)

                # -----------ADMIN NAME------------

        login_heading = Label(frame_for_login, text="LOGIN", bg=dark_color, fg="#00e5ff",
                                    font=("Maiandra GD", 28, "bold"))
        admin_login_username_name = Label(frame_for_login, text="Username", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                            fg="#00e5ff")
        # admin_login_username_name.place(rely=0.32, relx=0.05)

        admin_login_username_value = StringVar(frame_for_login)
        # settingUp_admin_name_value2.set(admin_name_to_display)
        admin_login_username_entry = Entry(frame_for_login, textvariable=admin_login_username_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                            width=17)
        # admin_login_username_entry.place(rely=0.357, relx=0.55)

        # -----------BRANCH ADDRESS------------
        admin_login_password_label = Label(frame_for_login, text="Password", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                                fg="#00e5ff")
        admin_login_password_label.place(rely=0.54, relx=0.05)
        admin_login_password_value = StringVar(frame_for_login)
        admin_login_password_entry = Entry(frame_for_login, textvariable=admin_login_password_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                                relief=FLAT)
    
        def login_button_hover(event):
            login_button.configure(fg="#00e5ff", bg="#ffffff")

        def login_button_left(event):
            login_button.configure(bg="#00e5ff", fg="#ffffff")

        def close_login_button_hover(event):
            close_login_button.configure(fg="#00e5ff", bg="#ffffff")

        def close_login_button_left(event):
            close_login_button.configure(bg="#00e5ff", fg="#ffffff")

        def forgot_password_login_button_hover(event):
            forgot_password_login_button.configure(fg="#00e5ff", bg="#ffffff")

        def forgot_password_login_button_left(event):
            forgot_password_login_button.configure(bg="#00e5ff", fg="#ffffff")

        login_button = Button(frame_for_login, text="Login", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)#, command=click_login)

        login_button.bind("<Enter>", login_button_hover)
        login_button.bind("<Leave>", login_button_left)

        close_login_button = Button(frame_for_login, text="Close", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        close_login_button.bind("<Enter>", close_login_button_hover)
        close_login_button.bind("<Leave>", close_login_button_left)

        forgot_password_login_button = Button(frame_for_login, text="Forgot", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        forgot_password_login_button.bind("<Enter>", forgot_password_login_button_hover)
        forgot_password_login_button.bind("<Leave>", forgot_password_login_button_left)

        mouse = Controller()
        mouse.position = (680, 470)
        settings_window_frame = Frame(root, height=420, width=500, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
        
        shortcut_keys_heading = Label(settings_window_frame, justify=LEFT, text="SettingUp",
                        bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
        shortcut_keys_heading.place(rely=0.07, relx=0.5, anchor=CENTER)

        conn = db.connect("Dark Town Database.db")
        cur = conn.cursor()
        query = "SELECT * FROM `SETTINGUP` ORDER BY `cia` ASC"

        cur.execute(query)

        data = cur.fetchall()
        for row in data:
            admin_cia_to_display  = row[0]
            admin_name_to_display  = row[1]
            admin_address_to_display  = row[2]
            admin_email_to_display  = row[3]
            admin_login_username_to_display  = row[4]
            admin_login_password_to_display  = row[5]
            admin_contact_to_display  = row[6].replace("+92-", "")
            admin_cnic_to_display  = row[7]
        conn.close()
        
        def settings_window_frame_close(*args):
            settings_window_frame.place_forget()
            settings_button.configure(state=NORMAL, cursor="hand2")
            
        def settingUp_update(*args):
            if check_login == False:
                # login_fun()
                m_box.showerror("Error", "Please login to update.")
            else:
                # settings_window_frame.place_forget()()
                settingUp_admin_name_value_for_check = settingUp_admin_name_value.get()
                settingUp_admin_address_value_for_check = settingUp_admin_address_value.get() 
                settingUp_admin_email_value_for_check = settingUp_admin_email_value.get()
                settingUp_admin_login_username_value_for_check = settingUp_admin_login_username_value.get()
                settingUp_admin_login_password_value_for_check = settingUp_admin_login_password_value.get()
                settingUp_admin_contact_value_for_check = settingUp_admin_contact_value.get()
                settingUp_admin_cnic_value_for_check = settingUp_admin_cnic_value.get()

                # if  settingUp_admin_name_value_for_check == admin_name_to_display or settingUp_admin_address_value_for_check == admin_address_to_display or  settingUp_admin_email_value_for_check == admin_email_to_display or settingUp_admin_login_username_value_for_check == admin_login_username_to_display or settingUp_admin_login_password_value_for_check == admin_login_password_to_display or settingUp_admin_contact_value_for_check == admin_contact_to_display or settingUp_admin_cnic_value_for_check == admin_cnic_to_display:
                #     m_box.showerror("Error", "Do changes to update")

                if  settingUp_admin_name_value_for_check == "" or settingUp_admin_address_value_for_check == "" or  settingUp_admin_email_value_for_check == "" or settingUp_admin_login_username_value_for_check == "" or settingUp_admin_login_password_value_for_check == "" or settingUp_admin_contact_value_for_check == "" or settingUp_admin_cnic_value_for_check == "":
                    m_box.showerror("Error", "Fill up the field(s)")
                else:
                    try:
                        settingUp_admin_contact_value_for_check = int(settingUp_admin_contact_value_for_check)
                        settingUp_admin_cnic_value_for_check = int(settingUp_admin_cnic_value_for_check)

                    except ValueError:
                        m_box.showerror('Error', 'Contact and CNIC number must be only in numerals.')

                    else:
                        email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                        username_regex = re.compile(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$")
                        password_regex = re.compile(r"^.*(?=.{5,14})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$")
                        settingUp_admin_contact_value_for_check = str(settingUp_admin_contact_value_for_check)
                        settingUp_admin_cnic_value_for_check = str(settingUp_admin_cnic_value_for_check)
                        settingUp_admin_name_value_for_check = settingUp_admin_name_value_for_check.replace(" ","")

                        if settingUp_admin_name_value_for_check.isdigit() >= settingUp_admin_name_value_for_check.isalpha():
                            m_box.showerror('Error', 'Admin Name must be in letters.')

                        elif len(settingUp_admin_name_value_for_check.replace(" ",""))<3 or len(settingUp_admin_name_value_for_check.replace(" ",""))>15:
                            m_box.showerror('Error', 'Admin Name has at least 3-15 characters.')

                        elif len(settingUp_admin_address_value_for_check.replace(" ",""))<6 or len(settingUp_admin_address_value_for_check.replace(" ",""))>25:
                            m_box.showerror('Error', 'Branch Address has at least 6-25 characters.')

                        elif not email_regex.match(settingUp_admin_email_value_for_check):  
                            m_box.showerror('Error', 'Invalid Email')

                        elif not username_regex.match(settingUp_admin_login_username_value_for_check):
                            m_box.showerror('Error', 'Username must have 8-14 characters Uppercase, Lowercase, Numbers and Special Characters') 

                        elif not password_regex.match(settingUp_admin_login_password_value_for_check):
                            m_box.showerror('Error', 'Password must have 5-13 characters Uppercase, Lowercase, Numbers and Special Characters') 

                        elif len(settingUp_admin_contact_value_for_check)<8 or len(settingUp_admin_contact_value_for_check)>14:
                            m_box.showerror("Error", "Admin  has at least 8-14 digits.")
                        
                        elif len(settingUp_admin_cnic_value_for_check)<10 or len(settingUp_admin_cnic_value_for_check)>16:
                            m_box.showerror("Error", "Admin CNIC number has at least 10-16 digits.")

                        else:
                            def update_settingsUp(*args):
                                conn = db.connect("Dark Town Database.db")
                                cur = conn.cursor()
                                cur.execute('''CREATE TABLE IF NOT EXISTS SETTINGUP
                                    (
                                        cia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        AdminName Text,
                                        AdminAddress Text,
                                        Email Text,
                                        LoginUsername Text,
                                        LoginPassword Text,
                                        AdminContact Text,
                                        AdminCNIC Text,
                                        Time Text
                                    )''')
                                time = getdate()
                                cur.execute("UPDATE `SETTINGUP` SET `adminname` = ?, `adminaddress` = ?, `email` = ?, `loginusername` = ?, `loginpassword` =?, `admincontact` = ?, `admincnic` = ?, time = ? WHERE cia = ?",
                                    (
                                        str(settingUp_admin_name_value_for_check), str(settingUp_admin_address_value_for_check), str(settingUp_admin_email_value_for_check), str(settingUp_admin_login_username_value_for_check), str(settingUp_admin_login_password_value_for_check),
                                        str(settingUp_admin_contact_value_for_check), str(settingUp_admin_cnic_value_for_check), time, int(admin_cia_to_display)))
                                conn.commit()
                                cur.close()
                                conn.close()
                                frame_for_login.place_forget()
                                m_box.showinfo('Updated', 'Data has been updated.')
                                global check_login
                                check_login = True
                                # settings_button.configure(state=NORMAL, cursor="hand2")
                            
                            # update_settingsUp()

                            if settingUp_admin_email_value_for_check != admin_email_to_display:
                                check_change_email = m_box.askquestion("Warning", "You changed email, so you have to verfiy again, Are you sure?", icon="warning")

                                if check_change_email == "yes":    
                                    def verify_email_func(*args):
                                        verify_email_enter_code_value_get = verify_email_enter_code_value.get()
                                        
                                        if verify_email_enter_code_value_get == '':
                                            m_box.showerror("Error", "Enter the verification code.")
                                        
                                        elif verify_email_enter_code_value_get != otp:
                                            m_box.showerror("Error", "Verification code doesn't match.")

                                        else:
                                            verify_email_enter_code_value.set("")
                                            # settings_window_frame.place_forget()
                                            update_settingsUp()
                                            settings_window()
                                            verify_email_frame.place_forget()

                                    mouse = Controller()
                                    mouse.position = (680, 470)
                                    
                                    settings_window_frame.place_forget()    
                                    # verify_email_frame = Frame(root, height=300, width=455, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
                                    verify_email_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

                                    # verify_email_frame_heading = Label(verify_email_frame, justify=LEFT, text="Verify Now",
                                    # bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
                                    verify_email_frame_heading.place(rely=0.125, relx=0.5, anchor=CENTER)

                                    # -----------ENTER CODE------------
                                    
                                    message_label.configure(text=f"We sent a verification code on,\n {settingUp_admin_email_value_for_check} also check spams")
                                    message_label.place(rely=0.65, relx=0.5, anchor=CENTER)
                                    # verify_email_enter_code_label = Label(verify_email_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")
                                    verify_email_enter_code_label.place(rely=0.35, relx=0.05)
                                    # verify_email_enter_code_value = StringVar(verify_email_frame)
                                    # verify_email_enter_code_entry = Entry(verify_email_frame, textvariable=verify_email_enter_code_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                                                        # width=17)
                                    verify_email_enter_code_entry.place(rely=0.387, relx=0.55)

                                    def change_email(*args):
                                        verify_email_frame.place_forget()
                                        settings_window()

                                    def verify_change_email_button_hover(event):
                                        verify_change_email_button.configure(fg="#00e5ff", bg="#ffffff")

                                    def verify_change_email_button_left(event):
                                        verify_change_email_button.configure(bg="#00e5ff", fg="#ffffff")

                                    def verify_email_button_hover(event):
                                        verify_email_button.configure(fg="#00e5ff", bg="#ffffff")

                                    def verify_email_button_left(event):
                                        verify_email_button.configure(bg="#00e5ff", fg="#ffffff")

                                    def verify_email_close(*args):
                                        verify_email_frame.place_forget()
                                        settings_window()
                                    verify_email_close_button.place(rely=0.818, relx=0.147)
                                    verify_email_close_button.configure(command=verify_email_close)

                                    verify_change_email_button.configure(command=change_email)
                                    verify_change_email_button.place(rely=0.818, relx=0.345)
                                    verify_change_email_button.bind("<Enter>", verify_change_email_button_hover)
                                    verify_change_email_button.bind("<Leave>", verify_change_email_button_left)
                                    verify_change_email_button.bind("<Return>",change_email)

                                    verify_email_button.configure(command=verify_email_func)
                                    verify_email_button.place(rely=0.818, relx=0.7)
                                    verify_email_button.bind("<Return>",verify_email_func)
                                    m_box.showinfo('Verify', 'Please verify email address.')

                                    name_value.set("")
                                    surname_value.set("")
                                    age_value.set("")
                                    address_value.set("")
                                    booking_unit_value.set("")
                                    contact_value.set("")
                                    cnic_value.set("")

                                    otp=""
                                    for i in range(4):
                                        otp+=str(random.randint(1,9))
                                    # print (otp)
                                    server = smtplib.SMTP("smtp.gmail.com", 587)
                                    server.ehlo()
                                    server.starttls()
                                    server.login("youremail", "yourpassword")
                                    server.sendmail(f"youremail", settingUp_admin_email_value_for_check, f"Subject:Your Verification Code\n\n{otp}")
                                    server.close()

                            else:
                                update_settingsUp()
        def login_fun(*args):            
            def click_login(*args):
                admin_login_username_value_getting = admin_login_username_value.get()
                admin_login_password_value_getting = admin_login_password_value.get()

                if admin_login_username_value_getting == "" or admin_login_password_value_getting == "":
                    m_box.showerror('Error', "Fill up the field(s)")

                elif admin_login_username_value_getting != admin_login_username_to_display:
                    m_box.showerror('Error', "Worng username")
                
                elif admin_login_password_value_getting != admin_login_password_to_display:
                    m_box.showerror('Error', "Worng password")
                
                else:
                    global check_login
                    check_login = True
                    settings_window()
                    root.update()
                    frame_for_login.place_forget()
            def close_login(*args):
                frame_for_login.place_forget()
                settings_window_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
            
            def forgot_password_func(*args):
                def forget_password(*args):
                    admin_login_username_value.set("")
                    admin_login_password_value.set("")
                    getting_code = verify_email_enter_code_value.get()

                    if getting_code == '':
                            m_box.showerror("Error", "Enter the verification code.")
                        
                    elif getting_code != otp:
                        m_box.showerror("Error", "Verification code doesn't match.")
                    else:
                        verify_email_enter_code_entry.configure(state=DISABLED, cursor="X_cursor")
                        verify_email_frame_heading.configure(text="Verified")
                        message_label.configure(text=f"Password is {getting_password}")
                        def copy_password(*args):
                            clipboard.copy(getting_password)
                            m_box.showinfo("Copied", "Password has copied." )
                        m_box.showinfo("Verified", "Thanks for verifying." )
                        verify_email_button.configure(text="Copy", command=copy_password)
                        copy_password()
                        # new_password_frame = Frame(root, height=220, width=420, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
                        # new_password_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

                        # new_password_frame_heading = Label(new_password_frame, justify=LEFT, text="Verify Now",
                        #                     bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
                        # new_password_enter_code_label = Label(new_password_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")
                        # new_password_message_label = Label(new_password_frame, justify=CENTER, bg=dark_color, fg="#00e5ff", font=("Ebrima", 11))

                        # new_password_enter_code_label = Label(new_password_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")

                        # new_password_enter_code_value = StringVar(new_password_frame)
                        # new_password_enter_code_entry = Entry(new_password_frame, textvariable=new_password_enter_code_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                        #                     width=17)
                        # new_password_button = Button(new_password_frame, text="Verify", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=6, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)#, 


                        # new_password_frame_heading.place(rely=0.23, relx=0.5, anchor=CENTER)
                        # new_password_enter_code_label.place(rely=0.45, relx=0.05)                
                        # new_password_enter_code_entry.place(rely=0.487, relx=0.55)
                        # new_password_button.place(rely=0.713, relx=0.7)

                def close_forget_password(*args):
                    verify_email_frame.place_forget()
                    settings_window()

                frame_for_login.place_forget()

                conn = db.connect("Dark Town Database.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM SETTINGUP ORDER BY `cia` ASC")
                fetch = cur.fetchall()
                for data in fetch:
                    getting_email = data[3].replace(" ","")
                    getting_password = data[5]
                conn.commit()
                cur.close()
                conn.close()

                verify_email_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

                verify_email_frame_heading.place(rely=0.138, relx=0.5, anchor=CENTER)

                verify_email_enter_code_label.place(rely=0.35, relx=0.0)
                # -----------ENTER CODE------------
                verify_email_enter_code_entry.place(rely=0.387, relx=0.5)
                
                message_label.configure(text=f"We sent a verification code on,\n {getting_email} also check spams")
                message_label.place(rely=0.65, relx=0.5, anchor=CENTER)

                verify_email_button.place(rely=0.795, relx=0.7)
                verify_email_button.configure(command=forget_password)

                verify_email_close_button.place(rely=0.795, relx=0.5)
                verify_email_close_button.configure(command=close_forget_password)
                # generate_num_send_email()

                otp=""
                for i in range(4):
                    otp+=str(random.randint(1,9))
                # print (otp)
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login("youremail", "yourpassword")
                server.sendmail(f"youremail", getting_email, f"Subject:Your Verification Code\n\n{otp}")
                server.close()
                # verific

            settings_window_frame.place_forget()
            frame_for_login.place(relx=0.5, rely=0.5, anchor=CENTER)

            login_heading.place(rely=0.135, relx=0.5, anchor=CENTER)
                    # -----------ADMIN NAME------------
            admin_login_username_name.place(rely=0.3, relx=0.0)
            admin_login_username_entry.place(rely=0.337, relx=0.5)
            # -----------BRANCH ADDRESS------------
            admin_login_password_label.place(rely=0.47, relx=0.0)
            admin_login_password_entry.place(rely=0.512, relx=0.5)

            login_button.place(rely=0.77, relx=0.725)
            login_button.configure(command=click_login)
            login_button.bind("<Return>", click_login)

            forgot_password_login_button.place(rely=0.77, relx=0.525)
            forgot_password_login_button.configure(command=threading.Thread(target=forgot_password_func).start)
            forgot_password_login_button.bind("<Return>", lambda event:threading.Thread(target=forgot_password_func).start)

            close_login_button.place(rely=0.77, relx=0.322)
            close_login_button.configure(command=close_login)
            close_login_button.bind("<Return>", close_login)

        # -----------ADMIN NAME------------
        settingUp_admin_name = Label(settings_window_frame, text="Admin Name", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                            fg="#00e5ff").place(rely=0.16, relx=0.05)
        settingUp_admin_name_value = StringVar(settings_window_frame)
        settingUp_admin_name_value.set(admin_name_to_display)
        settingUp_admin_name_entry = Entry(settings_window_frame, textvariable=settingUp_admin_name_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                            width=17)
        settingUp_admin_name_entry.place(rely=0.187, relx=0.55)

        # -----------BRANCH ADDRESS------------
        settingUp_admin_address_label = Label(settings_window_frame, text="Branch Address", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                                fg="#00e5ff").place(rely=0.256, relx=0.05)
        settingUp_admin_address_value = StringVar(settings_window_frame)
        settingUp_admin_address_value.set(admin_address_to_display)
        settingUp_admin_address_entry = Entry(settings_window_frame, textvariable=settingUp_admin_address_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                                relief=FLAT)
        settingUp_admin_address_entry.place(rely=0.282, relx=0.55)

        # -----------EMAIL------------
        settingUp_admin_email_label = Label(settings_window_frame, text="Email", font=local_font, width=18, height=1, bg=dark_color, pady=10, padx=10,
                        fg="#00e5ff").place(rely=0.353, relx=0.05)#.place(rely=0.488, relx=0.05)
        settingUp_admin_email_value = StringVar(settings_window_frame)
        settingUp_admin_email_value.set(admin_email_to_display)
        settingUp_admin_email_entry = Entry(settings_window_frame, textvariable=settingUp_admin_email_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17, relief=FLAT)
        settingUp_admin_email_entry.place(rely=0.377, relx=0.55)

        # -----------LOGIN USERNAME------------
        settingUp_admin_login_username_label = Label(settings_window_frame, text="Login Username", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                            fg="#00e5ff").place(rely=0.448, relx=0.05)
        settingUp_admin_login_username_value = StringVar(settings_window_frame)
        settingUp_admin_login_username_value.set(admin_login_username_to_display)
        settingUp_admin_login_username_entry = Entry(settings_window_frame, textvariable=settingUp_admin_login_username_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                            relief=FLAT)
        settingUp_admin_login_username_entry.place(rely=0.475, relx=0.55)#.place(rely=0.397, relx=0.55)

        # -----------LOGIN PASSWORD------------
        settingUp_admin_login_password_label = Label(settings_window_frame, text="Login Password", font=local_font, bg=dark_color, pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.548, relx=0.05)#.place(rely=0.838, relx=0)
        settingUp_admin_login_password_value = StringVar(settings_window_frame)

        settingUp_admin_login_password_value.set(admin_login_password_to_display)
        settingUp_admin_login_password_entry = Entry(settings_window_frame, textvariable=settingUp_admin_login_password_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                            relief=FLAT)
        settingUp_admin_login_password_entry.place(rely=0.574, relx=0.55)#.place(rely=0.865, relx=0.5)
        if check_login == False:
            settingUp_admin_login_password_entry.configure(show="*")

        # -----------CONTACT------------
        settingUp_admin_contact_label = Label(settings_window_frame, text="Contact", font=local_font, bg=dark_color, pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.643, relx=0.05)#.place(rely=0.608, relx=0)
        settingUp_admin_contact_value = StringVar(settings_window_frame)
        settingUp_admin_contact_value.set(admin_contact_to_display)
        settingUp_admin_contact_entry = Entry(settings_window_frame, textvariable=settingUp_admin_contact_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                                relief=FLAT)
        settingUp_admin_contact_entry.place(rely=0.67, relx=0.55)#.place(rely=0.634, relx=0.5)

        settingUp_code_button = Label(settings_window_frame, text="+92-", relief=FLAT, bg=dark_color, fg="gray45", font=("Rockwell 11 "))
        settingUp_code_button.place(rely=0.67, relx=0.472)

        # -----------CNIC NAME------------
        settingUp_admin_cnic_num = Label(settings_window_frame, text="CNIC Number", font=local_font, bg=dark_color, pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.743, relx=0.05) #.place(rely=0.723, relx=0)
        settingUp_admin_cnic_value = StringVar(settings_window_frame)
        settingUp_admin_cnic_value.set(admin_cnic_to_display)
        settingUp_admin_cnic_entry = Entry(settings_window_frame, textvariable=settingUp_admin_cnic_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                            relief=FLAT)
        settingUp_admin_cnic_entry.place(rely=0.77, relx=0.55)#.place(rely=0.75, relx=0.5)
        # settingUp_admin_cnic_entry.configure(state=DISABLED, cursor="X_cursor")
        # -----------BUTTONS------------
        def threaded_settingUp_update(*args):
            threading.Thread(target=settingUp_update).start()

        def settingUp_update_hover(event):
            settingUp_update_button.configure(fg="#00e5ff", bg="#ffffff")

        def settingUp_update_left(event):
            settingUp_update_button.configure(bg="#00e5ff", fg="#ffffff")

        def settingUp_login_hover(event):
            settingUp_update_button_login.configure(fg="#00e5ff", bg="#ffffff")

        def settingUp_login_left(event):
            settingUp_update_button_login.configure(bg="#00e5ff", fg="#ffffff")

        settingUp_update_button = Button(settings_window_frame, text="Update", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3, command=threaded_settingUp_update)
        settingUp_update_button.place(rely=0.88, relx=0.7)
        settingUp_update_button.bind("<Enter>",  settingUp_update_hover)
        settingUp_update_button.bind("<Leave>",  settingUp_update_left)
        settingUp_update_button.bind("<Return>", threaded_settingUp_update)

        settingUp_update_button_login = Button(settings_window_frame, text="Login", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
        settingUp_update_button_login.place(rely=0.88, relx=0.7)
        settingUp_update_button_login.bind("<Enter>",  settingUp_login_hover)
        settingUp_update_button_login.bind("<Leave>",  settingUp_login_left)

        if check_login == False:
            settingUp_update_button_login.place(rely=0.88, relx=0.53)
            settingUp_update_button_login.configure(command=login_fun)
            # settingUp_submit_button.bind("<Enter>",  settingUp_submit_hover)
            # settingUp_submit_button.bind("<Leave>",  settingUp_submit_left)
            # settingUp_submit_button.bind("<Return>", settingUp_submit)
        else:
            def click_logout(*args):
                global check_login
                check_login = False
                settings_window_frame.place_forget()
                settingUp_update_button_login.configure(text="Login",command=login_fun)
                settingUp_update_button_login.bind("<Return>", login_fun)

                settings_window()
            settingUp_update_button_login.place(rely=0.88, relx=0.53)
            settingUp_update_button_login.configure(text="Logout", command=click_logout)
            settingUp_update_button_login.bind("<Return>", click_logout)

        def settingUp_update_button_close_hover(event):
            settingUp_update_button_close.configure(fg="#00e5ff", bg="#ffffff")

        def settingUp_update_button_close_left(event):
            settingUp_update_button_close.configure(bg="#00e5ff", fg="#ffffff")

        settingUp_update_button_close = Button(settings_window_frame, text="Close", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3, command=settings_window_frame_close)
        settingUp_update_button_close.place(rely=0.88, relx=0.355)
        settingUp_update_button_close.bind("<Enter>", settingUp_update_button_close_hover)
        settingUp_update_button_close.bind("<Leave>", settingUp_update_button_close_left)

        def hide_settings_frame(event):
            pass
            # settings_window_frame.place_forget()
            # settings_button.configure(state=NORMAL)

        root.bind("<Button-1>", hide_settings_frame)
        settings_button.configure(state=DISABLED, cursor="X_cursor")

        settings_window_frame.place(rely=0.5, relx=0.5, anchor=CENTER)

    # except Exception:
        # m_box.showerror("Error", "Can't open now")
    settings_button = Button(far, text="SettingUp", font=menu_buttons_fonts, bg="#ffffff", fg=dark_color, activebackground=dark_color, activeforeground="#ffffff",height=1, width=27, pady=6.3, relief=FLAT, bd=0, cursor="hand2",command=settings_window)
    settings_button.place(rely=0.26, relx=0.038)
    # about_button.place(rely=0.12, relx=0.038)
    settings_button.configure(state=NORMAL, cursor="hand2")
    settings_button.bind("<Enter>", settings_button_hover)
    settings_button.bind("<Leave>", settings_button_leave)

    # light_theme_btn = Button(far, text="Light Theme", command="", font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=11, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=4.5)
    # light_theme_btn.place(rely=0.33, relx=0.043)
    # light_theme_btn.bind("<Enter>", light_theme_btn_hover)
    # light_theme_btn.bind("<Leave>", light_theme_btn_left)


    # dark_theme_btn = Button(far, text="Dark Theme", command="", font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=11, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=4.5)
    # dark_theme_btn.place(rely=0.33, relx=0.52)
    # # dark_theme_btn.bind("<Enter>", dark_theme_btn_hover)
    # # dark_theme_btn.bind("<Leave>", dark_theme_btn_left)
    # light_theme_btn.configure(state=NORMAL, cursor="hand2")


    def hide(*args):
        far.place_forget()
        # hide.place_forget()
        menu_button.configure(image=menu_image, command=menu_bar)

    menu_button.configure(image=menu_close_image, command=hide)
    far.place(rely=0.00, relx=0.019)

frame_side_menu = Frame(root, width=28, height=770, bg=dark_color)
menu_image_import = Image.open("Images\\menu.png")
menu_image = ImageTk.PhotoImage(menu_image_import)
menu_button = Button(frame_side_menu, image=menu_image, relief=FLAT, bg=dark_color, activebackground=dark_color, bd=0, cursor="hand2", command=menu_bar)
menu_button.place(rely=0.045, relx=0.0003)

menu_close_image_import = Image.open("Images\\close.png")
menu_close_image = ImageTk.PhotoImage(menu_close_image_import)

info_image_import = Image.open("Images\\info.png")
info_image = ImageTk.PhotoImage(info_image_import)
info_idea = Label(frame_side_menu, image=info_image, bd=0)
# info_idea.place(rely=0.1275, relx=0.0018)
info_idea.place(rely=0.135, relx=0.07)

about_image_import = Image.open("Images\\about.png")
about_image = ImageTk.PhotoImage(about_image_import)
about_idea = Label(frame_side_menu, image=about_image, bd=0)
about_idea.place(rely=0.202, relx=0.07)

settingUp_image_import = Image.open("Images\\settings.png")
settingUp_image = ImageTk.PhotoImage(settingUp_image_import)
settingUp_idea = Label(frame_side_menu, image=settingUp_image, bd=0)
settingUp_idea.place(rely=0.272, relx=0.07)

frame_side_menu.place(rely=0.0, relx=0.0)

global top_heading
top_heading = Label(text="D A R K  T O W N", width=13, font=("Poor Richard", 40), fg=dark_color, bg="#242936",height=0)

# top_heading.place(rely=0.02,relx=0.377)
top_heading.place(rely=0.05, relx=0.42)
top_heading.bind("<Enter>", when_hover)
top_heading.bind("<Leave>", when_leave)

logo_import = Image.open("Images\\Logo Header 145px.png")
logo = ImageTk.PhotoImage(logo_import)
logo_label = Label(image=logo, width=0, font=("Poor Richard", 40), fg="#00e5ff", bg="#ffffff", height=0, bd=0)

dark_logo_import = Image.open("Images\\Logo Header Hover 145px.png")
dark_logo = ImageTk.PhotoImage(dark_logo_import)
dark_logo_label = Label(image=dark_logo, width=0, font=("Poor Richard", 40), fg="#00e5ff", bg="#ffffff", height=0, bd=0)

logo_label.place(rely=-0.01, relx=0.31)
frame = Frame(root, width=443.5, height=516, bg='#15171f', pady=30)
frame.place(rely=0.222, relx=0.021)
 
main_headings_font = Font(frame, family="Algerian", size=25)

data_entry_frame = Frame(root,bg=dark_color,width=444,height=99)
data_entry_frame.place(rely=0.185, relx=0.021)
data_entry_label = Label(data_entry_frame, text="DATA ENTRY", bg=dark_color, fg="#ffffff",
            font=main_headings_font)
data_entry_label.place(rely=0.5, relx=0.5, anchor=CENTER)

# -----------USER NAME------------
user_name = Label(frame, text="User Name", font=local_font, width=18, height=1, pady=10, bg="#15171f", padx=10,
                    fg="#00e5ff").place(rely=0.14, relx=0)
name_value = StringVar(frame)
name_entry = Entry(frame, textvariable=name_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                    width=17)
name_entry.place(rely=0.167, relx=0.5)

# -----------SUR NAME------------
surname_label = Label(frame, text="Sur Name", font=local_font, width=18, height=1, pady=10, bg="#15171f", padx=10,
                        fg="#00e5ff").place(rely=0.256, relx=0)
surname_value = StringVar(frame)
surname_entry = Entry(frame, textvariable=surname_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                        relief=FLAT)
surname_entry.place(rely=0.282, relx=0.5)

# -----------AGE------------
age_label = Label(frame, text="Age", font=local_font, width=18, height=1, pady=10, bg="#15171f", padx=10,
                    fg="#00e5ff").place(rely=0.373, relx=0)
age_value = StringVar(frame)
age_entry = Entry(frame, textvariable=age_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                    relief=FLAT)
age_entry.place(rely=0.397, relx=0.5)

# -----------ADDRESS------------
address = Label(frame, text="Address", font=local_font, width=18, height=1, bg="#15171f", pady=10, padx=10,
                fg="#00e5ff").place(rely=0.488, relx=0)
address_value = StringVar(frame)
address_entry = Entry(frame, textvariable=address_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17, relief=FLAT)
address_entry.place(rely=0.515, relx=0.5)

# -----------BOOKING UNIT------------
booking_unit_label = Label(frame, text="Booking Unit", font=local_font, bg="#15171f", pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.608, relx=0)#.place(rely=0.838, relx=0)
booking_unit_value = StringVar(frame)
booking_unit_entry = Entry(frame, textvariable=booking_unit_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                    relief=FLAT)
booking_unit_entry.place(rely=0.634, relx=0.5)#.place(rely=0.865, relx=0.5)

# -----------CONTACT------------

contact_label = Label(frame, text="Contact", font=local_font, bg="#15171f", pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.723, relx=0)#.place(rely=0.608, relx=0)
contact_value = StringVar(frame)
contact_entry = Entry(frame, textvariable=contact_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                        relief=FLAT)
contact_entry.place(rely=0.75, relx=0.5)#.place(rely=0.634, relx=0.5)

code_button = Label(frame, text="+92-", relief=FLAT, bg="#15171f", fg="gray45", font=("Rockwell 11 "))
code_button.place(rely=0.747, relx=0.422)

# -----------CNIC NAME------------
cnic_num = Label(frame, text="CNIC Number", font=local_font, bg="#15171f", pady=10, padx=10, width=18, fg="#00e5ff").place(rely=0.838, relx=0) #.place(rely=0.723, relx=0)
cnic_value = StringVar(frame)
cnic_entry = Entry(frame, textvariable=cnic_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17,
                    relief=FLAT)
cnic_entry.place(rely=0.865, relx=0.5)#.place(rely=0.75, relx=0.5)

# -----------BUTTONS------------
buttons_font = Font(family="Arial Rounded MT Bold", size=13)

submit_button = Button(frame, text="Submit", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3, command=submit)
submit_button.place(rely=0.963, relx=0.7)
submit_button.bind("<Enter>", sub_hover)
submit_button.bind("<Leave>", sub_left)
submit_button.bind("<Return>",submit)

clear_button = Button(frame, text="Clear", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=6, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3,command=clear)
clear_button.place(rely=0.963, relx=0.515)
clear_button.bind("<Enter>", cls_hover)
clear_button.bind("<Leave>", cls_left)
clear_button.bind("<Return>",clear)

record_frame = Frame(root,bg=dark_color,width=886.5,height=99)
record_frame.place(rely=0.185, relx=0.3485)
# 350553

record_label = Label(record_frame,text="RECORDS",font=main_headings_font, bg=dark_color, fg="#ffffff")
record_label.place(relx=0.5, rely=0.3, anchor=CENTER)

more_buttons_fonts = Font(family="Arial rounded MT", weight="bold", size=13)


def more_buttons_hover_update(event):
    update.configure(font=buttons_font, fg="#00e5ff", bg="#ffffff")

def more_buttons_left_update(event):
    update.configure(font=buttons_font, bg="#00e5ff", fg="#ffffff")

update = Button(frame, text="Update", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT,
                padx=0.1, width=6, command=Update,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
update.place(rely=0.963, relx=0.335)
update.bind("<Return>", Update)
# update.config(state=DISABLED, bg="#ffffff", cursor="X_cursor")
update.config(state=DISABLED, bg=dark_color, cursor="X_cursor")
update.bind("<Enter>", "")
update.bind("<Leave>", "")

btn_add_payment = Button(record_frame, text="Add Pay", command=add_payment, font=more_buttons_fonts, relief=FLAT, bg="#00e5ff",fg="#ffffff", activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3,width=7)
btn_add_payment.place(relx=0.065, rely=0.73, anchor=CENTER)
btn_add_payment.bind("<Enter>", add_payment_hover)
btn_add_payment.bind("<Leave>", add_payment_left)
btn_add_payment.bind("<Return>", add_payment)

btn_display_payment = Button(record_frame, text="Display Pay", command=display_payment, font=more_buttons_fonts, relief=FLAT, bg="#00e5ff",fg="#ffffff", activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3,width=9)
btn_display_payment.place(relx=0.172, rely=0.73, anchor=CENTER)
btn_display_payment.bind("<Enter>", display_payment_hover)
btn_display_payment.bind("<Leave>", display_payment_left)
btn_display_payment.bind("<Return>", display_payment)

delete_selected = Button(record_frame,text="Delete", activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3, font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff", relief=FLAT, width=6,
                            command=Delete_selected)
delete_selected.place(relx=0.2745, rely=0.73, anchor=CENTER)
delete_selected.bind("<Enter>", more_buttons_hover_delete_selected)
delete_selected.bind("<Leave>", more_buttons_left_delete_selected)
delete_selected.bind("<Return>", Delete_selected)

delete_all = Button(record_frame ,text="Delete All", activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3, font=more_buttons_fonts, bg="#00e5ff", fg="#ffffff", relief=FLAT, width=7,
                    padx=5.48, command=Delete_all)
delete_all.place(relx=0.368, rely=0.73, anchor=CENTER)
delete_all.bind("<Enter>", more_buttons_hover_delete_all)
delete_all.bind("<Leave>", more_buttons_left_delete_all)
delete_all.bind("<Return>", Delete_all)

search_buttons_fonts = Font(family="Arial rounded", weight="bold", size=13)

SEARCH = StringVar()
search = Entry(record_frame, textvariable=SEARCH, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), width=16, bg="#ffffff", relief=FLAT)
# search.configure(state=NORMAL)

search.place(rely=0.65, relx=0.65)
search.bind("<Return>", Search)

btn_search = Button(record_frame, text="Search", command=Search, font=search_buttons_fonts, relief=FLAT, bg="#00e5ff",fg="#ffffff", activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3,width=6)
btn_search.place(relx=0.85, rely=0.73, anchor=CENTER)
btn_search.bind("<Enter>", search_button_hover)
btn_search.bind("<Leave>", search_button_left)
btn_search.bind("<Return>", Search)

btn_reset = Button(record_frame, text="Reset", command=Reset, font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff",width=6, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
btn_reset.place(relx=0.935, rely=0.73, anchor=CENTER)
btn_reset.bind("<Enter>", reset_button_hover)
btn_reset.bind("<Leave>", reset_button_left)
btn_reset.bind("<Return>", Reset)

minimize_btn = Button(text="Minimize", fg="#ffffff", pady=5.3, bg="#00e5ff", width=8, relief=FLAT, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2",font=("ArialRounded", 13, "bold"), command=lambda: root.wm_state("iconic"))
minimize_btn.place(rely=0.0, relx=0.86)
minimize_btn.bind("<Enter>", minimize_btn_hover)
minimize_btn.bind("<Leave>", minimize_btn_left)
minimize_btn.bind("<Return>",lambda: root.wm_state("iconic"))


exit_btn = Button(text="Exit", fg="#ffffff", pady=5.3, bg="#00e5ff", width=6, relief=FLAT,font=("ArialRounded", 13, "bold"), activebackground="red3",bd=0,activeforeground="#ffffff",cursor="hand2", command=Exit)
exit_btn.place(rely=0.0, relx=0.936)
exit_btn.bind("<Enter>", exit_btn_hover)
exit_btn.bind("<Leave>", exit_btn_left)
exit_btn.bind("<Return>",Exit)

# tree_view_frame = Frame(root)
# tree_view_frame.place(rely=0.314, relx=0.39)

# tv = ttk.Treeview(tree_view_frame, height=20, selectmode="extended",
#                   column=('cia', 'Name', 'Surname', 'Age', 'Address', 'Contact', 'CNIC', 'Date/Time'))
scroll_bar_horizontal = ttk.Scrollbar(tree_view_frame,orient="horizontal",command=tv.xview)
scroll_bar_vertical = ttk.Scrollbar(tree_view_frame,orient="vertical",command=tv.yview)
tv.configure(xscrollcommand=scroll_bar_horizontal.set)
tv.configure(yscrollcommand=scroll_bar_vertical.set)
scroll_bar_horizontal.pack(fill=X,side=BOTTOM)
scroll_bar_vertical.pack(fill=Y,side=RIGHT)
tv.heading('Name', text="Name", anchor="n")
tv.heading('Surname', text="Surname", anchor="n")
tv.heading('Age', text="Age", anchor="n")
tv.heading('Address', text="Address", anchor="n")
tv.heading('Booking Unit', text="Booking Unit", anchor="n")
tv.heading('Contact', text="Contact", anchor="n")
tv.heading('CNIC', text="CNIC", anchor="n")
tv.heading('Date/Time', text="Date/Time", anchor="n")

tv.column('#0', minwidth=0, width=0, anchor='w')
tv.column('#1', minwidth=0, width=0, anchor='w')
# tv.column('#2', minwidth=114, width=114, anchor='w')
# tv.column('#3', minwidth=125, width=125, anchor='w')
# tv.column('#4', minwidth=65, width=65, anchor='w')
tv.column('#2', minwidth=100, width=100, anchor='w')
tv.column('#3', minwidth=100, width=100, anchor='w')
tv.column('#4', minwidth=50, width=50, anchor='w')
tv.column('#5', minwidth=110, width=110, anchor='w')
tv.column('#6', minwidth=100, width=100, anchor='w')
tv.column('#7', minwidth=122, width=122, anchor='w')
tv.column('#8', minwidth=125, width=125, anchor='w')
tv.column('#9', minwidth=160, width=160, anchor='w')
# btn_add_payment.bind("<Return>", )

style = ttk.Style(root)
ttk.Style().configure(".", font=('calibri', 11))
ttk.Style().configure("Heading", font=('Arial Rounded MT Bold', 12), foreground="#00e5ff",background=dark_color, bd=0)
style.configure("Name", highlightthickness=0, bd=0, font=('Calibri', 11))  # Modify the font of the body
tv.bind("<Double-Button-1>", selectedRows)
# if tv.selection() == True:
def right_click_menu(event):
    for i in tv.get_children():
        curItem = tv.focus()
        contents = (tv.item(curItem))
        selecteditem = contents['values']
        if (len(selecteditem)) != 0:
            my_menu = Menu(root, tearoff = False)
            my_menu.add_command(label="Add Payment", command=add_payment)
            my_menu.add_command(label="Display Payment", command=display_payment)
            my_menu.tk_popup(event.x_root, event.y_root)

tv.bind("<Button-3>", right_click_menu)
tv.pack()

displaydata()

root.bind("<Control-R>", Reset)
root.bind("<Control-r>", Reset)

root.bind("<Escape>", Exit)

def minimize_function(event):
    root.wm_state("iconic")

root.bind("<Control-M>", minimize_function)
root.bind("<Control-m>", minimize_function)

root.bind("<Control-Shift-S>", Search)
root.bind("<Control-Shift-s>", Search)

root.bind("<Control-S>", submit)
root.bind("<Control-s>", submit)

root.bind("<Control-Shift-C>", clear)
root.bind("<Control-Shift-c>", clear)

root.bind("<Control-D>", Delete_selected)
root.bind("<Control-d>", Delete_selected)

root.bind("<Control-Shift-D>", Delete_all)
root.bind("<Control-Shift-d>", Delete_all)

root.bind("<Control-P>", add_payment)
root.bind("<Control-p>", add_payment)

root.bind("<Control-Shift-P>", display_payment)
root.bind("<Control-Shift-p>", display_payment)

root.bind("<Control-U>", "")
root.bind("<Control-u>", "")

def text_file(*args):
    if os.path.isfile('text.txt'):
        # threading.Thread(target=settings_window).start()
        os.system('text.txt')
        os.rename("text.txt","readme.txt")

threading.Thread(target=text_file).start()


conn_c_e_SETTINGUP = db.connect("Dark Town Database.db")
ccur_c_e_SETTINGUP = conn_c_e_SETTINGUP.cursor()
ccur_c_e_SETTINGUP.execute(''' SELECT COUNT(*) FROM SETTINGUP''')

if ccur_c_e_SETTINGUP.fetchone()[0]==0:
    threading.Thread(target=settings_window).start()
    # menu_button.configure(state=DISABLED, cursor="X_cursor")

def verify_email_close_button_hover(event):
    verify_email_close_button.configure(fg="#00e5ff", bg="#ffffff")

def verify_email_close_button_left(event):
    verify_email_close_button.configure(bg="#00e5ff", fg="#ffffff")

verify_email_frame = Frame(root, height=250, width=420, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)
verify_email_frame_heading = Label(verify_email_frame, justify=LEFT, text="Verify Now",
                    bg=dark_color, fg="#00e5ff", font=("Maiandra GD", 28, "bold"))
verify_email_enter_code_label = Label(verify_email_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")

verify_email_enter_code_label = Label(verify_email_frame, text="Enter Code", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10, fg="#00e5ff")

verify_email_enter_code_value = StringVar(verify_email_frame)
verify_email_enter_code_entry = Entry(verify_email_frame, textvariable=verify_email_enter_code_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                    width=17)

message_label = Label(verify_email_frame, justify=CENTER, bg=dark_color, fg="#00e5ff", font=("Ebrima", 11))
verify_email_button = Button(verify_email_frame, text="Verify", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=6, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)#, command=verify_email_func)
verify_email_button.bind("<Enter>", verify_email_button_hover)
verify_email_button.bind("<Leave>", verify_email_button_left)

verify_email_close_button = Button(verify_email_frame, text="Close", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=6, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
verify_email_close_button.bind("<Enter>", verify_email_close_button_hover)
verify_email_close_button.bind("<Leave>", verify_email_close_button_left)


verify_change_email_button = Button(verify_email_frame, text="Change Email", font=buttons_font, bg="#00e5ff", fg="#ffffff", relief=FLAT, padx=0.1,width=12, activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
verify_change_email_button.bind("<Enter>", verify_change_email_button_hover)
verify_change_email_button.bind("<Leave>", verify_change_email_button_left)

frame_for_login = Frame(root, height=220, width=420, bg=dark_color, highlightbackground = "#00e5ff", highlightthickness=5)

        # -----------ADMIN NAME------------

login_heading = Label(frame_for_login, text="LOGIN", bg=dark_color, fg="#00e5ff",
                                    font=("Maiandra GD", 28, "bold"))

admin_login_username_name = Label(frame_for_login, text="Username", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                    fg="#00e5ff")
# admin_login_username_name.place(rely=0.32, relx=0.05)

admin_login_username_value = StringVar(frame_for_login)
# settingUp_admin_name_value2.set(admin_name_to_display)
admin_login_username_entry = Entry(frame_for_login, textvariable=admin_login_username_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", relief=FLAT,
                    width=17)
# admin_login_username_entry.place(rely=0.357, relx=0.55)

def login_button_hover(event):
    login_button.configure(fg="#00e5ff", bg="#ffffff")

def login_button_left(event):
    login_button.configure(bg="#00e5ff", fg="#ffffff")

def close_login_button_hover(event):
    close_login_button.configure(fg="#00e5ff", bg="#ffffff")

def close_login_button_left(event):
    close_login_button.configure(bg="#00e5ff", fg="#ffffff")

def forgot_password_login_button_hover(event):
    forgot_password_login_button.configure(fg="#00e5ff", bg="#ffffff")

def forgot_password_login_button_left(event):
    forgot_password_login_button.configure(bg="#00e5ff", fg="#ffffff")

def update_payment_cal_btn_hover(event):
    update_payment_cal_btn.configure(fg="#00e5ff", bg="#ffffff")

def update_payment_cal_btn_left(event):
    update_payment_cal_btn.configure(bg="#00e5ff", fg="#ffffff")

# -----------BRANCH ADDRESS------------
admin_login_password_label = Label(frame_for_login, text="Password", font=local_font, width=18, height=1, pady=10, bg=dark_color, padx=10,
                        fg="#00e5ff")
admin_login_password_label.place(rely=0.54, relx=0.05)
admin_login_password_value = StringVar(frame_for_login)
admin_login_password_entry = Entry(frame_for_login, textvariable=admin_login_password_value, insertbackground=dark_color, fg=dark_color, font=("Rockwell 11"), bg="#ffffff", width=17, relief=FLAT)

login_button = Button(frame_for_login, text="Login", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff", cursor="hand2", pady=3.3)#, command=click_login)
login_button.bind("<Enter>", login_button_hover)
login_button.bind("<Leave>", login_button_left)

forgot_password_login_button = Button(frame_for_login, text="Forgot", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
forgot_password_login_button.bind("<Enter>", forgot_password_login_button_hover)
forgot_password_login_button.bind("<Leave>", forgot_password_login_button_left)

close_login_button = Button(frame_for_login, text="Close", state=NORMAL, font=buttons_font, bg="#00e5ff", fg="#ffffff",relief=FLAT, padx=0.1, width=6,activebackground=dark_color,bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
close_login_button.bind("<Enter>", close_login_button_hover)
close_login_button.bind("<Leave>", close_login_button_left)

update_payment_frame = Frame(bg=dark_color, height=320, width=450, highlightbackground = "#00e5ff", highlightthickness=5)

update_payment_cal_btn =  Button(update_payment_frame, text="Select Date", font=search_buttons_fonts, bg="#00e5ff", fg="#ffffff", width=9, relief=FLAT, activebackground="#15171f",bd=0,activeforeground="#ffffff",cursor="hand2", pady=3.3)
update_payment_cal_btn.bind("<Enter>", update_payment_cal_btn_hover)
update_payment_cal_btn.bind("<Leave>", update_payment_cal_btn_left)
root.mainloop()
                                # --------------- THE END ---------------                                
