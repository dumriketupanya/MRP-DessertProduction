"""
Filename: getData.py
Description: This script serves as the central mechanism for downloading files and loading data into the system.
Author: Dumri Ketupanya
Date created: June 8, 2020
"""

# import required modules =========================================================================
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk  # ttk -> themed tk (for Combobox)
import time, datetime
import math
import sys

# SQLite Database Connection ======================================================================
bom_data_list = []
def select_bom_data():
    try:
        bom_data_list.clear()
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Ingredient_data
            """
            for row in con.execute(sql_cmd):
                bom_data_list.append(row)
    except Exception as e:
        print("Error -> {}".format(e))

def get_ingredient():
    make_sure = messagebox.askokcancel('Create file',"Creating a new file overwrite the old file in the same folder.")
    if make_sure == True:
        select_bom_data()
        print(bom_data_list)
        file_bom_obj = open('ingredient_data.txt', 'w', encoding='utf-8')
        for i in range(len(bom_data_list)):
            file_bom_obj.write(f'{bom_data_list[i]}\n')
    else:
        pass

order_record_list = []
def select_order_record():
    try:
        order_record_list.clear()
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Order_Records
            """
            for row in con.execute(sql_cmd):
                order_record_list.append(row)
    except Exception as e:
        print("Error -> {}".format(e))

def get_order_record():
    make_sure = messagebox.askokcancel('Create file',"Creating a new file overwrite the old file in the same folder.")
    if make_sure == True:
        select_order_record()
        print(order_record_list)
        file_bom_obj = open('order_record_data.txt', 'w', encoding='utf-8')
        for i in range(len(order_record_list)):
            file_bom_obj.write(f'{order_record_list[i]}\n')
    else:
        pass

production_lst = []
def select_production():
    try:
        production_lst.clear()
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Production_plan
            """
            for row in con.execute(sql_cmd):
                production_lst.append(row)
    except Exception as e:
        print("Error -> {}".format(e))

def get_production_plan():
    make_sure = messagebox.askokcancel('Create file',"Creating a new file overwrite the old file in the same folder.")
    if make_sure == True:
        select_production()
        print(production_lst)
        file_bom_obj = open('Production_plan_data.txt', 'w', encoding='utf-8')
        for i in range(len(production_lst)):
            file_bom_obj.write(f'{production_lst[i]}\n')
    else:
        pass

purchase_lst = []
def select_purchase_record():
    try:
        purchase_lst.clear()
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            SELECT * FROM PurchasedRecord
            """
            for row in con.execute(sql_cmd):
                purchase_lst.append(row)
    except Exception as e:
        print("Error -> {}".format(e))

def get_purchase_records():
    make_sure = messagebox.askokcancel('Create file',"Creating a new file overwrite the old file in the same folder.")
    if make_sure == True:
        select_purchase_record()
        print(purchase_lst)
        file_bom_obj = open('Purchase_records_data.txt', 'w', encoding='utf-8')
        for i in range(len(purchase_lst)):
            file_bom_obj.write(f'{purchase_lst[i]}\n')
    else:
        pass

inventory_lst = []
def select_inventory():
    try:
        inventory_lst.clear()
        with sqlite3.connect("Inventory_Management.sqlite") as con:
            sql_cmd = """
            SELECT * FROM InventoryManagement
            """
            for row in con.execute(sql_cmd):
                inventory_lst.append(row)
    except Exception as e:
        print("Error -> {}".format(e))

def get_inventory():
    make_sure = messagebox.askokcancel('Create file',"Creating a new file overwrite the old file in the same folder.")
    if make_sure == True:
        select_inventory()
        print(inventory_lst)
        file_bom_obj = open('Inventory_management_data.txt', 'w', encoding='utf-8')
        for i in range(len(inventory_lst)):
            file_bom_obj.write(f'{inventory_lst[i]}\n')
    else:
        pass


# User Interface Section =======================================================================================
root = Tk()
root.title("Export data")
root.option_add("*Font", "arial 15")

# Title
Title_frame = Frame(root, bg='gold')
Title_frame.grid(row=0, column=0, columnspan=9, sticky='news')
Title_Label = Label(Title_frame, text="Get data files")
Title_Label.pack(padx=40, pady=10, side=TOP)

# data
data_get_frame = Frame(root, bg='orange')
data_get_frame.grid(row=1, column=0, columnspan=9, sticky='news')

# button get data
Button(data_get_frame, text='BOM (Ingredient data)',command=get_ingredient).pack(fill=X,padx=5,pady=5)
Button(data_get_frame, text='Order records',command=get_order_record).pack(fill=X,padx=5,pady=5)
Button(data_get_frame, text='Production plan',command=get_production_plan).pack(fill=X,padx=5,pady=5)
Button(data_get_frame, text='Purchase records',command=get_purchase_records).pack(fill=X,padx=5,pady=5)
Button(data_get_frame, text='Inventory management',command=get_inventory).pack(fill=X,padx=5,pady=5)


root.mainloop()