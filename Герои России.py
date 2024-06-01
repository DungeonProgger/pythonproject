from os import *
from os.path import isfile
from tkinter.scrolledtext import ScrolledText
import HTML_creator
from HTML_creator import *


# поиск конфига проекта
def find_config(path):
    # Находим первый файл с расширением .ini в указанной директории
    cfg_file_list = [i for i in listdir(path) if isfile(join(path, i)) and i.count('.ini') == 1]
    return join(path, cfg_file_list[0])


# открытие конфига и изменение текущего окна под новые настройки
def cfg_open():
    # открытие окна для выбора файла конфига
    cfg_path = filedialog.askopenfilename(title="Выберите ini файл", filetypes=(("config", "*.ini"), ("all", "*.*")))
    if cfg_path != '':
        data_dir = path.join(cfg_path[:cfg_path.rfind('\\') + 1], 'yourdata')
        cfg = configparser.ConfigParser()
        cfg.read(cfg_path, 'utf8')

        # установка заголовка окна и его размера
        form1.title(cfg.get('main', 'name'))
        l, t, w, h = (form1.winfo_screenwidth() - int(cfg.get('main', 'width'))) // 2, (
                form1.winfo_screenheight() - int(cfg.get('main', 'height'))) // 2, cfg.get('main', 'width'), cfg.get(
            'main', 'height')
        form1.geometry(f"{w}x{h}+{l}+{t}")

        data = configparser.ConfigParser()
        data.read(find_config(data_dir), 'utf8')

        # Заполнение списка имен из файла конфига
        names = []
        for i in range(len(data.sections())):
            name = str(data.get('Item' + str(i), 'info'))
            name = name.replace('.txt', '')
            names.append(name)
        lb1.config(listvariable=(Variable(value=names)))

        # отображение первого элемента
        f_path = path.join(data_dir, data.get('Item0', 'info'))
        img_path = path.join(data_dir, data.get('Item0', 'image'))
        f = codecs.open(f_path, "r", "utf8")
        text = f.read()
        f.close()
        img = PhotoImage(file=str(img_path))
        st.config(state='normal')
        st.delete("1.0", END)
        st.insert(END, text)
        st.config(state='disabled')
        label1.config(image=img)
        img.image = img


# обработка выбора пользователя и изменение содержимого окна в зависимости от этого выбора
def on_selection(event, data):
    item_val = lb1.curselection()[0]
    f_path = path.join(path.join(os.getcwd(), 'yourdata'), data.get('Item' + str(item_val), 'info'))
    img_path = path.join(path.join(os.getcwd(), 'yourdata'), data.get('Item' + str(item_val), 'image'))

    # отображение выбранного элемента
    f = codecs.open(f_path, "r", "utf8")
    text = f.read()
    f.close()
    img = PhotoImage(file=str(img_path))
    st.config(state='normal')
    st.delete("1.0", END)
    st.insert(END, text)
    st.config(state='disabled')
    label1.config(image=img)
    img.image = img


# создание всех окон приложения и заполнения их данными из файлов
form1 = Tk()
cfg_path = find_config(os.getcwd())
data_dir = os.getcwd()
cfg = configparser.ConfigParser()
cfg.read(cfg_path, 'utf8')

# установка заголовка и размера главного окна
form1.title(cfg.get('main', 'name'))
l, t, w, h = (form1.winfo_screenwidth() - int(cfg.get('main', 'width'))) // 2, (
            form1.winfo_screenheight() - int(cfg.get('main', 'height'))) // 2, cfg.get('main', 'width'), cfg.get('main',
                                                                                                                 'height')
form1.geometry(f"{w}x{h}+{l}+{t}")

# создание меню приложения
main_menu = Menu()
help_menu = Menu(tearoff=0)
info_menu = Menu(tearoff=0)
main_menu.add_cascade(label="Меню", menu=help_menu)
help_menu.add_cascade(label="Открыть", command=cfg_open)
help_menu.add_cascade(label="Галлерея", command=lambda: HTML_creator.gallery(form1, label1))
help_menu.add_separator()
help_menu.add_cascade(label="Выход", command=form1.destroy)
info_menu.add_separator()

data = configparser.ConfigParser()
data.read(find_config(join(data_dir, 'yourdata')), 'utf8')

f_path = path.join(path.join(os.getcwd(), 'yourdata'), data.get('Item0', 'info'))
img_path = path.join(path.join(os.getcwd(), 'yourdata'), data.get('Item0', 'image'))
f = codecs.open(f_path, "r", "utf8")
text = f.read()
f.close()

# создание основного окна и выпадающего окна с меню и режимом презентации
frame0 = Frame(master=form1, borderwidth=0, relief='solid')
pw1 = PanedWindow(master=frame0, orient='horizontal', sashwidth=5)
pw1.pack(expand=True, fill='both')

# создание списка людей
frame1 = Frame(master=pw1, borderwidth=0, relief='solid')
names = []
for i in range(len(data.sections())):
    name = str(data.get('Item' + str(i), 'info'))
    name = name.replace('.txt', '')
    names.append(name)
lb1 = Listbox(master=frame1, listvariable=Variable(value=names), selectmode=SINGLE)
lb1.pack(anchor=NW, fill='both', expand=True, side=LEFT)
scrollbar1 = Scrollbar(master=frame1, orient='vertical', command=lb1.yview)
scrollbar1.pack(side=RIGHT, fill=Y)
lb1.config(yscrollcommand=scrollbar1.set)
frame2 = Frame(master=pw1, borderwidth=0, relief='solid')
pw2 = PanedWindow(master=frame2, orient='vertical', sashwidth=5)
pw2.pack(expand=True, fill='both')

# Создание поля для картинки
frame3 = Frame(master=pw2, borderwidth=0, relief='solid')
frame4 = Frame(master=pw2, borderwidth=0, relief='solid')
img = PhotoImage(file=str(img_path))
label1 = Label(master=frame3, image=img)
label1.pack(fill='both', expand=True)

# создание поля для описания человека
st = ScrolledText(master=frame4, wrap='word')
st.insert(INSERT, text)
st.config(state='disabled')
st.pack(fill='both', expand=True)

# размещение фреймов в окне приложения
frame3.pack(anchor=NW)
frame4.pack(anchor=SW)
pw2.add(frame3, height=400)
pw2.add(frame4, height=200)
frame1.pack(anchor=NW)
frame2.pack(anchor=NE)
pw1.add(frame1, width=200)
pw1.add(frame2, width=600)
frame0.pack(expand=True, fill=BOTH)

lb1.bind('<<ListboxSelect>>', lambda e, arg1=data: on_selection(e, arg1))
form1.config(menu=main_menu)
form1.mainloop()
