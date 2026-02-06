import random
import tkinter as tk
from biscuit.common.ui import Toplevel, Label
from biscuit.common.ui.native import Canvas
from .brain import ClippyBrain
import threading

class Clippy(Toplevel):
    """
    Clippy - The floating assistant / Game-style Notification.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.base = master
        self.brain = ClippyBrain(self.base)
        
        # Dimensions (will be dynamically adjusted)
        self.char_size = 40
        self.min_width = 250
        self.max_width = 500
        self.width = self.min_width
        self.height = 60
        
        # Remove window decorations and set interactions
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        # Transparent background setup
        try:
             self.config(bg="#000001")
             self.attributes("-transparentcolor", "#000001")
        except:
             self.config(bg=self.base.theme.border)

        # Main container (The Notification Bar)
        # We use a frame with a background color for the "dialog box" look
        self.container = tk.Frame(self, bg="#FFFFE0", relief=tk.RAISED, borderwidth=1)
        self.container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Layout: [Character] [Message]
        
        # LEFT: Character Canvas
        self.canvas = Canvas(self.container, width=self.char_size, height=self.char_size, bg="#FFFFE0", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        
        # RIGHT: Message Label
        self.msg_label = tk.Label(self.container, text="Hi! I'm ready to help.", 
                               font=("Consolas", 9), fg="black", bg="#FFFFE0", 
                               anchor="w", justify=tk.LEFT)
        self.msg_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)
        
        # FAR RIGHT: Close Button
        self.close_btn = tk.Label(self.container, text="x", font=("Consolas", 10, "bold"), 
                                  fg="black", bg="#FFFFE0", cursor="hand2")
        self.close_btn.pack(side=tk.RIGHT, anchor=tk.NE, padx=2, pady=0)
        self.close_btn.bind("<Button-1>", self.close)

        # Initial Position (Bottom Right of Window)
        self.update_idletasks()
        
        # We need to wait for the base window to be mapped/configured to know its true position
        # But we can try to guess or update later.
        
        self.user_closed = False
        self.suggestion_id = 0
        self.downloading = False
        self.rel_x = -1 # Relative X from top-left. If -1, not yet set.
        self.rel_y = -1 # Relative Y from top-left.
        
        # Bind to application focus events
        self.base.bind("<FocusIn>", self.on_focus_in, add="+")
        self.base.bind("<FocusOut>", self.on_focus_out, add="+")
        self.base.bind("<Configure>", self.on_window_configure, add="+")

        self.frames = {
            "idle": [
                "011010110",
                "011111110",
                "110111011",
                "110111011",
                "110111011",
                "011111110",
                "011010110",
                "000111000",
            ],
            "blink": [
                "011010110",
                "011111110",
                "111111111", # Eyes closed
                "111111111",
                "110111011",
                "011111110",
                "011010110",
                "000111000",
            ],
            "look_left": [
                "011010110",
                "011111110",
                "101110111", # Pupils left
                "101110111",
                "110111011",
                "011111110",
                "011010110",
                "000111000",
            ],
            "look_right": [
                "011010110",
                "011111110",
                "111011101", # Pupils right
                "111011101",
                "110111011",
                "011111110",
                "011010110",
                "000111000",
            ],
            "what": [
                "011010110",
                "011111110",
                "110111011",
                "101111101",
                "110111011",
                "011111110",
                "011010110",
                "000111000",
            ],
            # Drastic: Shock
            "shock": [
                "011111110",
                "111111111",
                "110010011",
                "110010011",
                "110010011",
                "111111111",
                "011010110",
                "000000000",
            ],
            # Drastic: Glitch (Random noise)
            "glitch_1": [
                "101010101",
                "010101010",
                "110011001",
                "001100110",
                "101010101",
                "010001010",
                "111011101",
                "000111001",
            ],
            "glitch_2": [
                "010101010",
                "101010101",
                "001100110",
                "110011001",
                "010101010",
                "101110101",
                "000100010",
                "111000110",
            ],
            # Drastic: Spin Sequence (Side, Back, Side)
            "spin_side": [
                "000111000",
                "000111000",
                "000101000",
                "000101000",
                "000101000",
                "000111000",
                "000111000",
                "000010000",
            ],
            "spin_back": [
                "011010110",
                "011111110",
                "111111111",
                "111111111",
                "111111111",
                "011111110",
                "011010110",
                "000111000",
            ],
            # Loading Spinner
            "spinner_1": [ # Front
                "011010110",
                "011111110",
                "110111011",
                "110111011",
                "110111011",
                "011111110",
                "011010110",
                "000111000",
            ],
            "spinner_2": [ # 3/4 Side
                "001101100",
                "001111100",
                "011011100",
                "011011100",
                "011011100",
                "001111100",
                "001101100",
                "000111000",
            ],
            "spinner_3": [ # Side
                "000111000",
                "000111000",
                "000101000",
                "000101000",
                "000101000",
                "000111000",
                "000111000",
                "000010000",
            ],
            "spinner_4": [ # 1/4 Side (Flipped)
                "001101100",
                "001111100",
                "001110110",
                "001110110",
                "001110110",
                "001111100",
                "001101100",
                "000111000",
            ],
        }
        
        self.current_frame = "idle"
        self.spinner_index = 0
        self.draw_frame(self.current_frame)
        
        # Bindings
        for widget in (self.container, self.canvas, self.msg_label):
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        self.tasks = [
            "Refactor this function",
            "Add docstrings",
            "Write unit tests",
            "Optimize imports",
            "Fix linting errors",
            "Explain this code",
        ]
        
        self.downloading = False
        self.start_animation_loop()

    def update_size_for_message(self, message):
        """Dynamically resize window based on message length."""
        import tkinter.font as tkfont
        
        # Get font metrics
        font = tkfont.Font(family="Consolas", size=9)
        
        # Calculate text width
        text_width = font.measure(message)
        
        # Account for padding (char + margins + close button)
        padding = 100
        
        # Determine optimal width
        if text_width + padding <= self.min_width:
            # Short message - use minimum
            self.width = self.min_width
            wrap_length = self.min_width - padding
        elif text_width + padding <= self.max_width:
            # Medium message - expand to fit
            self.width = text_width + padding
            wrap_length = text_width
        else:
            # Long message - use max width and wrap
            self.width = self.max_width
            wrap_length = self.max_width - padding
        
        # Update wraplength
        self.msg_label.config(wraplength=wrap_length)
        
        # Calculate height based on wrapped text
        # Estimate number of lines after wrapping
        estimated_lines = max(1, (text_width // wrap_length) + 1)
        line_height = font.metrics("linespace")
        required_height = max(60, min(200, 20 + estimated_lines * line_height + 20))
        
        self.height = int(required_height)
        
        # Force update
        self.update_idletasks()
        
        # Reposition to maintain bottom-right alignment
        if hasattr(self.base, 'winfo_width'):
            try:
                parent_x = self.base.winfo_rootx()
                parent_y = self.base.winfo_rooty()
                parent_w = self.base.winfo_width()
                parent_h = self.base.winfo_height()
                
                new_x = parent_x + parent_w - self.width - 20
                new_y = parent_y + self.rel_y if self.rel_y != -1 else parent_y + parent_h - self.height - 20
                
                self.geometry(f"{self.width}x{self.height}+{new_x}+{new_y}")
            except:
                pass

    def close(self, event=None):
        self.user_closed = True
        self.withdraw()

    def on_window_configure(self, event):
        # Respond to main window moving/resizing
        if event.widget == self.base:
            # Always stick to the right
            self.rel_x = event.width - self.width - 20
            
            # If we haven't set an initial position, set it to bottom-right now
            if self.rel_y == -1:
                self.rel_y = event.height - self.height - 20
            
            # Reposition
            new_x = event.x + self.rel_x
            new_y = event.y + self.rel_y
            self.geometry(f"{self.width}x{self.height}+{new_x}+{new_y}")

    def on_focus_in(self, event):
        # Only show if not explicitly closed by user
        if not self.user_closed:
            self.deiconify()

    def on_focus_out(self, event):
        self.withdraw()

    def draw_frame(self, frame_name):
        """Draws the pixel art character."""
        self.canvas.delete("all")
        pixel_map = self.frames.get(frame_name, self.frames["idle"])
        
        rows = len(pixel_map)
        cols = len(pixel_map[0])
        
        # Maximize pixel size within the canvas dimensions
        pixel_size = min(self.char_size / cols, self.char_size / rows)
        
        # Simple centering
        x_off = (self.char_size - (cols * pixel_size)) / 2
        y_off = (self.char_size - (rows * pixel_size)) / 2
        
        for r, row in enumerate(pixel_map):
            for c, char in enumerate(row):
                if char == '1':
                    x1 = x_off + c * pixel_size
                    y1 = y_off + r * pixel_size
                    x2 = x1 + pixel_size
                    y2 = y1 + pixel_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="", tags="body")
        
    def start_drag(self, event):
        self.dragging = False
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        self.dragging = True
        
        # Absolute mouse position
        mx = self.winfo_pointerx()
        my = self.winfo_pointery()
        
        # Calculate new absolute position for Clippy
        # new_x = mx - self.offset_x # IGNORED for X
        new_y = my - self.offset_y
        
        # Get main window absolute bounds
        root = self.base 
        parent_x = root.winfo_rootx()
        parent_y = root.winfo_rooty()
        parent_w = root.winfo_width()
        parent_h = root.winfo_height()
        
        # Clamp to bounds
        # Relative to parent
        # rel_x = new_x - parent_x # IGNORED
        rel_y = new_y - parent_y
        
        # Force X to be on the right side
        rel_x = parent_w - self.width - 20
        
        # Clamp relative Y position
        rel_y = max(0, min(rel_y, parent_h - self.height))
        
        # Update stored relative position
        self.rel_x = rel_x
        self.rel_y = rel_y
        
        # Apply absolute
        final_x = parent_x + rel_x
        final_y = parent_y + rel_y
        
        self.geometry(f"+{final_x}+{final_y}")

    def stop_drag(self, event):
        if not self.dragging:
            self.on_click(event)
        self.dragging = False

    def suggest(self, context=None):
        """Proactively suggest something based on context."""
        self.suggestion_id += 1
        current_id = self.suggestion_id
        
        if not self.brain.loading:
            # Flash animation
            self.play_drastic_animation()
            self.show_message("I noticed something... Thinking...", duration=None)
        
        def update_progress(msg):
            if current_id != self.suggestion_id and not msg.startswith("Downloading"): return
            self.base.root.after(0, lambda: self.show_message(msg))
            
        def ask_brain():
            self.downloading = True
            
            prompt = f"Help the user based on this context. Keep it short and helpful:\n{context}"
            # Brain is already using DeepSeek model now
            response = self.brain.ask(prompt, callback=update_progress)
            
            self.downloading = False
            if current_id == self.suggestion_id:
                self.base.root.after(0, lambda: self.show_message(response if response else "Nevermind."))

        threading.Thread(target=ask_brain).start()
        
        # Ensure visible
        if self.user_closed:
            self.base.root.after(0, self.deiconify)

    def on_click(self, event):
        self.suggestion_id += 1
        current_id = self.suggestion_id

        if not self.brain.loading:
            # Trigger local brain thought
            self.show_message("Thinking...", duration=None)
        
        def update_progress(msg):
            if current_id != self.suggestion_id and not msg.startswith("Downloading"): return
            self.base.root.after(0, lambda: self.show_message(msg))
            
        def ask_brain():
            self.downloading = True
            
            # Contextual prompt?
            prompt = "You are Clippy, a helpful, witty, and slightly chaotic coding assistant. Give me a short, one-sentence tip or a funny remark about coding."
            
            # This might trigger download
            response = self.brain.ask(prompt, callback=update_progress)
            
            self.downloading = False
            if current_id == self.suggestion_id:
                self.base.root.after(0, lambda: self.show_message(response if response else "Something went wrong."))

        threading.Thread(target=ask_brain).start()
        
        # Also show AI panel if needed, but maybe don't overwrite input if we are just chatting locally
        # if self.base.secondary_sidebar:
        #      self.base.secondary_sidebar.show_ai()

    def on_enter(self, event):
        self.container.config(bg="#EEE8AA")
        self.msg_label.config(bg="#EEE8AA")
        self.canvas.config(bg="#EEE8AA")
        self.config(cursor="hand2")

    def on_leave(self, event):
        self.container.config(bg="#FFFFE0")
        self.msg_label.config(bg="#FFFFE0")
        self.canvas.config(bg="#FFFFE0")
        self.config(cursor="")

    def start_animation_loop(self):
        """Main animation loop for frequent state changes."""
        self.animate()

    def animate(self):
        # If installing/downloading, play a busy animation
        if self.downloading:
            spinner_frames = ["spinner_1", "spinner_2", "spinner_3", "spinner_4"]
            self.spinner_index = (self.spinner_index + 1) % len(spinner_frames)
            
            self.draw_frame(spinner_frames[self.spinner_index])
            self.after(100, self.animate) # Fast rotation
            return

        # 0. Chance for drastic animation (e.g. 5%)
        if random.random() < 0.05:
            self.play_drastic_animation()
            return
            
        # 1. Decide next frame
        # We want frequent changes.
        choices = ["idle"] * 10 + ["blink"] * 2 + ["look_left"] * 3 + ["look_right"] * 3 + ["what"] * 1
        next_frame = random.choice(choices)
        
        self.draw_frame(next_frame)
        
        # 2. Decide duration until next frame
        # "animate frequently" -> 200ms to 2000ms?
        duration = random.choice([100, 200, 500, 1000, 2000])
        
        # If blinking, quick switch back
        if next_frame == "blink":
            duration = 150
            
        self.after(duration, self.animate)

    def play_drastic_animation(self):
        """Plays a multi-frame drastic animation sequence."""
        anim_type = random.choice(["spin", "glitch", "shock"])
        
        if anim_type == "spin":
            # Spin sequence: Side -> Back -> Side -> Front
            seq = [("spin_side", 100), ("spin_back", 100), ("spin_side", 100), ("idle", 100)]
        elif anim_type == "glitch":
            # Glitch sequence: Glitch1 -> Glitch2 -> Glitch1 -> Idle
            seq = [("glitch_1", 50), ("glitch_2", 50), ("glitch_1", 50), ("idle", 100)] * 3
        elif anim_type == "shock":
            # Shock: Shock -> Shake? -> Idle
            seq = [("shock", 100), ("idle", 50), ("shock", 100), ("idle", 2000)]
            
        self.run_sequence(seq)

    def run_sequence(self, sequence):
        """Runs a sequence of (frame_name, duration) tuples."""
        if not sequence:
            self.animate() # Return to normal loop
            return
            
        frame, duration = sequence[0]
        self.draw_frame(frame)
        self.after(duration, lambda: self.run_sequence(sequence[1:]))

    def show_message(self, text, duration=None):
        """Update the speech bubble text."""
        self.msg_label.config(text=text)
        self.update_size_for_message(text)
        # Messages now persist until next event (no auto-reset)
