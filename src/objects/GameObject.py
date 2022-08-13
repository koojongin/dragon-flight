from pygame.surface import Surface


class GameObject:

    def __init__(self):
        self.image: Surface = None
        self.position: tuple[int | float, int | float] = None
        self.is_destroyed = False

    def get_size(self):
        if self.image is None:
            raise Exception("self.image not defined")

        if self.position is None:
            raise Exception("self.image not defined")

        return self.image.get_size()

    def destroy(self):
        self.is_destroyed = True
