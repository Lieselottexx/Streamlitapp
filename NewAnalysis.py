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
        # Calculation of the yearly battery cycles
        # battery_charge = pd.DataFrame(index=data.index)
        # battery_charge = data[result_column_names[0]].copy().resample('1Y').sum() / info_dict_key['Battery']
        return costs #, battery_charge

    # '''Loading all stored inforamtions to the profile infos of the optimisations'''
    # def loading_optimised_data(self, profile_info):
    #     info_dict = profile_info.to_dict(orient='index')
    #     # read the csy file and sort the considered columns ito the dict
    #     for key, values in info_dict.items():
    #         # get the right csv file name out of the informations to the considered Profiles
    #         info_dict[key]["CSV File"] = str('L'+str(int(values['Load profile']))
    #                          +'Behav'+str(int(values['Behaviour']))
    #                          +'Batt'+str(int(values['Battery']))
    #                          +'PV'+str(int(values['PV System']))      +'.csv')
    #         # read the csv file 
    #         try:
    #             original_data = pd.read_csv(os.path.join(self.data_path, info_dict[key]["CSV File"]), delimiter=';', index_col='Datetime')
    #             original_data.index = pd.to_datetime(original_data.index, format='%Y-%m-%d %H:%M:%S')
    #         except:
    #             print('Failed to read the considered CSV-File with the name: ', info_dict[key]["CSV File"])

    #         info_dict[key]['Original Data'] = original_data.copy()
    #         selected_columns = ["Load Energy [kWh]", "PV-Energy [kWh]", "SLP-Energy [kWh]", "Supply from Grid [kWh]", "Grid Feed-in [kWh]"]
    #         for profile in selected_columns:
    #             info_dict[key][profile] = original_data[profile].copy()
    #         info_dict[key]['Load Profile [kWh]'] = info_dict[key]['Load Energy [kWh]'] - info_dict[key]['PV-Energy [kWh]']
    #         info_dict[key]['Sum Grid [kWh]'] = info_dict[key]["Supply from Grid [kWh]"] - info_dict[key]["Grid Feed-in [kWh]"]

    #     return info_dict
    
    # ''' Plot the average Loadprofile of one household'''
    # def average_load_profiles(self, info_dict, list_beh, name_beh):
    #     list_plot_data = []
    #     for number in range(len(list_beh)):
    #         data = pd.DataFrame()
    #         data = pd.DataFrame(info_dict[list_beh[number]]["Sum Grid [kWh]"].copy())
    #         data = data[data.index.month == 7]
    #         data_day = data[data.index.dayofweek < 5]
    #         data_day['Time'] = data_day.index.strftime('%H:%M')
    #         data_day.set_index('Time', inplace=True)
    #         list_plot_data.append(data_day.groupby(data_day.index).mean())
        
    #     load_data = pd.DataFrame(info_dict[list_beh[0]]["Load Profile [kWh]"].copy())    # 1
    #     load_data = load_data[load_data.index.month == 7]
    #     load_data_day = load_data[load_data.index.dayofweek < 5]
    #     load_data_day['Time'] = load_data_day.index.strftime('%H:%M')
    #     load_data_day.set_index('Time', inplace=True)
    #     list_plot_data.append(load_data_day.groupby(load_data_day.index).mean())

    #     slp_data = pd.DataFrame(info_dict[list_beh[0]]["SLP-Energy [kWh]"].copy())  # 1 
    #     slp_data = slp_data[slp_data.index.month == 7]
    #     slp_data_day = slp_data[slp_data.index.dayofweek < 5]
    #     slp_data_day['Time'] = slp_data_day.index.strftime('%H:%M')
    #     slp_data_day.set_index('Time', inplace=True)
    #     list_plot_data.append(slp_data_day.groupby(slp_data_day.index).mean())

    #     self.plot.average_load_profiles(list_plot_data, name_beh)



    # def calculate_combine_costs_optimisationwise(self, info_dict, number_opti, name_cost_file):
    #     costs               = pd.DataFrame()
    #     new_costs           = pd.DataFrame()
    #     newbatterycharge    = pd.DataFrame()
    #     batterycycle    = pd.DataFrame()
    #     for key, values in info_dict.items():
    #         if values['Behaviour'] == number_opti:
    #             new_costs, newbatterycharge = self.single_cost_batterycycle_calculation(values['Original Data'],values, values['Select Opti'])
    #             costs = pd.concat([costs, new_costs], axis=1) # 0 index , 1 columns 
    #             batterycycle = pd.concat([batterycycle, newbatterycharge], axis=1) # 0 index , 1 columns 
    #     # print('Für Optimierung Nummer ', number_opti, ' ergeben sich folgende Batteriezyklen:\n', batterycycle)
    #     costs.to_csv(os.path.join(self.data_path, name_cost_file), sep=';')
    #     costs.index = pd.to_datetime(costs.index)
        
    #     return costs
        
        
    # def differential_costs_yearly(self, profile_info, cost1, cost2):
    #     cost1 = cost1.resample('1Y').sum()
    #     cost2 = cost2.resample('1Y').sum()
    #     diff_costs = cost1 - cost2  # 1 - statisch , 2 - dynamisch 
    #     # print(diff_costs)
    #     savings = pd.DataFrame()
    #     savings['Gesamtkosten']     = diff_costs.loc['2024-12-31'].values
    #     savings['Category Load']    = profile_info['Category Load'].iloc[:len(cost1.columns)].copy()
    #     savings['Category PV']      = profile_info['Category PV'].iloc[:len(cost1.columns)].copy()
    #     savings['Category Battery'] = profile_info['Category Battery'].iloc[:len(cost1.columns)].copy()    
    #     print(savings)
    #     self.plot.diff_behaviour_analysis(savings)