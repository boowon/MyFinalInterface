from tkinter import *
from tkinter import messagebox 
from PIL import ImageTk,Image 
from tkinter import font
from tkcalendar import DateEntry
from tkinter import filedialog
import sqlite3
from call_model import cnn_model

maladieName = ''

 
def confexit():
    yesno = messagebox.askyesno(title="Exit", message="Are sure you want to exit?") #return 1 fro yes and 0 for No
    if yesno == 1:
        root.quit()
        
def submit():
    global maladieName, maladie_lbl
    #create a db or connect to it
    
    cnx = sqlite3.connect("basededonne.db")
    cur = cnx.cursor()
    #cur.execute(DROP TABLE IF EXISTS Data_Base_pateients)
    #creat a table
    cur.execute(""" CREATE TABLE IF NOT EXISTS Data_Base_pateients (
              Id_num text primary key,
              First_name text,
              Last_name text,
              Age date,
              Gender text,
              Maladie text
                )
                """)
    #inesrt infos
    if first_name.get()!="":
        if last_name.get()!="":
            if maladieName!="":
                if id_num.get() != "":
                    cur.execute("INSERT INTO Data_Base_pateients VALUES (:Id_num, :First_name, :Last_name, :Age, :Gender, :Maladie)",
                            {
                                'Id_num' : id_num.get(), 
                                'First_name' : first_name.get(),
                                'Last_name' : last_name.get(),
                                'Age' : age.get_date(),
                                'Gender': gender.get(),
                                'Maladie': maladieName
                             }
                         )
                    cnx.commit()
                    cnx.close()
                    first_name.delete(0, END)
                    last_name.delete(0, END)
                    id_num.delete(0, END)
                else:
                    messagebox.showerror(title="ERROR", message="The ID field is empty")    
            else:
                messagebox.showerror(title="ERROR", message="Analyse the image first")
        else :
            messagebox.showerror(title="ERROR", message="The Last name field is empty")
    else:
        messagebox.showerror(title="ERROR", message="The First name field is empty")
        
    maladieName= ''
    maladie_lbl.destroy()
    maladie_lbl = Label(maladie_frame, text=maladieName, font=from_font, background="white", width=20)
    maladie_lbl.pack()

def diaglog():
    global imgradio, lbl, path
    photo = filedialog.askopenfile(initialdir="C:/Users/bougu/Downloads", title="Select the Photo", filetypes=(("jpg files","*.jpg"),("png files","*.png"), ("All files","*.*")))
    add_btn.destroy() 
    text_lbl.destroy() 
    analy_btn['state'] = NORMAL
    dltph_btn['state'] = NORMAL
    path = str(photo)
    path = path.split("'")[1]
    image = Image.open(path)
    image = image.resize((400, 400), Image.LANCZOS)
    imgradio = ImageTk.PhotoImage(image)
    lbl = Label(frame_photo, image=imgradio)
    lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

    

