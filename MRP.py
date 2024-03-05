"""
Filename: MRP.py
Description: This script functions as a Material Requirement Planning (MRP) tool,
designed to facilitate and control the procurement process in alignment with the Just-in-Time (JIT) Manufacturing principle.
Author: Dumri Ketupanya
Date created: June 8, 2020
"""

############ MRP Not allowed to use when MPS not updated. ##################
# import required modules =====================================================================================
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk 
import time, datetime
import math

# SQLite Database Connection ===================================================================================
data_invent_list= []
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

bom_data_lst = []
def Select_Data():
    try:
        bom_data_lst.clear()
        with sqlite3.connect("Ingredient_data.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Ingredient_data
            """
            for row in con.execute(sql_cmd):
                bom_data_lst.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))

# Unit per batch
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
    except Exception as e :
        print("Error -> {}".format(e))

production_plan_lst = []
def select_production_data():
    try:
        production_plan_lst.clear()
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Production_Plan
            """
            for row in con.execute(sql_cmd):
                production_plan_lst.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))

# User Interface and Program Logic Section ====================================================================================
root = Tk()
root.title("Material Requirement Plan")
root.option_add("*Font", "arial 11")

# Title
Title_frame = Frame(root, bg='SteelBlue1')
Title_frame.grid(row=0, column=0, columnspan=10, sticky='news')
Title_Label = Label(Title_frame, text="Material Requirement Plan")
Title_Label.pack(padx=10, pady=10, side=LEFT)

# Overall title
col_num = 9
header_width = 17
overview_frame = Frame(root, bg='LightSkyBlue1')
overview_frame.grid(row=1, column=0, columnspan=10, sticky='news')
overview_1 = ["Production status", "Pudding available now", "Total Budget required", "Select latest"]
for e, i in enumerate(overview_1):
    Label(overview_frame, text=i, width=header_width, bg="green yellow").grid(row=1, column=e, padx=1, sticky='news')

req_ingre = []
diff_ava_ingre = []
# Overall data
def pudding_available():
    # data from bom
    global req_ingre
    req_ingre = []
    Select_Data()
    for i in range(len(bom_data_lst)):
        req_ingre.append([bom_data_lst[i][1], bom_data_lst[i][2]])
    # get from inventory check expired
    select_invent_data()
    for i in range(len(data_invent_list)):
        start_struc = time.strptime(data_invent_list[i][7], '%Y-%m-%d')
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        data_invent_list[i].append(pubdate)
    current_date = datetime.date.today()
    for i in range(len(data_invent_list)):
        if data_invent_list[i][8] <= current_date:
            data_invent_list[i].append("Expired")
        else:
            data_invent_list[i].append("Available")
    # rearrange inventory data
    remain_mat = []
    for i in range(len(data_invent_list)):
        remain_mat.append([data_invent_list[i][1], data_invent_list[i][3], data_invent_list[i][9]])
    # get only available ingredients
    available_remain_mat = []
    for i in range(len(remain_mat)):
        if remain_mat[i][-1] == 'Available':
            available_remain_mat.append([remain_mat[i][0], remain_mat[i][1]])

    global diff_ava_ingre
    diff_ava_ingre = [] # sum difference ingredients units
    check_ava_lst = []
    for i in range(len(req_ingre)):
        prep = []
        prep_unit_ava = []
        for t in range(len(available_remain_mat)):
            if req_ingre[i][0] == available_remain_mat[t][0]:
                prep_unit_ava.append(available_remain_mat[t][1]) # add to sum difference ingredients units
                check_ava = math.ceil(available_remain_mat[t][1]/req_ingre[i][1]) # to check available puddings
                prep.append(check_ava)
        sum_ingre = sum(prep)
        check_ava_lst.append(sum_ingre)
        diff_ava_ingre.append([req_ingre[i][0], sum(prep_unit_ava)])
    
    # Check minimum constrain
    maximum_produce = []
    maximum_produce = min(check_ava_lst)
    c_maximum_produce_b = math.ceil(maximum_produce)
    Select_fill_Data()
    global c_maximum_produce_unit
    c_maximum_produce_unit = c_maximum_produce_b*float(unit_per_batch[0])
    Label(root, text=c_maximum_produce_unit, bg="yellow", width=header_width).grid(row=2, padx=1, column=1, sticky='news')
