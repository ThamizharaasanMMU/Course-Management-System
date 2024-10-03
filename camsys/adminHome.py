import tkinter as t
from tkinter.ttk import *
from functools import partial
from tkcalendar import DateEntry
from datetime import datetime as dt
import random
import json
import string
import os

today_date = dt.now()

tk = t.Tk()


tk.title('Admin Homepage')
tk.geometry("900x650")

def userJson():
    with open('user.json', 'r') as users:
        db_user = json.load(users)
    
    user = []
    for i in db_user["students_det"]:
        user.append ({
            "ID" : i["ID"],
            "name" : i["name"],
            "age" : i["age"],
            "password" : i["password"],
            "courses" : i["courses"]

        })
    return user

def user_detJson():
    with open('user.json', 'r') as users:
        db_user = json.load(users)
    
    return db_user


def courseJson():
    with open('course.json', 'r') as course:
        db_course = json.load(course)
    
    courses = []
    for i in db_course["course_det"]:
        courses.append ({
            "CourseID" : i["CourseID"],
            "LecturerName" : i["LecturerName"],
            "CourseName" : i["CourseName"],
            "Students" : i["Students"],
            "ClassCapacity" : i["ClassCapacity"],
            "CourseStartDate" : i["CourseStartDate"],
            "CourseEndDate" : i["CourseEndDate"]

        })
    return courses  

def course_detJson():
    with open('course.json', 'r') as course:
        db_course = json.load(course)

    return db_course

    
 
 
# print(len(courseJson()))
# print(courseJson()[len(courseJson())-1]["CourseID"])


# The function generates a random ID number between 20000 and 29999 and checks if it already exists in
# a user JSON file, recursively generating a new ID if it does.
# :return: a random ID number that is not already present in the userJson data.
    
def randomID() :
    num = random.randint(20000,29999)
    user = userJson()

    for i in user:
        if (num != i["ID"]):
            return num
        elif( num == i["ID"]):
            return randomID()



   
# The function "randomPassword" generates a random password consisting of letters, digits, and special
# characters.
# :return: a randomly generated password.
   
def randomPassword() :

    char = string.ascii_letters + string.digits + "@" + "#" + "$"
    password = ""

    for i in range (8):
        password += random.choice(char)

    return password


# print(randomPassword())

def logOut():
    tk.destroy()
    os.system('python login.py')


        
def addStudent(name, age, table):
    new_id= randomID()
    new_pass = randomPassword()

    # if (name.get() != "" and age.get() != ""):
    #     table.insert(parent='', index='end', iid=new_id,  values=(new_id, name.get().upper(), age.get(), new_pass))
    existingName = ""
    user = userJson()
    for i in user:
        if (i["name"] == name.get().upper() ):
            existingName = i["name"]
            print("Name already exist")

    if (existingName == ""):
        if (name.get() != "" and age.get() != ""):
            table.insert(parent='', index='end', iid=new_id,  values=(new_id, name.get().upper(), age.get(), new_pass))
            
                        
            dictionary = {
                "name": name.get().upper(),
                "age": age.get(),
                "ID": str(new_id),
                "password": new_pass,
                "courses": []
            }

        with open('user.json', 'r') as f_student:
            db_student = json.load(f_student)

        db_student['students_det'].append(dictionary)

        with open('user.json', 'w') as f_student:
            json.dump(db_student, f_student, indent=4)
  

    name.delete(0,t.END)
    name.insert(0, "")

    age.delete(0,t.END)
    age.insert(0,"")
    
    return



def selectStudent(event):
    userNameEntryBox.delete(0,t.END)
    ageEntryBox.delete(0,t.END)

    selected = students.focus()
    values = students.item(selected, 'values')

    userNameEntryBox.insert(0, values[1])
    ageEntryBox.insert(0,values[2])



def updateStudent():

    selected = students.focus()
    values = students.item(selected, 'values')

    if (userNameEntryBox.get() != "" or ageEntryBox.get() != ""):
        students.item(selected, text="", values=(values[0], userNameEntryBox.get().upper(), ageEntryBox.get(), values[3]))
        
        with open('user.json', 'r') as f_student:
            db_student = json.load(f_student)

        for i in range (len(db_student['students_det'])):
            if (db_student['students_det'][i]["ID"] == values[0] ):
                db_student['students_det'][i]["name"] = userNameEntryBox.get().upper()
                db_student['students_det'][i]["age"] = ageEntryBox.get()




        with open('user.json', 'w') as f_student:
            json.dump(db_student, f_student, indent=4)

    userNameEntryBox.delete(0,t.END)
    ageEntryBox.delete(0,t.END)


