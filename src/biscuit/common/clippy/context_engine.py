import time
import threading
from .watchers import ASTWatcher, TerminalWatcher, GitWatcher, UserBehaviorWatcher

class SignalAggregator:
    def __init__(self):
        self.signals = []
        self._lock = threading.Lock()

    def add_signal(self, signal_type, data, confidence):
        with self._lock:
            self.signals.append({
                "type": signal_type,
                "data": data,
                "confidence": confidence,
                "timestamp": time.time()
            })
            
            # Keep only recent signals (last 5 minutes)
            cutoff = time.time() - 300
            self.signals = [s for s in self.signals if s["timestamp"] > cutoff]

    def get_context(self):
        """Returns all current signals."""
        with self._lock:
            return list(self.signals)

class TriggerScoringEngine:
    def calculate_score(self, signals):
        score = 0
        
        for signal in signals:
            signal_type = signal["type"]
            confidence = signal["confidence"]
            
            if signal_type == "terminal_error":
                score += 35 * confidence # 2 errors = 56 approx
            elif signal_type == "undo_burst":
                score += 40 * confidence
            elif signal_type == "idle":
                score += 25 * confidence
            elif signal_type == "complexity_spike":
                score += 15 * confidence
                
        return min(100, score)

class ContextEngine:
    _instance = None

    def __new__(cls, base):
        if cls._instance is None:
            cls._instance = super(ContextEngine, cls).__new__(cls)
            cls._instance.base = base
            cls._instance.setup()
        return cls._instance

    def setup(self):
        self.aggregator = SignalAggregator()
        self.scorer = TriggerScoringEngine()
        
        self.ast_watcher = ASTWatcher(self)
        self.terminal_watcher = TerminalWatcher(self)
        self.git_watcher = GitWatcher(self.base)
        self.user_watcher = UserBehaviorWatcher(self)
        
        self.watchers = [
            self.ast_watcher,
            self.terminal_watcher,
            self.git_watcher,
            self.user_watcher
        ]
        
        self.suggestion_callback = None
        self.running = False

    def start(self):
        self.running = True
        for watcher in self.watchers:
            watcher.start()
        
        threading.Thread(target=self.loop, daemon=True).start()

    def stop(self):
        self.running = False
        for watcher in self.watchers:
            watcher.stop()

    def loop(self):
        """Main loop: occasionally flushes old signals and checks for triggers."""
        while self.running:
            time.sleep(2) # CHECK EVERY 2 SECONDS
            with self.aggregator._lock:
                now = time.time()
                cutoff = now - 60
                self.aggregator.signals = [s for s in self.aggregator.signals if s["timestamp"] > cutoff]
            
            # Non-blocking check for triggers
            self.check_and_trigger()

    def check_and_trigger(self):
        """Check if current signals warrant a suggestion."""
        signals = self.aggregator.get_context()
        if not signals: return
        
        score = self.scorer.calculate_score(signals)
        
        if score >= 50:
            print(f"ContextEngine: Threshold met ({score}). Triggering!")
            self.trigger_suggestion(signals)
            with self.aggregator._lock:
                self.aggregator.signals.clear()

    def trigger_suggestion(self, signals):
        if self.base.clippy:
            print("ContextEngine: Clippy found, sending suggestion...")
            
            # Analyze signals to create a helpful prompt
            error_count = sum(1 for s in signals if s['type'] == 'terminal_error')
            
            # Get the actual error text
            error_text = ""
            if error_count > 0:
                recent_errors = [s['data'] for s in signals if s['type'] == 'terminal_error']
                if recent_errors:
                    error_text = recent_errors[-1][:1000]
            
            context = f"The user ran a command and got this error:\n{error_text[:300]}\n\n"
            context += "Instruction: Suggest the correct command or a brief fix. One sentence only."
            
            if hasattr(self.base.clippy, 'suggest'):
                self.base.clippy.suggest(context)

    def report_terminal_output(self, output, command=None):
        if self.running:
            self.terminal_watcher.report_output(output, command=command)

    def report_ast_change(self, file_path, content, indentation):
        if self.running:
            self.ast_watcher.report_change(file_path, content, indentation)

    def report_signal(self, signal_type, data, confidence=1.0):
        # Only log high confidence or important signals to console
        if confidence > 0.7 or signal_type == "terminal_error":
            print(f"ContextEngine: Signal received: {signal_type}")
            
        self.aggregator.add_signal(signal_type, data, confidence)
        
        # If it's a critical signal (error), trigger immediately
        if signal_type == "terminal_error":
             self.check_and_trigger()

    def report_user_action(self, action_type, **kwargs):
        if self.running:
            self.user_watcher.report_action(action_type, **kwargs)
