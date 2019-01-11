import Tkinter
from Tkinter import *
import tkMessageBox
from threading import Timer
import random

top = Tkinter.Tk()
frame = Tkinter.Frame(top)
frame.pack()
but_frame = Tkinter.Frame(top)
but_frame.pack()

#時間物件
time_str = Tkinter.StringVar()
time_str.set("Time : 0 s")
time_label = Tkinter.Label(frame, textvariable=time_str)
time_label.grid(row=0, column=0)
#輸入答案物件
enter_box = Tkinter.Entry(frame)
enter_box.grid(row=1, column=0)
guess_button = Tkinter.Button(frame, text="Guess!", borderwidth=5, width=10, command=lambda: guess())
guess_button.grid(row=2, column=0)
#顯示結果物件
result_box = Tkinter.Text(frame, height=20)
result_box.grid(row=3, column=0)
#顯示答案 重新開始 離開按鈕
answer_button = Tkinter.Button(but_frame, text="Answer", borderwidth=5, width=10, command=lambda: show_ans())
answer_button.grid(row=0, column=0)
restart_button = Tkinter.Button(but_frame, text="New Game", borderwidth=5, width=10, command=lambda: restart())
restart_button.grid(row=0, column=1)
exit_button = Tkinter.Button(but_frame, text="Exit", borderwidth=5, width=10, command=lambda: exit())
exit_button.grid(row=0, column=2)

#初始化各種東西
round = 0
ans = ""
ans_list = []
name_list = []
round_list = []
time_list = []

#加時間的function
def add_time():
    global t
    #把時間取出來
    time = int(''.join(filter(str.isdigit, time_str.get())))
    #時間加+1
    time += 1;
    #時間塞回去
    time_str.set("Time: " + str(time) + " s")
    #要重複call才會一直執行
    t = Timer(1.0, add_time)
    t.start()

#生成題目的function
def gen_ran():
    global ans
    #gen 4 number by sampling
    temp = random.sample(range(0, 10), 4)
    #串起來
    ans = "".join(map(str, temp))

#顯示答案的function
def show_ans():
    global ans
    #用messagebox顯示答案
    tkMessageBox.showinfo("ANS", ans)

#贏了的時候執行的function (part1 輸入名字)
def win():
    global toplv
    global name_box
    #開一個新的框框
    toplv = Tkinter.Toplevel()
    frame = Tkinter.Frame(toplv)
    frame.pack()
    #OK的按鍵 (輸入完名字後按的)
    ok_button = Tkinter.Button(frame, text="OK", borderwidth=5, width=10, command=lambda: win2())
    ok_button.grid(row=1, column=0)
    name_box = Tkinter.Entry(frame)
    name_box.grid(row=0, column=0)
    name_box.insert(0, "Enter Your Name")

#贏了之後輸入完名字執行的function (part2 顯示高分榜)
def win2():
    global toplv
    #把名字存起來，把輸入名字的框框殺掉
    name = name_box.get()
    toplv.destroy()
    toplv = Tkinter.Toplevel()
    frame = Tkinter.Frame(toplv)
    frame.pack()
    #顯示名字的文字框
    score_box = Tkinter.Text(frame, height=20)
    score_box.grid(row=0, column=0)
    score_box.insert(Tkinter.END, "Name\t\tRound\t\tTime\n")
    restart_button = Tkinter.Button(frame, text="New Game", borderwidth=5, width=10, command=lambda: end_restart())
    restart_button.grid(row=1, column=0)
    exit_button = Tkinter.Button(frame, text="Exit", borderwidth=5, width=10, command=lambda: exit())
    exit_button.grid(row=2, column=0)
    #把時間記起來
    time = int(''.join(filter(str.isdigit, time_str.get())))
    #計算新的高分要插入的位置，先比回合數再比花費時間
    index = 0
    while index < len(name_list) and round > round_list[index]:
        index += 1
    while index < len(name_list) and time > time_list[index] and round == round_list[index]:
        index += 1
    #把資訊都插入他該在的位置
    name_list.insert(index, name)
    round_list.insert(index, round)
    time_list.insert(index, time)
    #如果超過十個人上榜就刪掉多的
    if len(name_list) > 10:
        name_list.pop()
        round_list.pop()
        time_list.pop()
    index = 0
    #串到高分榜的文字框
    for index in range(0, len(name_list)):
        score_box.insert(Tkinter.END,
                         name_list[index] + "\t\t" + str(round_list[index]) + "\t\t" + str(time_list[index]) + "\n")

