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
        return costs 

