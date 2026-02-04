from tkinter import ttk


class Scrollbar(ttk.Scrollbar):
    """Auto-hiding scrollbar widget
    Derived from ttk.Scrollbar"""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master) # , *args, **kwargs)

    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, low, high)
