import os

from matplotlib.widgets import TextBox
import GitHubAdapter.FileModel
import matplotlib.pyplot as plt
import matplotlib.patches
import math
import colorsys
from GitHubAdapter.GitHubAdapter import PopulateModelDatabaseFromJson, readJson
import math
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, VPacker, TextArea
from matplotlib.cbook import get_sample_data
from GitHubAdapter.FileModel import download_zip_and_unpack


def asses_commits(repo_owner,repo_name,file_path_base, access_token):
    repository_model = PopulateModelDatabaseFromJson(file_path_base)
    DictOfDicOfCommitDetails = readJson(file_path_base+"_commit_details.json") if os.path.exists(file_path_base+"_commit_details.json") else None

    download_zip_and_unpack( repo_owner, repo_name, access_token, False)
    file_model = read_files_recursive("."+os.sep + repo_owner + "_" + repo_name)

    for pull in repository_model.dict_pulls.values():
        for event in pull.events:
            if event['event'] == 'merged':
                if DictOfDicOfCommitDetails:
                    if event['commit_id'] in DictOfDicOfCommitDetails:
                        if not pull.commit_details:
                            pull.commit_details = []
                        commit_detail = DictOfDicOfCommitDetails[event['commit_id']]
                        for file in commit_detail['files']:
                            file_model.add_change("."+os.sep + repo_owner + "_" + repo_name + os.sep + file['filename'].replace('/', os.sep))
                        pull.commit_details.append( commit_detail )


    file_model.calculate_size()
    list_x_files=list()
    list_y_files=list()
    list_sizes_files=list()
    list_texts_files=list()
    list_changed_filenumber=list()
    list_changed_filescore=list()
    file_model.populate_position_size_lists_files(list_x_files, list_y_files, list_sizes_files, list_texts_files, list_changed_filenumber, list_changed_filescore)

    list_rectangles_files = list()
    list_facecolors_files=list()
    xlimit=0
    ylimit=0
    for x,y,size, changed_filescore in zip( list_x_files, list_y_files, list_sizes_files, list_changed_filescore):
        list_rectangles_files.append(matplotlib.patches.Rectangle([x+0.2,y+0.2], max(0.1,size-0.4), max(0.1,size-0.4)))
        r,g,b=colorsys.hsv_to_rgb( 0.33-((0.66*math.atan(changed_filescore))/math.pi), 1.0,1.0)
        list_facecolors_files.append( [r,g,b,0.5])
        xlimit=max(xlimit, x+size)
        ylimit=max(ylimit, y+size)

    list_rectangles_top_directories = list()
    list_x_top_directories=list()
    list_y_top_directories=list()
    list_sizes_top_directories=list()
    list_texts_top_directories=list()
    file_model.populate_position_size_lists_top_relevant_directories(list_x_top_directories, list_y_top_directories, list_sizes_top_directories, list_texts_top_directories)


    for x,y,size in zip( list_x_top_directories, list_y_top_directories, list_sizes_top_directories):
        list_rectangles_top_directories.append(matplotlib.patches.Rectangle([x+0.2,y+0.2], max(0.1,size-0.4), max(0.1,size-0.4)))
        xlimit=max(xlimit, x+size)
        ylimit=max(ylimit, y+size)
    
    figure, axis_system = plt.subplots()
    axis_system.set_xlim(0,xlimit)
    axis_system.set_ylim(0,ylimit)
    axis_system.set_aspect(1)


    patch_collection_top_directories=axis_system.add_collection(matplotlib.collections.PatchCollection(list_rectangles_top_directories, edgecolor='#00000060', facecolors='#00000009'))

    patch_collection_files = axis_system.add_collection(matplotlib.collections.PatchCollection(list_rectangles_files, edgecolor='#000000', facecolors=list_facecolors_files))

    image_file = None
    with get_sample_data(os.path.abspath("./INIMASU_GUI/Images/weather-severe-alert-2.png")) as file:
        image_file = plt.imread(file)
    annotation_offset_image_severe_alert = OffsetImage(image_file)
    annotation_offset_image_severe_alert.image.axes = axis_system

    with get_sample_data(os.path.abspath("./INIMASU_GUI/Images/weather-few-clouds-2.png")) as file:
        image_file = plt.imread(file)
    annotation_offset_image_few_clouds = OffsetImage(image_file)
    annotation_offset_image_few_clouds.image.axes = axis_system

    with get_sample_data(os.path.abspath("./INIMASU_GUI/Images/weather-clear-2.png")) as file:
        image_file = plt.imread(file)
    annotation_offset_image_clear = OffsetImage(image_file)
    annotation_offset_image_clear.image.axes = axis_system

    annotation_text_area =TextArea("Test Text")
    annotation_vpacker=VPacker(children=[annotation_offset_image_severe_alert,annotation_offset_image_clear,annotation_offset_image_few_clouds,annotation_text_area], align="center")
    annotation_bbox = AnnotationBbox(annotation_vpacker, xy=(0,0), xybox=(160,50), xycoords='data',boxcoords="offset points",bboxprops=dict(boxstyle="round", facecolor="#ff0000"),arrowprops=dict(arrowstyle="->"))

    axis_system.add_artist(annotation_bbox)
    annotation_bbox.set_visible(False)

    def hover(event):
        if (event.inaxes==axis_system):
            bfound, dict_index = patch_collection_files.contains(event)
            if bfound:
                annotation_bbox.set_visible(False)
                index=dict_index['ind'][0]
                annotation_text_area.set_text(list_texts_files[index]+'\n('+str(list_changed_filenumber[index]) + ' times changed)')
                annotation_bbox.xy=[list_x_files[index]+list_sizes_files[index]*0.5, list_y_files[index]+list_sizes_files[index]*0.5]
                bboxprops=dict(boxstyle="round", facecolor=[list_facecolors_files[index][0],list_facecolors_files[index][1],list_facecolors_files[index][2]])
                annotation_bbox.patch.set(**bboxprops)
                annotation_offset_image_clear.set_visible(list_changed_filescore[index]<=1)
                annotation_offset_image_few_clouds.set_visible((list_changed_filescore[index]>1) and (list_changed_filescore[index]<=3))
                annotation_offset_image_severe_alert.set_visible(list_changed_filescore[index]>3)
                annotation_bbox.set_visible(True)
            else:
                bfound, dict_index = patch_collection_top_directories.contains(event)
                if bfound:
                    annotation_bbox.set_visible(False)
                    index=dict_index['ind'][0]
                    annotation_text_area.set_text(list_texts_top_directories[index])
                    annotation_bbox.xy=[list_x_top_directories[index]+list_sizes_top_directories[index]*0.5, list_y_top_directories[index]+list_sizes_top_directories[index]*0.5]
                    bboxprops=dict(boxstyle="round", facecolor="#b0b0b0")
                    annotation_bbox.patch.set(**bboxprops)
                    annotation_offset_image_clear.set_visible(False)
                    annotation_offset_image_few_clouds.set_visible(False)
                    annotation_offset_image_severe_alert.set_visible(False)
                    annotation_bbox.set_visible(True)
                else:
                    annotation_bbox.set_visible(False)

    figure.canvas.mpl_connect("motion_notify_event", hover)

    plt.ion()

    plt.show()
    annotation_bbox.set_visible(False)


