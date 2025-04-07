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


        pass

    def __del__(self):
        pass


    def calculation(self, session, progress_bar_loading, status_text_loading, progress_bar_Opti1, status_text_Opti1, 
                         progress_bar_Opti2, status_text_Opti2):

        progress_loading = 5
        progress_bar_loading.progress(progress_loading)
        status_text_loading.text(f"Daten werden geladen... {progress_loading}% abgeschlossen")

        ''' Lastprofile, PV Daten und Börsenstrompreise einlesen '''
        loadprofiles = {2000: 3,  3000: 5,  4000: 12,
                        5000: 13, 6000: 17, 7000: 15, 8000: 16}
        
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
                                                              select_opti, session)
        print("1. Opti fertig")
        progress_Opti1 = 90
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")

        
        # calculation of the costs and store in a Dataframe to concat all together later
        costs_selected = self.analysis.single_cost_batterycycle_calculation(data_optimised, select_opti)
        progress_Opti1 = 100
        progress_bar_Opti1.progress(progress_Opti1)
        status_text_Opti1.text(f"Optimierter Lastgang wird berechnet... {progress_Opti1}% abgeschlossen")

        progress_Opti2 = 5
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")

        select_opti = self.select_optimisation_behaviour(1)
        print(select_opti[0])
        progress_Opti2 = 10
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")
        data_optimised = self.opimisation.select_optimisation(self.data.astype(Param.datatype), 
                                                              input_optimisation, 
                                                              select_opti, session)
        print("zweite Opti fertig")
        progress_Opti2 = 90
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")
        
        
        # calculation of the costs and store in a Dataframe to concat all together later
        costs_evo = self.analysis.single_cost_batterycycle_calculation(data_optimised, select_opti)
        progress_Opti2 = 100
        progress_bar_Opti2.progress(progress_Opti2)
        status_text_Opti2.text(f"Eigenverbrauchsoptimierung wird berechnet... {progress_Opti2}% abgeschlossen")
        print(costs_evo, ' - ', costs_selected)
        benefit = costs_evo['2024-12-31'] - costs_selected['2024-12-31']
        print('= ',benefit)
        status_text_Opti2.text(f"Einsparungen werden berechnet... {progress_Opti2}% abgeschlossen")
        return benefit, progress_bar_loading, status_text_loading, progress_bar_Opti1, status_text_Opti1, progress_bar_Opti2, status_text_Opti2
        
    
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
        if   yearofinstallation == 2012: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [19.50, 19.50, 19.50, 19.50, 19.31, 18.92, 18.73, 18.54, 18.36, 17.90, 17.45, 17.02],
                        'static_feed_in_price': [19.50, 19.50, 19.50, 19.50, 19.31, 18.92, 18.73, 18.54, 18.36, 17.90, 17.45, 17.02]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif   yearofinstallation == 2013: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [16.64, 16.28, 16.28, 15.92, 15.63, 15.35, 15.07, 14.80, 14.54, 14.27, 14.07, 13.88],
                        'static_feed_in_price': [16.64, 16.28, 16.28, 15.92, 15.63, 15.35, 15.07, 14.80, 14.54, 14.27, 14.07, 13.88]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif   yearofinstallation == 2014: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [13.07, 13.55, 13.41, 13.28, 13.14, 13.01, 12.88, 13.15, 13.08, 13.05, 13.02, 12.99],
                        'static_feed_in_price': [13.07, 13.55, 13.41, 13.28, 13.14, 13.01, 12.88, 12.75, 12.69, 12.65, 12.62, 12.59]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif   yearofinstallation == 2015: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [12.95, 12.92, 12.89, 12.86, 12.82, 12.97, 12.76, 12.73, 12.70, 12.70, 12.70, 12.70],
                        'static_feed_in_price': [12.56, 12.53, 12.50, 12.47, 12.43, 12.40, 12.37, 12.34, 12.31, 12.31, 12.31, 12.31]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif   yearofinstallation == 2016: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [12.70, 12.70, 12.70, 12.70, 12.70, 12.70, 12.70, 12.70, 12.70, 12.70, 12.70, 12.70],
                        'static_feed_in_price': [12.31, 12.31, 12.31, 12.31, 12.31, 12.31, 12.31, 12.31, 12.31, 12.31, 12.31, 12.31]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif   yearofinstallation == 2017: 
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [12.70, 12.70, 12.70, 12.70, 12.67, 12.64, 12.60, 12.60, 12.60, 12.60, 12.60, 12.60],
                        'static_feed_in_price': [12.30, 12.30, 12.30, 12.30, 12.27, 12.24, 12.20, 12.20, 12.20, 12.20, 12.20, 12.20]
                        }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        elif   yearofinstallation == 2018: 
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
        elif yearofinstallation == 2025:
            eeg_prices = pd.DataFrame({
                        'static_bonus_feed_in': [8.43, 8.34, 8.34, 8.34, 8.34, 8.34, 8.34],
                        'static_feed_in_price': [8.30, 7.94, 7.94, 7.94, 7.94, 7.94, 7.94]
                        }, index=[1,2,3,4,5,6,7])
        else: pass
                
        return eeg_prices.at[monthofinstallation, 'static_feed_in_price'],  eeg_prices.at[monthofinstallation, 'static_bonus_feed_in'] 
        