import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", palette='pastel', color_codes=True) 
sns.mpl.rc('figure', figsize=(10,6))

# opening the vector 
mapshp_path = "\\District_Boundary.shp" # reading the shape file by using reader function of the shape 
shp_path = ''
libsf = shp.Reader(shp_path)

# t = len(sf.shapes())
# sf.records()