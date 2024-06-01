import webbrowser
from tkinter import *
import codecs
import pathlib
import os
from os.path import join
from pathlib import Path
from tkinter import filedialog
import configparser

# выбор файла конфига
def galery_open(label, form):
    _cfg_path = filedialog.askopenfilename(title="Выберите ini файл", filetypes=(("config", "*.ini"), ("all", "*.*")))
    label.config(text=_cfg_path)
    form.lift()

# чтение данных из файла
def read_description(file_path):
    descr = codecs.open(filename=file_path, mode="r", encoding="utf8")
    text = descr.read()
    descr.close()
    return text

# функция для создания отображения данных приложения в веб браузере
def create_gallery(choice, form, label2, label1):
    _cfg_path = label2.cget("text")
    form.destroy()
    label1.config(image=label1.cget("image"))
    data_dir = join(_cfg_path[:_cfg_path.rfind('\\') + 1], 'yourdata')
    _cfg_path = pathlib.Path(_cfg_path)
    _cfg = configparser.ConfigParser()
    _cfg.read(_cfg_path, 'utf-8')
    _cfg_path = str(_cfg_path)
    index = configparser.ConfigParser()
    index.read(join(data_dir, 'index.ini'), encoding='utf8')
    _names = []
    _photos = []
    # собираем имена и пути к фотографиям
    for i in range(len(index.sections())):
        _names.append(join(data_dir, index.get(f"Item{i}", 'info')))
        _photos.append(join(data_dir, index.get(f"Item{i}", 'image')))

    filename = Path(join(_cfg_path[:_cfg_path.rfind('/') + 1], _cfg.get('main', 'name')) + '.html')
    file = codecs.open(filename=filename, mode= "w", encoding="utf8")
    # HTML код для начала страницы
    file.write("""<!DOCTYPE html>
    <html lang="ru">
    <head>
    <meta charset="UTF-8">
    <title>База данных</title>
    <style>
    body { font-family: Arial, sans-serif; }
    .page { display: none; }
    .page.active { display: block; }
    img { max-width: 100%; height: auto; }
    button { margin: 5px; padding: 10px; }
    .inline {display:inline-block;margin-right:5px;}
    </style>
    <script>
    function showPage(pageId) 
    {const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');}
    </script>
    </head>
    <body>
    <div id="main" class="page active">
    <p align="center" style="margin-bottom: 150px;"><font size="7"><b>Галерея</b></font></p><p align="center" style="margin-bottom: 200px;"><font size="5">""")

    file.write(_cfg.get('main', 'name'))
    file.write("""</font></p><center><button onclick="showPage('page1')"><font size="3">Начать просмотр</font></button></center></div>""")
    # HTML код для каждой страницы
    for i in range(len(index.sections())):
        prev_page_id = f"page{i}" if i > 0 else "main"
        next_page_id = f"page{i + 2}" if i < (len(index.sections()) - 1) else "main"
        button_next = f"<button onclick=\"showPage('{next_page_id}')\">{'Вперед' if i < (len(index.sections()) - 1) else 'Вернуться на главную'}</button>"
        description = read_description(_names[i])
        file.write(f"""<div id="page{i + 1}" class="page"><center><img src="{_photos[i]}" alt="Фотография {i + 1}"></center><p>{description}</p><div align="center"><button onclick="showPage('{prev_page_id}')">Назад</button>{button_next}</div></div>""")
    file.write("""</body></html>""")
    file.close()
    # Открытие созданного HTML файла в  веб браузере
    if choice.get():
        webbrowser.open_new_tab(filename)

# функция для открытия окна выбора папки и создания представления
def gallery(form1, label1):
    form3 = Toplevel(master=form1)
    form3.title("Выбор папки")
    w, h = 500, 100
    l, t = (form3.winfo_screenwidth() - w) // 2, (form3.winfo_screenheight() - h) // 2
    form3.geometry(f"{w}x{h}+{l}+{t}")
    frame5 = Frame(master=form3, borderwidth=0, relief='solid')
    frame6 = Frame(master=form3, borderwidth=0, relief='solid')
    label2 = Label(master=frame5, text=join(os.getcwd(), 'Герои Росcии.ini'))
    button1 = Button(master=frame5, text='...', command=lambda: galery_open(label2, form3))
    choice = BooleanVar()
    choice.set(0)
    ch_button1 = Checkbutton(master=frame6, onvalue=1, offvalue=0, text='Открыть в браузере', variable=choice)
    button2 = Button(master=frame6, text="Закрыть", command=form3.destroy)
    button3 = Button(master=frame6, text="Создать галерею", command=lambda: create_gallery(choice, form3, label2, label1))
    button1.pack(side=RIGHT, padx=10, ipadx=10)
    label2.pack(side=LEFT, padx=10)
    ch_button1.pack(side=LEFT, padx=10)
    button2.pack(side=RIGHT, padx=10, pady=10)
    button3.pack(side=LEFT, padx=10, pady=10)
    frame5.pack(fill='both', anchor=NW, expand=True)
    frame6.pack(fill='both', anchor=SW, side=BOTTOM)
    form3.mainloop()