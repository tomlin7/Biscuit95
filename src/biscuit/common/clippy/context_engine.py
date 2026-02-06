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
        
        self.watchers = [
            ASTWatcher(self),
            TerminalWatcher(self),
            GitWatcher(self.base),
            UserBehaviorWatcher(self)
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
        """Main loop: occasionally flushes old signals but otherwise we are event-driven."""
        while self.running:
            time.sleep(5)
            with self.aggregator._lock:
                cutoff = time.time() - 60
                self.aggregator.signals = [s for s in self.aggregator.signals if s["timestamp"] > cutoff]

    def check_and_trigger(self):
        """Check if current signals warrant a suggestion."""
        signals = self.aggregator.get_context()
        score = self.scorer.calculate_score(signals)
        
        if score >= 50:
            print(f"ContextEngine: Threshold met ({score}). Triggering!")
            self.trigger_suggestion(signals)
            self.aggregator.signals.clear()

    def trigger_suggestion(self, signals):
        if self.base.clippy:
            print("ContextEngine: Clippy found, sending suggestion...")
            
            # Analyze signals to create a helpful prompt
            error_count = sum(1 for s in signals if s['type'] == 'terminal_error')
            has_idle = any(s['type'] == 'idle' for s in signals)
            has_undo_burst = any(s['type'] == 'undo_burst' for s in signals)
            
            # Get the actual error text
            error_text = ""
            if error_count > 0:
                recent_errors = [s['data'] for s in signals if s['type'] == 'terminal_error']
                if recent_errors:
                    # Use the most recent error context, but truncate to 1000 chars to be safe
                    error_text = recent_errors[-1][:1000]
            
            # Clean Instruct prompt for DeepSeek-Coder 1.3B
            context = f"The user ran a command and got this error:\n{error_text[:300]}\n\n"
            context += "Instruction: Suggest the correct command or a brief fix. One sentence only."
            
            # print(f"DEBUG: Final prompt being sent to LLM:\n{context}\n")
            
            # Proactively ask brain
            if hasattr(self.base.clippy, 'suggest'):
                self.base.clippy.suggest(context)
            else:
                print("ContextEngine: Clippy has no suggest method!")
        else:
            print("ContextEngine: Clippy instance NOT found in self.base!")

    def report_signal(self, signal_type, data, confidence=1.0):
        print(f"ContextEngine: Signal received: {signal_type} ({confidence})")
        self.aggregator.add_signal(signal_type, data, confidence)
        self.check_and_trigger()
