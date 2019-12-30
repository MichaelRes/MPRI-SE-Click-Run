import pygame as pg


def load_image(name, dim = None):
    try:
        image = pg.image.load("../ressources/" + name)
        if dim != None:
            image = pg.transform.scale(image, dim)
    except pg.error:
        print("Ressource manquante : ", name)
        image = pg.Surface((20, 20))
        image = image.convert()
        image.fill((10, 10, 10))
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image
