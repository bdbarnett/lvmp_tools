# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import math
from .misc import add_btn


class RoundView(lv.obj):
    def __init__(self, parent, num_items, zoomed=False):
        super().__init__(parent)

        self.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.set_style_bg_opa(lv.OPA._0, 0)
        self.set_style_pad_all(0, 0)
        self.set_size(lv.pct(100), lv.pct(100))
        self.center()
        self.update_layout()
        diam = min([self.get_content_width(), self.get_content_height()])
        
        self.num_items = num_items

        if zoomed:
            circum_rad, child_diam, cont_diam = self.calc_sizes_zoomed(diam, max([4, num_items]), diam / 30)
            self.set_size(cont_diam, cont_diam) # Resize to zoomed size
            self.align(lv.ALIGN.TOP_LEFT, 0, 0)
            self.update_layout()
            parent.scroll_to((self.get_width() - child_diam) // 2, 0, lv.ANIM.ON)
        else:
            circum_rad, child_diam, cont_diam = self.calc_sizes(diam, max([4, num_items]), diam / 30)
        self.child_size = (child_diam, child_diam)

        self._child_positions = []
        x_offset = (self.get_width() - child_diam) // 2
        y_offset = (self.get_height() - child_diam) // 2
        for i in range(num_items):
            theta = (i * 2 * math.pi / num_items) - (math.pi / 2)
            x = int(circum_rad * math.cos(theta))
            y = int(circum_rad * math.sin(theta))
            x += x_offset
            y += y_offset
            self._child_positions.append((lv.ALIGN.TOP_LEFT, x, y))
        self._next_child_pos = 0

        # set_focus_cb(group, self, zoomed=zoomed, rotate=rotate, scroll_gp=True, exclude=[parent.back_btn])


    def add_btn(self, icon, text):
        btn = add_btn(self, icon, text, self.child_size, self._child_positions[self._next_child_pos])
        self._next_child_pos = (self._next_child_pos + 1) % self.num_items
        return btn

    def get_next_child_align(self):
        align = self._child_positions[self._next_child_pos]
        self._next_child_pos = (self._next_child_pos + 1) % self.num_items
        return align

    def calc_sizes(self, cont_diam, divs, btn_pad):
        child_diam_plus_pad = (2 * math.sin(math.pi / divs) * (cont_diam / 2) / (1 + math.sin(math.pi / divs)))
        circum_rad = (cont_diam / 2) - (child_diam_plus_pad / 2)
        child_diam = int(child_diam_plus_pad - btn_pad + 0.5)  # add .5 to round
        return circum_rad, child_diam, cont_diam

    def calc_sizes_zoomed(self, child_diam_plus_pad, divs, btn_pad):
        circum_rad = (child_diam_plus_pad) / (2 * math.sin(math.pi / divs))
        cont_diam = int(((child_diam_plus_pad) / 2 + circum_rad) * 2)
        child_diam = int(child_diam_plus_pad - btn_pad + 0.5)
        return circum_rad, child_diam, cont_diam


class FlexFlowView(lv.obj):
    def __init__(self, parent, flex_flow=lv.FLEX_FLOW.ROW):
        super().__init__(parent)

        self.clear_flag(lv.obj.FLAG.CLICKABLE)
        self.set_flex_flow(flex_flow)
        self.add_flag(lv.obj.FLAG.SCROLLABLE)
        self.set_style_bg_opa(lv.OPA._0, 0)
        self.set_style_pad_all(0, 0)
        self.set_size(lv.pct(100), lv.pct(100))
        self.center()
        self.update_layout()