pudding_available()

# check status
def check_status():
    if c_maximum_produce_unit <= 0:
        Label(root, text="Unavailable", bg="red", width=header_width).grid(row=2, padx=1, column=0, sticky='news')
    else:
        Label(root, text="Available", bg="lawn green", width=header_width).grid(row=2, padx=1, column=0, sticky='news')
check_status()

#bud req
set_start_col = 2
bud_req = Label(root, text="", width=header_width, bg="yellow")
bud_req.grid(row=2, padx=1, sticky='news', column=set_start_col)

# split product
def spilt_str_produce(string):
    a, b = string.split(", ")
    z, produce_n = a.split("(")
    surplus_n, q = b.split(")")
    return produce_n, surplus_n

# data table
# Title
Title_frame2 = Frame(root, bg='SteelBlue1')
Title_frame2.grid(row=3, column=0, columnspan=10, sticky='news')
Title_Label = Label(Title_frame2, text="Material Required")
Title_Label.pack(padx=10, pady=10, side=LEFT)

# subtitle
table_width = 13
Subtitle_req = ["Serial NO.", "Name", "Material available", "Total required","Surplus", "Unit", "Purchase needed", "Unit",
                "Budget required"]
for e, i in enumerate(Subtitle_req):
    Label(root, text=i, bg="gold2", width=table_width).grid(row=5, column=e, sticky='news')

# plain data
def plain_data():
    Select_Data()
    for row in range(len(bom_data_lst)):
        for col in range(len(Subtitle_req)):
            Label(root, text='', bg='light salmon').grid(sticky="news", row=row + 6, column=col, padx=1)
plain_data()

