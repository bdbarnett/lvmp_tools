# SPDX-FileCopyrightText: 2023 Brad Barnett
#
# SPDX-License-Identifier: MIT

import lvgl as lv

def load_img(filename):
    try:
        with open(filename,"rb") as f:
            img_data = f.read()
        img = lv.img_dsc_t({'data_size': len(img_data), 'data': img_data})
    except:
        # print(f"Error loading {filename}")
        img = lv.SYMBOL.WARNING
    return img

class ImageCache():

    def __init__(self, prefix=""):
        self._prefix = prefix
        self._img_cache = {}

    def img(self, filename):
        full_name = self._prefix + filename

        if full_name not in self._img_cache.keys():
            # print(f"ImageCache:  Adding {full_name} to image cache")
            self._img_cache[full_name] = load_img(full_name)
        # else: print(f"ImageCache:  Cache hit -> {full_name}")

        return self._img_cache[full_name]
    
    def preload(self, img_list):
        for filename in img_list:
            self.img(filename)

    def clear(self):
        self._img_cache = {}

    def change_prefix(self, new_prefix):
        self._prefix = new_prefix

    def contents(self):
        return self._img_cache.keys()
