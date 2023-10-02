# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

palette_list = {
    lv.PALETTE.AMBER: "lv.PALETTE.AMBER",
    lv.PALETTE.BLUE: "lv.PALETTE.BLUE",
    lv.PALETTE.BLUE_GREY: "lv.PALETTE.BLUE_GREY",
    lv.PALETTE.BROWN: "lv.PALETTE.BROWN",
    lv.PALETTE.CYAN: "lv.PALETTE.CYAN",
    lv.PALETTE.DEEP_ORANGE: "lv.PALETTE.DEEP_ORANGE",
    lv.PALETTE.DEEP_PURPLE: "lv.PALETTE.DEEP_PURPLE",
    lv.PALETTE.GREEN: "lv.PALETTE.GREEN",
    lv.PALETTE.GREY: "lv.PALETTE.GREY",
    lv.PALETTE.INDIGO: "lv.PALETTE.INDIGO",
    lv.PALETTE.LIGHT_BLUE: "lv.PALETTE.LIGHT_BLUE",
    lv.PALETTE.LIGHT_GREEN: "lv.PALETTE.LIGHT_GREEN",
    lv.PALETTE.LIME: "lv.PALETTE.LIME",
    lv.PALETTE.NONE: "lv.PALETTE.NONE",
    lv.PALETTE.ORANGE: "lv.PALETTE.ORANGE",
    lv.PALETTE.PINK: "lv.PALETTE.PINK",
    lv.PALETTE.PURPLE: "lv.PALETTE.PURPLE",
    lv.PALETTE.RED: "lv.PALETTE.RED",
    lv.PALETTE.TEAL: "lv.PALETTE.TEAL",
    lv.PALETTE.YELLOW: "lv.PALETTE.YELLOW",
}

color_props = [
    "set_style_bg_color",
    "set_style_bg_grad_color",
    "set_style_border_color",
    "set_style_outline_color",
    "set_style_shadow_color",
    "set_style_text_color",
    "set_style_arc_color",
    "set_style_line_color",
]


