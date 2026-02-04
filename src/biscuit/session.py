# Credits: RINO-GAELICO

from __future__ import annotations

import os
import toml
import typing

if typing.TYPE_CHECKING:
    from biscuit import App


class SessionManager:
    def __init__(self, base: App):
        self.base = base
        self.path = self.base.datadir / "session.toml"

    def restore_session(self):
        if not self.path.exists():
            return

        try:
            with open(self.path, "r") as f:
                config = toml.load(f)
                
            active_directory = config.get("active_directory")
            opened_files = config.get("opened_files", [])

            if active_directory:
                self.base.open_directory(active_directory)
            
            self.base.open_files(opened_files)
        except Exception as e:
            self.base.logger.error(f"Failed to restore session: {e}")

    def clear_session(self):
        if self.path.exists():
            try:
                os.remove(self.path)
            except Exception as e:
                self.base.logger.error(f"Failed to clear session: {e}")

    def save_session(self, opened_files, active_directory):
        data = {
            "active_directory": active_directory,
            "opened_files": opened_files
        }
        
        try:
            with open(self.path, "w") as f:
                toml.dump(data, f)
        except Exception as e:
            self.base.logger.error(f"Failed to save session: {e}")

    def close(self):
        pass
