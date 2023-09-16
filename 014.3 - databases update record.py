
#using databases with tkinter

import sqlite3 #import the database module, built in with python
from tkinter import *
import time

root = Tk()
root.title("Tkinter & databases")
root.geometry("355x600")

#--------------------------------------------------------

#create db or connect to one
conn = sqlite3.connect('address_book.db') #connect to a given db

# create cursor, that will retrieve info from db
c = conn.cursor()

'''
#create table
# this will create a db file in the dir where the current script is stored
c.execute("""CREATE TABLE addresses(
        first_name text,
        last_name text,
        address text,
        city text,
        state text,
        contact_num integer
        )""")
# this only need to be executed once, after which we can just comment out
 '''

#----------------------------------------------------------------

# add items to db function
def submit():
    conn = sqlite3.connect('address_book.db') #connect to a given db
    c = conn.cursor()    # create cursor, that will retrieve info from db

    #insert into table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :addr, :cty, :st, :c_num)",
              # create a dict for key/value pairs
              {
                  'f_name': f_name.get(),
                  'l_name': l_name.get(),
                  'addr': addr.get(),
                  'cty': cty.get(),
                  'st': st.get(),
                  'c_num': c_num.get()
              }
              
              )

    conn.commit()    # any changes to db, need to be committed
    conn.close()    # need to close the connection when done

    f_name.delete(0,END) # clear text boxes
    l_name.delete(0, END)
    addr.delete(0, END)
    cty.delete(0, END)
    st.delete(0, END)
    c_num.delete(0, END)

def retrieve():
    conn = sqlite3.connect('address_book.db') #connect to a given db
    c = conn.cursor()    # create cursor, that will retrieve info from db

    #query the db
    c.execute("SELECT *, oid FROM addresses") # oid is auto created by sqlite as a primary key, but we have to explicitly refer to it 
    records = c.fetchall() # fetches all records

    # loop through results 
    print_records = ''
    for record in records:
        print_records += str(record[0]) + ' ' + str(record[1]) + ': ' + str(record[6]) + ' ' + str(record[2]) + ', ' + str(record[3]) + ', ' + str(record[4]) + ', ' + str(record[5]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)
    conn.commit()    # any changes to db, need to be committed
    conn.close()    # need to close the connection when done


#delete record
def delete():
    conn = sqlite3.connect('address_book.db') #connect to a given db
    c = conn.cursor()    # create cursor, that will retrieve info from db

    #delete a record
    c.execute("DELETE FROM addresses WHERE oid= " + id_box.get())

    conn.commit()    # any changes to db, need to be committed
    conn.close()    # need to close the connection when done


# update is used by edit(), it will save the updated address (ie edit() calls this when it wants to save / update)
def update():
    conn = sqlite3.connect('address_book.db') #connect to target db
    c = conn.cursor() # create cursor to interact with db
    
    record_id = id_box.get()
    
    # update the addresses table and set x to equal y, where the primary kety matches
    c.execute("""UPDATE addresses SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        contact_num = :contact

        WHERE oid = :oid""",
        {
            'first': f_name_editor.get(),
            'last': l_name_editor.get(),
            'address': addr_editor.get(),
            'city': cty_editor.get(),
            'state': st_editor.get(),
            'contact': c_num_editor.get(),
            'oid': record_id
        }
        
        )

    confirm_label = Label(editWin, text='record updated')
    confirm_label.grid(row=7, columnspan=2)

    conn.commit()    # any changes to db, need to be committed
    conn.close()    # need to close the connection when done
        
    #editWin.destroy() # close the window
    
