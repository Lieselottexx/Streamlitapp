# Import Bibs
from datetime import datetime # , timedelta
import pandas as pd
import os
# Import Python Files
import Param
import NewPlot as plot


class Analysis():

    def __init__(self):
        self.plot = plot.Plot_Data()
        self.data_path = Param.data_path
        self.log_file_name = "log.txt"
        pass

    def __del__(self):
        pass


    ''' Function to calculate the costs of the optimised load profile and the battery cycles for every year'''
    def single_cost_batterycycle_calculation(self, data, select_opti):
        result_column_names =   ['Battery Charge [kWh]', 'Battery Discharge[kWh]', 
                                'Battery SOC', 'Supply from Grid [kWh]', 
                                'Grid Feed-in [kWh]']
        # Calculation of the costs
        costs_of_grid_supply = pd.DataFrame(index=data.index)
        payment_of_feed_in = pd.DataFrame(index=data.index)
        costs = pd.DataFrame(index=data.index)
        costs_of_grid_supply = data[result_column_names[3]] * (data[select_opti[5]]/100)
        payment_of_feed_in = data[result_column_names[4]] *(data[select_opti[6]]/100)
        costs = costs_of_grid_supply - payment_of_feed_in
        costs_of_grid_supply = costs_of_grid_supply.resample('1Y').sum()
        payment_of_feed_in = payment_of_feed_in.resample('1Y').sum() 
        costs = costs.resample('1Y').sum()

    
        self.related_path_data = Param.data_path
        self.original_data_path ='Original_Data_2024'
        load_path = os.path.join(self.related_path_data, self.original_data_path, 'CO2_Emissionen')
        column_names = ['Datetime', 'Co2-Emissions [gCO2/kWh]']
        co2_data = pd.read_csv(os.path.join(load_path, 'CO2Emissionen2024.csv'), delimiter=';', header=0, names=column_names, index_col='Datetime')
        co2_data.index = pd.to_datetime(co2_data.index, format='%d.%m.%Y %H:%M')

        grid_supply_orig = pd.DataFrame()
        grid_supply_orig    = data[result_column_names[3]].copy()
        feed_in_orig        = data[result_column_names[4]].copy()
        grid_supply         = grid_supply_orig.resample('1H').sum()
        feed_in_orig        = feed_in_orig.resample('1H').sum()
        co2_data = pd.concat([co2_data, grid_supply, feed_in_orig], axis=0)
        print(co2_data)
        co2 = co2_data['Co2-Emissions [gCO2/kWh]'] * (grid_supply/1000) - co2_data['Co2-Emissions [gCO2/kWh]'] * (feed_in_orig/1000)
        co2 = co2.resample('1Y').sum() 

        # print(co2)

        return costs , co2

