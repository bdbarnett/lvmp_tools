# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import gc


class Animation(lv.anim_t):
    """
    Usage:  anim=Animate(button, button.set_x, 50, 100, 500)

    path_cb options:
        lv.anim_t.path_linear: linear animation
        lv.anim_t.path_step: change in one step at the end
        lv.anim_t.path_ease_in: slow at the beginning
        lv.anim_t.path_ease_out: slow at the end
        lv.anim_t.path_ease_in_out: slow at the beginning and end
        lv.anim_t.path_overshoot: overshoot the end value
        lv.anim_t.path_bounce: bounce back a little from the end value

    """

    def __init__(
        self,
        var,
        custom_exec_cb,
        start,
        end,
        dur,
        del_anims=False,
        del_obj=False,
        delay=None,
        playback_time=None,
        playback_delay=None,
        repeat_cnt=None,
        repeat_delay=None,
        early_apply=None,
        get_value_cb=None,
        path_cb=None,
        start_cb=None,
        ready_cb=None,
        deleted_cb=None,
    ):
        super().__init__()
        self.init()

        if del_anims or del_obj:
            self.set_ready_cb(
                lambda a: self._delete(a, del_anims, var, del_obj, ready_cb)
            )
        elif ready_cb:
            self.set_ready_cb(ready_cb)

        # MANDATORY SETTINGS
        self.set_var(var)
        self.set_custom_exec_cb(custom_exec_cb)
        self.set_values(start, end)
        self.set_time(dur)

        # OPTIONAL SETTINGS
        if delay:
            self.set_delay(delay)
        if playback_time:
            self.set_playback_time(playback_time)
        if playback_delay:
            self.set_playback_delay(playback_delay)
        if repeat_cnt:
            self.set_repeat_count(repeat_cnt)
        if repeat_delay:
            self.set_repeat_delay(repeat_delay)
        if early_apply:
            self.set_early_apply(early_apply)

        # OPTIONAL CALLBACKS
        if get_value_cb:
            self.set_get_value_cb(get_value_cb)
        if path_cb:
            self.set_path_cb(path_cb)
        if start_cb:
            self.set_start_cb(start_cb)
        if ready_cb:
            self.set_ready_cb(ready_cb)
        if deleted_cb:
            self.set_deleted_cb(deleted_cb)

    def _delete(self, anim, del_anims, obj, del_obj, callback):
        if callback:
            callback(anim)
        if del_obj:
            obj.delete()
        if del_anims:
            lv.anim_del(anim, None)
        gc.collect()


def move_xy(obj, start_pos, dest_pos, dur=500, path_cb=None, ready_cb=None):
    x1, y1 = start_pos
    x2, y2 = dest_pos

    animate_x = Animation(
        obj, (lambda a, val: obj.set_x(val)), x1, x2, dur, path_cb=path_cb
    )
    animate_y = Animation(
        obj,
        (lambda a, val: obj.set_y(val)),
        y1,
        y2,
        dur,
        path_cb=path_cb,
        ready_cb=ready_cb,
    )
    animate_x.start()
    animate_y.start()


def spin_grow(obj, start_area, dest_area, shrink=False, dur=500, path_cb=None, del_obj=False):

    if shrink:
        zoom_start = lv.ZOOM_NONE
        zoom_end = 0
        start_x = start_area.x1
        start_y = start_area.y1
        dest_x = dest_area.x1 - ((start_area.get_width() - dest_area.get_width()) // 2)
        dest_y = dest_area.y1 - ((start_area.get_height() - dest_area.get_height()) // 2)
    else:
        zoom_start = 0
        zoom_end = lv.ZOOM_NONE
        start_x = start_area.x1 - ((dest_area.get_width() - start_area.get_width()) // 2)
        start_y = start_area.y1 - ((dest_area.get_height() - start_area.get_height()) // 2)
        dest_x = dest_area.x1
        dest_y = dest_area.y1

    animate_x = Animation(
        obj, (lambda a, val: obj.set_x(val)), start_x, dest_x, dur, path_cb=path_cb
    )
    animate_y = Animation(
        obj, (lambda a, val: obj.set_y(val)), start_y, dest_y, dur, path_cb=path_cb
    )
    animate_zoom = Animation(
        obj, (lambda a, val: obj.set_style_transform_zoom(val, 0)), zoom_start, zoom_end, dur, path_cb=path_cb,
    )
    animate_angle = Animation(
        obj, (lambda a, val: obj.set_style_transform_angle(val, 0)), 0, 3600, dur + 100, path_cb=path_cb, del_anims=True, del_obj=del_obj,
    )

    animate_x.start()
    animate_y.start()
    animate_zoom.start()
    animate_angle.start()
