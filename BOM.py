"""
Filename: BOM.py
Description: This script performs as a Bill of Materials (BOM). Which is a comprehensive list of raw ingredients for production.
Author: Dumri Ketupanya
Date created: June 8, 2020
"""

# import required modules =========================================================================
from tkinter import *
import sqlite3
from tkinter import messagebox

# SQLite Database Connection ======================================================================
def Create_Data_Table():
    try:
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = """
            create table Ingredient_data(
            Serial_Number text primary key,Name text,BOM_Qty real,
            Purchased_Unit real,Quantity_per_Unit real,Edit_Q real, 
            Unit real,Cost_Baht real,Edit_cost real);
            """
            con.execute(sql_cmd)
    except Exception as e:
        print("Error -> {}".format(e))


def Create_Fill_Data_Table():
    try:
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd1 = """
            create table Fill(
            num text primary key,Custard_Filling real,Caramel_Filling real,
            Unit_per_Batch real);
            """
            con.execute(sql_cmd1)
    except Exception as e:
        print("Error -> {}".format(e))


# DATASET of Ingredients & Materials
# User can edit : 'Quantity_per_Unit','Cost_Baht'
# Only admin can edit: 'Serial_Number','Name','BOM QTy.','Purchased_Unit','Unit'

Data_list = []

