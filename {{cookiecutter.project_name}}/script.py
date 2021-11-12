import pandas as pd
import numpy as np
# import colorcet as cc
import xarray
import time

print('Yes, it worked')

results = [1, 2, 3, 4]
np.savetxt('res/results.txt', results)
print('Sleeping for 60 seconds')
time.sleep(60)
print('Done!')