def forminfo():
    global first_name, last_name, age, gender, maladie_lbl, maladie_frame, frame_info, from_font, id_num
    
    from_font = font.Font(family='Courier', weight='bold', size=10)
    
    #inputs             
    id_num = Entry(frame_info, width=20)
    first_name = Entry(frame_info, width=20)
    last_name = Entry(frame_info, width=20)
    age = DateEntry(frame_info, selectmode='day')
    gender_frame = LabelFrame(frame_info, text="Gender", pady=3, background="#96765a", font=from_font)
    gender = StringVar()
    gender.set("Female")
    Radiobutton(gender_frame, text="Female", variable=gender, value="Female", background="#96765a", font=from_font).pack(side=LEFT)
    Radiobutton(gender_frame, text="Male", variable=gender, value="Male", background="#96765a", font=from_font).pack(side=LEFT)
    maladie_frame = LabelFrame(frame_info, text="Diagnostic", pady=3, background="#96765a", font=from_font)
    maladie_lbl = Label(maladie_frame, text=maladieName, font=from_font, background="white", width=20)

    id_num.grid(row= 0, column=1, pady=10)
    first_name.grid(row= 1, column=1, pady=10)
    last_name.grid(row= 2, column=1, pady=10)
    age.grid(row= 4, column=1, pady=10)
    gender_frame.grid(row=5, column=0, columnspan=2,sticky=EW, pady=10)
    maladie_frame.grid(row=6, column=0, columnspan=2,sticky=EW, pady=10)
    maladie_lbl.pack()

    
    #titles
    id_num_lbl = Label(frame_info, text= "Folder Number", anchor=W, background="#96765a", font=from_font)
    first_name_lbl = Label(frame_info, text= "First Name", anchor=W, background="#96765a", font=from_font)
    last_name_lbl = Label(frame_info, text= "Last Name", anchor=W, background="#96765a", font=from_font)
    age_lbl = Label(frame_info, text= "Birthdate", anchor=W, background="#96765a", font=from_font)
    
    id_num_lbl.grid(row= 0, column=0, padx=5, pady=10, sticky=W+E)
    first_name_lbl.grid(row= 1, column=0, padx=5, pady=10, sticky=W+E)
    last_name_lbl.grid(row= 2, column=0, padx=5, pady=10,sticky=W+E)
    age_lbl.grid(row= 4, column=0, sticky=W+E)

    
    #buttoon
    btnfont = font.Font(family='Courier', weight='bold', size=10)
    #
    btn_submit = Button(frame_info, text="Submit", background="White", font=btnfont, anchor=S, command=submit)
    btn_submit.grid(row= 8, column=0, columnspan=2, sticky=N+S)

def search():
    global id_num, first_name, last_name, age, gender_f, maladie_lbl, f_name, l_name, age_val, gender_val, maladieName
    
    f_name = 'XXXXXX'
    l_name = 'YYYYYY'
    age_val = '2002/08/28'
    gender_val = 'Female' 
    maladieName = 'Rien a signaler'
    
    if id_num.get()!='':
        maladie_lbl.destroy()
        first_name.destroy()
        last_name.destroy()
        age.destroy()
        gender_f.destroy()
        first_name = Label(frame_info, text=f_name, font= from_font, background='white' ,width=20)
        last_name = Label(frame_info, text=l_name, font= from_font, background='white', width=20)
        age = Label(frame_info, text=age_val, font= from_font, background='white', width=20)
        gender_f = Label(frame_info, text=gender_val, font= from_font, background='white', width=20 )
        maladie_lbl = Label(maladie_frame, text=maladieName, font=from_font, background="white", width=20)
        maladie_lbl.pack()
        first_name.grid(row= 2, column=1, pady=10)
        last_name.grid(row= 3, column=1, pady=10)
        age.grid(row= 5, column=1, pady=10)
        gender_f.grid(row=6, column=1, padx=5, pady=10, sticky=W+E)
        
    else:
        messagebox.showerror(title="ERROR", message="The ID field is empty")
        
        
