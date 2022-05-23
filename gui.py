import tkinter as tk
from algoritm import extract_csv, get_questions
from os import getcwd
from PIL import Image, ImageTk

from functools import partial

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
    def show(self):
        self.lift()

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

        #self.text_1 = tk.Label(self, text=self.domanda, font = ("Tahoma", 25))
        #self.text_1.place(relx=0.5, rely=0.15, anchor="center")
        #self.text_1.config(bg="white")
        
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
                main.values.append(i.value)
                self.destroy()
                break

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.questions = get_questions()
        self.values = []
        self.table = extract_csv("sistema_periodico.csv")
        self.caratteristiche = self.table[0][1:]
        
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
        
        
    def show_pages(self):
        for i in self.pages:
            i.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
            i.show()

    def show_credits(self):
        pass
                

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.resizable(False, False)
    root.configure(background='#FFFFFF')
    root.mainloop()
