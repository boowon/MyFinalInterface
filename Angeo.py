from tkinter import *
from tkinter import messagebox 
from PIL import ImageTk,Image 
from tkinter import font
from tkcalendar import DateEntry
from tkinter import filedialog
import sqlite3
from call_model import cnn_model


def Pred(path):
    global maladieName
    maladieName = cnn_model(path)
    print(maladieName)
    messagebox.showinfo(title="Maladie", message=maladieName)
    
def confexit():
    yesno = messagebox.askyesno(title="Exit", message="Are sure you want to exit?") #return 1 fro yes and 0 for No
    if yesno == 1:
        root.quit()

def submit():
    #create a db or connect to it
    cnx = sqlite3.connect("basededonne.db")
    cur = cnx.cursor()
    #cur.execute('''DROP TABLE IF EXISTS Data_Base_pateients''')
    #creat a table
    cur.execute(""" CREATE TABLE IF NOT EXISTS Data_Base_pateients (
              First_name text,
              Last_name text,
              Gender text
                )
                """)
    #inesrt infos
    if fname.get()!="":
        if lname.get()!="":
            cur.execute("INSERT INTO Data_Base_pateients VALUES (:First_name, :Last_name, :Gender)",
                 { 'First_name' : fname.get(),
                   'Last_name' : lname.get(),
                   'Gender': gender.get()
                 }
                ) 
            cnx.commit()
            cnx.close()

            fname.delete(0, END)
            lname.delete(0, END)
        else :
            messagebox.showerror(title="ERROR", message="The Last name field is empty")
    else:
        messagebox.showerror(title="ERROR", message="The First name field is empty")

def diaglog():
    global imgradio, lbl, path
    photo = filedialog.askopenfile(initialdir="C:/Users/bougu/Downloads", title="Select the Photo", filetypes=(("jpg files","*.jpg"),("png files","*.png"), ("All files","*.*")))
    addbtn.destroy() 
    textlbl.destroy() 
    analybtn['state'] = NORMAL
    dltphbtn['state'] = NORMAL
    path = str(photo)
    path = path.split("'")[1]
    image = Image.open(path)
    image = image.resize((400, 400), Image.LANCZOS)
    imgradio = ImageTk.PhotoImage(image)
    lbl = Label(framephoto, image=imgradio)
    lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

def redraw_selcet():
    btnfont2 = font.Font(family='Courier', weight='bold', size=13)
    lbl.destroy()
    analybtn['state'] = DISABLED
    dltphbtn['state'] = DISABLED
    textlbl = Label(framephoto, text="Select Photo", font=btnfont2)
    addbtn = Button(framephoto,text="+", borderwidth=0, font=btnfont2, command=diaglog)
    textlbl.place(relx=0.5, rely=0.4, anchor=CENTER)
    addbtn.place(relx=0.5, rely=0.5, anchor=CENTER)
    



def forminfo():
    global fname, lname, age, gender
    btnfont3 = font.Font(family='Courier', weight='bold', size=10)
    #inputs             
    fname = Entry(frameinfo, width=20)
    lname = Entry(frameinfo, width=20)
    age = DateEntry(frameinfo, selectmode='day')
    genderfr = LabelFrame(frameinfo, text="Gender", pady=3, background="#96765a", font=btnfont3)
    gender = StringVar()
    gender.set("Female")
    Radiobutton(genderfr, text="Female", variable=gender, value="Female", background="#96765a", font=btnfont3).pack(side=LEFT)
    Radiobutton(genderfr, text="Male", variable=gender, value="Male", background="#96765a", font=btnfont3).pack(side=LEFT)
    
    fname.grid(row= 0, column=1, pady=10)
    lname.grid(row= 1, column=1, pady=10)
    age.grid(row= 2, column=1, pady=10)
    genderfr.grid(row=3, column=0, columnspan=2,sticky=EW, pady=10)
    
    #titles
    fnamelbl = Label(frameinfo, text= "First Name", anchor=W, background="#96765a", font=btnfont3)
    lnamelbl = Label(frameinfo, text= "Last Name", anchor=W, background="#96765a", font=btnfont3)
    agelbl = Label(frameinfo, text= "Birthdate", anchor=W, background="#96765a", font=btnfont3)
    fnamelbl.grid(row= 0, column=0, padx=5, pady=10, sticky=W+E)
    lnamelbl.grid(row= 1, column=0, padx=5, pady=10,sticky=W+E)
    agelbl.grid(row= 2, column=0, sticky=W+E)
    #buttoon
    btnfont = font.Font(family='Courier', weight='bold', size=10)
    btn = Button(frameinfo, text="Submit", command=submit, background="White", font=btnfont, anchor=S)
    btn.grid(row= 4, column=0, columnspan=2, sticky=N+S)
              
