# ----------------------------------------------------------------import framework ที่ใช้ -------------------------------------------------------------
import requests # import ตัวดึง api
from tkinter import * # import gui
from tkinter import ttk # import gui
from csv import * # import csv ตัวบันทึกข้อมูลสามารถเปิดใน excel ได้ฮ้าฟฟู่ว
# import ttkbootstrap as ttk #  วิธีติดตั้ง pip install ttkbootstrap # ยังไม่ได้ใช้เอาไว้ตกแต่ง
# from ttkbootstrap.constants import *  # วิธีติดตั้ง pip install ttkbootstrap # ยังไม่ได้ใช้เอาไว้ตกแต่ง
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#------------------------- ดึง api ชื่อสกุลเงิน -----------------------------------------------------------------------------
url = "https://v6.exchangerate-api.com/v6/ecb1c418cf63e6c636a628e4/codes" # api รายชื่อสกุลต่างๆ ดึงเอามาจาก https://www.exchangerate-api.com/

# เริ่มต้นดึง api
response = requests.get(url) # ดึง api ผ่าน url
data = response.json() #แปลงเป็นข้อมูลที่ดึงเป็น json แล้วมาใช้งานได้

rates = data['supported_codes'] # ดึงข้อมูลจากฐานข้อมูลชื่อสกุลเงินจาก api

namerates = []  #array ชื่อสกุลเงิน ที่เก็บไว้ใช้ ********************

namerates.sort() #นำรายชื่อในarrayมาเรียงตัวอักษร A-Z จะได้ index ตรงกับค่าเงิน

for i in rates: # วนลูป api เข้า array
    namerates.append(i[0]) # ดึง api แค่ชื่อสกุลเงิน จาก index 0

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------- ส่วน gui ----------------------------------------------------------------------------
idlist = 0 # ค่าเริ่มต้นของ id ในฐานข้อมูล table ที่จะแสดงค่าต่างๆ
alllist = [] # array เก็บข้อมูลทั้งหมด เช่น พวก รายชื่อสินค้า จำนวนสินค้า ราคาสินค้าต่างๆทั้งค่าที่แปลงแล้วและไม่แปลง
def main(returnpage=False): ##หน้าแรกใส่กำหนดชื่อหัวข้อทริป
    global alllist,idlist # ทำให้เป็น publice จะได้เปลี่ยนค่าข้างบนที่ประกาศไว้ได้
    if returnpage: #เช็คว่าได้มีการย้อนกลับของหน้า addmenu
        addmenuwin.destroy() #ปิดหน้าต่าง addmenu
        idlist = 0 #ให้ค่าเริ้มต้นเท่ากับ 0 ในฐานข้อมูลตอนกลับมา
        alllist.clear() #ล้างค่าทั้งหมดที่เก็บไว้ตอนกลับมา
    try:
        global mywin
        mywin = Tk()
        mywin.iconbitmap('favicons.ico')
        mywin.title("โปรแกรมคำนวณค่าใช้จ่ายเที่ยวที่ต่างๆในต่างประเทศที่ต่างๆในต่างประเทศ")
        mywin.minsize(400,200)
        mywin.maxsize(400,200)

        Trip = StringVar() #ตัวแปรหัวข้อชื่อทริป

        title = Label(mywin,text="หัวข้อชื่อทริปเที่ยว" , font=20,fg="#1798f5")
        title.pack(side=TOP, pady=30)
        entry1 = Entry(mywin,textvariable=Trip,width=40)
        entry1.pack()

        nextbtn = Button(mywin,text="ต่อไป",command=lambda: addmenu(Trip),bg="#4db5ff",fg="white") #กดไปหน้าต่อไปเรียกให้ฟังชั้น addmenu (หน้าเมนูหน้าเพิ่มข้อมูลต่างๆ)
        nextbtn.pack(side=RIGHT,padx=10,pady=12)
        closebtn = Button(mywin,text="ปิดหน้าต่าง", command=mywin.destroy,bg="#4db5ff",fg="white") # กดปิดหน้าต่าง
        closebtn.pack(side=LEFT,padx=10,pady=10)
        mywin.mainloop()
    except Exception as error:
        print(error)


