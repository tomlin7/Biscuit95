import os

import toml


class Config:
    """Loads and manages configurations for biscuit."""

    def __init__(self, master) -> None:
        self.base = master.base

        self.font = ("Fira Code", 12)
        self.uifont = ("Fira Code", 10)

        self.auto_save_enabled = False
        self.auto_save_timer_ms = 10000

        self.clippy_enabled = False
        self.clippy_listeners = ["ast", "terminal", "git", "user_behavior"]

        self.load_data()

    def get_config_path(self, relative_path: str) -> str:
        """Get the absolute path to the resource

        Args:
            relative_path (str): path relative to the config directory"""

        return os.path.join(self.base.configdir, relative_path)

    def load_config(self) -> dict:
        path = self.get_config_path("settings.toml")
        if not os.path.exists(path):
            return {}
            
        with open(path, "r") as settingsfile:
            config = toml.load(settingsfile)

        return config

    def save_config(self) -> None:
        config = self.load_config()
        config["clippy_enabled"] = self.clippy_enabled
        config["clippy_listeners"] = self.clippy_listeners
        
        path = self.get_config_path("settings.toml")
        with open(path, "w") as settingsfile:
            toml.dump(config, settingsfile)

    def load_data(self) -> None:
        config = self.load_config()
        self.clippy_enabled = config.get("clippy_enabled", False)
        self.clippy_listeners = config.get("clippy_listeners", ["ast", "terminal", "git", "user_behavior"])
        
        # self.font = (config.get("font", "Fira Code"), config.get("font_size", 12))
