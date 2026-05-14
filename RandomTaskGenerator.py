import tkinter as tk
import json
import random

# Загружаем задачи из файла
def load_tasks():
   try:
       with open("tasks.json", "r", encoding="utf-8") as file:
           return json.load(file)
   except (FileNotFoundError, json.JSONDecodeError):
       return []
   
# Сохраняем задачи в файл   
def save_tasks(task_list):
    with open("tasks.json", "w", encoding="utf-8") as file:
           json.dump(task_list, file, ensure_ascii=False, indent=4)
    
# Обновляем список задач в интерфейсе с учётом фильтра
def update_listbox():
   task_listbox.delete(0, tk.END)
   selected_type = filter_var.get()
   if selected_type == "Все":
       filtered_tasks = tasks
   else:
       filtered_tasks = [task for task in tasks if task.get("type", "работа") == selected_type]
   
   for task in filtered_tasks:
       task_listbox.insert(tk.END, f"{task['name']} [{task['type']}]")
       
# Добавляем новую задачу
def add_task():
   task = entry_task.get().strip()
   
   if(task!=""):
       task_type = type_var.get()
       tasks.append({"name": task, "type": task_type})
       entry_task.delete(0,tk.END)            
       update_listbox()
       save_tasks(tasks)
   else:
       error_label.config(text="Ошибка: введите текст задачи", fg="red")

random_tasks=[]

# Обновляем историю в интерфейсе
def update_history_listbox():
   history_listbox.delete(0, tk.END)
   for task in random_tasks:
       history_listbox.insert(tk.END, f"{task['name']} [{task['type']}]")

# Генерируем случайную задачу
def random_task():
    selected_type = filter_var.get()
    if selected_type == "Все":
        available_tasks = tasks
    else:
        available_tasks = [task for task in tasks if task.get("type", "работа") == selected_type]
    
    if available_tasks:
        num=random.randint(0, len(available_tasks)-1)
        selected_task = available_tasks[num]
        current_task_label["text"]=f"{selected_task['name']} [{selected_task['type']}]"
        random_tasks.append(selected_task)
        update_history_listbox()
        save_history()
        print(random_tasks)
    else:
        error_label.config(text="Ошибка: нет задач выбранного типа", fg="red")

# Сохраняем историю в JSON
def save_history():
    try:
        with open("history.json", "w", encoding="utf-8") as file:
            json.dump(random_tasks, file, ensure_ascii=False, indent=4)
    except:
        pass

# Загружаем историю из файла
def load_history():
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Применяем фильтр при изменении выбора
def apply_filter(*args):
   update_listbox()

# Создаём главное окно
window= tk.Tk()
window.title("Список задач")
window.geometry("600x700")

# Загружаем сохранённую историю
random_tasks = load_history()

# Список задач
task_listbox=tk.Listbox(window,height=8,width=50,selectmode=tk.SINGLE)
task_listbox.pack(pady=10)

tasks = load_tasks()

# Конвертируем старый формат задач, если нужно
if tasks and isinstance(tasks[0], str):
    tasks = [{"name": task, "type": "работа"} for task in tasks]
    save_tasks(tasks)

# Блок фильтрации
filter_frame = tk.Frame(window)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT, padx=5)

filter_var = tk.StringVar(value="Все")
filter_var.trace('w', apply_filter)

types = ["Все", "учеба", "спорт", "работа"]
for t in types:
    tk.Radiobutton(filter_frame, text=t, variable=filter_var, value=t).pack(side=tk.LEFT, padx=5)

# Выбор типа для новой задачи
type_frame = tk.Frame(window)
type_frame.pack(pady=5)

tk.Label(type_frame, text="Тип новой задачи:").pack(side=tk.LEFT, padx=5)

type_var = tk.StringVar(value="работа")
type_menu = tk.OptionMenu(type_frame, type_var, "учеба", "спорт", "работа")
type_menu.pack(side=tk.LEFT)

# Поле ввода новой задачи
entry_task=tk.Entry(window,font="Arial 12", width=40)
entry_task.pack(pady=10)

# Кнопка добавления
but_add=tk.Button(window,text="Добавить задачу", bg="green", fg="white", command=add_task)
but_add.pack(pady=5)

# Кнопка генерации
but_random=tk.Button(window,text="Сгенерировать задачу",bg="lightblue",fg="white", command=random_task)
but_random.pack(pady=5)

# Отображение текущей задачи
current_task_label=tk.Label(window,text="Нажмите кнопку для генерации", font="Arial 12", fg="blue", wraplength=500)
current_task_label.pack(pady=10)

# Метка для ошибок
error_label=tk.Label(window, text="", font="Arial 10", fg="red")
error_label.pack(pady=5)

# Блок истории
tk.Label(window, text="История сгенерированных задач:", font="Arial 10 bold").pack(pady=5)
history_listbox=tk.Listbox(window,height=8,width=50)
history_listbox.pack(pady=5)
update_history_listbox()

window.mainloop()