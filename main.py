# Family Feud Graphical Game
# Author: D. Depatie
# Date: 12/3/2022

import tkinter as tk
from multiprocessing import Process
from playsound import playsound

import survey
import scoreboard
from time import sleep


tkWindow = tk.Tk()
ogBack = tkWindow.cget("background")
global x
x = Process(target=playsound, args=["sounds/FFtheme.mp3"])

# tkWindow.geometry("2000x1250")
# tk.Grid.columnconfigure(tkWindow, index=0, weight=1)

def buildGUI():
    tkWindow.title('Depatie Family Feud!')
    # TODO: change icon to something FF related
    # tkWindow.iconbitmap(getcwd() + '/PROicon.ico')

    title = "Depatie Family Feud!\nChristmas Edition"
    color = "Red"
    greeting = tk.Label(text=title, font="Arial 100 bold", relief="ridge", padx=20, fg=color)
    greeting.pack()
    # canvas = tk.Canvas(tkWindow, width=435, height=275)
    # canvas.pack()
    # img = ImageTk.PhotoImage(Image.open("PROlogo.png"))
    # canvas.create_image(5, 5, anchor='nw', image=img)
    start_button = tk.Button(tkWindow, text="Start", height='5', width='20', font='Arial 40', relief='ridge', bd='3',
                             command=lambda: handle_start(start_button, greeting))
    start_button.pack()
    # TODO: try the method of using after in test.py to oscillate the greeting label color.
    # greeting.after(1000, greetingFlip(color, greeting))
    x.start()
    tkWindow.mainloop()

# def greetingFlip():
#     global greeting
#     global color
#     if color == "Red":
#         color = "Green"
#         greeting.config(fg=color)
#     elif color == "Green":
#         color = "Red"
#         greeting.config(fg=color)

    # greeting.after(1000, greetingFlip)

def handle_start(start_button, greeting):
    # TODO: resize if time available
    start_button.destroy()
    greeting.destroy()
    x.kill()
    t1Label = tk.Label(tkWindow, text="Family 1: ", font="Arial 12 bold", relief="ridge", padx=100)
    t1Label.grid(row=0, column=0, sticky='w')
    t1Entry = tk.Entry(tkWindow, width=100)
    t1Entry.grid(row=0, column=1, sticky='w')
    t2Label = tk.Label(tkWindow, text="Family 2: ", font="Arial 12 bold", relief="ridge", padx=100)
    t2Label.grid(row=1, column=0, sticky='w')
    t2Entry = tk.Entry(tkWindow, width=100)
    t2Entry.grid(row=1, column=1, sticky='w')
    sub_button = tk.Button(tkWindow, text="Submit",
                           command=lambda: handle_sub(sub_button, t1Label, t2Label, t1Entry, t2Entry))
    sub_button.grid(row=2, column=1, sticky='s')


def handle_sub(sub_button, t1Label, t2Label, t1Entry, t2Entry):
    score = scoreboard.scoreboard(t1Entry.get(), t2Entry.get())
    sub_button.destroy()
    t1Label.destroy()
    t2Label.destroy()
    t1Entry.destroy()
    t2Entry.destroy()
    qnum = 0
    q = readSurveys()
    startGame(score, q, qnum)

def startGame(score, q, qnum):
    pointTotal = sum(q[qnum].points)
    surveyFrame = tk.Frame(tkWindow)
    surveyFrame.grid(row=0, column=0, pady=20)
    qLabels = []
    for i in range(len(q[qnum].ans)):
        qLabels.append(tk.Label(surveyFrame, text=i+1, font="Arial 20 bold", relief="ridge", padx=20, width=40, height=5))
        if i > 3:
            qLabels[i].grid(row=i-4, column=1)
        else:
            qLabels[i].grid(row=i, column=0)

    scoreFrame = tk.Frame(tkWindow)
    scoreFrame.grid(row=1, column=0, pady=20)
    strike1Frame = tk.Frame(scoreFrame)
    strike2Frame = tk.Frame(scoreFrame)
    t1 = tk.Label(scoreFrame, text=score.team1, font="Arial 20 bold", relief="ridge", padx=20, width=15, height=5)
    t2 = tk.Label(scoreFrame, text=score.team2, font="Arial 20 bold", relief="ridge", padx=20, width=15, height=5)
    t1score = tk.Label(scoreFrame, text=score.score1, font="Arial 20 bold", relief="ridge", padx=20, width=15, height=5)
    t2score = tk.Label(scoreFrame, text=score.score2, font="Arial 20 bold", relief="ridge", padx=20, width=15, height=5)

    pLabel = tk.Label(scoreFrame, text=score.points, font="Arial 20 bold", relief="ridge", padx=20, width=15, height=5)
    t1.grid(row=0, column=0, padx=20)
    t1score.grid(row=1, column=0)
    strike1Frame.grid(row=2, column=0, pady=10)
    strikes1 = []
    for i in range(3):
        strikes1.append(tk.Label(strike1Frame, text="X", font="Arial 100 bold", relief="ridge", padx=10, fg="gray"))
        strikes1[i].grid(row=0, column=i)
    t2.grid(row=0, column=5, padx=20)
    t2score.grid(row=1, column=5)
    strike2Frame.grid(row=2, column=5, pady=10)
    strikes2 = []
    for i in range(3):
        strikes2.append(tk.Label(strike2Frame, text="X", font="Arial 100 bold", relief="ridge", padx=10, fg="gray"))
        strikes2[i].grid(row=0, column=i)
    pLabel.grid(row=0, column=3)

    admin = tk.Toplevel(tkWindow)
    admin.geometry("500x500")
    q_buttonFrame = tk.Frame(admin)
    q_buttonFrame.pack()
    q_buttons = []
    for i in range(len(q[qnum].ans)):
        q_buttons.append(tk.Button(q_buttonFrame, text=q[qnum].ans[i] + "\t" + str(q[qnum].points[i]),
                                   command=lambda i=i: handleQButton(i, q_buttons, q, qnum, qLabels[i], score, pLabel, pointTotal, t1score, t2score)))
        q_buttons[i].pack()

    activeFrame = tk.Frame(admin, padx=20, pady=20)
    activeFrame.pack()
    a1 = tk.Button(activeFrame, text="Active: " + score.team1,
                   command=lambda: activeHandle(1, t1, score))
    a1.pack()
    a2 = tk.Button(activeFrame, text="Active: " + score.team2,
                   command=lambda: activeHandle(2, t2, score))
    a2.pack()

    sButtonFrame = tk.Frame(admin, padx=20, pady=20)
    sButtonFrame.pack()
    s1 = tk.Button(sButtonFrame, text="Strike!: " + score.team1,
                   command=lambda strikes=strikes1: strikeHandle(t1, t2, t1score, t2score, strikes, score))
    s1.pack()
    s2 = tk.Button(sButtonFrame, text="Strike!: " + score.team2,
                   command=lambda strikes=strikes2: strikeHandle(t1, t2, t1score, t2score, strikes, score))
    s2.pack()
    # TODO: create next game admin button!
    destroy = tk.Button(admin, text="Next Question", padx=20, pady=20,
                        command=lambda: nextQuestion(admin, score, q, qnum))
    destroy.pack()
    admin.mainloop()

