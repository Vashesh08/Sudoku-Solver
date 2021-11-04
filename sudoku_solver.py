import tkinter
import tkinter.messagebox
import tkinter.font
import random


class Sudoku:

    def __init__(self):
        self.possible_numbers = []
        self.integer_list = []
        for j in range(9):
            a = []
            for t in range(9):
                a.append({i for i in range(1, 10)})
            self.possible_numbers.append(a)

        self.box_list = [[tkinter.IntVar() for i in range(9)] for j in range(9)]

        self.box_to_list(0, 3)
        self.box_to_list(3, 6)
        self.box_to_list(6, 9)

    def box_to_list(self, a: int, d: int):
        b = []
        for t in range(a, d):
            for k in range(3):
                b.append(self.box_list[t][k])
        self.integer_list.append(b)

        b = []
        for t in range(a, d):
            for k in range(3, 6):
                b.append(self.box_list[t][k])
        self.integer_list.append(b)

        b = []
        for t in range(a, d):
            for k in range(6, 9):
                b.append(self.box_list[t][k])
        self.integer_list.append(b)

    def box_solve(self, a, b, val):
        if a < 3:
            p = 0
        elif a < 6:
            p = 3
        else:
            p = 6

        if b < 3:
            q = 0
        elif b < 6:
            q = 3
        else:
            q = 6

        temp = q

        for m in range(3):
            q = temp
            for n in range(3):
                if val in self.possible_numbers[p][q]:
                    self.possible_numbers[p][q].discard(val)
                q += 1
            p += 1

    def new_game(self):
        for i in range(9):
            for j in range(9):
                self.integer_list[i][j].set(0)

    def check(self):
        var = 0
        for i in range(9):
            for j in range(9):
                try:
                    if self.integer_list[i][j].get() < 0 or self.integer_list[i][j].get() > 9:
                        tkinter.messagebox.showinfo("Error", message="Please Enter a Number between 0 and 10")
                        return True
                    elif self.integer_list[i][j].get() != 0:
                        var += 1
                except tkinter.TclError:
                    tkinter.messagebox.showinfo("Error", message="Please Enter a Number. If number does not exists, enter '0'")
                    return True

        if var == 81:
            return True

        return False

    def remove_combinations(self):
        for i in range(9):
            for j in range(9):
                value = self.integer_list[i][j].get()
                # if value > 9 or value < 0:
                #     tkinter.messagebox.showinfo("Error", message="Please Enter a Number between 0 and 10")
                #     return None
                if value != 0:
                    self.possible_numbers[i][j].clear()
                    self.box_solve(i, j, value)
                    for k in range(9):
                        self.possible_numbers[i][k].discard(value)
                        self.possible_numbers[k][j].discard(value)

    def solve(self):
        self.remove_combinations()
        self.row_check()
        self.remove_combinations()
        self.column_check()
        self.remove_combinations()

        for i in range(9):
            for j in range(9):
                if len(self.possible_numbers[i][j]) == 1:
                    if self.integer_list[i][j].get() == 0:
                        var = self.possible_numbers[i][j].pop()
                        # print(i, j, var)
                        self.integer_list[i][j].set(var)

    def column_check(self):
        for i in range(9):
            a = dict()
            for v in range(1, 10):
                a.setdefault(v, 0)
            p = 1
            for k in range(9):
                for j in range(9):
                    if p in self.possible_numbers[j][i]:
                        a[p] += 1
                p += 1

            p = 1
            if 1 in a.values():
                for t in range(9):
                    f = 0
                    if a[p] == 1:
                        for w in range(9):
                            if p in self.possible_numbers[w][i]:
                                for k in range(9):
                                    if p == self.integer_list[w][k].get():
                                        f += 1
                                if f == 0:
                                    if self.box_not(w, i, p):
                                        self.integer_list[w][i].set(p)
                                        # print(w, i, p, sep=',')
                    p += 1

    def row_check(self):
        for i in range(9):
            a = dict()
            for v in range(1, 10):
                a.setdefault(v, 0)
            p = 1
            for k in range(9):
                for j in range(9):
                    if p in self.possible_numbers[i][j]:
                        a[p] += 1
                p += 1

            p = 1
            if 1 in a.values():
                for t in range(9):
                    f = 0
                    if a[p] == 1:
                        for w in range(9):
                            if p in self.possible_numbers[i][w]:
                                for k in range(9):
                                    if p == self.integer_list[k][w].get():
                                        f += 1
                                if f == 0:
                                    if self.box_not(i, w, p):
                                        self.integer_list[i][w].set(p)
                                        # print(i, w, p, sep=',')
                    p += 1

    def box_not(self, a, b, val):
        if a < 3:
            p = 0
        elif a < 6:
            p = 3
        else:
            p = 6

        if b < 3:
            q = 0
        elif b < 6:
            q = 3
        else:
            q = 6

        temp = q

        count = 0

        for m in range(3):
            q = temp
            for n in range(3):
                if val == self.integer_list[p][q].get():
                    count += 1
                q += 1
            p += 1

        if count > 1:
            return False

        return True

    def solve_sudoku(self):
        n = 0
        while n < 1000:
            if self.check():
                # print(n)
                return
            self.solve()
            n += 1
        else:
            tkinter.messagebox.showinfo("Error", message="Invalid Number of Inputs")



if __name__ == '__main__':
    main_window = tkinter.Tk()
    main_window.geometry('735x600')
    S = Sudoku()

    main_window.title("Sudoku Solver")
    main_window.maxsize(1366, 768)
    main_window.minsize(735, 555)

    font = tkinter.font.Font(font='TkHeadingFont', weight="ITALIC")

    new_list = ['red', 'green', 'orange']
    frame_list = []

    for i in range(9):
        frame_list.append(tkinter.Frame(main_window, background=new_list[random.randint(0, 2)], height=150, borderwidth=3, width=75, relief='sunken'))
        one_list = []
        for j in range(9):
            one_list.append(tkinter.Entry(frame_list[i], background='yellow', font=(font, 18), width=4, relief='sunken', justify='center', fg='black', textvariable=S.box_list[i][j]))
            one_list[j].grid(row=j // 3, column=j % 3, padx=1, pady=1,
                             ipady=10, ipadx=10)
        frame_list[i].grid(row=i // 3, column=i % 3, padx=2, pady=2, sticky='se')

    Solve_Button = tkinter.Button(main_window, text="Solve", fg='white', relief='raised', font=(font, 20), background='blue', activebackground='light green', command=S.solve_sudoku)
    Solve_Button.grid(row=3, column=0, sticky='nsew', pady=5, padx=2)

    New_Game_Button = tkinter.Button(main_window, text="Reset", fg='black', relief='raised', font=(font, 20), background='orange', activebackground='light green', command=S.new_game)
    New_Game_Button.grid(row=3, column=1, sticky='nsew', pady=5, padx=2)

    main_window.mainloop()
