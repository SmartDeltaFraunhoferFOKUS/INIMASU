import tkinter as tk

class HoverButton(tk.Button):
    def __init__(self, master, activebackground='SystemHighlight', **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.activebackground = activebackground

    def on_enter(self, e):
        if self['state']==tk.NORMAL:
            self['background'] = self.activebackground

    def on_leave(self, e):
        self['background'] = self.defaultBackground