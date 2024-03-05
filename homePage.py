"""
Filename: homePage.py
Description: This script serves as the home page to access other module of a program.
Author: Dumri Ketupanya
Date created: June 8, 2017
"""

# import required modules =====================================================================================
from tkinter import *
import sqlite3
import os

# User Interface Section =======================================================================================
root = Tk()
root.title("Operation management V1.0")
root.option_add("*Font","arial 20")

Label(root,text="Welcome!", bg='deep sky blue').grid(row=0,column=0,sticky="news",ipady=10)

Portal_frame = Frame(root, bg='green')
Portal_frame.grid(row=1,column=0)

def bom():
    os.system("BOM.py")
def new_order():
    os.system("OrderRecord.py")
def mps():
    os.system("MPS.py")
def mrp():
    os.system("MRP.py")
def purchased_rec():
    os.system("PurchaseRecords.py")
def inventory():
    os.system("InventoryManagement.py")
def get_data():
    os.system("getdata.py")

Button(Portal_frame, text='Bill of Materials (BOM)',command=bom).pack(fill=X,padx=10,pady=10)
Button(Portal_frame, text='New Order',command=new_order).pack(fill=X,padx=10,pady=10)
Button(Portal_frame, text='Purchase records', command=purchased_rec).pack(fill=X,padx=10,pady=10) 
Button(Portal_frame, text='Inventory Management', command=inventory).pack(fill=X,padx=10,pady=10) 
Button(Portal_frame, text='Master Plan Schedule (MPS)',command=mps).pack(fill=X,padx=10,pady=10) 
Button(Portal_frame, text='Materials Requirement Plan (MRP)', command=mrp).pack(fill=X,padx=10,pady=10) 
Button(Portal_frame, text='Get data files', command=get_data).pack(fill=X,padx=10,pady=10)

root.mainloop()