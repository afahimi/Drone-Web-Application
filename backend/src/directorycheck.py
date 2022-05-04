import glob
import re


class DirectoryCheck:
    def __init__(self):
        self.largest = 0
    def updateLargest(self):
        newscan = glob.glob('../../frontend/public/fetched-images/*.jpg')
        for string in newscan:
            new = int(re.search(r'\d+', string).group())
            if new > self.largest:
                self.largest = new
        print(self.largest)