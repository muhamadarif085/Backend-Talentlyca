import os
import sys
from prediction import downloadFile, predict

filename = sys.argv[1]

filepath = downloadFile(filename)


print(predict(filepath))
