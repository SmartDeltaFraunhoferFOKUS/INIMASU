from tkinter import *
from xmlrpc.client import DateTime
import matplotlib.pyplot as pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.widgets import Slider
import matplotlib.dates as mdates
import colorsys

class IssueSolutionContributionInfo:
    def __init__(self, contributing_user_info, issue):
        self.contributing_user_info = contributing_user_info
        self.issue=issue

def overlaps(start1, end1, start2, end2):
    if end1 < start2:
        return False
    if start1 > end2:
        return False
    return True


class Gantt_Issues_Control:
    #def __init__(self):
    def Load(self, tkinter_context, RepositoryModel):
        color_sequence = mpl.color_sequences['tab10']
        color_sequence_half_transparant = []
        for c in color_sequence:
            color_sequence_half_transparant.append([c[0], c[1], c[2], 0.5])

        color_sequence_light=[]
        for c in color_sequence:
            color_sequence_light.append([c[0]*0.1+0.9, c[1]*0.1+0.9,c[2]*0.1+0.9])
        dict_user_login_names_issue_solution_contribution_info = dict()
        for key_issue in list(reversed(list(RepositoryModel.dict_issues))):
            if RepositoryModel.dict_issues[key_issue].solution_contributing_user_infos:
                for contributing_user_info in RepositoryModel.dict_issues[key_issue].solution_contributing_user_infos:
                    if not contributing_user_info['login'] in dict_user_login_names_issue_solution_contribution_info:
                        if len(dict_user_login_names_issue_solution_contribution_info) < 10:
                            dict_user_login_names_issue_solution_contribution_info[contributing_user_info['login']]=[]
                    if contributing_user_info['login'] in dict_user_login_names_issue_solution_contribution_info:
                        if RepositoryModel.dict_issues[key_issue].closed_at:
                            dict_user_login_names_issue_solution_contribution_info[contributing_user_info['login']].append(IssueSolutionContributionInfo(contributing_user_info, RepositoryModel.dict_issues[key_issue]))
    
        labels = list(sorted(list(dict_user_login_names_issue_solution_contribution_info)))
        label_tops = []
        actual_tops = []
        heights = []
        lefts = []
        widths = []
        colors= []
        edgecolors = []
        issue_solution_contribution_infos = []
        index_key_login = 0
        datetime_earliest = datetime.now()
        datetime_last = datetime.now()

        lefts_not_yet_working = []
        widths_not_yet_working = []
        colors_not_yet_working = []

        for key_login in labels:
            for issue_solution_contribution_info in dict_user_login_names_issue_solution_contribution_info[key_login]:
                label_tops.append(labels.index(key_login))
                actual_tops.append(labels.index(key_login))
                start_working_on_it_time=datetime.strptime( issue_solution_contribution_info.contributing_user_info['start_working_on_it'] if issue_solution_contribution_info.contributing_user_info['start_working_on_it'] and issue_solution_contribution_info.contributing_user_info['start_working_on_it'] > issue_solution_contribution_info.issue.created_at else issue_solution_contribution_info.issue.created_at, "%Y-%m-%dT%H:%M:%SZ")
                if start_working_on_it_time < datetime_earliest:
                    datetime_earliest = start_working_on_it_time
                lefts.append(start_working_on_it_time)
                closed_time =datetime.strptime( issue_solution_contribution_info.issue.closed_at, "%Y-%m-%dT%H:%M:%SZ") 
                widths.append(closed_time - start_working_on_it_time)

                datetime_created_at = datetime.strptime(issue_solution_contribution_info.issue.created_at, "%Y-%m-%dT%H:%M:%SZ")
                lefts_not_yet_working.append(datetime_created_at)
                widths_not_yet_working.append(start_working_on_it_time-datetime_created_at)
                colors_not_yet_working.append(color_sequence_light[index_key_login])

                heights.append(1)
                colors.append(color_sequence_half_transparant[index_key_login])
                edgecolors.append(color_sequence[index_key_login])
                issue_solution_contribution_infos.append(issue_solution_contribution_info)
            index_key_login = index_key_login + 1
        
        for label_top in range( len(labels)):
            dict_level_list_of_index_start_end_tuples_not_overlapping = dict()
            dict_level_list_of_index_start_end_tuples_not_overlapping[0]=[]
            for index in range(len(label_tops)):
                if label_tops[index]==label_top:
                    level=0
                    is_inserted = False
                    while not is_inserted:
                        is_overlapping = False
                        for index_start_end_tuples_not_overlappin in dict_level_list_of_index_start_end_tuples_not_overlapping[level]:
                            if overlaps(lefts[index], lefts[index] + widths[index], index_start_end_tuples_not_overlappin[1], index_start_end_tuples_not_overlappin[2]):
                                is_overlapping = True
                                break
                        if is_overlapping:
                            level = level + 1
                            if not level in dict_level_list_of_index_start_end_tuples_not_overlapping:
                                dict_level_list_of_index_start_end_tuples_not_overlapping[level]=[]
                        else:
                            dict_level_list_of_index_start_end_tuples_not_overlapping[level].append([index, lefts[index], lefts[index] + widths[index]])
                            is_inserted = True
            number_of_levels = len( dict_level_list_of_index_start_end_tuples_not_overlapping)
            if number_of_levels > 1:
                for level in dict_level_list_of_index_start_end_tuples_not_overlapping:
                    for index_start_end_tuples_not_overlappin in dict_level_list_of_index_start_end_tuples_not_overlapping[level]:
                        heights[index_start_end_tuples_not_overlappin[0]]=1.0/number_of_levels
                        actual_tops[index_start_end_tuples_not_overlappin[0]]=label_tops[index_start_end_tuples_not_overlappin[0]] + (1.0/number_of_levels)*level


        figure_gantt, figure_gantt_subplot = pyplot.subplots(figsize=(12,8))

        pyplot.subplots_adjust(bottom=0.25)
        figure_gantt_subplot.set_facecolor('#ffffff')
        
        the_barhs_not_yet_working = figure_gantt_subplot.barh(y=actual_tops, height=heights, left=lefts_not_yet_working, width=widths_not_yet_working, color=color_sequence_light)
        the_barhs = figure_gantt_subplot.barh(y=actual_tops, height=heights, left=lefts, width=widths, color=colors, edgecolor=edgecolors)
        pyplot.yticks(range(len(labels)), labels)
        figure_gantt_subplot.set_xlabel("Time")
        pyplot.axis([mpl.dates.date2num(datetime_last- relativedelta(years=1)), datetime_last, -0.5,9.5])        
        figure_gantt_subplot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        figure_canvas_gantt = FigureCanvasTkAgg(figure_gantt, tkinter_context)

        my_slider = Slider(pyplot.axes([0.1, 0.025, 0.8, 0.1], facecolor='teal'), "Start time:", valmin=mpl.dates.date2num(datetime_earliest), valmax=mpl.dates.date2num(datetime_last-relativedelta(years=1)), valinit=mpl.dates.date2num(datetime_last-relativedelta(years=2)))
        my_slider.valtext.set_text( datetime_last-relativedelta(years=1) )
        def handle_horizontal_slider_changed(val):
            my_slider.valtext.set_text(mdates.num2date(val).date())
            figure_gantt_subplot.axis([val, val+(mpl.dates.date2num(datetime_last)-mpl.dates.date2num(datetime_last-relativedelta(years=1))), -0.5,9.5])
            figure_canvas_gantt.draw_idle()

        my_slider.on_changed(handle_horizontal_slider_changed)
        handle_horizontal_slider_changed(mpl.dates.date2num(datetime_last-relativedelta(years=2)))

        annot = figure_gantt_subplot.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",bbox=dict(boxstyle="round", fc="w"),arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def rgb_changeHSV_Svalue(rgb, new_s):
            h,s,v=colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            r,g,b=colorsys.hsv_to_rgb(h, new_s, v)
            rgb_result=[r,g,b]
            return rgb_result

        def hover(event):
            hover_index=-1
            if (event.inaxes==figure_gantt_subplot):
                for idx, patch in enumerate(the_barhs.patches):
                    if patch.contains(event)[0]:
                        hover_index=idx
                        break
            if hover_index>=0:
                hover_info=issue_solution_contribution_infos[hover_index].issue.title
                annot.set_text(hover_info)
                annot.xy=the_barhs.patches[hover_index].xy
                annot.get_bbox_patch().set_facecolor(rgb_changeHSV_Svalue(edgecolors[hover_index],0.2))
                annot.set_visible(True)
            else:
                annot.set_visible(False)

        figure_gantt.canvas.mpl_connect("motion_notify_event", hover)

        pyplot.ion()

        figure_canvas_gantt.draw()
        figure_canvas_gantt.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

