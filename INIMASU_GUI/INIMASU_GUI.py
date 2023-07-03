
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pathlib
import sys
import json
import datetime
import os.path
import tkinter
sys.path.append(str(pathlib.Path().resolve()))

from ExtractJsonFromRepository.ExtractJsonFromRepository import get_issues_in_json
from JsonToIssue.JsonToIssue import jsonToIssue
from VisualizeIssues.VisualizeIssues import visualizeIssues


widget_main = Tk()
widget_main.title("INIMASU")
widget_main.geometry("800x600")
widget_main.iconbitmap("INIMASU_Logo.ico")

StringVar_repository_owner = StringVar()
StringVar_repository_name = StringVar()
StringVar_repository_local_database_name = StringVar()

StringVar_repository_URI = StringVar()

Label_Combobox_repository_URI = Label(widget_main, text="Repository URI")
Label_Combobox_repository_URI.grid(column=0, row=0)

Combobox_repository_URI = ttk.Combobox(widget_main, textvariable=StringVar_repository_URI)
Combobox_repository_URI["width"] = 120
Combobox_repository_URI.grid(column=0, row=1)

Label_Entry_AccessToken = Label(widget_main, text="Access Token")
Label_Entry_AccessToken.grid(column=0, row=2)

StringVar_AccessToken=StringVar();
Entry_AccessToken = Entry(widget_main, textvariable=StringVar_AccessToken)
Entry_AccessToken.grid(column=0, row=3, sticky=(E,W))
string_AccessToken_from_file=""
bool_store_access_token=False
if os.path.exists("access_token.json"):
    with open("access_token.json", 'r') as file:
        string_AccessToken_from_file = json.load(file)
    StringVar_AccessToken.set(string_AccessToken_from_file);


array_repository_uris=[]
bool_array_repository_uris_changed=False
if os.path.exists("array_repository_uris.json"):
    with open("array_repository_uris.json", 'r') as file:
        array_repository_uris = json.load(file)
else:
    array_repository_uris=("https://github.com/vaadin/flow", "https://github.com/vaadin/hilla", "https://github.com/vaadin/flow-components", "https://github.com/vaadin/web-components")
    bool_array_repository_uris_changed = True

Combobox_repository_URI["values"] = array_repository_uris

StringVar_Repository_File_Info = StringVar()
Label_Repository_File_Info = Label(widget_main, textvariable=StringVar_Repository_File_Info)
Label_Repository_File_Info.grid(column=0, row=4)

def ReadRepositoryInLocalDatabase():
    global bool_array_repository_uris_changed
    global bool_store_access_token
    global array_repository_uris
    if get_issues_in_json(StringVar_repository_owner.get(),StringVar_repository_name.get(),StringVar_AccessToken.get(),StringVar_repository_local_database_name.get()):
        if StringVar_repository_URI.get() not in Combobox_repository_URI["values"]:
            Combobox_repository_URI["values"] += (StringVar_repository_URI.get(),)
            bool_array_repository_uris_changed = True
            array_repository_uris = Combobox_repository_URI["values"]
        if string_AccessToken_from_file != StringVar_AccessToken.get():
            bool_store_access_token = True
        Update_UI()

def AnalyzeIssuesInLocalDatabase():
    issues = jsonToIssue(StringVar_repository_local_database_name.get())
    visualizeIssues(issues)

def RemoveLocalDatabase():
    if os.path.exists(StringVar_repository_local_database_name.get()):
        messagebox_RemoveLocalDatabase_result = messagebox.askquestion('Caution:','Are you sure you want to remove local database?',icon='warning')
        if messagebox_RemoveLocalDatabase_result == 'yes':
            os.remove(StringVar_repository_local_database_name.get())
            Update_UI()

Button_ReadIssuesInLocalDatabase = Button(widget_main, text="Read repository in local database", width=40, command=ReadRepositoryInLocalDatabase)
Button_ReadIssuesInLocalDatabase.grid(column=0, row=5)
Button_AnalyzeIssuesInLocalDatabase = Button(widget_main, text="Analyze issues in local database", width=40, command=AnalyzeIssuesInLocalDatabase)
Button_AnalyzeIssuesInLocalDatabase.grid(column=0, row=6)
Button_RemoveLocalDatabase = Button(widget_main, text="Remove local database", width=40, command=RemoveLocalDatabase)
Button_RemoveLocalDatabase.grid(column=0, row=7)

def Handle_StringVar_repository_URI_Changed(index, value, op):
    StringVar_repository_owner.set(None)
    StringVar_repository_name.set(None)
    StringVar_repository_local_database_name.set(None)
    string_URI = StringVar_repository_URI.get()
    int_index_after_github_com = string_URI.index("github.com/") + 11
    if int_index_after_github_com>=11:
        int_repository_name_start_index_minus_one = string_URI.index("/", int_index_after_github_com+1)
        if int_repository_name_start_index_minus_one > 0:
            StringVar_repository_owner.set(string_URI[int_index_after_github_com:int_repository_name_start_index_minus_one])
            StringVar_repository_name.set(string_URI[int_repository_name_start_index_minus_one+1:])
            StringVar_repository_local_database_name.set(StringVar_repository_owner.get()+"_"+StringVar_repository_name.get()+".json")
    Update_UI()

def Update_UI():
    if StringVar_repository_local_database_name.get():
        if os.path.exists(StringVar_repository_local_database_name.get()):
            StringVar_Repository_File_Info.set("Local databese file " + StringVar_repository_local_database_name.get() + " last updated " + str(datetime.datetime.fromtimestamp(pathlib.Path(StringVar_repository_local_database_name.get()).stat().st_mtime)))
            Button_RemoveLocalDatabase['state']=tkinter.NORMAL
            Button_AnalyzeIssuesInLocalDatabase['state']=tkinter.NORMAL
            Button_ReadIssuesInLocalDatabase['state']=tkinter.NORMAL
        else:
            StringVar_Repository_File_Info.set("No local database exists")
            Button_RemoveLocalDatabase['state']=tkinter.DISABLED
            Button_AnalyzeIssuesInLocalDatabase['state']=tkinter.DISABLED
            Button_ReadIssuesInLocalDatabase['state']=tkinter.NORMAL
    else:
        StringVar_Repository_File_Info.set("Invalid repository uri")
        Button_RemoveLocalDatabase['state']=tkinter.DISABLED
        Button_AnalyzeIssuesInLocalDatabase['state']=tkinter.DISABLED
        Button_ReadIssuesInLocalDatabase['state']=tkinter.DISABLED


StringVar_repository_URI.trace("w", Handle_StringVar_repository_URI_Changed)
Combobox_repository_URI.current(0)



widget_main.mainloop()

if bool_array_repository_uris_changed:
    with open("array_repository_uris.json", 'w') as file:
        json.dump(array_repository_uris, file, indent=4)

if bool_store_access_token:
    with open("access_token.json", 'w') as file:
        json.dump(StringVar_AccessToken.get(), file, indent=4)