def deleteStudent():
    selected = students.focus()
    values = students.item(selected, 'values')
    students.delete(selected)
    
    db_user = user_detJson()
    db_student = db_user["students_det"]

    for i in range (len(db_student)):
        if (db_student[i]["ID"] == values[0] ):
            db_student.remove(db_student[i])
            break


    with open('user.json', 'w') as f_student:
        json.dump(db_user, f_student, indent=4)

    
    userNameEntryBox.delete(0,t.END)
    ageEntryBox.delete(0,t.END)


def viewStudentBtn() :
    viewStudents_frame.place(x=0,y=65)
    createCourse_frame.place_forget()
    viewCourse_frame.place_forget()
    return



def createCourseButton():
    createCourse_frame.place(x=0,y=65)
    viewStudents_frame.place_forget()
    viewCourse_frame.place_forget()
    return


def viewCourseBtn():
    viewCourse_frame.place(x=0,y=65)
    viewStudents_frame.place_forget()
    createCourse_frame.place_forget()
    return





############## BUTTON FRAME ######################################################################################

buttons_frame = t.LabelFrame(tk, width=900, height=50, bg='darkblue', font=(16), fg="yellow")
buttons_frame.place(x=0, y=5)


view_student = t.Button(buttons_frame, text="View Students", width=15,  bg="yellow", command=viewStudentBtn)
view_student.place(x = 70, y=10)

create_course = t.Button(buttons_frame, text="Create Course", width=15,  bg="yellow", command=createCourseButton)
create_course.place(x=300, y=10)


view_course = t.Button(buttons_frame, text="View Course", width=15,  bg="yellow", command=viewCourseBtn)
view_course.place(x=500, y=10)

logOut = t.Button(buttons_frame, text="Logout", width=15,  bg="yellow", command=logOut)
logOut.place(x=730, y=10)

#####################################################################################################################

# with open("course.json",'r') as course:
#     data = json.load(course)
#     print(data['course_det'])

# with open('course.json', 'w') as course:
#     data = json.load(course)
#     print(data['course_det'])


#################      WORK FRAME - View Students     ###############################################################

viewStudents_frame = t.LabelFrame(tk, width=900, height=565, bg='darkblue')
viewStudents_frame.place(x=0,y=65)
viewStudents_frame.place_forget()

style = Style()
style.theme_use("clam")
style.configure("Treeview",  fieldbackground="cyan", background="cyan")

students = Treeview(viewStudents_frame, style="Treeview")

students.place(x=40,y=30)

students['column'] = ('userID', 'name', 'age', 'password')

students.column("#0", width=0)

students.column("userID",anchor='center')
students.column("name", anchor='center')
students.column('age', anchor='center')
students.column('password', anchor='center')

students.heading("userID",text="ID")
students.heading("name",text="Name")
students.heading("age",text="Age")
students.heading("password",text="Password")


data = userJson()

for i in data:
    students.insert(parent='',index='end', iid=i["ID"], values=(i["ID"],i["name"],i["age"], i["password"]))


# students.insert(parent='',index='end', values=("12011","tmz","21", "abc"))

create_new = t.LabelFrame(viewStudents_frame, width=800, height=150, bg='darkblue', text="CREATE NEW STUDENT", fg="yellow")
create_new.place(x=40,y=270)


userName = t.Label(create_new, text="Name : ", bg='darkblue', fg='yellow', font=("Consolas", 14))  
userName.place(x=40, y=20)

userNameEntryBox = t.Entry(create_new, width=25 , bg='cyan' ,font=("Consolas", 14))
userNameEntryBox.place(x=110, y = 20)

ageLbl = t.Label(create_new, text="Age  : ", bg='darkblue', fg='yellow', font=("Consolas", 14))  
ageLbl.place(x=40, y=70)

ageEntryBox = t.Entry(create_new, width=25 , bg='cyan' ,font=("Consolas", 14))
ageEntryBox.place(x=110, y = 70)


passCredentials = partial(addStudent, userNameEntryBox, ageEntryBox, students)

