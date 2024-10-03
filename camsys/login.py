import tkinter as t
from functools import partial
import json
import os

tk = t.Tk()


tk.title('Login Page')
tk.geometry("300x300")

def admLogin(event) :
    tk.destroy()  # close main window


    # open new window for admin login
    # window name  = admWindow
    admWindow = t.Tk()
    

    admWindow.title("Admin Login")
 
    # sets the geometry 
    admWindow.geometry("400x300")

    #textfield for user ID / userID -> user ID
    userID = t.Label(text="Enter user ID : ", bg='darkblue', fg='yellow', font=("Consolas", 16))  
    userIDEntryBox = t.Entry (admWindow, width=25 , bg='cyan' ,font=("Consolas", 12))

    #textfield for user password / userPass-> user Password
    userPass = t.Label(text="Enter password : ", bg='darkblue', fg='yellow', font=("Consolas", 16))
    userPassEntryBox = t.Entry (admWindow, width=25 , bg='cyan' ,font=("Consolas", 12))

    error = t.Label(admWindow, text="INVALID USER ID/ PASSWORD. TRY AGAIN !!", fg="red", bg="darkblue")

    passCredentials = partial(loginCredentials, userIDEntryBox,userPassEntryBox, "admin_det", error, admWindow)

    #login button - lgnBtn
    lgnBtn = t.Button(admWindow, text="LOGIN", width=25 , bg="yellow", command=passCredentials)

    userID.place(x=35, y=55)
    userIDEntryBox.place(x=36, y=85)

    userPass.place(x=35, y=125)
    userPassEntryBox.place(x=36, y=155)

    lgnBtn.place(x=113.5, y=220)

    admWindow.configure(bg='darkblue')
    admWindow.mainloop()
    

    
 
    
def loginCredentials(user_id,user_pass, user, err, window) : 

    id = user_id.get()
    password = user_pass.get()

    with open('user.json', 'r') as users:
        db_user = json.load(users)

    for i in db_user[user]:
        if ((i["ID"]) == id):
            if (i["password"] == password):
                
                err.place_forget()
                window.destroy()
                if (user == "admin_det"):
                    os.system('python adminHome.py')
                elif (user == "students_det"):
                    os.system(f'python studentHome.py {id}')
    
        else:
            print("wrong pass")
            err.place(x=80, y=270)

    return

    


def stdLogin(event) :
    tk.destroy()  # close main window

    # open new window for student login
    # window name  = stdWindow
    stdWindow = t.Tk()
    stdWindow.title("Student Login")

    #textfield for user ID / userID -> user ID
    userID = t.Label(text="Enter user ID : ", bg='darkblue', fg='yellow', font=("Consolas", 16))  
    userIDEntryBox = t.Entry (stdWindow, width=25 , bg='cyan' ,font=("Consolas", 12))

    #textfield for user password / userPass-> user Password
    userPass = t.Label(text="Enter password : ", bg='darkblue', fg='yellow', font=("Consolas", 16))
    userPassEntryBox = t.Entry (stdWindow, width=25 , bg='cyan' ,font=("Consolas", 12))

    error = t.Label(stdWindow, text="INVALID USER ID/ PASSWORD. TRY AGAIN !!", fg="red", bg="darkblue")

    passCredentials = partial(loginCredentials, userIDEntryBox,userPassEntryBox, "students_det", error, stdWindow)

    #login button - lgnBtn
    lgnBtn = t.Button(stdWindow, text="LOGIN", width=25 , bg="yellow", command=passCredentials)


    userID.place(x=35, y=55)
    userIDEntryBox.place(x=36, y=85)

    userPass.place(x=35, y=125)
    userPassEntryBox.place(x=36, y=155)

    lgnBtn.place(x=113.5, y=220)

    error.place(x=80, y=270)
    error.place_forget()
 
    # sets the geometry 
    stdWindow.geometry("400x300")
    stdWindow.configure(bg='darkblue')
    stdWindow.mainloop()

btnAdminLogin = t.Button(tk, text='Admin Login', width=25, bg="yellow")
btnStudentLogin = t.Button(tk, text='Student Login', width=25,  bg="yellow")


btnAdminLogin.bind( "<Button>", admLogin)
btnStudentLogin.bind("<Button>", stdLogin)

btnAdminLogin.place(x=62.5, y=75)
btnStudentLogin.place(x=62.5, y=120)

# set window background color
tk.configure(bg='darkblue')
tk.mainloop()