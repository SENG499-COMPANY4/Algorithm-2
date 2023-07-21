import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from src.class_size_predictor import returnClassSize

f = json.load(open("test/data/one_class.json"))
print(f)
classes = 1
print(returnClassSize(f))

predicted = {5:91,9:159,1:353}

output = []
year = 2017
while len(f[0]["pastEnrollment"]) > 3:
    tmp = returnClassSize(f)
    avg = 0
    for x in tmp:
        avg += abs((predicted[x["term"]]*100/x["size"]))
        print(x)
        print(predicted[x["term"]])
    sz = len(f[0]["pastEnrollment"])
    f[0]["pastEnrollment"] = [yr for yr in f[0]["pastEnrollment"] if yr["year"] != year]
    output.insert(0,abs(avg/(sz-len(f[0]["pastEnrollment"])) -100))
    year +=1



x = np.arange(0, 6, 1)
y1 = output
print(y1)
plt.xlabel('Years of data') 
plt.ylabel('Average Percent Error')
plt.xticks(range(len(output)+1),labels=range(1, len(output)+2))
plt.plot(x, y1[::-1], linestyle='--', color='red')
plt.show()