def read_files_recursive(path, parent=None):
    number_of_relevant_files = 0
    number_of_relevant_child_directories = 0
    list_children_file_models = list()
    file_model = GitHubAdapter.FileModel.FileModel(path, os.path.basename(path), list_children_file_models, True, parent, False, 0, 0)
    for entry in os.scandir(path):
        if entry.is_dir():
            child_file_model = read_files_recursive(entry.path, file_model)
            if child_file_model.number_of_relevant_children:
                if child_file_model.number_of_relevant_children > 0:
                    file_model.number_of_relevant_children = file_model.number_of_relevant_children + child_file_model.number_of_relevant_children
                    number_of_relevant_child_directories = number_of_relevant_child_directories + 1
            list_children_file_models.append( child_file_model )
        else: 
            if entry.is_file():
                if ( entry.name.endswith(".java") ):
                    fsize=entry.stat().st_size
                    list_children_file_models.append(GitHubAdapter.FileModel.FileModel(entry.path, entry.name, None, False, file_model, True, 0, entry.stat().st_size ))
                    file_model.number_of_relevant_children = file_model.number_of_relevant_children +1
                    number_of_relevant_files = number_of_relevant_files+1

    if number_of_relevant_files > 0:
        print(path + " contains " + str( number_of_relevant_files ) + " relevant files")
        if number_of_relevant_child_directories > 0:
            print(path + " also contains " + str(number_of_relevant_child_directories) + " relevant child directories - total relevant files: " + str(file_model.number_of_relevant_children))
        
        file_model.must_be_visualized = True
    else:
        file_model.must_be_visualized = False
        if number_of_relevant_child_directories > 1:
            for child_file_model in list_children_file_models:
                child_file_model.must_be_visualized = True
            print(path + " contains " + str(number_of_relevant_child_directories) + " relevant child directories - total relevant files: " + str(file_model.number_of_relevant_children))

    return file_model


