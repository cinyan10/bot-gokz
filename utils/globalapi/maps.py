
class Maps:
    def __init__(self, mode='kz_timer'):
        if mode == 'kz_timer':
            self.tier = [933, 121, 272, 239, 150, 65, 63, 23]
        elif mode == 'kz_simple':
            self.tier = [917, 122, 272, 235, 142, 64, 60, 22]
        else:
            self.tier = [524, 122, 242, 133, 22, 3, 1, 1]
