define _sprite_images = []
default _sprite_saved_vars = {}

init -10 python:

    import ctypes

init 0 python:

    def _isPathWithCompatibleFormat(path):
        format_list = [".png", ".jpg", ".webp"]
        for x in format_list:
            if path.endswith(x):
                return True
        return False

    # _internal_file_path_var = ""
    # def _generateImageWithStyle(file_path):
    #     global _internal_file_path_var
    #     _internal_file_path_var = file_path
    #     params = _internal_file_path_var.split(".")[1:-1]
    #     file_format = _internal_file_path_var.split("/")[-1].split(".")[-1]
    #     file_name = _internal_file_path_var.split("/")[-1].split(".")[0]
    #     text = ""
    #     for x in params:
    #         if x.split("=")[0] in dir(Style):
    #             text += ", "+x.replace(",", ".")
    #     response = eval("Image(_internal_file_path_var"+text+")")
    #     return response

    # def load():
    #     for path in renpy.list_files():
    #         if path.startswith("images/") and _isPathWithCompatibleFormat(path):
    #             path_list = path.split("/")
    #             file_path = path
    #             img_name = path_list[-1].split(".")[0]
    #             renpy.image(img_name, _generateImageWithStyle(file_path))

    def _image_objects(image_name = None):
        response = {}
        for x in renpy.display.image.images:
            response[" ".join(x)] = renpy.display.image.images[x]
        if image_name is None:
            return response
        elif image_name in response:
            return response[image_name]
        return None

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

    def f(name = None):
        return _getSpriteSavedStateObj(name)

    class FolderSprite(LayeredImage):
        def __init__(self, folder_path, *args, **kwargs):

            # for directory in renpy.list_files():
            #     if directory.startswith(path):

            
            global _sprite_images
            _sprite_images.append(self)

            self._img_name = None

            self._attrs_to_save = ['_attrs_to_save']
            self._base_imgs = []
            self._folder_imgs = []
            for path in renpy.list_files():
                if path.startswith(folder_path) and _isPathWithCompatibleFormat(path):
                    path_list = path.split("/")
                    if str("/".join(path_list[:-1]))==folder_path:
                        self._base_imgs.append([path_list[-1].split(".")[0], Image(path)])
                    else:
                        if hasattr(self, path_list[-2]) is False:
                            setattr(self, path_list[-2], 'default') 
                            self._attrs_to_save.append(path_list[-2])
                        self._folder_imgs.append(
                            [path_list[-2], 
                            path_list[-1].split(".")[0],
                            ConditionSwitch(
                                "_getSpriteSavedStateObj(ctypes.cast("+str(id(self))+", ctypes.py_object).value.getImageName()) is not None and _getSpriteSavedStateObj(ctypes.cast("+str(id(self))+", ctypes.py_object).value.getImageName())."+path_list[-2]+"=='"+path_list[-1].split(".")[0]+"'", path,
                                "True", Null())])
            
            

            self._layered_img = []
            for x in self._base_imgs:
                self._layered_img.append(x[1])
            for x in self._folder_imgs:
                self._layered_img.append(x[2])

            super().__init__(self._layered_img, *args, **kwargs)


        def getImageName(self):
            if self._img_name is None:
                for x in renpy.display.image.images:
                    if renpy.display.image.images[x] is self:
                        self._img_name = str(x).split("'")[1]
            return self._img_name

image tester = FolderSprite(
    "images/linda")
    # go_foward = 
    # ["hair", "expression"], 
    # hair = "default")#Falta implementar suporte para a opção go_foward e para setar a iamgem default dos objetos

#     renpy.image("tester exp2", AutoLayeredImage([Image("images/01Linda_LindaBody02.png", xpos = -100), "images/01Linda_LindaFace03.png"]))
    
#     # renpy.image("tester", "images/Character/Linda/Images/01/01Linda_LindaBody07.png")
# image tester = LayeredImage([Image("images/01Linda_LindaFace03.png", xpos = -500)])
# image tester2 = LayeredImage([Image("images/01Linda_LindaFace04.png", xpos = -300)])
# image testagain fasgd gfgs = "gfgdfsg/sdgdgf.png"
# screen test:
#     imagebutton idle "defeat" hover "defeat" xpos -200 focus_mask True action NullAction()

#     global vartest
#     vartest = 1234
#     def funcaux(dad):
#         resp = []
#         for x in dir(Style):
#             resp.append(x)
#             exec("renpy.say(None, str(x), gdsfgd='gdfgsdgsd')")
#         return resp

# # image test3 = LayeredImage([ConditionSwitch(
# #         "False", "images/characters/petra/dress/main-crown.png",
# #         "True", Null()),])