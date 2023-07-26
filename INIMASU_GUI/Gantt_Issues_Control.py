from tkinter import *
from xmlrpc.client import DateTime
import matplotlib.pyplot as pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.widgets import Slider
import matplotlib.dates as mdates


class Gantt_Issues_Control:
    #def __init__(self):
    def Load(self, tkinter_context, RepositoryModel):
        figure_gantt, figure_gantt_subplot = pyplot.subplots(figsize=(12,8))
        pyplot.subplots_adjust(bottom=0.25)
        figure_gantt_subplot.set_facecolor('#ffffff')
        color_sequence = mpl.color_sequences['tab10']
        color_sequence_half_transparant = []
        for c in color_sequence:
            color_sequence_half_transparant.append([c[0], c[1], c[2], 0.5])

        dict_contributing_user_logins_issues = dict()
        for key_issue in list(reversed(list(RepositoryModel.dict_issues))):
            if RepositoryModel.dict_issues[key_issue].solution_contributing_user_logins:
                for login in RepositoryModel.dict_issues[key_issue].solution_contributing_user_logins:
                    if not login in dict_contributing_user_logins_issues:
                        if len(dict_contributing_user_logins_issues) < 10:
                            dict_contributing_user_logins_issues[login]=[]
                    if login in dict_contributing_user_logins_issues:
                        if RepositoryModel.dict_issues[key_issue].closed_at:
                            dict_contributing_user_logins_issues[login].append(RepositoryModel.dict_issues[key_issue])
    
        labels = []
        lefts = []
        widths = []
        colors= []
        edgecolors = []
        index_key_login = 0
        datetime_earliest = datetime.now()
        datetime_last = datetime.now()

        for key_login in list(sorted(list(dict_contributing_user_logins_issues))):
            for issue in dict_contributing_user_logins_issues[key_login]:
                labels.append(key_login)
                create_time=datetime.strptime( issue.created_at, "%Y-%m-%dT%H:%M:%SZ")
                if create_time < datetime_earliest:
                    datetime_earliest = create_time
                lefts.append(create_time)
                closed_time =datetime.strptime( issue.closed_at, "%Y-%m-%dT%H:%M:%SZ") 
                widths.append(closed_time - create_time)
                colors.append(color_sequence_half_transparant[index_key_login])
                edgecolors.append(color_sequence[index_key_login])
            index_key_login = index_key_login + 1
        
        #figure_gantt_subplot.set_xlim(datetime.now() - relativedelta(years=1), datetime.now())
        figure_gantt_subplot.barh(y=labels, left=lefts, width=widths, color=colors, edgecolor=edgecolors)
        figure_gantt_subplot.set_xlabel("Time")
        pyplot.axis([mpl.dates.date2num(datetime_last- relativedelta(years=1)), datetime_last, -0.5,9.5])        
        figure_gantt_subplot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        #figure_gantt_subplot.set_title("time")
        figure_canvas_gantt = FigureCanvasTkAgg(figure_gantt, master=tkinter_context)

        my_slider = Slider(pyplot.axes([0.1, 0.025, 0.8, 0.1], facecolor='teal'), "Start time", valmin=mpl.dates.date2num(datetime_earliest), valmax=mpl.dates.date2num(datetime_last-relativedelta(years=1)), valinit=mpl.dates.date2num(datetime_last-relativedelta(years=1)))
        my_slider.valtext.set_text( datetime_last-relativedelta(years=1) )
        def handle_horizontal_slider_changed(val):
            my_slider.valtext.set_text(mdates.num2date(val).date())
            figure_gantt_subplot.axis([val, val+(mpl.dates.date2num(datetime_last)-mpl.dates.date2num(datetime_last-relativedelta(years=1))), -0.5,9.5])
            figure_canvas_gantt.draw_idle()

        my_slider.on_changed(handle_horizontal_slider_changed)

        figure_canvas_gantt.draw()
        figure_canvas_gantt.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