def Select_Data():
    try:
        Data_list.clear()
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Ingredient_data
            """
            for row in con.execute(sql_cmd):
                Data_list.append(row)
    except Exception as e:
        print("Error -> {}".format(e))

Data_fill_list = []

def Select_fill_Data():
    try:
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = '''
            SELECT * FROM Fill
            '''
            for row in con.execute(sql_cmd):
                Data_fill_list.append(row)
                # print(row)
    except Exception as e:
        print("Error -> {}".format(e))


Create_Data_Table()
Create_Fill_Data_Table()
Select_Data()
Select_fill_Data()

# User Interface and Program Logic Section ======================================================================
root = Tk()
root.title("Bill of materials")
root.option_add("*Font", "arial 11")

# Submit command
# Require to restart after submit to update the database yet.
def click_submit():
    ReadQ_data()
    Read_Cost_data()
    print(Lst_Q_per_Unit)
    print(Lst_Cost)
    global Fill_Custard_set, Fill_Custard_set, Unit_per_batch
    Unit_per_batch = convert_pb.get()
    Fill_Custard_set = convert_custard.get()
    Fill_Caramel_set = convert_caramel.get()
    with sqlite3.connect("Ingredient_data.sqlite") as con:
        for i in range(len(Lst_Q_per_Unit)):
            if Lst_Q_per_Unit[i] != 0:
                con.execute(f"""UPDATE Ingredient_data SET Quantity_per_Unit = {Lst_Q_per_Unit[i]}
                    WHERE Serial_Number = {Data_list[i][0]}""")
    with sqlite3.connect("Ingredient_data.sqlite") as con:
        for i in range(len(Lst_Cost)):
            if Lst_Cost[i] != 0:
                con.execute(f"""UPDATE Ingredient_data SET Cost_Baht = {Lst_Cost[i]}
                    WHERE Serial_Number = {Data_list[i][0]}""")
    with sqlite3.connect("Ingredient_data.sqlite") as con:
        if Fill_Custard_set != 0:
            sql_cmd1 = f"""UPDATE Fill SET Custard_Filling = {Fill_Custard_set} WHERE num = '1'"""
            custard_filling.set(f'Custard ({Fill_Custard_set})')
            con.execute(sql_cmd1)  #####
        if Fill_Caramel_set != 0:
            sql_cmd2 = f"""UPDATE Fill SET Caramel_Filling = {Fill_Caramel_set} WHERE num = '1'"""
            caramel_filling.set(f'Caramel ({Fill_Caramel_set})')
            con.execute(sql_cmd2)  #####
        if Unit_per_batch != 0:
            sql_cmd3 = f"""UPDATE Fill SET Unit_per_Batch = {Unit_per_batch} WHERE num = '1'"""
            Per_batch.set(f'Unit per batch ({Unit_per_batch})')
            con.execute(sql_cmd3)  #####
    Select_fill_Data()
    del Data_fill_list[0]
    Select_Data()
    del Data_list[0:len(Dict_data)]
    Dict_Edit_Data()
    Data_Table()
    print(Dict_data)
    print(Fill_Custard_set, Fill_Caramel_set, Unit_per_batch)


# Title
Title_frame = Frame(root, bg='gold')
Title_frame.grid(row=0, column=0, columnspan=9, sticky='news')
Title_Label = Label(Title_frame, text="Pudding ingredients & Materials")
Title_Label.pack(padx=40, pady=10, side=LEFT)

convert_pb = DoubleVar()
convert_custard = DoubleVar()
convert_caramel = DoubleVar()
filling = DoubleVar()
custard_filling = DoubleVar()
caramel_filling = DoubleVar()

# Filling quantity
label_grid = Frame(root, bg='lemon chiffon')
label_grid.grid(row=1, column=0, columnspan=9, sticky='news')
Label(label_grid, textvariable=filling, bg='OliveDrab2').grid(row=1, column=0, columnspan=2, sticky='news')
filling.set('filling quantity per cup (ml.)')
Label(label_grid, textvariable=custard_filling, bg='green yellow').grid(row=2, column=0, sticky=W)
custard_filling.set(f'Custard ({Data_fill_list[0][1]})')
Label(label_grid, textvariable=caramel_filling, bg='green yellow').grid(row=3, column=0, sticky=W)
caramel_filling.set(f'Caramel ({Data_fill_list[0][2]})')
Ent_custard_fill = Entry(label_grid, textvariable=convert_custard, width=8).grid(row=2, column=1, sticky=W)
Ent_caramel_fill = Entry(label_grid, textvariable=convert_caramel, width=8).grid(row=3, column=1, sticky=W)

# Submit Button
Button(label_grid, text="save", bg='orchid2', command=click_submit).grid(row=2, column=5, sticky='news', padx=10)

def add_new_material():
    root_add = Tk()
    root_add.title("Add materials")
    root_add.option_add("*Font", "arial 11")
    # Title
    Data_title_add = ['Serial number', 'Name', 'BOM quantity', 'Purchased unit', 'Quantity per unit'
    , 'Unit', 'Cost (Baht)']
    for i, a in enumerate(Data_title_add):
        Label(root_add, text=a, bg='RoyalBlue1').grid(sticky="news", row=0, column=(i), padx=1)
    # Fill data
    add_data_lst = []
    for i in range(len(Data_title_add)):
        en_add = Entry(root_add, textvariable=DoubleVar(), width=15)
        en_add.grid(sticky="news", row=1, column=i, padx=1)
        add_data_lst.append(en_add)
    print(add_data_lst)

    def add_new_mat():
        add_lst = []
        for entry in add_data_lst:
            add_lst.append(entry.get())
        Select_Data()
        print(add_lst)
        # print(Data_list)
        serial_check = []
        for i in range(len(Data_list)):
            serial_check.append(Data_list[i][0])
        print(serial_check)
        check_num = [add_lst[1], add_lst[3], add_lst[5]]
        try:
            with sqlite3.connect("Ingredient_data.sqlite") as con:
                a = 0
                for i in serial_check:
                    if i == add_lst[0]:
                        messagebox.showerror('Data error!', 'Duplicate serial number!')
                        a = 1
                if a == 1:
                    pass
                elif add_lst[0] == '' or add_lst[1] == '' or add_lst[2] == '' or add_lst[3] == '' or add_lst[4] == '' or\
                    add_lst[5] == '' or add_lst[6] == '':
                    messagebox.showerror('Data missing!', 'Data missing!')
                    pass
                else:
                    try:
                        with sqlite3.connect("Ingredient_data.sqlite") as con:
                            sql_cmd = f"""
                                INSERT into Ingredient_data values ('{add_lst[0]}','{add_lst[1]}',{float(add_lst[2])},
                                '{add_lst[3]}', {float(add_lst[4])},'','{add_lst[5]}',{float(add_lst[6])}, '')"""
                            print(sql_cmd)
                            con.execute(sql_cmd)
                            messagebox.showinfo("Success!","Data added successfully!")
                    except Exception as e:
                        messagebox.showerror('Data error!', '{}'.format(e))
        except Exception as e:
            print("Error -> {}".format(e))

    # Approved button
    approve_but = Button(root_add, text="add", bg='plum2', width=10, command=add_new_mat)
    approve_but.grid(sticky="news", row=1, column=len(Data_title_add), padx=1)
    root_add.mainloop()

# Add Button
Button(label_grid, text="add new material", bg='plum2', command=add_new_material).grid(row=2, column=6,
                                                                                       sticky='news', padx=10)

def delete_material():
    root_search = Tk()
    root_search.title("Delete materials")
    root_search.option_add("*Font", "arial 11")
    # Title
    Data_title_add = ['Serial number', 'Name', 'BOM quantity', 'Purchased unit', 'Quantity per unit'
    , 'Unit', 'Cost (Baht)']
    for i, a in enumerate(Data_title_add):
        Label(root_search, text=a, bg='RoyalBlue1',width=15).grid(sticky="news", row=0, column=(i), padx=1)

    en_serial = Entry(root_search, textvariable=DoubleVar(), width=15)
    en_serial.grid(sticky="news", row=1, column=0, padx=1)

    data_search_lst = []
    def select_Data():
        try:
            data_search_lst.clear()
            with sqlite3.connect("Ingredient_data.sqlite") as con:
                sql_cmd = """
                SELECT * FROM Ingredient_data
                """
                for row in con.execute(sql_cmd):
                    data_search_lst.append(list(row))
        except Exception as e:
            print("Error -> {}".format(e))

    def search_data():
        select_Data()
        print(data_search_lst)
        serial = en_serial.get()
        data_print = []
        for i in range(len(data_search_lst)):
            if data_search_lst[i][0] == serial:
                data_print = data_search_lst[i]
        print(data_print)
        try:
            del data_print[5]
            del data_print[-1]
            del data_print[0]
            for i, a in enumerate(data_print):
                Label(root_search, text=a, bg='light cyan', width=15).grid(sticky="news", row=1, column=i+1, padx=1)
        except Exception as e:
            messagebox.showerror("error!","Serial number not found!!")

    def delete_data():
        try:
            with sqlite3.connect("Ingredient_data.sqlite") as con:
                sql_cmd = f"""
                      DELETE FROM Ingredient_data WHERE Serial_Number = {en_serial.get()}
                  """
                con.execute(sql_cmd)
                messagebox.showinfo("Delete", "Data delete successfully!")
        except Exception as e:
            print("Error -> {}".format(e))


    # search button
    serial_select = Button(root_search, text="search", bg='plum2', width=10, command=search_data)
    serial_select.grid(sticky="news", row=2, column=0, padx=1)

    # Delete button
    delete_but = Button(root_search, text="delete", bg='plum2', width=10, command=delete_data)
    delete_but.grid(sticky="news", row=2, column=len(Data_title_add)-1, padx=1)
    root_search.mainloop()


# delete Button
Button(label_grid, text="delete material", bg='plum1', command=delete_material).grid(row=2, column=7,
                                                                                       sticky='news', padx=10)

Per_batch = DoubleVar()
# Unit per batch
Label(label_grid, textvariable=Per_batch, bg='green yellow').grid(row=2, column=2, sticky=W)
Per_batch.set(f'Unit per batch ({Data_fill_list[0][3]})')
Ent_per_batch = Entry(label_grid, textvariable=convert_pb, width=8).grid(row=2, column=3, sticky=W)

# Title Data
Data_title = ['Serial number', 'Name', 'BOM quantity', 'Purchased unit', 'Quantity per unit', 'Edit quantity'
    , 'Unit', 'Cost (Baht)', 'Edit (Cost)']
for i, a in enumerate(Data_title):
    Label(root, text=a, bg='RoyalBlue1').grid(sticky="news", row=4, column=(i), padx=1)

# Create Dictionary
Dict_data = {}
Dict_data_title = {}


def Dict_Edit_Data_Title():
    for number1, name1 in enumerate(Data_title):
        Dict_data_title[number1] = name1
        # print(Dict_data_title)


def Dict_Edit_Data():
    for number2, name2 in enumerate(Data_list):
        Dict_data[number2] = name2
        # print(Dict_data)


Dict_Edit_Data()
Dict_Edit_Data_Title()


# Data Table
# Read Only
def Data_Table():
    for food in range(len(Dict_data)):
        for food_data in range(len(Dict_data_title)):
            if food_data == 5:
                pass
            elif food_data == 8:
                pass
            else:
                Label(root, text=Dict_data[food][food_data], bg='light cyan').grid(sticky="news", row=food + 5,
                                                                                   column=food_data, padx=1)


Data_Table()

# Edit table
Lst_Q = []
Lst_Q_per_Unit = []
def Q_per_Unit():
    for i in range(len(Dict_data)):
        en = Entry(root, textvariable=DoubleVar(), width=15)
        en.grid(row=i + 5, column=5, padx=0)
        Lst_Q.append(en)
Q_per_Unit()
# print(Lst_Q)

def Read_iniQ_data():
    for entry in Lst_Q:
        Lst_Q_per_Unit.append(float(entry.get()))
    # print(Lst_Q_per_Unit)
Read_iniQ_data()

def ReadQ_data():
    for entry in Lst_Q:
        Lst_Q_per_Unit.append(float(entry.get()))
    del Lst_Q_per_Unit[0:len(Dict_data)]
    # print(Lst_Q_per_Unit)
ReadQ_data()

Lst_C = []
Lst_Cost = []


def Cost():
    for i in range(len(Dict_data)):
        en = Entry(root, textvariable=DoubleVar(), width=15)
        en.grid(row=i + 5, column=8, padx=0)
        Lst_C.append(en)
Cost()

def Read_ini_Cost_data():
    for entry in Lst_C:
        Lst_Cost.append(float(entry.get()))
    # print(Lst_Cost)
Read_ini_Cost_data()


def Read_Cost_data():
    for entry in Lst_C:
        Lst_Cost.append(float(entry.get()))
    del Lst_Cost[0:len(Dict_data)]
    # print(Lst_Cost)
Read_Cost_data()

root.mainloop()
