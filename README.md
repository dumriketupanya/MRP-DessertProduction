
# Integrated Material Requirements Planning (MRP) Program for a Dessert Production 

This project aims to develop an Integrated MRP program for dessert production, which can also be adapted for other products based on its underlying principles. The objective of the program is to create an interactive platform enabling users to add orders, create bills of materials, manage inventories, control production batches, and facilitate the procurement process.

Our primary goal is to oversee the entire process, fostering more efficient operational management and cost-effective control.


## Material Requirement Plan (MRP)
## Sample program - Order Management System (OMS)

Below is a sample of the Order Management module, which is a component of our program. We have developed this prototype using the Python language to interact with an SQLite3 database, known for its robustness. The graphical user interface (GUI) has been created using tkinter to provide an interactive experience.

#### Importing necessary modules
    from tkinter import *               # Importing the entire tkinter module
    from tkinter import ttk             # Importing the ttk submodule for themed widgets
    from tkinter import messagebox      # Importing the messagebox submodule
    import sqlite3                      # Importing the sqlite3 module
    import time, datetime               # Importing the time and datetime modules for time-related operations


### Database interaction

#### Function to create the 'Order_Records' table in the 'Production_Plan.sqlite' database
    def create_data_table():
        try:
        with sqlite3.connect("Production_Plan.sqlite") as con:          # Establishing a connection to the 'Production_Plan.sqlite' database
            sql_cmd = """                                               # SQL command to create the 'Order_Records' table with specific columns
            CREATE TABLE IF NOT EXISTS Order_Records (
                Order_Number REAL PRIMARY KEY,
                Customer TEXT,
                Product TEXT,
                Order_Quantity REAL,
                Record_Datetime TEXT,
                Due_Datetime TEXT,
                Progress TEXT
            );
            """
            con.execute(sql_cmd)                                        # Executing the SQL command to create the table
    
    except Exception as e:                                              # Printing an error message if an exception occurs
        print("Error -> {}".format(e))          
####
    # Create Global lists to store data retrieved from the database
    Data_list = []
    data_lst_eff = []


#### Function to select and populate data from the 'Order_Records' table into the 'Data_list' global list
    def select_data():
    try:
        data_lst_eff.clear()                                            # Clearing the existing data list
        with sqlite3.connect("Production_Plan.sqlite") as con:          # Establishing a connection to the 'Production_Plan.sqlite' database
            sql_cmd = """	                                            # SQL command to select all data from the 'Order_Records' table
            SELECT * FROM Order_Records
            """
            for row in con.execute(sql_cmd):	                        # Executing the SQL command and iterating over the result set
                Data_list.append(list(row))	                            # Appending each row (converted to a list) to the 'Data_list' global list

	except Exception as e:	                                            # Printing an error message if an exception occurs
        print("Error -> {}".format(e))

#### Function to efficiently select and populate data from the 'Order_Records' table into the 'data_lst_eff' global list
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
#### 
    # Global list to store data retrieved from the 'setting_property' table
    setting_lst = []


##### Function to select and populate data from the 'setting_property' table into the 'setting_lst' global list
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
#### 
    # Global variable to store data retrieved from the 'Fill' table
    unit_per_batch = 0

#### Function to select and retrieve data from the 'Unit_per_Batch' column of the 'Fill' table
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
		

#### Creating the 'Order_Records' table and selecting when executing a program 
    create_data_table()
    select_data()