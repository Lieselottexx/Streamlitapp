# Import Bibs
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np
# Import Python Files
import Param


class PriceGenerator():

    def __init__(self):
        # Name for the protocol of the current calculation, log file
        self.log_file_name = "log.txt"
        # loading the current related data path out of the Param.py file
        self.data_path = Param.data_path
        self.datatype       = Param.datatype        # minimum 32 please 
        self.str_datatype   = Param.str_datatype    # minimum 32 please
        pass


    def __del__(self):
        pass

    def calculate_energy_prices(self, data, averageEnergyHousehold, StbVE): 
        # Calculation of dynamic prices 
        data = self.dynamic_pricing(data)
        # Calculation of static prices
        data = self.static_pricing(data, averageEnergyHousehold)
        # data.to_csv(os.path.join(self.data_path, self.optimisation_input_file_name), sep=';')  
        if StbVE == 1:
            data = self.time_variable_Netzentgelte(data)
        else:
            pass
        print(data)
        with open(os.path.join(self.data_path, self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nSaved the data DataFrame to CSV as opti_input!\n\n'))
        return data
    
    def dynamic_pricing(self, data):
        # Netznutzung brutto, Konzessionsabg. brutto, Stromsteuer, Offshore, KWKG, NEV Umlage, Tibber Aufschlag
        dym_variable_costs = Param.variable_costs
        # Fixed costs are taken out 
        data['Dynamic Electricity Price [Cent/kWh]'] = pd.Series(dtype=self.datatype)

        data['Dynamic Electricity Price [Cent/kWh]'] =  ( data['Energy Price [Cent/kWh]'] 
                                                        + data['Energy Price [Cent/kWh]'] * 0.19 
                                                        + dym_variable_costs ).astype(self.str_datatype)

        with open(os.path.join(self.data_path,self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nLoaded the dynamic energy prices.\n\n'))
        return data 
    
    def static_pricing(self, data, averageEnergyHousehold):
        year_sums = {year: 0 for year in range(Param.start_date.year, (Param.stop_date.year + 1))}
        # Group by year and calculate the sum for dynamic electricity price and energy consumption
        grouped_data = data.groupby(data.index.year)
        for year, group in grouped_data:
            if year in year_sums:
                year_sums[year] = (group['Dynamic Electricity Price [Cent/kWh]'] * group['SLP-Energy [kWh]']).sum() # if float16 - result = inf

        # Calculate static prices
        prices = {year: year_sums[year] / averageEnergyHousehold for year in year_sums}

        data['Static Electricity Price [Cent/kWh]'] = pd.Series(dtype=self.datatype)
        # Apply static prices based on year (vectorized)
        # if prices[year] not exist, it will take the price of 2023
        try:
            data['Static Electricity Price [Cent/kWh]'] = (data.index.year.map(lambda year: prices.get(year, prices[2024]))).astype(self.str_datatype) 
        except:
            pass
        additional = 0
        for index, row in data.iterrows():
            # To get the first optimisation to behave like in real life 
            # make the price for the energy out of the grid cheaper with the time 
            additional += 1e-8
            data.at[index, "Static Electricity Price [Cent/kWh]"] = data.at[index, "Static Electricity Price [Cent/kWh]"] - additional
        # Fill the last row for 2024 New Years hour with the static price of 2023
        # Lambda Funktion macht dies unnötig da bereits nicht vorhandene Daten den Wert aus 2023 zugewiesen bekommen
        # data['Static Electricity Price [Cent/kWh]'] = data['Static Electricity Price [Cent/kWh]'].ffill()

        with open(os.path.join(self.data_path,self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nLoaded the static energy prices.\n\n'))
        return data
    

    def time_variable_Netzentgelte(self, data):
        # in the static and dynamic prices are the standard_NE added (all prices with included taxes)
        # to calculate: add or substrate the difference to the standard
        high_NE     = 17.75     # 15 - 20 Uhr 
        standard_NE = 11.88     # 6  - 15 Uhr , 20 - 24 Uhr 
        low_NE      = 1.19      # 0  -  6 Uhr

        # add the columns for static and dynamic with time variable NE
        data['Static Timevariant Electricity Price [Cent/kWh]']    = data['Static Electricity Price [Cent/kWh]'].copy()
        data['Dynamic Timevariant Electricity Price [Cent/kWh]']   = data['Dynamic Electricity Price [Cent/kWh]'].copy()
        print(data.index.dtype)
        # fill it with the add and substraction with the difference to the standard price
        data.loc[data.index.hour < 6, 'Static Timevariant Electricity Price [Cent/kWh]'] = data["Static Electricity Price [Cent/kWh]"] - (standard_NE - low_NE)
        data.loc[(data.index.hour >= 15) & (data.index.hour < 20), 'Static Timevariant Electricity Price [Cent/kWh]'] = data["Static Electricity Price [Cent/kWh]"] + (high_NE - standard_NE)

        data.loc[data.index.hour < 6, 'Dynamic Timevariant Electricity Price [Cent/kWh]'] = data["Dynamic Electricity Price [Cent/kWh]"] - (standard_NE - low_NE)
        data.loc[(data.index.hour>= 15) & (data.index.hour < 20), 'Dynamic Timevariant Electricity Price [Cent/kWh]'] = data["Dynamic Electricity Price [Cent/kWh]"] + (high_NE - standard_NE)

        data['Static Timevariant Electricity Price [Cent/kWh]'] = data['Static Timevariant Electricity Price [Cent/kWh]'].ffill()
        data['Static Timevariant Electricity Price [Cent/kWh]'] = data['Static Timevariant Electricity Price [Cent/kWh]'].ffill()

        print("dynamic",data["Dynamic Electricity Price [Cent/kWh]"])
        print('timevariant',data["Dynamic Timevariant Electricity Price [Cent/kWh]"])

        with open(os.path.join(self.data_path,self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nLoaded the time variable Netzentgelte.\n\n'))
        return data 
