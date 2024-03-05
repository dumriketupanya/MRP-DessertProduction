"""
Filename: IMS.py
Description: This script serves as the Inventory Management System (IMS). Which use for inventory management and tracking.
Author: Dumri Ketupanya
Date created: June 8, 2017
"""

# import required modules =====================================================================================
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk  # ttk -> themed tk (for Combobox)
from datetime import date, datetime, time
from time import strptime

# SQLite Database Connection ===================================================================================
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


data_bom_list = []


def select_product_data():
    try:
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Ingredient_data
            """
            for row in con.execute(sql_cmd):
                data_bom_list.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))


data_invent_list = []

def select_invent_data():
    try:
        data_invent_list.clear()
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            SELECT * FROM InventoryManagement
            """
            for row in con.execute(sql_cmd):
                data_invent_list.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))

def clear_zero():
    try:
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            for e,i in enumerate(data_invent_list):
                if data_invent_list[e][2] == 0:
                    sql_cmd = f"""
                          DELETE FROM InventoryManagement WHERE Unit_Quantity_init = 0
                      """
                    con.execute(sql_cmd)
    except Exception as e:
        print("Error -> {}".format(e))

create_inven_table()
select_product_data()
select_invent_data()
print(data_invent_list)
clear_zero()

# User Interface Section =======================================================================================
root = Tk()
root.title("Inventory Management")
root.option_add("*Font", "arial 11")

# Title
Title_frame = Frame(root, bg='SteelBlue1')
Title_frame.grid(row=0, column=0, columnspan=10, sticky='news')
Title_Label = Label(Title_frame, text="Overall Inventory")
Title_Label.pack(padx=10, pady=10, side=LEFT)

