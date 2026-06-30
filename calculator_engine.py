"""
calculator_engine.py
---------------------
All calculation logic for SmartCalc Pro, kept separate from the GUI so the
math can be tested and reused independently of Tkinter.
"""

import math
import statistics
from datetime import date, datetime


class CalculationError(Exception):
    """Raised for invalid calculator input (division by zero, bad data, etc)."""
    pass


# --------------------------------------------------------------------------
# Basic operations
# --------------------------------------------------------------------------

def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise CalculationError("Cannot divide by zero")
    return a / b


def modulus(a: float, b: float) -> float:
    if b == 0:
        raise CalculationError("Cannot take modulus by zero")
    return a % b


def power(a: float, b: float) -> float:
    return a ** b


def square(a: float) -> float:
    return a ** 2


def cube(a: float) -> float:
    return a ** 3


def percentage(part: float, whole: float) -> float:
    if whole == 0:
        raise CalculationError("Whole value cannot be zero")
    return (part / whole) * 100


# --------------------------------------------------------------------------
# Scientific functions
# --------------------------------------------------------------------------

def square_root(a: float) -> float:
    if a < 0:
        raise CalculationError("Cannot take square root of a negative number")
    return math.sqrt(a)


def cube_root(a: float) -> float:
    return math.copysign(abs(a) ** (1 / 3), a)


def factorial(a: float) -> int:
    if a < 0 or a != int(a):
        raise CalculationError("Factorial requires a non-negative integer")
    return math.factorial(int(a))


def log_natural(a: float) -> float:
    if a <= 0:
        raise CalculationError("Log requires a positive number")
    return math.log(a)


def log_base10(a: float) -> float:
    if a <= 0:
        raise CalculationError("Log requires a positive number")
    return math.log10(a)


def exp(a: float) -> float:
    return math.exp(a)


def sin_deg(a: float) -> float:
    return math.sin(math.radians(a))


def cos_deg(a: float) -> float:
    return math.cos(math.radians(a))


def tan_deg(a: float) -> float:
    return math.tan(math.radians(a))


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------

def _parse_numbers(text: str) -> list[float]:
    try:
        values = [float(x) for x in text.replace(",", " ").split()]
    except ValueError as e:
        raise CalculationError("Enter numbers separated by spaces or commas") from e
    if not values:
        raise CalculationError("Enter at least one number")
    return values


def stats_summary(text: str) -> dict:
    values = _parse_numbers(text)
    summary = {
        "Count": len(values),
        "Mean": statistics.mean(values),
        "Median": statistics.median(values),
        "Maximum": max(values),
        "Minimum": min(values),
        "Range": max(values) - min(values),
    }
    try:
        summary["Mode"] = statistics.mode(values)
    except statistics.StatisticsError:
        summary["Mode"] = "No unique mode"
    if len(values) > 1:
        summary["Std Dev"] = statistics.stdev(values)
        summary["Variance"] = statistics.variance(values)
    else:
        summary["Std Dev"] = 0.0
        summary["Variance"] = 0.0
    return summary


# --------------------------------------------------------------------------
# Finance / Economics
# --------------------------------------------------------------------------

def simple_interest(principal: float, rate: float, years: float) -> dict:
    if principal < 0 or rate < 0 or years < 0:
        raise CalculationError("Principal, rate, and years must be non-negative")
    interest = (principal * rate * years) / 100
    return {"Interest": interest, "Total Amount": principal + interest}


def compound_interest(principal: float, rate: float, years: float, n: float = 1) -> dict:
    if principal < 0 or rate < 0 or years < 0 or n <= 0:
        raise CalculationError("Principal, rate, and years must be non-negative; n must be > 0")
    amount = principal * (1 + (rate / 100) / n) ** (n * years)
    return {"Interest": amount - principal, "Total Amount": amount}


def emi_calculator(principal: float, annual_rate: float, years: float) -> dict:
    if principal <= 0 or annual_rate < 0 or years <= 0:
        raise CalculationError("Principal and years must be positive; rate must be non-negative")
    months = years * 12
    if annual_rate == 0:
        emi = principal / months
    else:
        monthly_rate = (annual_rate / 100) / 12
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / (
            (1 + monthly_rate) ** months - 1
        )
    total_payment = emi * months
    return {
        "Monthly EMI": emi,
        "Total Payment": total_payment,
        "Total Interest": total_payment - principal,
    }


def cagr(initial_value: float, final_value: float, years: float) -> float:
    if initial_value <= 0 or years <= 0:
        raise CalculationError("Initial value and years must be positive")
    return ((final_value / initial_value) ** (1 / years) - 1) * 100


def percentage_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        raise CalculationError("Old value cannot be zero")
    return ((new_value - old_value) / abs(old_value)) * 100


def inflation_adjustment(amount: float, inflation_rate: float, years: float) -> float:
    if amount < 0 or years < 0:
        raise CalculationError("Amount and years must be non-negative")
    return amount * (1 + inflation_rate / 100) ** years


# --------------------------------------------------------------------------
# Utility tools
# --------------------------------------------------------------------------

def bmi_calculator(weight_kg: float, height_cm: float) -> dict:
    if weight_kg <= 0 or height_cm <= 0:
        raise CalculationError("Weight and height must be positive")
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {"BMI": bmi, "Category": category}


def age_calculator(birth_date: date, on_date: date | None = None) -> dict:
    on_date = on_date or date.today()
    if birth_date > on_date:
        raise CalculationError("Birth date cannot be in the future")

    years = on_date.year - birth_date.year
    months = on_date.month - birth_date.month
    days = on_date.day - birth_date.day

    if days < 0:
        months -= 1
        prev_month = on_date.month - 1 or 12
        prev_year = on_date.year if on_date.month != 1 else on_date.year - 1
        days_in_prev_month = (date(prev_year, prev_month % 12 + 1, 1) - date(prev_year, prev_month, 1)).days
        days += days_in_prev_month
    if months < 0:
        months += 12
        years -= 1

    total_days = (on_date - birth_date).days
    return {"Years": years, "Months": months, "Days": days, "Total Days": total_days}


TEMP_UNITS = ("Celsius", "Fahrenheit", "Kelvin")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        raise CalculationError(f"Unknown unit: {from_unit}")

    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        result = celsius + 273.15
        if result < 0:
            raise CalculationError("Resulting Kelvin temperature cannot be negative")
        return result
    raise CalculationError(f"Unknown unit: {to_unit}")


LENGTH_TO_METERS = {
    "Millimeters": 0.001,
    "Centimeters": 0.01,
    "Meters": 1.0,
    "Kilometers": 1000.0,
    "Inches": 0.0254,
    "Feet": 0.3048,
    "Miles": 1609.34,
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        raise CalculationError("Unknown length unit")
    meters = value * LENGTH_TO_METERS[from_unit]
    return meters / LENGTH_TO_METERS[to_unit]


WEIGHT_TO_KG = {
    "Grams": 0.001,
    "Kilograms": 1.0,
    "Pounds": 0.453592,
    "Ounces": 0.0283495,
}


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in WEIGHT_TO_KG or to_unit not in WEIGHT_TO_KG:
        raise CalculationError("Unknown weight unit")
    kg = value * WEIGHT_TO_KG[from_unit]
    return kg / WEIGHT_TO_KG[to_unit]
