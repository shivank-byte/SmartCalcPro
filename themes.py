"""
themes.py
---------
Color palettes for the dark/light theme toggle.
"""

THEMES = {
    "Dark": {
        "bg": "#1e1e2e",
        "fg": "#f5f5f5",
        "panel_bg": "#2a2a3c",
        "entry_bg": "#11111b",
        "entry_fg": "#a6e3a1",
        "accent": "#89b4fa",
        "button_bg": "#313244",
        "button_fg": "#f5f5f5",
        "button_active": "#45475a",
        "error_fg": "#f38ba8",
    },
    "Light": {
        "bg": "#f5f5f5",
        "fg": "#1e1e2e",
        "panel_bg": "#ffffff",
        "entry_bg": "#eaeaea",
        "entry_fg": "#1e1e2e",
        "accent": "#1e66f5",
        "button_bg": "#e0e0e0",
        "button_fg": "#1e1e2e",
        "button_active": "#cfcfcf",
        "error_fg": "#d20f39",
    },
}

DEFAULT_THEME = "Dark"
