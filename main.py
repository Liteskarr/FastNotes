"""
Точка входа в программу.
"""

import configparser
import sys

from PyQt5.QtWidgets import (QApplication)

from widgets.window import Window

app: QApplication
window: Window

config_filename = 'config.ini'
config: configparser.ConfigParser


def enable_file_logging():
    sys.stdout = open(config.get('debug', 'logs_file'), 'w', encoding='utf-8')


def enable_threads_exceptions() -> None:
    excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook


def enable_debug_mode() -> None:
    enable_threads_exceptions()
    enable_file_logging()


def load_cfg(filename: str) -> None:
    global config
    config = configparser.ConfigParser()
    config.read(filename)


def save_cfg(filename: str) -> None:
    global config
    config.write(open(filename, mode='w', encoding='utf-8'))


def main():
    global config_filename, config, app, window
    load_cfg(config_filename)
    if config.get('debug', 'debug') == '1':
        enable_debug_mode()
    app = QApplication(sys.argv)
    window = Window(dbname=config.get('settings', 'db_path'),
                    header=''.join(open(config.get('settings', 'header_path'), encoding='utf-8')))
    window.show()
    exit_status = app.exec()
    save_cfg(config_filename)
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