createBtn = t.Button(create_new, width=25 , text="Create", bg='yellow' ,command=passCredentials)
createBtn.place(x=600, y=100)

editDelete = t.LabelFrame(viewStudents_frame, width=800, height=130, bg='darkblue', text="EDIT/DELETE", fg="yellow")
editDelete.place(x=40,y= 430)

userName = t.Label(editDelete, text="Name : ", bg='darkblue', fg='yellow', font=("Consolas", 14))  
userName.place(x=40, y=20)

userNameEntryBox = t.Entry(editDelete, width=25 , bg='cyan' ,font=("Consolas", 14))
userNameEntryBox.place(x=110, y = 20)

ageLbl = t.Label(editDelete, text="Age  : ", bg='darkblue', fg='yellow', font=("Consolas", 14))  
ageLbl.place(x=40, y=70)

ageEntryBox = t.Entry(editDelete, width=25 , bg='cyan' ,font=("Consolas", 14))
ageEntryBox.place(x=110, y = 70)

students.bind("<Button>", selectStudent)

editBtn = t.Button(editDelete, width=25 , text="Edit", bg='yellow', command=updateStudent)
deleteBtn = t.Button(editDelete, width=25 , text="Delete", bg='yellow', command=deleteStudent)

editBtn.place(x=400, y=80)
deleteBtn.place(x=600,y=80)

#####################################################################################################################

def addCapacity(event):
    capacity = int(constVal.cget("text"))
    constVal.config(text = capacity+1)
    # print(endcalendar.get_date())

def subCapacity(event):
    capacity = int(constVal.cget("text"))
    constVal.config(text = capacity-1)




def createCourseBtn(event):
    if (courseNameEntryBox.get() == "" or lecturerNameEntryBox.get() == ""):
        errMsg.config(text = "Please fill in all the details")
    elif (courseNameEntryBox.get() != "" and lecturerNameEntryBox.get() != ""):
        db_course = course_detJson()
        courseLib = courseJson()
        newCourse_id = courseLib[len(courseLib)-1]["CourseID"]+1
        db_course['course_det'].append ({
            "CourseID" : newCourse_id,
            "LecturerName" : lecturerNameEntryBox.get().upper(),
            "CourseName" : courseNameEntryBox.get().upper(),
            "Students" : [],
            "ClassCapacity" : constVal.cget("text"),
            "Day" : classDayEntryBox.get().upper(),
            "CourseStartDate" : startcalendar.get_date().strftime("%d-%m-%Y"),
            "CourseEndDate" : endcalendar.get_date().strftime("%d-%m-%Y")

        })
        courses.insert(parent='',index='end', iid=newCourse_id, values=(newCourse_id,courseNameEntryBox.get().upper(),lecturerNameEntryBox.get().upper(), constVal.cget("text")))

        with open('course.json', 'w') as f_course:
            json.dump(db_course, f_course, indent=4)
        # print(courseLib)
        errMsg.config(fg="yellow")
        errMsg.config(text = f"Course Name : {courseNameEntryBox.get().upper()} created successfully !!"
                                "\nWant to create another course ??")
        courseNameEntryBox.delete(0,t.END)
        lecturerNameEntryBox.delete(0,t.END)
        startcalendar.set_date(today_date.strftime("%d-%m-%Y"))
        endcalendar.set_date(today_date.strftime("%d-%m-%Y"))
        constVal.config(text = 25)




#################      WORK FRAME - Create course     ###############################################################


createCourse_frame = t.LabelFrame(tk, width=900, height=565, bg='darkblue')
createCourse_frame.place(x=0,y=65)
createCourse_frame.place_forget()

courseName = t.Label(createCourse_frame, text="Course Name    : ", fg="yellow", bg="darkblue", font=("Consolas", 14))
courseName.place(x=40, y=20)

courseNameEntryBox = t.Entry(createCourse_frame, width=35, bg="cyan", font=("Consolas",14))
courseNameEntryBox.place(x=210, y=20)

lecturerName = t.Label(createCourse_frame, text="Lecturer Name  : ", fg="yellow", bg="darkblue", font=("Consolas", 14))
lecturerName.place(x= 40, y = 80)

lecturerNameEntryBox = t.Entry(createCourse_frame, width=35, bg="cyan", font=("Consolas",14))
lecturerNameEntryBox.place(x=210, y=80)

