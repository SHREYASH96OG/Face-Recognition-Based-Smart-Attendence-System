# -*- coding: utf-8 -*-
"""
Created on Tue March 12 11:41:26 2023

@author: G12
"""
import tkinter  as tk 
from tkinter import * 
import sqlite3
my_conn = sqlite3.connect('face.db')
###### end of connection ####

##### tkinter window ######
import tkinter  as tk 
from tkinter import * 
my_w = tk.Tk()
my_w.geometry("400x400") 

r_set=my_conn.execute('''SELECT * from user''');
i=0 # row value inside the loop 
for student in r_set: 
    for j in range(len(student)):
        e = Entry(my_w, width=10, fg='black') 
        e.grid(row=i, column=j) 
        e.insert(END, student[j])
    i=i+1
my_w.mainloop()