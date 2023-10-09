# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

def do_nothing(*args, **kwargs):
    return

def add_label(parent, text, alignment):
    label = lv.label(parent)
    label.set_text(text)
    if alignment: label.align(*alignment)
    return label

def add_btn(parent, icon=None, text=None, size=None, alignment=None, callback=None):
    btn = lv.btn(parent)
    if icon: btn.set_style_bg_img_src(icon, 0)
    if text: label = add_label(btn, text, (lv.ALIGN.CENTER, 0, 20))
    if size: btn.set_size(*size)
    if alignment: btn.align(*alignment)
    if callback: btn.add_event(callback, lv.EVENT.SHORT_CLICKED, None)
    return btn

def make_square(obj):
    obj.update_layout()
    w = obj.get_width()
    h = obj.get_height()
    if w < h:
        obj.set_height(w)
    elif w > h:
        obj.set_width(h)

def obj_details(obj, details=""):
    details += f"{obj}; "
    if obj is not None:
        details += f"Size {obj.get_width(), obj.get_height()}; "
        details += f"Pos {obj.get_x(), obj.get_y()}; "
        details += f"Scroll x, y {obj.get_scroll_x(), obj.get_scroll_y()}; "
        print(details)
    return details

