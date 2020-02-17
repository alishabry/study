from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
import json
import itertools
from tkinter import messagebox as mb
import networkx as nx

 
class data:  
    def __init__(self):
        self.file = None
        self.dict = dict()
        self.graf = nx.Graph()
        self.nameActor = None

    def ListOfInter(self):
        films = {}
        name = []
        for i in self.dict:
            k=[]
            name.append(i["name"])
            for j in i['films']:
                k.append(str(j['title'])+'_'+str(j['year']))
            films.update({i["name"]:k})
        for i in range(len(name)-1):
            for j in range(i,len(name)):
                if len(intersection(films[name[i]], films[name[j]])) >0:
                    self.graf.add_edge(name[i], name[j])
        
        path = nx.shortest_path(self.graf, self.nameActor, "Kevin Bacon")
        makeText = []
        

        for i in range(len(path) - 1):
            makeText.append(path[i] + " was in " + ''.join(intersection(films[path[i]], films[path[i+1]])) + " with " + path[i+1] + '\n')
        print(str("Path from " + self.nameActor + " to Kevin Bacon: \n").join(makeText) + self.nameActor+'s'+ " Bacon number is " +  str(len(nx.shortest_path(self.graf, self.nameActor, "Kevin Bacon")) - 1))
   
        return str("Path from " + self.nameActor + " to Kevin Bacon: \n") + ''.join(makeText) + self.nameActor+'s'+ " Bacon number is " +  str(len(nx.shortest_path(self.graf, self.nameActor, "Kevin Bacon")) - 1)
  





def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 


def ok():
    try:
        data.file = askopenfilename(filetypes =[('json', '*.json')])  
        file = open(data.file)
        if file is not None: 
            data.dict = json.load(file)

    except:
         mb.showerror("Error", "Wrong file")

    names = []
    text.config(text = 'Select an actor')
    for i in data.dict:
        names.append(i['name'])

    comb.config(values=names)
    comb.set(names[0])

    




def ok1():
    data.nameActor = comb.get()

    text2.config(text = data.ListOfInter())

    
data = data()
window = Tk()
window.title('Bacon Number')

bgc = '#E6E6FA'
ws = window.winfo_screenwidth() 
hs = window.winfo_screenheight() 
window.configure(background=bgc)
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
window.wm_geometry("+%d+%d" % (x, y))
window.resizable(0, 0)
frame1 = Frame(window, bg = bgc)
frame2 = Frame(window, bg = bgc)
frame3 = Frame(window, bg = bgc)
frame5 = Frame(window, bg = bgc)
frame4 = Frame(window, bg = bgc)
frame4.grid(column = 0, row =0)
frame5.grid(column = 0, row =5)  
text2 = Label(frame5,font=("Calibri Bold",14), bg = bgc)
text2.grid(column = 0, row =0)


text = Label(frame1,text = 'Select a data file',font=("Calibri Bold",20), bg = bgc)
butChoose = Button(frame2, text = '...',command = ok, font=("Calibri Bold",15),bg = '#B0C4DE')
butOk = Button(frame3, text = 'OK',font=("Calibri Bold",15), bg = '#B0C4DE',command = ok1)
frame1.grid(column = 0, row = 1)
frame2.grid(column = 0 , row = 2)
frame3.grid(column = 0 , row = 3)
comb = ttk.Combobox(frame2,height=20,width = 15,font=("Calibri Bold",12),justify='center')
comb.grid(column =0, row = 0)

text.pack(side=LEFT, expand=2, ipadx=10, ipady=10, anchor=E)
butChoose.grid(column= 1, row =0)
butOk.grid(column = 1, row = 0)

window.mainloop()