classCapacity = t.Label(createCourse_frame, text="Class Capacity : ", fg="yellow", bg="darkblue",  font=("Consolas", 14))
classCapacity.place(x=40, y=140 )

minusBtn = t.Button(createCourse_frame, text="-", bg="gray")
minusBtn.place(x=220, y=140)

constVal = t.Label(createCourse_frame, text="25", fg="yellow", bg="darkblue", font=("Consolas", 14))
constVal.place(x=240, y=140)

plusBtn = t.Button(createCourse_frame, text="+", bg="gray")
plusBtn.place(x=270, y=140)

classDay = t.Label(createCourse_frame, text="Class Day      : ", fg="yellow", bg="darkblue", font=("Consolas", 14))
classDay.place(x=40, y=200)

classDayEntryBox = t.Entry(createCourse_frame, width=35, bg="cyan", font=("Consolas",14))
classDayEntryBox.place(x=210, y=200)


startDate = t.Label(createCourse_frame, text="Start Date     : ", fg="yellow", bg="darkblue",  font=("Consolas", 14))
startDate.place(x=40, y=260)

startcalendar = DateEntry(createCourse_frame, width= 16, date_pattern='dd-MM-yyyy')
startcalendar.place(x=210,y=265)


endDate = t.Label(createCourse_frame, text="End Date       : ", fg="yellow", bg="darkblue",  font=("Consolas", 14))
endDate.place(x=40, y=320)

endcalendar = DateEntry(createCourse_frame, width= 16, date_pattern='dd-MM-yyyy')
endcalendar.place(x=210, y=325)

errMsg = t.Label(createCourse_frame, bg="darkblue", fg="red", font=('Consolas',14))
errMsg.place(x=200 , y=400)

plusBtn.bind("<Button>", addCapacity)
minusBtn.bind("<Button>", subCapacity)


createBtn = t.Button(createCourse_frame, text="Create", bg="yellow" , width=20)
createBtn.place(x=700, y=500)

createBtn.bind("<Button>", createCourseBtn)


#####################################################################################################################
def addCapacity(event):
    capacity = int(constVal_edit.cget("text"))
    constVal_edit.config(text = capacity+1)
    # print(endcalendar.get_date())

def subCapacity(event):
    capacity = int(constVal_edit.cget("text"))
    constVal_edit.config(text = capacity-1)

def selectCourses(event):
    courseNameEntry.delete(0,t.END)
    lecturerNameEntry.delete(0,t.END)

    courseData = courseJson() 

    selected = courses.focus()
    values = courses.item(selected, 'values')

    for i in courseData:
        if (int(values[0]) == i["CourseID"]):
            startcalendar_edit.set_date(i["CourseStartDate"])
            endcalendar_edit.set_date(i["CourseEndDate"])

    courseNameEntry.insert(0, values[1])
    lecturerNameEntry.insert(0, values[2])
    constVal_edit.config(text = values[3])



def updateCourse():

    selected = courses.focus()
    values = courses.item(selected, 'values')
    # courses.delete(selected)

    if (courseNameEntry.get() != "" or lecturerNameEntry.get() != ""):
        courses.item(selected, text="", values=(values[0], courseNameEntry.get().upper(), lecturerNameEntry.get().upper(), constVal_edit.cget("text")))


        with open('course.json', 'r') as f_course:
            db_course = json.load(f_course)

        for i in range (len(db_course['course_det'])):
            if (db_course['course_det'][i]["CourseID"] == int(values[0]) ):
                db_course['course_det'][i]["CourseName"] = courseNameEntry.get().upper()
                db_course['course_det'][i]["LecturerName"] = lecturerNameEntry.get().upper()


        with open('course.json', 'w') as f_course:
            json.dump(db_course, f_course, indent=4)


    courseNameEntry.delete(0,t.END)
    lecturerNameEntry.delete(0,t.END)
    startcalendar_edit.set_date(today_date.strftime("%d-%m-%Y"))
    endcalendar_edit.set_date(today_date.strftime("%d-%m-%Y"))
    constVal_edit.config(text = 25)