# data table
def create_data_today():
    Select_Data()
    # print(bom_data_lst) # ingredients
    select_production_data()
    # print(production_plan_lst) # MPS
    Select_fill_Data()
    # print(unit_per_batch[0]) # Unit per batch
    select_invent_data()
    # print(data_invent_list)

    # Find material available in current range # same number in every date ranges
    pudding_available()

    # get waiting range     # select current date
    current_date = datetime.date.today() ############
    for i in range(len(production_plan_lst)):
        start_struc = time.strptime(production_plan_lst[i][0], '%Y-%m-%d %H:%M:%S') # convert duetime
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        production_plan_lst[i].append(pubdate)
    # print(production_plan_lst)
    # print(current_date)
    # find AND waiting required materials.
    production_select = []
    for i in range(len(production_plan_lst)):
        if production_plan_lst[i][-1] == current_date:
            if production_plan_lst[i][6] == 'Waiting':
                production_select.append(production_plan_lst[i])
    print(production_select)
    # get production batch number # arrangement
    product_arrangement = []
    for i in range(len(production_select)):
        produce_n, surplus_n = spilt_str_produce(production_select[i][3])
        product_arrangement.append(int(produce_n))
    # print(product_arrangement)
    req_batch_material = sum(product_arrangement)
    # print(req_batch_material)

    # find total required per ingredients
    # bom material # use pudding available function
    for i in range(len(req_ingre)):
        req_ingre[i][1] = round(req_ingre[i][1]*req_batch_material,5) #  round-off error (5 decimal place)

    # find surplus #change diff available ingredients to surplus
    surplus_lst = []
    for i in range(len(req_ingre)):
        sup_num = round(diff_ava_ingre[i][1]-req_ingre[i][1],5) #  round-off error (5 decimal place)
        name_mat = diff_ava_ingre[i][0]
        surplus_lst.append([name_mat, sup_num])

    #find purchase needed
    # print(bom_data_lst)
    purchase_qty = []
    purchase_needed = []
    for i in range(len(bom_data_lst)):
        purchase_qty.append([bom_data_lst[i][1], bom_data_lst[i][4], bom_data_lst[i][7]])
    # print(purchase_qty)
    for i in range(len(surplus_lst)):
        if surplus_lst[i][1] < 0:
            purchase_needed.append(surplus_lst[i])
    # print(purchase_needed)
    purchase_needed_ans = []
    for i in range(len(purchase_needed)):
        for t in range(len(purchase_qty)):
            if purchase_needed[i][0] == purchase_qty[t][0]:
                prod_name = purchase_needed[i][0]
                buy_qty = math.ceil(abs(purchase_needed[i][1])/purchase_qty[t][1])
                budget_needed = buy_qty*purchase_qty[t][2]
                purchase_needed_ans.append([prod_name, buy_qty, budget_needed])

    # print(diff_ava_ingre) # Material available #add [2]:Material avail.
    # print(req_ingre) #purchase and budget needed #add [3]: Total req.
    # print(surplus_lst) #surplus # add [4]:surplus
    # print(purchase_needed_ans) # total required materials #add [6]: Purchase needed, [8] Budget needed

    #  print(bom_data_lst) #keep [0]:serial, [1]:Name, [3]:purchase unit, [6]:ind. unit # add [0],[1],[7],[5]
    # create data to show
    data_show = []
    total_budget_lst = [] # find total budget spend needed
    for i in range(len(bom_data_lst)):
        data_set = []
        seq_0, seq_1 = bom_data_lst[i][0], bom_data_lst[i][1]
        seq_2 = diff_ava_ingre[i][1]
        seq_3 = req_ingre[i][1]
        seq_4 = surplus_lst[i][1]
        seq_5 = bom_data_lst[i][6]
        seq_6 = 0
        seq_8 = 0
        for t in range(len(purchase_needed_ans)):
            if seq_1 == purchase_needed_ans[t][0]:
                seq_6 = purchase_needed_ans[t][1]
                seq_8 = purchase_needed_ans[t][2]
                total_budget_lst.append(seq_8)
                break
            else:
                seq_6 = 0
                seq_8 = 0
        seq_7 = bom_data_lst[i][3]
        data_set.append([seq_0, seq_1, seq_2, seq_3, seq_4, seq_5, seq_6,seq_7, seq_8])
        data_show.append(data_set)
    # print(data_show)
    for row in range(len(data_show)):
        for col in range(len(Subtitle_req)):
            Label(root, text=data_show[row][0][col], bg='light salmon').grid(sticky="news", row=row + 6, column=col, padx=1)
    # surplus show alert
    for row in range(len(data_show)):
        if data_show[row][0][4] < 0:
            Label(root, text=data_show[row][0][4], bg='red').grid(sticky="news", row=row + 6, column=4, padx=1)
        else:
            Label(root, text=data_show[row][0][4], bg='lawn green').grid(sticky="news", row=row + 6, column=4, padx=1)
    # show total budget
    total_budget = sum(total_budget_lst)
    Label(root, text=total_budget, bg='yellow').grid(sticky="news", row=2, column=2, padx=1)


