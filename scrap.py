# # # # python program demonstrating 
# # # # Combobox widget using tkinter 


# # # import tkinter as tk 
# # # from tkinter import ttk 

# # # # Creating tkinter window 
# # # window = tk.Tk() 
# # # window.title('Combobox') 
# # # window.geometry('500x250') 

# # # # label text for title 
# # # ttk.Label(window, text = "GFG Combobox Widget", 
# # #         background = 'green', foreground ="white", 
# # #         font = ("Times New Roman", 15)).grid(row = 0, column = 1) 

# # # # label 
# # # ttk.Label(window, text = "Select the Month :", 
# # #         font = ("Times New Roman", 10)).grid(column = 0, 
# # #         row = 5, padx = 10, pady = 25) 

# # # # Combobox creation 
# # # n = tk.StringVar() 
# # # receiver_name_choosen = ttk.Combobox(window, width = 27, textvariable = n) 

# # # # Adding combobox drop down list 
# # # receiver_name_choosen['values'] = [' January', 
# # #                         ' February', 
# # #                         ' March', 
# # #                         ' April', 
# # #                         ' May', 
# # #                         ' June', 
# # #                         ' July', 
# # #                         ' August', 
# # #                         ' September', 
# # #                         ' October', 
# # #                         ' November', 
# # #                         ' December'] 
# # # def cc():
# # #     print(receiver_name_choosen.get())
# # #     dd = receiver_name_choosen.get()
# # #     receiver_name_choosen['values']+= (dd,)
    
# # # ttk.Button(text="rr", command=cc).grid(column = 3, row = 5) 

# # # receiver_name_choosen.grid(column = 1, row = 5) 
# # # receiver_name_choosen.current() 
# # # window.mainloop() 
# # # import random
# # # #Generate 5 random numbers between 10 and 30
# # # randomlist = random.sample(range(10, 30), 5)
# # # print(randomlist)

# # # import random as r
# # # # function for otp generation
# # # def otpgen():
# # #     otp=""
# # #     for i in range(4):
# # #         otp+=str(r.randint(1,9))
# # #     print ("Your One Time Password is ")
# # #     print (otp)
# # # otpgen()

# # import random as r
# # # function for otp generation
# # otp=""
# # for i in range(4):
# #     otp+=str(random.randint(1,9))
# # print (otp)

# # python program demonstrating 
# # Combobox widget using tkinter 


# import tkinter as tk 
# from tkinter import ttk 
# import sqlite3 as db

# # Creating tkinter window 
# window = tk.Tk() 
# window.title('Combobox') 
# window.geometry('500x250') 

# # label text for title 
# ttk.Label(window, text = "GFG Combobox Widget", 
#         background = 'green', foreground ="white", 
#         font = ("Times New Roman", 15)).grid(row = 0, column = 1) 

# # label 
# ttk.Label(window, text = "Select the Month :", 
#         font = ("Times New Roman", 10)).grid(column = 0, 
#         row = 5, padx = 10, pady = 25) 

# value_of_receiver_name = tk.StringVar() 
# receiver_name_choosen = ttk.Combobox(window, width = 27, textvariable = value_of_receiver_name) 
# receiver_name_choosen.grid(column = 1, row = 5) 
# receiver_name_choosen.current() 

# value_of_receiver_cnic = tk.StringVar() 
# receiver_cnic_choosen = ttk.Combobox(window, width = 27, textvariable = value_of_receiver_cnic) 
# receiver_cnic_choosen.grid(column = 1, row = 10) 
# receiver_cnic_choosen.current() 

# def add_combobox_values_for_receiver_name():
#     conn = db.connect("exit_vixit.db")
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
#     window.update()
#     cur.close()
#     conn.commit()
#     conn.close()

# def display_combobox_values_for_receiver_name(faiz, ziaz):
#     conn = db.connect("exit_vixit.db")
#     cur = conn.cursor()
#     cur.execute('''CREATE TABLE  IF NOT EXISTS CHOOSE
#         (
#             "ReceiverName" TEXT,
#             "ReceiverCNIC" TEXT
#         )'''
#     )
#     query = f"SELECT {faiz} FROM `CHOOSE`"

#     cur.execute(query)
#     ids = cur.fetchall()
#     ziaz['values'] = ids
#     # ziaz.refresh()

# add_to_combobox_for_receiver_name = ttk.Button(window, text='add', command=add_combobox_values_for_receiver_name)
# add_to_combobox_for_receiver_name.grid(column = 5, row = 5)
# display_combobox_values_for_receiver_name("ReceiverName", receiver_name_choosen)
# display_combobox_values_for_receiver_name("ReceiverCNIC", receiver_cnic_choosen)
# window.mainloop()

import sqlite3 as db

conn = db.connect("Dark Town Database.db")
cur = conn.cursor()
# cur.execute(f"""SELECT cnic FROM DATA WHERE cnic='123939993949293'""")
# if len(cur) > 0:
#     print("1")
# else:
#     print("2")
pin = "123939993949293"
c = cur.execute("""SELECT EXISTS (SELECT 1 
                                     FROM DATA 
                                     WHERE CNIC=?)""", (pin, )).fetchone()[0]
if c:
    print("vip")
else:
    print("b")