def addmenu(Trip,returnpage=False): #หน้าเมนูหน้าเพิ่มข้อมูลต่างๆ
    global Triptitle,namestock,pricestock,countstock,menuitem,addmenuwin
    if not returnpage:
        Triptitle = Trip.get()
    if Triptitle:
        if returnpage == True:
            rendermenu.destroy()
        else:
            mywin.destroy()

        addmenuwin= Tk()
        addmenuwin.iconbitmap('favicons.ico')
        addmenuwin.title("โปรแกรมคำนวณค่าใช้จ่ายเที่ยวที่ต่างๆในต่างประเทศ")
        addmenuwin.minsize(800,500)
        addmenuwin.maxsize(800,500)

# ---------------------------------- เมนูเพิ่มรายการ list สินค้า -------------------------------
        
        namestock = StringVar()
        countstock = StringVar()
        pricestock = StringVar()
        countstock.set("0")
        pricestock.set("0")

        titlemenu= Label(addmenuwin,text="ชื่อทริป  "+Triptitle, font=20,fg="#1798f5")
        titlemenu.place(x=50,y=70)


        Label(addmenuwin,text="ชื่อรายการสินค้า").place(x=60,y=120)
        Entry(addmenuwin,textvariable=namestock).place(x=40,y=150)

        Label(addmenuwin,text="จำนวนสินค้า").place(x=70,y=190)
        Entry(addmenuwin,textvariable=countstock).place(x=40,y=220)

        Label(addmenuwin,text="ราคาสินค้า").place(x=75,y=260)
        Entry(addmenuwin,textvariable=pricestock).place(x=40,y=290)

        Button(text="เพิ่มรายการสินค้า",command=addlistmenu,bg="#4db5ff",fg="white").place(x=62,y=340)

        Button(text="ล้างรายการสินค้าทั้งหมด",command=clearlist,bg="#4db5ff",fg="white").place(x=45,y=380)

# ----------------------------------รายการ list สินค้า-------------------------------------------------
        Label(addmenuwin,text="รายการสินค้า" , font=20,fg="#1798f5").place(x=450,y=30)

        addmenuwin_frame = Frame(addmenuwin)
        addmenuwin_frame.place(x=285,y=70)

        #scrollbar
        addmenuwin_scroll = Scrollbar(addmenuwin_frame)
        addmenuwin_scroll.pack(side=RIGHT, fill=Y)

        addmenuwin_scroll = Scrollbar(addmenuwin_frame,orient='horizontal')
        addmenuwin_scroll.pack(side= BOTTOM, fill=X)

        menuitem = ttk.Treeview(addmenuwin_frame,yscrollcommand=addmenuwin_scroll.set, xscrollcommand =addmenuwin_scroll.set)

        menuitem.pack()
        addmenuwin_scroll.config(command=menuitem.yview)
        addmenuwin_scroll.config(command=menuitem.xview)

        

        menuitem['columns'] = ('idlist', 'namelist', 'countlist', 'pricelist')

        menuitem.column("#0", width=0,  stretch=NO)
        menuitem.column("idlist",anchor=CENTER, width=100)
        menuitem.column("namelist",anchor=CENTER,width=120)
        menuitem.column("countlist",anchor=CENTER,width=100)
        menuitem.column("pricelist",anchor=CENTER,width=100)

        menuitem.heading("#0",text="",anchor=CENTER)
        menuitem.heading("idlist",text="ไอดี",anchor=CENTER)
        menuitem.heading("namelist",text="ชื่อรายการสินค้า",anchor=CENTER)
        menuitem.heading("countlist",text="จำนวนสินค้า",anchor=CENTER)
        menuitem.heading("pricelist",text="ราคาสินค้า",anchor=CENTER)

        if returnpage: # ถ้าย้อนกลับจากหน้า render มาให้มาแสดงเหมือนเดิม
            for i in range(len(alllist)):
                menuitem.insert(parent='',index='end',iid=i,text='',
                values=(i,alllist[i][0],alllist[i][1],alllist[i][2]))

        menuitem.pack()

