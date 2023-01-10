import threading
import tkinter
from tkinter import ttk
from tkinter import *
from queue import Queue
from PIL import Image, ImageTk
import time


def strihaj():
    zoz = []
    for i in range(12):
        obr = str(i) + '.gif'
        im = Image.open(obr)
        zoz.append(ImageTk.PhotoImage(im))
    return zoz


class Input:
    def __init__(self):
        self.flag = True
        self.now = 'white'
        self.now_figure = '0'
        self.kor = [-1, -1]
        self.From = '0'
        self.WereCanGO = []
        self.GoClear = True
        self.game = []
        self.click = 0
        self.but = -1
        self.end = -1
        self.KolWhite = 12
        self.KOlBlack = 12
        self.canvas = tkinter.Canvas(width=500, height=700)
        self.canvas['background'] = '#D2B48C'
        self.canvas.create_text(250, 100, text='Checkers', font='Arial 50', fill='#F5DEB3')
        self.White = Image.open('White2.png')
        self.White = self.White.resize((50, 50))
        self.White = ImageTk.PhotoImage(self.White)
        self.Black = Image.open('Black2.png')
        self.Black = self.Black.resize((50, 50))
        self.Black = ImageTk.PhotoImage(self.Black)
        self.FBlack = Image.open('FWhite.png')
        self.FBlack = self.FBlack.resize((50, 50))
        self.FBlack = ImageTk.PhotoImage(self.FBlack)
        self.FWhite = Image.open('FBlack.png')
        self.FWhite = self.FWhite.resize((50, 50))
        self.FWhite = ImageTk.PhotoImage(self.FWhite)
        self.canvas.pack()
        self.file = open('game.txt', "w")
        self.file.write("\nStart of game:\n\n")


