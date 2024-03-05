"""
Filename: purchaseRecords.py
Description: This script functions as a purchase record which designed to tracking prucurement.
Author: Dumri Ketupanya
Date created: June 8, 2017
"""

# import required modules =====================================================================================
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from datetime import date
from datetime import time
import datetime

# SQLite Database Connection ===================================================================================
def create_purchased_table():
    try:
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            CREATE table PurchasedRecord(Purchased_Number real primary key,
            Date_of_Purchase text, Serial_Number real, Name text,
            Order_Quantity real, Unit_Quantity real, Unit text, 
            Cost_Actual_Baht real, Production_Date text,
            Expiration_Date text);
            """
            con.execute(sql_cmd)
    except Exception as e:
        print("Error -> {}".format(e))


def create_inven_table():
    try:
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            CREATE table InventoryManagement(Serial_Number real, Name text, Unit_Quantity_init real, Unit_Quantity_left real
            , Unit text, Cost_init_Baht real, Cost_left_Baht real, Expiration_Date text);
            """
            con.execute(sql_cmd)
    except Exception as e:
        print("Error -> {}".format(e))


data_list = []


def select_product_data():
    try:
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Ingredient_data
            """
            for row in con.execute(sql_cmd):
                data_list.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))


data_pur = []


def select_purchased_data():
    try:
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            SELECT * FROM PurchasedRecord
            """
            for row in con.execute(sql_cmd):
                data_pur.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))


data_inventory = []


