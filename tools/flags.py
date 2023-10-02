# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

"""
Usage:
    import lvgl as lv
    from flags import flags
    
    obj1 = lv.btn()
    obj2 = lv.label()

    # to see the flags of obj1
    obj_flags(obj1)
    
    # to see the flags in one but not the other
    obj_flags(obj1).difference(obj_flags(obj2))
    
    # to see the flags obj1 has that obj2 doesn't
    obj_flags(obj1).intersection(obj_flags(obj1).difference(obj_flags(obj2)))
    
    # to see the flags obj2 has that obj1 doesn't
    obj_flags(obj2).intersection(obj_flags(obj1).difference(obj_flags(obj2)))
    
    # to see any of the above sorted, just wrap with sorted
    sorted(obj_flags(obj1))
"""


def obj_flags(obj):
    return {flag_dict[flag] for flag in flag_dict.keys() if obj.has_flag(flag)}


flag_dict = {
    lv.obj.FLAG.ADV_HITTEST: "lv.obj.FLAG.ADV_HITTEST",
    lv.obj.FLAG.CHECKABLE: "lv.obj.FLAG.CHECKABLE",
    lv.obj.FLAG.CLICK_FOCUSABLE: "lv.obj.FLAG.CLICK_FOCUSABLE",
    lv.obj.FLAG.CLICKABLE: "lv.obj.FLAG.CLICKABLE",
    lv.obj.FLAG.EVENT_BUBBLE: "lv.obj.FLAG.EVENT_BUBBLE",
    lv.obj.FLAG.FLOATING: "lv.obj.FLAG.FLOATING",
    lv.obj.FLAG.GESTURE_BUBBLE: "lv.obj.FLAG.GESTURE_BUBBLE",
    lv.obj.FLAG.HIDDEN: "lv.obj.FLAG.HIDDEN",
    lv.obj.FLAG.IGNORE_LAYOUT: "lv.obj.FLAG.IGNORE_LAYOUT",
    lv.obj.FLAG.LAYOUT_1: "lv.obj.FLAG.LAYOUT_1",
    lv.obj.FLAG.LAYOUT_2: "lv.obj.FLAG.LAYOUT_2",
    lv.obj.FLAG.OVERFLOW_VISIBLE: "lv.obj.FLAG.OVERFLOW_VISIBLE",
    lv.obj.FLAG.PRESS_LOCK: "lv.obj.FLAG.PRESS_LOCK",
    lv.obj.FLAG.SCROLL_CHAIN: "lv.obj.FLAG.SCROLL_CHAIN",
    lv.obj.FLAG.SCROLL_CHAIN_HOR: "lv.obj.FLAG.SCROLL_CHAIN_HOR",
    lv.obj.FLAG.SCROLL_CHAIN_VER: "lv.obj.FLAG.SCROLL_CHAIN_VER",
    lv.obj.FLAG.SCROLL_ELASTIC: "lv.obj.FLAG.SCROLL_ELASTIC",
    lv.obj.FLAG.SCROLL_MOMENTUM: "lv.obj.FLAG.SCROLL_MOMENTUM",
    lv.obj.FLAG.SCROLL_ON_FOCUS: "lv.obj.FLAG.SCROLL_ON_FOCUS",
    lv.obj.FLAG.SCROLL_ONE: "lv.obj.FLAG.SCROLL_ONE",
    lv.obj.FLAG.SCROLL_WITH_ARROW: "lv.obj.FLAG.SCROLL_WITH_ARROW",
    lv.obj.FLAG.SCROLLABLE: "lv.obj.FLAG.SCROLLABLE",
    lv.obj.FLAG.SNAPPABLE: "lv.obj.FLAG.SNAPPABLE",
    lv.obj.FLAG.USER_1: "lv.obj.FLAG.USER_1",
    lv.obj.FLAG.USER_2: "lv.obj.FLAG.USER_2",
    lv.obj.FLAG.USER_3: "lv.obj.FLAG.USER_3",
    lv.obj.FLAG.USER_4: "lv.obj.FLAG.USER_4",
    lv.obj.FLAG.WIDGET_1: "lv.obj.FLAG.WIDGET_1",
    lv.obj.FLAG.WIDGET_2: "lv.obj.FLAG.WIDGET_2",
}
