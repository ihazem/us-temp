# Code to chart Air Temperature (Yearly Average) in USA from 1900 to 2017. Values are mean (average) in degrees Celsius
#
# Dataset Citation: Goodman, S., BenYishay, A., Lv, Z., & Runfola, D. (2019). GeoQuery: Integrating HPC systems and public web-based geospatial data tools. Computers & Geosciences, 122, 103-112.
# Metadata:
#	Boundary: United States ADM1 - GeoBoundaries v1.3.3

import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import re

# Define vars
markers = ["o", "D", "P", "^", "<", ">", "s", "v", "p", "X"]
# Read in air temp data in US from 1900 to 2017, along with 2020 population data
temps = pd.read_csv("air-temps.csv")
popul = pd.read_csv("population.csv")

# Set NAME (state) as index for both dataframes
temps = temps.set_index('NAME').reset_index()
popul = popul.set_index('NAME').reset_index()

# Merge (join) the two dataframes on the NAME index and keep the state population column (gpw_v4_count.2020.sum) from population.csv
temps = pd.merge(temps,popul[["NAME","gpw_v4_count.2020.sum"]],on="NAME",how="left")

## Cleanup data ##
# Remove unnecessary columns from data
temps = temps.drop(['Level','adm_int','feature_id','iso','ISO_Code','gqid','asdf_id','adm','gbid'], axis=1)
# Rename columns to only have YYYY
temps = temps.rename(columns=lambda x: re.sub('udel_air_temp_v501_mean.','',x))
temps = temps.rename(columns=lambda x: re.sub('.mean','',x))

# Sort by population to get the top 10 most populated states, then drop population data
temps = temps.sort_values(by=['gpw_v4_count.2020.sum'], ascending=False).head(10).drop(['gpw_v4_count.2020.sum'], axis=1)

# Transpose dataframe to chart it properly and then keep only the last 25 years worth of temperature data, and reset index to NAME again
temps = temps.set_index('NAME')
temps = temps.T
temps = temps.iloc[-25:]
# Print for debugging after cleanup
print(temps)

sns.lineplot(data=temps, dashes=False, markers = markers, palette="deep")
plt.legend(loc='upper right', bbox_to_anchor=(.63, .5, 0.5, 0.5), ncol=1)
plt.title('USA Mean Temperature 1993-2017, of 10 Most Populous States', fontsize=15)
plt.xlabel('Year')
plt.ylabel('Degrees (in Celsius)')
plt.show()