def select_inven_data():
    try:
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            SELECT * FROM InventoryManagement
            """
            for row in con.execute(sql_cmd):
                data_inventory.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))


create_purchased_table()
create_inven_table()
select_product_data()
select_purchased_data()
print(data_inventory)

#  User Interface and Program Logic Section ======================================================================================
root = Tk()
root.title("Purchased Records")
root.option_add("*Font", "arial 11")

# Title
Title_frame = Frame(root, bg='blue violet')
Title_frame.grid(row=0, column=0, columnspan=10, sticky='news')
Title_Label = Label(Title_frame, text="Newly purchased")
Title_Label.pack(padx=10, pady=10, side=LEFT)
row_num = 9
# Subtitle
Subtitle_1 = ["Purchased NO.", "Date of Purchase", "", "Serial NO.", "Name", "Order Quantity", "Unit Quantity", "Unit",
              "Cost (Baht)", "Production Date", "", "Expiration Date", ""]
for e, i in enumerate(Subtitle_1):
    Label(root, text=i, bg="magenta").grid(row=(e // row_num) * 2 + 1, column=(e) % row_num, padx=1, sticky='news')

collect_time_purchase = [0]


def calendar_purchase():
    root2 = Tk()

    def date_submit(e):
        collect_date = date(int(year.get()), int(month.get()), int(day.get()))
        collect_time = time(int(hour.get()), int(minute.get()), int(sec.get()))
        collect_time_print = f"{collect_date} {collect_time}"
        collect_time_purchase.insert(0, f"{collect_date} {collect_time}")  # To collect time
        # print(collect_date)
        # print(collect_time)
        # print(currentDT)
        Due_Time = Label(root, text=collect_time_print, bg="plum")
        Due_Time.grid(row=2, column=(Subtitle_1.index("Date of Purchase")))

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


collect_time_produce = [0]


def calendar_product():
    root2 = Tk()

    def date_submit(e):
        collect_date = date(int(year.get()), int(month.get()), int(day.get()))
        collect_time_print = f"{collect_date}"
        collect_time_produce.insert(0, f"{collect_date}")  # To collect time
        # print(collect_date)
        # print(collect_time)
        # print(currentDT)
        product_date.grid_forget()
        Due_Time = Label(root, text=collect_time_print, bg="plum", width=19)
        Due_Time.grid(row=4, column=((Subtitle_1.index("Production Date")) % row_num))

    root2.title("Calendar")
    root2.option_add("*Font", "consolas 15")
    day_list = range(1, 32)
    month_list = (range(1, 13))
    year_list = range(2019, 2030)
    title = ["Day", "Month", "Year"]
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
    submit = Button(root2, text="Submit", bg='cornsilk')
    submit.grid(row=1, column=len(title) + 1, padx=10)
    submit.bind("<Button-1>", date_submit)
    root2.mainloop()


collect_time_expired = [0]


def calendar_expired():
    root2 = Tk()

    def date_submit(e):
        collect_date = date(int(year.get()), int(month.get()), int(day.get()))
        collect_time_print = f"{collect_date} "
        collect_time_expired.insert(0, f"{collect_date}")  # To collect time
        # print(collect_date)
        # print(type(collect_date))
        # print(collect_time)
        # print(currentDT)
        exp_date.grid_forget()
        Due_Time = Label(root, text=collect_time_print, bg="plum", width=15)
        Due_Time.grid(row=4, column=((Subtitle_1.index("Expiration Date") % row_num)))

    root2.title("Calendar")
    root2.option_add("*Font", "consolas 15")
    day_list = range(1, 32)
    month_list = (range(1, 13))
    year_list = range(2019, 2030)
    title = ["Day", "Month", "Year", ]
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
    submit = Button(root2, text="Submit", bg='cornsilk')
    submit.grid(row=1, column=len(title) + 1, padx=10)
    submit.bind("<Button-1>", date_submit)
    root2.mainloop()


# Purchase Number
if data_pur == []:
    new_pur_number = 0
else:
    new_pur_number = (data_pur[-1][0]) + 1


def pur_num():
    purchase_num = Label(root, text=new_pur_number, width=19, bg="plum")
    purchase_num.grid(row=2, column=((Subtitle_1.index("Purchased NO.")) % row_num), sticky="e")


pur_num()

date_width = 15
# Date of Purchase
pur_date = Label(root, width=date_width, text="Set date of purchase", bg="plum")
pur_date.grid(row=2, column=((Subtitle_1.index("Date of Purchase")) % row_num))
add_pur_time = Button(root, text="edit time", height=1, bg="plum", command=calendar_purchase)
add_pur_time.grid(row=2, padx=5, column=((Subtitle_1.index("Date of Purchase")) % row_num + 1))

# Production date
product_date = Label(root, width=19, text="Set production date", bg="plum")
product_date.grid(row=4, column=((Subtitle_1.index("Production Date")) % row_num))
add_product_date = Button(root, text="edit time", height=1, bg="plum", command=calendar_product)
add_product_date.grid(row=4, padx=5, column=((Subtitle_1.index("Production Date")) % row_num + 1))

# Expired date
exp_date = Label(root, width=date_width, text="Set expiration date", bg="plum")
exp_date.grid(row=4, column=((Subtitle_1.index("Expiration Date")) % row_num))
add_exp_date = Button(root, text="edit time", height=1, bg="plum", command=calendar_expired)
add_exp_date.grid(row=4, padx=5, column=((Subtitle_1.index("Expiration Date") % row_num) + 1))

# Name
product_name = []


def select_name():
    for e, i in enumerate(data_list):
        product_name.append(data_list[e][1])

wid = 4

select_name()
product = ttk.Combobox(root, values=product_name, width=22, state="readonly")
product.grid(row=2, column=((Subtitle_1.index("Name")) % row_num))

# Order quantity
order_quan_set = DoubleVar()
en_order_quan = Entry(root, textvariable=order_quan_set)
en_order_quan.grid(row=2, column=((Subtitle_1.index("Order Quantity")) % row_num))

# Actual Cost
cost_set = DoubleVar()
en_cost = Entry(root, textvariable=cost_set)
en_cost.grid(row=2, column=((Subtitle_1.index("Cost (Baht)")) % row_num))

# Serial number
serial_num = Label(root, width=12, text="", bg="plum")
serial_num.grid(row=2, column=((Subtitle_1.index("Serial NO.")) % row_num), sticky="e")

# Product unit
product_unit = Label(root, width=12, text="", bg="plum")
product_unit.grid(row=2, column=((Subtitle_1.index("Unit")) % row_num), sticky="e")

# product quantity
product_quan = Label(root, width=12, text="", bg="plum")
product_quan.grid(row=2, column=((Subtitle_1.index("Unit Quantity")) % row_num), sticky="e")

# Check
serial = []
unit_a = []
unit_quan_a = []


def check():
    select_product_data()
    # print(product.get())
    # print(data_list)
    product_check = product.get()
    quantity = en_order_quan.get()
    for e, i in enumerate(data_list):
        if data_list[e][1] == product_check:
            serial.clear()
            serial_local = data_list[e][0]
            serial.append(serial_local)
            serial_num = Label(root, width=12, text=f"{serial_local}", bg="plum")
            serial_num.grid(row=2, column=((Subtitle_1.index("Serial NO.")) % row_num), sticky="e", padx=1)
        if data_list[e][1] == product_check:
            unit_a.clear()
            unit_a_local = data_list[e][6]
            unit_a.append(unit_a_local)
            product_unit = Label(root, width=12, text=f"{unit_a_local}", bg="plum")
            product_unit.grid(row=2, column=((Subtitle_1.index("Unit")) % row_num), sticky="e", padx=1)
        if data_list[e][1] == product_check:
            unit_quan_a.clear()
            unit_quan_a_local = float(data_list[e][4]) * float(quantity)
            unit_quan_a.append(unit_quan_a_local)
            product_quan = Label(root, width=12, text=f"{unit_quan_a_local}", bg="plum")
            product_quan.grid(row=2, column=((Subtitle_1.index("Unit Quantity")) % row_num), sticky="e", padx=1)


# Check button
but_check = Button(root, text="check", bg="green yellow", width=9, command=check)
but_check.grid(row=4, sticky="w", column=((Subtitle_1.index("Expiration Date")) % row_num + 2))


# Add
def new_purchase_ex():
    check()
    global new_pur_number
    try:
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            if collect_time_purchase == [0] or serial == [] or product.get() == '' or en_order_quan.get() == '0.0' or \
                    unit_a == [] or unit_quan_a == [] or en_cost.get() == '0.0' or \
                    collect_time_produce == [0] or collect_time_expired == [0]:
                messagebox.showerror('Data Missing!', 'Data Missing!')
                pass
            else:
                dat = {"n_pur_num": new_pur_number, "n_date_purchase": collect_time_purchase[0],
                       "n_serial_num": serial[0], "n_name": product.get(),
                       "n_order_qty": en_order_quan.get(), "n_unit_qty": unit_quan_a[0], "n_unit": unit_a[0],
                       "n_cost_baht": en_cost.get(), "n_date_product": collect_time_produce[0],
                       "n_date_exp": collect_time_expired[0]}
                sql_cmd = f'''
                INSERT INTO  PurchasedRecord (Purchased_Number, Date_of_Purchase, Serial_Number, Name,
                Order_Quantity, Unit_Quantity, Unit, Cost_Actual_Baht,
                Production_Date, Expiration_Date) VALUES ({dat.get("n_pur_num")},'{dat.get("n_date_purchase")}', {dat.get("n_serial_num")},
                '{dat.get("n_name")}', {dat.get("n_order_qty")}, {dat.get("n_unit_qty")}, '{dat.get("n_unit")}',
                {dat.get("n_cost_baht")}, '{dat.get("n_date_product")}', '{dat.get("n_date_exp")}')'''
                # print(sql_cmd)
                con.execute(sql_cmd)
                new_pur_number = new_pur_number + 1
                pur_num()
                messagebox.showinfo("Success", "Purchase record has been added successfully!")
                #######################
                select_inven_data()
                # print(dat.get("n_date_exp"))
                # print(float(dat.get("n_serial_num")))
                repeat_check = []
                for e, i in enumerate(data_inventory):
                    if dat.get("n_date_exp") == data_inventory[e][7] and float(dat.get("n_serial_num")) == \
                            data_inventory[e][0]:
                        repeat_check.append("1")
                        # print(repeat_check)
                        # print(data_inventory[e])
                        old_quan_data = data_inventory[e][2]
                        old_quan_left_data = data_inventory[e][3]
                        # (old_quan_left_data)
                        old_cost_data = data_inventory[e][5]
                        old_cost_left_data = data_inventory[e][6]
                        # print(old_cost_left_data)
                        new_quan_data = old_quan_data + float(dat.get("n_unit_qty"))
                        new_quan_left_data = old_quan_left_data + float(dat.get("n_unit_qty"))
                        new_cost_data = old_cost_data + float(dat.get("n_cost_baht"))
                        new_cost_left_data = old_cost_left_data + float(dat.get("n_cost_baht"))
                        update_inven = f"""UPDATE InventoryManagement SET Unit_Quantity_init = {new_quan_data}, Cost_init_Baht = {new_cost_data},
                                        Unit_Quantity_left = {new_quan_left_data}, Cost_left_Baht = {new_cost_left_data}
                                        WHERE Expiration_Date = '{data_inventory[e][7]}' AND Serial_Number = {data_inventory[e][0]} """
                        con.execute(update_inven)
                        print(update_inven)
                        break
                if len(repeat_check) == 1:
                    pass
                else:
                    insert_inven = f'''
                    INSERT INTO InventoryManagement (Serial_Number, Name, Unit_Quantity_init, Unit_Quantity_left,
                    Unit, Cost_init_Baht, Cost_left_Baht, Expiration_Date) VALUES ({dat.get("n_serial_num")}, '{dat.get("n_name")}',
                    {dat.get("n_unit_qty")}, {dat.get("n_unit_qty")}, '{dat.get("n_unit")}', {dat.get("n_cost_baht")}, 
                    {dat.get("n_cost_baht")}, '{dat.get("n_date_exp")}')'''
                    # print(repeat_check)
                    print(insert_inven)
                    con.execute(insert_inven)
                repeat_check.clear()
                data_inventory.clear()
                ######################
    except Exception as e:
        print("Error -> {}".format(e))


# Add button
add_check = Button(root, text="add", bg="turquoise", width=10, command=new_purchase_ex)
add_check.grid(row=4, sticky="w", column=((Subtitle_1.index("Expiration Date")) % row_num + 3))

# ____________________________________Show data____________________________________
# Show data table
order_des_show = []
order_show = []


def show_data():
    try:
        print("_____________________")
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = f"""
                SELECT * FROM PurchasedRecord ORDER BY Purchased_Number DESC LIMIT {select_filter.get()}
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
        print("_____________________")
        crate_pur_table()
    except Exception as e:
        print("Error -> {}".format(e))

