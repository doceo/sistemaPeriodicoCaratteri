import tkinter as tk
import warnings
from functools import partial
from os import getcwd
from json import load as json_load

warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

from utils import *


class Value_Button(tk.Button):
    def __init__(self, number: int, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.value = int(number)
        self.text=""
        self.unclicked = ImageTk.PhotoImage(Image.open(getcwd()+f"/buttons/{self.value}_unclicked.png"))
        self.clicked = ImageTk.PhotoImage(Image.open(getcwd()+f"/buttons/{self.value}_clicked.png"))
        self.active = "unclicked"
        self.config(image=self.unclicked)
        self.next = 0

class Image_Button(tk.Button):
    def __init__(self, button_name: str, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.text=""
        self.button_image = ImageTk.PhotoImage(Image.open(getcwd()+f"/buttons/{button_name}.png"))
        self.config(image=self.button_image)

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.value = None 
    def show(self):
        self.lift()

class Final_Page(Page):
    def __init__(self, percentuali, labels, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.selected_wedge = None
        self.percentuali = percentuali

        with open("elementi.json", "r", encoding='utf-8') as f:
            self.data = json_load(f)
        #Graph
        self.fig = Figure(figsize=(12, 6), dpi=120, facecolor="white") 
        self.ax = self.fig.add_subplot()
        
        self.wedges, _ = self.ax.pie(percentuali.values(), labels=get_symbols(), counterclock=False)

        self.ax.legend(percentuali.values(), labels=labels, loc='upper right', bbox_to_anchor=(-0.1, 1.),fontsize=8)
        self.fig.subplots_adjust(right=0.905, left=0, bottom=0.067, top=0.89)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().configure(background='white')
        
        self.fig.canvas.mpl_connect("motion_notify_event", self.update)
        
        self.annotation = self.ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",color='yellow',bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),arrowprops=dict(arrowstyle="->"))
        self.annotation.set_visible(False)
        
        self.canvas.draw() 
        self.canvas.get_tk_widget().place(relx=0.0, rely=1.04, anchor="sw")
        
        self.text_1 = tk.Label(self, text="Basandosi sulle tue risposte, tu sei una lega composta da:", font = ("Tahoma", 35))
        self.text_1.place(relx=0.5, rely=0.07, anchor="center")
        self.text_1.config(bg="white")

    
    def update(self, event):
        if self.selected_wedge is not None:
            self.selected_wedge.set_center((0, 0))
            self.selected_wedge = None

        if event.inaxes == self.ax:
            for w in self.wedges:
                if w.contains_point([event.x, event.y]):
                    element = self.data[w.get_label()]
                    title = center_text(f"{element[0]} - {round(self.percentuali[element[0]], 3)}%", 50)
                    text1 = split_line(element[1], 50)
                    text2 = split_line(element[2], 50)
                
                    self.annotation.set_text(f" {title}\n\n{text1}\n\n{text2}")
                    self.annotation.xy = (event.xdata, event.ydata)
                    self.annotation.set_visible(True)
                    theta = np.radians((w.theta1 + w.theta2) / 2)
                    w.set_center((.2 * np.cos(theta), .2 * np.sin(theta)))
                    self.selected_wedge = w
                    self.fig.canvas.draw_idle()

        if self.selected_wedge is None and self.annotation.get_visible():
            self.annotation.set_visible(False)
            self.fig.canvas.draw_idle()
        

class Credits_Page(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.text_1 = tk.Label(self, text="Crediti:", font = ("Tahoma", 30))
        self.text_1.place(relx=0.5, rely=0, anchor="n")
        self.text_1.config(bg="white")
            
        self.text_2 = tk.Text(self,  font=("Tahoma", 25))
        self.text_2.place(relx=0.5, rely=0.08, anchor="n")
        self.text_2.insert(1.0, get_credits_desc())
        self.text_2.tag_configure("center", justify='center')
        self.text_2.tag_add("center", 1.0, "end")
        self.text_2.config(bg="white", wrap='word', relief='flat', state='disabled',  width=65, height=13) 
        
        self.back_button = Image_Button("back", self, command=self.back, borderwidth=0)
        self.back_button.place(relx=0.5, rely=0.99, anchor="s")
        self.back_button.config(bg="white", width = 450, height=120)
    
    def back(self):
        self.destroy()

class Question_Page(Page):
    def __init__(self, caratteristica, domanda, page_number, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.caratteristica = caratteristica
        self.domanda = domanda
        self.page_number = page_number
        self.value = None
        
        self.text_1 = tk.Text(self,  font=("Tahoma", 35))
        self.text_1.place(relx=0.5, rely=0.15, anchor="center")
        self.text_1.insert(1.0, self.domanda)
        self.text_1.tag_configure("center", justify='center')
        self.text_1.tag_add("center", 1.0, "end")
        self.text_1.config(bg="white", wrap='word', relief='flat', state='disabled', width=45, height=3) 
        
        self.value_buttons = []
        for i in range(1, 6):
           self.value_buttons.append(Value_Button(int(i), self, command=partial(self.check_box, i), borderwidth=0))

        for i in self.value_buttons:
            if i.value in [1,5]:
               dimension = 150
               x_pos = 0.1 if i.value == 1 else 0.9
            elif i.value in [2,4]:
                dimension = 125
                x_pos = 0.3 if i.value == 2 else 0.7
            else:
                dimension = 100
                x_pos = 0.5
                
            i.place(relx=x_pos, rely=0.45, anchor="center")
            i.config(bg="white", width = dimension, height=dimension)
            
            
            self.next_button = Image_Button("next", self, command=self.next, borderwidth=0)
            self.next_button.place(relx=0.5, rely=0.7, anchor="center")
            self.next_button.config(bg="white", width = 400, height=120)

            self.text_2 = tk.Label(self, text=self.caratteristica, font = ("Tahoma", 30))
            self.text_2.place(relx=0.05, rely=0.9, anchor="w")
            self.text_2.config(bg="white")
            
            self.text_3 = tk.Label(self, text=str(self.page_number)+"/12", font = ("Tahoma", 30))
            self.text_3.place(relx=0.95, rely=0.9, anchor="e")
            self.text_3.config(bg="white")
    
    def check_box(self, value):
        for i in self.value_buttons:
            if i.value == value:
                if i.active == "unclicked":
                    i.config(image=i.clicked)
                    i.active = "clicked"
                else:
                    i.config(image=i.unclicked)
                    i.active = "unclicked"
            else:
                i.config(image=i.unclicked)
                i.active = "unclicked"

    def next(self):
        for i in self.value_buttons:
            if i.active == "clicked":
                main.add_value(i.value)
                self.destroy()
                if self.page_number == 12:
                    main.show_results()
                break

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.questions = get_questions()
        self.risposte = []
        self.table = extract_csv("punteggi.csv")
        self.caratteristiche = self.table[0][1:]
        self.elementi = {i[0]: [int(i) for i in i[1:]] for i in self.table[1:]}
        self.pages = list(
            reversed(
                [
                    Question_Page(
                        self.caratteristiche[i], 
                        self.questions[i], 
                        i+1
                        ) for i in range(
                            len(
                                self.caratteristiche
                                )
                            )
                        ]
                )
            )

        for i in self.pages:
            i.config(bg="white")
            

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.config(bg="white")
        
        self.text_1 = tk.Label(self, text="SISTEMA PERIODICO", font = ("Tahoma", 50))
        self.text_1.place(relx=0.5, rely=0.15, anchor="center")
        self.text_1.config(bg="white")

        self.start_button = Image_Button("start", self, command=self.show_pages, borderwidth=0)
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")
        self.start_button.config(bg="white", width = 540, height=161)
        
        self.credits_button = Image_Button("credits", self, command=self.show_credits, borderwidth=0)
        self.credits_button.place(relx=0.5, rely=0.8, anchor="center")
        self.credits_button.config(bg="white", width = 412, height=161)
        
    
    def add_value(self, value):
        self.risposte.append(value)

    def show_pages(self):
        for i in self.pages:
            i.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
            i.show()

    def show_results(self):
        
        self.punteggi = {elemento: get_points(self.elementi[elemento], self.risposte) for elemento in self.elementi.keys()}
        totale_punti = sum(list(self.punteggi.values()))

        percentuali = {elemento: percentage(totale_punti, self.punteggi[elemento]) for elemento in self.elementi.keys()}

        labels = [f"{k} - {round(percentuali[k], 3)}%" for k in percentuali]

        self.final_page = Final_Page(percentuali, labels)
        self.final_page.config(bg="white")
        self.final_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.final_page.show()
                
    def show_credits(self):
        self.credits_page = Credits_Page()
        self.credits_page.config(bg="white")
        self.credits_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.credits_page.show()
                

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.resizable(False, False)
    root.configure(background='#FFFFFF')
    root.title("Sistema Periodico")
    #root.iconbitmap(getcwd()+"icon.ico")
    #root.attributes('-toolwindow', True)
    root.mainloop()
