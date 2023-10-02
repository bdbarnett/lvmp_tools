# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

event_dict = {
    0: "lv.EVENT.ALL",
    1: "lv.EVENT.PRESSED",
    2: "lv.EVENT.PRESSING",
    3: "lv.EVENT.PRESS_LOST",
    4: "lv.EVENT.SHORT_CLICKED",
    5: "lv.EVENT.LONG_PRESSED",
    6: "lv.EVENT.LONG_PRESSED_REPEAT",
    7: "lv.EVENT.CLICKED",
    8: "lv.EVENT.RELEASED",
    9: "lv.EVENT.SCROLL_BEGIN",
    10: "lv.EVENT.SCROLL_THROW_BEGIN",
    11: "lv.EVENT.SCROLL_END",
    12: "lv.EVENT.SCROLL",
    13: "lv.EVENT.GESTURE",
    14: "lv.EVENT.KEY",
    15: "lv.EVENT.FOCUSED",
    16: "lv.EVENT.DEFOCUSED",
    17: "lv.EVENT.LEAVE",
    18: "lv.EVENT.HIT_TEST",
    19: "lv.EVENT.COVER_CHECK",
    20: "lv.EVENT.REFR_EXT_DRAW_SIZE",
    21: "lv.EVENT.DRAW_MAIN_BEGIN",
    22: "lv.EVENT.DRAW_MAIN",
    23: "lv.EVENT.DRAW_MAIN_END",
    24: "lv.EVENT.DRAW_POST_BEGIN",
    25: "lv.EVENT.DRAW_POST",
    26: "lv.EVENT.DRAW_POST_END",
    27: "lv.EVENT.DRAW_PART_BEGIN",
    28: "lv.EVENT.DRAW_PART_END",
    29: "lv.EVENT.VALUE_CHANGED",
    30: "lv.EVENT.INSERT",
    31: "lv.EVENT.REFRESH",
    32: "lv.EVENT.READY",
    33: "lv.EVENT.CANCEL",
    34: "lv.EVENT.DELETE",
    35: "lv.EVENT.CHILD_CHANGED",
    36: "lv.EVENT.CHILD_CREATED",
    37: "lv.EVENT.CHILD_DELETED",
    38: "lv.EVENT.SCREEN_UNLOAD_START",
    39: "lv.EVENT.SCREEN_LOAD_START",
    40: "lv.EVENT.SCREEN_LOADED",
    41: "lv.EVENT.SCREEN_UNLOADED",
    42: "lv.EVENT.SIZE_CHANGED",
    43: "lv.EVENT.STYLE_CHANGED",
    44: "lv.EVENT.LAYOUT_CHANGED",
    45: "lv.EVENT.GET_SELF_SIZE",
    46: "lv.EVENT.MSG_RECEIVED",
    47: "lv.EVENT.INVALIDATE_AREA",
    48: "lv.EVENT.RENDER_START",
    49: "lv.EVENT.RENDER_READY",
    50: "lv.EVENT.RESOLUTION_CHANGED",
    51: "lv.EVENT.REFR_START",
    52: "lv.EVENT.REFR_FINISH",
    53: "lv.EVENT.FLUSH_START",
    54: "lv.EVENT.FLUSH_FINISH",
    128: "lv.EVENT.PREPROCESS",
}

exclude_list = [
    lv.EVENT.SCROLL_BEGIN,
    lv.EVENT.SCROLL_THROW_BEGIN,
    lv.EVENT.SCROLL_END,
    lv.EVENT.SCROLL,
    lv.EVENT.GESTURE,
    lv.EVENT.HIT_TEST,
    lv.EVENT.COVER_CHECK,
    lv.EVENT.REFR_EXT_DRAW_SIZE,
    lv.EVENT.DRAW_MAIN_BEGIN,
    lv.EVENT.DRAW_MAIN,
    lv.EVENT.DRAW_MAIN_END,
    lv.EVENT.DRAW_POST_BEGIN,
    lv.EVENT.DRAW_POST,
    lv.EVENT.DRAW_POST_END,
    lv.EVENT.DRAW_PART_BEGIN,
    lv.EVENT.DRAW_PART_END,
    lv.EVENT.INSERT,
    lv.EVENT.REFRESH,
    lv.EVENT.READY,
    lv.EVENT.CANCEL,
    lv.EVENT.DELETE,
    lv.EVENT.SCREEN_UNLOAD_START,
    lv.EVENT.SCREEN_LOAD_START,
    lv.EVENT.SCREEN_LOADED,
    lv.EVENT.SCREEN_UNLOADED,
    lv.EVENT.SIZE_CHANGED,
    lv.EVENT.STYLE_CHANGED,
    lv.EVENT.LAYOUT_CHANGED,
    lv.EVENT.GET_SELF_SIZE,
    lv.EVENT.INVALIDATE_AREA,
    lv.EVENT.RENDER_START,
    lv.EVENT.RENDER_READY,
    lv.EVENT.RESOLUTION_CHANGED,
    lv.EVENT.REFR_START,
    lv.EVENT.REFR_FINISH,
    lv.EVENT.FLUSH_START,
    lv.EVENT.FLUSH_FINISH,
    lv.EVENT.PREPROCESS,
]


def debug_event_cb(event, *args, **kwargs):
    code = event.get_code()
    param = event.get_param()
    user_data = event.get_user_data()
    target_obj = event.get_target_obj()
    current_target_obj = event.get_current_target_obj()

    obj = target_obj
    if code not in exclude_list:
        print(
            f"\ndebug_event_cb: {obj} at position ({obj.get_x()}, {obj.get_y()}) received event: {event_dict[code]}"
        )
        obj_info = ""
        attr_found = False
        for attr in ["get_text", "get_value", "get_selected", "get_rgb"]:
            if hasattr(obj, attr):
                if attr_found == True: obj_info += ", "
                obj_info += f"{attr} = {getattr(obj, attr)()}"
                attr_found = True
        if attr_found: print('%s' % (obj_info))
        if args: print(f"    Positional arguments: {args}")
        if kwargs: print(f"    Keyword arguments: {kwargs}")
