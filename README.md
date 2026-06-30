# SmartCalc Pro

A desktop calculator built with Python and Tkinter, covering basic math,
scientific functions, statistics, finance/economics, and everyday utility
conversions — with calculation history, error handling, and a dark/light
theme toggle.

Built as a minor project to demonstrate solid Python fundamentals (OOP,
modules, file handling, error handling, GUI event-driven programming)
without overshadowing larger portfolio projects.

## Features

**Basic**
Add, subtract, multiply, divide, modulus, power, square, cube, percentage-of.

**Scientific**
Square root, cube root, factorial, natural log, log10, eˣ, sin/cos/tan (degrees).

**Statistics**
Paste a list of numbers and get mean, median, mode, standard deviation,
variance, range, max, and min in one click.

**Finance / Economics**
- Simple interest
- Compound interest (with configurable compounding frequency)
- EMI calculator (loan amount, rate, tenure → monthly payment)
- CAGR (compound annual growth rate)
- Percentage change
- Inflation adjustment (what's ₹100 from year X worth today, given a rate)

**Utility**
BMI calculator, age calculator (exact years/months/days + total days lived),
temperature converter, length converter, weight converter.

**Quality-of-life**
- Calculation history, saved to `history.txt` and viewable in-app
- Clear history button
- Dark / Light theme toggle
- Status bar showing the last calculation or error
- Keyboard shortcuts: `Ctrl+H` (history), `Ctrl+L` (clear status)
- Input validation with readable error messages instead of crashes

## Screenshots

<!--
Add screenshots or a short screen recording here once you've run the app
locally. In GitHub's file editor, drag and drop image/GIF files directly
into this README and it'll auto-generate the markdown for you, like:

![Basic tab](screenshots/basic_tab.png)
![Finance tab](screenshots/finance_tab.png)

A short GIF showing a few calculations + the theme toggle works well too.
-->

## Project structure

```
main.py                # GUI: tabs, layout, event handling
calculator_engine.py   # All calculation logic, GUI-independent
history.py             # Reads/writes history.txt
themes.py               # Color palettes for dark/light mode
requirements.txt
```

The calculation logic is deliberately separated from the GUI — every
function in `calculator_engine.py` can be imported and tested on its own,
without launching Tkinter. That's the part worth pointing to if asked about
design decisions: it's a small example of separating business logic from
presentation.

## Run it

```bash
python main.py
```

No external dependencies — everything used is in the Python standard
library (`tkinter`, `math`, `statistics`, `datetime`).

## Resume line

**SmartCalc Pro | Python, Tkinter**
Built a desktop calculator with 25+ functions across basic, scientific,
statistical, financial, and utility categories. Separated calculation
logic from the GUI layer, implemented persistent calculation history,
input validation, and a theme switcher.
