"""
Filename: OMS.py
Description: This script functions as a Order Management System (OMS). Designed to tracking customer orders.
Author: Dumri Ketupanya
Date created: June 8, 2020
"""

# import required modules =====================================================================================
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk  # ttk -> themed tk (for Combobox)
import time, datetime

# SQLite Database Connection ===================================================================================
def create_data_table():
    try:
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            CREATE table Order_Records(
            Order_Number real primary key, Customer text, Product text,
            Order_Quantity real, Record_Datetime text, Due_Datetime text, Progress text);
            """
            con.execute(sql_cmd)
    except Exception as e:
        print("Error -> {}".format(e))

Data_list = []
data_lst_eff = []

def select_data():
    try:
        data_lst_eff.clear()
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Order_Records
            """
            for row in con.execute(sql_cmd):
                Data_list.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))


def select_data_eff():
    try:
        data_lst_eff.clear()
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Order_Records
            """
            for row in con.execute(sql_cmd):
                data_lst_eff.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))


setting_lst = []
def select_setting_data():
    try:
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM setting_property
            """
            setting_lst.clear()
            for row in con.execute(sql_cmd):
                setting_lst.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))

unit_per_batch = 0
def Select_fill_Data():
    global unit_per_batch
    unit_per_batch = 0
    try:
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = '''
            SELECT Unit_per_Batch FROM Fill
            '''
            for row in con.execute(sql_cmd):
                unit_per_batch = row
    except Exception as e:
        print("Error -> {}".format(e))

create_data_table()
select_data()

#  User Interface and Program Logic Section ======================================================================================
root = Tk()
root.title("Order Records")
root.option_add("*Font", "arial 11")

col_width = 15

# Title
Title_frame = Frame(root, bg='blue violet')
Title_frame.grid(row=0, column=0, columnspan=9, sticky='news')
Title_Label = Label(Title_frame, text="New orders")
Title_Label.pack(padx=10, pady=10, side=LEFT)

# Subtitle
Subtitle_1 = ["Order NO.", "Customer", "Product", "Order Quantity", "Record datetime", "Due datetime"]
for e, i in enumerate(Subtitle_1):
    Label(root, text=i, bg="magenta").grid(row=1, column=(e), padx=1, sticky='news')

# Entryform(editable)
# Customer name
Customer_Name = StringVar()
En_Customername = Entry(root, textvariable=Customer_Name)
En_Customername.grid(row=2, column=(Subtitle_1.index("Customer")))

# Order  Quantity
Order_Qty = DoubleVar()
En_Order_Qty = Entry(root, textvariable=Order_Qty, width=13)
En_Order_Qty.grid(row=2, column=(Subtitle_1.index("Order Quantity")))

# AutogeneratedData (Read_Only)
# Order_No. #Order by using data from database.
# Order NO. stick with that order forever.
# If it need to change, delete then create new.
if Data_list == []:
    new_order_number = 0
else:
    new_order_number = (Data_list[-1][0]) + 1


def order_number():
    Order_Num = Label(root, text=(new_order_number), bg="plum")
    Order_Num.grid(row=2, column=(Subtitle_1.index("Order NO.")))

order_number()

# RecordTime
currentDT = datetime.datetime.now()
Date_Record = Label(root, text=(currentDT.strftime("%Y-%m-%d %H:%M:%S")), bg="plum")
Date_Record.grid(row=2, column=(Subtitle_1.index("Record datetime")))

# Calender
collect_time_str = [0]


def calendar():
    root2 = Tk()

    def date_submit(e):
        collect_date = datetime.date(int(year.get()), int(month.get()), int(day.get()))
        collect_time = datetime.time(int(hour.get()), int(minute.get()), int(sec.get()))
        collect_time_print = f"{collect_date} {collect_time}"
        collect_time_str.insert(0, f"{collect_date} {collect_time}")
        # print(collect_date)
        # print(collect_time)
        # print(currentDT)
        Due_Time = Label(root, text=collect_time_print, bg="plum")
        Due_Time.grid(row=2, column=(Subtitle_1.index("Due datetime")))

    root2.title("Calendar")
    root2.option_add("*Font", "consolas 15")
    day_list = range(1, 32)
    month_list = (range(1, 13))
    year_list = range(2019, 2030)
    hour_list = range(0, 25)
    minute_list = range(0, 61)
    sec_list = range(0, 61)
    title = ["Day", "Month", "Year", "  ", "Hour", "Minute", "Sec"]
    for e, i in enumerate(title):
        Label(root2, text=i).grid(row=0, column=e, sticky=W)
    currentdate = datetime.datetime.now()
    day = ttk.Combobox(root2, values=list(day_list), width=3)
    day.grid(row=1, column=title.index("Day"))
    day.current(currentdate.day - 1)
    month = ttk.Combobox(root2, values=list(month_list), width=3)
    month.grid(row=1, column=title.index("Month"))
    month.current(currentdate.month - 1)
    year = ttk.Combobox(root2, values=list(year_list), width=5)
    year.grid(row=1, column=title.index("Year"))
    year.current(1)  # Static value
    hour = ttk.Combobox(root2, values=list(hour_list), width=3)
    hour.grid(row=1, column=title.index("Hour"))
    hour.current(12)
    minute = ttk.Combobox(root2, values=list(minute_list), width=3)
    minute.grid(row=1, column=title.index("Minute"))
    minute.current(0)
    sec = ttk.Combobox(root2, values=list(sec_list), width=3)
    sec.grid(row=1, column=title.index("Sec"))
    sec.current(0)
    submit = Button(root2, text="Submit", bg='cornsilk')
    submit.grid(row=1, column=len(title) + 1, padx=10)
    submit.bind("<Button-1>", date_submit)
    root2.mainloop()

