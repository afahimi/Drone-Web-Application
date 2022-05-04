import glob 
import re

largest = 0
numlist = glob.glob('./images/*.png')
for string in numlist:
    new = int(re.search(r'\d+', string).group())
    if new > largest:
        largest = new
print(largest)