def crate_pur_table(): ###########################
    for r in range(max(see_data)):
        for col in range(len(Subtitle_2)):
            Label(root, text="", bg='light salmon',width=wid).grid(sticky="news", row=r + 8, column=col, padx=1)
    for order in range(int(select_filter.get())):
        for order_data in range(len(Subtitle_2)):
            Label(root, text=order_show[order][order_data], bg='light salmon',width=wid).grid(sticky="news"
                                                                                              , row=order + 8,
                                                                                    column=order_data, padx=1)


def custom_data():
    root3 = Tk()
    root3.title("Custom data")
    root3.option_add("*Font", "consolas 13")
    Subtitle_cus = ["Purchased number", "Date of Purchase", "Serial NO.", "Name", "Order Quantity", "Unit Quantity",
                    "Unit", "Cost (Baht)", "Production Date", "Expiration Date"]
    for e, i in enumerate(Subtitle_cus):
        Label(root3, text=i, bg="magenta").grid(row=1, column=(e), padx=1, sticky='news')
    # fill serial number
    Custom_pur_num = DoubleVar()
    custom_select = Entry(root3, textvariable=Custom_pur_num, width=len("Purchased NO."))
    custom_select.grid(row=2, column=(Subtitle_1.index("Purchased NO.")))

    # Search data
    def search_dt():
        try:
            searching = []
            with sqlite3.connect("Inventory_Management.sqlite") as con:
                sql_cmd = f"""
                    SELECT * FROM PurchasedRecord WHERE Purchased_Number = {custom_select.get()}
                """
                for i in con.execute(sql_cmd):
                    # print(i)
                    searching.append(i)
                for x in range(len(searching[0]) - 1):
                    Label(root3, text=searching[0][x + 1], bg='light salmon').grid(sticky="news", row=2, column=x + 1,
                                                                                   padx=1)
                con.execute(sql_cmd)
            # print(searching)
        except Exception as e:
            messagebox.showerror("error!", e)

    # Delete data
    def delete_dt():
        try:
            select_inven_data()
            prep_del = []
            with sqlite3.connect("Inventory_Management.sqlite") as con:
                sql_cmd_prep = f"""
                    SELECT Serial_Number, Unit_Quantity, Cost_Actual_Baht, 
                    Expiration_Date  FROM PurchasedRecord WHERE Purchased_Number = {custom_select.get()}
                """
                for i in con.execute(sql_cmd_prep):
                    # print(i)
                    prep_del.append(i)
                for e, i in enumerate(data_inventory):
                    if prep_del[0][3] == data_inventory[e][7] and float(prep_del[0][0]) == data_inventory[e][0]:
                        print(prep_del)
                        old_quan_data = data_inventory[e][2]
                        old_quan_left_data = data_inventory[e][3]
                        old_cost_data = data_inventory[e][5]
                        old_cost_left_data = data_inventory[e][6]
                        new_quan_data = old_quan_data - float(prep_del[0][1])
                        new_quan_left_data = old_quan_left_data - float(prep_del[0][1])
                        new_cost_data = old_cost_data - float(prep_del[0][2])
                        new_cost_left_data = old_cost_left_data - float(prep_del[0][2])
                        update_inven_2 = f"""UPDATE InventoryManagement SET Unit_Quantity_init = {new_quan_data}, Cost_init_Baht = {new_cost_data},
                                        Unit_Quantity_left = {new_quan_left_data}, Cost_left_Baht = {new_cost_left_data}
                                        WHERE Expiration_Date = '{data_inventory[e][7]}' AND Serial_Number = {data_inventory[e][0]} """
                        con.execute(update_inven_2)
                        print(update_inven_2)
                        data_inventory.clear()
                        break
            with sqlite3.connect("Inventory_Management.sqlite") as con:
                sql_cmd = f"""
                      DELETE FROM PurchasedRecord WHERE Purchased_Number = {custom_select.get()}
                  """
                con.execute(sql_cmd)
                messagebox.showinfo("Delete", "Delete successfully!")
        except Exception as e:
            print("Error -> {}".format(e))

    delete_submit = Button(root3, text="delete", bg='pink', command=delete_dt)
    delete_submit.grid(row=4, column=len(Subtitle_2) - 1, sticky='se', pady=1)
    # edit_submit = Button(root3, text="edit", bg='pink', command=edit_dt)
    # edit_submit.grid(row=4, column=len(Subtitle_1)-2, sticky='se', pady=1)
    search_submit = Button(root3, text="search", bg='pink', command=search_dt)
    search_submit.grid(row=4, column=0, sticky='ws', pady=1)
    root3.mainloop()