class Checkers(Input):
    def __init__(self):
        super().__init__()
        self.start()
        self.desk()
        self.canvas.bind('<Button-1>', self.kli)
        self.win()
        tkinter.mainloop()

    def start(self):
        x = 30
        y = 225
        for i in range(8):
            self.canvas.create_text(x, y, fill='black', text=str(8 - i), font='Arial 18')
            y += 50

        x = 75
        y = 615
        for i in range(97, 105):
            self.canvas.create_text(x, y, fill='black', font='Arial 18', text=chr(i))
            x += 50

        for j in range(8):
            mas = []
            for i in range(8):
                mas.append(['0', 'no'])
            self.game.append(mas)

        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 1:
                    if i < 3:
                        self.game[i][j] = ['P', 'black']
                    if i > 4:
                        self.game[i][j] = ['P', 'white']

    def desk(self):
        x = 50
        y = 200
        self.canvas.create_text(110, 25, text='Now going:', font=("Verdana", 24, 'bold'))
        if self.now == 'black':
            self.canvas.create_image(250, 27, image=self.Black)
        else:
            self.canvas.create_image(250, 27, image=self.White)
        if self.GoClear is True:
            self.GoClear = False
            for i in range(8):
                for j in range(8):
                    color = '#FFF8DC'
                    if (i + j) % 2 == 1:
                        color = '#808080'
                    self.canvas.create_rectangle(x + i * 50, y + j * 50, x + (i + 1) * 50, y + (j + 1) * 50, fill=color)
        x = 75
        y = 225
        for i in range(8):
            for j in range(8):
                col = self.game[j][i][1]
                if col == 'white':
                    if self.game[j][i][0] == 'F':
                        self.canvas.create_image(x + i * 50, y + j * 50, image=self.FWhite)
                    else:
                        self.canvas.create_image(x + i * 50, y + j * 50, image=self.White)
                if col == 'black':
                    if self.game[j][i][0] == 'F':
                        self.canvas.create_image(x + i * 50, y + j * 50, image=self.FBlack)
                    else:
                        self.canvas.create_image(x + i * 50, y + j * 50, image=self.Black)

    def kli(self, event):
        if 50 <= event.x < 50 + 50 * 8 and 200 <= event.y <= 200 + 8 * 50:
            x = (event.x - 50)//50
            y = (event.y - 200)//50
            pole = self.game[y][x][0]
            col = self.game[y][x][1]
            if col != self.now and col != 'no':
                self.click = 0
                return
            if self.now == 'white' or self.now == 'black':
                if self.click == 1:
                    if pole == 'P' or pole == 'F':
                        self.click = 0
                    else:
                        for i in range(len(self.WereCanGO)):
                            if self.WereCanGO[i][0] == y and self.WereCanGO[i][1] == x:
                                c = chr(ord('a') + self.kor[1]) + str(8 - self.kor[0])
                                c2 = chr(ord('a') + x) + str(8 - y)
                                add = c + "->" + c2 + "\n"
                                self.file.write(add)
                                self.game[self.kor[0]][self.kor[1]] = ['0', 'no']
                                if len(self.WereCanGO[i]) >= 3 and len(self.WereCanGO[i][2]) != 0:
                                    for j in range(len(self.WereCanGO[i][2])):
                                        self.game[self.WereCanGO[i][2][j][0]][self.WereCanGO[i][2][j][1]] = ['0', 'no']
                                    if self.now == 'white':
                                        self.KOlBlack -= len(self.WereCanGO[i][2])
                                    else:
                                        self.KolWhite -= len(self.WereCanGO[i][2])
                                self.game[y][x] = [self.From, self.now]
                                if y == 0 and self.now == 'white':
                                    self.game[y][x] = ['F', self.now]
                                if y == 7 and self.now == 'black':
                                    self.game[y][x] = ['F', self.now]
                                self.GoClear = True
                                self.desk()
                                self.GoClear = False
                                if self.now == 'white':
                                    self.now = 'black'
                                else:
                                    self.now = 'white'
                                break
                        self.GoClear = True
                        self.desk()
                    self.WereCanGO.clear()
                if self.click == 0:
                    self.From = pole
                    self.kor = [y, x]
                    self.GoClear = True
                    self.desk()
                    self.click = 1
                    if pole == 'P':
                        if col == 'white' or col == 'black':
                            color = {'white': 'black', 'black': 'white'}
                            self.kor = [y, x]
                            q = Queue()
                            q.put([y, x, []])
                            dx = [-2, -2, 2, 2]
                            dy = [-2, 2, -2, 2]
                            wx = [-1, -1, 1, 1]
                            wy = [-1, 1, -1, 1]
                            used = []
                            while q.empty() is False:
                                pair = q.get()
                                used.append(pair)
                                mas = pair[2]
                                for i in range(4):
                                    canx = pair[1] + dx[i]
                                    cany = pair[0] + dy[i]
                                    px = pair[1] + wx[i]
                                    py = pair[0] + wy[i]
                                    if 0 <= px <= 7 and 0 <= py <= 7:
                                        if (self.game[py][px][0] == 'P' or self.game[py][px][0] == 'F') and \
                                                self.game[py][px][1] == color[col]:
                                            if 0 <= canx <= 7 and 0 <= cany <= 7 and self.game[cany][canx][0] == '0':
                                                flag = True
                                                for j in used:
                                                    if j[0] == cany and j[1] == canx:
                                                        flag = False
                                                if flag:
                                                    cop = []
                                                    for w in mas:
                                                        cop.append(w)
                                                    cop.append([py, px])
                                                    q.put([cany, canx, cop])
                                                    self.WereCanGO.append([cany, canx, cop])
                                                self.canvas.create_oval(canx * 50 + 50 + 18, cany * 50 + 200 + 18,
                                                                        (canx + 1) * 50 + 50 - 18, (cany + 1) * 50 +
                                                                        200 - 18,
                                                                        fill='#98FB98')
                            if len(self.WereCanGO) == 0:
                                if col == 'white':
                                    if x - 1 >= 0 and y - 1 >= 0:
                                        if self.game[y - 1][x - 1][0] == '0':
                                            self.WereCanGO.append([y - 1, x - 1])
                                            self.canvas.create_oval((x - 1) * 50 + 50 + 18, (y - 1) * 50 + 200 + 18,
                                                                    x * 50 + 50 - 18, y * 50 + 200 - 18,
                                                                    fill='#98FB98')
                                    if x + 1 <= 7 and y - 1 >= 0:
                                        if self.game[y - 1][x + 1][0] == '0':
                                            self.WereCanGO.append([y - 1, x + 1])
                                            self.canvas.create_oval((x + 1) * 50 + 50 + 18, (y - 1) * 50 + 200 + 18,
                                                                    (x + 2) * 50 + 50 - 18, y * 50 + 200 - 18,
                                                                    fill='#98FB98')
                                else:
                                    if x + 1 <= 7 and y + 1 <= 7:
                                        if self.game[y + 1][x + 1][0] == '0':
                                            self.WereCanGO.append([y + 1, x + 1])
                                            self.canvas.create_oval((x + 1) * 50 + 50 + 18, (y + 1) * 50 + 200 + 18,
                                                                    (x + 2) * 50 + 50 - 18, (y + 2) * 50 + 200 - 18,
                                                                    fill='#98FB98')
                                    if x - 1 >= 0 and y + 1 <= 7:
                                        if self.game[y + 1][x - 1][0] == '0':
                                            self.WereCanGO.append([y + 1, x - 1])
                                            self.canvas.create_oval((x - 1) * 50 + 50 + 18, (y + 1) * 50 + 200 + 18,
                                                                    x * 50 + 50 - 18, (y + 2) * 50 + 200 - 18,
                                                                    fill='#98FB98')
                    elif pole == 'F':
                        used = []
                        for i in range(8):
                            new = []
                            for j in range(8):
                                new.append(False)
                            used.append(new)
                        used[y][x] = True
                        q = Queue()
                        q.put([y, x, []])
                        while q.empty() is False:
                            pair = q.get()
                            used[pair[0]][pair[1]] = True
                            mas = pair[2]
                            dx = [-1, -1, 1, 1]
                            dy = [-1, 1, -1, 1]
                            bit = [0, 0, 0, 0]
                            for j in range(4):
                                have = 0
                                other = 0
                                for i in range(1, 8):
                                    px = pair[1] + i * dx[j]
                                    py = pair[0] + i * dy[j]
                                    if 0 <= px <= 7 and 0 <= py <= 7:
                                        if self.game[py][px][0] == 'P' or self.game[py][px][0] == 'F':
                                            if self.game[py][px][1] == col:
                                                break
                                            else:
                                                if 0 <= py + dy[j] <= 7 and 0 <= px + dx[j] <= 7:
                                                    if self.game[py + dy[j]][px + dx[j]][0] == 'P' or \
                                                            self.game[py + dy[j]][px + dx[j]][0] == 'F':
                                                        break
                                                if used[py][px] is False:
                                                    other += 1
                                        else:
                                            if other != 0:
                                                have += 1
                                    else:
                                        break
                                bit[j] = have

                            summa = bit[0] + bit[1] + bit[2] + bit[3]
                            if summa == 0 and len(mas) == 0:
                                for j in range(4):
                                    for i in range(1, 8):
                                        px = pair[1] + i * dx[j]
                                        py = pair[0] + i * dy[j]
                                        if 0 <= px <= 7 and 0 <= py <= 7:
                                            if self.game[py][px][0] == '0':
                                                used[py][px] = True
                                                self.canvas.create_oval(px * 50 + 50 + 18, py * 50 + 200 + 18, (px + 1)
                                                                        * 50 + 50 - 18, (py + 1) * 50 + 200 - 18,
                                                                        fill='#98FB98')
                                                self.WereCanGO.append([py, px, mas])
                                            else:
                                                break
                            else:
                                for j in range(4):
                                    if bit[j] != 0:
                                        p = 0
                                        cop = []
                                        for w in mas:
                                            cop.append(w)
                                        for i in range(1, 8):
                                            px = pair[1] + i * dx[j]
                                            py = pair[0] + i * dy[j]
                                            if 0 <= px <= 7 and 0 <= py <= 7:
                                                if self.game[py][px][0] == '0':
                                                    if p != 0:
                                                        if used[py][px] is False:
                                                            cop2 = []
                                                            for r in cop:
                                                                cop2.append(r)
                                                            q.put([py, px, cop2])
                                                            self.WereCanGO.append([py, px, cop2])
                                                        self.canvas.create_oval(px * 50 + 50 + 18, py * 50 + 200 + 18,
                                                                                (px + 1) * 50 + 50 - 18, (py + 1) * 50 +
                                                                                200 - 18,
                                                                                fill='#98FB98')
                                                else:
                                                    if self.game[py][px][0] == 'P' or self.game[py][px][0] == 'F':
                                                        if self.game[py][px][1] == col:
                                                            break
                                                        else:
                                                            p += 1
                                                            if p <= bit[j]:
                                                                cop.append([py, px])
                                                used[py][px] = True
                                            else:
                                                break
        self.win()

    def newgame(self):
        self.canvas.destroy()
        self.but.destroy()
        self.end.destroy()
        root = Tk()
        root.title('Wait')
        root.geometry("300x30+250+500")

        pb = ttk.Progressbar(root, mode="determinate", length=250)
        pb.pack()

        def progress():
            for i in range(11):
                pb['value'] += 10
                time.sleep(.3)
            root.destroy()
            self.canvas.after(500, Checkers)

        threading.Thread(target=progress).start()
        root.mainloop()

    def gameover(self):
        self.flag = False
        self.file.close()
        self.canvas.destroy()
        self.but.destroy()
        self.end.destroy()
        exit()

    def win(self):
        t = 'Black Win'
        flag = False
        if self.KolWhite == 0:
            t = 'Black Win'
            flag = True
        if self.KOlBlack == 0:
            t = 'White Win'
            flag = True
        if flag is True:
            self.canvas.create_rectangle(25, 250, 475, 550, fill="#FA8072")
            self.canvas.create_text(250, 350, text=t, font='Arial 50', fill='#4aea37')
            zoz = strihaj()
            tk_id1 = self.canvas.create_image(130, 450)
            tk_id2 = self.canvas.create_image(390, 450)
            faza = 0
            self.flag = True
            self.but = tkinter.Button(text="New Game", command=self.newgame, bg="yellow", width=15, height=2)
            self.but.place(x=200, y=420)
            self.end = tkinter.Button(text='Exit', command=self.gameover, bg='red', width=15, height=2)
            self.end.place(x=200, y=470)
            while self.flag:
                self.canvas.itemconfig(tk_id1, image=zoz[faza])
                self.canvas.itemconfig(tk_id2, image=zoz[faza])
                faza = (faza + 1) % len(zoz)
                self.canvas.update()
                self.canvas.after(100)


Checkers()
