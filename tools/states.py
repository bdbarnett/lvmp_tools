# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

state_dict = {
    lv.STATE.ANY: "lv.STATE.ANY",
    lv.STATE.CHECKED: "lv.STATE.CHECKED",
    lv.STATE.DEFAULT: "lv.STATE.DEFAULT",
    lv.STATE.DISABLED: "lv.STATE.DISABLED",
    lv.STATE.EDITED: "lv.STATE.EDITED",
    lv.STATE.FOCUS_KEY: "lv.STATE.FOCUS_KEY",
    lv.STATE.FOCUSED: "lv.STATE.FOCUSED",
    lv.STATE.HOVERED: "lv.STATE.HOVERED",
    lv.STATE.PRESSED: "lv.STATE.PRESSED",
    lv.STATE.SCROLLED: "lv.STATE.SCROLLED",
    lv.STATE.USER_1: "lv.STATE.USER_1",
    lv.STATE.USER_2: "lv.STATE.USER_2",
    lv.STATE.USER_3: "lv.STATE.USER_3",
    lv.STATE.USER_4: "lv.STATE.USER_4",
}


def obj_states(obj):
    state_list = ""
    for state, description in state_dict.items():
        if obj.has_state(state):
            state_list += f"{description}, "
    print(f"{obj} has states: {state_list}")
