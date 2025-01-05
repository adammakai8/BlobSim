import os
import shutil
import pygetwindow as gw
from typing import Any

import keyboard

from domain.utils.constants import CYCLES_PER_EON, CYCLES_PER_EPOCH, CYCLES_PER_SEASON, EPOCHS_PER_SEASON
from domain.dtos.event_dto import EventTypeDto
from presentation.constants import APP_NAME, BRONZE_FORMAT, GOLD_FORMAT, SILVER_FORMAT


def color_by_position(position: int, data: Any) -> str:
    if position == 1:
        return GOLD_FORMAT.format(data)
    elif position == 2:
        return SILVER_FORMAT.format(data)
    elif position == 3:
        return BRONZE_FORMAT.format(data)
    else:
        return str(data)


def highlight_by_condition(data: Any, condition: bool) -> str:
    if condition:
        return f'[cyan]{data}[/cyan]'
    else:
        return str(data)


def clear_console():
    """Clears the console based on the operating system.
    (Disclaimer: this function was generated by Gemini)"""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')


def get_console_width() -> int:
    return shutil.get_terminal_size().columns


def get_console_height() -> int:
    return shutil.get_terminal_size().lines


def format_sim_time(time: int) -> str:
    return f'Eon: {int(time / CYCLES_PER_EON)} Season: {int(time / CYCLES_PER_SEASON) + 1}. '\
        f'{int(time / CYCLES_PER_EPOCH) % EPOCHS_PER_SEASON} - {time % CYCLES_PER_EPOCH}'


def format_sim_time_short(time: int) -> str:
    return f'{int(time / CYCLES_PER_SEASON) + 1}. {int(time / CYCLES_PER_EPOCH) % EPOCHS_PER_SEASON:2d} - {time % CYCLES_PER_EPOCH}'


def capture_keypress() -> str | None:
    key = keyboard.read_event()
    if APP_NAME in gw.getActiveWindowTitle():
        return key.name
    else:
        return None


def get_text_by_key(key: str) -> str:
    """ Returns a string assigned to a specified translation key. Used to translate enum values to readable text. """

    if key == EventTypeDto.QUARTERED_TWO_SHOT_SCORING:
        return 'Quartered two-shot high jump'
    if key == EventTypeDto.QUARTERED_ONE_SHOT_SCORING:
        return 'Quartered one-shot high jump'
    return 'Unknown key'
