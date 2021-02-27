import random


class BagRandomizer:
    def __init__(self, items_num):
        self.current_item = 0
        self.items = [i for i in range(items_num)]
        random.shuffle(self.items)

    def get_number(self):
        if self.current_item == len(self.items):
            self.current_item = 0
            self.shuffle()

        item = self.items[self.current_item]
        self.current_item += 1
        return item

    def shuffle(self):
        random.shuffle(self.items)

    def reset(self):
        self.current_item = 0
        self.shuffle()