def forminfold():
    global first_name, last_name, age, gender_f, maladie_lbl, maladie_frame, frame_info, from_font, id_num, f_name, l_name, age_val, gender_val
    
    f_name = ''
    l_name = ''
    age_val = ''
    gender_val = ''
    id_num = ''
    
    from_font = font.Font(family='Courier', weight='bold', size=10)
    
    #inputs    
    id_num = Entry(frame_info, width=20)         
    first_name = Label(frame_info, text=f_name, font= from_font, background='white' ,width=20)
    last_name = Label(frame_info, text=l_name, font= from_font, background='white', width=20)
    age = Label(frame_info, text=age_val, font= from_font, background='white', width=20)
    gender_frame = Label(frame_info, text="Gender", pady=3, background="#96765a", font=from_font)
    gender_f = Label(frame_info, text=gender_val, font= from_font, background='white', width=20 )
    maladie_frame = LabelFrame(frame_info, text="Diagnostic", pady=3, background="#96765a", font=from_font)
    maladie_lbl = Label(maladie_frame, text=maladieName, font=from_font, background="white", width=20)

    
    
    id_num.grid(row=0, column=1, pady=10)
    first_name.grid(row= 2, column=1, pady=10)
    last_name.grid(row= 3, column=1, pady=10)
    age.grid(row= 5, column=1, pady=10)
    gender_frame.grid(row=6, column=0, pady=10)
    gender_f.grid(row=6, column=1, padx=5, pady=10, sticky=W+E)
    maladie_frame.grid(row=7, column=0, columnspan=2,sticky=EW, pady=10)
    maladie_lbl.pack()

    btnfont = font.Font(family='Courier', weight='bold', size=10)

    
    #titles
    #
    id_num_lbl = Label(frame_info, text= "Folder Number", anchor=W, background="#96765a", font=from_font)
    btn_search = Button(frame_info, text="Rechereche", background="White", font=btnfont, anchor=S, command=search)

    first_name_lbl = Label(frame_info, text= "First Name", anchor=W, background="#96765a", font=from_font)
    last_name_lbl = Label(frame_info, text= "Last Name", anchor=W, background="#96765a", font=from_font)
    age_lbl = Label(frame_info, text= "Birthdate", anchor=W, background="#96765a", font=from_font)
    
    id_num_lbl.grid(row= 0, column=0, padx=5, pady=10, sticky=W+E)
    btn_search.grid(row= 1, column=0, columnspan=2, sticky=N+S)
    first_name_lbl.grid(row= 2, column=0, padx=5, pady=10, sticky=W+E)
    last_name_lbl.grid(row= 3, column=0, padx=5, pady=10,sticky=W+E)
    age_lbl.grid(row= 5, column=0, sticky=W+E)

    
    #buttoon
    #
    btn_submit = Button(frame_info, text="Submit", background="White", font=btnfont, anchor=S, command=submit)
    btn_submit.grid(row= 8, column=0, columnspan=2, sticky=N+S)

def Pred(path):
    global maladieName, maladie_lbl
    maladieName = cnn_model(path)
    print(maladieName)
    maladie_lbl.destroy()
    maladie_lbl = Label(maladie_frame, text=maladieName, font=from_font, background="white", width=20)
    maladie_lbl.pack()
    

def redraw_selcet():
    global maladie_lbl
    maladieName= ''
    btnfont2 = font.Font(family='Courier', weight='bold', size=13)
    lbl.destroy()
    maladie_lbl.destroy()
    maladie_lbl = Label(maladie_frame, text=maladieName, font=from_font, background="white", width=20)
    maladie_lbl.pack()
    analy_btn['state'] = DISABLED
    dltph_btn['state'] = DISABLED
    textlbl = Label(frame_photo, text="Select Photo", font=btnfont2)
    addbtn = Button(frame_photo,text="+", borderwidth=0, font=btnfont2, command=diaglog)
    textlbl.place(relx=0.5, rely=0.4, anchor=CENTER)
    addbtn.place(relx=0.5, rely=0.5, anchor=CENTER)

                
            
