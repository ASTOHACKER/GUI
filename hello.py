import tkinter as tk
from tkinter import ttk
import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pythonwork_014"
)

columns = ("StudentID", "StudentName", "StudentLastName", "Age")
cursor = database.cursor()

insert_row = "StudentName, StudentLastName, Age"


def insert_command():
    EntryName = StudentName_Entry.get()
    EntryLastName = StudentLastName_Entry.get()
    EntryAge = Age_Entry.get()

    Query = f"INSERT INTO studentinfo ({insert_row}) VALUES (%s, %s, %s)"
    cursor.execute(Query, (EntryName, EntryLastName, EntryAge))

    database.commit()
    update_treeview()


def delete_command():
    selection = view.selection()
    if selection:
        item_id = selection[0]
        cursor.execute("DELETE FROM studentinfo WHERE StudentID = %s", (view.item(item_id, 'values')[0],))
        database.commit()
        update_treeview()


def edit_command():
    selection = view.selection()
    if selection:
        item_id = selection[0]
        # Retrieve existing data
        existing_data = view.item(item_id, 'values')

        # Clear entry widgets
        clear_entry_widgets()

        # Populate entry widgets with existing data for editing
        StudentName_Entry.insert(0, existing_data[1])
        StudentLastName_Entry.insert(0, existing_data[2])
        Age_Entry.insert(0, existing_data[3])

        # Disable the Insert and Edit buttons while editing
        Insert_button['state'] = 'disabled'
        edit_button['state'] = 'disabled'
        delete_button['state'] = 'disabled'
        update_button['state'] = 'normal'


def apply_edit_changes():
    selection = view.selection()
    if selection:
        item_id = selection[0]
        EntryName = StudentName_Entry.get()
        EntryLastName = StudentLastName_Entry.get()
        EntryAge = Age_Entry.get()

        # Update the entry in the Treeview
        view.item(item_id, values=(view.item(item_id, 'values')[0], EntryName, EntryLastName, EntryAge))

        # Clear entry widgets
        clear_entry_widgets()

        # Enable the Insert and Edit buttons after applying changes
        Insert_button['state'] = 'normal'
        edit_button['state'] = 'normal'
        update_button['state'] = 'normal'


def clear_entry_widgets():
    StudentName_Entry.delete(0, tk.END)
    StudentLastName_Entry.delete(0, tk.END)
    Age_Entry.delete(0, tk.END)


def update_treeview():
    cursor.execute("SELECT * FROM studentinfo")
    records = cursor.fetchall()

    for deldata in view.get_children():
        view.delete(deldata)

    for i, datarow in enumerate(records):
        tags = ('evenrow', 'oddrow')[i % 2]
        view.insert('', 'end', values=datarow, tags=tags)

    if view.get_children():
        view.selection_set(view.get_children()[0])  # Auto Selection
        delete_button['state'] = 'normal'
    else:
        delete_button['state'] = 'disable'


