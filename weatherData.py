import numpy as np
import pandas as pd

#Opening Weather Data File
with open('weather_data.dat', 'r') as data:
    lines = data.readlines()

#Read data
#Skip header, footer and any blank lines
raw_data = lines[4:-2]
del raw_data[1]

#Find common whitespace and convert them to split bars.
whitespace = np.all([[(c==' ' or c=='*') for c in line] for line in raw_data], axis=0)
raw_table = []
for line in raw_data:
    del_line = ''
    for i, c in enumerate(line):
        del_line += c if not whitespace[i] else '|'
    raw_table.append([val for val in del_line.split('|') if not val == ''])

#Remove whitespace
raw_table = [[ele.strip() for ele in row] for row in raw_table]

#Split remaining columns
_raw_table = []
for row in raw_table:
    _row = []
    for ele in row:
        if ele == '':
            _row.append('')
        else:
            _row.extend(ele.split())
    _raw_table.append(_row)

raw_table = raw_table

#Convert to DataFrame
data_frame_weather = pd.DataFrame(raw_table[1:])
data_frame_weather.columns = raw_table[0]

#Convert string columns to numeric values
cols = ['Dy', 'MxT', 'MnT', 'AvT', 'HDDay', 'AvDP', '1HrP', 'TPcpn', 'PDir',
        'AvSp', 'Dir', 'MxS', 'SkyC', 'MxR', 'MnR', 'AvSLP']
data_frame_weather[cols] = data_frame_weather[cols].apply(pd.to_numeric, errors='coerce')

#Add New Spread Column
data_frame_weather['SpT'] = data_frame_weather['MxT'] - data_frame_weather['MnT']
min_spt_row = data_frame_weather.iloc[data_frame_weather['SpT'].idxmin()][['Dy', 'SpT']]

#Output
print('Day {} had the minimum temperature spread of {} degrees for the month' .format(*min_spt_row.values))