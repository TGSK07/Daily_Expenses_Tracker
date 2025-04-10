# import modules 
from tkinter import *
from tkinter import ttk,simpledialog
import datetime as dt
import pandas as pd 
from csv import writer
from tkinter import messagebox


# functions
def saveRecord():
    entry_data = [item_name.get(), item_amt.get(), transaction_date.get()]
    try:
        data = pd.read_csv('expenses.csv',header=None)
        data.loc[len(data.index)] = entry_data
        data.to_csv("expenses.csv",index=None,header=None)
    except:
        with open('expenses.csv','w') as f:
            data = writer(f)
            data.writerow(entry_data)
        fetch_records()
    

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    try:
        data = pd.read_csv("expenses.csv",header=None)
        count = 1
        for i in data.index:
            screen.insert(parent='', index='0', iid=count, values=(count,data[0][i], data[1][i], data[2][i]))
            count += 1
        screen.after(400, refreshData)
    except:
        pass




def balance():
    bal = simpledialog.askstring(title="Balance",prompt='Enter Your Initial Balance')
    with open('balance.txt','w') as f:
        if bal!=None:
            f.write(bal)
        else:
            f.write('0')

def totalBalance():
    total = 0
    bal = 0
    with open('balance.txt','r') as f:
        bal = float(f.read())
    try:
        data = pd.read_csv("expenses.csv",header=None)
        for i in data.index:
            total += float(data[1][i])
    except:
        pass
        
    messagebox.showinfo('Current Balance: ', f"Total Expense: {total} \nBalance Remaining: {bal - total}")


def refreshData():
    for item in screen.get_children():
      screen.delete(item)
    fetch_records()
   
def deleteRow():
    try:
        data = pd.read_csv("expenses.csv",header=None)
        try:
            data = data.drop(data.index[-1])
        except:
            data = data.drop(data.index[0])
        data.to_csv('expenses.csv',index=False,header=None)
    except:
        pass
    refreshData()

# create tkinter object
ws = Tk()
ws.title('Daily Expenses')
photo = PhotoImage(file = "budget.png")
ws.iconphoto(False, photo)

f = open('balance.txt','r+')



# variables
f = ('Times new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widget
f2 = Frame(ws)
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets 
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


# Action buttons
cur_date = Button(
    f1, 
    text='Current Date', 
    font=f, 
    bg='#04C4D9', 
    command=setDate,
    width=15
    )

submit_btn = Button(
    f1, 
    text='Save Record', 
    font=f, 
    command=saveRecord, 
    bg='#42602D', 
    fg='white'
    )

clr_btn = Button(
    f1, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries, 
    bg='#D9B036', 
    fg='white'
    )

quit_btn = Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='#D33532', 
    fg='white'
    )

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='#486966',
    command=totalBalance
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=None
)

bal_btn = Button(
    f1, 
    text='Balance',
    bg='#C2BB00',
    command=balance,
    font=f
)

del_btn = Button(
    f1, 
    text='Delete',
    bg='#BD2A2E',
    command=deleteRow,
    font=f
)

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
bal_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
screen = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
screen.pack(side="left")

# add heading to treeview
screen.column(1, anchor=CENTER, stretch=NO, width=70)
screen.column(2, anchor=CENTER)
screen.column(3, anchor=CENTER)
screen.column(4, anchor=CENTER)
screen.heading(1, text="Serial no")
screen.heading(2, text="Item Name", )
screen.heading(3, text="Item Price")
screen.heading(4, text="Purchase Date")



# style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbarqqa
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=screen.yview)
scrollbar.pack(side="right", fill="y")
screen.config(yscrollcommand=scrollbar.set)

# calling function 
fetch_records()

# infinite loop
ws.mainloop()