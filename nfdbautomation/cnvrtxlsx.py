import pandas as pd
import numpy as np


# Reading the csv file
df_new = pd.read_csv('result.csv',delimiter='@', skiprows=0, low_memory=False)

# saving xlsx file
GFG = pd.ExcelWriter('Reports.xlsx')
df_new.to_excel(GFG, index = False, header=None)

GFG.save()

