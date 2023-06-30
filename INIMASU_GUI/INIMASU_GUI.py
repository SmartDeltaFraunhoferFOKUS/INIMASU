
from tkinter import *
from tkinter import ttk
import pathlib
import sys
import json
import datetime
import os.path
import tkinter
sys.path.append(str(pathlib.Path().resolve()))

from ExtractJsonFromRepository.ExtractJsonFromRepository import get_issues_in_json


widget_main = Tk()
widget_main.title("INIMASU")
widget_main.geometry("800x600")
widget_main.iconbitmap("INIMASU_Logo.ico")

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
if os.path.exists("access_token.json"):
    with open("access_token.json", 'r') as file:
        string_AccessToken_from_file = json.load(file)
    StringVar_AccessToken.set(string_AccessToken_from_file);


array_repository_uris=[]
if os.path.exists("array_repository_uris.json"):
    with open("array_repository_uris.json", 'r') as file:
        array_repository_uris = json.load(file)
else:
    array_repository_uris=("https://github.com/vaadin/flow", "https://github.com/vaadin/hilla", "https://github.com/vaadin/flow-components", "https://github.com/vaadin/web-components")

Combobox_repository_URI["values"] = array_repository_uris

StringVar_Repository_File_Info = StringVar()
Label_Repository_File_Info = Label(widget_main, textvariable=StringVar_Repository_File_Info)
Label_Repository_File_Info.grid(column=0, row=4)

def ReadRepositoryInLocalDatabase():
    get_issues_in_json("vaadin","flow",StringVar_AccessToken.get(),"vaadin_flow.json")

Button_ReadIssuesInLocalDatabase = Button(widget_main, text="Read repository in local database", width=40, command=ReadRepositoryInLocalDatabase)
Button_ReadIssuesInLocalDatabase.grid(column=0, row=5)
Button_AnalyzeIssuesInLocalDatabase = Button(widget_main, text="Analyze issues in local database", width=40)
Button_AnalyzeIssuesInLocalDatabase.grid(column=0, row=6)
Button_RemoveLocalDatabase = Button(widget_main, text="Remove local database", width=40)
Button_RemoveLocalDatabase.grid(column=0, row=7)

string_repository_owner = None
string_repository_name = None
string_repository_local_database_name = None
def Handle_Repository_URI_changed(event_argument):
    string_repository_owner = None
    string_repository_name = None
    string_repository_local_database_name = None
    string_URI = StringVar_repository_URI.get()
    int_index_after_github_com = string_URI.index("github.com/") + 11
    if int_index_after_github_com>=11:
        int_repository_name_start_index_minus_one = string_URI.index("/", int_index_after_github_com+1)
        if int_repository_name_start_index_minus_one > 0:
            string_repository_owner = string_URI[int_index_after_github_com:int_repository_name_start_index_minus_one]
            string_repository_name = string_URI[int_repository_name_start_index_minus_one+1:]
            string_repository_local_database_name=string_repository_owner+"_"+string_repository_name+".json"
    if string_repository_local_database_name:
        if os.path.exists(string_repository_local_database_name):
            StringVar_Repository_File_Info.set("Local databese file " + string_repository_local_database_name + " last updated " + str(datetime.datetime.fromtimestamp(pathlib.Path(string_repository_local_database_name).stat().st_mtime)))
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



Combobox_repository_URI.bind('<<ComboboxSelected>>',Handle_Repository_URI_changed)
Combobox_repository_URI.current(0)
Handle_Repository_URI_changed(None)



widget_main.mainloop()

with open("array_repository_uris.json", 'w') as file:
    json.dump(array_repository_uris, file, indent=4)

with open("access_token.json", 'w') as file:
    json.dump(StringVar_AccessToken.get(), file, indent=4)

