import tkinter as t
from tkinter.ttk import *
from functools import partial
from tkcalendar import DateEntry
from datetime import datetime as dt
import random
import json
import string
import os
import sys

today_date = dt.now()

student_id = sys.argv[1]
print(student_id)

tk = t.Tk()
tk.title('Student Homepage')
tk.geometry("900x650")


def logOut():
    tk.destroy()
    os.system('python login.py')


def registerCourseBtn() :
    registerCourse_frame.place(x=0,y=65)
    viewSchedule_frame.place_forget()
    return

def viewScheduleBtn() :
    registerCourse_frame.place_forget()
    viewSchedule_frame.place(x=0,y=65)
    return


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
            "Day" : i["Day"],
            "CourseStartDate" : i["CourseStartDate"],
            "CourseEndDate" : i["CourseEndDate"]

        })
    return courses

def filterCourse():
    with open('user.json', 'r') as user:
        db_user = json.load(user)

    for i in range(len(db_user["students_det"])):
        if (db_user['students_det'][i]["ID"] == student_id):
            studentCourses = db_user['students_det'][i]["courses"]

    return studentCourses




def selectCourses(event):

    selected = courses.focus()

    values = courses.item(selected, 'values')
    courseNameEntry.config(text=f"{values[1]}")
    courseIDEntry.config(text=f"{selected}")
    
    # print(selected)

def enrollBtnCommand():
    courseID = courseIDEntry.cget("text")

    if (courseID == ""):
        enrollMsgLabel.config(text="Please select a course")
    else:
        with open('user.json', 'r') as f_user:
            db_user = json.load(f_user)

        for i in range(len(db_user["students_det"])):
            if (db_user['students_det'][i]["ID"] == student_id):
                if (int(courseID) not in db_user['students_det'][i]["courses"]):
                    db_user['students_det'][i]["courses"].append(int(courseID))
                else:
                    enrollMsgLabel.config(text="Course already registered !!", fg="yellow")
                


        with open('user.json', 'w') as f_user:
            json.dump(db_user, f_user, indent=4)
                
        enrollMsgLabel.config(text="Course registered successfully !!", fg="yellow")




############## BUTTON FRAME ######################################################################################

buttons_frame = t.LabelFrame(tk, width=900, height=50, bg='darkblue', font=(16), fg="yellow")
buttons_frame.place(x=0, y=5)


register_course = t.Button(buttons_frame, text="Register Course", width=15,  bg="yellow", command=registerCourseBtn)
register_course.place(x = 70, y=10)

view_schedule = t.Button(buttons_frame, text="View Schedule", width=15,  bg="yellow", command=viewScheduleBtn)
view_schedule.place(x=400, y=10)

logOut = t.Button(buttons_frame, text="Logout", width=15,  bg="yellow", command=logOut)
logOut.place(x=730, y=10)

#####################################################################################################################

style = Style()
style.theme_use("clam")
style.configure("Treeview",  fieldbackground="cyan", background="cyan")

#################      WORK FRAME - Register course     ###############################################################

registerCourse_frame = t.LabelFrame(tk, width=900, height=565, bg='darkblue')
registerCourse_frame.place(x=0,y=65)
registerCourse_frame.place_forget()

courses = Treeview(registerCourse_frame, style="Treeview")

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


enrollBtn = t.Button(registerCourse_frame, width=25 , text="Enroll", bg='yellow', command=enrollBtnCommand)
enrollBtn.place(x=660, y=300)

courseNameLbl = t.Label(registerCourse_frame, text="Course Name    : ", fg="yellow", bg="darkblue", font=("Consolas", 14))
courseNameLbl.place(x=40, y=300)

courseNameEntry = t.Label(registerCourse_frame, text="", width=35, bg="cyan", font=("Consolas",14))
courseNameEntry.place(x=210, y=300)

courseIDEntry = t.Label(registerCourse_frame, text="", width=35, fg="darkblue", bg="darkblue", font=("Consolas",14))
courseIDEntry.place(x=210, y=350)

enrollMsgLabel = t.Label(registerCourse_frame, text="", fg="red",bg="darkblue", width=35, font=("Consolas",14) )
enrollMsgLabel.place(x=40, y=400)


courses.bind("<Button>", selectCourses)


#####################################################################################################################



#################      WORK FRAME - View Schedule     ###############################################################

viewSchedule_frame = t.LabelFrame(tk, width=900, height=565, bg='darkblue')
viewSchedule_frame.place(x=0,y=65)
viewSchedule_frame.place_forget()


registeredCourses = Treeview(viewSchedule_frame, style="Treeview")

registeredCourses.place(x=40,y=30)

registeredCourses['column'] = ('courseName', 'lecturer', 'classDay')

registeredCourses.column("#0", width=0)


registeredCourses.column("courseName", anchor='center')
registeredCourses.column('lecturer', anchor='center')
registeredCourses.column('classDay', anchor='center')


registeredCourses.heading("courseName", text='Course Name')
registeredCourses.heading('lecturer', text='Lecturer Name')
registeredCourses.heading('classDay', text='Class Day')

courseData = courseJson()

for i in courseData:
    if (i["CourseID"] in filterCourse()):
        registeredCourses.insert(parent='',index='end', iid=i["CourseID"], values=(i["CourseName"],i["LecturerName"], i["Day"]))


#####################################################################################################################


tk.configure(bg='darkblue')
tk.mainloop()