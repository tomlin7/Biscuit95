import os
import threading
import requests
import logging

try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except ImportError:
    HAS_LLAMA = False

class ClippyBrain:
    def __init__(self, base):
        self.base = base
        self.model = None
        self.model_name = "qwen1_5-0_5b-chat-q4_k_m.gguf"
        self.model_url = "https://huggingface.co/Qwen/Qwen1.5-0.5B-Chat-GGUF/resolve/main/qwen1_5-0_5b-chat-q4_k_m.gguf"
        # Fix: config_dir -> configdir (ConfigManager attribute)
        self.model_path = os.path.join(self.base.configdir, "models", self.model_name)
        self.loading = False
        
        # Ensure model directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def is_available(self):
        return HAS_LLAMA and os.path.exists(self.model_path)

    def load_model(self, callback=None):
        if not HAS_LLAMA:
            logging.error("llama-cpp-python not installed. Cannot run local brain.")
            return False

        if self.model:
            return True

        if not os.path.exists(self.model_path):
            self.download_model(callback)
            
        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4, # Adjust as needed
                verbose=False
            )
            return True
        except Exception as e:
            logging.error(f"Failed to load Clippy model: {e}")
            return False

    def download_model(self, callback=None):
        if self.loading: 
            return
        
        self.loading = True
        try:
            logging.info(f"Downloading {self.model_name}...")
            if callback:
                callback("Downloading brain... 0%")
                
            response = requests.get(self.model_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(self.model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if callback and total_size > 0:
                        percent = int((downloaded_size / total_size) * 100)
                        callback(f"Downloading brain... {percent}%")
            
            logging.info("Model downloaded successfully.")
        except Exception as e:
            logging.error(f"Failed to download model: {e}")
            # Clean up partial file
            if os.path.exists(self.model_path):
                os.remove(self.model_path)
        finally:
            self.loading = False

    def ask(self, prompt, callback=None):
        if not self.is_available():
            if not HAS_LLAMA:
                return "I need a brain! (Install llama-cpp-python)"
            if not os.path.exists(self.model_path):
                threading.Thread(target=self.load_model, args=(callback,)).start()
                return # Async download started, we will just wait or user clicks again
                # Actually, better logic is to let load_model be called synchronously in the thread wrapper in view

        if not self.model:
            self.load_model(callback)
            
        if not self.model:
            return "My brain hurts. (Model failed to load)"

        # Simple ChatML-like format for Qwen
        formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        try:
            output = self.model(
                formatted_prompt,
                max_tokens=128, # Keep it short and snappy
                stop=["<|im_end|>"],
                echo=False
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            logging.error(f"Inference error: {e}")
            return "I'm confused."
