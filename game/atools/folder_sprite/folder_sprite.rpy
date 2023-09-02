define _sprite_images = []
default _sprite_saved_vars = {}

init -999 python:

    import ctypes
    import copy

init -998 python:

    def _isPathWithCompatibleFormat(path):
        format_list = [".png", ".jpg", ".webp"]
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
        def __init__(self, folder_path, go_foward = [], attributes = [], *args, **kwargs):
            
            global _sprite_images
            _sprite_images.append(self)

            self._img_name = None

            if isinstance(go_foward, list) is False:
                go_foward = [ go_foward ] 
            go_foward.reverse()
            self._go_foward = go_foward
            if isinstance(attributes, list) is False:
                attributes = [ attributes ] 

            self._attributes_and_paths = {}
            self._attrs_to_save = ['_attrs_to_save']
            self._base_imgs = []
            self._folder_imgs = []
            for path in renpy.list_files():
                if path.startswith(folder_path) and _isPathWithCompatibleFormat(path):
                    path_list = path.split("/")
                    if str("/".join(path_list[:-1]))==folder_path:
                        self._base_imgs.append([path_list[-1].split(".")[0], Image(path)])
                    else:
                        if path_list[-2] not in attributes:
                            if hasattr(self, path_list[-2]) is False:
                                setattr(self, path_list[-2], 'default') 
                                self._attrs_to_save.append(path_list[-2])
                            self._folder_imgs.append(
                                [path_list[-2], 
                                path_list[-1].split(".")[0],
                                ConditionSwitch(
                                    "_getSpriteSavedStateObj(ctypes.cast("+str(id(self))+", ctypes.py_object).value.getImageName()) is not None and _getSpriteSavedStateObj(ctypes.cast("+str(id(self))+", ctypes.py_object).value.getImageName())."+path_list[-2]+"=='"+path_list[-1].split(".")[0]+"'", path,
                                    "True", Null())])
                        else:
                            if path_list[-2] not in self._attributes_and_paths:
                                self._attributes_and_paths[path_list[-2]] = []
                            self._attributes_and_paths[path_list[-2]].append(Attribute(path_list[-2], path_list[-1].split(".")[0], path, path_list[-1].split(".")[0]=='default'))

            self._attributes_imgs = []
            for key, value in self._attributes_and_paths.items():
                if key not in go_foward:
                    for y in value:
                        self._attributes_imgs.append(y)
            for x in go_foward:
                for key, value in self._attributes_and_paths.items():
                    if key==x:
                        for y in value:
                            self._attributes_imgs.append(y)


            _new_folder_imgs = []
            for x in self._folder_imgs:
                if x[0] not in go_foward:
                    _new_folder_imgs.append(x)
            for x in go_foward:
                for y in self._folder_imgs:
                    if y[0]==x:
                        _new_folder_imgs.append(y)
            self._folder_imgs = _new_folder_imgs

            _new_base_imgs = []
            for x in self._base_imgs:
                if x[0] not in go_foward:
                    _new_base_imgs.append(x)
            for x in go_foward:
                for y in self._base_imgs:
                    if y[0]==x:
                        _new_base_imgs.append(y)
            self._base_imgs = _new_base_imgs
                    

            self._layered_img = []
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

    def fsc(name = None):
        return _getSpriteSavedStateObj(name)

image tester = FolderSprite(
    "images/linda",
    xpos = 200,
    go_foward = 
    ["hair", "expression", "clothing"],
    attributes = ["expression"])
    # hair = "default",
    # hair_xpos = 100,
    # hair_default_xpos = -100,
    # ypos = -100)#Falta implementar suporte para a opção go_foward e para setar a iamgem default dos objetos
