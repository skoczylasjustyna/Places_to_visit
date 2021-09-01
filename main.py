import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3

############# Functions section ########################################################################

#part for creating table if it doesn't exist

#cursor.execute("""CREATE TABLE places (
#               name text,
 #               country text,
 #               address text,
 #               extra_info text,
#                visited integer)"""

sub_var = 0
# showing entry frames when user want's to add new place to the list
def show_entry():
    sub_var = 0

    submit_heading1.grid(row=2, columnspan=3, pady=5)
    submit_heading2.grid(row=3, columnspan=3, pady=10)

    # Packing fields
    name.grid(row=4, column=1)
    country.grid(row=5, column=1)
    city.grid(row=6, column=1)
    extra.grid(row=7, column=1)

    name_entry.grid(row=4, column=2)
    country_entry.grid(row=5, column=2)
    city_entry.grid(row=6, column=2)
    extra_entry.grid(row=7, column=2)
    save_submit_btn.grid(row=9, column=1, columnspan=2, padx=5, ipadx=179)

#showing list of places added to bucket list
def query():
    connection = sqlite3.connect('places_to_go.db')
    cursor = connection.cursor()
    cursor.execute("SELECT *, oid FROM places")
    records = cursor.fetchall()

    # Showing results in form of string
    print_records = ''
    for record in records:
        print_records += str(record[-1]) + ". " + str(record[0]) + " " + str(record[1]) + ", city: " + str(
            record[2]) + ", extra info: " + str(record[3]) + ", visited: " + str(record[4])+ "\n"

    query_label = Label(root, text=print_records, bg="#12263b", foreground='white')
    query_label.grid(row=16, column=1, columnspan=2)

    connection.commit()
    connection.close()

# updating query so that it's marked as visited = 1 (if not visited = 0)
def updt_var():
    global var
    var += 1
    # after clicking button entry appears, user can type ID of place where he/she was already - to check ID user should click button ,,Show all''
    if var != 0:
        visited_id.grid(row=11, column=1)
        visited_id_entry.grid(row=11, column=2)
        id_del = visited_value.get()

        connection = sqlite3.connect('places_to_go.db')
        cursor = connection.cursor()

        cursor.execute("""UPDATE places SET visited = :visited
                    WHERE oid = :oid""",
                        {'oid': id_del,
                        'visited': 1
                        })

        visited_value.set(0)

        connection.commit()
        connection.close()
        query()

# chosing random place to go from places marked 0 - not visited before
def chose():
    connection = sqlite3.connect('places_to_go.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * from places WHERE visited=0 ORDER BY RANDOM() LIMIT 1")
    print_record = ""
    record = cursor.fetchone()

    for x in range(len(record)):
        print_record = "Next place you should visit is: " + str(record[0])

    chose_label = Label(root, text=print_record, bg="#12263b", foreground='white')
    chose_label.grid(row=14, column=1, columnspan=2, pady=10)

    connection.commit()
    connection.close()

# function to save new places
def save_submit():
    global sub_var
    sub_var += 1
    #after clicking ,,save'' button - adding a new record
    if sub_var != 0:
        connection = sqlite3.connect('places_to_go.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO places VALUES (:name, :country, :address, :extra, :visited)",
                        {
                            'name': name_value.get(),
                            'country': country_value.get(),
                            'address': city_value.get(),
                            'extra': extra_value.get(),
                            'visited': 0  # 0 stands for not visited, 1 - visited places
                        })
        connection.commit()
        connection.close()

        # clearing entries after submitting
        country_entry.delete(0, END)
        name_entry.delete(0, END)
        city_entry.delete(0, END)
        extra_entry.delete(0, END)

########################Main app#######################################################################
root = Tk()
root.geometry("402x600")
root.resizable(True,True)
root.title("Places to go - bucket list")
root.configure(bg='#12263b')

connection = sqlite3.connect('places_to_go.db')
cursor = connection.cursor()
#cursor.execute("DELETE from places")

# Heading
heading = Label(root, text="Places to visit", font=("Bebas Neue", 25), bg="#12263b", foreground = 'white').grid(row=0, column=1, columnspan=2, pady=12)
info = Label(root, text="What do you want to do today?", font=("Work Sans Regular",11), bg="#12263b", foreground = 'white').grid(row=1, column=1,columnspan=2, pady=5)

# headings for submit section
submit_heading1 = Label(root, text="Planning future trip ", font=("Bebas Neue", 15), bg="#12263b",
                        foreground='white')
submit_heading2 = Label(root, text="Details about place you want to visit : ", bg="#12263b",
                        foreground='white')

var = 0 # variable which works with mark as visited button
visited_value = tk.IntVar()
visited_id = Label(root, text="ID of visited place: ", bg="#12263b", foreground='white')
visited_id_entry = tk.Entry(root, textvariable=visited_value, width=45)

# labels for submit section
name = Label(root, text="Name: ", bg="#12263b", foreground='white')
country = Label(root, text="Country: ", bg="#12263b", foreground='white')
extra = Label(root, text="Extra info: ", bg="#12263b", foreground='white')
city = Label(root, text="City: ", bg="#12263b", foreground='white')

# Variables for storing data
name_value = StringVar()
country_value = StringVar()
city_value = StringVar()
extra_value = StringVar()

# Creating & packing entry fields
name_entry = tk.Entry(root, textvariable=name_value, width=53)
country_entry = tk.Entry(root, textvariable=country_value, width=53)
city_entry = tk.Entry(root, textvariable=city_value, width=53)
extra_entry = tk.Entry(root, textvariable=extra_value, width=53)

#buttons section
submit_btn =Button(text="I have a new trip in mind",bg="white",  command=show_entry)
submit_btn.grid(row=10, column=1, columnspan=2, padx=5, pady=1, ipadx=126)
query_btn = Button(text="Show all", bg = "white",fg = "#12263b",  command=query)
query_btn.grid(row=12, column=1, columnspan=2,  padx=5, ipadx=169)
updt_btn = Button(text="Mark place as visited ", bg="white", fg = "#12263b", command=updt_var)
updt_btn.grid(row=13, column=1, columnspan=2, padx=5, ipadx=135)
chose_btn = Button(text="Undecided where to go? Let me chose for you", bg="white", fg = "#12263b", command=chose)
chose_btn.grid(row=15, column=1, columnspan=2, padx=5, ipadx=70)

#button save only appears when option submit was chosen
save_submit_btn = Button(text="Save",  bg="white", fg = "#12263b", command=save_submit)

connection.commit()
connection.close()
root.mainloop()