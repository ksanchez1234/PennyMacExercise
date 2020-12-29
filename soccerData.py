import numpy as np
import pandas as pd

from IPython.display import display

#Opening Soccer Data File
with open('soccer_data.dat', 'r') as data:
    lines = data.readlines()

#Read data
#Skip header, footer and any blank lines
raw_data = lines[3:24]
del raw_data[17]

#Find common whitespace and convert them to split bars.
whitespace = np.all([[(c in [' ', '-', '.']) for c in line] for line in raw_data], axis=0)
raw_table = []
for line in raw_data:
    del_line = ''
    for i, c in enumerate(line):
        del_line += c if not whitespace[i] else '|'
    raw_table.append([val for val in del_line.split('|') if not val == ''])

#Remove whitespace
raw_table = [[ele.strip() for ele in row] for row in raw_table]

#Convert to DataFrame
data_frame_soccer = pd.DataFrame(raw_table)
data_frame_soccer.columns = ['ID', 'Team', 'P', 'W', 'L', 'D', 'F', 'A', 'Pts']

#Convert string columns to numeric values
cols = ['P', 'W', 'L', 'D', 'F', 'A', 'Pts']
data_frame_soccer[cols] = data_frame_soccer[cols].apply(pd.to_numeric, errors='coerce')

#Add New Spread Column
data_frame_soccer['FADiff'] = np.abs(data_frame_soccer['F'] - data_frame_soccer['A'])
min_diff_row = data_frame_soccer.iloc[data_frame_soccer['FADiff'].idxmin()][['Team', 'FADiff']]

#Output
print('Team {} had the minimum spread of {} points for the English Premier League' .format(*min_diff_row.values))







