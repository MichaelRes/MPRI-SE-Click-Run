import pygame


def load_image(name):
    try:
        image = pygame.image.load("../ressources/"+name)
    except:
        print("Ressource manquante : ",name)
        image=pygame.Surface((20,20))
        image=image.convert()
        image.fill((10,10,10))
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image
