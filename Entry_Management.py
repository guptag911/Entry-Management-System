from twilio.rest import Client
import mysql.connector
import tkinter as tk
import smtplib
import tkinter.messagebox
from PIL import ImageTk, Image


### PLEASE FILL THESE DETAILS TO RUN THE SOFTWARE ON YOUR SYSTEM
GmailID="Your Gmail ID"
password="Your Gmail Password"
acc_ID= "Your Account SID from twilio.com/console"
aut_token="Your Auth Token from twilio.com/console"
number="YOur Twilio number"
username="YOur MYSQL username generally root"
sqlpass="Your MYSQL password"


##Popup message when user's information has been stored during check-in time!!
def popup1():
    tk.messagebox.showinfo("SAVED", "Your information has been stored!")

##Popup Message when user has been sucessfully checked out
def popup2():
    tk.messagebox.showinfo("Checked-Out", "You have been successfully checked out!")


##Popup Message when user enter invalid details!!
def popup3():
    tk.messagebox.showerror("Error","Please enter valid details!")

##Popup Message when the same user check's in again without check-out
def popup4():
    tk.messagebox.showerror("Error","You haven't checked out yet!")


#Function To store user data in Mysql database
def save_query(name1, mail1, phone1, name2, mail2, phone2):
    cursor1 = mydb.cursor()
    sql = "INSERT INTO INFORMATION (Vis_Name, Vis_mail, Vis_phone, Host_name, Host_phone,Host_email) VALUES(%s, %s, " \
          "%s, %s, %s, %s) "
    Val = (name1, mail1, phone1, name2, phone2, mail2)
    cursor1.execute(sql, Val)
    mydb.commit()

#Function to send Emails using smtp
def send_email(mail1, name, mail2, number):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GmailID, password)
    msg = name + " is coming to meet you and visitor's Contact Number is " + number
    server.sendmail(mail1, mail2, msg)

#Function to Send Mail to visitor after check out
def send_email_checkout(mail1):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GmailID, password)
    msg = "Here are the details of your meeting.\n"
    cursor3 = mydb.cursor()
    sql = "SELECT Vis_Name FROM INFORMATION WHERE Vis_mail=%s"
    cursor3.execute(sql, (mail1,))
    name = ""
    for i in cursor3:
        name = str(i[0])

    sql = "SELECT Vis_phone FROM INFORMATION WHERE Vis_mail=%s"
    cursor3.execute(sql, (mail1,))
    phone = ""
    for i in cursor3:
        phone = str(i[0])

    sql = "SELECT Check_in FROM INFORMATION WHERE Vis_mail=%s"
    cursor3.execute(sql, (mail1,))
    cintime = ""
    for i in cursor3:
        cintime = str(i[0])

    sql = "SELECT Check_out FROM INFORMATION WHERE Vis_mail=%s"
    cursor3.execute(sql, (mail1,))
    couttime = ""
    for i in cursor3:
        #print(i[0])
        couttime = str(i[0])

    sql = "SELECT Host_Name FROM INFORMATION WHERE Vis_mail=%s"
    cursor3.execute(sql, (mail1,))
    hname = ""
    for i in cursor3:
        hname = str(i[0])

    sql = "SELECT Host_email FROM INFORMATION WHERE Vis_mail=%s"
    cursor3.execute(sql, (mail1,))
    mail2 = ""
    for i in cursor3:
        mail2 = str(i[0])

    details = "Name: " + name + "\nPhone No.: " + phone + "\nCheck-In Time: " + cintime + "\nCheck-Out Time: " + couttime + "\nHost Name: " + hname + "\nAdress: Innovaccer Office"
    #print(details)
    msg += details
    #print(msg)
    server.sendmail(mail2 ,mail1, msg)

##Function to take in user data and check wether entered data is valid or not
def get_data(a, b, c, d, e, f):
    Name_vis = a.get()
    Mail_vis = b.get()
    Phone_vis = c.get()
    Name_host = d.get()
    Mail_host = e.get()
    Phone_host = f.get()

    try:

        send_sms(Phone_host, Name_vis, Phone_vis)
        send_email(Mail_vis, Name_vis, Mail_host, Phone_vis)
        save_query(Name_vis, Mail_vis, Phone_vis, Name_host, Mail_host, Phone_host)
        popup1()
    except:
        popup3()

        
##Function to sand SMS using Twilio
def send_sms(number2, name, number1):
    # Your Account SID from twilio.com/console
    account_sid = str(acc_ID)
    # Your Auth Token from twilio.com/console
    auth_token = str(aut_token)

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+91" + str(number2),
        from_=str(number),
        body=name + " is coming to meet you and visitor's Contact Number is " + number1)

