
# Integrated Material Requirements Planning (MRP) Program for a Dessert Production 

This project aims to develop an Integrated MRP program for dessert production, which can also be adapted for other products based on its underlying principles. The objective of the program is to create an interactive platform enabling users to add orders, create bills of materials, manage inventories, control production batches, and facilitate the procurement process.

Our primary goal is to oversee the entire process, fostering more efficient operational management and cost-effective control.


## Take a tour
Here's an overview of the 6 modules included in this program. We'll explain the principles behind each module as we tour through them. This diagram illustrates the overall principles behind the program.

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/MRP_Diagram.jpg" width="500" />
</p>

Let's get started!

### Home Page
The home page serves as the central hub to access other modules. User can also export the data files from the database too.

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/homePage.png" width="200" />
</p>

### Bill of materials (BOM)
The Bill of Materials (BOM) is a list of ingrediants, raw materials, components, or sub-assemblies needed to create a product. It includes quantities and sometimes also specify the hierarchy of components, showing how they are assembled.

Currently, the program is designed for a single product,which is a pudding!! Users can specify the quantities of each ingredient used. And can add or delete ingredients as needed. Additionally, the program allows users to input the cost of each ingredient too.

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/BOM.png" width="800" />
</p>

### Order Management System (OMS)
This module help streamlines the order processing workflow. It is an order tracking which starts from order creation and continues through inventory management, which is handled in another module.

Users can input customer names, products, order quantities, and adjust delivery times. A capacity gauge the remaining capacity for preventing order overload. Users also have the option to view, edit, and delete order history.

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/OMS.png" width="800" />
</p>


### Purchase Records
A Purchase Record is a detailed log of all purchased. It should includes information such as supplier details, purchase quantities, unit prices, and transaction dates. Purchase Records are essential for tracking procurement activities.

Users can create a purchase log by selecting the ingredient name from the Bill of Materials (BOM), specifying order quantities, cost, procurement date, production date, and expiration date. Also, users can view a detailed historical log of purchases.

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/PurchaseRecord.png" width="800" />
</p>


### Inventory Management System (IMS)
An Inventory Management helps track and manage store inventory levels. It shouldprovides a stock levels, locations, and movement, enabling better inventory control and reducing the risk of stockouts or overstocking.

Users can select an ingredient's name and then click "check." The system will display the available quantity of that ingredient, and users can also view the inventory list.

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/IMS.png" width="800" />
</p>



### Master Plan Schedule (MPS)
This is a detailed plan that specifies what products will be manufactured, in what quantities, and when. The MPS serves as a blueprint for production activities. It considers factors such as customer demand , production capacity, and resource availability which is derived from the other components.

The MPS displays production times per batch, working hours, maximum efficiency, and effective efficiency. The table shows total orders received and the status of each produced batch, including "waiting," "work in process (WIP)," and "Finished."

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/MPS.png" width="800" />
</p>


### Materials Requirement Plan (MRP)
A production planning and inventory control system that determines the materials needed for production based master plan Schedule. MRP helps in maintaining optimal inventory levels and ensuring that materials are available when needed for production.

This module displays production status, product availability, and the total budget required. The table lists each required ingredient and indicates any shortages or surpluses, which are related to the Master Plan Schedule (MPS).

<p align="center">
  <img src="https://github.com/dumriketupanya/MRP-DessertProduction/raw/main/Pictures/MRP.png" width="800" />
</p>




## Sample script - Order Management System

Below is a sample line of codes in the Order Management module, which is a component of our program. We have developed this prototype using the Python language to interact with an SQLite3 database, known for its robustness. The graphical user interface (GUI) has been created using tkinter to provide an interactive experience.

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

#### Function to select and populate data from the 'Order_Records' table into the 'data_lst_eff' global list
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


#### Function to select and populate data from the 'setting_property' table into the 'setting_lst' global list
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


#### Add new orders
    def new_order_ex():
    global new_order_number
    n_order_num = new_order_number
    n_customer = En_Customername.get()
    n_product = product.get()
    n_qty = float(En_Order_Qty.get())
    n_record = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    n_due = collect_time_str[0]
    # print(f'''
    #        INSERT INTO Order_record (Order_Number, Customer, Product,
    #        Order_Quantity, Record_Datetime, Due_Datetime) VALUES ({n_order_num}, {n_customer},
    #        {n_product}, {n_qty}, {n_record}, {n_due})
    #        ''')
    # print(type(n_order_num), type(n_customer), type(n_product), type(n_qty), type(n_record), type(n_due))
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
    except Exception as e:
        print("Error -> {}".format(e))
