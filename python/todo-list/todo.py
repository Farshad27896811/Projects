import json
import os
from datetime import datetime, timedelta
import threading
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Task:
    def __init__(self, title, priority="متوسط", category="عمومی", deadline=None, description="", completed=False, done_date=None):
        self.title = title
        self.priority = priority  # "کم", "متوسط", "زیاد"
        self.category = category
        self.deadline = deadline  # رشته تاریخ مثل "2025-05-30 15:00"
        self.description = description
        self.completed = completed
        self.done_date = done_date

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "category": self.category,
            "deadline": self.deadline,
            "description": self.description,
            "completed": self.completed,
            "done_date": self.done_date
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data.get("priority", "متوسط"),
            data.get("category", "عمومی"),
            data.get("deadline"),
            data.get("description", ""),
            data.get("completed", False),
            data.get("done_date")
        )

class ToDoList:
    def __init__(self, filename="todo.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return [Task.from_dict(item) for item in data]
                except json.JSONDecodeError:
                    return []
        return []

    def save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def edit_task(self, index, new_task: Task):
        if 0 <= index < len(self.tasks):
            self.tasks[index] = new_task
            self.save_tasks()

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.completed = True
            task.done_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_tasks()

    def search_tasks(self, keyword):
        return [task for task in self.tasks if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]

    def filter_tasks(self, completed=None, category=None, priority=None):
        filtered = self.tasks
        if completed is not None:
            filtered = [t for t in filtered if t.completed == completed]
        if category is not None and category != "همه":
            filtered = [t for t in filtered if t.category == category]
        if priority is not None and priority != "همه":
            filtered = [t for t in filtered if t.priority == priority]
        return filtered

    def get_report(self):
        total = len(self.tasks)
        done = len([t for t in self.tasks if t.completed])
        pending = total - done
        return f"کل کارها: {total}\nانجام‌شده: {done}\nدر انتظار: {pending}"

# ---------------------- رابط گرافیکی ----------------------

class ToDoApp:
    def __init__(self, root):
        self.todo = ToDoList()
        self.root = root
        self.root.title("مدیریت کارها پیشرفته")
        self.root.geometry("850x500")

        # بخش فیلتر و جستجو
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill="x")

        tk.Label(top_frame, text="جستجو:").pack(side="right")
        self.search_var = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.search_var).pack(side="right", padx=5)
        tk.Button(top_frame, text="جستجو", command=self.search_task).pack(side="right", padx=5)

        # فیلتر دسته‌بندی
        tk.Label(top_frame, text="دسته‌بندی:").pack(side="right", padx=10)
        self.category_var = tk.StringVar(value="همه")
        categories = ["همه"] + list(set([t.category for t in self.todo.tasks]))
        self.category_combo = ttk.Combobox(top_frame, values=categories, textvariable=self.category_var, width=15)
        self.category_combo.pack(side="right")
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_tasks())

        # فیلتر اولویت
        tk.Label(top_frame, text="اولویت:").pack(side="right", padx=10)
        self.priority_var = tk.StringVar(value="همه")
        priorities = ["همه", "کم", "متوسط", "زیاد"]
        self.priority_combo = ttk.Combobox(top_frame, values=priorities, textvariable=self.priority_var, width=10)
        self.priority_combo.pack(side="right")
        self.priority_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_tasks())

        # فیلتر وضعیت
        tk.Label(top_frame, text="وضعیت:").pack(side="right", padx=10)
        self.status_var = tk.StringVar(value="همه")
        statuses = [("همه", "all"), ("انجام‌شده", "done"), ("در انتظار", "pending")]
        for text, val in statuses:
            tk.Radiobutton(top_frame, text=text, variable=self.status_var, value=val, command=self.filter_tasks).pack(side="right")

        # جدول نمایش کارها
        columns = ("عنوان", "اولویت", "دسته‌بندی", "تاریخ سررسید", "وضعیت", "توضیحات")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "توضیحات" else 250)
        self.tree.pack(expand=True, fill="both")

        # دکمه‌ها
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="افزودن کار", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="ویرایش", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="حذف", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="انجام‌شده", command=self.mark_done).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="نمایش گزارش", command=self.show_report).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="نمایش همه", command=self.refresh_list).grid(row=0, column=5, padx=5)

        self.refresh_list()
        self.start_reminder_thread()

    def refresh_list(self, tasks=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if tasks is None:
            tasks = self.todo.tasks
        for i, task in enumerate(tasks):
            status = "✅" if task.completed else "⏳"
            deadline = task.deadline if task.deadline else "-"
            self.tree.insert("", "end", iid=i, values=(task.title, task.priority, task.category, deadline, status, task.description))

    def add_task(self):
        dialog = TaskDialog(self.root)
        self.root.wait_window(dialog.top)
        if dialog.task:
            self.todo.add_task(dialog.task)
            self.update_categories()
            self.refresh_list()

    def edit_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("هشدار", "یک کار را انتخاب کنید.")
            return
        index = int(selected)
        task = self.todo.tasks[index]

        dialog = TaskDialog(self.root, task)
        self.root.wait_window(dialog.top)
        if dialog.task:
            self.todo.edit_task(index, dialog.task)
            self.update_categories()
            self.refresh_list()

    def delete_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("هشدار", "یک کار را انتخاب کنید.")
            return
        index = int(selected)
        self.todo.remove_task(index)
        self.update_categories()
        self.refresh_list()

    def mark_done(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("هشدار", "یک کار را انتخاب کنید.")
            return
        index = int(selected)
        self.todo.mark_done(index)
        self.refresh_list()

    def search_task(self):
        keyword = self.search_var.get()
        if keyword.strip() == "":
            self.refresh_list()
            return
        results = self.todo.search_tasks(keyword)
        self.refresh_list(results)

    def filter_tasks(self):
        status = self.status_var.get()
        if status == "all":
            completed = None
        elif status == "done":
            completed = True
        else:
            completed = False

        category = self.category_var.get()
        priority = self.priority_var.get()

        filtered = self.todo.filter_tasks(completed=completed, category=category, priority=priority)
        self.refresh_list(filtered)

    def show_report(self):
        report = self.todo.get_report()
        messagebox.showinfo("گزارش وضعیت کارها", report)

    def update_categories(self):
        categories = ["همه"] + sorted(set([t.category for t in self.todo.tasks]))
        self.category_combo['values'] = categories
        if self.category_var.get() not in categories:
            self.category_var.set("همه")

    def start_reminder_thread(self):
        def reminder_loop():
            while True:
                now = datetime.now()
                for i, task in enumerate(self.todo.tasks):
                    if task.deadline and not task.completed:
                        try:
                            deadline_dt = datetime.strptime(task.deadline, "%Y-%m-%d %H:%M")
                            diff = (deadline_dt - now).total_seconds()
                            if 0 < diff <= 60:  # یادآوری 1 دقیقه قبل از سررسید
                                self.root.after(0, lambda t=task: messagebox.showinfo("یادآوری", f"کار '{t.title}' به زمان سررسید نزدیک شده!"))
                        except:
                            pass
                time.sleep(30)

        t = threading.Thread(target=reminder_loop, daemon=True)
        t.start()

class TaskDialog:
    def __init__(self, parent, task=None):
        self.task = None
        self.top = tk.Toplevel(parent)
        self.top.title("افزودن/ویرایش کار")
        self.top.geometry("400x400")
        self.top.grab_set()

        tk.Label(self.top, text="عنوان کار:").pack(anchor="w", padx=10, pady=5)
        self.title_var = tk.StringVar(value=task.title if task else "")
        tk.Entry(self.top, textvariable=self.title_var).pack(fill="x", padx=10)

        tk.Label(self.top, text="توضیحات:").pack(anchor="w", padx=10, pady=5)
        self.desc_text = tk.Text(self.top, height=5)
        if task:
            self.desc_text.insert("1.0", task.description)
        self.desc_text.pack(fill="x", padx=10)

        tk.Label(self.top, text="اولویت:").pack(anchor="w", padx=10, pady=5)
        self.priority_var = tk.StringVar(value=task.priority if task else "متوسط")
        ttk.Combobox(self.top, values=["کم", "متوسط", "زیاد"], textvariable=self.priority_var).pack(fill="x", padx=10)

        tk.Label(self.top, text="دسته‌بندی:").pack(anchor="w", padx=10, pady=5)
        self.category_var = tk.StringVar(value=task.category if task else "عمومی")
        tk.Entry(self.top, textvariable=self.category_var).pack(fill="x", padx=10)

        tk.Label(self.top, text="تاریخ سررسید (YYYY-MM-DD HH:MM):").pack(anchor="w", padx=10, pady=5)
        self.deadline_var = tk.StringVar(value=task.deadline if task else "")
        tk.Entry(self.top, textvariable=self.deadline_var).pack(fill="x", padx=10)

        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="ذخیره", command=self.save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="انصراف", command=self.top.destroy).pack(side="left", padx=5)

    def save(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("خطا", "عنوان کار نمی‌تواند خالی باشد.")
            return
        description = self.desc_text.get("1.0", "end").strip()
        priority = self.priority_var.get()
        category = self.category_var.get().strip() or "عمومی"
        deadline = self.deadline_var.get().strip()
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("خطا", "فرمت تاریخ سررسید باید به شکل YYYY-MM-DD HH:MM باشد.")
                return

        self.task = Task(title, priority, category, deadline, description)
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()