#輸掉的時候呼叫的function
def lose():
    global toplv
    toplv = Tkinter.Toplevel()
    frame = Tkinter.Frame(toplv)
    frame.pack()
    #重新開始的按鈕跟離開的按鈕
    restart_button = Tkinter.Button(frame, text="New Game", borderwidth=5, width=10, command=lambda: end_restart())
    restart_button.grid(row=0, column=0)
    exit_button = Tkinter.Button(frame, text="Exit", borderwidth=5, width=10, command=lambda: exit())
    exit_button.grid(row=1, column=0)

#遊戲結束時的new game
def end_restart():
    toplv.destroy()
    restart()

#遊戲還沒結束時的new game (其實可以用try except做) 
def restart():
    global round
    global ans_list
    global t
    #各種初始化跟timer重開
    ans_list = []
    round = 0
    gen_ran()
    result_box.delete("1.0", Tkinter.END)
    time_str.set("Time : 0 s")
    t.cancel()
    t = Timer(1.0, add_time)
    t.start()

#檢查幾A幾B的function，會回傳字串XAXB
def check_ab(input):
    global ans
    a = 0
    b = 0
    #如果輸入的字串的各個字元有在答案裡，位置一樣就a++，不然就b++
    for char in input:
        i = ans.find(char)
        if i != -1:
            if input[i] == char:
                a += 1
            else:
                b += 1
    return str(a) + "A" + str(b) + "B"

#送出答案時呼叫的function
def guess():
    global round
    global ans_list
    global ans
    #把使用者輸入存起來然後清空輸入框
    input = enter_box.get()
    enter_box.delete(0, END)
    #檢查長度是否為4
    if len(input) != 4:
        result = input + "\tInvalid Input!! (Length Error)\n"
        result_box.insert(Tkinter.END, result)
        return
    #檢查是否都是數字
    if not input.isdigit():
        result = input + "\tInvalid Input!! (Input not Number)\n"
        result_box.insert(Tkinter.END, result)
        return
    #檢查4個數字裡面有沒有重複的
    for i in range(0, 4):
        if input.find(input[i], i + 1) != -1:
            result = input + "\tInvalid Input!! (Charcter Repeat)\n"
            result_box.insert(Tkinter.END, result)
            return
    #檢查有沒有輸入過這個答案
    if input in ans_list:
        result = input + "\tInvalid Input!! (Repeated Guess)\n"
        result_box.insert(Tkinter.END, result)
        return
    #確認沒問題後回合數+1(初始為0) ，並把答案塞到答案陣列裡(用來檢查有沒有輸入過用)
    round += 1
    ans_list.insert(0, input)
    #呼叫funtion看是幾A幾B並把結果塞到顯示框裡
    ab = check_ab(input)
    result = "Round" + str(round) + "\t" + input + "\t" + ab + "\n"
    result_box.insert(Tkinter.END, result)
    #如果猜中了就呼叫猜贏的function
    if ab == "4A0B":
        result_box.insert(Tkinter.END, "You win!!")
        t.cancel()
        win()
    #超過十回合就輸了
    elif round >= 10:
        result_box.insert(Tkinter.END, "You lose.\n QQ Answer is " + ans)
        lose()

#遊戲結束
def exit():
    t.cancel()
    top.destroy()

#遊戲開始
t = Timer(1.0, add_time)
t.start()
gen_ran()
top.mainloop()