# Overview
col_num = 9
header_width = 17
overview_frame = Frame(root, bg='LightSkyBlue1')
overview_frame.grid(row=1, column=0, columnspan=10, sticky='news')
overview_1 = ["Serial NO.", "Name", "Available", "Unit", "Remaining Cost (Baht)"]
for e, i in enumerate(overview_1):
    Label(overview_frame, text=i, width=header_width, bg="magenta").grid(row=(e // col_num) * 2 + 1,
                                                                         column=(e) % col_num, padx=1, sticky='news')

# Serial  number
# Date of Purchase
overview_dat_frame = Frame(root, bg='LightSkyBlue1')
overview_dat_frame.grid(row=2, column=0, columnspan=10, sticky='news')
serial_num = Label(overview_dat_frame, width=header_width, text="", bg="plum")
serial_num.grid(row=2, column=((overview_1.index("Serial NO.")) % col_num), padx=1, sticky="e")

# select Name
product_name = []
def select_name(x):
    for e, i in enumerate(data_bom_list):
        product_name.append(data_bom_list[e][x])

# Name Combobox
select_name(1)
product = ttk.Combobox(overview_dat_frame, values=product_name, width=header_width, state="readonly")
product.grid(row=2, column=((overview_1.index("Name")) % col_num), padx=1)

# Available
avialable = Label(overview_dat_frame, width=header_width, text="", bg="plum")
avialable.grid(row=2, column=((overview_1.index("Available")) % col_num), sticky="e", padx=1)

# Unit
unit_title = Label(overview_dat_frame, width=header_width, text="", bg="plum")
unit_title.grid(row=2, column=((overview_1.index("Unit")) % col_num), sticky="e", padx=1)

# Remaining cost
remaining_cost = Label(overview_dat_frame, width=header_width, text="", bg="plum")
remaining_cost.grid(row=2, column=((overview_1.index("Remaining Cost (Baht)")) % col_num), sticky="e", padx=1)

# Sub Program - Overall check =======================================================================================
check_qty_left = []
check_cost_left = []
def overall_check():
    ################
    product_check = product.get()
    for e, i in enumerate(data_bom_list):
        if data_bom_list[e][1] == product_check:
            serial_local = data_bom_list[e][0]
            unit_local = data_bom_list[e][6]
            serial_num = Label(overview_dat_frame, width=header_width, text=f"{serial_local}", bg="plum")
            serial_num.grid(row=2, column=((overview_1.index("Serial NO.")) % col_num), padx=1, sticky="e")
            unit_show = Label(overview_dat_frame, width=header_width, text=f"{unit_local}", bg="plum")
            unit_show.grid(row=2, column=((overview_1.index("Unit")) % col_num), padx=1, sticky="e")
    #################
    pub_date = date.today()
    max_pub_date_time = datetime.combine(pub_date, time.max)  # Make time to 23:59:59
    con_current_DT = max_pub_date_time.strftime("%Y-%m-%d")
    date_current = datetime.strptime(con_current_DT, '%Y-%m-%d').date()
    for e, r in enumerate(range(len(data_invent_list))):
        get_date = data_invent_list[r][len(table_title) - 2]
        change_type_date = datetime.strptime(get_date, '%Y-%m-%d').date()
        if date_current >= change_type_date:
            pass
            # Label(root, text="Expired", bg='red').grid(sticky="news", row=e + 7, column=col_num - 1, padx=1)
        else:
            # Label(root, text="Available", bg='green2').grid(sticky="news", row=e + 7, column=col_num - 1, padx=1)
            if product_check == data_invent_list[r][1]:
                check_qty_left.append(data_invent_list[e][3])
                check_cost_left.append(data_invent_list[e][6])
    sum_qty_left = sum(check_qty_left)
    sum_cost_left = sum(check_cost_left)
    if product_check == "":
        sum_cost_left = ""
        sum_qty_left = ""
    l_sum_qty_left = Label(overview_dat_frame, width=header_width, text=sum_qty_left, bg="plum")
    l_sum_qty_left.grid(row=2, column=((overview_1.index("Available")) % col_num), sticky="e", padx=1)
    l_sum_cost_left = Label(overview_dat_frame, width=header_width, text=sum_cost_left, bg="plum")
    l_sum_cost_left.grid(row=2, column=((overview_1.index("Remaining Cost (Baht)")) % col_num), sticky="e", padx=1)
    check_qty_left.clear()
    check_cost_left.clear()


# Check button
check_name = Button(overview_dat_frame, text="check", bg="turquoise", width=10, command=overall_check)
check_name.grid(row=2, sticky="w", column=((overview_1.index("Remaining Cost (Baht)")) % col_num + 1))

# Data Visualization (Table) =======================================================================================
# Table title
table_frame_t = Frame(root, bg='forest green')
table_frame_t.grid(row=3, column=0, columnspan=10, sticky='news')
table_Label = Label(table_frame_t, text="Individual Inventory List")
table_Label.pack(padx=10, pady=10, side=LEFT)
table_label_t = Frame(root, bg='lime green')
table_label_t.grid(row=4, column=0, columnspan=10, sticky='news')
last_lable = Label(table_label_t, text="Select latest expiration date")
last_lable.pack(padx=10, pady=10, side=LEFT)

# Current time
currentDT = datetime.now()
table_Label = Label(table_frame_t, text=(currentDT.strftime("%Y-%m-%d")))
table_Label.pack(padx=10, pady=10, side=RIGHT)
table_Label = Label(table_frame_t, text="Current Date")
table_Label.pack(padx=10, pady=10, side=RIGHT)

# Table header
col_num = 9
table_title = ["Serial NO.", "Name", "Initial Quantity", "Quantity Left",
               "Unit", "Initial Cost (Baht)", "Remaining cost (Baht)", "Expiration Date", "Status"]
for e, i in enumerate(table_title):
    if table_title[e] != "Name":
        x = Label(root, text=i, width=header_width, bg="lawn green").grid(row=5, column=(e) % col_num, padx=1,
                                                                                 sticky='news')
    else:
        x = Label(root, text=i, width=header_width, bg="lawn green").grid(row=5, column=(e) % col_num, padx=1,
                                                                                 sticky='news')

# Time comparison
def time_compare():
    for e,i in enumerate(range(max(see_data)+1)):
        del_lab = Label(root, text= "", bg='light salmon').grid(sticky="news", row=e + 6, column=col_num - 1, padx=1)
    pub_date = date.today()
    max_pub_date_time = datetime.combine(pub_date, time.max)  # Make time to 23:59:59
    con_current_DT = max_pub_date_time.strftime("%Y-%m-%d")
    date_current = datetime.strptime(con_current_DT, '%Y-%m-%d').date()
    # print(order_sel_show)
    sort_datetime = []
    all_get_date = []
    sorted_dt = []
    sorted_data = []
    for e, r in enumerate(range(len(order_show))):
        print(order_show[r])
        get_date = list(order_show[r])
        con_get_date = list(order_show[r])
        # print(get_date)
        con_get_date[-1] = datetime.strptime(get_date[len(table_title) - 2], '%Y-%m-%d').date()
        all_get_date.append(con_get_date)
        # print(con_get_date)
        val_get_date = datetime.strptime(get_date[len(table_title) - 2], '%Y-%m-%d').date()
        sort_datetime.append(val_get_date)
    # print(all_get_date)
    sorted_dt = sorted(sort_datetime)
    seq = 0
    print(len(sorted_dt))
    for lo in range(len(sorted_dt)):
        for i in range(len(sorted_dt)):
            if all_get_date[i][-1] == sorted_dt[seq]:
                sorted_data.append(all_get_date[i])
                del all_get_date[i]
                seq = seq+1
                break
    # print(sorted_data)
    ##########################
    for r in range(max(see_data)):
        for col in range(len(table_title) - 1):
            Label(root, text="", bg='light salmon').grid(sticky="news", row=r + 6, column=col, padx=1)
    # Create form bottom to top
    sel_fil = 0
    if len(sorted_data) <= float(select_filter.get()):
        sel_fil = len(sorted_data)
    if len(sorted_data) > float(select_filter.get()):
        sel_fil = select_filter.get()
    # print(len(sorted_data))
    # print(sel_fil)
    if len(sorted_data) - int(sel_fil) != 0:
        for i in range(len(sorted_data)-int(sel_fil)):
            del sorted_data[0]
    for x in range(int(sel_fil)):
        for y in range(len(table_title) - 1):
            Label(root, text=sorted_data[x][y], bg='light salmon').grid(sticky="news", row=x + 6, column=y, padx=1)
    ############################
    for e, r in enumerate(range(len(sorted_data))):
        if date_current >= sorted_data[e][-1]:
            Label(root, text="Expired", bg='red').grid(sticky="news", row=e + 6, column=col_num - 1, padx=1)
        else:
            Label(root, text="Available", bg='green2').grid(sticky="news", row=e + 6, column=col_num - 1, padx=1)
            # print(date_current - change_type_date)
        get_date = ""
        change_type_date = ""

# Show data table
order_des_show = []
order_show = []

def show_data():
    try:
        print("1_____________________")
        prod_fil = select_prod_filter.get()
        num_lst =  select_filter.get()
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = f"""
                SELECT * FROM InventoryManagement  WHERE Name = '{prod_fil}'
            """
            order_des_show.clear()
            order_show.clear()
            for row in con.execute(sql_cmd):
                order_des_show.append(row)
                print(row)
            con.execute(sql_cmd)
        for s in range(len(order_des_show)):
            order_show.append(order_des_show[len(order_des_show) - 1 - s])
        ###########
        time_compare()
    except Exception as e:
        print("Error -> {}".format(e))


# Create table
def create_invent_table():
    for r in range(max(see_data)):
        for col in range(len(table_title) - 1):
            Label(root, text="", bg='light salmon').grid(sticky="news", row=r + 6, column=col, padx=1)
    for x in range(int(select_filter.get())):
        for y in range(len(table_title) - 1):
            Label(root, text=order_show[x][y], bg='light salmon').grid(sticky="news", row=x + 6, column=y, padx=1)


# Filter
see_data = [5, 10, 15]
select_filter = ttk.Combobox(table_label_t, values=list(see_data), width=3, state="readonly")
select_filter.pack(side=LEFT, padx=10, ipady=2)
select_filter.current(0)
select_prod_filter = ttk.Combobox(table_label_t, values=product_name, width=header_width - 2, state="readonly")
select_prod_filter.pack(side=LEFT, padx=5, ipady=2)
select_prod_filter.current(0)
submit_filter = Button(table_label_t, text="select", bg='pink', command=show_data)
submit_filter.pack(side=LEFT, padx=10, ipady=2)


# Create plain table
def crate_plain_table():
    for r in range(max(see_data)):
        for col in range(len(table_title)):
            Label(root, text="", bg='light salmon').grid(sticky="news", row=r + 7, column=col, padx=1)
crate_plain_table()

root.mainloop()