# Add a function to handle the search
def search_command():
    search_query = search_entry.get()
    if search_query:
        cursor.execute(
            "SELECT * FROM studentinfo WHERE StudentID LIKE %s OR StudentName LIKE %s OR StudentLastName LIKE %s OR Age LIKE %s",
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        records = cursor.fetchall()

        # Update the Treeview with the search results
        update_treeview_with_search(records)
    else:
        # If the search query is empty, show all records
        update_treeview()


# Add a function to update the Treeview with search results
def update_treeview_with_search(records):
    view.delete(*view.get_children())  # Clear existing data

    for i, datarow in enumerate(records):
        tags = ('evenrow', 'oddrow')[i % 2]
        view.insert('', 'end', values=datarow, tags=tags)

    if view.get_children():
        view.selection_set(view.get_children()[0])  # Auto Selection
        delete_button['state'] = 'normal'
    else:
        delete_button['state'] = 'disable'


# Add a function to handle sorting options
def sort_command(event):
    selected_option = sort_var.get()

    # Handle sorting logic based on the selected option
    if selected_option == "StudentID":
        # Sort by StudentID
        cursor.execute("SELECT * FROM studentinfo ORDER BY StudentID")
    elif selected_option == "StudentName":
        # Sort by StudentName
        cursor.execute("SELECT * FROM studentinfo ORDER BY StudentName")
    elif selected_option == "StudentLastName":
        # Sort by StudentLastName
        cursor.execute("SELECT * FROM studentinfo ORDER BY StudentLastName")
    elif selected_option == "Age":
        # Sort by Age
        cursor.execute("SELECT * FROM studentinfo ORDER BY Age")

    records = cursor.fetchall()

    # Update the Treeview with sorted results
    update_treeview_with_search(records)


# Make tkinter
root = tk.Tk()

# LabelName
StudentName_label = ttk.Label(root, text="กรอกชื่อ :")
StudentName_label.grid(row=0, column=0, padx=5, pady=5)

# MakeEntryForname
StudentName_Entry = ttk.Entry(root)
StudentName_Entry.grid(row=0, column=1, padx=5, pady=5)

# LabelLastName
StudentLastName_label = ttk.Label(root, text="กรอกนามสกุล :")
StudentLastName_label.grid(row=1, column=0, padx=5, pady=5)

# MakeEntryForLastname
StudentLastName_Entry = ttk.Entry(root)
StudentLastName_Entry.grid(row=1, column=1, padx=5, pady=5)

# LabelAge
Age_label = ttk.Label(root, text="อายุ :")
Age_label.grid(row=2, column=0, padx=5, pady=5)

# Entry Age
Age_Entry = ttk.Entry(root)
Age_Entry.grid(row=2, column=1, padx=5, pady=5)

# Sorting Options
sort_label = ttk.Label(root, text="เรียงตาม:")
sort_label.grid(row=0, column=2, padx=5, pady=5)

sort_options = ["StudentID", "StudentName", "StudentLastName", "Age"]
sort_var = tk.StringVar()

sort_menu = ttk.Combobox(root, textvariable=sort_var, values=sort_options)
sort_menu.grid(row=0, column=3, padx=5, pady=5)
sort_menu.set(sort_options[0])  # Set default option

# Bind an event to the sorting option menu
sort_menu.bind("<<ComboboxSelected>>", sort_command)

# Insert Button
Insert_button = ttk.Button(root, text="บันทึก", command=insert_command)
Insert_button.grid(row=3, column=0, pady=10)

delete_button = ttk.Button(root, text="ลบ", command=delete_command)
delete_button.grid(row=3, column=1, pady=10)
delete_button['state'] = 'disabled'

# Edit Button
edit_button = ttk.Button(root, text="เลือก", command=edit_command)
edit_button.grid(row=3, column=2, pady=10)

# Update Button
update_button = ttk.Button(root, text="แก้ไข", command=apply_edit_changes)
update_button.grid(row=3, column=3, pady=10)
update_button['state'] = 'disabled'

# Label and Entry for Search
search_label = ttk.Label(root, text="ค้นหา:")
search_label.grid(row=0, column=4, padx=5, pady=5)

search_entry = ttk.Entry(root)
search_entry.grid(row=0, column=5, padx=5, pady=5)

search_button = ttk.Button(root, text="ค้นหา", command=search_command)
search_button.grid(row=0, column=6, padx=5, pady=5)

# Show Data
view = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    view.heading(col, text=col, anchor="center")

# Configure tags for alternating row colors
view.tag_configure('evenrow', background='#f0f0f0')  # Light gray
view.tag_configure('oddrow', background='#e0e0e0')  # Slightly darker gray

view.grid(row=4, column=0, columnspan=7, pady=10)

# Update Data
update_treeview()

# Start the Tkinter main loop
if __name__ == "__main__":
    root.mainloop()

# Close resources using try...finally
try:
    cursor.close()
    database.close()
    print("Database has closed successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    print("การเชื่อมต่อมีปัญหา")