# Combobox (Choose data)
# DueTime
Due_Time = Label(root, width=19, text="Set due date", bg="plum")
Due_Time.grid(row=2, column=(Subtitle_1.index("Due datetime")))
add_time = Button(root, text="edit time", height=1, bg="plum", command=calendar)
add_time.grid(row=2, padx=5, column=(Subtitle_1.index("Due datetime") + 1))

# Product
product_list = ["Pudding"]
product = ttk.Combobox(root, values=product_list, width=12, state="readonly")
product.grid(row=2, column=(Subtitle_1.index("Product")))

# Make new data to tuple
New_order_tup = (new_order_number, En_Customername.get(), product.get(),
                 En_Order_Qty.get(), str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                 collect_time_str[0])


# Data Record Title
Title_frame = Frame(root, bg='orange')
Title_frame.grid(row=5, column=0, columnspan=9, sticky='news')
Title_Label = Label(Title_frame, text="Order records")
Title_Label.pack(padx=10, pady=10, side=LEFT)

# Current date
currentDT2 = datetime.datetime.now()
Date_Record = Label(Title_frame, text=(currentDT2.strftime("%Y-%m-%d")))
Date_Record.pack(padx=10, pady=10, side=RIGHT)
Title_Label = Label(Title_frame, text="Current Date", bg='plum')
Title_Label.pack(padx=10, pady=10, side=RIGHT)

# Show data
order_des_show = []
order_show = []


def show_data():
    try:
        print("_____________________")
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = f"""
                SELECT Order_Number, Customer, Product, Order_Quantity,
                Record_Datetime, Due_Datetime, Progress FROM Order_Records ORDER BY Order_Number DESC LIMIT {select_filter.get()}
            """
            order_des_show.clear()
            order_show.clear()
            for row in con.execute(sql_cmd):
                order_des_show.append(row)
                print(row)
            con.execute(sql_cmd)
        print("_____________________")
        print(order_des_show)
        print(len(order_des_show))
        for s in range(len(order_des_show)):
            order_show.append(order_des_show[len(order_des_show) - 1 - s])
        print(order_show)
        data_order_table()
        print("_____________________")
    except Exception as e:
        print("Error -> {}".format(e))


def data_order_table():
    for order in range(max(see_data)):
        for order_data in range(len(Subtitle_1)+1):
            Label(root, text="", bg='light salmon').grid(sticky="news", row=order + 8, column=order_data, padx=1)
    for order in range(int(select_filter.get())):
        for order_data in range(len(Subtitle_1)+1):
            if order_show[order][order_data] == 'Waiting':
                Label(root, text=order_show[order][order_data], bg='Red').grid(sticky="news", row=order + 8, column=order_data, padx=1)
            elif order_show[order][order_data] == 'Work in process':
                Label(root, text=order_show[order][order_data], bg='yellow').grid(sticky="news", row=order + 8, column=order_data, padx=1)
            elif order_show[order][order_data] == 'Finished':
                Label(root, text=order_show[order][order_data], bg='green').grid(sticky="news", row=order + 8, column=order_data, padx=1)
            else:
                Label(root, text=order_show[order][order_data], bg='light salmon').grid(sticky="news", row=order + 8, column=order_data, padx=1)


# Filter
Title_frame2 = Frame(root, bg='light salmon')
Title_frame2.grid(row=6, column=0, columnspan=5, sticky='news')
Label(Title_frame2, text='Select latest').pack(side=LEFT, padx=10, pady=10)
see_data = [5, 10, 15, 20]
select_filter = ttk.Combobox(Title_frame2, values=list(see_data), width=3, state="readonly")
select_filter.pack(side=LEFT)
select_filter.current(0)
submit_filter = Button(Title_frame2, text="select", bg='pink', command=show_data)
submit_filter.pack(side=LEFT, padx=10, ipady=2)
Title_frame3 = Frame(root, bg='coral')
Title_frame3.grid(row=6, column=5, columnspan=2, sticky='news')

