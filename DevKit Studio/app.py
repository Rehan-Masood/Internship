import base64
import hashlib
import json
import tkinter as tk
from tkinter import messagebox, ttk

# --- MODERN DARK THEME COLOR PALETTE ---
BG_DARK = "#121218"
CARD_BG = "#1e1e28"
ACCENT_CYAN = "#00f2fe"
ACCENT_BLUE = "#3a86ff"
TEXT_LIGHT = "#e0e0e0"
TEXT_MUTED = "#a0a0b0"
CONSOLE_BG = "#0a0a0f"


class DevKitApp(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("DevKit Studio — Essential Developer Utilities")
    self.geometry("900x650")
    self.minsize(800, 550)
    self.configure(bg=BG_DARK)

    self._apply_custom_styles()
    self._build_ui()

  def _apply_custom_styles(self):
    style = ttk.Style(self)
    style.theme_use("clam")

    # Configure Tabs / Notebook
    style.configure("TNotebook", background=BG_DARK, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=CARD_BG,
        foreground=TEXT_LIGHT,
        padding=[14, 8],
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", ACCENT_BLUE)],
        foreground=[("selected", "#ffffff")],
    )

    # Buttons
    style.configure(
        "Accent.TButton",
        font=("Segoe UI", 9, "bold"),
        background=ACCENT_CYAN,
        foreground="#000000",
        bordercolor=ACCENT_CYAN,
        borderwidth=1,
    )
    style.map("Accent.TButton", background=[("active", "#00d8e6")])

    style.configure(
        "Dark.TButton",
        font=("Segoe UI", 9, "bold"),
        background="#2a2a3a",
        foreground=TEXT_LIGHT,
        bordercolor="#3a3a4c",
        borderwidth=1,
    )
    style.map("Dark.TButton", background=[("active", "#3a3a4c")])

  def _build_ui(self):
    # Header Banner
    header = tk.Frame(self, bg=CARD_BG, height=55, padx=20)
    header.pack(fill=tk.X, side=tk.TOP)

    title_label = tk.Label(
        header,
        text="🛠️ DevKit Studio",
        font=("Segoe UI", 15, "bold"),
        bg=CARD_BG,
        fg=ACCENT_CYAN,
    )
    title_label.pack(side=tk.LEFT, pady=10)

    subtitle_label = tk.Label(
        header,
        text="Essential Swiss Army Knife for Software Engineers",
        font=("Segoe UI", 9, "italic"),
        bg=CARD_BG,
        fg=TEXT_MUTED,
    )
    subtitle_label.pack(side=tk.LEFT, padx=12, pady=12)

    # Notebook Tabs
    notebook = ttk.Notebook(self)
    notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    # Tab 1: JSON Formatter
    tab_json = tk.Frame(notebook, bg=BG_DARK)
    notebook.add(tab_json, text=" 📝 JSON Formatter ")

    # Tab 2: Base64 Encoder / Decoder
    tab_base64 = tk.Frame(notebook, bg=BG_DARK)
    notebook.add(tab_base64, text=" 🔐 Base64 Tool ")

    # Tab 3: Hash Generator
    tab_hash = tk.Frame(notebook, bg=BG_DARK)
    notebook.add(tab_hash, text=" ⚡ Hash Generator ")

    # Tab 4: Text Case Converter
    tab_text = tk.Frame(notebook, bg=BG_DARK)
    notebook.add(tab_text, text=" 🔤 Text Case & Stats ")

    self._build_json_tab(tab_json)
    self._build_base64_tab(tab_base64)
    self._build_hash_tab(tab_hash)
    self._build_text_tab(tab_text)

    # Status Bar
    self.status_bar = tk.Label(
        self,
        text="Ready | DevKit Studio Active",
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W,
        bg=CARD_BG,
        fg=TEXT_MUTED,
        font=("Consolas", 9),
        padx=10,
        pady=4,
    )
    self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

  # --- TAB 1: JSON FORMATTER ---
  def _build_json_tab(self, parent):
    frame = tk.Frame(parent, bg=CARD_BG, padx=15, pady=15)
    frame.pack(fill=tk.BOTH, expand=True, pady=10)

    tk.Label(
        frame,
        text="Input Raw JSON:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W)

    self.json_input = tk.Text(
        frame,
        height=8,
        bg=CONSOLE_BG,
        fg=ACCENT_CYAN,
        insertbackground="#ffffff",
        font=("Consolas", 10),
        bd=1,
        relief=tk.SOLID,
        padx=8,
        pady=8,
    )
    self.json_input.insert(
        tk.END, '{"name":"John Doe","role":"Developer","skills":["Python","SQL"]}'
    )
    self.json_input.pack(fill=tk.BOTH, expand=True, pady=(2, 8))

    btn_bar = tk.Frame(frame, bg=CARD_BG)
    btn_bar.pack(fill=tk.X, pady=5)

    ttk.Button(
        btn_bar,
        text="✨ Format & Beautify JSON",
        style="Accent.TButton",
        command=self._format_json,
    ).pack(side=tk.LEFT, padx=4)
    ttk.Button(
        btn_bar,
        text="⚡ Minify JSON",
        style="Dark.TButton",
        command=self._minify_json,
    ).pack(side=tk.LEFT, padx=4)

    tk.Label(
        frame,
        text="Formatted Output:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W, pady=(8, 2))

    self.json_output = tk.Text(
        frame,
        height=10,
        bg=CONSOLE_BG,
        fg="#00ff66",
        insertbackground="#ffffff",
        font=("Consolas", 10),
        bd=1,
        relief=tk.SOLID,
        padx=8,
        pady=8,
    )
    self.json_output.pack(fill=tk.BOTH, expand=True)

  def _format_json(self):
    raw_str = self.json_input.get("1.0", tk.END).strip()
    try:
      parsed = json.loads(raw_str)
      formatted = json.dumps(parsed, indent=4)
      self.json_output.delete("1.0", tk.END)
      self.json_output.insert(tk.END, formatted)
      self.status_bar.config(text="JSON successfully formatted and validated!")
    except Exception as e:
      messagebox.showerror("Invalid JSON", f"JSON Syntax Error:\n{e}")

  def _minify_json(self):
    raw_str = self.json_input.get("1.0", tk.END).strip()
    try:
      parsed = json.loads(raw_str)
      minified = json.dumps(parsed, separators=(",", ":"))
      self.json_output.delete("1.0", tk.END)
      self.json_output.insert(tk.END, minified)
      self.status_bar.config(text="JSON successfully minified!")
    except Exception as e:
      messagebox.showerror("Invalid JSON", f"JSON Syntax Error:\n{e}")

  # --- TAB 2: BASE64 TOOL ---
  def _build_base64_tab(self, parent):
    frame = tk.Frame(parent, bg=CARD_BG, padx=15, pady=15)
    frame.pack(fill=tk.BOTH, expand=True, pady=10)

    tk.Label(
        frame,
        text="Input String:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W)

    self.b64_input = tk.Text(
        frame,
        height=7,
        bg=CONSOLE_BG,
        fg=TEXT_LIGHT,
        insertbackground="#ffffff",
        font=("Consolas", 10),
        bd=1,
        relief=tk.SOLID,
        padx=8,
        pady=8,
    )
    self.b64_input.insert(tk.END, "Hello World! Welcome to DevKit Studio.")
    self.b64_input.pack(fill=tk.BOTH, expand=True, pady=(2, 8))

    btn_bar = tk.Frame(frame, bg=CARD_BG)
    btn_bar.pack(fill=tk.X, pady=5)

    ttk.Button(
        btn_bar,
        text="🔒 Encode to Base64",
        style="Accent.TButton",
        command=self._encode_b64,
    ).pack(side=tk.LEFT, padx=4)
    ttk.Button(
        btn_bar,
        text="🔓 Decode from Base64",
        style="Dark.TButton",
        command=self._decode_b64,
    ).pack(side=tk.LEFT, padx=4)

    tk.Label(
        frame,
        text="Result:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W, pady=(8, 2))

    self.b64_output = tk.Text(
        frame,
        height=7,
        bg=CONSOLE_BG,
        fg=ACCENT_CYAN,
        insertbackground="#ffffff",
        font=("Consolas", 10),
        bd=1,
        relief=tk.SOLID,
        padx=8,
        pady=8,
    )
    self.b64_output.pack(fill=tk.BOTH, expand=True)

  def _encode_b64(self):
    text = self.b64_input.get("1.0", tk.END).strip()
    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    self.b64_output.delete("1.0", tk.END)
    self.b64_output.insert(tk.END, encoded)
    self.status_bar.config(text="Base64 Encoding Completed")

  def _decode_b64(self):
    text = self.b64_input.get("1.0", tk.END).strip()
    try:
      decoded = base64.b64decode(text.encode("utf-8")).decode("utf-8")
      self.b64_output.delete("1.0", tk.END)
      self.b64_output.insert(tk.END, decoded)
      self.status_bar.config(text="Base64 Decoding Completed")
    except Exception:
      messagebox.showerror(
          "Decode Error", "Invalid Base64 encoded string provided."
      )

  # --- TAB 3: HASH GENERATOR ---
  def _build_hash_tab(self, parent):
    frame = tk.Frame(parent, bg=CARD_BG, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True, pady=10)

    tk.Label(
        frame,
        text="Input Plaintext:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W)

    self.hash_input = tk.Entry(
        frame,
        font=("Consolas", 11),
        bg=CONSOLE_BG,
        fg=TEXT_LIGHT,
        bd=1,
        relief=tk.SOLID,
    )
    self.hash_input.insert(0, "DevKitStudio2026")
    self.hash_input.pack(fill=tk.X, pady=(4, 15), ipady=6)

    ttk.Button(
        frame,
        text="⚡ Compute Hashes",
        style="Accent.TButton",
        command=self._generate_hashes,
    ).pack(anchor=tk.W, pady=(0, 15))

    tk.Label(
        frame,
        text="MD5 Hash:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W)
    self.md5_output = tk.Entry(
        frame,
        font=("Consolas", 10),
        bg=CONSOLE_BG,
        fg="#ff007f",
        bd=1,
        relief=tk.SOLID,
    )
    self.md5_output.pack(fill=tk.X, pady=(2, 12), ipady=5)

    tk.Label(
        frame,
        text="SHA-256 Hash:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W)
    self.sha256_output = tk.Entry(
        frame,
        font=("Consolas", 10),
        bg=CONSOLE_BG,
        fg="#00ff66",
        bd=1,
        relief=tk.SOLID,
    )
    self.sha256_output.pack(fill=tk.X, pady=(2, 10), ipady=5)

  def _generate_hashes(self):
    val = self.hash_input.get().encode("utf-8")
    md5_str = hashlib.md5(val).hexdigest()
    sha256_str = hashlib.sha256(val).hexdigest()

    self.md5_output.delete(0, tk.END)
    self.md5_output.insert(0, md5_str)

    self.sha256_output.delete(0, tk.END)
    self.sha256_output.insert(0, sha256_str)

    self.status_bar.config(text="Cryptographic Hashes Generated!")

  # --- TAB 4: TEXT CASE CONVERTER ---
  def _build_text_tab(self, parent):
    frame = tk.Frame(parent, bg=CARD_BG, padx=15, pady=15)
    frame.pack(fill=tk.BOTH, expand=True, pady=10)

    tk.Label(
        frame,
        text="Text Input:",
        bg=CARD_BG,
        fg=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor=tk.W)

    self.text_editor = tk.Text(
        frame,
        height=10,
        bg=CONSOLE_BG,
        fg=TEXT_LIGHT,
        insertbackground="#ffffff",
        font=("Consolas", 10),
        bd=1,
        relief=tk.SOLID,
        padx=8,
        pady=8,
    )
    self.text_editor.pack(fill=tk.BOTH, expand=True, pady=(2, 10))

    btn_bar = tk.Frame(frame, bg=CARD_BG)
    btn_bar.pack(fill=tk.X, pady=5)

    ttk.Button(
        btn_bar,
        text="UPPERCASE",
        style="Dark.TButton",
        command=lambda: self._convert_case("upper"),
    ).pack(side=tk.LEFT, padx=3)
    ttk.Button(
        btn_bar,
        text="lowercase",
        style="Dark.TButton",
        command=lambda: self._convert_case("lower"),
    ).pack(side=tk.LEFT, padx=3)
    ttk.Button(
        btn_bar,
        text="Title Case",
        style="Dark.TButton",
        command=lambda: self._convert_case("title"),
    ).pack(side=tk.LEFT, padx=3)

    self.stats_label = tk.Label(
        frame,
        text="Characters: 0 | Words: 0 | Lines: 0",
        bg=CARD_BG,
        fg=ACCENT_CYAN,
        font=("Segoe UI", 10, "bold"),
    )
    self.stats_label.pack(anchor=tk.E, pady=5)

    self.text_editor.bind("<KeyRelease>", self._update_text_stats)

  def _convert_case(self, case_type):
    content = self.text_editor.get("1.0", tk.END)
    if case_type == "upper":
      new_content = content.upper()
    elif case_type == "lower":
      new_content = content.lower()
    elif case_type == "title":
      new_content = content.title()

    self.text_editor.delete("1.0", tk.END)
    self.text_editor.insert(tk.END, new_content)
    self._update_text_stats()

  def _update_text_stats(self, event=None):
    content = self.text_editor.get("1.0", tk.END)
    chars = len(content) - 1
    words = len(content.split())
    lines = int(self.text_editor.index("end-1c").split(".")[0])
    self.stats_label.config(
        text=f"Characters: {chars} | Words: {words} | Lines: {lines}"
    )


if __name__ == "__main__":
  app = DevKitApp()
  app.mainloop()