show_data_lst = []
def create_data_select():
    Select_Data()
    # print(bom_data_lst) # ingredients
    select_production_data()
    # print(production_plan_lst) # MPS
    Select_fill_Data()
    # print(unit_per_batch[0]) # Unit per batch
    select_invent_data()
    # print(data_invent_list)

    # Find material available in current range # same number in every date ranges
    pudding_available()

    # get waiting range
    # select current date
    get_date = range_date_cbo.get()
    bench_filday = datetime.timedelta(days=0)
    filday = datetime.timedelta(days=0)
    if get_date == "Today":
        filday = datetime.timedelta(days=0)
    elif get_date == "Last 3 days":
        filday = datetime.timedelta(days=-3)
    elif get_date == "Last 7 days":
        filday = datetime.timedelta(days=-7)
    elif get_date == "Next 3 days":
        filday = datetime.timedelta(days=3)
    elif get_date == "Next 7 days":
        filday = datetime.timedelta(days=7)
    plain_data()
    for i in range(len(production_plan_lst)):
        start_struc = time.strptime(production_plan_lst[i][0], '%Y-%m-%d %H:%M:%S') # convert duetime
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        production_plan_lst[i].append(pubdate)
        # print(data_table_lst[0][-1]-current_date) # Last ### days -
        # print(data_table_lst[-1][-1]-current_date) # Next ### days +
    current_date = datetime.date.today()
    global  show_data_lst
    show_data_lst = []
    for i in range(len(production_plan_lst)):
        if (production_plan_lst[i][-1]-current_date) >= filday and (production_plan_lst[i][-1]-current_date) <= bench_filday:
            show_data_lst.append(production_plan_lst[i])
        if (production_plan_lst[i][-1]-current_date) <= filday and (production_plan_lst[i][-1]-current_date) >= bench_filday:
            show_data_lst.append(production_plan_lst[i])
    for i in range(len(production_plan_lst)):
        del production_plan_lst[i][-1]

    # find and waiting required materials
    production_select = []
    for i in range(len(show_data_lst)):
        if production_plan_lst[i][6] == 'Waiting':
            production_select.append(production_plan_lst[i])
    
    # get production batch number # arrangement
    product_arrangement = []
    for i in range(len(production_select)):
        produce_n, surplus_n = spilt_str_produce(production_select[i][3])
        product_arrangement.append(int(produce_n))
    req_batch_material = sum(product_arrangement)

    # find total required per ingredients
    # bom material # use pudding available function
    for i in range(len(req_ingre)):
        req_ingre[i][1] = round(req_ingre[i][1]*req_batch_material,5) # round-off error (5 decimal place)

    # find surplus #change diff available ingredients to surplus
    surplus_lst = []
    for i in range(len(req_ingre)):
        sup_num = round(diff_ava_ingre[i][1]-req_ingre[i][1],5) # round-off error (5 decimal place)
        name_mat = diff_ava_ingre[i][0]
        surplus_lst.append([name_mat, sup_num])

    #find purchase needed
    purchase_qty = []
    purchase_needed = []
    for i in range(len(bom_data_lst)):
        purchase_qty.append([bom_data_lst[i][1], bom_data_lst[i][4], bom_data_lst[i][7]])
    
    for i in range(len(surplus_lst)):
        if surplus_lst[i][1] < 0:
            purchase_needed.append(surplus_lst[i])
    
    purchase_needed_ans = []
    for i in range(len(purchase_needed)):
        for t in range(len(purchase_qty)):
            if purchase_needed[i][0] == purchase_qty[t][0]:
                prod_name = purchase_needed[i][0]
                buy_qty = math.ceil(abs(purchase_needed[i][1])/purchase_qty[t][1])
                budget_needed = buy_qty*purchase_qty[t][2]
                purchase_needed_ans.append([prod_name, buy_qty, budget_needed])

    # print(diff_ava_ingre) # Material available #add [2]:Material avail.
    # print(req_ingre) #purchase and budget needed #add [3]: Total req.
    # print(surplus_lst) #surplus # add [4]:surplus
    # print(purchase_needed_ans) # total required materials #add [6]: Purchase needed, [8] Budget needed

    #  print(bom_data_lst) #keep [0]:serial, [1]:Name, [3]:purchase unit, [6]:ind. unit # add [0],[1],[7],[5]
    # create data to show
    total_budget_lst = [] # find total budget spend needed
    data_show = []
    for i in range(len(bom_data_lst)):
        data_set = []
        seq_0, seq_1 = bom_data_lst[i][0], bom_data_lst[i][1]
        seq_2 = diff_ava_ingre[i][1]
        seq_3 = req_ingre[i][1]
        seq_4 = surplus_lst[i][1]
        seq_5 = bom_data_lst[i][6]
        seq_6 = 0
        seq_8 = 0
        for t in range(len(purchase_needed_ans)):
            if seq_1 == purchase_needed_ans[t][0]:
                seq_6 = purchase_needed_ans[t][1]
                seq_8 = purchase_needed_ans[t][2]
                total_budget_lst.append(seq_8)
                break
            else:
                seq_6 = 0
                seq_8 = 0
        seq_7 = bom_data_lst[i][3]
        data_set.append([seq_0, seq_1, seq_2, seq_3, seq_4, seq_5, seq_6,seq_7, seq_8])
        data_show.append(data_set)
    # print(data_show)
    for row in range(len(data_show)):
        for col in range(len(Subtitle_req)):
            Label(root, text=data_show[row][0][col], bg='light salmon').grid(sticky="news", row=row + 6, column=col, padx=1)
    # surplus show alert
    for row in range(len(data_show)):
        if data_show[row][0][4] < 0:
            Label(root, text=data_show[row][0][4], bg='red').grid(sticky="news", row=row + 6, column=4, padx=1)
        else:
            Label(root, text=data_show[row][0][4], bg='lawn green').grid(sticky="news", row=row + 6, column=4, padx=1)
    # show total budget
    total_budget = sum(total_budget_lst)
    Label(root, text=total_budget, bg='yellow').grid(sticky="news", row=2, column=2, padx=1)


