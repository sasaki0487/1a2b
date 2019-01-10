import tkinter
from tkinter import *
from tkinter import messagebox
from threading import Timer
import random
import bisect

top = tkinter.Tk()
frame = tkinter.Frame(top)
frame.pack()
but_frame = tkinter.Frame(top)
but_frame.pack()

time_str = tkinter.StringVar()
time_str.set("Time : 0 s")
time_label = tkinter.Label(frame, textvariable = time_str)
time_label.grid(row = 0, column = 0)
enter_box = tkinter.Entry(frame)
enter_box.grid(row = 1 , column = 0)
guess_button = tkinter.Button(frame, text = "Guess!" , borderwidth = 5 , width = 10 , command = lambda: guess())
guess_button.grid(row = 2, column = 0)
result_box = tkinter.Text(frame , height = 20)
result_box.grid(row = 3 , column = 0)
answer_button = tkinter.Button(but_frame, text = "Answer" , borderwidth = 5 , width= 10 , command = lambda: show_ans())
answer_button.grid(row = 0 , column = 0)
restart_button = tkinter.Button(but_frame, text = "New Game" , borderwidth = 5 , width= 10 , command = lambda: restart())
restart_button.grid(row = 0 , column = 1)
exit_button = tkinter.Button(but_frame, text = "Exit" , borderwidth = 5 , width = 10 , command = lambda: exit())
exit_button.grid(row = 0 , column = 2)

round = 0
ans = ""
ans_list = []
name_list = []
round_list = []
time_list = []

def add_time():
    global t
    time = int(''.join(filter(str.isdigit, time_str.get())))
    time += 1;
    time_str.set("Time: " + str(time) + " s")
    t = Timer(1.0, add_time)
    t.start()

def gen_ran():
    global ans
    temp = random.sample(range(0,10),4)
    ans = "".join(map(str,temp))

def show_ans():
    global ans
    messagebox.showinfo("ANS", ans)

def win():
    global toplv
    global name_box
    toplv = tkinter.Toplevel()
    frame = tkinter.Frame(toplv)
    frame.pack()
    ok_button = tkinter.Button(frame, text = "OK" , borderwidth = 5 , width= 10 , command = lambda: win2())
    ok_button.grid(row = 1 , column = 0)
    name_box = tkinter.Entry(frame)
    name_box.grid(row = 0 , column = 0)
    name_box.insert(0,"Enter Your Name")

def win2():
    global toplv
    name = name_box.get()
    toplv.destroy()
    toplv = tkinter.Toplevel()
    frame = tkinter.Frame(toplv)
    frame.pack()
    score_box = tkinter.Text(frame , height = 20)
    score_box.grid(row = 0 , column = 0)
    score_box.insert(tkinter.END,"Name\t\tRound\t\tTime\n")
    restart_button = tkinter.Button(frame, text = "New Game" , borderwidth = 5 , width= 10 , command = lambda: end_restart())
    restart_button.grid(row = 1 , column = 0)
    exit_button = tkinter.Button(frame, text = "Exit" , borderwidth = 5 , width = 10 , command = lambda: exit())
    exit_button.grid(row = 2 , column = 0)
    time = int(''.join(filter(str.isdigit, time_str.get())))
    index = 0
    while index < len(name_list) and round > round_list[index] : 
        index += 1
    while index < len(name_list) and time > time_list[index] and round == round_list[index] :
        index += 1
    name_list.insert(index,name)
    round_list.insert(index,round)
    time_list.insert(index,time)
    index = 0
    for index in range(0,len(name_list)):
        score_box.insert(tkinter.END,name_list[index] + "\t\t" + str(round_list[index]) + "\t\t" + str(time_list[index]) + "\n")
    if len(name_list) > 10 :
        name_list.pop()
        round_list.pop()
        time_list.pop()

def lose():
    global toplv 
    toplv = tkinter.Toplevel()
    frame = tkinter.Frame(toplv)
    frame.pack()
    restart_button = tkinter.Button(frame, text = "New Game" , borderwidth = 5 , width= 10 , command = lambda: end_restart())
    restart_button.grid(row = 0 , column = 0)
    exit_button = tkinter.Button(frame, text = "Exit" , borderwidth = 5 , width = 10 , command = lambda: exit())
    exit_button.grid(row = 1 , column = 0)

def end_restart():
    toplv.destroy()
    restart()

def restart():
    global round
    global ans_list
    global t
    ans_list = []
    round = 0
    gen_ran()
    result_box.delete("1.0",tkinter.END)
    time_str.set("Time : 0 s")
    t.cancel()
    t = Timer(1.0, add_time)
    t.start()

def check_ab(input):
    global ans
    a = 0
    b = 0
    for char in input:
        i = ans.find(char)
        if i != -1:
            if input[i] == char:
                a += 1
            else:
                b += 1 
    return str(a) + "A" + str(b) + "B"

def guess():
    global round
    global ans_list
    global ans
    input = enter_box.get()
    enter_box.delete(0,END)
    if len(input) != 4 :
        result = input + "\tInvalid Input!! (Length Error)\n"
        result_box.insert(tkinter.END,result)
        return
    if not input.isdigit() :
        result = input + "\tInvalid Input!! (Input not Number)\n"
        result_box.insert(tkinter.END,result)
        return
    for i in range(0,4):
        if input.find(input[i],i+1) != -1:
            result = input + "\tInvalid Input!! (Charcter Repeat)\n"
            result_box.insert(tkinter.END,result)
            return
    if input in ans_list:
        result = input + "\tInvalid Input!! (Repeated Guess)\n"
        result_box.insert(tkinter.END,result)
        return
    round += 1
    ans_list.insert(0,input)
    ab = check_ab(input)
    result = "Round" + str(round) + "\t" + input + "\t" + ab + "\n"
    result_box.insert(tkinter.END,result)
    if ab == "4A0B" :
        result_box.insert(tkinter.END,"You win!!")
        t.cancel()
        win()
    elif round >= 10 :
        result_box.insert(tkinter.END,"You lose.\n QQ Answer is " + ans)
        lose()

def exit():
    t.cancel()
    top.destroy()
 
t = Timer(1.0, add_time)
t.start()
gen_ran()
top.mainloop()