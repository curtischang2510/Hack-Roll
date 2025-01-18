from .main_window import MainWindow

__all__ = ["MainWindow", "CustomButton", "ErrorDialog", "InfoDialog"]

import os

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
