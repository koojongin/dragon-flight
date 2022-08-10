class IApplication:
    current_scene = None

    def run(self):
        pass

    def next_scene(self):
        pass

    def load_scenes(self):
        pass

    def load_images(self):
        pass

    def load_audios(self):
        pass

    def set_scene(self, index):
        pass

    def get_width_by_height(self, height, image):
        pass

    def get_height_by_width(self, width, image):
        pass