# Subtitle2
Subtitle_2 = ["Order NO.", "Customer", "Product", "Order Quantity", "Record datetime", "Due datetime", "Progress"]
for e, i in enumerate(Subtitle_2):
    Label(root, text=i, bg="magenta",width=col_width).grid(row=7, column=(e), padx=1, sticky='news')


def custom_data():
    root3 = Tk()
    root3.title("Custom data")
    root3.option_add("*Font", "arial 11")
    Subtitle_2 = ["Order NO.", "Customer", "Product", "Order Quantity", "Record datetime", "Due datetime", "Progress"]
    for e, i in enumerate(Subtitle_2):
        Label(root3, text=i, bg="magenta",width=col_width).grid(row=1, column=(e), padx=1, sticky='news')
    # fill serial number
    Custom_num = DoubleVar()
    custom_select = Entry(root3, textvariable=Custom_num, width=col_width)
    custom_select.grid(row=2, column=(Subtitle_1.index("Order NO.")))

    # Search data
    def search_dt():
        try:
            searching = []
            with sqlite3.connect("Production_Plan.sqlite") as con:
                sql_cmd = f"""
                    SELECT * FROM Order_Records WHERE Order_Number = {custom_select.get()}
                """
                for i in con.execute(sql_cmd):
                    print(i)
                    searching.append(i)
                for x in range(len(searching[0]) - 1):
                    # print(searching[0][x + 1])
                    if searching[0][x + 1] == 'Waiting':
                        Label(root3, text=searching[0][x + 1], bg='Red',width=col_width).grid(sticky="news", row=2, column=x + 1,
                                                                                   padx=1)
                    elif searching[0][x + 1] == 'Work in process':
                        Label(root3, text=searching[0][x + 1], bg='Yellow',width=col_width).grid(sticky="news", row=2, column=x + 1,
                                                                                   padx=1)
                    else:
                        Label(root3, text=searching[0][x + 1], bg='light salmon',width=col_width).grid(sticky="news", row=2, column=x + 1,
                                                                                   padx=1)
                con.execute(sql_cmd)
        except Exception as e:
            messagebox.showerror("error!", e)

    # Delete data
    def delete_dt():
        try:
            with sqlite3.connect("Production_Plan.sqlite") as con:
                sql_cmd = f"""
                      DELETE FROM Order_Records WHERE Order_Number = {custom_select.get()}
                  """
                sql_cmd_prod_plan = f"""
                      DELETE FROM Production_plan WHERE Order_Number = {custom_select.get()}
                  """
                con.execute(sql_cmd)
                con.execute(sql_cmd_prod_plan)
                messagebox.showinfo("Delete", "Delete successfully!")
            show_data()
            working_hour_show()
        except Exception as e:
            print("Error -> {}".format(e))

    delete_submit = Button(root3, text="delete", bg='pink', command=delete_dt)
    delete_submit.grid(row=4, column=len(Subtitle_1), sticky='se', pady=1)
    # edit_submit = Button(root3, text="edit", bg='pink', command=edit_dt)
    # edit_submit.grid(row=4, column=len(Subtitle_1)-2, sticky='se', pady=1)
    search_submit = Button(root3, text="search", bg='pink', command=search_dt)
    search_submit.grid(row=4, column=0, sticky='ws', pady=1)
    root3.mainloop()


# custom filter
custom_filter = Button(Title_frame2, text="custom", bg='pink', command=custom_data)
custom_filter.pack(side=LEFT, padx=10, ipady=2)

# Edit and Delete
# delete_data = Button(Title_frame2, text="delete", bg='pink', command=custom_data)
# delete_data.pack(side=RIGHT, padx=10, ipady=2)
edit_data = Button(Title_frame2, text="edit", bg='pink', command=custom_data)
edit_data.pack(side=LEFT, padx=10, ipady=2)

for order in range(max(see_data)):
    for order_data in range(len(Subtitle_1)+1):
        Label(root, text="", bg='light salmon').grid(sticky="news", row=order + 8, column=order_data, padx=1)

