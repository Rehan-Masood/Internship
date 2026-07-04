import tkinter as tk

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rehan's BMI Calculator")
        self.root.geometry("420x520")
        self.root.minsize(380, 460)
        self.root.resizable(True, True)   # allow resizing + maximize

        # ---------- Premium color palette ----------
        self.COLOR_BG = "#14152B"
        self.COLOR_CARD = "#1F2142"
        self.COLOR_ACCENT = "#7C6FE8"
        self.COLOR_ACCENT_HOVER = "#6355D6"
        self.COLOR_GOLD = "#D4AF37"
        self.COLOR_TEXT = "#F5F3FF"
        self.COLOR_MUTED = "#9B9BB8"

        self.root.configure(bg=self.COLOR_BG)

        # ---------- Root grid ----------
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Outer frame fills and expands with the window.
        # Row 0 and row 6 are "spacer" rows that absorb extra space,
        # which keeps all the real content vertically centered when maximized.
        outer = tk.Frame(self.root, bg=self.COLOR_BG)
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(0, weight=1)   # top spacer
        outer.grid_rowconfigure(6, weight=1)   # bottom spacer

        # ---------- Title (row 1) ----------
        tk.Label(outer, text="BMI Calculator", font=("Helvetica", 22, "bold"),
                 bg=self.COLOR_BG, fg=self.COLOR_TEXT).grid(row=1, column=0, pady=(10, 5))

        tk.Label(outer, text="Check your Body Mass Index", font=("Arial", 11),
                 bg=self.COLOR_BG, fg=self.COLOR_MUTED).grid(row=2, column=0, pady=(0, 20))

        # ---------- Input card (row 3), width scales with window, capped ----------
        card_wrapper = tk.Frame(outer, bg=self.COLOR_BG)
        card_wrapper.grid(row=3, column=0, sticky="ew", padx=40)
        card_wrapper.grid_columnconfigure(0, weight=1)

        card = tk.Frame(card_wrapper, bg=self.COLOR_CARD, padx=30, pady=30)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        tk.Label(card, text="Weight (kg)", font=("Arial", 11),
                 bg=self.COLOR_CARD, fg=self.COLOR_MUTED, anchor="w").grid(row=0, column=0, sticky="ew")
        self.weight_entry = tk.Entry(card, font=("Arial", 13), bg="#2A2D52", fg=self.COLOR_TEXT,
                                      insertbackground=self.COLOR_TEXT, relief="flat")
        self.weight_entry.grid(row=1, column=0, sticky="ew", ipady=8, pady=(5, 18))

        tk.Label(card, text="Height (cm)", font=("Arial", 11),
                 bg=self.COLOR_CARD, fg=self.COLOR_MUTED, anchor="w").grid(row=2, column=0, sticky="ew")
        self.height_entry = tk.Entry(card, font=("Arial", 13), bg="#2A2D52", fg=self.COLOR_TEXT,
                                      insertbackground=self.COLOR_TEXT, relief="flat")
        self.height_entry.grid(row=3, column=0, sticky="ew", ipady=8, pady=(5, 5))

        # ---------- Calculate button (row 4) ----------
        self.calc_button = tk.Button(outer, text="Calculate BMI", command=self.calculate_bmi,
                                      bg=self.COLOR_ACCENT, fg="white", font=("Arial", 12, "bold"),
                                      relief="flat", padx=20, pady=12, bd=0, cursor="hand2")
        self.calc_button.grid(row=4, column=0, pady=25)
        self.calc_button.bind("<Enter>", lambda e: self.calc_button.config(bg=self.COLOR_ACCENT_HOVER))
        self.calc_button.bind("<Leave>", lambda e: self.calc_button.config(bg=self.COLOR_ACCENT))

        # ---------- Result display (row 5) ----------
        result_wrapper = tk.Frame(outer, bg=self.COLOR_BG)
        result_wrapper.grid(row=5, column=0, pady=(0, 20))

        self.result_label = tk.Label(result_wrapper, text="", font=("Helvetica", 26, "bold"),
                                      bg=self.COLOR_BG, fg=self.COLOR_GOLD)
        self.result_label.pack()

        self.category_label = tk.Label(result_wrapper, text="", font=("Arial", 12),
                                        bg=self.COLOR_BG, fg=self.COLOR_TEXT)
        self.category_label.pack(pady=(5, 0))

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height_cm = float(self.height_entry.get())

            if weight <= 0 or height_cm <= 0:
                self.result_label.config(text="⚠", fg="#E74C3C")
                self.category_label.config(text="Enter values greater than 0")
                return

            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)

            if bmi < 18.5:
                category = "Underweight"
                color = "#3498DB"
            elif bmi < 25:
                category = "Normal weight"
                color = "#2ECC71"
            elif bmi < 30:
                category = "Overweight"
                color = "#F39C12"
            else:
                category = "Obese"
                color = "#E74C3C"

            self.result_label.config(text=f"{bmi:.1f}", fg=self.COLOR_GOLD)
            self.category_label.config(text=category, fg=color)

        except ValueError:
            self.result_label.config(text="⚠", fg="#E74C3C")
            self.category_label.config(text="Please enter valid numbers")


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
