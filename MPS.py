"""
Filename: MPS.py
Description: This script serves as the Master Plan Schedule (MPS). Which use for effectively control the production line.
Author: Dumri Ketupanya
Date created: June 8, 2020
"""

# import required modules =====================================================================================
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk  # ttk -> themed tk (for Combobox)
import time, datetime
import math
import sys

# SQLite Database Connection ===================================================================================
def create_setting_data_table():
    try:
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            CREATE table setting_property(Ideal_production_time real, Start_time text,
            Finish_time text, Expected_time real, Margin_of_safety real, AVG_Distribution_time real,
            Time_produce_per_batch real);
            """
            con.execute(sql_cmd)
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

cal_time_pro = []
sum_cal_time_pro = []
ans_sum = 0

def calculate_time_produce(): #AVG_Distribution_time is Excluded!!
    try:
        global ans_sum
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT Expected_time, Margin_of_safety FROM setting_property
            """
            cal_time_pro.clear()
            sum_cal_time_pro.clear()
            ans_sum = 0
            for row in con.execute(sql_cmd):
                cal_time_pro.append(list(row))
            for i in (cal_time_pro[0]):
                sum_cal_time_pro.append(float(i))
            ans_sum = sum(sum_cal_time_pro)
    except Exception as e:
        print("Error -> {}".format(e))

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

create_setting_data_table()
calculate_time_produce()

# User Interface and Program Logic Section =======================================================================================
root = Tk()
root.title("Purchased Records")
root.option_add("*Font", "arial 11")

# Title
Title_frame = Frame(root, bg='wheat1')
Title_frame.grid(row=0, column=0, columnspan=12, sticky='news')
Title_Label = Label(Title_frame, text="Master Plan Schedule")
Title_Label.pack(padx=10, pady=10, side=LEFT)

# Subtitle
subtitle_width = 16
Title_frame1 = Frame(root, bg='wheat1')
Title_frame1.grid(row=1, column=0, columnspan=6, sticky='news')
Subtitle_1 = ["Batch production time", "units per batch", "Working hours", "Maximum efficiency", "Effective efficiency"]
for e, i in enumerate(Subtitle_1):
    Label(Title_frame1, text=i, bg="gold2", width=subtitle_width).pack(padx=1, pady=1, side=LEFT)

# Overall data
Title_frame2 = Frame(root, bg='wheat1')
Title_frame2.grid(row=2, column=0, columnspan=6, sticky='news')

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

Select_fill_Data()

# print(unit_per_batch[0])
unit_batch_data = Label(Title_frame2, text=unit_per_batch[0], width=subtitle_width, height=1, bg="plum")
unit_batch_data.grid(row=2, padx=1, sticky='news', column=(Subtitle_1.index("units per batch")))