# -------------------------------- เลือกสกุลเงิน --------------------------------------------
            
        global coinconvert1,coinconvert2,countpeople

        coinconvert1 = StringVar(addmenuwin) # ตัวแปรชื่อสกุลเริ่มต้น
        coinconvert1.set(namerates[146]) # ค่าเริ่มต้นชื่อสกุล

        coin1 = ttk.Combobox(addmenuwin, textvariable=coinconvert1, values=namerates) # values ดึงข้อมูลชื่อสกุลเงินทั้งหมดที่เคยประกาศไว้แล้วในตัวแปร array namerates
        coin1.place(x=330,y=320,width=100)

        Label(addmenuwin,text="Convert to -->", fg="#1798f5").place(x=450,y=320)

        coinconvert2 = StringVar(addmenuwin) # ตัวแปรชื่อสกุลที่จะเปลี่ยน
        coinconvert2.set(namerates[134]) # ค่าเริ่มต้นชื่อสกุลที่จะเปลี่ยน

        coin2 = ttk.Combobox(addmenuwin, textvariable=coinconvert2, values=namerates) # values ดึงข้อมูลชื่อสกุลเงินทั้งหมดที่เคยประกาศไว้แล้วในตัวแปร array namerates
        coin2.place(x=560,y=320,width=100)

        countpeople = StringVar() # ตัวแปรจำนวนคนที่จะหารค่าใช้จ่ายทั้งหมด
        countpeople.set("0") # ค่าเริ่มต้นจำนวนคนหาร แต่ถ้าใส่จริงห้ามเป็น 0 จะให้ทำเกิน ZeroError แต่ ดัก error ไว้แล้วฮ้าฟฟู่ว
        Label(addmenuwin,text="โปรป้อนจำนวนคนที่จะหารค่าใช้จ่ายทั้งหมด", fg="#1798f5").place(x=285,y=370)
        Entry(addmenuwin,textvariable=countpeople).place(x=500,y=370)



        nextbtn = Button(addmenuwin,text="ต่อไป",bg="#4db5ff",fg="white",command=render) #กดไปหน้าต่อไปเรียกให้ฟังชั้น render
        nextbtn.place(x=750,y=450)
        prevbtn = Button(addmenuwin,text="ย้อนกลับ",command=lambda: main(returnpage=True),bg="#4db5ff",fg="white") #ย้อนกลับไปหน้าตั้งชื่อทริปแล้วให้รีเซ็ทข้อมูลต่างๆที่เพิ่มไป
        prevbtn.place(x=10,y=450)


        addmenuwin.mainloop()

    else:
        # ------------------------------ เช็คหัวข้อทริปว่ามีไหม ------------------
        mywin.destroy()

        alert = Tk()
        alert.iconbitmap('favicons.ico')
        alert.title("ERROR")
        alert.minsize(400,200)
        alert.maxsize(400,200)
        
        title = Label(alert,text="กรุณาใส่ชื่อหัวข้อทริปครั้งนี้ก่อน!!",font=20)
        title.pack(pady=50)
        btn = Button(alert, text="กลับไปตั้งหัวข้อทริป", command=alert.destroy,bg="#4db5ff",fg="white")
        btn.pack()

        alert.mainloop()
        main()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def render(): #หน้าเมนูสรุปค่าใช้จ่าย
    try:
        if alllist:
            if int(countpeople.get()) > 0:
                    addmenuwin.destroy()
                    apicoinconvert()

                    # --------------------------------- 
                    for i in range(len(alllist)): # loop ใส่ข้อมูลเพิ่มเติมเข้า array alllist
                        alllist[i].append(round(float(alllist[i][2])*coinrates2,2)) #เก็บค่าเงินที่แปลงเป็นสกุลเงินที่ต้องการแล้ว coinrates2 คือ ค่าเรทของสกุลเงินที่แปลง
                        alllist[i].append(countpeople.get()) #เก็บค่าจำนวนคนหารทั้งหมด
                        alllist[i].append(round(float(alllist[i][2])/int(countpeople.get()),2)) #ค่าเงินที่ยังไม่แปลงแล้วนำมาหาร
                        alllist[i].append(round((float(alllist[i][2])*coinrates2)/int(countpeople.get()),2)) #ค่าเงินที่แปลงแล้วนำมาหาร
                    #---------------------------------
                    

                    # ------------------------------------------ ตารางสรุปค่าใช้จ่ายฮ้าฟฟู่ว ------------------------------
                    global rendermenu,sumpricelist1,sumpricelist2,sumpricelist3,sumpricelist4
                    rendermenu = Tk()
                    rendermenu.iconbitmap('favicons.ico')
                    rendermenu.title("โปรแกรมคำนวณค่าใช้จ่ายเที่ยวที่ต่างๆในต่างประเทศ")
                    rendermenu.minsize(1000,450)
                    rendermenu.maxsize(1000,450)

                    Label(rendermenu,text="ตารางสรุปค่าใช้จ่ายทั้งหมด" , font=20,fg="#1798f5").place(x=400,y=30)

                    rendermenu_frame = Frame(rendermenu)
                    rendermenu_frame.place(x=100,y=70)

                    #scrollbar
                    rendermenu_scroll = Scrollbar(rendermenu_frame)
                    rendermenu_scroll.pack(side=RIGHT, fill=Y)

                    rendermenu_scroll = Scrollbar(rendermenu_frame,orient='horizontal')
                    rendermenu_scroll.pack(side= BOTTOM, fill=X)

                    rendermenuitem = ttk.Treeview(rendermenu_frame,yscrollcommand=rendermenu_scroll.set, xscrollcommand =rendermenu_scroll.set)

                    rendermenuitem.pack()
                    rendermenu_scroll.config(command=rendermenuitem.yview)
                    rendermenu_scroll.config(command=rendermenuitem.xview)

                        

                    rendermenuitem['columns'] = ('idlist', 'namelist', 'countlist', 'pricelist1', 'pricelist2', 'countpeoplelist', 'pricelistpeople1' , 'pricelistpeople2')

                    rendermenuitem.column("#0", width=0,  stretch=NO)
                    rendermenuitem.column("idlist",anchor=CENTER, width=80)
                    rendermenuitem.column("namelist",anchor=CENTER,width=120)
                    rendermenuitem.column("countlist",anchor=CENTER,width=80)
                    rendermenuitem.column("pricelist1",anchor=CENTER,width=100)
                    rendermenuitem.column("pricelist2",anchor=CENTER,width=100)
                    rendermenuitem.column("countpeoplelist",anchor=CENTER,width=80)
                    rendermenuitem.column("pricelistpeople1",anchor=CENTER,width=120)
                    rendermenuitem.column("pricelistpeople2",anchor=CENTER,width=120)

                    rendermenuitem.heading("#0",text="",anchor=CENTER)
                    rendermenuitem.heading("idlist",text="ไอดี",anchor=CENTER)
                    rendermenuitem.heading("namelist",text="ชื่อรายการสินค้า",anchor=CENTER)
                    rendermenuitem.heading("countlist",text="จำนวนสินค้า",anchor=CENTER)
                    rendermenuitem.heading("pricelist1",text="ราคาสินค้า "+str(coinconvert1.get()),anchor=CENTER)
                    rendermenuitem.heading("pricelist2",text="ราคาสินค้า "+str(coinconvert2.get()),anchor=CENTER)
                    rendermenuitem.heading("countpeoplelist",text="จำนวนคนหาร",anchor=CENTER)
                    rendermenuitem.heading("pricelistpeople1",text="ราคาสินค้าหาร "+str(coinconvert1.get()),anchor=CENTER)
                    rendermenuitem.heading("pricelistpeople2",text="ราคาสินค้าหาร "+str(coinconvert2.get()),anchor=CENTER)

                    arraysumpricelist1 = [] #array ราคาสินค้าUSD
                    arraysumpricelist2 = [] #array ราคาสินค้าTHB
                    arraysumpricelist3 = [] #array ราคาสินค้าหารUSD
                    arraysumpricelist4 = [] #array ราคาสินค้าหารTHB

                    for i in range(len(alllist)):
                        rendermenuitem.insert(parent='',index='end',iid=i,text='',
                        values=(i,alllist[i][0],alllist[i][1],alllist[i][2],alllist[i][3],alllist[i][4],alllist[i][5],alllist[i][6]))
                        arraysumpricelist1.append(round(float(alllist[i][2]),2))
                        arraysumpricelist2.append(round(float(alllist[i][3]),2))
                        arraysumpricelist3.append(round(float(alllist[i][5]),2))
                        arraysumpricelist4.append(round(float(alllist[i][6]),2))

                    sumpricelist1 = round(sum(arraysumpricelist1),2) # ราคาสินค้าUSD ที่รวมแล้วเป็นค่าใช้จ่ายสุทธิ
                    sumpricelist2 = round(sum(arraysumpricelist2),2) # ราคาสินค้าTHB ที่รวมแล้วเป็นค่าใช้จ่ายสุทธิ
                    sumpricelist3 = round(sum(arraysumpricelist3),2) # ราคาสินค้าหารUSD ที่รวมแล้วเป็นค่าใช้จ่ายสุทธิ
                    sumpricelist4 = round(sum(arraysumpricelist4),2) # ราคาสินค้าหารTHB ที่รวมแล้วเป็นค่าใช้จ่ายสุทธิ

                    rendermenuitem.pack()

                    Label(rendermenu,text=(str(coinconvert1.get())+" RATES : "+str(round(coinrates1,2))) ,fg="#1798f5").place(x=100,y=320)
                    Label(rendermenu,text=(str(coinconvert2.get())+" RATES : "+str(round(coinrates2,2))) ,fg="#1798f5").place(x=200,y=320)
                    Label(rendermenu,text=("จำนวนคนหารทั้งหมด : "+str(countpeople.get())) ,fg="#1798f5").place(x=100,y=345)
                    Label(rendermenu,text=("ราคาสินค้ารวมทั้งหมด "+str(coinconvert1.get())+": "+str(sumpricelist1)) ,fg="#1798f5").place(x=530,y=320)
                    Label(rendermenu,text=("ราคาสินค้ารวมทั้งหมด "+str(coinconvert2.get())+": "+str(sumpricelist2)) ,fg="#1798f5").place(x=530,y=345)
                    Label(rendermenu,text=("ราคาสินค้ารวมหารทั้งหมด "+str(coinconvert1.get())+": "+str(sumpricelist3)) ,fg="#1798f5").place(x=710,y=320)
                    Label(rendermenu,text=("ราคาสินค้ารวมหารทั้งหมด "+str(coinconvert2.get())+": "+str(sumpricelist4)) ,fg="#1798f5").place(x=710,y=345)

                    nextbtn = Button(rendermenu,text="บันทึกข้อมูลและปิดหน้าต่าง",bg="#4db5ff",fg="white",command=addlisttocsv)
                    nextbtn.place(x=860,y=400)
                    prevbtn = Button(rendermenu,text="ย้อนกลับ",command=lambda: addmenu(Triptitle,returnpage=True),bg="#4db5ff",fg="white")
                    prevbtn.place(x=10,y=400)

                    rendermenu.mainloop()
            else:
                countpeople.set("กรุณาใส่ตัวเลขที่มากกว่า 0")
        else:
            alert = Tk()
            alert.iconbitmap('favicons.ico')
            alert.title("ERROR")
            alert.minsize(400,200)
            alert.maxsize(400,200)
                
            title = Label(alert,text="กรุณาใส่ข้อมูลให้ครบก่อน!!!",font=20)
            title.pack(pady=50)
            btn = Button(alert, text="ตกลง", command=alert.destroy,bg="#4db5ff",fg="white")
            btn.pack()
            alert.mainloop()
    except Exception:
        countpeople.set("กรุณาใส่ตัวเลขจำนวนเต็ม")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addlistmenu(): #ฟังชั่นย่อยเพิ่มข้อมูลแต่ละอันของหน้า เพิ่มเมนู addmenu()
    global alllist,idlist
    if namestock.get() and countstock.get() and pricestock.get(): #ถ้าได้รับค่าทั้งหมดมาจริงให้เลิกใช้งาน
        try:
            if int(countstock.get()) > 0 and float(pricestock.get()) >= 0: #เช็คว่าเป็นเท่า 0 หรือ น้อยกว่า 0 ไหม
                countconveted = int(countstock.get())
                priceconveted = float(pricestock.get())
                # -------------- ทำเป็น array 2มิติแล้วเพิ่มเข้าแต่ละอัน ----------------
                alllist.append([])
                alllist[idlist].append(namestock.get())
                alllist[idlist].append(countconveted)
                alllist[idlist].append(round(priceconveted,2))
                # ------------------------------------------------
                for i in range(idlist,len(alllist)): #loop เพิ่มดึงข้อมูลจากที่เพิ่มในมูลในalllist จากการทำarray 2มิติเข้าตาราง
                    menuitem.insert(parent='',index='end',iid=idlist,text='', #insertข้อมูลเข้าตารางของ addmenu()
                    values=(idlist,alllist[i][0],alllist[i][1],alllist[i][2]))  #การดึงarray 2มิติ
                idlist = idlist + 1 #ให้ id เพิ่มไปเรื่อยๆจากที่เป็น 0 ที่เคยประกาศไว้ข้างบน
            else:
                if int(countstock.get()) <= 0:
                    countstock.set("กรุณาใส่จำนวนมากกว่า 0")
                elif float(pricestock.get()) < 0:
                    pricestock.set("กรุณาใส่จำนวนมากกว่าเท่ากับ 0")
        except Exception:
            try:
                countconveted = int(countstock.get())
            except Exception:
                countstock.set("กรุณาใส่ตัวเลขจำนวนเต็ม")
            try:
                priceconveted = float(pricestock.get())
            except Exception:
                pricestock.set("กรุณาใส่ตัวเลข")
    else:
        # ------------------------------ เช็คหัวข้อทริปว่ามีไหม ------------------
        alert = Tk()
        alert.iconbitmap('favicons.ico')
        alert.title("ERROR")
        alert.minsize(400,200)
        alert.maxsize(400,200)
            
        title = Label(alert,text="กรุณาใส่รายการให้ครบ!!",font=20)
        title.pack(pady=50)
        btn = Button(alert, text="ตกลง", command=alert.destroy)
        btn.pack()

        alert.mainloop()
        addmenu()


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clearlist(): #ล้างค่าทั้งหมดที่บันทึกไว้ในตาราง
    global idlist
    alllist.clear() #ล้างข้อมูลในarray alllist ทั้งหมด
    for item in menuitem.get_children(): #loop ดึง idlist ที่เคยกำหนดไว้
        menuitem.delete(item) #ลบidlist แต่ละอัน เช่นถ้ามี 0 1 จะลบทั้ง 0 1
    idlist = 0 #ลบเสร็จกำหนดให้เป็น 0 เพิ่มไปใช้ใหม่ตอนหลัง

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def apicoinconvert(): #ดึงค่าเรทเงินของประเทศนั้นๆและหาค่าเรทให้ตรงกับประเทศที่จะแปลง
        # ---------------------------------- ดึง api เรทค่าเงิน จาก exchangerate  ----------------------------------------
    # The API endpoint
    url = "https://v6.exchangerate-api.com/v6/ecb1c418cf63e6c636a628e4/latest/" # api เรทเงิน จะดึงเอามาจาก https://www.exchangerate-api.com/

    global basecoin 
    basecoin = coinconvert1.get() #ค่าเงินเริ่มต้นที่ต้องการจะเปลี่ยน

    # A GET request to the API
    response = requests.get(url+basecoin) # ดึง api
    data = response.json() #แปลงเป็นไฟล์อ่านง่ายเป็น json จากมาใช้งานจริง

    ratesdata = data['conversion_rates'] # ดึงข้อมูลฐานข้อมูลค่าเงินจากapi
    sortrates = dict(sorted(ratesdata.items())) #จัดเรียงค่าข้อมูลให้ตรงกับ index ของประเทศ
    rates = [] #จำนวนเรทแลกเปลี่ยนสกุลเงิน

    for i in sortrates: # loop ดึง api เข้า arry
        rates.append(ratesdata[i]) # ใส่เรทสกุลเงินทั้งหมดเข้า array rates

    index1 = namerates.index(coinconvert2.get()) #หา index namerates ที่ต้องการเปลี่ยน ใน rates
    index2 = namerates.index(coinconvert1.get()) #หา index namerates ค่าเริ่มต้น ใน rates
    global coinrates2,coinrates1
    coinrates1 = rates[index2] #ค่าเริ่มต้นเรทเงิน
    coinrates2 = rates[index1]  #ค่าที่จะแปลงเรทเงิน

    # --------------------------------------------- จบการดึง api ----------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addlisttocsv(): #อัพเดตรายการในสินค้าในcsv
    rendermenu.destroy()

    with open(("Trip/"+"Trip-"+Triptitle+".csv"),'w',encoding='utf-8') as additemtocsv:
        w = writer(additemtocsv,lineterminator="\n")
        w.writerow(['รายการสินค้า','จำนวนสินค้า','ราคาสินค้า'+str(coinconvert1.get()),'ราคาสินค้า'+str(coinconvert2.get()),'จำนวนคนหาร','ราคาสินค้าหาร'+str(coinconvert1.get()),'ราคาสินค้าหาร'+str(coinconvert2.get())])
        w.writerows(alllist)
        w.writerow([str(coinconvert1.get())+" RATES",str(coinconvert2.get())+" RATES","จำนวนคนหารทั้งหมด","ราคาสินค้ารวมทั้งหมด "+str(coinconvert1.get()),"ราคาสินค้ารวมทั้งหมด "+str(coinconvert2.get()),"ราคาสินค้ารวมหารทั้งหมด "+str(coinconvert1.get()),"ราคาสินค้ารวมหารทั้งหมด "+str(coinconvert2.get())])
        w.writerow([round(coinrates1,2),round(coinrates2,2),countpeople.get(),sumpricelist1,sumpricelist2,sumpricelist3,sumpricelist4])

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------เริ่มต้นใช้ง่าย-----------------------------------------------------------------------------------------------
print("--------------------")
print("โปรแกรมคำนวณค่าใช้จ่ายเที่ยวที่ต่างๆในต่างประเทศ")
print("Start")
print("--------------------")
main()
print("--------------------")
print("โปรแกรมคำนวณค่าใช้จ่ายเที่ยวที่ต่างๆในต่างประเทศ")
print("END")
print("--------------------")
    