#Frame for New Patient  
def pass_new_patient():
    
    #destroy the old frame
    imgLabel.destroy()
    btnNewPatient.destroy()
    btnOldPatient.destroy()
    
    #create a new frame
    root.configure(background='white')
    global frame_info, add_btn, text_lbl, analy_btn, frame_photo, dltph_btn, frame_tool, frame_analy, frame_analy_in
    
    #create a frame for the tools bar
    frame_tool = LabelFrame(root, background="#96765a", borderwidth=0)
    frame_tool.grid(row=0, column=0, columnspan=2, sticky=EW)  
    btn_font1 = font.Font(family='Courier', weight='bold', size=8)
    
    #Help button
    btn_help = Button(frame_tool, text="Help", borderwidth=0, background="#96765a", font=btn_font1, padx=2)
    btn_help.grid(row=0, column=0)
    
    #Exit button
    #, command=confexit
    btn_exit = Button(frame_tool, text="Exit", borderwidth=0, background="#96765a", font=btn_font1)
    btn_exit.grid(row=0, column=1)
    
    #Fill your patient info
    frame_font = font.Font(family='Courier', weight='bold', size=13)
    frame_info = LabelFrame(root, text="Entry patient informations:", background="#96765a", padx= 50, font=frame_font)
    frame_info.grid(row=1, column=0, sticky=NSEW) 
    
    #Form info function
    forminfo()
 
    #Part AI 
    
    #Frame for the photo
    
    frame_analy = LabelFrame(root, background="white")
    frame_analy_in = LabelFrame(frame_analy, text="Analysis:", padx=30, pady=30, font=frame_font, background="white")
    frame_photo = LabelFrame(frame_analy_in, bd="1", relief=SUNKEN)
    text_lbl = Label(frame_photo, text="Select Photo", font=frame_font)
    #
    add_btn = Button(frame_photo,text="+", borderwidth=0, font=frame_font, command=diaglog)
    text_lbl.place(relx=0.5, rely=0.4, anchor="center")
    add_btn.place(relx=0.5, rely=0.55, anchor="center")
    frame_photo.grid(row=0, column=0, sticky=NSEW)
    
    frame_analy_in.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=15, pady=15)
    frame_analy_in.grid_rowconfigure(0, weight=1) 
    frame_analy_in.grid_columnconfigure(0, weight=1)
    

    #Analyse button
    #
    analy_btn = Button(frame_analy_in, text="Start analyse", font=btn_font1, state=DISABLED, command=lambda: Pred(path))
    analy_btn.grid(row=1, column=0, pady=15, ipadx=60)

    
    #Delete photo button
    #
    dltph_btn = Button(frame_analy, text="Delete photo", font=btn_font1, state=DISABLED, command=redraw_selcet)
    dltph_btn.grid(row=1, column=0, pady=20, padx=10, sticky=W+S)
    
    #Return Home button
    return_btn = Button(frame_analy, text="Return Home", font=btn_font1, command=return_home)
    return_btn.grid(row=1, column=1, pady=20, sticky=S)
    
    frame_analy.grid(row=1, column=1, sticky=NSEW) 
    
    frame_analy.grid_rowconfigure(0, weight=1) 
    frame_analy.grid_columnconfigure(0, weight=1)
    
    root.grid_rowconfigure(1, weight=1) 
    root.grid_columnconfigure(1, weight=1) 