def create_data_total():
    Select_Data()
    # print(bom_data_lst) # ingredients
    select_production_data()
    # print(production_plan_lst) # MPS
    Select_fill_Data()
    # print(unit_per_batch[0]) # Unit per batch
    select_invent_data()
    # print(data_invent_list)

    # Find material available in current range # same number in every date ranges
    pudding_available()

    # get waiting range     # select current date
    current_date = datetime.date.today() 
    for i in range(len(production_plan_lst)):
        start_struc = time.strptime(production_plan_lst[i][0], '%Y-%m-%d %H:%M:%S') # convert duetime
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        production_plan_lst[i].append(pubdate)

    # find and waiting required materials.
    production_select = []
    for i in range(len(production_plan_lst)):
        if production_plan_lst[i][6] == 'Waiting':
            production_select.append(production_plan_lst[i])
    print(production_select)
    # get production batch number # arrangement
    product_arrangement = []
    for i in range(len(production_select)):
        produce_n, surplus_n = spilt_str_produce(production_select[i][3])
        product_arrangement.append(int(produce_n))
    # print(product_arrangement)
    req_batch_material = sum(product_arrangement)
    # print(req_batch_material)

    # find total required per ingredients
    # bom material # use pudding available function
    for i in range(len(req_ingre)):
        req_ingre[i][1] = round(req_ingre[i][1]*req_batch_material,5) #  round-off error (5 decimal place)

    # find surplus #change diff available ingredients to surplus
    surplus_lst = []
    for i in range(len(req_ingre)):
        sup_num = round(diff_ava_ingre[i][1]-req_ingre[i][1],5) #  round-off error (5 decimal place)
        name_mat = diff_ava_ingre[i][0]
        surplus_lst.append([name_mat, sup_num])

    #find purchase needed
    # print(bom_data_lst)
    purchase_qty = []
    purchase_needed = []
    for i in range(len(bom_data_lst)):
        purchase_qty.append([bom_data_lst[i][1], bom_data_lst[i][4], bom_data_lst[i][7]])
    # print(purchase_qty)
    for i in range(len(surplus_lst)):
        if surplus_lst[i][1] < 0:
            purchase_needed.append(surplus_lst[i])
    # print(purchase_needed)
    purchase_needed_ans = []
    for i in range(len(purchase_needed)):
        for t in range(len(purchase_qty)):
            if purchase_needed[i][0] == purchase_qty[t][0]:
                prod_name = purchase_needed[i][0]
                buy_qty = math.ceil(abs(purchase_needed[i][1])/purchase_qty[t][1])
                budget_needed = buy_qty*purchase_qty[t][2]
                purchase_needed_ans.append([prod_name, buy_qty, budget_needed])

    # print(diff_ava_ingre) # Material available #add [2]:Material avail.
    # print(req_ingre) #purchase and budget needed #add [3]: Total req.
    # print(surplus_lst) #surplus # add [4]:surplus
    # print(purchase_needed_ans) # total required materials #add [6]: Purchase needed, [8] Budget needed

    #  print(bom_data_lst) #keep [0]:serial, [1]:Name, [3]:purchase unit, [6]:ind. unit # add [0],[1],[7],[5]
    # create data to show
    data_show = []
    total_budget_lst = [] # find total budget spend needed
    for i in range(len(bom_data_lst)):
        data_set = []
        seq_0, seq_1 = bom_data_lst[i][0], bom_data_lst[i][1]
        seq_2 = diff_ava_ingre[i][1]
        seq_3 = req_ingre[i][1]
        seq_4 = surplus_lst[i][1]
        seq_5 = bom_data_lst[i][6]
        seq_6 = 0
        seq_8 = 0
        for t in range(len(purchase_needed_ans)):
            if seq_1 == purchase_needed_ans[t][0]:
                seq_6 = purchase_needed_ans[t][1]
                seq_8 = purchase_needed_ans[t][2]
                total_budget_lst.append(seq_8)
                break
            else:
                seq_6 = 0
                seq_8 = 0
        seq_7 = bom_data_lst[i][3]
        data_set.append([seq_0, seq_1, seq_2, seq_3, seq_4, seq_5, seq_6,seq_7, seq_8])
        data_show.append(data_set)
    # print(data_show)
    for row in range(len(data_show)):
        for col in range(len(Subtitle_req)):
            Label(root, text=data_show[row][0][col], bg='light salmon').grid(sticky="news", row=row + 6, column=col, padx=1)
    # surplus show alert
    for row in range(len(data_show)):
        if data_show[row][0][4] < 0:
            Label(root, text=data_show[row][0][4], bg='red').grid(sticky="news", row=row + 6, column=4, padx=1)
        else:
            Label(root, text=data_show[row][0][4], bg='lawn green').grid(sticky="news", row=row + 6, column=4, padx=1)
    # show total budget
    total_budget = sum(total_budget_lst)
    Label(root, text=total_budget, bg='yellow').grid(sticky="news", row=2, column=2, padx=1)

