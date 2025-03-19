import math
import requests
import json
import os
import zipfile

class FileModel:
    def __init__(self, id=None, name=None, children=None, is_directory=None, parent=None, must_be_visualized=None, number_of_relevant_children=0, file_size_in_bytes=0):
        self.id = id
        self.name=name
        self.children=children
        self.is_directory = is_directory
        self.parent=parent
        self.must_be_visualized = must_be_visualized
        self.number_of_relevant_children = number_of_relevant_children
        self.file_size_in_bytes = file_size_in_bytes
        self.size=0.0
        self.x=0.0
        self.y=0.0
        self.changes=[]

    def get_change_score(self):
        score=0
        for change in self.changes:
            score+=change
        return score

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"Issue object has no attribute '{attribute}'.")

    def calculate_size(self):
        if self.number_of_relevant_children > 0:
            width=0.0
            height=0.0
            cage_x=0.0
            current_x=0.0
            current_y=0.0
            row_completed=False

            if self.children:
                for child in self.children:
                    child_size = child.calculate_size()
                    if row_completed==False:
                        if current_x >= cage_x:
                            row_completed=True
                        width=max(width, current_x+child_size)
                        height=max(height, current_y+child_size)
                        child.x=current_x
                        child.y=current_y
                        if row_completed == False:
                            current_x = current_x + child_size

                    else:
                        if current_y >= child_size:
                            width=max(width, current_x+child_size)
                            current_y = current_y - child_size
                            child.x=current_x
                            child.y=current_y
                        else:
                            current_y=height
                            current_x=0.0
                            width=max(width, current_x+child_size)
                            height=max(height, current_y+child_size)
                            child.x=current_x
                            child.y=current_y
                            current_x = current_x + child_size
                            row_completed = False
                            cage_x=width

            self.size=max(width,height)
            return self.size
        if self.must_be_visualized:
            self.size=5*math.atan( self.file_size_in_bytes / 1024.0)
            return self.size
        return 0.0

    def get_x(self):
        if self.parent:
            return self.parent.get_x()+self.x
        return self.x
    
    def get_y(self):
        if self.parent:
            return self.parent.get_y()+self.y
        return self.y

    def populate_position_size_lists_files( self, list_x, list_y, list_sizes, list_texts, list_changed_filenumber, list_changed_filescore ):
        if self.children:
            for child in self.children:
                child.populate_position_size_lists_files( list_x, list_y, list_sizes, list_texts, list_changed_filenumber, list_changed_filescore )
        if self.must_be_visualized:
            if self.is_directory==False:
                list_x.append(self.get_x())
                list_y.append(self.get_y())
                list_sizes.append(self.size)
                list_texts.append(self.name)
                list_changed_filenumber.append(len(self.changes))
                list_changed_filescore.append(self.get_change_score())


    def populate_position_size_lists_top_relevant_directories( self, list_x, list_y, list_sizes, list_texts ):
        if self.must_be_visualized:
            if self.is_directory:
                list_x.append(self.get_x())
                list_y.append(self.get_y())
                list_sizes.append(self.size)
                list_texts.append(self.name)
        else:
            if self.children:
                for child in self.children:
                    if child.number_of_relevant_children>0:
                        child.populate_position_size_lists_top_relevant_directories( list_x, list_y, list_sizes, list_texts )


    def add_change(self, file_path, criticality = 1):
        if self.id == file_path:
            self.changes.append(criticality)
        else:
            if self.children:
                for child in self.children:
                    if file_path.startswith(child.id):
                        child.add_change(file_path, criticality)

def download_zip_and_unpack(repo_owner,repo_name,access_token, force_download_even_if_exists):
    directory_to_extract_to="."+os.sep + repo_owner + "_" + repo_name
    if os.path.isdir("."+os.sep + repo_owner + "_" + repo_name ):
        if not force_download_even_if_exists:
            return

    headers = {'Authorization': f'token {access_token}'}
    r = requests.get('https://api.github.com/repos/'+repo_owner+'/'+repo_name+'/zipball/', headers=headers)

    print('downloading ' + repo_owner + '_' + repo_name+ '.zip - please wait')

    if r.status_code == 200:
        with open(repo_owner + '_' + repo_name+ '.zip', 'wb') as fh:
            fh.write(r.content)
        print('downloaded ' + repo_owner + '_' + repo_name+ '.zip' + ' (size:' + str(len(r.content)) + ')')
        print('unpacking ' + repo_owner + '_' + repo_name+ '.zip' + ' (size:' + str(len(r.content)) + ') - please wait')
        with zipfile.ZipFile(repo_owner + '_' + repo_name+ '.zip', 'r') as zip_ref:
            zipinfos=zip_ref.infolist()
            for zipinfo in zipinfos:
                index=zipinfo.filename.find('/')
                if index>=0:
                    zipinfo.filename = repo_owner + "_" + repo_name + '/' + zipinfo.filename[index+1:]
                else:
                    zipinfo.filename = repo_owner + "_" + repo_name
                zip_ref.extract(zipinfo)
        print('unpack completed')

    else:
        print(r.text)    