#edit a record
def edit():
    conn = sqlite3.connect('address_book.db') #connect to target db
    c = conn.cursor() # create cursor to interact with db
    
    # open a new window to edit the given record
    global editWin # to be used by update function
    editWin = Tk()
    editWin.title("Update a record")
    editWin.geometry("325x240")
    
    #global variables for text boxes - used in the update() function
    global f_name_editor
    global l_name_editor
    global addr_editor
    global cty_editor
    global st_editor
    global c_num_editor

    #create entry boxes in editor window
    f_name_editor = Entry(editWin, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10,3)) #use a tuple to pad; top and bottom pad-figures

    l_name_editor = Entry(editWin, width=30)
    l_name_editor.grid(row=1, column=1, padx=20, pady=3)

    addr_editor = Entry(editWin, width=30)
    addr_editor.grid(row=2, column=1, padx=20, pady=3)

    cty_editor = Entry(editWin, width=30)
    cty_editor.grid(row=3, column=1, padx=20, pady=3)

    st_editor = Entry(editWin, width=30)
    st_editor.grid(row=4, column=1, padx=20, pady=3)

    c_num_editor = Entry(editWin, width=30)
    c_num_editor.grid(row=5, column=1, padx=20, pady=3)


    # create labels in editor window
    f_name_label = Label(editWin, text='first name:')
    f_name_label.grid(row=0, column=0, padx=2, pady=(10,3))

    l_name_label = Label(editWin, text='last name:')
    l_name_label.grid(row=1, column=0, padx=2)

    addr_label = Label(editWin, text='address:')
    addr_label.grid(row=2, column=0, padx=2)

    cty_label = Label(editWin, text='city:')
    cty_label.grid(row=3, column=0, padx=2)

    st_label = Label(editWin, text='state:')
    st_label.grid(row=4, column=0, padx=2)

    c_num_label = Label(editWin, text='contact number:')
    c_num_label.grid(row=5, column=0, padx=2)

    #create save button - save edited record
    update_button = Button(editWin, text="Save & Update Record", command=update)
    update_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=90)

    record_id = id_box.get() # the given user id (record we want to amend)
    #query the db
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id) # select the address items of the given user id
    records = c.fetchall() # fetches all records

    #loop through results & add the address items to the corresponding text fields in the editor window, ie to update
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        addr_editor.insert(0, record[2])
        cty_editor.insert(0, record[3])
        st_editor.insert(0, record[4])
        c_num_editor.insert(0, record[5])

    conn.commit() # commit the changes to the db
    conn.close() # close the db connection


#----------------------------------------------------------------
#widgets:

# create text boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10,3)) #use a tuple to pad; top and bottom pad-figures

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20, pady=3)

addr = Entry(root, width=30)
addr.grid(row=2, column=1, padx=20, pady=3)

cty = Entry(root, width=30)
cty.grid(row=3, column=1, padx=20, pady=3)

st = Entry(root, width=30)
st.grid(row=4, column=1, padx=20, pady=3)

c_num = Entry(root, width=30)
c_num.grid(row=5, column=1, padx=20, pady=3)

id_box = Entry(root, width=36)
id_box.grid(row=9, column=1)

# create labels
f_name_label = Label(root, text='first name:')
f_name_label.grid(row=0, column=0, padx=2, pady=(10,3))

l_name_label = Label(root, text='last name:')
l_name_label.grid(row=1, column=0, padx=2)

addr_label = Label(root, text='address:')
addr_label.grid(row=2, column=0, padx=2)

cty_label = Label(root, text='city:')
cty_label.grid(row=3, column=0, padx=2)

st_label = Label(root, text='state:')
st_label.grid(row=4, column=0, padx=2)

c_num_label = Label(root, text='contact number:')
c_num_label.grid(row=5, column=0, padx=2)

id_box_label = Label(root, text='id number')
id_box_label.grid(row=9, column=0)

# create submit button
submit_button = Button(root, text="Add record to database", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#create query button
query_button = Button(root, text="Show all records", command=retrieve)
query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=118)

#create delete button
delete_button = Button(root, text="Delete record from database", command=delete)
delete_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=87)

# create edit button
edit_button = Button(root, text="Edit record from database", command=edit)
edit_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=93.25)

#-------------------------------------------------------------

# any changes to db, need to be committed
conn.commit()

# need to close the connection when done
conn.close()

root.mainloop()