# Title
Title_frame = Frame(root, bg='chocolate1')
Title_frame.grid(row=5, column=0, columnspan=10, sticky='news')
Title_Label = Label(Title_frame, text="Purchased records")
Title_Label.pack(padx=10, pady=10, side=LEFT)
filter_frame = Frame(root, bg='chocolate1')
filter_frame.grid(row=6, column=0, columnspan=10, sticky='news')
Label(filter_frame, text='Select latest').pack(side=LEFT, padx=10, pady=10)

# Filter
see_data = [5, 10, 15]
select_filter = ttk.Combobox(filter_frame, values=list(see_data), width=3, state="readonly")
select_filter.pack(side=LEFT)
select_filter.current(0)
submit_filter = Button(filter_frame, text="select", bg='pink', command=show_data)
submit_filter.pack(side=LEFT, padx=10, ipady=2)

# Custom filter
custom_filter = Button(filter_frame, text="custom", bg='pink', command=custom_data)
custom_filter.pack(side=LEFT, padx=10, ipady=2)

# Subtitle
Subtitle_2 = ["Purchased number", "Date of Purchase", "Serial NO.", "Name", "Order Quantity", "Unit Quantity", "Unit",
              "Cost (Baht)", "Production Date", "Expiration Date"]
for e, i in enumerate(Subtitle_2):
    Label(root, text=i, bg="tan1").grid(row=7, column=e, padx=1, sticky='news')


# Create plain table
def crate_plain_table():
    for r in range(max(see_data)):
        for col in range(len(Subtitle_2)):
            Label(root, text="", bg='light salmon',width=12).grid(sticky="news", row=r + 8, column=col, padx=1)


crate_plain_table()

root.mainloop()
