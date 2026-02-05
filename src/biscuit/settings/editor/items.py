import tkinter as tk
from tkinter import ttk

from biscuit.common.ui import Entry, Frame


class Item(Frame):
    def __init__(self, master, name="Example", *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.name = name
        self.config(padding=10)

        self.lbl = ttk.Label(
            self,
            text=self.name,
            font=self.base.settings.uifont_bold,
            anchor=tk.W,
        )
        self.lbl.pack(side=tk.LEFT, fill=tk.X)

class DropdownItem(Item):
    def __init__(
        self,
        master,
        name="Example",
        options=["True", "False"],
        default=0,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(master, name, *args, **kwargs)

        self.var = tk.StringVar(self, value=options[default])
        m = ttk.OptionMenu(self, self.var, options[default], *options)
        m.config(width=30)
        m.pack(side=tk.RIGHT)

    @property
    def value(self) -> str:
        return self.var.get()


class IntegerItem(Item):
    def __init__(self, master, name="Example", default="0", *args, **kwargs) -> None:
        super().__init__(master, name, *args, **kwargs)
        self.base.register(self.validate)

        self.entry = ttk.Entry(
            self,
            font=self.base.settings.uifont,
            width=30,
            validate="key",
            validatecommand=(self.register(self.validate), "%P"),
        )
        self.entry.insert(0, default)
        self.entry.pack(side=tk.RIGHT)

    def validate(self, value) -> None:
        return bool(value.isdigit() or value == "")

    @property
    def value(self) -> str:
        return self.entry.get()


class StringItem(Item):
    def __init__(
        self, master, name="Example", default="placeholder", *args, **kwargs
    ) -> None:
        super().__init__(master, name, *args, **kwargs)

        self.entry = ttk.Entry(self, font=self.base.settings.uifont, width=30)
        self.entry.insert(tk.END, default)
        self.entry.pack(side=tk.RIGHT)

    @property
    def value(self) -> str:
        return self.entry.get()


class CheckboxItem(Item):
    def __init__(self, master, name="Example", default=True, *args, **kwargs) -> None:
        super().__init__(master, name, *args, **kwargs)
        
        # Remove the default label as Checkbutton has its own
        self.lbl.destroy()

        self.var = tk.BooleanVar(self, value=default)
        ttk.Checkbutton(self, text=name, variable=self.var, cursor="hand2").pack(
            fill=tk.X, anchor=tk.W
        )

    @property
    def value(self) -> str:
        return self.var.get()
