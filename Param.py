''' Restructuring of the code in March 2025
    First use of a Parameter File 
    Masters thesis Laura Weghake 
    
    The following parameters are set by the file 
    'Load_profile_informations_csv.csv' match the individual optimisations:

    Sorting in the Categories used for Analysis: 
    Load Profile Catogory
    PV-System Category
    Battery-Capacity Category

    Parameter for the Optimisation:
    Number of the Load Profile
    Peak-Power of the PV-System
    Battery Capacity 
    PV Orientation (South/East&West)
    Battery Charging Power (usualy Capacity over an hour)
    Behaviour of the Optimisation (1-10)
    '''
# Convert to Datetime format
from datetime import datetime
import numpy as np


''' General Parameters '''
# Number of years considered
num_years = 1  # nessesary?

# Start Date - data collection
y_start = '2024'
m_start = '01'
d_start = '01'

# Stop Date - data collection
y_stop = '2025'
m_stop = '01'
d_stop = '01'

# Convert to Datetime format
start_date = datetime.fromisoformat(f'{y_start}-{m_start}-{d_start}')
stop_date = datetime.fromisoformat(f'{y_stop}-{m_stop}-{d_stop}')

# data types for numbers
datatype       = np.float32
str_datatype   = 'float32'


''' Parameter used in the Optimisation'''
# used datapath for the results and needed files
# have to include the 'Masterthesis' Folder with the Python Files
data_path = '' # "C:\\Users\\lwegh\\Documents\\Study\\MasterThesis"
# '..'

# Battery Costs per kWh (between 5 and 14 Cent/kWh)
battery_costs = 10 # Cent/kWh

# the power with which the household can get energy from the grid
grid_power = 11 * 5/60 # kW * 5/60 h 

# The time over how long an optimisation step should be calculated
# how long the optimisation should be able to take a prediction into account
optimise_time = 24 # h

# time duration of new calculation 
step_time = 18 # h

'''Year of installation of the pv system, nicht mehr benutzt'''
# derive the feed-in price 
# year_pv_installation  = 2024
# month_pv_installation = 12


''' Energy Price Parameter '''
# Variable costs of Tibber including:
# Netznutzung brutto, Konzessionsabg. brutto, Stromsteuer, Offshore, KWKG, NEV Umlage, Tibber Aufschlag
variable_costs = 11.88 + 1.571 + 2.05 + 0.816 + 0.277 + 1.558 + 2.15 

