# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

def add_children_to_group(cont, group):
    for idx in range(cont.get_child_cnt()):
        child = cont.get_child(idx)
        if child.has_flag(lv.obj.FLAG.CLICKABLE):
            group.add_obj(child)

def move_indevs(to_group, from_group=None, indevs=[]):
    if from_group:
        indev = lv.indev_t()
        while True:
            indev = indev.get_next()
            if not indev:
                break
            if indev.get_group() == from_group:
                indevs.append(indev)
    for indev in indevs:
        indev.set_group(to_group)
    return indevs

class IndevManager():
	"""
	im = IndevManager([enc1, enc2, keypad])
	im.remove(enc2)
	im.clear()
	im.add(enc3)
	im.push(group)
	im.pop()
	im.items[0]
	im.history[-1]
	im.clear_history()
	"""
	def __init__(self, indevs=None, default_group=lv.group_get_default()):
		self._indevs = []
		self._history = []
		self.default_group = default_group

		for indev in indevs:
			self.add(indev)

	def add(self, indev):
		self._indevs.append(indev)
	
	def remove(self, indev):
		if indev in self._indevs: self._indevs.remove(indev)

	def clear(self):
		self._indevs.clear()
		self._history.clear()

	def push(self, group):
		self._history.append(group)
		for indev in self._indevs:
			indev.wait_release()
			indev.set_group(group)

	def pop(self):
		if len(self._history):
			self._history.pop()
			self.peek()
		else:
			raise(IndexError("Already at the beginning of the list"))

	def peek(self):
		if len(self._history) > 0:
			group = self._history[-1]
		else:
			group = self.default_group

		for indev in self._indevs:
			indev.set_group(group)

	@property
	def indevs(self):
		return self._indevs

	@property
	def history(self):
		return self._history






