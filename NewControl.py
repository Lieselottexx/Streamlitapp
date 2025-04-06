# Import Bibs
import pandas as pd
import multiprocessing
import os
import streamlit as st

# Import Python Files
import Param
import NewDataGenerator as d
import NewPriceGenerator as p
import NewOptimisation as o
import NewAnalysis as a




class Control():

    def __init__(self):
        self.data_generator = d.DataGenerator()
        self.price_generator = p.PriceGenerator()
        self.opimisation = o.Optimisation()
        self.analysis = a.Analysis()
        self.data_path = Param.data_path
        # get the prices once is enough
        
        # st.title('Uber pickups in NYC')
        # self.program_flow()

        pass

    def __del__(self):
        pass


    def calculation(self, progress_bar_loading, status_text_loading, progress_bar_Opti1, status_text_Opti1, 
                         progress_bar_Opti2, status_text_Opti2):

        progress_loading = 5
        progress_bar_loading.progress(progress_loading)
        status_text_loading.text(f"Daten werden geladen... {progress_loading}% abgeschlossen")

        ''' Lastprofile, PV Daten und Börsenstrompreise einlesen '''
        loadprofiles = {1000: 1, 1500: 2, 2000: 3, 2500: 4, 3000: 5, 3500: 6,  4000: 7,
                        4500: 8, 5000: 9, 5500: 10, 6000: 11, 6500: 12, 7000: 13,  7500: 14, 8000: 15}
        
        progress_loading = 7
        progress_bar_loading.progress(progress_loading)
        status_text_loading.text(f"Daten werden geladen... {progress_loading}% abgeschlossen")

        st.session_state.loadprofile = loadprofiles[st.session_state.consumption]
        print(f"Lastprofil: {st.session_state.loadprofile}")
        del(loadprofiles)

        progress_loading = 10
        progress_bar_loading.progress(progress_loading)
        status_text_loading.text(f"Daten werden geladen... {progress_loading}% abgeschlossen")

        self.data, averageEnergyHousehold = self.data_generator.loadData(st.session_state.loadprofile,
                                                                         st.session_state.pv_direction, 
                                                                         st.session_state.pv_power) 
        progress_loading = 70
        progress_bar_loading.progress(progress_loading)
        status_text_loading.text(f"Daten werden geladen... {progress_loading}% abgeschlossen")



        '''Stromtarife berechnen'''
        self.data = self.price_generator.calculate_energy_prices(self.data, averageEnergyHousehold,
                                                                 st.session_state.controllable_device)
        progress_loading = 100
        progress_bar_loading.progress(progress_loading)
        status_text_loading.text(f"Daten werden geladen... {progress_loading}% abgeschlossen")
        
        progress_Opti1 = 5
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")


        '''Wenn das ein dann nur statisch mit Zeitvariablen Netzentgelten rechnen'''
        if st.session_state.static_ZVNE == 1:
            select_opti = self.select_optimisation_behaviour(9)
        else:
            if st.session_state.has_eeg:
                select_opti = self.select_optimisation_behaviour(3)
                if st.session_state.controllable_device:
                    select_opti = self.select_optimisation_behaviour(10)
            else:
                select_opti = self.select_optimisation_behaviour(8)
                if st.session_state.controllable_device:
                    select_opti = self.select_optimisation_behaviour(11)
        
        progress_Opti1 = 10
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")
        
        st.write(f"Das ausgewählte Verhalten ist: {select_opti[0]}")
   
        month_pv_installation = st.session_state.installation_date.month
        year_pv_installation  = st.session_state.installation_date.year
        self.static_feed_in_price, self.static_bonus_feed_in = self.get_eeg_prices(year_pv_installation,month_pv_installation)

        battery_power = st.session_state.battery_capacity * 5/60 

        input_optimisation =    [Param.optimise_time, Param.step_time, st.session_state.battery_capacity,
                                 Param.battery_costs,
                                 battery_power, 
                                 Param.grid_power, self.static_feed_in_price, self.static_bonus_feed_in]
        
        progress_Opti1 = 20
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")
        
        
        data_optimised = self.opimisation.select_optimisation(self.data.astype(Param.datatype), 
                                                              input_optimisation, 
                                                              select_opti)
        progress_Opti1 = 90
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")

        
        # calculation of the costs and store in a Dataframe to concat all together later
        costs_selected, battery_charge = self.analysis.single_cost_batterycycle_calculation(data_optimised, select_opti)
        progress_Opti1 = 100
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")

        progress_Opti2 = 5
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")

        select_opti = self.select_optimisation_behaviour(1)
        progress_Opti2 = 10
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")
        data_optimised = self.opimisation.select_optimisation(self.data.astype(Param.datatype), 
                                                              input_optimisation, 
                                                              select_opti)
        progress_Opti2 = 90
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")
        
        
        # calculation of the costs and store in a Dataframe to concat all together later
        costs_evo, battery_charge = self.analysis.single_cost_batterycycle_calculation(data_optimised, select_opti)
        progress_Opti2 = 100
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")

        benefit = costs_evo - costs_selected
        status_text_Opti2.text(f"Einsparungen werden berechnet... {progress_Opti2}% abgeschlossen")
        return benefit, progress_bar_loading, status_text_loading, progress_bar_Opti1, status_text_Opti1, progress_bar_Opti2, status_text_Opti2
        
    # def program_flow(self):
    #     profile_info = self.loading_of_categories_file()
    #     ''' Optimisation '''
    #     self.optimisation_process(profile_info)
        
    #     ''' Analysis '''
    #     # info_dict = self.analysis.loading_optimised_data(profile_info)
    #     # for key, values in info_dict.items():
    #     #     info_dict[key]['Select Opti'] = self.select_optimisation_behaviour(values['Behaviour'])
    #     '''Cost and battery cycle analysis for one specific profile out of the dict'''
    #     # num = 3
    #     # select_opti = self.select_optimisation_behaviour(9)
    #     # costs = self.analysis.single_cost_batterycycle_calculation(info_dict[num]['Original Data'], profile_info.iloc[num], select_opti)
    #     # print(costs)

        
    #     '''Calculation of the costs files of the different optimisation types'''
    #     # cost1  = self.analysis.calculate_combine_costs_optimisationwise(info_dict, 1,  'costs_1.csv')
    #     # cost3  = self.analysis.calculate_combine_costs_optimisationwise(info_dict, 3,  'costs_3.csv')
    #     # cost8  = self.analysis.calculate_combine_costs_optimisationwise(info_dict, 8,  'costs_8.csv')
    #     # cost9  = self.analysis.calculate_combine_costs_optimisationwise(info_dict, 9,  'costs_9.csv')
    #     # cost10 = self.analysis.calculate_combine_costs_optimisationwise(info_dict, 10, 'costs_10.csv')
    #     # cost11 = self.analysis.calculate_combine_costs_optimisationwise(info_dict, 11, 'costs_11.csv')

    #     ''' Open Presaved Cost Files '''
    #     # column_names = ['Datetime', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    #     #                             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #     #                             '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    #     #                             '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
    #     #                             '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    #     #                             '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
    #     #                             '61', '62', '63', '64']
    #     # cost1         = pd.read_csv(os.path.join(self.data_path, 'costs_1.csv'),    delimiter=';', header=0, names=column_names, index_col='Datetime')
    #     # cost1.index   = pd.to_datetime(cost1.index, format='%Y-%m-%d %H:%M:%S')
    #     # # cost3         = pd.read_csv(os.path.join(self.data_path, 'costs_3.csv'),    delimiter=';', header=0, names=column_names, index_col='Datetime')
    #     # # cost3.index   = pd.to_datetime(cost3.index, format='%Y-%m-%d %H:%M:%S')
    #     # # cost8         = pd.read_csv(os.path.join(self.data_path, 'costs_8.csv'),    delimiter=';', header=0, names=column_names, index_col='Datetime')
    #     # # cost8.index   = pd.to_datetime(cost8.index, format='%Y-%m-%d %H:%M:%S')
    #     # # cost9         = pd.read_csv(os.path.join(self.data_path, 'costs_9.csv'),    delimiter=';', header=0, names=column_names, index_col='Datetime')
    #     # # cost9.index   = pd.to_datetime(cost9.index, format='%Y-%m-%d %H:%M:%S')
    #     # # cost10        = pd.read_csv(os.path.join(self.data_path, 'costs_10.csv'),  delimiter=';', header=0, names=column_names, index_col='Datetime')
    #     # # cost10.index  = pd.to_datetime(cost10.index, format='%Y-%m-%d %H:%M:%S')
    #     # cost11        = pd.read_csv(os.path.join(self.data_path, 'costs_11.csv'),  delimiter=';', header=0, names=column_names, index_col='Datetime')
    #     # cost11.index  = pd.to_datetime(cost11.index, format='%Y-%m-%d %H:%M:%S')
        
    #     # ''' Calculation of the Differential-Costs between two Optimisations '''
    #     # self.analysis.differential_costs_yearly(profile_info, cost1, cost11) # 1 - statisch , 2 - dynamisch 


    #     ''' Ploting the time based Results of the Optimisation '''
    #     # number_load_profile = 383
    #     # result_column_names =   ['Battery Charge [kWh]', 'Battery Discharge[kWh]', 
    #     #                         'Battery SOC', 'Supply from Grid [kWh]', 
    #     #                         'Grid Feed-in [kWh]']  # Könnte man mal vereinheitlichen!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #     # self.analysis.plot.print_self_consumption_optimisation(info_dict[number_load_profile]['Original Data'], info_dict[number_load_profile]['Select Opti'], result_column_names)

    #     ''' Ploting average time based Results'''
    #     # list_beh = [63,                             127,               191,         255,                319,            383]
    #     # name_beh = ['Eigenverbrauchsoptimierung',   'dyn. Stromtarif', 'ohne EEG',  'Eig. mit ZVNE',    'dyn. ZVNE',    'ZVNE ohne EEG']
    #     # self.analysis.average_load_profiles(info_dict, list_beh, name_beh)

    #     ''' Plot show only once in the end of the script '''
    #     # self.analysis.plot.show()





    # def loading_of_categories_file(self):
    #     # Loading of the Parameter for the different Optimisations
    #     profile_info = pd.DataFrame()
    #     profile_info = pd.read_csv(os.path.join(self.data_path, 'Load_profile_informations_csv.csv'), delimiter=';')
    #     return profile_info

    # def optimisation_process(self, profile_info):
    #     # seperate the inputs, every row is a new optimisation
    #     input_list = [row for _, row in profile_info.iterrows()]

    #     # seperate Optimisation Processes at the same time as many as the cpu can process
    #     with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    #         # return costs for each year
    #     #     self.pool_costs, self.pool_battery_cycles = pool.map(self.loading_optimisation, input_list)
    #         pool.map(self.loading_optimisation, input_list)
    #     # # concat the costs results into a big dataframe
    #     # result_costs = pd.concat(self.pool_result, axis=1)
    #     # result_battery_cycles = pd.concat(self.pool_battery_cycles, axis=1)
    #     # # save the costs results to a csv file
    #     # result_costs.to_csv(os.path.join(self.data_path, 'costs.csv'), sep=';') 
    #     # result_battery_cycles.to_csv(os.path.join(self.data_path, 'batterycycles.csv'), sep=';')

    # def loading_optimisation(self, profile_info):
    #     self.data, averageEnergyHousehold = self.data_generator.loadData(profile_info['Load profile'], 
    #                                                                      profile_info['PV Mode'], 
    #                                                                      profile_info['PV System']) 
            
    #     # Calculating the Electricity prices dynamic and static 
    #     self.data = self.price_generator.calculate_energy_prices(self.data, averageEnergyHousehold)

    #     select_opti = self.select_optimisation_behaviour(profile_info['Behaviour'])

    #     # correct of the blindspace data name with the info of the optimisation
    #     select_opti[4] = str('L'+str(int(profile_info['Load profile']))
    #                          +'Behav'+str(int(profile_info['Behaviour']))
    #                          +'Batt'+str(int(profile_info['Battery']))
    #                          +'PV'+str(int(profile_info['PV System']))      +'.csv')
        
    #     # eventuell input loading übergeben und alles andere im optimisation task festlegen aus param
    #     # input_optimisation =    [Param.optimise_time, Param.step_time, profile_info['Battery'],
    #     #                          Param.battery_costs,
    #     #                         profile_info['Battery Power'], 
    #     #                         Param.grid_power, self.static_feed_in_price, self.static_bonus_feed_in]
        
    #     # data_optimised = self.opimisation.select_optimisation(self.data.astype(Param.datatype), 
    #     #                                                       input_optimisation, 
    #     #                                                       select_opti)
        
    #     # # calculation of the costs and store in a Dataframe to concat all together later
    #     # costs, battery_charge = self.analysis.single_cost_batterycycle_calculation(data_optimised, 
    #     #                                                                     profile_info, 
    #     #                                                                     select_opti)
        
    #     st.write("Hi ich bin fertig mit rechnen!")#(f"**Power:** {costs} Euro")
    #     # return costs, battery_charge
    
    def select_optimisation_behaviour(self, number_optimisation):
        ''' Select Opti:
        0 - Number of Optimisation [0]
        1 - Energy price: 0 - static, 1 - dynamic [1
        2 - Einspeisung: 0 - static, 1 - dynamic [2]
        3 - EEG: 0 - no EEG System, 1 - EEG System [3] 
        4 - Name of the CSV of the Optimisation [4]
        5 - energy price name of the column[5] 
        6 - feed in name of the column[6]'''

        
        # Selection of the behaviour of the Optimisation
        if number_optimisation == 1:
            select_opti = [1, 0, 0, 1, 'eeg_static_static_optimisation.csv', 'Static Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 2:
            select_opti = [2, 0, 1, 1, 'eeg_static_direct_optimisation.csv', 'Static Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price [Cent/kWh]']
        elif number_optimisation == 3:
            select_opti = [3, 1, 0, 1, 'eeg_dynamic_static_optimised.csv', 'Dynamic Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 4:
            select_opti = [4, 1, 1, 1, 'eeg_dynamic_direct_optimisation.csv','Dynamic Electricity Price [Cent/kWh]' , 'Dynamic Feed-in Price [Cent/kWh]']
        elif number_optimisation == 5:
            select_opti = [5, 0, 0, 0, 'static__static_optimisation.csv', 'Static Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 6:
            select_opti = [6, 0, 1, 0, 'static_direct_optimisation.csv', 'Static Electricity Price [Cent/kWh]', 'Energy Price [Cent/kWh]']
        elif number_optimisation == 7:
            select_opti = [7, 1, 0, 0, 'dynamic_static_optimised.csv', 'Dynamic Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 8:
            select_opti = [8, 1, 1, 0, 'alles_float16_mit_variable_2024_10_16_opti_ergebniss.csv','Dynamic Electricity Price [Cent/kWh]' , 'Energy Price [Cent/kWh]'] 
        elif number_optimisation == 9:
            select_opti = [9, 0, 0, 1, 'eeg_static_static_optimisation.csv', 'Static Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 10:
            select_opti = [10, 1, 0, 1, 'eeg_dynamic_static_optimised.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 11:
            select_opti = [11, 1, 1, 0, 'dynZVNEohneEEG.csv','Dynamic Timevariant Electricity Price [Cent/kWh]' , 'Energy Price [Cent/kWh]']
        return select_opti
        


    def get_eeg_prices(self, yearofinstallation, monthofinstallation):
        if   yearofinstallation == 2018: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [12.60, 12.60, 12.60, 12.60, 12.60, 12.60, 12.60, 12.48, 12.35, 12.23, 12.11, 11.99],
                        'static_feed_in_price': [12.20, 12.20, 12.20, 12.20, 12.20, 12.20, 12.20, 12.08, 11.95, 11.83, 11.71, 11.59]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif yearofinstallation == 2019: 
            eeg_prices = pd.DataFrame({ 
                        'static_bonus_feed_in': [11.87, 11.75, 11.63, 11.51, 11.35, 11.19, 11.04, 10.88, 10.73, 10.58, 10.48, 10.37],
                        'static_feed_in_price': [11.47, 11.35, 11.23, 11.11, 10.95, 10.79, 10.64, 10.48, 10.33, 10.18, 10.08, 9.97]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif yearofinstallation == 2020: 
            eeg_prices = pd.DataFrame({ 
                        'static_bonus_feed_in': [10.27, 10.12, 9.98, 9.84, 9.70, 9.57, 9.43, 9.30, 9.17, 9.04, 8.88, 8.72],
                        'static_feed_in_price': [ 9.87,  9.72, 9.58, 9.44, 9.30, 9.17, 9.03, 8.90, 8.77, 8.64, 8.48, 8.32]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif yearofinstallation == 2021: 
            eeg_prices = pd.DataFrame({ 
                        'static_bonus_feed_in': [8.56, 8.44, 8.32, 8.21, 8.09, 7.98, 7.87, 7.76, 7.65, 7.54, 7.43, 7.33],
                        'static_feed_in_price': [8.16, 8.04, 7.92, 7.81, 7.69, 7.58, 7.47, 7.36, 7.25, 7.14, 7.03, 6.93]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif yearofinstallation == 2022: 
            eeg_prices = pd.DataFrame({ 
                        'static_bonus_feed_in': [7.23, 7.13, 7.03, 6.93, 6.83, 6.74, 6.64, 8.60, 8.60, 8.60, 8.60, 8.60],
                        'static_feed_in_price': [6.83, 6.73, 6.63, 6.53, 6.43, 6.34, 6.24, 8.20, 8.20, 8.20, 8.20, 8.20]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif yearofinstallation == 2023:
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [8.60, 8.60, 8.60, 8.60, 8.60, 8.60, 8.60, 8.60, 8.60, 8.60, 8.60, 8.60],
                        'static_feed_in_price': [8.20, 8.20, 8.20, 8.20, 8.20, 8.20, 8.20, 8.20, 8.20, 8.20, 8.20, 8.20]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif yearofinstallation == 2024:
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [8.60, 8.51, 8.51, 8.51, 8.51, 8.51, 8.51, 8.43, 8.43, 8.43, 8.43, 8.43],
                        'static_feed_in_price': [8.20, 8.11, 8.11, 8.11, 8.11, 8.11, 8.11, 8.03, 8.03, 8.03, 8.03, 8.03]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        else: pass
                
        return eeg_prices.at[monthofinstallation, 'static_feed_in_price'],  eeg_prices.at[monthofinstallation, 'static_bonus_feed_in'] 
        