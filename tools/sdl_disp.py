# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv


def sdl_display(width, height, title="LVGL Simulator", default_group=False):
    display = lv.sdl_window_create(width, height)
    lv.sdl_window_set_title(display, title)
    mouse = lv.sdl_mouse_create()
    mouse.set_disp(display)
    keyboard = lv.sdl_keyboard_create()
    keyboard.set_disp(display)
    if default_group is False:
        group = lv.group_create()
    elif default_group is True:
        group = lv.group_get_default()
    else:
        group = default_group
    keyboard.set_group(group)
    return display, group
