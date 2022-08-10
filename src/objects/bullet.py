from src.objects.util import calculate_distance_dot


class Bullet:
    def __init__(self, image, position=(0, 0), speed=0.2):
        self.image = image
        self.x = position[0]
        self.y = position[1]

        self.x = 0
        self.y = 0
        self.speed = speed
        self.destination = (0, 0)
        self.departure = (0, 0)
        self.is_destroy = False

    def destroy(self):
        self.is_destroy = True

    def update(self, scene, delta_time):
        is_close = False
        if (
                calculate_distance_dot(self.x, self.destination[0] + 800) <= 5
                and calculate_distance_dot(self.y, self.destination[1] + 800) <= 5
        ):
            is_close = True
            self.destroy()

        if is_close is False:
            distance_x = calculate_distance_dot(self.destination[0], self.departure[0])
            distance_y = calculate_distance_dot(self.destination[1], self.departure[1])

            sdt = self.speed * delta_time
            direction_x = 1
            direction_y = 1
            if self.departure[0] > self.destination[0]:
                direction_x = -1

            if self.departure[1] > self.destination[1]:
                direction_y = -1

            if distance_y >= distance_x:
                self.x += sdt * direction_x * (distance_x / distance_y)
                self.y += sdt * direction_y

            if distance_y < distance_x:
                self.x += sdt * direction_x
                self.y += sdt * direction_y * (distance_y / distance_x)
