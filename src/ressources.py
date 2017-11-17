import pygame as pg
import pickle


def load_image(name, dim=None):
    try:
        image = pg.image.load("../ressources/" + name)
        if dim is not None:
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


def load_options():
    try:
        return pickle.load(open("options_file.data", "rb"))
    except FileNotFoundError:
        return {"CHARACTER": "mario",
                "DIFFICULTY": "normal",
                "NUMBER_OF_PLAYER": 1
         }