class ColorTester(lv.obj):
    def __init__(self, parent=None, host_obj=lv.scr_act()):
        if parent == None:
            from .sdl_disp import sdl_display

            disp, group = sdl_display(320, 960, "Color Tester")
            parent = disp.get_scr_act()

        super().__init__(parent)
        from .states import state_dict
        from .parts import parts_list

        self.set_size(lv.pct(100), lv.pct(100))

        self.group = group

        self.host_obj = host_obj
        self.target_group = None
        self.target_obj = None
        self.grad_dir = 0

        self.set_flex_flow(lv.FLEX_FLOW.COLUMN)

        self.obj_label = lv.label(self)
        self.obj_label.set_width(lv.pct(100))

        self.btnmatrix = lv.btnmatrix(self)
        self.btnmatrix.set_map(["Focused", "Parent", "GParent", ""])
        self.btnmatrix.set_size(lv.pct(100), lv.pct(7))
        self.btnmatrix.set_one_checked(True)
        self.btnmatrix.set_ctrl_map([1 | lv.btnmatrix.CTRL.CHECKABLE] * 3)
        self.btnmatrix.set_selected_btn(0)
        self.btnmatrix.add_event(self.get_target_obj, lv.EVENT.VALUE_CHANGED, None)
        self.group.add_obj(self.btnmatrix)

        self.state_selector = lv.dropdown(self)
        self.state_selector.set_width(lv.pct(100))
        self.state_selector.clear_options()
        self.group.add_obj(self.state_selector)

        self.states = {}
        for idx, (state, text) in enumerate(state_dict.items()):
            self.state_selector.add_option(text, idx)
            self.states[idx] = state

        self.part_selector = lv.dropdown(self)
        self.part_selector.set_width(lv.pct(100))
        self.part_selector.clear_options()
        self.group.add_obj(self.part_selector)

        self.parts = {}
        for idx, (part, text) in enumerate(parts_list.items()):
            self.part_selector.add_option(text, idx)
            self.parts[idx] = part

        top_cont = lv.obj(self)
        top_cont.set_size(lv.pct(100), lv.pct(37))
        top_cont.set_flex_flow(lv.FLEX_FLOW.COLUMN)

        self.property_selector = lv.dropdown(top_cont)
        self.property_selector.set_width(lv.pct(100))
        self.property_selector.clear_options()
        self.group.add_obj(self.property_selector)

        self.properties = {}
        for idx, property in enumerate(color_properties):
            self.property_selector.add_option(property, idx)
            self.properties[idx] = property

        self.color_list = lv.list(top_cont)
        self.color_list.set_size(lv.pct(100), lv.pct(83))
        self.group.add_obj(self.color_list)

        for color, text in palette_list.items():
            self.add_btn(color, text)

        bottom_cont = lv.obj(self)
        bottom_cont.set_size(lv.pct(100), lv.pct(41))
        bottom_cont.set_flex_flow(lv.FLEX_FLOW.COLUMN)

        border_label = lv.label(bottom_cont)
        border_label.set_width(lv.pct(100))
        border_label.set_text("Border")

        self.border_slider = lv.slider(bottom_cont)
        self.border_slider.set_width(lv.pct(100))
        self.border_slider.set_range(0, 9)
        self.group.add_obj(self.border_slider)

        outline_label = lv.label(bottom_cont)
        outline_label.set_width(lv.pct(100))
        outline_label.set_text("Outline")

        self.outline_slider = lv.slider(bottom_cont)
        self.outline_slider.set_width(lv.pct(100))
        self.outline_slider.set_range(0, 9)
        self.group.add_obj(self.outline_slider)

        shadow_label = lv.label(bottom_cont)
        shadow_label.set_width(lv.pct(100))
        shadow_label.set_text("Shadow")

        self.shadow_slider = lv.slider(bottom_cont)
        self.shadow_slider.set_width(lv.pct(100))
        self.shadow_slider.set_range(0, 19)
        self.group.add_obj(self.shadow_slider)

        offset_label = lv.label(bottom_cont)
        offset_label.set_width(lv.pct(100))
        offset_label.set_text("Shadow offset")

        self.offset_slider = lv.slider(bottom_cont)
        self.offset_slider.set_width(lv.pct(100))
        self.offset_slider.set_range(0, 19)
        self.group.add_obj(self.offset_slider)

        gradient_label = lv.label(bottom_cont)
        gradient_label.set_width(lv.pct(100))
        gradient_label.set_text("Gradient Direction")

        self.gradient_selector = lv.btnmatrix(bottom_cont)
        self.gradient_selector.set_map(["None", "Ver", "Hor", ""])
        self.gradient_selector.set_size(lv.pct(100), lv.pct(20))
        self.gradient_selector.set_one_checked(True)
        self.gradient_selector.set_ctrl_map([1 | lv.btnmatrix.CTRL.CHECKABLE] * 3)
        self.gradient_selector.add_event(
            self.set_grad_dir, lv.EVENT.VALUE_CHANGED, None
        )
        self.group.add_obj(self.gradient_selector)

        apply_btn = lv.btn(bottom_cont)
        apply_btn.set_width(lv.pct(100))
        apply_btn.add_event(self.set_target_options, lv.EVENT.SHORT_CLICKED, None)
        apply_label = lv.label(apply_btn)
        apply_label.set_text("Apply")
        apply_label.align(lv.ALIGN.CENTER, 0, 0)
        self.group.add_obj(apply_btn)

        self.host_obj.add_event(self.get_target_group, lv.EVENT.CHILD_CHANGED, None)
        self.get_target_group(None)

    def get_target_group(self, event):
        if self.target_group != lv.group_get_default():
            self.target_group = lv.group_get_default()
            self.target_group.set_focus_cb(self.get_target_obj)
            self.get_target_obj()

    def get_target_obj(self, evt=None):
        if self.target_group is None:
            return
        target = self.target_group.get_focused()
        id = self.btnmatrix.get_selected_btn()
        txt = self.btnmatrix.get_btn_text(id)
        if txt == "Parent":
            target = target.get_parent()
        if txt == "GParent" and target is not None:
            target = target.get_parent()
        self.target_obj = target
        self.obj_label.set_text(f"{txt} Object type: {type(self.target_obj)}")

    def add_btn(self, color, text):
        btn = self.color_list.add_btn(None, text)
        btn.set_style_bg_color(lv.palette_main(color), lv.STATE.DEFAULT)
        btn.add_event(
            lambda e: self.set_target_color(color), lv.EVENT.SHORT_CLICKED, None
        )
        self.group.add_obj(btn)

    def set_grad_dir(self, evt):
        self.grad_dir = evt.get_target_obj().get_selected_btn()

    def set_target_color(self, color):
        property = self.properties[self.property_selector.get_selected()]
        if not hasattr(self.target_obj, property):
            return
        parent = self.target_obj.get_parent()
        params = (
            self.states[self.state_selector.get_selected()]
            | self.parts[self.part_selector.get_selected()]
        )
        if parent is not None:
            siblings = parent.get_child_cnt()
            for idx in range(siblings):
                child = parent.get_child(idx)
                if type(child) == type(self.target_obj):
                    func = getattr(child, property)
                    func(lv.palette_main(color), params)
        else:
            func = getattr(self.target_obj, property)
            func(lv.palette_main(color), params)

    def set_target_options(self, event=None):
        if self.target_obj is None:
            return
        parent = self.target_obj.get_parent()
        params = (
            self.states[self.state_selector.get_selected()]
            | self.parts[self.part_selector.get_selected()]
        )
        if parent is not None:
            siblings = parent.get_child_cnt()
            for idx in range(siblings):
                child = parent.get_child(idx)
                if type(child) == type(self.target_obj):
                    child.set_style_border_width(self.border_slider.get_value(), params)
                    child.set_style_outline_width(
                        self.outline_slider.get_value(), params
                    )
                    child.set_style_shadow_width(self.shadow_slider.get_value(), params)
                    child.set_style_shadow_ofs_y(self.offset_slider.get_value(), params)
                    child.set_style_bg_grad_dir(self.grad_dir, params)
        else:
            self.target_obj.set_style_border_width(
                self.border_slider.get_value(), params
            )
            self.target_obj.set_style_outline_width(
                self.outline_slider.get_value(), params
            )
            self.target_obj.set_style_shadow_width(
                self.shadow_slider.get_value(), params
            )
            self.target_obj.set_style_shadow_ofs_y(
                self.offset_slider.get_value(), params
            )
            self.target_obj.set_style_bg_grad_dir(self.grad_dir, params)