def custom_day():
    root2 = Tk()

    def date_submit(e):
        Select_Data()
        # print(bom_data_lst) # ingredients
        select_production_data()
        # print(production_plan_lst) # MPS
        Select_fill_Data()
        # print(unit_per_batch[0]) # Unit per batch
        select_invent_data()
        # print(data_invent_list)

        # Find material available in current range # same number in every date ranges
        pudding_available()

        # get waiting range     # select current date
        for i in range(len(production_plan_lst)):
            start_struc = time.strptime(production_plan_lst[i][0], '%Y-%m-%d %H:%M:%S')  # convert duetime
            pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
            production_plan_lst[i].append(pubdate)
        # print(production_plan_lst)
        # print(current_date)
        # find and waiting required materials.
        production_select = []
        current_date = datetime.date(int(year.get()), int(month.get()), int(day.get()))
        for i in range(len(production_plan_lst)):
            if production_plan_lst[i][-1] == current_date: #########
                if production_plan_lst[i][6] == 'Waiting':
                    production_select.append(production_plan_lst[i])
        print(production_select)
        # get production batch number # arrangement
        product_arrangement = []
        for i in range(len(production_select)):
            produce_n, surplus_n = spilt_str_produce(production_select[i][3])
            product_arrangement.append(int(produce_n))
        # print(product_arrangement)
        req_batch_material = sum(product_arrangement)
        # print(req_batch_material)

        # find total required per ingredients
        # bom material # use pudding available function
        for i in range(len(req_ingre)):
            req_ingre[i][1] = round(req_ingre[i][1] * req_batch_material, 5)  # round-off error (5 decimal place)

        # find surplus #change diff available ingredients to surplus
        surplus_lst = []
        for i in range(len(req_ingre)):
            sup_num = round(diff_ava_ingre[i][1] - req_ingre[i][1], 5)  # round-off error (5 decimal place)
            name_mat = diff_ava_ingre[i][0]
            surplus_lst.append([name_mat, sup_num])

        # find purchase needed
        # print(bom_data_lst)
        purchase_qty = []
        purchase_needed = []
        for i in range(len(bom_data_lst)):
            purchase_qty.append([bom_data_lst[i][1], bom_data_lst[i][4], bom_data_lst[i][7]])
        # print(purchase_qty)
        for i in range(len(surplus_lst)):
            if surplus_lst[i][1] < 0:
                purchase_needed.append(surplus_lst[i])
        # print(purchase_needed)
        purchase_needed_ans = []
        for i in range(len(purchase_needed)):
            for t in range(len(purchase_qty)):
                if purchase_needed[i][0] == purchase_qty[t][0]:
                    prod_name = purchase_needed[i][0]
                    buy_qty = math.ceil(abs(purchase_needed[i][1]) / purchase_qty[t][1])
                    budget_needed = buy_qty * purchase_qty[t][2]
                    purchase_needed_ans.append([prod_name, buy_qty, budget_needed])

        # print(diff_ava_ingre) # Material available #add [2]:Material avail.
        # print(req_ingre) #purchase and budget needed #add [3]: Total req.
        # print(surplus_lst) #surplus # add [4]:surplus
        # print(purchase_needed_ans) # total required materials #add [6]: Purchase needed, [8] Budget needed

        #  print(bom_data_lst) #keep [0]:serial, [1]:Name, [3]:purchase unit, [6]:ind. unit # add [0],[1],[7],[5]
        # create data to show
        data_show = []
        total_budget_lst = []  # find total budget spend needed
        for i in range(len(bom_data_lst)):
            data_set = []
            seq_0, seq_1 = bom_data_lst[i][0], bom_data_lst[i][1]
            seq_2 = diff_ava_ingre[i][1]
            seq_3 = req_ingre[i][1]
            seq_4 = surplus_lst[i][1]
            seq_5 = bom_data_lst[i][6]
            seq_6 = 0
            seq_8 = 0
            for t in range(len(purchase_needed_ans)):
                if seq_1 == purchase_needed_ans[t][0]:
                    seq_6 = purchase_needed_ans[t][1]
                    seq_8 = purchase_needed_ans[t][2]
                    total_budget_lst.append(seq_8)
                    break
                else:
                    seq_6 = 0
                    seq_8 = 0
            seq_7 = bom_data_lst[i][3]
            data_set.append([seq_0, seq_1, seq_2, seq_3, seq_4, seq_5, seq_6, seq_7, seq_8])
            data_show.append(data_set)
        # print(data_show)
        for row in range(len(data_show)):
            for col in range(len(Subtitle_req)):
                Label(root, text=data_show[row][0][col], bg='light salmon').grid(sticky="news", row=row + 6, column=col,
                                                                                 padx=1)
        # surplus show alert
        for row in range(len(data_show)):
            if data_show[row][0][4] < 0:
                Label(root, text=data_show[row][0][4], bg='red').grid(sticky="news", row=row + 6, column=4, padx=1)
            else:
                Label(root, text=data_show[row][0][4], bg='lawn green').grid(sticky="news", row=row + 6, column=4,
                                                                             padx=1)
        # show total budget
        total_budget = sum(total_budget_lst)
        Label(root, text=total_budget, bg='yellow').grid(sticky="news", row=2, column=2, padx=1)

    root2.title("Calendar")
    root2.option_add("*Font", "arial 15")
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

# Select date
# range cbo
date_range = ["Next 3 days","Next 7 days","Last 3 days","Last 7 days"]
range_date_cbo = ttk.Combobox(root, values=date_range, width=header_width)
range_date_cbo.current(1)
range_date_cbo.grid(row=2, padx=1, sticky='news', column=set_start_col+1)
# range select
range_date_but = Button(root, text="select", height=1, bg="plum", command=create_data_select)
range_date_but.grid(row=2, padx=1, sticky='news', column=set_start_col+2)
# today button
today_but = Button(root, text="today", height=1, bg="plum", command=create_data_today)
today_but.grid(row=2, padx=1, sticky='news', column=set_start_col+3)
# total button
total_but = Button(root, text="total", height=1, bg="plum", command=create_data_total)
total_but.grid(row=2, padx=1, sticky='news', column=set_start_col+4)
# custom button
cus_but = Button(root, text="custom", height=1, bg="plum", command=custom_day)
cus_but.grid(row=2, padx=1, sticky='news', column=set_start_col+5)


root.mainloop()
