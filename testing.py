import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()


# Create a Style object
style = ttk.Style()

# Apply the 'clam' theme
style.theme_use("clam")


# Create a modern ttk Button
ttk.Button(root, text="Click Me").pack()

# Create a classic tk Button (for comparison)
tk.Button(root, text="Classic Button").pack()

# Start the GUI event loop
root.mainloop()