##Function to gather the visitor that haven't checked out yet and update his checkout time
def check_out(mk):
    cursor2 = mydb.cursor()
    val = mk.get()
    sql = "UPDATE INFORMATION SET Check_out=NOW() WHERE Vis_mail=%s and Check_out is NULL"
    cursor2.execute(sql, (val,))
    mydb.commit()
    try:
        send_email_checkout(val)
        popup2()
    except:
        popup3()

mydb = mysql.connector.connect(host="localhost", user=str(username), passwd=str(sqlpass))
cursor = mydb.cursor()

try:
    cursor.execute("CREATE DATABASE entry_info")
    cursor.execute("USE entry_info")
    cursor.execute("CREATE TABLE INFORMATION (Vis_Name varchar(255),Vis_mail varchar(255),Vis_phone varchar(255),"
                   "Check_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Check_out TIMESTAMP, Host_name varchar(255),"
                   "Host_phone varchar(255),Host_email "
                   "varchar(255))")
except:
    cursor.execute("USE entry_info")

###GUI BEGINS!!
class EntryManger(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('500x500')
        self.iconbitmap('inno.ico')
        self.resizable(0,0)             #Disable Maximize Button
        self.config(bg='white')
        self.title("Entry Management Application")
        self._frame = None
        self.switch_frame(PageOne)

    def switch_frame(self, frame_class):
        if self._frame is not None:
            self._frame.destroy()
        new_frame = frame_class(self)
        new_frame.config(bg='white')
        new_frame.pack(expand=1, fill='both')
        self._frame = new_frame

##Start Screen
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="  Visitor Information", fg='orange', font=('Candara 15 bold'),bg='white').grid(row=0)

        l1 = tk.Label(self, text="Visitor's Name: ", font=('Candara 12 bold'),bg='white').grid(row=1)
        # l1.config(font=('Arial', 10, 'Bold'))
        e1 = tk.Entry(self, width=50, selectforeground='white',bd=3)
        e1.grid(row=1, column=2)

        tk.Label(self, text="Visitor's Email:", font=('Candara 12 bold'),bg='white').grid(row=2)
        e2 = tk.Entry(self, width=50, selectforeground='white',bd=3)
        e2.grid(row=2, column=2);

        tk.Label(self, text="Visitor's Phone:", font=('Candara 12 bold'),bg='white').grid(row=3)
        e3 = tk.Entry(self, width=50, selectforeground='white',bd=3)
        e3.grid(row=3, column=2)

        label = tk.Label(self, text="Host Information", fg='orange', font=('Candara 15 bold'),bg='white').grid(row=4)

        tk.Label(self, text="Host's Name:", font=('Candara 12 bold'),bg='white').grid(row=5)
        e4 = tk.Entry(self, width=50, selectforeground='white',bd=3)
        e4.grid(row=5, column=2)

        tk.Label(self, text="Host's Email:", font=('Candara 12 bold'),bg='white').grid(row=6)
        e5 = tk.Entry(self, width=50, selectforeground='white',bd=3)
        e5.grid(row=6, column=2)

        tk.Label(self, text="Host's Phone:", font=('Candara 12 bold'),bg='white').grid(row=7)
        e6 = tk.Entry(self, width=50, selectforeground='white',bd=3)
        e6.grid(row=7, column=2)

        tk.Button(self, text="Check-In", command=lambda: get_data(e1, e2, e3, e4, e5, e6), activebackground='orange', bd=3, width=10, height=2).place(x=180, y=230)
        tk.Button(self, text="Go to Check-Out", command=lambda: master.switch_frame(PageTwo), activebackground='orange', bd=3, width=14, height=2, ).place(x=300, y=230)

        load = Image.open("background.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=300)

##Second Screen
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #tk.Frame(self,width=100, height=100)
        l1 = tk.Label(self, text="Welcome for Check-Out ", fg='orange', font=('Candara 16 bold'), bg='white').place(x=10, y=0)
        tk.Label(self, text="Visitor's Mail ID:", font=('Candara 12 bold'), bg='white').place(x=40, y=45)
        ek = tk.Entry(self, width=52, selectforeground='black',bd=3)
        ek.place(x=160, y=50)
        b1 = tk.Button(self, text="Check-Out", command=lambda: check_out(ek), activebackground='orange', bd=4,width=8, height=2)
        b1.place(x=300, y=80)
        b2 = tk.Button(self, text="Go Back", command=lambda: master.switch_frame(PageOne), activebackground='orange', bd=3,width=8, height=2)
        b2.place(x=200, y=82)

        load = Image.open("backgroud.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=300)

if __name__ == '__main__':
    app = EntryManger()
    app.mainloop()
