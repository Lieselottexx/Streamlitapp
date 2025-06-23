# Import Bibs
import pandas as pd
import multiprocessing
import os
import time
# import streamlit as st

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
        multiprocessing.set_start_method("spawn", force=True)

            
        self.optimise_time      = Param.optimise_time
        self.step_time          = Param.step_time
        self.battery_costs      = Param.battery_costs
        self.grid_power         = Param.grid_power
        self.min_data           = Param.min_data

        
        

        pass

    def __del__(self):
        pass


    def opti_und_cost_calc(self, data, input_optimisation, select_opti, battery_usage, queue, num):
        data_optimised = self.opimisation.select_optimisation(data,
                                                              input_optimisation, 
                                                              select_opti, battery_usage, queue, num)
        print(data_optimised)
        costs_selected = self.analysis.single_cost_batterycycle_calculation(data_optimised, select_opti)
        print(costs_selected)
        return costs_selected
    
    
    
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
        a = 'fester Strompreis'
        b = 'dynamischer Strompreis'
        c = 'fester Strompreis mit zeitvariablen Netzentgelten'
        d = 'dynamischer Strompreis mit zeitvariablen Netzentgelten'

        e = 'feste Einspeisevergütung'
        f = 'Direktvermarktung'

        if number_optimisation == 1:
            select_opti = [1, a, e, 1, '1.csv',   'Static Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 2:  
            select_opti = [2, a, f, 1, '2.csv',   'Static Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price [Cent/kWh]']
        elif number_optimisation == 3:  
            select_opti = [3, b, e, 1, '3.csv',   'Dynamic Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 4:  
            select_opti = [4, b, f, 1, '4.csv',   'Dynamic Electricity Price [Cent/kWh]' , 'Dynamic Feed-in Price [Cent/kWh]']
        elif number_optimisation == 5:  
            select_opti = [5, a, e, 0, '5.csv',   'Static Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 6:  
            select_opti = [6, a, f, 0, '6.csv',   'Static Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price U20 [Cent/kWh]']
        elif number_optimisation == 7:  
            select_opti = [7, b, e, 0, '7.csv',   'Dynamic Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 8:  
            select_opti = [8, b, f, 0, '8.csv',   'Dynamic Electricity Price [Cent/kWh]' , 'Dynamic Feed-in Price U20 [Cent/kWh]'] 
        elif number_optimisation == 9:  
            select_opti = [9, c, e, 1, '9.csv',   'Static Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 10:
            select_opti = [10, c, f, 1, '10.csv', 'Static Timevariant Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price [Cent/kWh]']
        elif number_optimisation == 11:
            select_opti = [11, d, e, 1, '11.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 12:
            select_opti = [12, d, f, 1, '12.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]' , 'Dynamic Feed-in Price [Cent/kWh]']
        elif number_optimisation == 13:
            select_opti = [13, c, e, 0, '13.csv', 'Static Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 14:
            select_opti = [14, c, f, 0, '14.csv', 'Static Timevariant Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price U20 [Cent/kWh]']
        elif number_optimisation == 15:
            select_opti = [15, d, e, 0, '15.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        elif number_optimisation == 16:
            select_opti = [16, d, f, 0, '16.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]' , 'Dynamic Feed-in Price U20 [Cent/kWh]']
        elif number_optimisation == 17:
            select_opti = [17, a, f, 0, '17.csv', 'Static Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price U20 [Cent/kWh]']
        elif number_optimisation == 18:
            select_opti = [18, b, f, 0, '18.csv', 'Dynamic Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price U20 [Cent/kWh]']
        elif number_optimisation == 19:
            select_opti = [19, c, f, 0, '19.csv', 'Static Timevariant Electricity Price [Cent/kWh]', 'Dynamic Feed-in Price U20 [Cent/kWh]']
        elif number_optimisation == 20:
            select_opti = [20, d, f, 0, '20.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]' , 'Dynamic Feed-in Price U20 [Cent/kWh]']
        


        # elif number_optimisation == 10:
        #     select_opti = [10, 1, 0, 1, 'eeg_dynamic_static_optimised.csv', 'Dynamic Timevariant Electricity Price [Cent/kWh]', 'Static Feed-in Price [Cent/kWh]']
        # elif number_optimisation == 11:
        #     select_opti = [11, 1, 1, 0, 'dynZVNEohneEEG.csv','Dynamic Timevariant Electricity Price [Cent/kWh]' , 'Energy Price [Cent/kWh]']
        return select_opti
        


    def get_eeg_prices(self, yearofinstallation, monthofinstallation, pv_power):
        # if   yearofinstallation == 2005: 
        #     eeg_prices = pd.DataFrame({
        #                 'static_bonus_feed_in': [54.80, 54.80, 54.80, 54.80, 54.80, 54.80, 54.80, 54.80, 54.80, 54.80, 54.80, 54.80],
        #                 'static_feed_in_price': [54.40, 54.40, 54.40, 54.40, 54.40, 54.40, 54.40, 54.40, 54.40, 54.40, 54.40, 54.40]
        #                 }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        # elif   yearofinstallation == 2006: 
        #     eeg_prices = pd.DataFrame({
        #                 'static_bonus_feed_in': [52.20, 52.20, 52.20, 52.20, 52.20, 52.20, 52.20, 52.20, 52.20, 52.20, 52.20, 52.20],
        #                 'static_feed_in_price': [51.80, 51.80, 51.80, 51.80, 51.80, 51.80, 51.80, 51.80, 51.80, 51.80, 51.80, 51.80]
        #                 }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        # elif   yearofinstallation == 2007: 
        #     eeg_prices = pd.DataFrame({
        #                 'static_bonus_feed_in': [49.60, 49.60, 49.60, 49.60, 49.60, 49.60, 49.60, 49.60, 49.60, 49.60, 49.60, 49.60],
        #                 'static_feed_in_price': [49.20, 49.20, 49.20, 49.20, 49.20, 49.20, 49.20, 49.20, 49.20, 49.20, 49.20, 49.20]
        #                 }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
        # elif   yearofinstallation == 2008: 
        #     eeg_prices = pd.DataFrame({
        #                 'static_bonus_feed_in': [47.15, 47.15, 47.15, 47.15, 47.15, 47.15, 47.15, 47.15, 47.15, 47.15, 47.15, 47.15],
        #                 'static_feed_in_price': [46.75, 46.75, 46.75, 46.75, 46.75, 46.75, 46.75, 46.75, 46.75, 46.75, 46.75, 46.75]
        #                 }, index=[1,2,3,4,5,6,7,8,9,10,11,12])   # https://www.iwr.de/re/wf/eeg%20photovoltaik.htm




        if pv_power > 10:
            # größer 10:
            if   yearofinstallation == 2009: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41],
                            'static_feed_in_price': [25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])  # bleiben 
            elif   yearofinstallation == 2010: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16],
                            'static_feed_in_price': [22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12]) # bleiben
            elif   yearofinstallation == 2011: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56],
                            'static_feed_in_price': [21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12]) # bleiben 
            elif   yearofinstallation == 2012: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [19.90, 19.90, 19.90, 19.90, 18.72, 18.53, 18.35, 18.17, 17.99, 17.82, 17.38, 16.96],
                            'static_feed_in_price': [19.50, 19.50, 19.50, 19.50, 18.32, 18.13, 17.95, 17.77, 17.59, 17.42, 16.98, 16.56]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12]) # 
            elif   yearofinstallation == 2013: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [16.54, 16.19, 15.84, 15.50, 15.23, 14.96, 14.70, 14.44, 14.19, 13.94, 13.75, 13.57],
                            'static_feed_in_price': [16.14, 15.79, 15.44, 15.10, 14.83, 14.56, 14.30, 14.04, 13.79, 13.54, 13.35, 13.17]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2014: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [13.38, 13.25, 13.12, 13.00, 12.87, 12.74, 12.62, 12.80, 12.74, 12.70, 12.67, 12.64],
                            'static_feed_in_price': [12.98, 12.85, 12.72, 12.60, 12.47, 12.34, 12.22, 12.40, 12.34, 12.31, 12.28, 12.25]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2015: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [12.61, 12.58, 12.55, 12.51, 12.48, 12.45, 12.42, 12.39, 12.36, 12.36, 12.36, 12.36],
                            'static_feed_in_price': [12.22, 12.18, 12.15, 12.12, 12.09, 12.06, 12.03, 12.00, 11.97, 11.97, 11.97, 11.97]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2016: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [12.36, 12.36, 12.36, 12.36, 12.36, 12.36, 12.36, 12.36, 12.36, 12.36, 12.36, 12.36],
                            'static_feed_in_price': [11.97, 11.97, 11.97, 11.97, 11.97, 11.97, 11.97, 11.97, 11.97, 11.97, 11.97, 11.97]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2017: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [12.36, 12.36, 12.36, 12.36, 12.33, 12.30, 12.27, 12.27, 12.27, 12.27, 12.27, 12.27],
                            'static_feed_in_price': [11.96, 11.96, 11.96, 11.96, 11.93, 11.90, 11.87, 11.87, 11.87, 11.87, 11.87, 11.87]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2018: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [12.27, 12.27, 12.27, 12.27, 12.27, 12.27, 12.27, 12.14, 12.02, 11.90, 11.78, 11.67],
                            'static_feed_in_price': [11.87, 11.87, 11.87, 11.87, 11.87, 11.87, 11.87, 11.74, 11.62, 11.50, 11.38, 11.27]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2019: 
                eeg_prices = pd.DataFrame({ 
                            'static_bonus_feed_in': [11.55, 11.43, 11.32, 11.21, 11.05, 11.90, 11.74, 10.59, 10.44, 10.30, 10.19, 10.09],
                            'static_feed_in_price': [11.15, 11.03, 10.92, 10.81, 10.65, 10.50, 10.34, 10.19, 10.04,  9.90,  9.79,  9.69]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2020: 
                eeg_prices = pd.DataFrame({ 
                            'static_bonus_feed_in': [10.99, 10.85, 9.71, 9.58, 9.44, 9.31, 9.18, 9.05, 8.93, 8.80, 8.64, 8.49],
                            'static_feed_in_price': [ 9.59,  9.45, 9.31, 9.18, 9.04, 8.91, 8.78, 8.65, 8.53, 8.40, 8.24, 8.09]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2021: 
                eeg_prices = pd.DataFrame({ 
                            'static_bonus_feed_in': [8.33, 8.21, 8.10, 7.98, 7.87, 7.76, 7.65, 7.55, 7.44, 7.34, 7.23, 7.13],
                            'static_feed_in_price': [7.93, 7.81, 7.70, 7.59, 7.47, 7.36, 7.24, 7.15, 7.04, 6.94, 6.83, 6.73]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2022: 
                eeg_prices = pd.DataFrame({ 
                            'static_bonus_feed_in': [7.03, 6.93, 7.84, 6.74, 6.65, 6.55, 6.46, 7.50, 7.50, 7.50, 7.50, 7.50],
                            'static_feed_in_price': [6.63, 6.53, 6.44, 6.34, 6.25, 6.15, 6.06, 7.10, 7.10, 7.10, 7.10, 7.10]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2023:
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50, 7.50],
                            'static_feed_in_price': [7.10, 7.10, 7.10, 7.10, 7.10, 7.10, 7.10, 7.10, 7.10, 7.10, 7.10, 7.10]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2024:
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [7.50, 7.43, 7.43, 7.43, 7.43, 7.43, 7.43, 7.35, 7.35, 7.35, 7.35, 7.35],
                            'static_feed_in_price': [7.10, 7.03, 7.03, 7.03, 7.03, 7.03, 7.03, 6.95, 6.95, 6.95, 6.95, 6.95]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif yearofinstallation == 2025:
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [7.35, 7.28, 7.28, 7.28, 7.28, 7.28, 7.28],
                            'static_feed_in_price': [6.95, 6.88, 6.88, 6.88, 6.88, 6.88, 6.88]
                            }, index=[1,2,3,4,5,6,7])
        else:

            if   yearofinstallation == 2009: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41, 25.41],
                            'static_feed_in_price': [25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01, 25.01]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2010: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16, 23.16],
                            'static_feed_in_price': [22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76, 22.76]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12]) # https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/Photovoltaik/ArchivDatenMeldgn/DegressionsVergSaetze2010_pdf.pdf?__blob=publicationFile&v=1
            elif   yearofinstallation == 2011: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56],
                            'static_feed_in_price': [21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56, 21.56]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12]) # https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/Photovoltaik/ArchivDatenMeldgn/DegressionsVergSaetze2011_pdf.pdf?__blob=publicationFile&v=1
            elif   yearofinstallation == 2012: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [19.90, 19.90, 19.90, 19.90, 19.71, 19.32, 19.13, 18.94, 18.76, 18.30, 17.85, 17.42],
                            'static_feed_in_price': [19.50, 19.50, 19.50, 19.50, 19.31, 18.92, 18.73, 18.54, 18.36, 17.90, 17.45, 17.02]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2013: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [17.04, 16.68, 16.68, 16.32, 16.03, 15.75, 15.47, 15.20, 14.94, 14.67, 14.47, 14.28],
                            'static_feed_in_price': [16.64, 16.28, 16.28, 15.92, 15.63, 15.35, 15.07, 14.80, 14.54, 14.27, 14.07, 13.88]
                            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])
            elif   yearofinstallation == 2014: 
                eeg_prices = pd.DataFrame({
                            'static_bonus_feed_in': [13.47, 13.95, 13.81, 13.68, 13.54, 13.41, 13.28, 13.15, 13.08, 13.05, 13.02, 12.99],
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

        print(yearofinstallation, monthofinstallation)
        print(eeg_prices.at[monthofinstallation, 'static_feed_in_price'],  eeg_prices.at[monthofinstallation, 'static_bonus_feed_in'])
        return eeg_prices.at[monthofinstallation, 'static_feed_in_price'],  eeg_prices.at[monthofinstallation, 'static_bonus_feed_in'] 
        

def opti_und_cost_calc_wrapper(args):
    self_obj, data, input_optimisation, select_opti, session = args
    return self_obj.opti_und_cost_calc(data, input_optimisation, select_opti, session)