# Setting command
def setting():
    root_setting = Tk()
    root_setting.title("Setting property")
    root_setting.option_add("*Font", "arial 11")
    # Function call
    select_setting_data()
    print(setting_lst)
    # header
    head1 = Frame(root_setting, bg='green')
    head1.grid(row=0, column=0, columnspan=5, sticky='news')
    header = Label(head1, text="Setting property")
    header.pack(padx=10, pady=10, side=LEFT)
    # data discription
    data_dis_lab = ['Information', 'Amount of time', 'Unit', 'Edit data']
    for e,i in enumerate(data_dis_lab):
        Label(root_setting, text=i, bg='yellow2').grid(row=1, column=e)

    # Left side: data title
    title_name = ['Ideal production time', 'Start time of the day', 'Finish time of the day', '',
                  'Expected production time' , 'Time margin of safety', 'Average distribution time',
                  'Time produce per batch']
    title_row = 2
    title_f = Frame(root_setting, bg='green')
    title_f.grid(row=title_row, column=0)
    date_f = Frame(root_setting, bg='gold2')
    date_f.grid(row=title_row, column=1)
    unit_f = Frame(root_setting, bg='khaki1')
    unit_f.grid(row=title_row, column=2)
    entry_f_col = 'yellow2'
    entry_f = Frame(root_setting, bg=entry_f_col)
    entry_f.grid(row=title_row, column=3)
    date_button_f = Frame(root_setting, bg=entry_f_col)
    date_button_f.grid(row=title_row, column=4)
    def create_table_set():
        data_seq = 0
        for e,i in enumerate(title_name):
            if i != '':
                Label(title_f, bg='green', text=title_name[e]).grid(row=e+1, pady=1, sticky='w')
                Label(date_f, bg='gold2', text= setting_lst[0][data_seq], width=15).grid(row=e + 1, pady=1, sticky='news')
                Label(unit_f, bg='khaki2', text='minutes', width=7).grid(row=e + 1, pady=1)
                data_seq = data_seq+1
            if i == 'Start time of the day':
                Label(unit_f, bg='khaki2', text='hours', width=7).grid(row=e + 1, pady=1)
            if i == 'Finish time of the day':
                Label(unit_f, bg='khaki2', text='hours', width=7).grid(row=e + 1, pady=1)
            if i == '':
                Label(title_f, bg='green', text='', width=15).grid(row=e + 1, pady=1, sticky='w')
                Label(date_f, bg='gold2', text='', width=15).grid(row=e + 1, pady=1, sticky='news')
                Label(unit_f, bg='khaki2', text='', width=7).grid(row=e + 1, pady=1)
    create_table_set()
    # Entry form
    lst_entry = []
    def entry_form():
        for i in range(len(title_name)):
            n = title_name[i]
            if n == '' or n == 'Start time of the day' or n == 'Finish time of the day' or n == 'Average distribution time'\
                    or n == 'Time produce per batch':
                Label(entry_f, bg=entry_f_col, text='', width=7).grid(row=i + 1, pady=1)
            else:
                en = Entry(entry_f, textvariable=DoubleVar(), width=15)
                en.grid(row=i + 1, pady=1)
                lst_entry.append(en)
    entry_form()
    # date_form
    collect_start_time = []
    def start_time_add():
        root2 = Tk()
        def date_submit(e):
            collect_time = datetime.time(int(hour.get()), int(minute.get()), int(sec.get()))
            collect_time_print = f"{collect_time}"
            collect_start_time.insert(0, f"{collect_time}")  # To collect time
            # print(collect_date)
            # print(collect_time)
            # print(currentDT)
            Start_time = Label(entry_f, text=collect_time_print, bg="plum")
            Start_time.grid(row=2, padx=5, sticky='w')
        root2.title("Calendar")
        root2.option_add("*Font", "consolas 15")
        hour_list = range(0, 25)
        minute_list = range(0, 61)
        sec_list = range(0, 61)
        title = ["Hour", "Minute", "Sec"]
        for e, i in enumerate(title):
            Label(root2, text=i).grid(row=0, column=e, sticky=W)
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

    collect_finish_time = []
    def finish_time_add():
        root2 = Tk()
        def date_submit(e):
            collect_time = datetime.time(int(hour.get()), int(minute.get()), int(sec.get()))
            collect_time_print = f"{collect_time}"
            collect_finish_time.insert(0, f"{collect_time}")  # To collect time
            # print(collect_date)
            # print(collect_time)
            # print(currentDT)
            Start_time = Label(entry_f, text=collect_time_print, bg="plum")
            Start_time.grid(row=3, padx=5, sticky='w')
        root2.title("Calendar")
        root2.option_add("*Font", "consolas 15")
        hour_list = range(0, 25)
        minute_list = range(0, 61)
        sec_list = range(0, 61)
        title = ["Hour", "Minute", "Sec"]
        for e, i in enumerate(title):
            Label(root2, text=i).grid(row=0, column=e, sticky=W)
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

    # date button
    for i in range(len(title_name)):
        Label(date_button_f, bg=entry_f_col, text='', width=7).grid(row=i + 1, pady=1)
    start_time = Button(date_button_f, text="edit time", height=1, bg="plum", command=start_time_add)
    start_time.grid(row=2, padx=5, sticky='w')
    finish_time = Button(date_button_f, text="edit time", height=1, bg="plum", command=finish_time_add)
    finish_time.grid(row=3, padx=5, sticky='w')

    # Get AVG Distribution time # Float data type
    avg_dis_time = [0]
    def avg_time_update():
        # Get data from distribution window
        # Change avg_dis_time
        Label(entry_f, bg=entry_f_col, text=avg_dis_time[0], width=7).grid(row=7, pady=1)
    avg_time_update()

    # approved command
    def approved_data():
        # Seperate type of data (float, str)
        select_setting_data()
        data_approved_form = []
        for entry in lst_entry:
            try:
                data_approved_form.append(float(entry.get()))
            except:
                data_approved_form.append(0)
        print(data_approved_form)
        try:
            start_time_collected = collect_start_time[0]
            data_approved_form.insert(1,start_time_collected)
        except:
            data_approved_form.insert(1,'NONE')
        try:
            fin_time_collected = collect_finish_time[0]
            data_approved_form.insert(2,fin_time_collected)
        except:
            data_approved_form.insert(2,'NONE')
        print(data_approved_form)
        head_title = ['Ideal_production_time', 'Start_time', 'Finish_time', 'Expected_time', 'Margin_of_safety']
        # ZERO unapproved
        with sqlite3.connect("Production_Plan.sqlite") as con:
            for e,i in enumerate(data_approved_form):
                if i == 0 or i == 'NONE':
                    print('a')
                elif type(i) == str:
                    print('b')
                    print(head_title[e])
                    print(data_approved_form[e])
                    con.execute(f"""UPDATE setting_property SET {head_title[e]} = '{i}'""")
                else:
                    print('c')
                    print(head_title[e])
                    print(data_approved_form[e])
                    con.execute(f"""UPDATE setting_property SET {head_title[e]} = {i}""")
            # calculate_time_produce()
            # print(ans_sum)
            # con.execute(f"""UPDATE setting_property SET Time_produce_per_batch = {ans_sum}""")
            # Database not updated immediately. If you want to get new updated data, do it in new 'with' command!!
        with sqlite3.connect("Production_Plan.sqlite") as con:
            calculate_time_produce()
            print(ans_sum)
            con.execute(f"""UPDATE setting_property SET Time_produce_per_batch = {ans_sum}""")
        select_setting_data()
        batch_prod_time_show()
        working_hour_show()
        # print(ans_sum)
        create_table_set()
        working_period()

    # Edit approved button
    approved = Button(root_setting, text="approved", height=1, bg="plum", command=approved_data)
    approved.grid(row=1, column=len(data_dis_lab))

    root_setting.mainloop()

# Setting button
set_but = Button(Title_frame2, text="setting", height=1, bg="plum", command=setting)
set_but.grid(row=2, padx=1, sticky='news', column=(Subtitle_1.index('Effective efficiency'))+1)

# Batch production time show
select_setting_data()
def batch_prod_time_show():
    batch_prod_time_ans = setting_lst[0][-1]
    batch_prd_data = Label(Title_frame2, text=batch_prod_time_ans, width=subtitle_width, height=1, bg="plum")
    batch_prd_data.grid(row=2, padx=1, sticky='news', column=(Subtitle_1.index("Batch production time")))
