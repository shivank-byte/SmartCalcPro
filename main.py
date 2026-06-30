"""
main.py
-------
SmartCalc Pro -- a desktop calculator with basic, scientific, statistics,
finance/economics, and utility tools, built with Tkinter.

Run:
    python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

import calculator_engine as calc
import history
from themes import THEMES, DEFAULT_THEME


class SmartCalcPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartCalc Pro")
        self.geometry("760x620")
        self.minsize(680, 560)

        self.theme_name = DEFAULT_THEME
        self.theme = THEMES[self.theme_name]

        self._build_layout()
        self._apply_theme()

    # ----------------------------------------------------------------
    # Layout
    # ----------------------------------------------------------------

    def _build_layout(self):
        # Top bar: title + theme toggle
        self.top_bar = tk.Frame(self)
        self.top_bar.pack(fill="x", padx=10, pady=(10, 0))

        self.title_label = tk.Label(self.top_bar, text="SmartCalc Pro", font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side="left")

        self.theme_btn = tk.Button(self.top_bar, text="Toggle Theme", command=self.toggle_theme, relief="flat")
        self.theme_btn.pack(side="right")

        self.history_btn = tk.Button(self.top_bar, text="History", command=self.show_history, relief="flat")
        self.history_btn.pack(side="right", padx=8)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabs = {}
        self._build_basic_tab()
        self._build_scientific_tab()
        self._build_stats_tab()
        self._build_finance_tab()
        self._build_utility_tab()

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_bar.pack(fill="x", side="bottom")

        # Keyboard shortcuts
        self.bind("<Control-h>", lambda e: self.show_history())
        self.bind("<Control-l>", lambda e: self.clear_status())

    def _add_tab(self, name: str) -> tk.Frame:
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        self.tabs[name] = frame
        return frame

    # ----------------------------------------------------------------
    # Basic operations tab
    # ----------------------------------------------------------------

    def _build_basic_tab(self):
        frame = self._add_tab("Basic")

        row1 = tk.Frame(frame)
        row1.pack(pady=20)
        tk.Label(row1, text="A:").grid(row=0, column=0, padx=5)
        a_entry = tk.Entry(row1, width=12)
        a_entry.grid(row=0, column=1, padx=5)
        tk.Label(row1, text="B:").grid(row=0, column=2, padx=5)
        b_entry = tk.Entry(row1, width=12)
        b_entry.grid(row=0, column=3, padx=5)

        result_var = tk.StringVar(value="Result will appear here")
        result_label = tk.Label(frame, textvariable=result_var, font=("Segoe UI", 14, "bold"))
        result_label.pack(pady=10)

        def run(op_name, op_func, needs_b=True):
            try:
                a = float(a_entry.get())
                b = float(b_entry.get()) if needs_b else None
                result = op_func(a, b) if needs_b else op_func(a)
                expr = f"{a} {op_name} {b}" if needs_b else f"{op_name}({a})"
                self._show_result(result_var, expr, result)
            except ValueError:
                self._show_error(result_var, "Enter valid numbers")
            except calc.CalculationError as e:
                self._show_error(result_var, str(e))

        ops_grid = tk.Frame(frame)
        ops_grid.pack(pady=10)

        buttons = [
            ("Add (+)", lambda: run("+", calc.add)),
            ("Subtract (-)", lambda: run("-", calc.subtract)),
            ("Multiply (×)", lambda: run("×", calc.multiply)),
            ("Divide (÷)", lambda: run("÷", calc.divide)),
            ("Modulus (%)", lambda: run("%", calc.modulus)),
            ("Power (^)", lambda: run("^", calc.power)),
            ("Square (A²)", lambda: run("square", calc.square, needs_b=False)),
            ("Cube (A³)", lambda: run("cube", calc.cube, needs_b=False)),
            ("% of B", lambda: run("% of", calc.percentage)),
        ]

        for i, (label, command) in enumerate(buttons):
            btn = tk.Button(ops_grid, text=label, width=14, command=command)
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6)

        self._register_themed(frame, result_label, ops_grid, row1)

    # ----------------------------------------------------------------
    # Scientific tab
    # ----------------------------------------------------------------

    def _build_scientific_tab(self):
        frame = self._add_tab("Scientific")

        row1 = tk.Frame(frame)
        row1.pack(pady=20)
        tk.Label(row1, text="Value:").grid(row=0, column=0, padx=5)
        entry = tk.Entry(row1, width=14)
        entry.grid(row=0, column=1, padx=5)

        result_var = tk.StringVar(value="Result will appear here")
        result_label = tk.Label(frame, textvariable=result_var, font=("Segoe UI", 14, "bold"))
        result_label.pack(pady=10)

        def run(op_name, op_func):
            try:
                a = float(entry.get())
                result = op_func(a)
                self._show_result(result_var, f"{op_name}({a})", result)
            except ValueError:
                self._show_error(result_var, "Enter a valid number")
            except calc.CalculationError as e:
                self._show_error(result_var, str(e))

        ops_grid = tk.Frame(frame)
        ops_grid.pack(pady=10)

        buttons = [
            ("√ Square Root", lambda: run("sqrt", calc.square_root)),
            ("∛ Cube Root", lambda: run("cbrt", calc.cube_root)),
            ("! Factorial", lambda: run("fact", calc.factorial)),
            ("ln (natural log)", lambda: run("ln", calc.log_natural)),
            ("log10", lambda: run("log10", calc.log_base10)),
            ("eˣ", lambda: run("exp", calc.exp)),
            ("sin (degrees)", lambda: run("sin", calc.sin_deg)),
            ("cos (degrees)", lambda: run("cos", calc.cos_deg)),
            ("tan (degrees)", lambda: run("tan", calc.tan_deg)),
        ]

        for i, (label, command) in enumerate(buttons):
            btn = tk.Button(ops_grid, text=label, width=16, command=command)
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6)

        self._register_themed(frame, result_label, ops_grid, row1)

    # ----------------------------------------------------------------
    # Statistics tab
    # ----------------------------------------------------------------

    def _build_stats_tab(self):
        frame = self._add_tab("Statistics")

        tk.Label(frame, text="Enter numbers separated by spaces or commas:").pack(pady=(20, 5))
        entry = tk.Entry(frame, width=50)
        entry.pack(pady=5)
        entry.insert(0, "e.g. 10 20 30 40 50")

        result_box = tk.Text(frame, height=10, width=60, state="disabled")
        result_box.pack(pady=15)

        def run():
            text = entry.get()
            try:
                summary = calc.stats_summary(text)
            except calc.CalculationError as e:
                self._set_text_box(result_box, f"Error: {e}")
                return
            lines = [f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}" for k, v in summary.items()]
            self._set_text_box(result_box, "\n".join(lines))
            history.add_entry(f"stats({text})", "; ".join(lines))

        btn = tk.Button(frame, text="Calculate Statistics", command=run)
        btn.pack(pady=5)

        self._register_themed(frame, result_box, btn, entry)

    # ----------------------------------------------------------------
    # Finance / Economics tab
    # ----------------------------------------------------------------

    def _build_finance_tab(self):
        frame = self._add_tab("Finance")

        sub_notebook = ttk.Notebook(frame)
        sub_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_simple_interest_panel(sub_notebook)
        self._build_compound_interest_panel(sub_notebook)
        self._build_emi_panel(sub_notebook)
        self._build_cagr_panel(sub_notebook)
        self._build_percentage_change_panel(sub_notebook)
        self._build_inflation_panel(sub_notebook)

        self._register_themed(frame, sub_notebook)

    def _labeled_entry(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=6)
        entry = tk.Entry(parent, width=18)
        entry.grid(row=row, column=1, padx=10, pady=6)
        return entry

    def _build_simple_interest_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Simple Interest")

        principal = self._labeled_entry(panel, "Principal:", 0)
        rate = self._labeled_entry(panel, "Annual Rate (%):", 1)
        years = self._labeled_entry(panel, "Years:", 2)
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                p, r, y = float(principal.get()), float(rate.get()), float(years.get())
                out = calc.simple_interest(p, r, y)
                text = f"Interest: {out['Interest']:.2f}\nTotal Amount: {out['Total Amount']:.2f}"
                result_var.set(text)
                history.add_entry(f"simple_interest(P={p}, R={r}%, Y={y})", text.replace("\n", "; "))
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, principal, rate, years, result_label)

    def _build_compound_interest_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Compound Interest")

        principal = self._labeled_entry(panel, "Principal:", 0)
        rate = self._labeled_entry(panel, "Annual Rate (%):", 1)
        years = self._labeled_entry(panel, "Years:", 2)
        n = self._labeled_entry(panel, "Compounds/year:", 3)
        n.insert(0, "1")
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                p, r, y = float(principal.get()), float(rate.get()), float(years.get())
                n_val = float(n.get() or 1)
                out = calc.compound_interest(p, r, y, n_val)
                text = f"Interest: {out['Interest']:.2f}\nTotal Amount: {out['Total Amount']:.2f}"
                result_var.set(text)
                history.add_entry(f"compound_interest(P={p}, R={r}%, Y={y}, n={n_val})", text.replace("\n", "; "))
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=4, column=0, columnspan=2, pady=10)
        self._register_themed(panel, principal, rate, years, n, result_label)

    def _build_emi_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="EMI")

        principal = self._labeled_entry(panel, "Loan Amount:", 0)
        rate = self._labeled_entry(panel, "Annual Rate (%):", 1)
        years = self._labeled_entry(panel, "Tenure (years):", 2)
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                p, r, y = float(principal.get()), float(rate.get()), float(years.get())
                out = calc.emi_calculator(p, r, y)
                text = (
                    f"Monthly EMI: {out['Monthly EMI']:.2f}\n"
                    f"Total Payment: {out['Total Payment']:.2f}\n"
                    f"Total Interest: {out['Total Interest']:.2f}"
                )
                result_var.set(text)
                history.add_entry(f"emi(P={p}, R={r}%, Y={y})", text.replace("\n", "; "))
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, principal, rate, years, result_label)

    def _build_cagr_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="CAGR")

        initial = self._labeled_entry(panel, "Initial Value:", 0)
        final = self._labeled_entry(panel, "Final Value:", 1)
        years = self._labeled_entry(panel, "Years:", 2)
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                i, f, y = float(initial.get()), float(final.get()), float(years.get())
                out = calc.cagr(i, f, y)
                text = f"CAGR: {out:.2f}%"
                result_var.set(text)
                history.add_entry(f"cagr(I={i}, F={f}, Y={y})", text)
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, initial, final, years, result_label)

    def _build_percentage_change_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="% Change")

        old = self._labeled_entry(panel, "Old Value:", 0)
        new = self._labeled_entry(panel, "New Value:", 1)
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                o, n = float(old.get()), float(new.get())
                out = calc.percentage_change(o, n)
                text = f"Change: {out:.2f}%"
                result_var.set(text)
                history.add_entry(f"pct_change(old={o}, new={n})", text)
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=2, column=0, columnspan=2, pady=10)
        self._register_themed(panel, old, new, result_label)

    def _build_inflation_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Inflation Adj.")

        amount = self._labeled_entry(panel, "Amount:", 0)
        rate = self._labeled_entry(panel, "Inflation Rate (%/yr):", 1)
        years = self._labeled_entry(panel, "Years:", 2)
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                a, r, y = float(amount.get()), float(rate.get()), float(years.get())
                out = calc.inflation_adjustment(a, r, y)
                text = f"Adjusted value: {out:.2f}"
                result_var.set(text)
                history.add_entry(f"inflation_adj(A={a}, R={r}%, Y={y})", text)
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, amount, rate, years, result_label)

    # ----------------------------------------------------------------
    # Utility tab
    # ----------------------------------------------------------------

    def _build_utility_tab(self):
        frame = self._add_tab("Utility")

        sub_notebook = ttk.Notebook(frame)
        sub_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_bmi_panel(sub_notebook)
        self._build_age_panel(sub_notebook)
        self._build_temp_panel(sub_notebook)
        self._build_length_panel(sub_notebook)
        self._build_weight_panel(sub_notebook)

        self._register_themed(frame, sub_notebook)

    def _build_bmi_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="BMI")

        weight = self._labeled_entry(panel, "Weight (kg):", 0)
        height = self._labeled_entry(panel, "Height (cm):", 1)
        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                w, h = float(weight.get()), float(height.get())
                out = calc.bmi_calculator(w, h)
                text = f"BMI: {out['BMI']:.2f}\nCategory: {out['Category']}"
                result_var.set(text)
                history.add_entry(f"bmi(W={w}kg, H={h}cm)", text.replace("\n", "; "))
            except ValueError:
                result_var.set("Enter valid numbers")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=2, column=0, columnspan=2, pady=10)
        self._register_themed(panel, weight, height, result_label)

    def _build_age_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Age Calculator")

        tk.Label(panel, text="Birth date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=10, pady=6)
        dob_entry = tk.Entry(panel, width=18)
        dob_entry.grid(row=0, column=1, padx=10, pady=6)

        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, justify="left", font=("Segoe UI", 11))
        result_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        def run():
            try:
                y, m, d = (int(x) for x in dob_entry.get().split("-"))
                birth = date(y, m, d)
                out = calc.age_calculator(birth)
                text = (
                    f"{out['Years']} years, {out['Months']} months, {out['Days']} days\n"
                    f"Total days lived: {out['Total Days']}"
                )
                result_var.set(text)
                history.add_entry(f"age({birth.isoformat()})", text.replace("\n", "; "))
            except ValueError:
                result_var.set("Use format YYYY-MM-DD")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Calculate", command=run).grid(row=1, column=0, columnspan=2, pady=10)
        self._register_themed(panel, dob_entry, result_label)

    def _build_temp_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Temperature")

        value = self._labeled_entry(panel, "Value:", 0)

        tk.Label(panel, text="From:").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        from_unit = ttk.Combobox(panel, values=calc.TEMP_UNITS, state="readonly", width=15)
        from_unit.current(0)
        from_unit.grid(row=1, column=1, padx=10, pady=6)

        tk.Label(panel, text="To:").grid(row=2, column=0, sticky="w", padx=10, pady=6)
        to_unit = ttk.Combobox(panel, values=calc.TEMP_UNITS, state="readonly", width=15)
        to_unit.current(1)
        to_unit.grid(row=2, column=1, padx=10, pady=6)

        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, pady=10)

        def run():
            try:
                v = float(value.get())
                out = calc.convert_temperature(v, from_unit.get(), to_unit.get())
                text = f"{out:.2f} {to_unit.get()}"
                result_var.set(text)
                history.add_entry(f"temp({v} {from_unit.get()} -> {to_unit.get()})", text)
            except ValueError:
                result_var.set("Enter a valid number")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Convert", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, value, result_label)

    def _build_length_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Length")

        units = list(calc.LENGTH_TO_METERS.keys())
        value = self._labeled_entry(panel, "Value:", 0)

        tk.Label(panel, text="From:").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        from_unit = ttk.Combobox(panel, values=units, state="readonly", width=15)
        from_unit.current(0)
        from_unit.grid(row=1, column=1, padx=10, pady=6)

        tk.Label(panel, text="To:").grid(row=2, column=0, sticky="w", padx=10, pady=6)
        to_unit = ttk.Combobox(panel, values=units, state="readonly", width=15)
        to_unit.current(2)
        to_unit.grid(row=2, column=1, padx=10, pady=6)

        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, pady=10)

        def run():
            try:
                v = float(value.get())
                out = calc.convert_length(v, from_unit.get(), to_unit.get())
                text = f"{out:.4f} {to_unit.get()}"
                result_var.set(text)
                history.add_entry(f"length({v} {from_unit.get()} -> {to_unit.get()})", text)
            except ValueError:
                result_var.set("Enter a valid number")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Convert", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, value, result_label)

    def _build_weight_panel(self, notebook):
        panel = tk.Frame(notebook)
        notebook.add(panel, text="Weight")

        units = list(calc.WEIGHT_TO_KG.keys())
        value = self._labeled_entry(panel, "Value:", 0)

        tk.Label(panel, text="From:").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        from_unit = ttk.Combobox(panel, values=units, state="readonly", width=15)
        from_unit.current(0)
        from_unit.grid(row=1, column=1, padx=10, pady=6)

        tk.Label(panel, text="To:").grid(row=2, column=0, sticky="w", padx=10, pady=6)
        to_unit = ttk.Combobox(panel, values=units, state="readonly", width=15)
        to_unit.current(1)
        to_unit.grid(row=2, column=1, padx=10, pady=6)

        result_var = tk.StringVar(value="")
        result_label = tk.Label(panel, textvariable=result_var, font=("Segoe UI", 11))
        result_label.grid(row=4, column=0, columnspan=2, pady=10)

        def run():
            try:
                v = float(value.get())
                out = calc.convert_weight(v, from_unit.get(), to_unit.get())
                text = f"{out:.4f} {to_unit.get()}"
                result_var.set(text)
                history.add_entry(f"weight({v} {from_unit.get()} -> {to_unit.get()})", text)
            except ValueError:
                result_var.set("Enter a valid number")
            except calc.CalculationError as e:
                result_var.set(str(e))

        tk.Button(panel, text="Convert", command=run).grid(row=3, column=0, columnspan=2, pady=10)
        self._register_themed(panel, value, result_label)

    # ----------------------------------------------------------------
    # Shared helpers
    # ----------------------------------------------------------------

    def _show_result(self, result_var: tk.StringVar, expr: str, result):
        formatted = f"{result:.6f}".rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
        result_var.set(f"{expr} = {formatted}")
        self.status_var.set(f"Calculated: {expr} = {formatted}")
        history.add_entry(expr, formatted)

    def _show_error(self, result_var: tk.StringVar, message: str):
        result_var.set(f"Error: {message}")
        self.status_var.set(f"Error: {message}")

    def _set_text_box(self, box: tk.Text, text: str):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.configure(state="disabled")

    def clear_status(self):
        self.status_var.set("Ready")

    def show_history(self):
        entries = history.load_entries()
        win = tk.Toplevel(self)
        win.title("Calculation History")
        win.geometry("520x420")
        win.configure(bg=self.theme["bg"])

        text_box = tk.Text(win, wrap="word", bg=self.theme["entry_bg"], fg=self.theme["entry_fg"])
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        text_box.insert("1.0", "\n".join(entries) if entries else "No history yet.")
        text_box.configure(state="disabled")

        def clear_all():
            if messagebox.askyesno("Clear History", "Delete all saved history?"):
                history.clear_history()
                text_box.configure(state="normal")
                text_box.delete("1.0", "end")
                text_box.insert("1.0", "No history yet.")
                text_box.configure(state="disabled")

        clear_btn = tk.Button(win, text="Clear History", command=clear_all)
        clear_btn.pack(pady=(0, 10))

    # ----------------------------------------------------------------
    # Theming
    # ----------------------------------------------------------------

    def _register_themed(self, *widgets):
        """Track widgets that need manual color updates on theme switch."""
        if not hasattr(self, "_themed_widgets"):
            self._themed_widgets = []
        self._themed_widgets.extend(widgets)

    def toggle_theme(self):
        self.theme_name = "Light" if self.theme_name == "Dark" else "Dark"
        self.theme = THEMES[self.theme_name]
        self._apply_theme()

    def _apply_theme(self):
        t = self.theme
        self.configure(bg=t["bg"])
        self.top_bar.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["fg"])
        self.theme_btn.configure(bg=t["button_bg"], fg=t["button_fg"], activebackground=t["button_active"])
        self.history_btn.configure(bg=t["button_bg"], fg=t["button_fg"], activebackground=t["button_active"])
        self.status_bar.configure(bg=t["panel_bg"], fg=t["fg"])

        for frame in self.tabs.values():
            self._theme_widget_tree(frame, t)

        if hasattr(self, "_themed_widgets"):
            for widget in self._themed_widgets:
                self._theme_widget_tree(widget, t)

    def _theme_widget_tree(self, widget, t):
        cls = widget.winfo_class()
        try:
            if cls in ("Frame",):
                widget.configure(bg=t["bg"])
            elif cls == "Label":
                widget.configure(bg=t["bg"], fg=t["fg"])
            elif cls == "Button":
                widget.configure(bg=t["button_bg"], fg=t["button_fg"], activebackground=t["button_active"])
            elif cls == "Entry":
                widget.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["entry_fg"])
            elif cls == "Text":
                widget.configure(bg=t["entry_bg"], fg=t["entry_fg"])
        except tk.TclError:
            pass

        for child in widget.winfo_children():
            self._theme_widget_tree(child, t)


if __name__ == "__main__":
    app = SmartCalcPro()
    app.mainloop()
