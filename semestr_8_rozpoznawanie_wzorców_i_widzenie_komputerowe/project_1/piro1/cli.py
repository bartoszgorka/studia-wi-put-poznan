import os.path
import sys

from .matcher import Matcher


class CLI:
    def __init__(self, root_path=sys.argv[1], num_images=sys.argv[2]):
        self.root_path = root_path
        self.num_images = int(num_images)

    def start(self):
        filenames = [os.path.join(self.root_path, "{}.png".format(i)) for i in range(self.num_images)]
        matcher = Matcher(filenames)
        matcher.match()
        for row in matcher.best_matches():
            print(' '.join(str(j) for j in row))