### User Interfaces

#### Main Window
    root = Tk()  # Main window creation
    root.title("Order Records")  # Set window title
    root.option_add("*Font", "arial 11")  # Global font setting


#### Title
    Title_frame = Frame(root, bg='blue violet')  # Creating a frame for the title 
    Title_frame.grid(row=0, column=0, columnspan=9, sticky='news')  # Placing the frame in the grid layout
    Title_Label = Label(Title_frame, text="New orders")  # Creating a label for the title
    Title_Label.pack(padx=10, pady=10, side=LEFT)  # Packing the label within the frame with padding and alignment


#### Subtitle
    # Creating labels for each subtitle item 
    Subtitle_1 = ["Order NO.", "Customer", "Product", "Order Quantity", "Record datetime", "Due datetime"]

    # placing them in the grid layout
    for e, i in enumerate(Subtitle_1):
        Label(root, text=i, bg="magenta").grid(row=1, column=e, padx=1, sticky='news')


####   Customer name 
    Customer_Name = StringVar()
    En_Customername = Entry(root, textvariable=Customer_Name)
    En_Customername.grid(row=2, column=(Subtitle_1.index("Customer")))

#### Order Quantity
    Order_Qty = DoubleVar()
    En_Order_Qty = Entry(root, textvariable=Order_Qty, width=13)
    En_Order_Qty.grid(row=2, column=(Subtitle_1.index("Order Quantity")))

#### Order Number 
    # Autogenerated Data and Read-Only
    if Data_list == []:
        new_order_number = 0
    else:
        new_order_number = (Data_list[-1][0]) + 1

    def order_number():
        # Function to display the order number
        Order_Num = Label(root, text=(new_order_number), bg="plum")
        Order_Num.grid(row=2, column=(Subtitle_1.index("Order NO.")))

    order_number()

#### Record Time
    currentDT = datetime.datetime.now()
    Date_Record = Label(root, text=(currentDT.strftime("%Y-%m-%d %H:%M:%S")), bg="plum")
    Date_Record.grid(row=2, column=(Subtitle_1.index("Record datetime")))

#### Subwindow - Calendar
    collect_time_str = [0]

    def calendar():
        # Function to create a calendar interface
        root2 = Tk()
        root2.title("Calendar")
        root2.option_add("*Font", "consolas 15")

        # Function to submit selected date
        def date_submit(e):
            collect_date = datetime.date(int(year.get()), int(month.get()), int(day.get()))
            collect_time = datetime.time(int(hour.get()), int(minute.get()), int(sec.get()))
            collect_time_print = f"{collect_date} {collect_time}"
            collect_time_str.insert(0, f"{collect_date} {collect_time}")
            Due_Time = Label(root, text=collect_time_print, bg="plum")
            Due_Time.grid(row=2, column=(Subtitle_1.index("Due datetime")))

        # Title
        title = ["Day", "Month", "Year", "  ", "Hour", "Minute", "Sec"]
        for e, i in enumerate(title):
            Label(root2, text=i).grid(row=0, column=e, sticky=W)

        # Comboboxes for date and time selection
        currentdate = datetime.datetime.now()
        day = ttk.Combobox(root2, values=list(range(1, 32)), width=3)
        day.grid(row=1, column=title.index("Day"))
        day.current(currentdate.day - 1)
        month = ttk.Combobox(root2, values=list(range(1, 13)), width=3)
        month.grid(row=1, column=title.index("Month"))
        month.current(currentdate.month - 1)
        year = ttk.Combobox(root2, values=list(range(2019, 2030)), width=5)
        year.grid(row=1, column=title.index("Year"))
        year.current(1)  # Static value
        hour = ttk.Combobox(root2, values=list(range(0, 25)), width=3)
        hour.grid(row=1, column=title.index("Hour"))
        hour.current(12)
        minute = ttk.Combobox(root2, values=list(range(0, 61)), width=3)
        minute.grid(row=1, column=title.index("Minute"))
        minute.current(0)
        sec = ttk.Combobox(root2, values=list(range(0, 61)), width=3)
        sec.grid(row=1, column=title.index("Sec"))
        sec.current(0)

        # Submit button
        submit = Button(root2, text="Submit", bg='cornsilk')
        submit.grid(row=1, column=len(title) + 1, padx=10)
        submit.bind("<Button-1>", date_submit)

