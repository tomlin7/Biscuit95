import time
import threading

class BaseWatcher:
    def __init__(self, engine):
        self.engine = engine
        self.active = False
        
    def start(self):
        self.active = True
        
    def stop(self):
        self.active = False

class ASTWatcher(BaseWatcher):
    """Monitors code complexity and structure."""
    def start(self):
        super().start()
        # In a real implementation, this would subscribe to editor events
        # via the engine. For now, it relies on 'report_change' being called manually.
    
    def report_change(self, file_path, content_length, indentation_level):
        if not self.active: return
        
        # Simple heuristic: rapid growth in indentation or length
        # This is a placeholder for real AST analysis
        pass

class TerminalWatcher(BaseWatcher):
    """Monitors terminal output for errors."""
    def __init__(self, engine):
        super().__init__(engine)
        self.output_buffer = []  # Store last N lines
        self.max_buffer_size = 50
        self.last_command = ""
    
    def report_output(self, output, command=None):
        if not self.active: return
        
        if command:
            self.last_command = command.strip()
        
        # Split into lines and filter
        lines = [l.strip() for l in output.split("\n") if l.strip()]
        for line in lines:
            if "Microsoft Windows" in line or "Version 10" in line: continue
            self.output_buffer.append(line)
        
        if len(self.output_buffer) > self.max_buffer_size:
            self.output_buffer = self.output_buffer[-self.max_buffer_size:]
        
        # Simple error detection
        keywords = ["Error", "Exception", "Traceback", "Fail", "not recognized", "not found", "fatal"]
        if any(k.lower() in output.lower() for k in keywords):
            # Send high-quality context: Last Command + Recent Output
            context = f"Command: {self.last_command}\n"
            context += "Terminal Output:\n"
            context += "\n".join(self.output_buffer[-3:])
            
            print(f"DEBUG: Error context being sent:\n{context}")
            self.engine.report_signal("terminal_error", context, confidence=0.8)

class GitWatcher(BaseWatcher):
    """Monitors git status."""
    def __init__(self, base):
        # We need base to access git logic if available
        # Passing None for engine initially as it might be circular, handled by ContextEngine passing itself
        self.base = base
        super().__init__(None) 

    def start(self):
        super().start()
        threading.Thread(target=self.poll, daemon=True).start()
        
    def poll(self):
        while self.active:
            # Placeholder: Check git status if available
            # if self.base.git.repo: ...
            time.sleep(30)

class UserBehaviorWatcher(BaseWatcher):
    """Tracks typing speed, idle time, undos."""
    def __init__(self, engine):
        super().__init__(engine)
        self.last_action_time = time.time()
        self.undo_count = 0
        self.redo_count = 0
        self.type_count = 0
        self.typing_start_time = 0
        self.fidget_count = 0
        self.warning_sent = False
        
    def report_action(self, action_type, **kwargs):
        if not self.active: return
        
        now = time.time()
        self.last_action_time = now
        self.warning_sent = False # Reset idle warning
        
        if action_type == "undo":
            self.undo_count += 1
            if self.undo_count > 3:
                print("DEBUG: UserBehaviorWatcher detected UNDO BURST")
                self.engine.report_signal("undo_burst", "Repeated undos", confidence=0.7)
                self.undo_count = 0
        elif action_type == "redo":
            self.redo_count += 1
            if self.redo_count > 3:
                print("DEBUG: UserBehaviorWatcher detected REDO BURST")
                self.engine.report_signal("redo_burst", "Repeated redos", confidence=0.7)
                self.redo_count = 0
        elif action_type == "type":
            if self.typing_start_time == 0:
                self.typing_start_time = now
            self.type_count += 1
            
            # If typed 30 chars in a burst, report progress
            if self.type_count > 30:
                elapsed = now - self.typing_start_time
                if elapsed < 10: # Fast typing (approx 180 CPM)
                     print("DEBUG: UserBehaviorWatcher detected TYPING BURST")
                     self.engine.report_signal("typing_flow", "User is in a typing flow", confidence=0.4)
                
                self.type_count = 0
                self.typing_start_time = now
        elif action_type == "selection":
            self.fidget_count += 1
            if self.fidget_count > 10:
                print("DEBUG: UserBehaviorWatcher detected FIDGETING")
                self.engine.report_signal("fidgeting", "Frequent selection changes", confidence=0.3)
                self.fidget_count = 0
        elif action_type == "save":
             print("DEBUG: UserBehaviorWatcher detected SAVE")
             self.engine.report_signal("file_save", "User saved the file", confidence=0.5)
        elif action_type == "paste":
            data = kwargs.get("data", "")
            if len(data) > 200:
                print(f"DEBUG: UserBehaviorWatcher detected LARGE PASTE ({len(data)} chars)")
                self.engine.report_signal("large_paste", f"Pasted {len(data)} characters", confidence=0.6)
        
        # Decay counts for other actions
        if action_type != "undo": self.undo_count = max(0, self.undo_count - 0.1)
        if action_type != "redo": self.redo_count = max(0, self.redo_count - 0.1)
        if action_type != "selection": self.fidget_count = max(0, self.fidget_count - 0.1)

    def start(self):
        super().start()
        threading.Thread(target=self.check_idle, daemon=True).start()
        
    def check_idle(self):
        while self.active:
            idle_time = time.time() - self.last_action_time
            if idle_time > 120: # 2 minutes for Deep Idle
                 if self.warning_sent != "deep":
                     print("DEBUG: UserBehaviorWatcher detected DEEP IDLE")
                     self.engine.report_signal("deep_idle", "User is likely away", confidence=0.8)
                     self.warning_sent = "deep"
            elif idle_time > 30: # 30 seconds for Idle
                 if not self.warning_sent:
                     print("DEBUG: UserBehaviorWatcher detected IDLE")
                     self.engine.report_signal("idle", "User is pondering", confidence=0.5)
                     self.warning_sent = True
            time.sleep(10)
