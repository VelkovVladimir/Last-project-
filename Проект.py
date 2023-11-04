import tkinter as tk
from tkinter import ttk
import sqlite3

# класс главного окна
class Main(tk.Frame):
    def __init__(self,root):
        # наследование из родительского класса
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        # панель инструментов
        # закрашиваем поле в определенный цвет 
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        # размищаем нашу колонку с ее характреристиками. Со смещение к верху и с растягиванием по горизонту(прямоугольник)
        toolbar.pack(side=tk.TOP, fill =tk.X)

        #создание кнопки добавления контакта
        self.add_img =tk.PhotoImage(file='./img/add.png')
        # настройка кнопки(ее цвета и границы)
        btn_add=tk.Button(toolbar, bg='#d7d7d7', bd=0,
                          image=self.add_img,
                          command=self.open_dialog)
        
        #создание кнопки редактирования  контакта
        self.edit_img =tk.PhotoImage(file='./img/update.png')
        # настройка кнопки(ее цвета и границы)
        btn_edit = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                          image=self.edit_img,
                          command=self.open_edit)
    
        #создание кнопки удаления  контакта
        self.del_img =tk.PhotoImage(file='./img/delete.png')
        # настройка кнопки(ее цвета и границы)
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                          image=self.del_img,
                          command=self.delete_records)
        
        #создание кнопки поиска контакта
        self.search_img =tk.PhotoImage(file='./img/search.png')
        # настройка кнопки(ее цвета и границы)
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                          image=self.search_img,
                          command=self.open_search)
        
        #создание кнопки обновлния 
        self.refresh_img =tk.PhotoImage(file='./img/refresh.png')
        # настройка кнопки(ее цвета и границы)
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                          image=self.refresh_img,
                          command=self.view_records)

        #добавление команды (добавления, изменения, удаления, поиска)
        btn_add.pack(side=tk.LEFT)
        btn_edit.pack(side=tk.LEFT)
        btn_del.pack(side=tk.LEFT)
        btn_search.pack(side=tk.LEFT)
        btn_refresh.pack(side=tk.LEFT)

        #создание таблицы
        self.tree = ttk.Treeview(root, 
                                 column=('id', 'name', 'tel', 'email', 'salary'),
                                 height=45,
                                 show='headings')
        #добавляем параметры столбцам 
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        #даем столбцам названия
        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        # делаем полосу прокрутки
        scroll=tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
        # Выравнивание по левой стороне
        self.tree.pack(side=tk.LEFT)

    # метод добавления
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
     
    #метод редактирования 
    def edit_record(self, name, tel, email, salary):
        ind = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''',(name, tel, email, salary, ind))
        self.db.conn.commit()
        self.view_records()

    # метод удаления
    def delete_records(self):
        # цикл пробегает по всем строкам в таблицу
        for i in self.tree.selection():
            # берем id кажой строки
            id = self.tree.set(i, '#1')
            # удаляем по id (id, ) - кортеж
            self.db.cur.execute('''
                    DELETE FROM users 
                    WHERE id = ? 
                    ''',(id, ))
        self.db.conn.commit()
        self.view_records()

    # метод поиска записей
    def search_records(self, name):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM users WHERE name Like ? ',
                            ('%' + name + '%', ))
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]
    
    
    # вызов дочернего окна
    def open_dialog(self):
        child()

    # вызов окна редактирования
    def open_edit(self):
        Update()

    # вызов окна поиска
    def open_search(self):
        Search()

    # метод для передеачи значений из базы данных 
    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM users ')
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]


# класс дочернего окна (для добавления)
class child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # характеристики дочернего класса
    def init_child(self):
        
        # добавление название дочернему окну
        self.title('Добавление')
        
        # размер окна
        self.geometry('450x200')
        
        # запрет на изменение
        root.resizable(False,False)
       
        # перехват всех событий приложения        
        self.grab_set()
        
        #захватывает фокус (всегда будет сверху приложения родительного)
        self.focus_set()

        # создание формы
        # размещение названий данных
        lebel_name= tk.Label(self, text='ФИО')
        lebel_name.place(x=50,y=50)
        
        lebel_tel= tk.Label(self, text='Телефон')
        lebel_tel.place(x=50,y=80)
        
        lebel_email= tk.Label(self, text='E-mail')
        lebel_email.place(x=50,y=110)

        lebel_salary= tk.Label(self, text='Зарплата')
        lebel_salary.place(x=50,y=140)

        #размещение полей для ввода данных
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200,y=50)
        
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200,y=80)
        
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200,y=110)

        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200,y=140)
        
        #создание кнопки добавления в дочернем окне
        self.btn_ok=tk.Button(self,text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: 
                    self.view.records(
                        self.entry_name.get(),
                        self.entry_tel.get(),
                        self.entry_email.get(),
                        self.entry_salary.get()
                        ))
        self.btn_ok.place(x=350,y=170)

        #создание кнопки закрытия дочеренго окна

        btn_cancel=tk.Button(self,text='Закрыть', command=self.destroy)
        btn_cancel.place(x=260,y=170)

# дочернмй класс изменения контакта
class Update(child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_edit()
        self.load_data()

    def init_edit(self):
        self.title('Изменение работника')
        
        # убираем кнопку добавления
        self.btn_ok.destroy()

        #создание кнопки редактировать в дочернем окне
        self.btn_ok=tk.Button(self,text='Редактировать')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.edit_record(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get(),
            self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=350,y=170)

    # метод автозаполнения
    def load_data(self):
        self.db.cur.execute('''SELECT * FROM users WHERE id = ?''',
                    self.view.tree.set(self.view.tree.selection()[0], '#1'))

        row = self.db.cur.fetchone()

        self.entry_name.insert(0, row[1])
        
        self.entry_tel.insert(0, row[2])
    
        self.entry_email.insert(0, row[3]) 

        self.entry_salary.insert(0, row[4])
        
# класс поискового окна 
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    # характеристики дочернего класса
    def init_search(self):
        
        # добавление название дочернему окну
        self.title('Поиск')
        
        # размер окна
        self.geometry('300x100')
        
        # запрет на изменение
        root.resizable(False,False)
       
        # перехват всех событий приложения        
        self.grab_set()
        
        #захватывает фокус (всегда будет сверху приложения родительного)
        self.focus_set()

        # создание формы
        # размещение названий данных
        lebel_name= tk.Label(self, text='ФИО')
        lebel_name.place(x=30,y=30)

        #размещение полей для ввода данных
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=100,y=30)
        
        
        #создание кнопки поиска в дочернем окне
        self.btn_ok=tk.Button(self,text='Найти')
        self.btn_ok.bind('<Button-1>', 
                         lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', 
                         lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=230,y=70)

        #создание кнопки закрытия дочеренго окна
        btn_cancel=tk.Button(self,text='Закрыть', command=self.destroy)
        btn_cancel.place(x=140,y=70)


# класс бд
class Db:
    def __init__(self):
            self.conn=sqlite3.connect('contacts.db')
            self.cur=self.conn.cursor()
            self.cur.execute(''' 
                    CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            salary TEXT       
                    )''')
    
    # метод добавления бд

    def insert_data(self, name, tel, email, salary):
        self.cur.execute('''
                INSERT INTO users(name, phone, email, salary)
                VALUES (?, ?, ?, ?)''', (name, tel, email, salary))
    
        self.conn.commit()


# запуск файла, объявляя его главным
if __name__ =='__main__':
    root = tk.Tk()
    db = Db()
    app =Main(root)
    # название приложения
    root.title('Работники')
    # размер окна
    root.geometry('800x400')
    # запрет на изменение
    root.resizable(False,False)
    root.mainloop()