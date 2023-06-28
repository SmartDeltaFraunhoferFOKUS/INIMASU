
from tkinter import *
from tkinter import ttk

widget_main = Tk()
widget_main.title("INIMASU")
widget_main.geometry("800x600")
widget_main.iconbitmap("INIMASU_Logo.ico")

StringVar_repository_URI = StringVar()

Label_Combobox_repository_URI = Label(widget_main, text="Repository URI")
Label_Combobox_repository_URI.grid(column=0, row=0)

Combobox_repository_URI = ttk.Combobox(widget_main, textvariable=StringVar_repository_URI)
Combobox_repository_URI["values"] = ("https://github.com/vaadin/flow", "https://github.com/vaadin/hilla", "https://github.com/vaadin/flow-components", "https://github.com/vaadin/web-components")
Combobox_repository_URI["width"] = 120
StringVar_repository_URI.set("https://github.com/vaadin/flow")

Combobox_repository_URI.grid(column=0, row=1)

Button_ReadIssuesInLocalDatabase = Button(widget_main, text="Read repository in local database", width=40)
Button_ReadIssuesInLocalDatabase.grid(column=0, row=3)
Button_AnalyzeIssuesInLocalDatabase = Button(widget_main, text="Analyze issues in local database", width=40)
Button_AnalyzeIssuesInLocalDatabase.grid(column=0, row=4)
Button_RemoveLocalDatabase = Button(widget_main, text="Remove local database", width=40)
Button_RemoveLocalDatabase.grid(column=0, row=5)

widget_main.mainloop()