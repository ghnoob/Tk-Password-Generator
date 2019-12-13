"""App that auto-generates password with the secrets module.

Generated passwords can have 8-50 characters, and be composed of
uppercase letters, lowercase letters, digits, and symbols
"""
__author__ = "Rodrigo Pietnechuk"

import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import secrets
import string
from i18n import get_lang

class MainApplication:
    """Contains all widgets, their configs and their functionalities.
    
    Parameters:
        master (tkinter.Tk): the base widget of the app.
    """
    
    def __init__(self, master):
        """Class initializator.
        
        Creates and configures the widgets.

        Parameters:
            master (tkinter.Tk): the base widget of the app

        Attibutes:
            include_low (tkinter.BooleanVar): controls wether the generated
            password has to contain lowercase ASCII letters (a-z) or not.
            True by default.  
            include_upp (tkinter.BooleanVar): controls wether the generated
            password has to contain uppercase ASCII letters (A-Z) or not.
            True by default.  
            include_num (tkinter.BooleanVar): controls wether the generated
            password has to contain ASCII digits (0-9) or not.
            True by default.  
            include_sym (tkinter.BooleanVar): controls wether the generated
            password has to contain ASCII symbols (defined by locale)
            or not. True by default.  
            password_lenght (tkinter.IntVar): the generated password lenght.
            8 by default.  
            password (tkinter.StringVar): the generated password.
        """
        global _
        # arguments
        self.master = master

        # attributes
        self.include_low = tk.BooleanVar(value=True)
        self.include_upp = tk.BooleanVar(value=True)
        self.include_num = tk.BooleanVar(value=True)
        self.include_sym = tk.BooleanVar(value=True)
        self.password_lenght = tk.IntVar(value=8)
        self.password = tk.StringVar()
        
        # calling methods
        _ = get_lang() # set language
        self.configure_widgets()
        self.create_widgets()
    
    def configure_widgets(self):
        """Config of the root widgets and creation of ttk styles."""
        # root config
        self.master.title("Tk Password Generator")
        self.master.resizable(False, False)
        self.master.config(bd=20)

        # styling
        s = ttk.Style()
        s.configure("TButton", font=("Consolas", 10), width=25, padding=1.5)
        s.configure("TCheckbutton", font=("Consolas",10))

    def create_widgets(self):
        """Calls methods that create different sections of the app."""
        self.create_upper_section()
        self.create_checkbox()
        self.create_password_lenght_section()
        self.create_lower_section()


    def create_upper_section(self):
        """Creates the widgets of the top section of the app."""
        ttk.Label(self.master, text="Tk Password Generator",
        font=("Consolas", 24, "bold") ).pack()

    
    def create_checkbox(self):
        """Creates the checkbox of the app.
        
        This checkbox allows the user to select what elements they
        want in the generates password: lowercase and uppercase letters,
        digits and symbols.  
        Having more elemets makes a password more secure.

        Clicking on any checkbutton calls a method that disables the
        password generation button if all of the checkbuttons are off,
        preventing the generation of empty passwords.
        """
        # frame to fit the widgets
        checkbox_frame = ttk.Frame()
        checkbox_frame.pack(anchor="w")

        # widgets
        
        # title label
        ttk.Label(checkbox_frame, text=_("The password must contain:"),
                  font=("Consolas",12)).pack(anchor="w")

        # checkbox
        ttk.Checkbutton(
            checkbox_frame,text=_("Lowercase letters"),
            variable=self.include_low, command=self.check_generate
            ).pack(anchor="w")
        ttk.Checkbutton(
            checkbox_frame, text=_("Uppercase letters"),
            variable=self.include_upp, command=self.check_generate
            ).pack(anchor="w")
        ttk.Checkbutton(
            checkbox_frame, text=_("Digits"),
            variable=self.include_num, command=self.check_generate
            ).pack(anchor="w")
        ttk.Checkbutton(
            checkbox_frame, text=_("Symbols"),
            variable=self.include_sym, command=self.check_generate
            ).pack(anchor="w")

    def create_password_lenght_section(self):
        """Creates the widgets of the password lenght select section.
        
        Allows the user to select the lenght in characters for the
        password.  
        Higher values make a password more secure.

        The password lenght is selected throught a spinbox. Accepted
        values are between 1 and 50.  
        It can be changed with the spinbox arrow or with the keyboard
        and the Enter key.  
        Doing the later triggers a method that prevents the input of
        invalid values as password lenght.
        """
        # frames
        lenght_frame = ttk.Frame(self.master)
        lenght_frame.pack(anchor="w")

        # title label
        ttk.Label(lenght_frame, text=_("Password lenght:"),
                  font=("Consolas",12)).grid(row=0, column=0)

        # spinbox to select password lenght
        spin = ttk.Spinbox(
            lenght_frame, from_=1, to=50, font=("Consolas", 10),
            justify="right",
            textvariable=self.password_lenght)
        spin.grid(row=0, column=1)
        spin.bind("<Return>", lambda event:self.check_password_lenght_value())

    
    def create_lower_section(self):
        """Creates the bottom section of the app.

        It includes a buttons to generate the passwords, copy them to
        the clipboard and save them as .txt files, and an entry field
        (read-only) to display the generated passwords.  
        Copy and save buttons are disabled by defalut and there are
        enabled only if the user generates a password to prevent
        copying and saving empty passwords.
        """
        # frame to fit widgets in
        lower_frame = ttk.Frame(self.master, borderwidth=10)
        lower_frame.pack()

        # generate password button
        self.genbutton = ttk.Button(
            lower_frame, text=_("Generate"),
            command=self.generate_password)
        self.genbutton.pack()
        
        # blank label to add space
        ttk.Label(lower_frame).pack()

        # generated passwords display
        ttk.Entry(lower_frame, width=52, font=("Consolas", 10),
                  state="readonly", cursor="", textvariable=self.password,
                  justify="center").pack()

        # copy to clipboard button
        self.copybutton = ttk.Button(
            lower_frame, text=_("Copy to clipboard"),
            state=["disabled"], command=self.copy_to_clipboard
            )
        self.copybutton.pack(side="left")
        
        # save as .txt button
        self.savebutton = ttk.Button(
            lower_frame, text=_("Save as .txt"),
            state=["disabled"], command=self.save_password)
        self.savebutton.pack(side="left")
         
         # blank label to add space
        ttk.Label(self.master, text=" ", font=("",5)).pack()

        # reset button
        ttk.Button(
            self.master, text="Reset", command=self.reset).pack()

    # gui functionalities
    def check_password_lenght_value(self):
        """Prevents the password lenght field to take an invalid value.
        
        Supported values are integers between 1 and 50.  
        If the value in the password lenght field is not an integer:
            if it is a float, it transforms it into an integer,  
            if it is another data type, it sets it to the default value.  
        If it is an integer:
            if it is lower than the min value, it sets it to the min,  
            if it is higher than the max value, it sets it to the max,  
            if it is in the supported range of values, it keeps that
            value.

        This method is called when the user presses the Enter key while
        editing the password lenght value or the password generation
        button.
        """
        
        try:
            # checks if the value is a number
            self.password_lenght.get()
        except:
            # if not it sets it to the default value
            self.password_lenght.set(8)
        
        else:
            # converts the value to int if it is a float
            if type(self.password_lenght.get()) is float:
                self.password_lenght.set(int(self.password_lenght.get()))

            # sets the password len to the allowed values if is it not.
            if self.password_lenght.get() < 1:
                self.password_lenght.set(1)
            elif self.password_lenght.get() > 50:
                self.password_lenght.set(50)

        finally:
            # takes the keyboard focus off the password lenght spinbox
            self.master.focus()


    def check_generate(self):
        """Prevents the generation of passwords without a sample.
        
        It triggers when any checkbutton of the checkbox is checked or
        unchecked.  
        Disables the password generation button if all the checkbuttons
        are unchecked.  
        Trying to generate a password with all the checkboxes unmarked
        will result in an exception.
        """

        if (self.include_low.get() or self.include_upp.get() or 
            self.include_num.get() or self.include_sym.get() ):

            self.genbutton.state(["!disabled"])

        else:
            self.genbutton.state(["disabled"])


    def generate_password(self):
        """Generates a random password.
        
        It randomly select characters from a string sample. The contents
        of the str sample are defined by what checkbuttons are marked.
        """
        password_sample = ""

        # add the characters to the sample if yhe checkboxes are on
        if self.include_low.get():
            password_sample += string.ascii_lowercase
        if self.include_upp.get(): 
            password_sample += string.ascii_uppercase
        if self.include_num.get():
            password_sample += string.digits
        if self.include_sym.get():
            password_sample += string.punctuation

        # prevents the password lenght value to be not valid
        self.check_password_lenght_value()

        # generates a list with all the characters
        password = [
            secrets.choice(password_sample) for i in range(
            self.password_lenght.get() ) ]

        # converts the list to a string
        password = "".join(password)
        self.password.set(password)

        # enable the copy and save password buttons
        self.savebutton.state(["!disabled"])
        self.copybutton.state(["!disabled"])

    def copy_to_clipboard(self):
        """Copies the generated password to the clipboard."""
        c = self.password.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(c)
        self.master.update()

    def save_password(self):
        """Saves the generated password in a .txt file."""
        
        file_ = tk.filedialog.asksaveasfile(
            filetypes=( ("Text file", "*.txt"), ),
            initialfile="password", defaultextension="*.txt"
        )

        # only saves of the uses doesn't press cancel
        if file_ is not None:
            file_.write(self.password.get())
            file_.close()

    def reset(self):
        """Resets all the password options to their default values."""
        self.include_low.set(True)
        self.include_upp.set(True)
        self.include_num.set(True)
        self.include_sym.set(True)
        self.password_lenght.set(8)
        self.password.set("")
        self.savebutton.state(["disabled"])
        self.copybutton.state(["disabled"])
        self.genbutton.state(["!disabled"])

# loop
if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()