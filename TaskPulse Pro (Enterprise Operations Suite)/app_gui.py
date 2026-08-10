import csv
import datetime
import queue
import sqlite3
import threading
import time
from tkinter import filedialog, messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Appearance Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DB_FILE = "taskpulse_enterprise.db"
EXCEL_FILE = "taskpulse_report.xlsx"
CSV_FILE = "taskpulse_report.csv"


class TaskPulsePro(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("TaskPulse Pro - Enterprise Operations Suite")
    self.geometry("1100x720")
    self.minsize(850, 580)

    # Make grid layout fully responsive on resize/maximize
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)

    self.log_queue = queue.Queue()
    self.completed_tasks = []
    self.active_threads = 0

    self.init_db()
    self.build_ui()

    # Periodic Queue Checker for Thread-Safe GUI Updates
    self.after(100, self.process_queue)

  def init_db(self):
    """Initializes SQLite Database for Task History."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                status TEXT,
                duration_sec REAL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

  def build_ui(self):
    # 1. Header Frame (Row 0)
    self.header_frame = ctk.CTkFrame(self, fg_color="#0d1117", height=70)
    self.header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

    self.lbl_title = ctk.CTkLabel(
        self.header_frame,
        text="⚡ TASKPULSE PRO",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#10b981",
    )
    self.lbl_title.pack(side="left", padx=20, pady=15)

    self.lbl_sub = ctk.CTkLabel(
        self.header_frame,
        text="Enterprise Asynchronous Operations & Performance Suite",
        font=ctk.CTkFont(size=12),
        text_color="#94a3b8",
    )
    self.lbl_sub.pack(side="left", padx=0, pady=15)

    # Search Bar (Functionality 4)
    self.search_entry = ctk.CTkEntry(
        self.header_frame,
        placeholder_text="🔍 Search console logs...",
        width=200,
    )
    self.search_entry.pack(side="right", padx=15, pady=15)
    self.search_entry.bind("<KeyRelease>", self.filter_console_logs)

    # 2. Key Metrics Cards (Row 1)
    self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
    self.metrics_frame.grid(
        row=1, column=0, sticky="ew", padx=15, pady=(0, 10)
    )

    for i in range(4):
      self.metrics_frame.grid_columnconfigure(i, weight=1)

    self.card_completed = self.create_card(
        self.metrics_frame, "Completed Tasks", "0", "#3b82f6"
    )
    self.card_active = self.create_card(
        self.metrics_frame, "Active Threads", "0", "#f59e0b"
    )
    self.card_status = self.create_card(
        self.metrics_frame, "System Status", "Idle", "#10b981"
    )
    self.card_total_time = self.create_card(
        self.metrics_frame, "Total Runtime", "0.0s", "#06b6d4"
    )

    self.card_completed.grid(row=0, column=0, sticky="ew", padx=5)
    self.card_active.grid(row=0, column=1, sticky="ew", padx=5)
    self.card_status.grid(row=0, column=2, sticky="ew", padx=5)
    self.card_total_time.grid(row=0, column=3, sticky="ew", padx=5)

    # 3. Main Split Content View (Row 2 - Terminal Left, Analytics Right)
    self.main_split = ctk.CTkFrame(self, fg_color="transparent")
    self.main_split.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 10))
    self.main_split.grid_columnconfigure(0, weight=3)
    self.main_split.grid_columnconfigure(1, weight=2)
    self.main_split.grid_rowconfigure(0, weight=1)

    # Left: Terminal & Progress View
    self.terminal_frame = ctk.CTkFrame(self.main_split, fg_color="#161b22")
    self.terminal_frame.grid(
        row=0, column=0, sticky="nsew", padx=(0, 5), pady=0
    )

    self.progress_bar = ctk.CTkProgressBar(
        self.terminal_frame,
        progress_color="#10b981",
        fg_color="#1f2937",
        height=10,
    )
    self.progress_bar.set(0)
    self.progress_bar.pack(fill="x", padx=15, pady=(15, 10))

    self.console = ctk.CTkTextbox(
        self.terminal_frame,
        font=ctk.CTkFont(family="Consolas", size=12),
        fg_color="#0d1117",
        text_color="#38bdf8",
    )
    self.console.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # Right: Embedded Matplotlib Performance Chart (Functionality 2)
    self.chart_frame = ctk.CTkFrame(self.main_split, fg_color="#161b22")
    self.chart_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)

    self.lbl_chart = ctk.CTkLabel(
        self.chart_frame,
        text="📊 Live Task Performance",
        font=ctk.CTkFont(size=14, weight="bold"),
    )
    self.lbl_chart.pack(anchor="w", padx=15, pady=(10, 5))

    self.fig, self.ax = plt.subplots(figsize=(4, 3), dpi=100)
    self.fig.patch.set_facecolor("#161b22")
    self.ax.set_facecolor("#0d1117")
    self.ax.tick_params(colors="#94a3b8", labelsize=8)
    self.ax.spines["bottom"].set_color("#374151")
    self.ax.spines["left"].set_color("#374151")
    self.ax.spines["top"].set_visible(False)
    self.ax.spines["right"].set_visible(False)

    self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
    self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    self.update_chart()

    # 4. Control Action Bar (Row 3)
    self.controls = ctk.CTkFrame(self, fg_color="transparent")
    self.controls.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))

    # Func 1: Quick Task
    self.btn_run_single = ctk.CTkButton(
        self.controls,
        text="▶ Run Quick Task",
        command=lambda: self.start_async_job("Quick Data Sync", steps=50),
        fg_color="#10b981",
        hover_color="#059669",
        text_color="#000",
        font=ctk.CTkFont(weight="bold"),
    )
    self.btn_run_single.pack(side="left", padx=4)

    # Func 1: Batch Engine
    self.btn_run_batch = ctk.CTkButton(
        self.controls,
        text="⚡ Heavy Batch Engine",
        command=lambda: self.start_async_job("Heavy Batch Processing", steps=100),
        fg_color="#06b6d4",
        hover_color="#0891b2",
        text_color="#000",
        font=ctk.CTkFont(weight="bold"),
    )
    self.btn_run_batch.pack(side="left", padx=4)

    # Func 3: Import & Parse Log File
    self.btn_import = ctk.CTkButton(
        self.controls,
        text="📁 Load Log File",
        command=self.import_and_process_log,
        fg_color="#3b82f6",
        hover_color="#2563eb",
    )
    self.btn_import.pack(side="left", padx=4)

    # Func 6: System Clean Utility
    self.btn_clean = ctk.CTkButton(
        self.controls,
        text="🧹 Clear Logs",
        command=self.clear_system_logs,
        fg_color="#ef4444",
        hover_color="#dc2626",
    )
    self.btn_clean.pack(side="left", padx=4)

    # Func 5: Multi-Format Export
    self.btn_export = ctk.CTkButton(
        self.controls,
        text="📊 Export Reports",
        command=self.export_audit,
        fg_color="#1f2937",
        hover_color="#374151",
    )
    self.btn_export.pack(side="right", padx=4)

    self.raw_logs = []
    self.log_message(
        "SYSTEM READY. Select an action to execute background tasks..."
    )

  def create_card(self, parent, title, value, color):
    frame = ctk.CTkFrame(
        parent, fg_color="#161b22", border_color=color, border_width=1
    )
    lbl_title = ctk.CTkLabel(
        frame, text=title, font=ctk.CTkFont(size=12), text_color="#94a3b8"
    )
    lbl_title.pack(anchor="w", padx=15, pady=(10, 0))

    lbl_val = ctk.CTkLabel(
        frame,
        text=value,
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=color,
    )
    lbl_val.pack(anchor="w", padx=15, pady=(0, 10))

    frame.lbl_val = lbl_val
    return frame

  def log_message(self, message):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    formatted = f"[{ts}] {message}"
    self.raw_logs.append(formatted)
    self.log_queue.put(formatted)

  def process_queue(self):
    """Processes thread logs safely in the main thread."""
    while not self.log_queue.empty():
      msg = self.log_queue.get()
      self.console.insert("end", f"{msg}\n")
      self.console.see("end")
    self.after(100, self.process_queue)

  # FUNCTIONALITY 1: Asynchronous Task Execution
  def start_async_job(self, task_name, steps):
    self.active_threads += 1
    self.card_active.lbl_val.configure(text=str(self.active_threads))
    self.card_status.lbl_val.configure(text="Processing", text_color="#f59e0b")

    thread = threading.Thread(
        target=self.worker_thread, args=(task_name, steps), daemon=True
    )
    thread.start()

  def worker_thread(self, task_name, steps):
    start_time = time.time()
    self.log_message(
        f"START: Initiating background thread for '{task_name}'..."
    )

    for i in range(1, steps + 1):
      time.sleep(0.04)
      progress = i / steps
      self.progress_bar.set(progress)

      if i % (steps // 5) == 0:
        self.log_message(
            f"PROGRESS: '{task_name}' at {int(progress * 100)}%..."
        )

    duration = round(time.time() - start_time, 2)
    self.log_message(
        f"SUCCESS: '{task_name}' completed in {duration} seconds."
    )

    record = {
        "task_name": task_name,
        "status": "Success",
        "duration_sec": duration,
        "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    self.completed_tasks.append(record)

    self.active_threads -= 1
    self.card_active.lbl_val.configure(text=str(self.active_threads))
    self.card_completed.lbl_val.configure(text=str(len(self.completed_tasks)))

    total_runtime = sum(t["duration_sec"] for t in self.completed_tasks)
    self.card_total_time.lbl_val.configure(text=f"{total_runtime:.1f}s")

    if self.active_threads == 0:
      self.card_status.lbl_val.configure(text="Idle", text_color="#10b981")

    # Update Chart Visualization
    self.update_chart()

  # FUNCTIONALITY 2: Live Performance Chart Visualization
  def update_chart(self):
    self.ax.clear()
    if self.completed_tasks:
      df = pd.DataFrame(self.completed_tasks)
      self.ax.bar(
          range(len(df)),
          df["duration_sec"],
          color="#10b981",
          edgecolor="#06b6d4",
      )
      self.ax.set_title("Runtime per Task (s)", color="#f8fafc", fontsize=9)
    else:
      self.ax.text(
          0.5,
          0.5,
          "No Task Data",
          color="#94a3b8",
          ha="center",
          va="center",
          transform=self.ax.transAxes,
      )

    self.canvas.draw()

  # FUNCTIONALITY 3: Import & Parse File Data
  def import_and_process_log(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Log & Text Files", "*.log *.txt *.csv")]
    )
    if not file_path:
      return

    self.log_message(f"FILE READ: Parsing '{file_path}'...")
    try:
      with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[:10]  # Read first 10 preview lines
        for line in lines:
          self.log_message(f"  └─ {line.strip()}")
      self.log_message(
          f"SUCCESS: Extracted {len(lines)} entries from file payload."
      )
    except Exception as e:
      self.log_message(f"ERROR: Failed to parse file: {e}")

  # FUNCTIONALITY 4: Live Console Search & Filtering
  def filter_console_logs(self, event):
    query = self.search_entry.get().strip().lower()
    self.console.delete("1.0", "end")

    if not query:
      for log in self.raw_logs:
        self.console.insert("end", f"{log}\n")
    else:
      for log in self.raw_logs:
        if query in log.lower():
          self.console.insert("end", f"{log}\n")

  # FUNCTIONALITY 5: Multi-Format Audit Export Engine
  def export_audit(self):
    if not self.completed_tasks:
      messagebox.showwarning(
          "Warning", "No completed task history available to export."
      )
      return

    # 1. SQLite Database Export
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for task in self.completed_tasks:
      cursor.execute(
          """
                INSERT INTO task_audit (task_name, status, duration_sec, completed_at)
                VALUES (?, ?, ?, ?)
            """,
          (
              task["task_name"],
              task["status"],
              task["duration_sec"],
              task["completed_at"],
          ),
      )
    conn.commit()
    conn.close()

    # 2. Excel Export
    df = pd.DataFrame(self.completed_tasks)
    df.to_excel(EXCEL_FILE, index=False)

    # 3. CSV Export
    df.to_csv(CSV_FILE, index=False)

    self.log_message(
        f"EXPORTS SUCCESSFUL: Reports generated in SQLite, Excel, and CSV."
    )
    messagebox.showinfo(
        "Export Successful",
        f"Reports generated:\n• {EXCEL_FILE}\n• {CSV_FILE}\n• {DB_FILE}",
    )

  # FUNCTIONALITY 6: System Memory & Log Cleaner
  def clear_system_logs(self):
    self.console.delete("1.0", "end")
    self.raw_logs.clear()
    self.progress_bar.set(0)
    self.log_message("CLEANUP: Console output and memory buffers cleared.")


if __name__ == "__main__":
  app = TaskPulsePro()
  app.mainloop()