def pass_new_patient():
    imglabel.destroy()
    btnnewpatient.destroy()
    btnoldpatient.destroy()
    root.configure(background='white')
    global frameinfo, addbtn, textlbl, analybtn, framephoto,dltphbtn 
    #top bar
    framesup = LabelFrame(root, background="#96765a", borderwidth=0)
    framesup.grid(row=0, column=0, columnspan=2, sticky=EW)  
    btnfont1 = font.Font(family='Courier', weight='bold', size=8)
    btnhelp = Button(framesup, text="Help", borderwidth=0, background="#96765a", font=btnfont1, padx=2)
    btnhelp.grid(row=0, column=0)
    root.grid_columnconfigure(0, weight=1)
    btnexit = Button(framesup, text="Exit", borderwidth=0, background="#96765a", font=btnfont1, command=confexit)
    btnexit.grid(row=0, column=1)
    
    #Fill your patient info
    btnfont2 = font.Font(family='Courier', weight='bold', size=13)
    frameinfo = LabelFrame(root, text="Entry patient informations:", background="#96765a", padx= 50, font=btnfont2)
    frameinfo.grid(row=1, column=0, sticky=NSEW) 
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=0)  
    forminfo()

    
    #Part AI 
    frameanaly = LabelFrame(root, text="Analysis:", padx= 50, pady=50, font=btnfont2, background="white")
    framephoto = LabelFrame(frameanaly, bd="1", relief=SUNKEN)
    textlbl = Label(framephoto, text="Select Photo", font=btnfont2)
    addbtn = Button(framephoto,text="+", borderwidth=0, font=btnfont2, command=diaglog)
    textlbl.place(relx=0.5, rely=0.4, anchor=CENTER)
    addbtn.place(relx=0.5, rely=0.5, anchor=CENTER)
    framephoto.grid(row=0, column=0,columnspan=2, sticky=NSEW) 
    frameanaly.grid_rowconfigure(0, weight=1)
    frameanaly.grid_columnconfigure(0, weight=1) 
    
    analybtn = Button(frameanaly, text="Start analyse", font=btnfont1, state=DISABLED, command=lambda: Pred(path))
    analybtn.grid(row=1, column=0, pady=20)
    
    dltphbtn = Button(frameanaly, text="Delete photo", font=btnfont1, state=DISABLED, command=redraw_selcet)
    dltphbtn.grid(row=1, column=1, pady=20)
    
    frameanaly.grid(row=1, column=1, sticky=NSEW, padx=15, pady=15) 
    root.grid_rowconfigure(1, weight=1) 
    root.grid_columnconfigure(1, weight=1) 




    
def expand():
    global imglabel,i,btnnewpatient,btnoldpatient
    if i <len(imglist):
        imglabel.destroy()
        imglabel = Label(root, image=imglist[i] ,borderwidth=0)
        imglabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        i+=1
        root.after(75,expand)
    else:
        btnfont = font.Font(family='Courier', weight='bold', size=8)
        btnnewpatient = Button(root, text="New patient", background="White", width=55, height=3, font=btnfont, command=pass_new_patient)
        btnnewpatient.place(relx=0.25, rely=0.9, anchor=CENTER)
        btnoldpatient = Button(root, text="Old patient", background="white", width=55, height=3, font=btnfont)
        btnoldpatient.place(relx=0.75, rely=0.9, anchor=CENTER)  

        
root = Tk()
root.title("Ophthalmology Angiography")
root.configure(background='#96765a')
root.iconbitmap("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.ico")
root.geometry("800x500")
root.minsize(600,375)
root.maxsize(1440,900)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((25, 25), Image.LANCZOS)
img = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((50, 50), Image.LANCZOS)
img1 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((75, 75), Image.LANCZOS)
img2 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((100, 100), Image.LANCZOS)
img21 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((125, 125), Image.LANCZOS)
img3 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((150, 150), Image.LANCZOS)
img31 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((175, 175), Image.LANCZOS)
img4 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((200, 200), Image.LANCZOS)
img41 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((225, 225), Image.LANCZOS)
img5 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((250, 250), Image.LANCZOS)
img51 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((275, 275), Image.LANCZOS)
img6 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((300, 300), Image.LANCZOS)
img61 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((325, 325), Image.LANCZOS)
img7 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((350, 350), Image.LANCZOS)
img71 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((375, 375), Image.LANCZOS)
img8 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((400, 400), Image.LANCZOS)
img81 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((425, 425), Image.LANCZOS)
img9 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((450, 450), Image.LANCZOS)
img91 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((475, 475), Image.LANCZOS)
img10 = ImageTk.PhotoImage(image)

image = Image.open("C:/Users/bougu/Documents/GitHub/MyFinalInterface/icon.png")
image = image.resize((500, 500), Image.LANCZOS)
img101 = ImageTk.PhotoImage(image)

imglist = [img, img1, img2, img21, img3, img31, img4, img41, img5, img51, img6, img61, img7, img71, img8, img81, img9, img91, img10, img101]

imglabel = Label(root, image=imglist[0] ,borderwidth=0, anchor=CENTER)
imglabel.place(relx=0.5, rely=0.5, anchor=CENTER)
i=1
expand()


root.mainloop()