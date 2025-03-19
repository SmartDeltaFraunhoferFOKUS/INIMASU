
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pathlib
import sys
import json
import datetime
import os.path
import tkinter
#from tkinter.tix import COLUMN
import matplotlib.pyplot as pyplot


sys.path.append(str(pathlib.Path().resolve()))

#from issueInspection.ExtractJsonFromRepository.ExtractJsonFromRepository import get_issues_in_json, get_issues_in_json_file
#from issueInspection.JsonToIssue.JsonToIssue import jsonToIssue
#from issueInspection.VisualizeIssues.VisualizeIssues import visualize
from UI_Elements.HoverButton import HoverButton
from Gantt_Issues_Control import Gantt_Issues_Control
from GitHubAdapter.GitHubAdapter import ReadFromGitHubAndStoreInJson, PopulateModelDatabaseFromJson
from AssesCommits import asses_commits


class INIMASU_GUI:
    def __init__(self):
        self.bool_store_access_token=False
        self.array_access_tokens=[]
        self.array_repository_uris=[]
        self.bool_array_repository_uris_changed=False
        self.button_width_in_pixels=92
        self.path_for_images="./INIMASU_GUI/Images/"

    def StartMainLoop(self) -> int:

        widget_main = Tk()
        widget_main.title("INIMASU")
        widget_main.geometry("800x600")
        widget_main.iconbitmap(self.path_for_images+"INIMASU_Logo.ico")

        Frame_Main = Frame(widget_main)
        Frame_Main.pack(fill=BOTH, expand=True, padx=2, pady=2)
        Frame_Main.grid_columnconfigure(0, weight=1)
        Frame_Main.grid_rowconfigure(6,weight=1)

        StringVar_repository_owner = StringVar()
        StringVar_repository_name = StringVar()
        StringVar_repository_local_database_name = StringVar()

        StringVar_repository_URI = StringVar()

        Label_Entry_AccessToken = Label(Frame_Main, text="Access Token")
        Label_Entry_AccessToken.grid(column=0, row=0, sticky=W)

        StringVar_AccessToken=StringVar();
        Combobox_access_tokens = ttk.Combobox(Frame_Main, textvariable=StringVar_AccessToken)
        Combobox_access_tokens.grid(column=0, row=1, sticky=(E,W))

        if os.path.exists("access_tokens.json"):
            with open("access_tokens.json", 'r') as file:
                self.array_access_tokens = json.load(file)
        Combobox_access_tokens["values"]=self.array_access_tokens

        Label_Combobox_repository_URI = Label(Frame_Main, text="Repository URI")
        Label_Combobox_repository_URI.grid(column=0, row=2, sticky=W,pady=(8,0))

        Combobox_repository_URI = ttk.Combobox(Frame_Main, textvariable=StringVar_repository_URI)
        #Combobox_repository_URI["width"] = 120
        Combobox_repository_URI.grid(column=0, row=3, sticky=W+E)

        if os.path.exists("array_repository_uris.json"):
            with open("array_repository_uris.json", 'r') as file:
                self.array_repository_uris = json.load(file)
        else:
            self.array_repository_uris=("https://github.com/vaadin/flow", "https://github.com/vaadin/hilla", "https://github.com/vaadin/flow-components", "https://github.com/vaadin/web-components")
            self.bool_array_repository_uris_changed = True

        Combobox_repository_URI["values"] = self.array_repository_uris

        StringVar_Repository_File_Info = StringVar()
        Label_Repository_File_Info = Label(Frame_Main, textvariable=StringVar_Repository_File_Info)
        Label_Repository_File_Info.grid(column=0, row=4, sticky=W)

        def ReadRepositoryInLocalDatabase():
            if ( StringVar_AccessToken.get() not in Combobox_access_tokens["values"]):
                Combobox_access_tokens["values"] += StringVar_AccessToken.get()
                self.array_access_tokens = Combobox_access_tokens["values"]
                self.bool_store_access_token=True

            if ReadFromGitHubAndStoreInJson(StringVar_repository_owner.get(),StringVar_repository_name.get(),self.array_access_tokens,StringVar_repository_local_database_name.get()):
                if StringVar_repository_URI.get() not in Combobox_repository_URI["values"]:
                    Combobox_repository_URI["values"] += (StringVar_repository_URI.get(),)
                    self.bool_array_repository_uris_changed = True
                    self.array_repository_uris = Combobox_repository_URI["values"]
                Update_UI()

        def AnalyzeCommitsInLocalDatabase():
            if StringVar_repository_local_database_name.get():
                if os.path.exists(StringVar_repository_local_database_name.get()+"_issues.json"):
                    asses_commits(StringVar_repository_owner.get(),StringVar_repository_name.get(), StringVar_repository_local_database_name.get(),StringVar_AccessToken.get())


        def AnalyzeIssuesInLocalDatabase():
            if StringVar_repository_local_database_name.get():
                if os.path.exists(StringVar_repository_local_database_name.get()+"_issues.json"):            
                    RepositoryModelDatabase=PopulateModelDatabaseFromJson(StringVar_repository_local_database_name.get())
                    Gantt_Issues_Control_Instance.Load(widget_main, RepositoryModelDatabase)

        def RemoveLocalDatabase():
            if os.path.exists(StringVar_repository_local_database_name.get()+"_issues.json"):
                messagebox_RemoveLocalDatabase_result = messagebox.askquestion('Caution:','Are you sure you want to remove local database?',icon='warning')
                if messagebox_RemoveLocalDatabase_result == 'yes':
                    os.remove(StringVar_repository_local_database_name.get()+"_issues.json")
                    Update_UI()

        def Application_Exit():
            pyplot.close('all')
            widget_main.destroy()

        Toolbar_Main = Frame(Frame_Main, borderwidth=1, relief=GROOVE)
        Toolbar_Main.grid(column=0, row=5, sticky='w',pady=(8,0))

        PhotoImage_ReadIssuesInLocalDatabase = PhotoImage(file=self.path_for_images+"download-2.png")
        Button_ReadIssuesInLocalDatabase = HoverButton(Toolbar_Main, text="Read repository in local database", wraplength=self.button_width_in_pixels, justify=CENTER, width=self.button_width_in_pixels, compound=TOP, image=PhotoImage_ReadIssuesInLocalDatabase, command=ReadRepositoryInLocalDatabase)
        Button_ReadIssuesInLocalDatabase.pack(side=LEFT)
        PhotoImage_RemoveLocalDatabase = PhotoImage(file=self.path_for_images+"edit-delete-9.png")
        Button_RemoveLocalDatabase = HoverButton(Toolbar_Main, text="Remove local database", wraplength=self.button_width_in_pixels, justify=CENTER, width=self.button_width_in_pixels, compound=TOP, image=PhotoImage_RemoveLocalDatabase, command=RemoveLocalDatabase)
        Button_RemoveLocalDatabase.pack(side=LEFT)
        ttk.Separator(Toolbar_Main, orient=VERTICAL).pack(side=LEFT, padx=2, fill=Y)
        PhotoImage_AnalyzeCommitsInLocalDatabase = PhotoImage(file=self.path_for_images+"weather-severe-alert-2.png")
        Button_AnalyzeCommitsInLocalDatabase = HoverButton(Toolbar_Main, text="Asses commits in local database", wraplength=self.button_width_in_pixels, justify=CENTER, width=self.button_width_in_pixels, compound=TOP, image=PhotoImage_AnalyzeCommitsInLocalDatabase, command=AnalyzeCommitsInLocalDatabase)
        Button_AnalyzeCommitsInLocalDatabase.pack(side=LEFT)
        ttk.Separator(Toolbar_Main, orient=VERTICAL).pack(side=LEFT, padx=2, fill=Y)
        PhotoImage_AnalyzeIssuesInLocalDatabase = PhotoImage(file=self.path_for_images+"office-chart-area.png")
        Button_AnalyzeIssuesInLocalDatabase = HoverButton(Toolbar_Main, text="Analyze issues in local database", wraplength=self.button_width_in_pixels, justify=CENTER, width=self.button_width_in_pixels, compound=TOP, image=PhotoImage_AnalyzeIssuesInLocalDatabase, command=AnalyzeIssuesInLocalDatabase)
        Button_AnalyzeIssuesInLocalDatabase.pack(side=LEFT)
        ttk.Separator(Toolbar_Main, orient=VERTICAL).pack(side=LEFT, padx=2, fill=Y)
        PhotoImageApplicationExit = PhotoImage(file=self.path_for_images+"application-exit-5.png")
        Button_Application_Exit = HoverButton(Toolbar_Main, text="Exit INIMASU Application",wraplength=self.button_width_in_pixels, justify=CENTER, width=self.button_width_in_pixels, compound=TOP, image=PhotoImageApplicationExit, command=Application_Exit)
        Button_Application_Exit.pack(side=LEFT)


        def Handle_StringVar_repository_URI_Changed(index, value, op):
            StringVar_repository_owner.set(None)
            StringVar_repository_name.set(None)
            StringVar_repository_local_database_name.set(None)
            string_URI = StringVar_repository_URI.get()
            if string_URI:
                int_index_after_github_com = string_URI.find("github.com/") + 11
                if (int_index_after_github_com>=11) and (len(string_URI) > int_index_after_github_com+1):
                    int_repository_name_start_index_minus_one = string_URI.find("/", int_index_after_github_com+1)
                    if int_repository_name_start_index_minus_one > 0:
                        StringVar_repository_owner.set(string_URI[int_index_after_github_com:int_repository_name_start_index_minus_one])
                        StringVar_repository_name.set(string_URI[int_repository_name_start_index_minus_one+1:])
                        StringVar_repository_local_database_name.set(StringVar_repository_owner.get()+"_"+StringVar_repository_name.get())
            Update_UI()

        def Update_UI():
            if StringVar_repository_local_database_name.get():
                if os.path.exists(StringVar_repository_local_database_name.get()+"_issues.json"):
                    StringVar_Repository_File_Info.set("Local databese file " + StringVar_repository_local_database_name.get()+"_issues.json" + " last updated " + str(datetime.datetime.fromtimestamp(pathlib.Path(StringVar_repository_local_database_name.get()+"_issues.json").stat().st_mtime)))
                    Button_RemoveLocalDatabase['state']=tkinter.NORMAL
                    Button_AnalyzeCommitsInLocalDatabase['state']=tkinter.NORMAL
                    Button_AnalyzeIssuesInLocalDatabase['state']=tkinter.NORMAL
                    Button_ReadIssuesInLocalDatabase['state']=tkinter.NORMAL
                else:
                    StringVar_Repository_File_Info.set("No local database exists")
                    Button_RemoveLocalDatabase['state']=tkinter.DISABLED
                    Button_AnalyzeCommitsInLocalDatabase['state']=tkinter.DISABLED
                    Button_AnalyzeIssuesInLocalDatabase['state']=tkinter.DISABLED
                    Button_ReadIssuesInLocalDatabase['state']=tkinter.NORMAL
            else:
                StringVar_Repository_File_Info.set("Invalid repository uri")
                Button_RemoveLocalDatabase['state']=tkinter.DISABLED
                Button_AnalyzeCommitsInLocalDatabase['state']=tkinter.DISABLED
                Button_AnalyzeIssuesInLocalDatabase['state']=tkinter.DISABLED
                Button_ReadIssuesInLocalDatabase['state']=tkinter.DISABLED


        StringVar_repository_URI.trace("w", Handle_StringVar_repository_URI_Changed)
        Combobox_repository_URI.current(0)

        Combobox_access_tokens.current(0)

        Frame_Gnat_Issues_Control = Frame(Frame_Main, borderwidth=1, relief=GROOVE)
        Frame_Gnat_Issues_Control.grid(column=0, row=6, sticky='wens',pady=(8,0))
        
        Gantt_Issues_Control_Instance = Gantt_Issues_Control()

        widget_main.mainloop()

        if self.bool_array_repository_uris_changed:
            with open("array_repository_uris.json", 'w') as file:
                json.dump(self.array_repository_uris, file, indent=4)

        if self.bool_store_access_token:
            with open("access_token.json", 'w') as file:
                json.dump(self.array_access_tokens, file, indent=4)

        return 0

def Main_INIMASU_GUI() -> int:
    Instance_INIMASU_GUI = INIMASU_GUI()
    sys.exit(Instance_INIMASU_GUI.StartMainLoop())

if __name__ == "__main__":
    Main_INIMASU_GUI()