import tkinter as tk
import calendar
from tkinter import simpledialog, messagebox
from datetime import datetime
import json
import os

class StudyBuddyApp:
    

    def __init__(self, root):
        self.root = root
        self.root.title("StudyBuddy")
        self.root.geometry("700x500")
        

        self.tasks = []

        self.data_file = "tasks.json"

        self.load_tasks()

        # Sidebar frame
        self.sidebar = tk.Frame(root, width=150, bg="#a3c1ad")
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.main_area = tk.Frame(root, bg="white")
        self.main_area.pack(side="right", fill="both", expand=True)

    
        # Sidebar buttons
        buttons = [("Tasks", self.show_tasks),
                   ("Timer", self.show_timer),
                   ("Calendar", self.show_calendar),
        ]
        exit_btn = tk.Button(self.sidebar, text="Exit", font=("Helvetica", 12), bg="#f28b82", command=self.exit_app) 
        exit_btn.pack(fill="x", pady=5, padx=5)


        for (text, command) in buttons:
            btn = tk.Button(self.sidebar, text=text, command=command, font=("Helvetica", 12), bg="#d5e4d7")
            btn.pack(fill="x", pady=5, padx=5)

        # Show welcome message initially
        self.show_welcome()

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    
    
    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_main_area()
        label = tk.Label(self.main_area, text="Welcome to StudyBuddy!\nSelect an option from the left.", font=("Helvetica", 16), bg="white")
        label.pack(pady=100)
       
    def show_tasks(self):
        self.clear_main_area()

        frame = tk.Frame(self.main_area, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        label = tk.Label(frame, text="Tasks", font=("Helvetica", 16), bg="white")
        label.pack()

        self.task_listbox = tk.Listbox(frame, height=10, font=("Helvetica", 12))
        self.task_listbox.pack(fill="x", pady=10)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack()

        add_btn = tk.Button(btn_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side="left", padx=5)

        edit_btn = tk.Button(btn_frame, text="Edit Task", command=self.edit_task)
        edit_btn.pack(side="left", padx=5)

        del_btn = tk.Button(btn_frame, text="Delete Task", command=self.delete_task)
        del_btn.pack(side="left", padx=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display = f"{task['title']} [{task['category']}] - Due: {task['due_date']}"
            self.task_listbox.insert(tk.END, display)

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Task Title:")
        if not title:
            return

        category = simpledialog.askstring("Add Task", "Category (Homework, Study, Exam Prep, Personal):")
        if category not in ["Homework", "Study", "Exam Prep", "Personal"]:
            messagebox.showerror("Error", "Invalid category.")
            return

        due_date = simpledialog.askstring("Add Task", "Due Date (YYYY-MM-DD):")
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Error", "Invalid date format.")
            return

        self.tasks.append({"title": title, "category": category, "due_date": due_date})
        self.refresh_task_list()
        self.save_tasks()


    def edit_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("Edit Task", "Select a task first.")
            return

        index = selection[0]
        task = self.tasks[index]

        title = simpledialog.askstring("Edit Task", "Task Title:", initialvalue=task["title"])
        if not title:
            return

        category = simpledialog.askstring("Edit Task", "Category (Homework, Study, Exam Prep, Personal):", initialvalue=task["category"])
        if category not in ["Homework", "Study", "Exam Prep", "Personal"]:
            messagebox.showerror("Error", "Invalid category.")
            return

        due_date = simpledialog.askstring("Edit Task", "Due Date (YYYY-MM-DD):", initialvalue=task["due_date"])
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Error", "Invalid date format.")
            return

        self.tasks[index] = {"title": title, "category": category, "due_date": due_date}
        self.refresh_task_list()
        self.save_tasks()


    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("Delete Task", "Select a task first.")
            return

        index = selection[0]
        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            self.tasks.pop(index)
            self.refresh_task_list()
            self.save_tasks()


    def show_timer(self):
        self.clear_main_area()

        

        frame = tk.Frame(self.main_area, bg="white")
        frame.pack(expand=True)

    # Label for timer display
        self.timer_label = tk.Label(frame, text="25:00", font=("Helvetica", 48), bg="white")
        self.timer_label.pack(pady=20)

    # Input for minutes
        input_frame = tk.Frame(frame, bg="white")
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Set minutes:", bg="white", font=("Helvetica", 12)).pack(side="left")
        self.minutes_entry = tk.Entry(input_frame, width=5, font=("Helvetica", 12))
        self.minutes_entry.pack(side="left", padx=5)
        self.minutes_entry.insert(0, "25")  # default 25 minutes
    # Buttons
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack()

        start_btn = tk.Button(btn_frame, text="Start", command=self.start_timer)
        start_btn.pack(side="left", padx=5)

        pause_btn = tk.Button(btn_frame, text="Pause", command=self.pause_timer)
        pause_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_timer)
        reset_btn.pack(side="left", padx=5)

    # Timer state
        self.timer_seconds = 25 * 60
        self.timer_running = False
        self.timer_id = None


    def update_timer(self):
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.timer_seconds > 0 and self.timer_running:
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.timer_seconds == 0:
            self.timer_running = False
            messagebox.showinfo("Time's up!", "Your study session has ended!")

    def start_timer(self):
        if not self.timer_running:
        # Get minutes from entry
            try:
                minutes = int(self.minutes_entry.get())
                if minutes <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter a positive integer for minutes.")
                return

            self.timer_seconds = minutes * 60
            self.timer_running = True
            self.update_timer()


    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

    def reset_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        try:
            minutes = int(self.minutes_entry.get())
            if minutes <= 0:
                minutes = 25
        except Exception:
            minutes = 25

        self.timer_seconds = minutes * 60
        self.timer_label.config(text=f"{minutes:02d}:00")


    def show_calendar(self):
        self.clear_main_area()

        frame = tk.Frame(self.main_area, bg="white")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        today = datetime.now()
        year = today.year
        month = today.month

    # Title: Month Year
        title = tk.Label(frame, text=f"{calendar.month_name[month]} {year}", font=("Helvetica", 16), bg="white")
        title.grid(row=0, column=0, columnspan=7, pady=10)

    # Weekday headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(frame, text=day, font=("Helvetica", 12, "bold"), bg="white").grid(row=1, column=i, padx=5, pady=5)

    # Month calendar data (weeks x days)
        month_days = calendar.monthcalendar(year, month)

    # Task category colors
        category_colors = {
            "Homework": "#FF9999",
            "Study": "#99CCFF",
            "Exam Prep": "#FFCC99",
            "Personal": "#99FF99"
        }
    def exit_app(self):
        self.root.quit()  # closes the app window

    # Callback when clicking a date
    def on_date_click(day):
        if day == 0:
            return
        date_str = f"{year}-{month:02d}-{day:02d}"
        due_tasks = [t for t in self.tasks if t["due_date"] == date_str]
        if not due_tasks:
            messagebox.showinfo("Tasks", f"No tasks due on {date_str}")
            return

        # Show tasks in a popup
        msg = ""
        for t in due_tasks:
            msg += f"{t['title']} [{t['category']}]\n"
        messagebox.showinfo(f"Tasks due {date_str}", msg)

    # Create buttons for each day
        for week_num, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                if day == 0:
                # Empty cell (day from previous/next month)
                    lbl = tk.Label(frame, text="", width=4, height=2, bg="white")
                    lbl.grid(row=week_num + 2, column=day_idx, padx=2, pady=2)
                else:
                # Check if tasks on this day for coloring
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    tasks_for_day = [t for t in self.tasks if t["due_date"] == date_str]
                    color = category_colors.get(tasks_for_day[0]["category"], "white") if tasks_for_day else "white"

                    btn = tk.Button(frame, text=str(day), width=4, height=2, bg=color, command=lambda d=day: on_date_click(d))
                    btn.grid(row=week_num + 2, column=day_idx, padx=2, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyBuddyApp(root)
    root.mainloop()