#Frame for New Patient  
def pass_old_patient():
    
    #destroy the old frame
    imgLabel.destroy()
    btnNewPatient.destroy()
    btnOldPatient.destroy()
    
    #create a new frame
    root.configure(background='white')
    global frame_info, add_btn, text_lbl, analy_btn, frame_photo, dltph_btn, frame_tool, frame_analy, frame_analy_in
    
    #create a frame for the tools bar
    frame_tool = LabelFrame(root, background="#96765a", borderwidth=0)
    frame_tool.grid(row=0, column=0, columnspan=2, sticky=EW)  
    btn_font1 = font.Font(family='Courier', weight='bold', size=8)
    
    #Help button
    btn_help = Button(frame_tool, text="Help", borderwidth=0, background="#96765a", font=btn_font1, padx=2)
    btn_help.grid(row=0, column=0)
    
    #Exit button
    #, command=confexit
    btn_exit = Button(frame_tool, text="Exit", borderwidth=0, background="#96765a", font=btn_font1)
    btn_exit.grid(row=0, column=1)
    
    #Fill your patient info
    frame_font = font.Font(family='Courier', weight='bold', size=13)
    frame_info = LabelFrame(root, text="Entry patient informations:", background="#96765a", padx= 50, font=frame_font)
    frame_info.grid(row=1, column=0, sticky=NSEW) 
    
    #Form info function
    forminfold()
 
    #Part AI 
    
    #Frame for the photo
    
    frame_analy = LabelFrame(root, background="white")
    frame_analy_in = LabelFrame(frame_analy, text="Analysis:", padx=30, pady=30, font=frame_font, background="white")
    frame_photo = LabelFrame(frame_analy_in, bd="1", relief=SUNKEN)
    text_lbl = Label(frame_photo, text="Select Photo", font=frame_font)
    #
    add_btn = Button(frame_photo,text="+", borderwidth=0, font=frame_font, command=diaglog)
    text_lbl.place(relx=0.5, rely=0.4, anchor="center")
    add_btn.place(relx=0.5, rely=0.55, anchor="center")
    frame_photo.grid(row=0, column=0, sticky=NSEW)
    
    frame_analy_in.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=15, pady=15)
    frame_analy_in.grid_rowconfigure(0, weight=1) 
    frame_analy_in.grid_columnconfigure(0, weight=1)
    

    #Analyse button
    #
    analy_btn = Button(frame_analy_in, text="Start analyse", font=btn_font1, state=DISABLED, command=lambda: Pred(path))
    analy_btn.grid(row=1, column=0, pady=15, ipadx=60)

    
    #Delete photo button
    #
    dltph_btn = Button(frame_analy, text="Delete photo", font=btn_font1, state=DISABLED, command=redraw_selcet)
    dltph_btn.grid(row=1, column=0, pady=20, padx=10, sticky=W+S)
    
    #Return Home button
    return_btn = Button(frame_analy, text="Return Home", font=btn_font1, command=return_home)
    return_btn.grid(row=1, column=1, pady=20, sticky=S)
    
    frame_analy.grid(row=1, column=1, sticky=NSEW) 
    
    frame_analy.grid_rowconfigure(0, weight=1) 
    frame_analy.grid_columnconfigure(0, weight=1)
    
    root.grid_rowconfigure(1, weight=1) 
    root.grid_columnconfigure(1, weight=1) 

#Return Home function
def return_home():
    
    #Return to initial state
    frame_info.destroy()
    frame_photo.destroy()
    frame_tool.destroy()
    frame_analy.destroy()
    root.configure(background='#96765a')
    
    global imgLabel,i,btnNewPatient,btnOldPatient
    i=0
    
    if i <len(imgList):
        imgLabel.destroy()
        imgLabel = Label(root, image=imgList[i] ,borderwidth=0)
        imgLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        i+=1
        root.after(75,expand)
    else:
        btn_font = font.Font(family='Courier', weight='bold', size=8)
        
        #New Patient button
        btnNewPatient = Button(root, text="New patient", background="White", width=55, height=3, font=btn_font, command=pass_new_patient)
        btnNewPatient.place(relx=0.25, rely=0.9, anchor=CENTER)
        
        #Old Patient button
        btnOldPatient = Button(root, text="Old patient", background="white", width=55, height=3, font=btn_font)
        btnOldPatient.place(relx=0.75, rely=0.9, anchor=CENTER)  


#First frame: Home   
def expand():
    global imgLabel,i,btnNewPatient,btnOldPatient
    if i <len(imgList):
        imgLabel.destroy()
        imgLabel = Label(root, image=imgList[i] ,borderwidth=0)
        imgLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        i+=1
        root.after(75,expand)
    else:
        btn_font = font.Font(family='Courier', weight='bold', size=8)
        
        #New Patient button
        btnNewPatient = Button(root, text="New patient", background="White", width=55, height=3, font=btn_font, command=pass_new_patient)
        btnNewPatient.place(relx=0.25, rely=0.9, anchor=CENTER)
        
        #Old Patient button
        btnOldPatient = Button(root, text="Old patient", background="white", width=55, height=3, font=btn_font, command=pass_old_patient)
        btnOldPatient.place(relx=0.75, rely=0.9, anchor=CENTER)  

        
#Create window, title, icon, size        
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

imgList = [img, img1, img2, img21, img3, img31, img4, img41, img5, img51, img6, img61, img7, img71, img8, img81, img9, img91, img10, img101]

imgLabel = Label(root, image=imgList[0] ,borderwidth=0, anchor=CENTER)
imgLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
i=1
expand()


root.mainloop()