import datetime
import os
import re
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd

# Set Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DB_FILE = "log_audit.db"
EXCEL_FILE = "daily_log_summary.xlsx"


class LogSentinelApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("LogSentinel Pro - Enterprise Log Auditor")
    self.geometry("1000x680")
    self.minsize(800, 550)  # Allows smooth resizing & maximizing

    # Make the root window grid scalable
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)  # Console row expands vertically

    self.parsed_records = []

    self.init_db()
    self.build_ui()

  def init_db(self):
    """Initializes SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS audited_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_level TEXT,
                ip_address TEXT,
                endpoint TEXT,
                status_code INTEGER,
                latency_ms INTEGER,
                audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

  def build_ui(self):
    # 1. Top Header Frame (Row 0)
    self.header_frame = ctk.CTkFrame(self, fg_color="#0d1117", height=70)
    self.header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

    self.title_label = ctk.CTkLabel(
        self.header_frame,
        text="🛡️ LOGSENTINEL PRO",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#10b981",
    )
    self.title_label.pack(side="left", padx=20, pady=15)

    self.subtitle_label = ctk.CTkLabel(
        self.header_frame,
        text="Automated Log Auditing & Anomaly Pipeline",
        font=ctk.CTkFont(size=12),
        text_color="#94a3b8",
    )
    self.subtitle_label.pack(side="left", padx=0, pady=15)

    # 2. Metrics Cards Frame (Row 1) - Equal Scaling Columns
    self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
    self.metrics_frame.grid(
        row=1, column=0, sticky="ew", padx=15, pady=(0, 10)
    )

    for i in range(4):
      self.metrics_frame.grid_columnconfigure(i, weight=1)

    self.card_total = self.create_card(
        self.metrics_frame, "Total Logs", "0", "#3b82f6"
    )
    self.card_errors = self.create_card(
        self.metrics_frame, "5xx Errors", "0", "#ef4444"
    )
    self.card_auth = self.create_card(
        self.metrics_frame, "4xx Violations", "0", "#f59e0b"
    )
    self.card_latency = self.create_card(
        self.metrics_frame, "Avg Latency", "0 ms", "#10b981"
    )

    self.card_total.grid(row=0, column=0, sticky="ew", padx=5)
    self.card_errors.grid(row=0, column=1, sticky="ew", padx=5)
    self.card_auth.grid(row=0, column=2, sticky="ew", padx=5)
    self.card_latency.grid(row=0, column=3, sticky="ew", padx=5)

    # 3. Console / Terminal View (Row 2 - Expands on Maximize)
    self.console_frame = ctk.CTkFrame(self, fg_color="#161b22")
    self.console_frame.grid(
        row=2, column=0, sticky="nsew", padx=15, pady=(0, 10)
    )

    self.console_textbox = ctk.CTkTextbox(
        self.console_frame,
        font=ctk.CTkFont(family="Consolas", size=13),
        fg_color="#0d1117",
        text_color="#38bdf8",
    )
    self.console_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    # 4. Action Control Bar (Row 3)
    self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
    self.controls_frame.grid(
        row=3, column=0, sticky="ew", padx=15, pady=(0, 15)
    )

    self.btn_gen_mock = ctk.CTkButton(
        self.controls_frame,
        text="⚡ Generate Mock Logs",
        command=self.generate_mock_log,
        fg_color="#1f2937",
        hover_color="#374151",
    )
    self.btn_gen_mock.pack(side="left", padx=5)

    self.btn_browse = ctk.CTkButton(
        self.controls_frame,
        text="📁 Load & Audit Log File",
        command=self.browse_and_audit,
        fg_color="#10b981",
        hover_color="#059669",
        text_color="#000",
        font=ctk.CTkFont(weight="bold"),
    )
    self.btn_browse.pack(side="left", padx=5)

    self.btn_export = ctk.CTkButton(
        self.controls_frame,
        text="📊 Export Excel & DB",
        command=self.export_reports,
        fg_color="#06b6d4",
        hover_color="#0891b2",
        text_color="#000",
        font=ctk.CTkFont(weight="bold"),
    )
    self.btn_export.pack(side="right", padx=5)

    self.log_message("SYSTEM INITIALIZED. Ready to parse logs...")

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
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=color,
    )
    lbl_val.pack(anchor="w", padx=15, pady=(0, 10))

    frame.lbl_val = lbl_val
    return frame

  def log_message(self, message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    self.console_textbox.insert("end", f"[{timestamp}] {message}\n")
    self.console_textbox.see("end")

  def generate_mock_log(self):
    mock_file = "server_app.log"
    log_entries = [
        (
            "2026-08-09 10:15:20 | INFO | 192.168.1.10 | GET /api/v1/users | 200"
            " | 45ms"
        ),
        (
            "2026-08-09 10:15:22 | ERROR | 192.168.1.12 | POST /api/v1/checkout"
            " | 500 | 1200ms"
        ),
        (
            "2026-08-09 10:15:25 | WARNING | 10.0.0.5 | GET /admin/login | 403 |"
            " 12ms"
        ),
        (
            "2026-08-09 10:15:28 | WARNING | 10.0.0.5 | GET /admin/login | 403 |"
            " 10ms"
        ),
        (
            "2026-08-09 10:15:30 | ERROR | 192.168.1.15 | GET /api/v1/products |"
            " 500 | 850ms"
        ),
        "2026-08-09 10:15:35 | INFO | 192.168.1.18 | GET /menu | 200 | 30ms",
        (
            "2026-08-09 10:15:40 | CRITICAL | 10.0.0.5 | POST /admin/config |"
            " 401 | 5ms"
        ),
    ]
    with open(mock_file, "w") as f:
      f.write("\n".join(log_entries))
    self.log_message(f"SUCCESS: Created mock log file '{mock_file}'.")

  def browse_and_audit(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt")]
    )
    if not file_path:
      return

    self.log_message(f"Reading log file: {file_path}")

    log_pattern = re.compile(
        r"(?P<timestamp>[\d\-:\s]+) \| (?P<level>\w+) \| (?P<ip>[\d\.]+) \|"
        r" (?P<method_endpoint>\w+ \S+) \| (?P<status>\d+) \|"
        r" (?P<latency>\d+)ms"
    )

    self.parsed_records = []
    with open(file_path, "r") as file:
      for line in file:
        match = log_pattern.search(line.strip())
        if match:
          self.parsed_records.append({
              "timestamp": match.group("timestamp"),
              "log_level": match.group("level"),
              "ip_address": match.group("ip"),
              "endpoint": match.group("method_endpoint"),
              "status_code": int(match.group("status")),
              "latency_ms": int(match.group("latency")),
          })
          self.log_message(
              f"PARSED: {match.group('method_endpoint')} ->"
              f" {match.group('status')}"
          )

    # Update GUI Metric Cards
    df = pd.DataFrame(self.parsed_records)
    if not df.empty:
      err_count = len(df[df["status_code"] >= 500])
      auth_count = len(df[df["status_code"].isin([401, 403])])
      avg_latency = df["latency_ms"].mean()

      self.card_total.lbl_val.configure(text=str(len(df)))
      self.card_errors.lbl_val.configure(text=str(err_count))
      self.card_auth.lbl_val.configure(text=str(auth_count))
      self.card_latency.lbl_val.configure(text=f"{avg_latency:.1f} ms")

      self.log_message(
          f"AUDIT COMPLETE: {len(df)} entries parsed. {err_count} server"
          " errors detected."
      )

  def export_reports(self):
    if not self.parsed_records:
      messagebox.showwarning(
          "Warning", "No parsed logs available to export. Run an audit first."
      )
      return

    # 1. Save to SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for r in self.parsed_records:
      cursor.execute(
          """
                INSERT INTO audited_logs (timestamp, log_level, ip_address, endpoint, status_code, latency_ms)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
          (
              r["timestamp"],
              r["log_level"],
              r["ip_address"],
              r["endpoint"],
              r["status_code"],
              r["latency_ms"],
          ),
      )
    conn.commit()
    conn.close()

    # 2. Save to Excel
    df = pd.DataFrame(self.parsed_records)
    df.to_excel(EXCEL_FILE, index=False)

    self.log_message(
        f"EXPORTS SUCCESSFUL: Saved to '{DB_FILE}' and '{EXCEL_FILE}'."
    )
    messagebox.showinfo(
        "Export Successful",
        f"Reports generated:\n• {EXCEL_FILE}\n• {DB_FILE}",
    )


if __name__ == "__main__":
  app = LogSentinelApp()
  app.mainloop()