# MIT License

# Copyright (c) 2023 Melo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# THE CODE BELOW WILL STILL BE ORGANIZED AND SEPARATED PROPERLY, SO DON'T JUDGE ME xD. Anyway, it's working 100%

define _sprite_images = []
default _sprite_saved_vars = {}

init -999 python:

    import ctypes
    import copy

init -998 python:

    def _isPathWithCompatibleFormat(path):
        format_list = [".png", ".webp"]
        for x in format_list:
            if path.endswith(x):
                return True
        return False

    def _imageObjects(image_name = None):
        response = {}
        for x in renpy.display.image.images:
            response[" ".join(x)] = renpy.display.image.images[x]
        if image_name is None:
            return response
        elif image_name in response:
            return response[image_name]
        return None

    class FolderSprite(LayeredImage):
        def __init__(self, folder_path, sort = [], attributes = [], sort_together = False, auto_attributes = False, *args, **kwargs):
            
            global _sprite_images
            _sprite_images.append(self)

            self._img_name = None

            if isinstance(sort, list) is False:
                sort = [ sort ] 
            sort.reverse()
            self._sort = sort
            if isinstance(attributes, list) is False:
                attributes = [ attributes ] 

            self._attributes_and_paths = {}
            self._attrs_to_save = ['_attrs_to_save']
            self._base_imgs = []
            self._folder_imgs = []
            kwargs_keys_to_be_deleted = []
            for path in renpy.list_files():
                if path.startswith(folder_path) and _isPathWithCompatibleFormat(path):
                    path_list = path.split("/")

                    current_transforms = {}
                    for key, value in kwargs.items():
                        for tkey, tvalue in renpy.atl.PROPERTIES.items():
                            if key.endswith("_"+tkey) and (key.startswith(path_list[-2]) or (key.startswith(path_list[-1].split(".")[0]) and path==folder_path+"/"+path_list[-1])):
                                if key==path_list[-2]+"_"+path_list[-1].split(".")[0]+"_"+tkey or key==path_list[-2]+"_"+tkey or key==path_list[-1].split(".")[0]+"_"+tkey:
                                    current_transforms[tkey] = value
                                    if key not in kwargs_keys_to_be_deleted:
                                        kwargs_keys_to_be_deleted.append(key)

                    if str("/".join(path_list[:-1]))==folder_path:
                        self._base_imgs.append([path_list[-1].split(".")[0], Transform(path, **current_transforms)])
                    else:
                        if path_list[-2] not in attributes and auto_attributes is False:
                            if hasattr(self, path_list[-2]) is False:
                                setattr(self, path_list[-2], kwargs[path_list[-2]] if path_list[-2] in kwargs else 'default') 
                                if path_list[-2] in kwargs:
                                    kwargs.pop(path_list[-2])
                                self._attrs_to_save.append(path_list[-2])
                            self._folder_imgs.append(
                                [path_list[-2], 
                                path_list[-1].split(".")[0],
                                ConditionSwitch(
                                    "_getSpriteSavedStateObj(ctypes.cast("+str(id(self))+", ctypes.py_object).value.getImageName()) is not None and _getSpriteSavedStateObj(ctypes.cast("+str(id(self))+", ctypes.py_object).value.getImageName())."+path_list[-2]+"=='"+path_list[-1].split(".")[0]+"'", 
                                    Transform(path, **current_transforms),
                                    "True", Null())])
                        else:
                            if auto_attributes and path_list[-2] not in attributes:
                                attributes.append(path_list[-2])
                            if path_list[-2] not in self._attributes_and_paths:
                                self._attributes_and_paths[path_list[-2]] = []
                            self._attributes_and_paths[path_list[-2]].append(Attribute(path_list[-2], path_list[-1].split(".")[0], path, True if path_list[-2] in kwargs and kwargs[path_list[-2]]==path_list[-1].split(".")[0] else path_list[-1].split(".")[0]=='default' and path_list[-2] not in kwargs, **current_transforms))
            
            for key in kwargs_keys_to_be_deleted:
                kwargs.pop(key)
            
            for x in attributes:
                if x in kwargs:
                    kwargs.pop(x)

            self._layered_img = []
            if sort_together:
                imgs_list = []

                imgs_list.extend(self._base_imgs)

                for x in self._folder_imgs:
                    imgs_list.append([x[0], x[2]])

                for key, value in self._attributes_and_paths.items():
                    for x in value:
                        imgs_list.append([key, x])

                new_imgs_list = []
                for x in imgs_list:
                    if x[0] not in sort:
                        new_imgs_list.append(x[1])
                for x in sort:
                    for y in imgs_list:
                        if y[0]==x:
                            new_imgs_list.append(y[1])
                
                self._layered_img = new_imgs_list
                
            else:
                self._attributes_imgs = []
                for key, value in self._attributes_and_paths.items():
                    if key not in sort:
                        for y in value:
                            self._attributes_imgs.append(y)
                for x in sort:
                    for key, value in self._attributes_and_paths.items():
                        if key==x:
                            for y in value:
                                self._attributes_imgs.append(y)


                _new_folder_imgs = []
                for x in self._folder_imgs:
                    if x[0] not in sort:
                        _new_folder_imgs.append(x)
                for x in sort:
                    for y in self._folder_imgs:
                        if y[0]==x:
                            _new_folder_imgs.append(y)
                self._folder_imgs = _new_folder_imgs

                _new_base_imgs = []
                for x in self._base_imgs:
                    if x[0] not in sort:
                        _new_base_imgs.append(x)
                for x in sort:
                    for y in self._base_imgs:
                        if y[0]==x:
                            _new_base_imgs.append(y)
                self._base_imgs = _new_base_imgs
                        
                for x in self._base_imgs:
                    self._layered_img.append(x[1])
                for x in self._folder_imgs:
                    self._layered_img.append(x[2])
                self._layered_img.extend(self._attributes_imgs)

            super().__init__(self._layered_img, *args, **kwargs)


        def getImageName(self):
            if self._img_name is None:
                for x in renpy.display.image.images:
                    if renpy.display.image.images[x] is self:
                        self._img_name = str(x).split("'")[1]
            return self._img_name

init 501 python:

    def _getSpriteSavedStateObj(sprite_name):
        if isinstance(sprite_name, str):
            if _getSpriteByName(sprite_name) is not None:
                global _sprite_saved_vars
                if sprite_name not in _sprite_saved_vars:
                    _sprite_saved_vars[sprite_name] = object()
                for x in _getSpriteByName(sprite_name)._attrs_to_save:
                    if hasattr(_sprite_saved_vars[sprite_name], x) is False:
                        setattr(_sprite_saved_vars[sprite_name], x, getattr(_getSpriteByName(sprite_name), x))
                for x in _sprite_saved_vars[sprite_name]._attrs_to_save:
                    if x not in _getSpriteByName(sprite_name)._attrs_to_save:
                        if hasattr(_sprite_saved_vars[sprite_name], x):
                            delattr(_sprite_saved_vars[sprite_name], x)
                return _sprite_saved_vars[sprite_name]
        return None

    def _getSpriteByName(name = None):
        if name is None:
            return _sprite_images
        for x in _sprite_images:
            if name==x.getImageName():
                return x
        return None

    def fsc(name):
        return _getSpriteSavedStateObj(name)