def readSurveys():
    q = []
    f = open("surveys.txt", 'r', encoding='utf-8')
    for line in f:
        question = line.strip('\n')
        ans = []
        points = []
        tempAns = []
        tempPoints = []
        for i in range(4):
            row = f.readline().strip('\n').split('\t')
            while True:
                try:
                    row.remove('')
                except ValueError as e:
                    break
            for i in range(len(row)):
                if i > 1:
                    if row[i].isnumeric():
                        tempPoints.append(int(row[i]))
                    else:
                        tempAns.append(row[i])
                else:
                    if row[i].isnumeric():
                        points.append(int(row[i]))
                    else:
                        ans.append(row[i])
        for i in range(len(tempAns)):
            ans.append(tempAns[i])
            points.append(tempPoints[i])
        q.append(survey.survey(question, ans, points))
    return q

def handleQButton(i, buttons, q, qnum, label, score, pLabel, pointTotal, t1score, t2score):
    label.config(text=q[qnum].ans[i] + "\t\t" + str(q[qnum].points[i]), bg="green", fg="white")
    p = Process(target=playsound, args=["sounds/09 Clang.mp3"])
    p.start()
    if score.winner == True:
        buttons[i].destroy()
        return
    elif score.strikes1 == 3 and score.active == score.team2:
        score.score2 += score.points
        t2score.config(text=str(score.score2))
        score.winner = True
    elif score.strikes2 == 3 and score.active == score.team1:
        score.score1 += score.points
        t1score.config(text=str(score.score1))
        score.winner = True
    else:
        score.addPoints(q[qnum].points[i])
        pLabel.config(text=score.points)
        if score.points == pointTotal:
            if score.active == score.team1:
                score.score1 += score.points
                t1score.config(text=str(score.score1))
                score.winner = True
            elif score.active == score.team2:
                score.score2 += score.points
                t2score.config(text=str(score.score2))
                score.winner = True
    buttons[i].destroy()

def strikeHandle(t1, t2, t1score, t2score, strikes, score):
    p = Process(target=playsound, args=["sounds/11 Strike.mp3"])
    p.start()
    if score.active == score.team1:
        score.strikes1 += 1
        for i in range(score.strikes1):
            strikes[i].config(fg="red")
        if score.strikes1 == 1 and score.strikes2 == 3:
            score.active = score.team2
            t1.config(bg=ogBack)
            t2.config(bg="green")
            score.score2 += score.points
            t2score.config(text=str(score.score2))
            score.winner = True
        elif score.strikes1 == 3:
            score.active = score.team2
            t1.config(bg=ogBack)
            t2.config(bg="green")
    elif score.active == score.team2:
        score.strikes2 += 1
        for i in range(score.strikes2):
            strikes[i].config(fg="red")
        if score.strikes2 == 1 and score.strikes1 == 3:
            score.active = score.team1
            t2.config(bg=ogBack)
            t1.config(bg="green")
            score.score1 += score.points
            t1score.config(text=str(score.score1))
            score.winner = True
        elif score.strikes2 == 3:
            score.active = score.team1
            t2.config(bg=ogBack)
            t1.config(bg="green")

def activeHandle(team, t, score):
    if team == 1:
        score.active = score.team1
        t.config(bg="green")
    elif team == 2:
        score.active = score.team2
        t.config(bg="green")

def nextQuestion(admin, score, q, qnum):
    score.points = 0
    score.strikes1 = 0
    score.strikes2 = 0
    score.winner = False
    for i in tkWindow.winfo_children():
        i.destroy()
    admin.destroy()
    qnum += 1
    startGame(score, q, qnum)

buildGUI()

#TODO: handle if both active buttons are pressed
#TODO: Add sound effects? Will require research