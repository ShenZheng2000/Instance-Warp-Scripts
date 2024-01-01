
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
import datetime
import sys
from matplotlib.ticker import MultipleLocator

# TODO: put the font below the point

# Function to convert year-month to datetime
def convert_to_datetime(year, month):
    return datetime.datetime(year, month, 1)

# Modified data with month and year
scores = sys.argv[1]

if scores == 'mAP50':
    data = {
        'UMT': (36.2, convert_to_datetime(2021, 3)),  # CVPR 2021 (Date: Mar 2020)
        'TDD': (34.6, convert_to_datetime(2022, 5)),  # CVPR 2022 (Date: May 2022)
        'AT': (38.5, convert_to_datetime(2022, 11)),   # CVPR 2022 (Date: Nov 2021)
        '2PCNet': (46.7, convert_to_datetime(2023, 3)), # CVPR 2023 (Date: Mar 2023)
        'Ours': (50.1, convert_to_datetime(2023, 11))  # Date: Nov 2023
    }
    YLIM = [32, 51]
    XLIM = [datetime.datetime(2020, 11, 1), datetime.datetime(2024, 3, 1)]

elif scores == 'mIoU':
    data = {
    'DACS': (41.2, convert_to_datetime(2020, 7)), # CVPR 2020 (Date: Apr 2020)
    'MGCDA': (48.7, convert_to_datetime(2020, 5)), # TPAMI 2020 (Date: May 2020)
    'DANNet': (50.0, convert_to_datetime(2021, 4)), # CVPR 2021 (Date: Apr 2021)
    'DAFormer': (57.6, convert_to_datetime(2022, 3)), # CVPR 2022 (Date: Mar 2022)
    'Ours': (61.8, convert_to_datetime(2023, 11)) # Date: Nov 2023
    }
    YLIM = [38, 63]
    XLIM = [datetime.datetime(2019, 12, 1), datetime.datetime(2024, 3, 1)]

else:
    data = {}

# Splitting the data into separate lists for plotting
models = list(data.keys())
values = [val[0] for val in data.values()]
dates = [val[1] for val in data.values()]

# Define custom colors and point shapes
colors = ["#ff7f00", "#984ea3", "#4daf4a", "#377eb8", "#e41a1c"]
point_shapes = ["^", "s", "p", "o", "*"]

# Plotting the data with custom colors and point shapes
plt.figure(figsize=(10, 8))
for i, (model, value, date) in enumerate(zip(models, values, dates)):
    plt.scatter(date, value, s=500, color=colors[i], marker=point_shapes[i])  # Increased scatter point size
    # Adjust y-offset to lower the text annotation below the scatter point
    text_y_offset = value - (max(values) - min(values)) * 0.05  # 5% of the value range for offset
    plt.text(date, text_y_offset, model, fontsize=30, ha='center', va='top',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2')
             )  # Adjuste

# Explicitly set the x and y axis limits
plt.xlim(XLIM)  # Hardcoded x-axis range
plt.ylim(YLIM)  # Hardcoded y-axis range

# Add padding around the plot for the text annotations
plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)

# Format the date on x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Show only the year
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

# Set y-axis ticks at intervals of 5
plt.gca().yaxis.set_major_locator(MultipleLocator(5))

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)

plt.xlabel('Date of Publication', fontsize=35)
plt.ylabel(f'{scores}', fontsize=35)
plt.tight_layout()
plt.grid(True)
# plt.savefig(f'{scores}.png')
plt.savefig(f'{scores}.pdf')
# plt.show()














# import matplotlib.pyplot as plt
# from matplotlib.ticker import MaxNLocator
# import sys

# # use year-month format,
# # remove legend, and move method name near points
# # Maybe: use same points and color for some methods

# scores = sys.argv[1]

# if scores == 'mAP50':

#     # Provided data for AP50 values with different methods and their publication years
#     data = {
#         'UMT': (36.2, 2021),  # CVPR 2021 (Date: Mar 2020)
#         'TDD': (34.6, 2022),  # CVPR 2022 (Date: May 2022)
#         'AT': (38.5, 2022),   # CVPR 2022 (Date: Nov 2021)
#         '2PCNet': (46.7, 2023), # CVPR 2023 (Date: Mar 2023)
#         'Ours': (50.1, 2024)  # Date: Nov 2023
#     }

# elif scores == 'mIoU':
#     data = {
#     'FDA': (45.7, 2020), # CVPR 2020 (Date: Apr 2020)
#     'MGCDA': (48.7, 2020), # TPAMI 2020  (Date: May 2020)
#     'DANNet': (50.0, 2021), # CVPR 2021  (Date: Apr 2021)
#     'DAFormer': (57.6, 2022), # CVPR 2022  (Date: Mar 2022)
#     'Our': (61.8, 2024) # Date: Nov 2023
#     }

# else:
#     data = {
#     }


# # Splitting the data into separate lists for plotting
# models = list(data.keys())
# values = [val[0] for val in data.values()]
# years = [val[1] for val in data.values()]

# # Define custom colors and point shapes
# colors = ["#ff7f00", "#984ea3", "#4daf4a", "#377eb8", "#e41a1c"]
# point_shapes = ["^", "s", "p", "o", "*"]

# # Plotting the data with custom colors and point shapes
# plt.figure(figsize=(10, 8))
# for i, (model, value, year) in enumerate(zip(models, values, years)):
#     plt.scatter(year, value, label=model, s=1300, color=colors[i], marker=point_shapes[i])

# # Setting the size of the legend
# plt.legend(prop={'size': 30},
#            loc = 'best'
#         #    loc='lower right'
#            )

# # Adjusting the x-axis to show only integer year values
# plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# plt.xticks(fontsize=25)
# plt.yticks(fontsize=25)

# plt.xlabel('Year', fontsize=35)
# plt.ylabel(f'{scores}', fontsize=35)
# plt.tight_layout()
# plt.savefig(f'{scores}.png')  # Uncomment this line to save the figure as a file
# # plt.savefig(f'{scores}.pdf')  # Uncomment this line to save the figure as a file
# # plt.show()
