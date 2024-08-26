from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from main import *

def openfile1():
    filepath = filedialog.askopenfilename()
    entry11.delete(0,END)
    entry11.insert(END, filepath)
def openfile2():
    filepath = filedialog.askopenfilename()
    entry12.delete(0,END)
    entry12.insert(END, filepath)
def openfile3():
    filepath = filedialog.askopenfilename()
    entry13.delete(0,END)
    entry13.insert(END, filepath)
def openfile4():
    filepath = filedialog.askopenfilename()
    entry14.delete(0,END)
    entry14.insert(END, filepath)
def openfile5():
    filepath = filedialog.askopenfilename()
    entry15.delete(0,END)
    entry15.insert(END, filepath)

window = Tk()

mainframe = ttk.Notebook()
mainframe.grid(column = 0, row = 0)

frame1 = ttk.Frame(mainframe)
frame2 = ttk.Frame(mainframe)
frame3 = ttk.Frame(mainframe)
frame4 = ttk.Frame(mainframe)

#вкладка 1
label00 = Label(frame1, text = "Цикл записи: хз")
label01 = Label(frame1, text = "Имя и текущей размер архива: test")
label02 = Label(frame1, text = "Число изменившихся аналоговых параметров: 0")
label03 = Label(frame1, text = "Число изменившихся дискретных параметров: 0")
label04 = Label(frame1, text = "Среднее число изменившихся параметров")

label00.grid(column = 0, row = 0)
label01.grid(column = 0, row = 1)
label02.grid(column = 0, row = 2)
label03.grid(column = 0, row = 3)
label04.grid(column = 0, row = 4)

#вкладка 2
label11 = Label(frame2, text = "Имя исходного файла текущих значений аналоговых параметров")
entry11 = Entry(frame2, width = 50)
button11 = Button(frame2,text = "Открыть", command = openfile1)

label12 = Label(frame2, text = "Имя исходного файла текущих значений дискретных параметров")
entry12 = Entry(frame2, width = 50)
button12 = Button(frame2,text = "Открыть", command = openfile2)

label13 = Label(frame2, text = "Имя создаваемого общего файла текущих значений всех параметров")
entry13 = Entry(frame2, width = 50)
button13 = Button(frame2,text = "Открыть", command = openfile3)

label14 = Label(frame2, text = "Имя создаваемого файла изменившихся значений параметров")
entry14 = Entry(frame2, width = 50)
button14 = Button(frame2,text = "Открыть", command = openfile4)

label15 = Label(frame2, text = "Путь к создаваемым архивам")
entry15 = Entry(frame2, width = 50)
button15 = Button(frame2,text = "Открыть", command = openfile5)

label11.grid(column = 0, row = 0, columnspan = 2)
entry11.grid(column = 0, row = 1)
button11.grid(column = 1, row = 1)

label12.grid(column = 0, row = 2, columnspan = 2)
entry12.grid(column = 0, row = 3)
button12.grid(column = 1, row = 3)

label13.grid(column = 0, row = 4, columnspan = 2)
entry13.grid(column = 0, row = 5)
button13.grid(column = 1, row = 5)

label14.grid(column = 0, row = 6, columnspan = 2)
entry14.grid(column = 0, row = 7)
button14.grid(column = 1, row = 7)

label15.grid(column = 0, row = 8, columnspan = 2)
entry15.grid(column = 0, row = 9)
button15.grid(column = 1, row = 9)

entry11.insert(END, r"C:\spd3\out\out.0")
entry12.insert(END, r"C:\spd3\out\out.1")
entry13.insert(END, r"C:\spd3\dat\out.dat")
entry14.insert(END, r"C:\spd3\dat\x.dat")
entry15.insert(END, r"C:\spd3\arc")

#вкладка 3
label31 = Label(frame3, text = "Периодичность чтения исходных данных, мсек")

check31 = Checkbutton(frame3, text = "Создавать архивный файл значений всех параметров")
check32 = Checkbutton(frame3, text = "Записывать в файл архив значения с признаком недостоверности")
check33 = Checkbutton(frame3, text = "Вести журнал состояния процесса архивирования")
check34 = Checkbutton(frame3, text = "Вести журнал учета времени работы оборудования")
check35 = Checkbutton(frame3, text = "Считать, что файлы текущих значений не обновляются (отставание)")

label31.grid(column = 0, row = 0)

check31.grid(column = 0, row = 1)
check32.grid(column = 0, row = 2)
check33.grid(column = 0, row = 3)
check34.grid(column = 0, row = 4)
check35.grid(column = 0, row = 5)

read_path = entry13.get()
data_to_archive = get_data_from_dat_file(read_path)

def get():
    data_to_archive = get_data_from_dat_file(read_path)

def wrtd():
    write_data_to_archive_file(desc_path, data_to_archive)

button0 = Button(text = "Собрать архив", command = wrtd)
button1 = Button(text = "Прочитать архив", command = get)

button0.grid(column = 0, row = 5)
button1.grid(column = 0, row = 6)


frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()

mainframe.add(frame1, text = "Основное")
mainframe.add(frame2, text = "Пути")
mainframe.add(frame3, text = "Архивирование")
mainframe.add(frame4, text = "Сервис")

window.mainloop()