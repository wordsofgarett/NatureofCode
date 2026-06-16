import numpy as np
import random

import noise


print(round(np.random.normal(0, 3, 1)[0]))

print(random.random())

r = [0,10]
print(r[0] + (noise.pnoise1(100)*(r[1]-r[0])))

for i in range(100, 110):
    x = r[0] + ((noise.pnoise1(i)-(-1))/2)*(r[1]-r[0])
    print(x)