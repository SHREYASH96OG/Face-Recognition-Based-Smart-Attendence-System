"""
Template classes for adding and editing the database items
"""
import logging
from tkinter import Toplevel, StringVar, Label, Frame, OptionMenu, Button, IntVar, Entry, messagebox
class AddEditEntry(Frame):
    """
    Template widget for adding/editing the entry
    """
    def __init__(self, parent, possiblecats):
        Frame.__init__(self, parent)
        self.__months = ("January", "February", "March", "April", "May",
                         "June", "July", "August", "September", "October",
                         "November", "December")
        self.__month_selected = StringVar(self, value=self.__months[0])
        self.__cat_selected = StringVar(self, value="Other")
        self.__name_var = StringVar(self)
        self.__day_var = IntVar(self, value=1)
        self.__year_var = IntVar(self, value=2000)
        self.__desc_var = StringVar(self)

        l_name = Label(self, text="Name:")
        self.__e_name = Entry(self, textvariable=self.__name_var)
        l_day = Label(self, text="Day:")
        self.__e_day = Entry(self, textvariable=self.__day_var)
        l_month = Label(self, text="Month:")
        self.__om_month = OptionMenu(self, self.__month_selected,
                                        *self.__months)
        l_year = Label(self, text="Year:")
        self.__e_year = Entry(self, textvariable=self.__year_var)
        l_desc = Label(self, text="Description")
        self.__t_desc = Entry(self, textvariable=self.__desc_var)
        l_cat = Label(self, text="Category")
        self.__om_cat = OptionMenu(self, self.__cat_selected, *possiblecats)

        l_name.grid(row=0, column=0)
        self.__e_name.grid(row=0, column=1)
        l_day.grid(row=1, column=0)
        self.__e_day.grid(row=1, column=1)
        l_month.grid(row=2, column=0)
        self.__om_month.grid(row=2, column=1)
        l_year.grid(row=3, column=0)
        self.__e_year.grid(row=3, column=1)
        l_desc.grid(row=4, column=0)
        self.__t_desc.grid(row=4, column=1)
        l_cat.grid(row=5, column=0)
        self.__om_cat.grid(row=5, column=1)

    def set_values(self, day, monthint, year, name, desc, cat):
        """
        Sets the values of the
        entries with the data given"
        """
        # makes it so that the value of the month list matches with the month number
        monthint -= 1
        self.__name_var.set(name)
        self.__day_var.set(day)
        self.__month_selected.set(self.__months[monthint])
        self.__year_var.set(year)
        self.__desc_var.set(desc)
        self.__cat_selected.set(cat)

    def get_values(self):
        """
        Returns pre-formated values
        """
        month = self.__months.index(self.__month_selected.get()) + 1
        date = "{self.__day_var.get()}.{month}.{self.__year_var.get()}"
        datatoreturn = (
            self.__name_var.get(),
            date,
            self.__desc_var.get(),
            self.__cat_selected.get()
            )
        return datatoreturn

class AddEditWindow(Toplevel):
    """
    tkinter add/edit menu popup
    """

    def __init__(self, possiblecategories):
        Toplevel.__init__(self)
        self.wm_title("Add Entry")
        self.__the_entry = AddEditEntry(self, possiblecategories)
        self.__b_ok = Button(self, text="Save", command=self.__closeWindow)
        self.__the_entry.pack()
        self.__b_ok.pack()

    def __closeWindow(self):
        """
        Closes the window
        """
        self.destroy()

    def get_data(self):
        """
        Returns TUPLE of (name, date(d,M,yyyy), desc, cat)
        """
        return self.__the_entry.get_values()
    
    def load_data(self, day, monthint, year, name, desc, cat):
        self.wm_title("Edit Entry")
        logging.debug("Loading data: {day, monthint, year, name, desc, cat}")
        self.__the_entry.set_values(day, monthint, year, name, desc, cat)

class AddCategory(Toplevel):
    """
    tkinter popup window to add a category
    """
    def __init__(self, categories):
        self.__entry_formated = None
        self.__categories = categories
        Toplevel.__init__(self)
        self.wm_title("Add Category")
        self.__entry = Entry(self)
        self.__confirm = Button(self, text="Confirm", command=self.confirm)
        self.__entry.pack()
        self.__confirm.pack()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        """
        Allows the user to choose whether to save or not when clicking the close button
        """
        if self.__entry.get() == "":
            self.destroy()
        else:
            dialog = messagebox.askyesnocancel("Leave without saving","Do you want to save before leaving?")
            if dialog:
                logging.debug("user wants to save before leaving")
                if self.confirm() != None:
                    self.confirm()
            elif dialog == None:
                logging.debug("User wants to stay")
            else:
                logging.debug("User wants to leave without saving")
                self.destroy()

    def get_data(self):
        """
        Returns the user data
        """
        return self.__entry_formated

    def confirm(self):
        """
        gets the user entry and compares it to the ones given
        if it is present in the ones given displays error message
        """
        if self.__entry.get().capitalize() not in self.__categories:
            self.__entry_formated = self.__entry.get().capitalize()
            self.destroy()
        else:
            logging.error("Category already exists")
            messagebox.showerror("Already exists", "The category you chose already exists!")