batch_prod_time_show()

# Working hour show # Maximum eff. calculator
def working_hour_show():
    start_day = setting_lst[0][1]  # [[60.0, '12:00:00', '14:00:00', 12.0, 51.0, 60.0, 123.0]]
    end_day = setting_lst[0][2]
    start_add_day = f'02/18/00 {start_day}'
    end_add_day = f"02/18/00 {end_day}"
    convert_start_day = time.strptime(start_add_day, '%m/%d/%y %H:%M:%S')
    convert_end_day = time.strptime(end_add_day, '%m/%d/%y %H:%M:%S')
    mk_start_day = time.mktime(convert_start_day) # day after EPOCH DAY needed to perform mk.time command.
    mk_end_day = time.mktime(convert_end_day)
    diff_time = mk_end_day-mk_start_day
    # print(diff_time)
    hour_diff_time = int(diff_time//3600)
    min_diff_time = int((diff_time//60)%60)
    sec_diff_time = int(diff_time%60)
    time_cal = Label(Title_frame2, text=f"{hour_diff_time}:{min_diff_time}:{sec_diff_time} hours", width=subtitle_width, height=1, bg="plum")
    time_cal.grid(row=2, padx=1, sticky='news', column=(Subtitle_1.index("Working hours")))
    # Max Eff. # (ROUNDDOWN(Working time/Ideal production time))*Unit per batch
    working_time_cal = int(diff_time // 60)
    ideal_min_cal = setting_lst[0][0]
    unit_p_batch_cal = unit_per_batch[0]
    max_eff_unit = (working_time_cal//ideal_min_cal)*unit_p_batch_cal
    maxeff__cal = Label(Title_frame2, text=f"{max_eff_unit} unit per day", width=subtitle_width, height=1, bg="plum")
    maxeff__cal.grid(row=2, padx=1, sticky='news', column=(Subtitle_1.index("Maximum efficiency")))
    # Effective eff. # (ROUNDDOWN(Working time/Expected production time))*Unit per batch
    expected_min_cal = setting_lst[0][3]
    efc_eff_unit = (working_time_cal//expected_min_cal)*unit_p_batch_cal
    efceff__cal = Label(Title_frame2, text=f"{efc_eff_unit} unit per day", width=subtitle_width, height=1, bg="plum")
    efceff__cal.grid(row=2, padx=1, sticky='news', column=(Subtitle_1.index("Effective efficiency")))
working_hour_show()

edge_table = 18
work_tab_width = 7
# Working period
working_time_lab = Label(root, text="Working period", bg='green yellow', width =work_tab_width)
working_time_lab.grid(row=3, column=0,padx=1, pady=5, columnspan=1, sticky='news')
# Accumulated eff. capacity
acc_unit_label = Label(root, text="Eff. capacity", bg='green yellow', width =work_tab_width)
acc_unit_label.grid(row=3, column=1,padx=1, pady=5, columnspan=1, sticky='news')
# Accumulated Maximum capacity
# acc_max_unit_label = Label(root, text="Max. capacity", bg='green yellow', width =work_tab_width)
# acc_max_unit_label.grid(row=3, column=1,padx=1, pady=5, columnspan=1, sticky='news')
edged = Label(root, bg='pink', width =1)
edged.grid(row=3, column=2, columnspan=1, rowspan= edge_table+1,sticky='news')

period_range = []
def working_period():
    select_setting_data()
    for a in range(edge_table):
        Label(root, text='', bg='green yellow', width=5).grid(row=4+a, column=0, padx=1, pady=1, columnspan=1, sticky='news')
        Label(root, text='', bg='green yellow', width=5).grid(row=4+a, column=1, padx=1, pady=1, columnspan=1, sticky='news')
    start_day = setting_lst[0][1] # [[60.0, '12:00:00', '14:00:00', 12.0, 51.0, 60.0, 123.0]]
    end_day = setting_lst[0][2]
    time_prod_batch = setting_lst[0][-1]
    start_add_day = f'02/18/00 {start_day}'
    end_add_day = f"02/18/00 {end_day}"
    convert_start_day = time.strptime(start_add_day, '%m/%d/%y %H:%M:%S')
    convert_end_day = time.strptime(end_add_day, '%m/%d/%y %H:%M:%S')
    mk_start_day = time.mktime(convert_start_day) # day after EPOCH DAY needed to perform mk.time command.
    mk_end_day = time.mktime(convert_end_day)
    # calculation
    diff_min_time = (mk_end_day-mk_start_day)/60
    period = diff_min_time//time_prod_batch
    global period_range
    period_range = []
    for t in range(int(period)):
        a = mk_start_day+(time_prod_batch*60)*t # minute time_prod_batch ---> second
        time_cona = time.ctime(a)
        time_con = time.strptime(time_cona, '%a %b %d %H:%M:%S %Y')
        t_hour = time_con.tm_hour
        t_min = time_con.tm_min
        t_sec = time_con.tm_sec
        prep_date = datetime.time(t_hour,t_min,t_sec)
        period_range.append(prep_date)
    excess_time= diff_min_time%time_prod_batch
    # maximum capacity
    Select_fill_Data()
    # print(unit_per_batch[0])
    # Show data
    for t in range(int(period)):
        Label(root, text=period_range[t], bg='green yellow', width=work_tab_width). \
            grid(row=4+t, column=0, padx=1, pady=1, columnspan=1, sticky='news')
        Label(root, text=unit_per_batch[0]*t, bg='green yellow', width=work_tab_width). \
            grid(row=4+t, column=1, padx=1, pady=1, columnspan=1, sticky='news')
    Label(root, text=f'left {excess_time} min.', bg='green yellow', width=work_tab_width).\
        grid(row=4 + int(period), column=0, padx=1, pady=1,columnspan=1, sticky='news')
    Label(root, text=unit_per_batch[0] * int(period), bg='green yellow', width=work_tab_width).\
        grid(row=4 + int(period), column=1, padx=1, pady=1,columnspan=1, sticky='news')
working_period()

# Data title table
dat_width = 15
data_title = ['Due time', 'Start time', 'Finish time', 'Produce', 'Order NO.', 'Order quantity', 'progress', '']
for e, i in enumerate(data_title):
    Label(root, text=i, bg="gold2",width=dat_width).grid(row=3, column=3+e, padx=1, pady=1,columnspan=1, sticky='news')

# Data schedule table
# Create PRoduction plan database
def create_production_plan_schedule_table():
    try:
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            CREATE table Production_plan(Due_time text, Start_time text, Finish_time text, Produce text, Order_Number real, 
            Order_Quantity real, progress text, Actual_Time text);
            """
            con.execute(sql_cmd)
    except Exception as e:
        print("Error -> {}".format(e))
create_production_plan_schedule_table()

# Get data
data_table_lst = []
def select_schedule_data():
    try:
        with sqlite3.connect("Production_Plan.sqlite") as con:
            sql_cmd = """
            SELECT * FROM Production_plan
            """
            data_table_lst.clear()
            for row in con.execute(sql_cmd):
                data_table_lst.append(list(row))
    except Exception as e:
        print("Error -> {}".format(e))
select_schedule_data()

def create_plain_table():
    for r in range(len(data_table_lst)):
        for col in range(len(data_title)):
            Label(root, text="", bg='light salmon').grid(sticky="news", row=r + 4, column=col+3, padx=1)
create_plain_table()


# Start and Finish time
def time_production():
    select_schedule_data()
    # print(data_table_lst)
    for i in range(len(data_table_lst)):
        convert_due_date = time.strptime(data_table_lst[i][0], '%Y-%m-%d %H:%M:%S')
        flo_due_date = time.mktime(convert_due_date)
        # convert_due_date = time.strptime(data_table_lst[i][0], '%Y-%m-%d %H:%M:%S')
        del data_table_lst[i][0]
        data_table_lst[i].insert(0,flo_due_date)
    select_setting_data() # Distribution time : setting_lst[0][5], Production per batch :setting_lst[0][6]
    dis_time_sec = (setting_lst[0][5])*60
    prod_time_sec = (setting_lst[0][6])*60
    for i in range(len(data_table_lst)):
        start_time = data_table_lst[i][0]-prod_time_sec-dis_time_sec
        c_start_time = time.ctime(start_time)
        struc_start_time = time.strptime(c_start_time,"%a %b %d %H:%M:%S %Y")
        time_st_form = time.strftime('%Y-%m-%d %H:%M:%S', struc_start_time)
        fin_time = data_table_lst[i][0]-dis_time_sec
        c_fin_time = time.ctime(fin_time)
        struc_fin_time = time.strptime(c_fin_time,"%a %b %d %H:%M:%S %Y")
        time_fin_form = time.strftime('%Y-%m-%d %H:%M:%S', struc_fin_time)
        del data_table_lst[i][1]
        data_table_lst[i].insert(1, time_st_form)
        del data_table_lst[i][2]
        data_table_lst[i].insert(2, time_fin_form)
    for i in range(len(data_table_lst)):
        c_due_time = time.ctime(data_table_lst[i][0])
        struc_due_time = time.strptime(c_due_time,"%a %b %d %H:%M:%S %Y")
        time_due_form = time.strftime('%Y-%m-%d %H:%M:%S', struc_due_time)
        del data_table_lst[i][0]
        data_table_lst[i].insert(0, time_due_form)
    working_period()
    try:
        for e,i in enumerate(data_table_lst):
            with sqlite3.connect("Production_Plan.sqlite") as con:
                sql_cmd_1 = f"""UPDATE Production_plan SET Start_time = '{data_table_lst[e][1]}' WHERE Order_Number = {data_table_lst[e][4]}"""
                sql_cmd_2 = f"""UPDATE Production_plan SET Finish_time = '{data_table_lst[e][2]}' WHERE Order_Number = {data_table_lst[e][4]}"""
                con.execute(sql_cmd_1)
                con.execute(sql_cmd_2)
    except Exception as e:
        print("Error -> {}".format(e))
time_production()

# Overall and select
overall_width=12

Subtitle_over = ["Overall output","Overall surplus","Select lastest"]
for e, i in enumerate(Subtitle_over):
    Label(root, text=i, bg="gold2", width=overall_width).grid(row=1, column=6+e, sticky='news')

# Overall plain table
Label(root, text="", bg="gold2", width=overall_width).grid(row=2, column=6, sticky='news')
Label(root, text="", bg="gold2", width=overall_width).grid(row=2, column=7, sticky='news')

#Filter combo box
date_range = ["Next 3 days","Next 7 days","Last 3 days","Last 7 days"] # "Today",
date_filter = ttk.Combobox(root, values=date_range, width=12, state="readonly")
date_filter.grid(row=2, column=8, sticky='news')
date_filter.current(0)

# Create schedule table
def create_sche_table():
    # time_production()
    for r in range(len(data_table_lst)):
        for col in range(len(data_title)-1): # Subtract_" "
            Label(root, text="", bg='light salmon').grid(sticky="news", row=r + 4, column=col+3, padx=1)
create_sche_table()

day_diff_set = {0} # PLace product arrangement before create table.
def produce_arrangenment():
    global day_diff_set
    select_schedule_data()
    for i in range(len(data_table_lst)):
        start_struc = time.strptime(data_table_lst[i][1], '%Y-%m-%d %H:%M:%S')
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        data_table_lst[i].append(pubdate)
        day_diff_set.update({pubdate})
    day_diff_set.remove(0)
    lst_before_sort_day_diff = list(day_diff_set)
    lst_day_diff = sorted(lst_before_sort_day_diff)
    # print(data_table_lst)
    # print(lst_day_diff)
    group = []
    for dif in range(len(lst_day_diff)):
        sub_group = []
        for dat in range(len(data_table_lst)):
            if data_table_lst[dat][-1] == lst_day_diff[dif]:
                sub_group.append(data_table_lst[dat])
        group.append(sub_group)
    # print(group) # Clear data to [[product, order NO., datetime]] #del 0,1,2,3,6,7 # append 4,5,8
    arrange_group = []
    for outer in range(len(group)):
        sub_arrange_group = []
        for inner in range(len(group[outer])):
            unit_ar = []
            unit_ar.append(group[outer][inner][4]) # add order NO.
            unit_ar.append(group[outer][inner][5]) # add order Qty.
            unit_ar.append(group[outer][inner][8]) # add datetime
            sub_arrange_group.append(unit_ar)
        arrange_group.append(sub_arrange_group)
    # print(arrange_group)
    Select_fill_Data()
    test = []
    # print(unit_per_batch[0]) # (batch, surplus) # Today's produced, Today's surplus # 0: Order NO., 1: qty., 2:datetime
    for outer in range(len(arrange_group)):
        start_day_set = [0] # Set zero for start of the day.
        for inner in range(len(arrange_group[outer])):
            acc_produce = start_day_set[-1]
            qty_get = arrange_group[outer][inner][1] # Get qty.
            if acc_produce < qty_get:
                produce = math.ceil((qty_get-acc_produce)/(unit_per_batch[0]))
                surplus = produce*(unit_per_batch[0])+start_day_set[-1]-qty_get
                sent_cmd = (produce, surplus)
                start_day_set.append(surplus)
                arrange_group[outer][inner].append(sent_cmd)
                test.append(sent_cmd)
            elif acc_produce >= qty_get:
                produce = 0
                surplus = start_day_set[-1]-qty_get
                sent_cmd = (produce, surplus)
                start_day_set.append(surplus)
                test.append(sent_cmd)
                arrange_group[outer][inner].append(sent_cmd)
    # print(test)
    # print(arrange_group)
    try:
        for outer in range(len(arrange_group)):
            for inner in range(len(arrange_group[outer])):
                with sqlite3.connect("Production_Plan.sqlite") as con:
                    con.execute(f"""UPDATE Production_plan SET Produce = '{arrange_group[outer][inner][3]}' 
                    WHERE Order_Number = {arrange_group[outer][inner][0]}""")
    except Exception as e:
        print("Error -> {}".format(e))
produce_arrangenment()

# Combobox change process
cbo_column_width = 10
long_row = 18
cbo_progress_lst = []
for i in range(long_row):
    progress_opt = ["Waiting", "Work in process", "Finished"]
    cbo_progress = ttk.Combobox(root, values=progress_opt, width=dat_width, state="readonly")
    cbo_progress.current(0)
    cbo_progress.grid(row=i+4, column=cbo_column_width)
    cbo_progress_lst.append(cbo_progress)

# Filter select
show_data_lst = []
def filter_select(): #  Choose from start production day.
    get_date = date_filter.get()
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
    select_schedule_data()
    for i in range(len(data_table_lst)):
        start_struc = time.strptime(data_table_lst[i][1], '%Y-%m-%d %H:%M:%S')
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        data_table_lst[i].append(pubdate)
    current_date = datetime.date.today()
    # print(data_table_lst[0][-1]-current_date) # Last ### days -
    # print(data_table_lst[-1][-1]-current_date) # Next ### days +
    global  show_data_lst
    show_data_lst = []
    for i in range(len(data_table_lst)):
        if (data_table_lst[i][-1]-current_date) >= filday and (data_table_lst[i][-1]-current_date) <= bench_filday:
            show_data_lst.append(data_table_lst[i])
        if (data_table_lst[i][-1]-current_date) <= filday and (data_table_lst[i][-1]-current_date) >= bench_filday:
            show_data_lst.append(data_table_lst[i])
    for i in range(len(show_data_lst)):
        del show_data_lst[i][-1]
    create_sche_table()
    #overall
    order_num_lst = []    # Get order NO.
    for i,a in enumerate(show_data_lst):
        order_num_lst.append([show_data_lst[i][4], show_data_lst[i][1], show_data_lst[i][3]]) # Due date, order number, produce get
    set_date = {0}
    for i in range(len(order_num_lst)):
        start_struc = time.strptime(order_num_lst[i][1], '%Y-%m-%d %H:%M:%S')
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        order_num_lst[i].append(pubdate)
        set_date.update({pubdate})
    set_date = list(set_date)
    set_date.remove(0)
    arrange_data = []
    for i in set_date:
        sub_ar = {}
        for x in range(len(order_num_lst)):
            if order_num_lst[x][3] == i:
                sub_ar[order_num_lst[x][0]] =order_num_lst[x][2]
        arrange_data.append(sub_ar)
    get_max = []
    get_all = []
    for i in range(len(arrange_data)):
        dict_item = arrange_data[i].items()
        sorted_dict_item = sorted(dict_item)
        for x in range(len(sorted_dict_item)):
            get_all.append(sorted_dict_item[x])
        get_max.append(sorted_dict_item[-1])
    prod_all_lst = []
    for i in range(len(get_all)):
        product_a, surplus_a = spilt_str_produce(get_all[i][-1])
        prod_all_lst.append(float(product_a))
    Select_fill_Data()
    sum_prod_all = sum(prod_all_lst)
    sum_prod_all_unit = sum_prod_all*unit_per_batch[0]
    sur_l_lst = []
    for i in range(len(get_max)):
        product_l, surplus_l = spilt_str_produce(get_max[i][-1])
        sur_l_lst.append(float(surplus_l))
    # ans_prod_unit = ans_prod*unit_per_batch[0]
    ans_sur = sum(sur_l_lst)
    Label(root, text=f"{ans_sur} units", bg="gold2", width=overall_width).grid(row=2, column=7, sticky='news')
    Label(root, text=f"{sum_prod_all} batches, {sum_prod_all_unit} units", bg="gold2", width=overall_width). \
        grid(row=2, column=6, sticky='news')
    for i in range(len(show_data_lst)):
        if show_data_lst[i][6] == 'Waiting':
            cbo_progress_lst[i].current(0)
        elif show_data_lst[i][6] == 'Work in process':
            cbo_progress_lst[i].current(1)
        elif show_data_lst[i][6] == 'Finished':
            cbo_progress_lst[i].current(2)
    print(show_data_lst)
    for r in range(len(show_data_lst)):
        for col in range(len(data_title) - 1):
            if show_data_lst[r][col] == 'Waiting':
                Label(root, text=show_data_lst[r][col], bg='red').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
            elif show_data_lst[r][col] == 'Work in process':
                Label(root, text=show_data_lst[r][col], bg='yellow').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
            elif show_data_lst[r][col] == 'Finished':
                Label(root, text=show_data_lst[r][col], bg='green').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
            else:
                Label(root, text=show_data_lst[r][col], bg='light salmon').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)


# split product
def spilt_str_produce(string):
    a, b = string.split(", ")
    z, produce_n = a.split("(")
    surplus_n, q = b.split(")")
    return produce_n, surplus_n

def submit_sure():
    make_sure = messagebox.askyesno("Confirm!", """This action cannot be reversed. 
    Do you want to proceed?""")
    if make_sure == True:
        submit_progress()
    else:
        pass

def submit_progress():
    update_progress = [] # Update process data
    update_invent = [] # Update invent data

    Select_Data() # bom data
    # global bom_data_lst
    Select_fill_Data()     # unit_per_batch[0]
    # global unit_per_batch
    select_invent_data() # inventory data
    # global data_invent_list

    for i in range(len(show_data_lst)):
        dat_prep = (cbo_progress_lst[i].get())
        order_num = show_data_lst[i][4]
        batch_prod,sur_prod = spilt_str_produce(show_data_lst[i][3])
        update_progress.append([order_num, dat_prep])
        update_invent.append([int(batch_prod), order_num, dat_prep])
    # print(show_data_lst)
    # print(update_progress)
    # print(update_invent)
    # get unit_per_batch

    # select change
    # Get old data
    for i in range(len(update_invent)):
        try:
            with sqlite3.connect("Production_Plan.sqlite") as con:
                sql_cmd = f'''
                SELECT progress FROM Production_plan WHERE Order_Number = {update_invent[i][1]}
                '''
                for row in con.execute(sql_cmd):
                    update_invent[i].append(row[0]) #update_invent[i][3] = old, update_invent[i][2] = new
        except Exception as e :
            print("Error -> {}".format(e))
    for i in range(len(update_invent)): # total 9 cases
        if update_invent[i][3] == update_invent[i][2]:
            update_invent[i].append(0) # static # 3 cases
        elif update_invent[i][3] == 'Work in process' and update_invent[i][2] == 'Finished':
            update_invent[i].append(0) # don't count # 1 case
        elif update_invent[i][2] == 'Work in process' and update_invent[i][3] == 'Finished':
            update_invent[i].append(0) # don't count # 1 case
        else:
            update_invent[i].append(1) #changes count # 4 case

    bat_prod_lst = [] 
    for i in range(len(update_invent)):
        if update_invent[i][-1] == 1 and update_invent[i][3] == 'Waiting': 
            bat_prod_lst.append(update_invent[i][0])
    bat_prod = sum(bat_prod_lst)

    bom_data_arange = []
    for i in range(len(bom_data_lst)): #name, BOM qty, Pur qty, cost [1][2][4][7]
        name = bom_data_lst[i][1]
        bom_qty = bom_data_lst[i][2]
        pur_qty = bom_data_lst[i][4]
        pur_cost = bom_data_lst[i][7]
        bom_data_arange.append([name, bom_qty, pur_qty, pur_cost])

    bom_data_cal = []
    for i in range(len(bom_data_arange)):
        name = bom_data_arange[i][0]
        total_bom_use = float(bom_data_arange[i][1]*bat_prod)
        pur_cost_a = float(bom_data_arange[i][3])
        pur_qty_a = float(bom_data_arange[i][2])
        total_cost_use = (pur_cost_a/pur_qty_a)*total_bom_use
        bom_data_cal.append([name, total_bom_use, total_cost_use])
    # print("A", bom_data_cal) # ready to execute in inventory management

    # print(data_invent_list) # chose available
    current_date = datetime.date.today() 
    for i in range(len(data_invent_list)):
        start_struc = time.strptime(data_invent_list[i][7], '%Y-%m-%d') # convert duetime
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        data_invent_list[i].append(pubdate)

    avai_ingre = []
    for i in range(len(data_invent_list)):
        if current_date < data_invent_list[i][-1]:
            avai_ingre.append(data_invent_list[i])

    arange_avai_ingre = []
    for i in range(len(avai_ingre)):
        name = avai_ingre[i][1]
        remain_qty = avai_ingre[i][3]
        remain_cost = math.ceil(avai_ingre[i][6])
        date_a = avai_ingre[i][8]
        arange_avai_ingre.append([name, remain_qty, remain_cost, date_a])

    group_app = []
    for i in range(len(bom_data_cal)):
        sort_date = []
        for t in range(len(arange_avai_ingre)):
            if bom_data_cal[i][0] == arange_avai_ingre[t][0]:
                sort_date.append([bom_data_cal[i][0],str(arange_avai_ingre[t][1]),str(arange_avai_ingre[t][2]),
                                  arange_avai_ingre[t][3]])
        sort_date = sorted(sort_date)
        group_app.append(sort_date)
    # print(group_app) # date_sored # sort first non_string type data ############
    #change str to float
    for t in range(len(group_app)):
        for i in range(len(group_app[t])):
            group_app[t][i][1] = float(group_app[t][i][1])
            group_app[t][i][2] = float(group_app[t][i][2])
    # print("B",group_app) # ready to use
    # check available
    sum_ava = []
    print(group_app)
    for i in range(len(group_app)):
        sum_prep = []
        for t in range(len(group_app[i])):
            sum_prep.append(group_app[i][t][1])
        sum_sh = sum(sum_prep)
        sum_ava.append([group_app[i][0][0], sum_sh])
    # print(sum_ava) # Error mean don't have materials.
    ready_to_update = 0
    for i in range(len(bom_data_cal)):
        if bom_data_cal[i][1] > sum_ava[i][1]:
            print("Error",i)
            messagebox.showerror("Error!","Insufficient materials for production") #Error mean don't have enough materials.
            ready_to_update = 1
            break

    data_ingredients_update = [] # If have sufficient materials.
    for b in range(len(bom_data_cal)):
        for d in range(len(group_app)):
            initial_ingre = bom_data_cal[b][1]
            initial_cost = bom_data_cal[b][2]
            for q in range(len(group_app[d])):
                if group_app[d][q][0] == bom_data_cal[b][0]:
                    ingredient_remain = group_app[d][q][1] - initial_ingre
                    cost_remain = group_app[d][q][2] - initial_cost
                    if ingredient_remain >= 0:
                        name_ing = group_app[d][q][0]
                        date_time = group_app[d][q][3]
                        data_ingredients_update.append([name_ing, ingredient_remain, cost_remain,date_time])
                        break
                    else:
                        name_ing = group_app[d][q][0]
                        date_time = group_app[d][q][3]
                        data_ingredients_update.append([name_ing, 0, 0,date_time])
                        initial_ingre = abs(group_app[d][q][1] - initial_ingre)
                        initial_cost = abs(group_app[d][q][2] - initial_cost)
    # print(data_ingredients_update) ## Finish
    # update data (subtract)
    if ready_to_update == 0:
        try:
            for i in range(len(data_ingredients_update)):
                with sqlite3.connect("Inventory_Management.sqlite") as con:
                    update_inven = f"""UPDATE InventoryManagement SET Unit_Quantity_left = {data_ingredients_update[i][1]}, 
                                        Cost_left_Baht = {data_ingredients_update[i][2]} WHERE Expiration_Date = 
                                        '{data_ingredients_update[i][3]}' AND Name = '{data_ingredients_update[i][0]}' """
                    con.execute(update_inven)
        except Exception as e:
                print("Error -> {}".format(e))
    
    print(data_ingredients_update)  ## Finish
    # update data (plus)
    try:
        for i in range(len(data_ingredients_update)):
            with sqlite3.connect("Inventory_Management.sqlite") as con:
                update_inven = f"""UPDATE InventoryManagement SET Unit_Quantity_left = {data_ingredients_update[i][1]},
                                     Cost_left_Baht = {data_ingredients_update[i][2]} WHERE Expiration_Date =
                                     '{data_ingredients_update[i][3]}' AND Name = '{data_ingredients_update[i][0]}' """
                con.execute(update_inven)
    except Exception as e:
        print("Error -> {}".format(e))
    
    try:
        for i in range(len(update_progress)):
            with sqlite3.connect("Production_Plan.sqlite") as con:
                con.execute(f"""UPDATE Production_plan SET progress = '{update_progress[i][1]}' 
                WHERE Order_Number = {update_progress[i][0]}""")
                con.execute(f"""UPDATE Order_Records SET Progress = '{update_progress[i][1]}' 
                                WHERE Order_Number = {update_progress[i][0]}""")
    except Exception as e:
        print("Error -> {}".format(e))
    
    ########################## prevent insufficients material
    for r in range(len(show_data_lst)):
        if update_progress[r][1] == 'Waiting':
            Label(root, text=update_progress[r][1], bg='red').grid(sticky="news", row=r + 4,
                                                                            column=9, padx=1)
        elif update_progress[r][1] == 'Work in process':
            Label(root, text=update_progress[r][1], bg='yellow').grid(sticky="news", row=r + 4,
                                                                            column=9, padx=1)
        elif update_progress[r][1] == 'Finished':
            Label(root, text=update_progress[r][1], bg='green').grid(sticky="news", row=r + 4,
                                                                            column=9, padx=1)
        else:
            Label(root, text=update_progress[r][1], bg='light salmon').grid(sticky="news", row=r + 4,
                                                                        column=9, padx=1)

def custom_day():
    root2 = Tk()

    def date_submit(e):
        select_schedule_data()
        for i in range(len(data_table_lst)):
            start_struc = time.strptime(data_table_lst[i][1], '%Y-%m-%d %H:%M:%S')
            pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
            data_table_lst[i].append(pubdate)
        current_date = datetime.date(int(year.get()), int(month.get()), int(day.get()))
        show_data_lst = []
        for i in range(len(data_table_lst)):
            if data_table_lst[i][-1] == current_date:
                show_data_lst.append(data_table_lst[i])
        for i in range(len(show_data_lst)):
            del show_data_lst[i][-1]
        create_sche_table()
        for r in range(len(show_data_lst)):
            for col in range(len(data_title) - 1):
                if show_data_lst[r][col] == 'Waiting':
                    Label(root, text=show_data_lst[r][col], bg='red').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
                elif show_data_lst[r][col] == 'Work in process':
                    Label(root, text=show_data_lst[r][col], bg='yellow').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
                elif show_data_lst[r][col] == 'Finished':
                    Label(root, text=show_data_lst[r][col], bg='green').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
                else:
                    Label(root, text=show_data_lst[r][col], bg='light salmon').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
        # overall data
        try:
            produce_last, surplus_last = spilt_str_produce(show_data_lst[-1][3])
            all_prod = []
            for i in range(len(show_data_lst)):
                produce_g, surplus_g = spilt_str_produce(show_data_lst[i][3])
                all_prod.append(float(produce_g))
            produce_last = sum(all_prod)
            Select_fill_Data()
            product_u_last = float(produce_last) * unit_per_batch[0]
            Label(root, text=f"{surplus_last} units", bg="gold2", width=overall_width).grid(row=2, column=7, sticky='news')
            Label(root, text=f"{produce_last} batches, {product_u_last} units", bg="gold2", width=overall_width).grid(row=2,
                                                                                                                      column=6,
                                                                                                                      sticky='news')

        except Exception as e:
            messagebox.showerror("Error!!" ,"No production!!")

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


# Custom day
custom_but = Button(root, text="custom", bg='pink', command=custom_day)
custom_but.grid(row=1, column=9,columnspan=1, sticky='news')

#Submit Button
submit_but = Button(root, text="submit", bg='orange red', command=submit_sure)
submit_but.grid(row=1, column=10,columnspan=1, sticky='news')

def filter_select_today():
    select_schedule_data()
    for i in range(len(data_table_lst)):
        start_struc = time.strptime(data_table_lst[i][1], '%Y-%m-%d %H:%M:%S')
        pubdate = datetime.date(start_struc.tm_year, start_struc.tm_mon, start_struc.tm_mday)
        data_table_lst[i].append(pubdate)
    current_date = datetime.date.today() ############
    global show_data_lst
    show_data_lst = []
    for i in range(len(data_table_lst)):
        if data_table_lst[i][-1] == current_date:
            show_data_lst.append(data_table_lst[i])
    for i in range(len(show_data_lst)):
        del show_data_lst[i][-1]
    for i in range(len(show_data_lst)):
        if show_data_lst[i][6] == 'Waiting':
            cbo_progress_lst[i].current(0)
        elif show_data_lst[i][6] == 'Work in process':
            cbo_progress_lst[i].current(1)
        elif show_data_lst[i][6] == 'Finished':
            cbo_progress_lst[i].current(2)
    create_sche_table()
    for r in range(len(show_data_lst)):
        for col in range(len(data_title) - 1):
            if show_data_lst[r][col] == 'Waiting':
                Label(root, text=show_data_lst[r][col], bg='red').grid(sticky="news", row=r + 4,
                                                                       column=col + 3, padx=1)
            elif show_data_lst[r][col] == 'Work in process':
                Label(root, text=show_data_lst[r][col], bg='yellow').grid(sticky="news", row=r + 4,
                                                                          column=col + 3, padx=1)
            elif show_data_lst[r][col] == 'Finished':
                Label(root, text=show_data_lst[r][col], bg='green').grid(sticky="news", row=r + 4,
                                                                         column=col + 3, padx=1)
            else:
                Label(root, text=show_data_lst[r][col], bg='light salmon').grid(sticky="news", row=r + 4,
                                                                                column=col + 3, padx=1)
    # overall data
    produce_last, surplus_last = spilt_str_produce(show_data_lst[-1][3])
    all_prod = []
    for i in range(len(show_data_lst)):
        produce_g, surplus_g = spilt_str_produce(show_data_lst[i][3])
        all_prod.append(float(produce_g))
    produce_last = sum(all_prod)
    Select_fill_Data()
    product_u_last = float(produce_last)*unit_per_batch[0]
    Label(root, text=f"{surplus_last} units", bg="gold2", width=overall_width).grid(row=2, column=7, sticky='news')
    Label(root, text=f"{produce_last} batches, {product_u_last} units", bg="gold2", width=overall_width).grid(row=2, column=6, sticky='news')


def spilt_str_produce(string):
    a,b = string.split(", ")
    z,produce_n = a.split("(")
    surplus_n,q = b.split(")")
    return produce_n,surplus_n

# Filter button
filter_but = Button(root, text="choose", bg='pink', command=filter_select)
filter_but.grid(row=2, column=9, sticky='news')

#Today Button
today_but = Button(root, text="today", bg='pink', command=filter_select_today)
today_but.grid(row=2, column=10, sticky='news')

root.mainloop()