# Working hour show # Maximum eff. calculator
select_setting_data()
Select_fill_Data()
def working_hour_show():
    # Operation
    start_day = setting_lst[0][1] 
    end_day = setting_lst[0][2]
    start_add_day = f'02/18/00 {start_day}'
    end_add_day = f"02/18/00 {end_day}"
    convert_start_day = time.strptime(start_add_day, '%m/%d/%y %H:%M:%S')
    convert_end_day = time.strptime(end_add_day, '%m/%d/%y %H:%M:%S')
    mk_start_day = time.mktime(convert_start_day) # day after EPOCH DAY needed to perform mk.time command.
    mk_end_day = time.mktime(convert_end_day)
    diff_time = mk_end_day-mk_start_day
    # Max Eff. # (ROUNDDOWN(Working time/Ideal production time))*Unit per batch
    working_time_cal = int(diff_time // 60)
    ideal_min_cal = setting_lst[0][0]
    unit_p_batch_cal = unit_per_batch[0]
    max_eff_unit = (working_time_cal//ideal_min_cal)*unit_p_batch_cal
    # Effective eff. # (ROUNDDOWN(Working time/Expected production time))*Unit per batch
    expected_min_cal = setting_lst[0][3]
    efc_eff_unit = (working_time_cal//expected_min_cal)*unit_p_batch_cal
    # Check left capacity
    sum_used = []
    time_lst = []
    select_data_eff()
    current_local_time = time.strftime("%Y-%m-%d") # current_local_time
    len_dat = len(data_lst_eff)
    # get date form
    for e,i in enumerate(data_lst_eff):
        get_time = data_lst_eff[e][-2]
        time_to_num = time.strptime(get_time, "%Y-%m-%d %H:%M:%S") #Change to structime
        time_string = time.strftime("%Y-%m-%d", time_to_num)
        time_lst.append(time_string)
    print(time_lst)
    for e in range(len_dat):
        del data_lst_eff[e][-2]
        data_lst_eff[e].insert(5, time_lst[e])
    print(data_lst_eff)
    # compare with current date
    print((current_local_time),"AA")
    for e in range(len_dat):
        if data_lst_eff[e][-2] == (current_local_time):
            print(data_lst_eff[e][-2])
            sum_used.append(data_lst_eff[e][3])
    print(sum_used)
    print(sum(sum_used))
    today_remain = efc_eff_unit-sum(sum_used)
    print(today_remain)
    if today_remain >= 0:
        ramain_cap_show = Label(root, text=f"{today_remain}", bg='pink')
        ramain_cap_show.grid(row=6, column=6 , sticky='news')
        ramain_cap = Label(root, text="Today remaining capacity", bg='pink')
        ramain_cap.grid(row=6, column=5,sticky='news')
    if today_remain < 0:
        ramain_cap_show = Label(root, text=f"({today_remain})", bg='pink')
        ramain_cap_show.grid(row=6, column=6, sticky='news')
        ramain_cap = Label(root, text="Overload capacity", bg='pink')
        ramain_cap.grid(row=6, column=5, sticky='news')
    print(efc_eff_unit-max_eff_unit)
    if today_remain < (efc_eff_unit-max_eff_unit):
        ramain_cap_show = Label(root, text=f"({today_remain})", bg='pink')
        ramain_cap_show.grid(row=6, column=6, sticky='news')
        ramain_cap = Label(root, text="Exceeding maximum capacity!!", bg='pink')
        ramain_cap.grid(row=6, column=5, sticky='news')



# add new order
def new_order_ex():
    global new_order_number
    n_order_num = new_order_number
    n_customer = En_Customername.get()
    n_product = product.get()
    n_qty = float(En_Order_Qty.get())
    n_record = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    n_due = collect_time_str[0]

    try:
        with sqlite3.connect("Production_Plan.sqlite") as con:
            if n_customer == "" or n_product == "" or n_qty == (0 or "") or n_due == 0:
                messagebox.showerror('Data Missing!', 'Data Missing!')
                pass
            else:
                sql_cmd = f'''
                INSERT INTO Order_Records (Order_Number, Customer, Product, Order_Quantity,
                Record_Datetime, Due_Datetime, Progress) VALUES ({n_order_num}, '{n_customer}',
                '{n_product}', {n_qty}, '{n_record}', '{n_due}', 'Waiting')'''
                sql_cmd_prod_plan = f'''
                INSERT INTO Production_plan (Due_time, Order_Number, Order_Quantity, progress) 
                VALUES ('{n_due}', {n_order_num}, {n_qty}, 'Waiting')'''
                # print(sql_cmd)
                con.execute(sql_cmd)
                con.execute(sql_cmd_prod_plan)
                new_order_number = new_order_number + 1
                order_number()
                messagebox.showinfo("Success", "Order has been added successfully!")
        show_data()
        working_hour_show()
    except Exception as e:
        print("Error -> {}".format(e))

# Get_data
Get_data_frame = Frame(root, bg='blue violet')
Get_data_frame.grid(row=3, column=0, columnspan=9, sticky='news')
order_button = Button(Get_data_frame, text="add order", bg="LightSkyBlue1", command=new_order_ex)
order_button.pack(padx=50, pady=5, side=RIGHT)

working_hour_show()

root.mainloop()