def deleteCourse():

    selected = courses.focus()
    values = courses.item(selected, 'values')
    courses.delete(selected)
    
    db_course = course_detJson()
    db_courses = db_course['course_det']

    for i in range (len(db_courses)):
        if (db_courses[i]["CourseID"] == int(values[0])):
            db_courses.remove(db_courses[i])
            break
            
    with open('course.json', 'w') as f_course:
        json.dump(db_course, f_course, indent=4)
    
    
    courseNameEntry.delete(0,t.END)
    lecturerNameEntry.delete(0,t.END)
    startcalendar_edit.set_date(today_date.strftime("%d-%m-%Y"))
    endcalendar_edit.set_date(today_date.strftime("%d-%m-%Y"))
    constVal_edit.config(text = 25)


#################      WORK FRAME - view course     ###############################################################


viewCourse_frame = t.LabelFrame(tk, width=900, height=565, bg='darkblue')
# viewCourse_frame.place(x=0,y=65)
viewCourse_frame.place_forget()

courses = Treeview(viewCourse_frame, style="Treeview")

courses.place(x=40,y=30)

courses['column'] = ('courseID', 'courseName', 'lecturer', 'classCapacity')

courses.column("#0", width=0)

courses.column("courseID",anchor='center')
courses.column("courseName", anchor='center')
courses.column('lecturer', anchor='center')
courses.column('classCapacity', anchor='center')

courses.heading("courseID",text='Course ID')
courses.heading("courseName", text='Course Name')
courses.heading('lecturer', text='Lecturer Name')
courses.heading('classCapacity', text='Class Capacity')



courseData = courseJson()

for i in courseData:
    courses.insert(parent='',index='end', iid=i["CourseID"], values=(i["CourseID"],i["CourseName"],i["LecturerName"], i["ClassCapacity"]))


edit_orDelete = t.LabelFrame(viewCourse_frame, width=800, height=270, bg='darkblue', text="EDIT/DELETE", fg="yellow")
edit_orDelete.place(x=40,y= 280)

editCourseBtn = t.Button(edit_orDelete, width=25 , text="Edit", bg='yellow', command=updateCourse)
deleteCourseBtn = t.Button(edit_orDelete, width=25 , text="Delete", bg='yellow', command=deleteCourse)

editCourseBtn.place(x=400, y=225)
deleteCourseBtn.place(x=600,y=225)

courseNameLbl = t.Label(edit_orDelete, text="Course Name    : ", fg="yellow", bg="darkblue", font=("Consolas", 14))
courseNameLbl.place(x=40, y=20)

courseNameEntry = t.Entry(edit_orDelete, width=35, bg="cyan", font=("Consolas",14))
courseNameEntry.place(x=210, y=20)


lecturerNameLbl = t.Label(edit_orDelete, text="Lecturer Name  : ", fg="yellow", bg="darkblue", font=("Consolas", 14))
lecturerNameLbl.place(x= 40, y = 55)

lecturerNameEntry = t.Entry(edit_orDelete, width=35, bg="cyan", font=("Consolas",14))
lecturerNameEntry.place(x=210, y=55)

classCapacity = t.Label(edit_orDelete, text="Class Capacity : ", fg="yellow", bg="darkblue",  font=("Consolas", 14))
classCapacity.place(x=40, y=90 )

minusBtn = t.Button(edit_orDelete, text="-", bg="gray")
minusBtn.place(x=220, y=90)

constVal_edit = t.Label(edit_orDelete, text="25", fg="yellow", bg="darkblue", font=("Consolas", 14))
constVal_edit.place(x=240, y=90)

plusBtn = t.Button(edit_orDelete, text="+", bg="gray")
plusBtn.place(x=270, y=90)

startDate = t.Label(edit_orDelete, text="Start Date     : ", fg="yellow", bg="darkblue",  font=("Consolas", 14))
startDate.place(x=40, y=125)

startcalendar_edit = DateEntry(edit_orDelete, width= 16, date_pattern='dd-MM-yyyy')
startcalendar_edit.place(x=210,y=128)

endDate = t.Label(edit_orDelete, text="End Date       : ", fg="yellow", bg="darkblue",  font=("Consolas", 14))
endDate.place(x=400, y=125)

endcalendar_edit = DateEntry(edit_orDelete, width= 16, date_pattern='dd-MM-yyyy')
endcalendar_edit.place(x=570, y=128)

courses.bind("<Button>", selectCourses)
plusBtn.bind("<Button>", addCapacity)
minusBtn.bind("<Button>", subCapacity)


#####################################################################################################################


tk.configure(bg='darkblue')
tk.mainloop()

