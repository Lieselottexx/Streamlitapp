# Import Bibs
from datetime import datetime, timedelta
import pandas as pd
import os
import pvlib 
import numpy as np
import time

# Import Python Files
import Param
# import Plot_Data as plot


class DataGenerator():

    def __init__(self):
        # Initiate the Class with all plot functions
        # self.plot = plot.Plot_Data()
        # loading the current related data path out of the Param.py file
        self.related_path_data = Param.data_path
        # Pathname of the Log file
        self.log_file_name  = "log.txt"
        # Foldername of the original Data which will get load
        self.original_data_path ='Original_Data_2024'  # 'Original_Data' for 2018-2023
        # Loading the Parameter of the datatypes 
        self.datatype       = Param.datatype
        self.str_datatype   = Param.str_datatype

        # loading of the Load profile, slp, pv, energy prices and average monthly market value 
        # out of the original data
    def loadData(self, profile_num, pv_direction, peak_power_pv, battery_cap):
        data = pd.DataFrame()
        # Loading the choosen load profile of the household
        data, averageEnergyHousehold = self.load_loadprofile_household(data, profile_num)
        # Loading the H0 SLP Profile an scale it with he average Energy consumption of the Household in a year
        # data = self.load_slp_profile(data, averageEnergyHousehold)
        data = self.load_slp_profile_h25(data, averageEnergyHousehold, peak_power_pv, battery_cap)
        # Loading the PV-Generation Profile 
        if peak_power_pv == 0:
            data["PV-Energy [kWh]"] = 0.0
        else:
            data = self.load_pv_generation_profile(data, pv_direction, peak_power_pv)
        # Loading energy prices from the web
        data = self.load_energy_prices(data)
        # Loading monthly average prices 
        # data = data.loc[start_date:stop_date]
        
        data = self.load_direct_marketing_data(data)
        
        # ------------- Limitation of the Data to the start and end date ------------------------ 
        data = data.loc[Param.start_date:Param.stop_date]
        				
        # Resample the Data to 15 min 
        # Preise behalten den ersten und Energiedaten werden aufsummiert
        data_resample = data.resample('10T').agg({
                                                    "Load Energy [kWh]"                 : "sum",
                                                    "SLP-Energy [kWh]"                  : "sum",
                                                    "PV-Energy [kWh]"                   : "sum",
                                                    "Energy Price [Cent/kWh]"           : "first",
                                                    "Monthly Average Price [Cent/kWh]"  : "first"
                                                })
        

        with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nSaved the data DataFrame to CSV!\n\n'))
        return data_resample, averageEnergyHousehold





    def load_loadprofile_household(self, data, profile_num):
        # ----- Load the Load Profile Number - choosen in the Control class --------------- 
        load_path = os.path.join(self.related_path_data, self.original_data_path, 'Load_Profiles')
        if profile_num == 1:
            path_energy = '01_07/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 2:
            path_energy = '02_13/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 3:
            path_energy = '03_09/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 4:
            path_energy = '04_25/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 5:
            path_energy = '05_24/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 6:
            path_energy = '06_23/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 7:
            path_energy = '07_01/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 8:
            path_energy = '08_55/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 9:
            path_energy = '09_08/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 10:
            path_energy = '10_22/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 11:
            path_energy = '11_43/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 12:
            path_energy = '12_03/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 13:
            path_energy = '13_45/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 14:
            path_energy = '14_60/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 15:
            path_energy = '15_05/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 16:
            path_energy = '16_20/SumProfiles_300s.General.Electricity.csv'
        elif profile_num == 17:
            path_energy = '17_57/SumProfiles_300s.General.Electricity.csv'
        else:
            print("Chose a Household Number between 1 and 17, please.")

        column_names = ['Timestep','Datetime', 'Load Energy [kWh]']

        if os.path.exists(os.path.join(load_path, path_energy)):
            dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
            Load_data = pd.read_csv(os.path.join(load_path, path_energy), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
            Load_data.index = pd.to_datetime(Load_data.index, format='%d.%m.%Y %H:%M')
            del Load_data['Timestep']
            data = pd.concat([data, Load_data], axis=0)
            print("Load the Load Profile Number ", profile_num, ".")
            averageEnergyHousehold = 0
            averageEnergyHousehold = Load_data['Load Energy [kWh]'].sum() / Param.num_years
            # Check whether the index is unique and, if necessary, ensure that it is unique (got error without)
            if not Load_data.index.is_unique:
                Load_data = Load_data.groupby(level=0).first()  # save the first     
            # Open the Log File in 'a' append mode
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\n'))
                file.write(str('Household Load Profile: '+ str(profile_num)+ '\n'))
                file.write(str('The average energy consumption of the household over one year is: '+ str(averageEnergyHousehold) + ' kWh/a \n\n'))
            #self.plot.print_load_profile(data)            

        else:
            print("Error while loading Houshold Load Profile!")
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(datetime.now(), '/nFailed to Load the Houshold Load Data.\n\n')
    
        return data, averageEnergyHousehold




    def load_slp_profile(self, data, averageEnergyHousehold):
        # ----------------------Loading the Standard load profile --------------------------------
        slp_path = os.path.join(self.related_path_data, self.original_data_path, 'SLP_H0')

        slp_energy_save = 'SLP_Energy.csv'

        if os.path.exists(os.path.join(slp_path,slp_energy_save)):
            # Read the csv File to DataFrame
            column_names = ['Datetime','SLP-Energy [kWh]']
            dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
            slp_energy = pd.read_csv(os.path.join(slp_path,slp_energy_save), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
            # Convert the Time column to Datetime Format and shift -15 min
            slp_energy.index = pd.to_datetime(slp_energy.index, format='%d.%m.%Y %H:%M:%S') - pd.Timedelta(minutes=15)
            # Set the Datetime to Index of the DataFramer
            print("Load the SLP from the preprocessed File.")
        else: 
            print("Loading the SLP Data failed. Please Check the SLP_Energy.csv File.")
                   
        
        # denormalise with the average energy consumtion over a year 
        slp_energy['SLP-Energy [kWh]'] = slp_energy['SLP-Energy [kWh]'] * averageEnergyHousehold / 1000
        
        # Write the SLP-Profile in the Data-DataFrame
        data = pd.concat([data, slp_energy], axis=1)
        data['SLP-Energy [kWh]'] = (data['SLP-Energy [kWh]'].ffill() / 3).astype(self.str_datatype)
        
        with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nLoaded the SLP Profile.\n\n'))

        # plot the SLP Profile 
        # self.plot.print_slp_profile(data)

        return data
    

    def load_slp_profile_h25(self, data, averageEnergyHousehold, peak_power_pv, battery_cap):
        # ----------------------Loading the Standard load profile --------------------------------
        if peak_power_pv < 1:
            slp_path = os.path.join(self.related_path_data, self.original_data_path, 'SLP_H25')
            slp_energy_save = 'h25_2024.csv'
        else:
            slp_path = os.path.join(self.related_path_data, self.original_data_path, 'SLP_H25')
            slp_energy_save = 'p25_2024.csv'
            if battery_cap < 1:
                pass
            else:
                slp_path = os.path.join(self.related_path_data, self.original_data_path, 'SLP_H25')
                slp_energy_save = 's25_2024.csv'
        if os.path.exists(os.path.join(slp_path,slp_energy_save)):
            print(slp_energy_save)
            # Read the csv File to DataFrame
            column_names = ['Datetime','SLP-Energy [kWh]']
            dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
            slp_energy = pd.read_csv(os.path.join(slp_path,slp_energy_save), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
            # print(slp_energy)
            # Convert the Time column to Datetime Format and shift -15 m
            slp_energy.index = pd.to_datetime(slp_energy.index, format='%Y-%m-%d %H:%M:%S')# - pd.Timedelta(minutes=15)
            # Set the Datetime to Index of the DataFrame
            print("Load the SLP from the preprocessed File. File name: ", slp_energy_save)
        else: 
            print("Loading the SLP Data failed. Please Check the  File.")
                   
        print(slp_energy)
        # denormalise with the average energy consumtion over a year 
        slp_energy['SLP-Energy [kWh]'] = slp_energy['SLP-Energy [kWh]'] * averageEnergyHousehold / 1000
        
        # Write the SLP-Profile in the Data-DataFrame
        data = pd.concat([data, slp_energy], axis=1)
        data['SLP-Energy [kWh]'] = (data['SLP-Energy [kWh]'].ffill() / 3).astype(self.str_datatype)
        
        with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nLoaded the SLP Profile.\n\n'))

        # plot the SLP Profile 
        # self.plot.print_slp_profile(data)
        return data


    def load_pv_generation_profile(self, data, pv_direction, peak_power_pv): 
        '''Umgeschrieben auf Veränderbare Ausrichtung statt Süd und Ost/West auswählbar'''
        # -------------Start PV-Geration --------------------------------------------------------

        start_date  = Param.start_date
        stop_date   = Param.stop_date

        # ------------ Calculation from the Weatherdata -----------------------------------------
        # Directory for the original and preprocessed Weather Data

        # Preprocessed Data Directory
        directory_Weather   = os.path.join(self.related_path_data, self.original_data_path, 'PV_Generation/Weather_Data')
        # Original Data Directories
        directory_Solar     = os.path.join(self.related_path_data, self.original_data_path, 'PV_Generation/Weather_Data/Einstrahlungswerte')
        directory_Wind      = os.path.join(self.related_path_data, self.original_data_path, 'PV_Generation/Weather_Data/Wind')
        directory_Temp      = os.path.join(self.related_path_data, self.original_data_path, 'PV_Generation/Weather_Data/Temperatur')

        # Filenames for the preprocessed Data
        solar_data = 'Solar_data.csv'
        wind_data = 'Wind_data.csv'
        temp_data = 'Temperature_data.csv'

        # precalculated Files for the PV-Generation
        directory_precalculated = os.path.join(self.related_path_data, self.original_data_path, 'PV_Generation')
        south_pv_file = 'PV_South.csv'
        east_west_pv_file = 'PV_East_West.csv'

        with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\n'))
            file.write(str(str(pv_direction)+'. Mode is selected!\n\n'))
        # Loading the precalculated PV-Energy for the selected Mode
        # Loading precalculated south oriented PV Energy
        
        # Solar irradiation data 
        # If the preprocessed File exist load it
        if os.path.exists(os.path.join(directory_Weather,solar_data)):
            # Read the csv File to DataFrame
            column_names = ["Datetime","Defuse_Rediation_dhi","Global_Radiation_ghi","Direct_Radiation_dni"]
            dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
            Solar_data = pd.read_csv(os.path.join(directory_Weather,solar_data), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
            Solar_data.index = pd.to_datetime(Solar_data.index, format='%Y-%m-%d %H:%M:%S')
            print("Load Solar irradiance from File")
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\nLoaded the preprocessed Solar Data CSV Data.\n\n'))

        # Else produce and save the original Solar irradiation data
        else: 
            Solar_data = pd.DataFrame()
            # Sorting the Solar CSV Files 
            new_data = pd.DataFrame()
            filenames = sorted([filename for filename in os.listdir(os.path.join(directory_Solar)) if filename.endswith(".txt")])
            # Set understandable Header Names
            column_names = ['Station_ID','Datetime', 'Quality_Level', 'Defuse_Rediation_dhi', 'Global_Radiation_ghi', 'Sunshine_duration',
                            'Direct_Radiation_dni', 'Error']
            dtype_dict = {  'Defuse_Rediation_dhi': self.str_datatype,
                            'Global_Radiation_ghi': self.str_datatype,
                            'Direct_Radiation_dni': self.str_datatype}
            # load the files individually
            for filename in filenames:
                new_data = pd.read_csv(os.path.join(directory_Solar, filename), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
                new_data.index = pd.to_datetime(new_data.index, format='%Y%m%d%H%M')
                # Delete all not used columns 
                del new_data['Quality_Level']
                del new_data['Station_ID']
                del new_data['Error']
                del new_data['Sunshine_duration']
                # because the direct radiation is definded everywhere as -999, calculate the real direct radiation
                new_data['Direct_Radiation_dni'] = round(new_data['Global_Radiation_ghi'] - new_data['Defuse_Rediation_dhi'], 2)
                # concatenate the individual files to one big solar irradiation Dataframe
                Solar_data = pd.concat([Solar_data,new_data], axis=0)
            # Delete Duplicated Indexes
            Solar_data = Solar_data[~Solar_data.index.duplicated(keep='first')]
            # Reduce the rows to the needed Datetimes
            Solar_data = Solar_data.loc[start_date:stop_date]
            # Save the data as preprocessed
            Solar_data.to_csv(os.path.join(directory_Weather, solar_data), sep=';')
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\nSaved the preprocessed Solar Data to CSV Data.\n\n'))  

        # Wind Speed Data 
        # If the preprocessed File exist load it
        if os.path.exists(os.path.join(directory_Weather,wind_data)):
            # Read the csv File to DataFrame
            column_names = ['Datetime','Wind_speed']
            dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
            Wind_data = pd.read_csv(os.path.join(directory_Weather,wind_data), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
            Wind_data.index = pd.to_datetime(Wind_data.index, format='%Y-%m-%d %H:%M:%S')
            print("Load wind speed from File")
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\nLoaded the preprocessed Wind Data CSV Data.\n\n'))

        # Else produce and save the wind speed Data
        else: 
            Wind_data = pd.DataFrame()
            # Get all Filenames (history, recent, now...)
            Wind_files  = os.listdir(os.path.join(directory_Wind))
            # Sorting the Wind CSV Files 
            new_data = pd.DataFrame()
            filenames = sorted([filename for filename in os.listdir(os.path.join(directory_Wind)) if filename.endswith(".txt")])
            # Set understandable Header Names
            column_names = ['Station_ID', 'Datetime', 'Quality_Level', 'Wind_speed', 'Wind_direction', 'Error']
            dtype_dict = {'Wind_speed': self.str_datatype}
            # load the files individually
            for filename in filenames:
                new_data = pd.read_csv(os.path.join(directory_Wind, filename), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
                new_data.index = pd.to_datetime(new_data.index, format='%Y%m%d%H%M')
                # Set Datetime to Index
                #new_data.set_index('Datetime', inplace=True)
                # Delete all not used columns
                del new_data['Quality_Level']
                del new_data['Station_ID']
                del new_data['Error']
                del new_data['Wind_direction']
                # concatenate the individual files to one big wind speed DataFrame
                Wind_data = pd.concat([Wind_data, new_data], axis=0)
            Wind_data = Wind_data[~Wind_data.index.duplicated(keep='first')]
            # Reduce the rows to the needed Datetimes
            Wind_data = Wind_data.loc[start_date:stop_date]
            # Save the data as preprocessed
            Wind_data.to_csv(os.path.join(directory_Weather, wind_data), sep=';')  
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\nSaved the preprocessed Wind Data to CSV Data.\n\n'))

        # Air Temperature data 
        # If the preprocessed File exist load it
        if os.path.exists(os.path.join(directory_Weather,temp_data)):
            # Read the csv File to DataFrame
            column_names = ['Datetime','Air_Temperature']
            dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
            Temp_data = pd.read_csv(os.path.join(directory_Weather,temp_data), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
            Temp_data.index = pd.to_datetime(Temp_data.index, format='%Y-%m-%d %H:%M:%S')
            print("Load air temperature from File")
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\nLoaded the preprocessed Temperature Data CSV Data.\n\n'))
        # Else produce and save the original Air Temperature Data
        else: 
            Temp_data = pd.DataFrame()
            # Get all Filenames (history, recent, now...)
            Temp_files  = os.listdir(os.path.join(directory_Temp))
            # Sorting the Temperatur CSV Files
            new_data = pd.DataFrame()
            filenames = sorted([filename for filename in os.listdir(os.path.join(directory_Temp)) if filename.endswith(".txt")])
            # Set understandable Header Names
            column_names = ['Station_ID','Datetime', 'Quality_Level', 'Air_Pressure','Air_Temperature', 'Ground_Temperature', 
                            'Relative_Humidity','Dew_Point', 'Error']
            dtype_dict = {'Air_Temperature': self.str_datatype}
            # load the files individually
            for filename in filenames:
                file_path = os.path.join(directory_Temp, filename)
                new_data = pd.read_csv(os.path.join(directory_Temp, filename), delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
                new_data.index = pd.to_datetime(new_data.index, format='%Y%m%d%H%M')
                # Delete all not used columns 
                del new_data['Quality_Level']
                del new_data['Station_ID']
                del new_data['Error']
                del new_data['Air_Pressure']
                del new_data['Ground_Temperature']
                del new_data['Relative_Humidity']
                del new_data['Dew_Point']
                # concatenate the individual files to one big Air Temperature Dataframe
                Temp_data = pd.concat([Temp_data, new_data], axis=0)
            Temp_data = Temp_data[~Temp_data.index.duplicated(keep='first')]
            # Reduce the rows to the needed Datetimes
            Temp_data = Temp_data.loc[start_date:stop_date]
            # Save the data as preprocessed
            Temp_data.to_csv(os.path.join(directory_Weather, temp_data), sep=';')  
            with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
                file.write(str(str(datetime.now())+'\nSaved the preprocessed Temperature Data to CSV Data.\n\n'))


        # --------------End Import Weatherdata --------------------------------------------------
            
        # --------------Calculation of the PV Energy -------------------------------------------
        start_function = time.time()
        # Set Location for the PV System to Soest, Fachhochschule Suedwestfalen
        latitude = 51.560376
        longitude = 8.113911

        # Load Inverter and Module Database
        sand_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
        # cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
        cec_module = sand_modules['SolarWorld_Sunmodule_250_Poly__2013_']
        # cec_inverter = cec_inverters['Delta_Electronics__M6_TL_US__240V_']

        # Konfiguration of the PV System
        system = {
            # 'number of modules' : 24, # Anzahl der Module in der PV Anlage
            # 'number of modules in a String' : 12, # Anzahl aller in Reihe geschalteter Module eines Strings
            'module': cec_module,  # 
            # 'inverter': cec_inverter, #
            'surface_azimuth': pv_direction,  # Annahme: 180 Südausrichtung
            'surface_tilt': 30,  # Annahme: Neigungswinkel Süd 30
            'albedo': 0.2  # Annahme: Standard-Albedo
        }

        data['PV-Energy [kWh]'] = pd.Series(dtype=self.datatype)
        # Calcualtion Process                      
        # Iteration over every Timestep in the Timespan
        
        # Assisting Array to get the needed timesteps with 10 min steps in the needed Timeduration
        times = pd.date_range(start=start_date, end=stop_date, freq='10T')


        # Calculation of the Solar Position: Solar Zenith and Azimuth 
        solar_position = pvlib.solarposition.get_solarposition(times, latitude, longitude) # Timezone or no timezone # Wrong Solarposition Winter +1h Summer +2h
        
        # Calculation of the Air Mass 
        # If the Sun is under the horizon the calculation get an error
        relative_airmass = pvlib.atmosphere.get_relative_airmass(solar_position['apparent_zenith'].clip(upper=90))
        # calculation of the absolute air mass
        absolute_airmass = pvlib.atmosphere.get_absolute_airmass(relative_airmass)

        # Calculation of the total irradiance with dni, ghi, dhi, Surface-Reflection, Module-and Sun-Position 
        total_irrad_south = pvlib.irradiance.get_total_irradiance( surface_tilt=system['surface_tilt'], 
                                                                    surface_azimuth=system['surface_azimuth'], 
                                                                    surface_type='asphalt', 
                                                                    solar_zenith=solar_position['apparent_zenith'], 
                                                                    solar_azimuth=solar_position['azimuth'],
                                                                    dni=(Solar_data['Direct_Radiation_dni'] * (50/3)), 
                                                                    ghi=(Solar_data['Global_Radiation_ghi']* (50/3)), 
                                                                    dhi=(Solar_data['Defuse_Rediation_dhi']* (50/3)))
        
        # calculation of the angle of irradiance 
        aoi_south = pvlib.irradiance.aoi(surface_tilt=system['surface_tilt'], 
                                surface_azimuth=system['surface_azimuth'], 
                                solar_zenith=solar_position['zenith'], 
                                solar_azimuth=solar_position['azimuth'])
        

        # Calculation of the effective irradiance for the PV Modules
        effective_irradiance_south = pvlib.pvsystem.sapm_effective_irradiance(total_irrad_south['poa_direct'],
                                                                            total_irrad_south['poa_diffuse'],
                                                                            airmass_absolute=absolute_airmass,
                                                                            aoi=aoi_south,
                                                                            module=system['module'])
        
        # Calculation of the cell temperature of the PV modules
        temperature_south = pvlib.temperature.sapm_cell(temp_air=Temp_data['Air_Temperature'], wind_speed=Wind_data['Wind_speed'],
                                                a=-3.56, b=0.075, deltaT=3, poa_global= total_irrad_south['poa_global']) 
        
        # Calculation of the DC Power a 6kWp 
        dc_power_south = pvlib.pvsystem.pvwatts_dc(effective_irradiance_south, temperature_south, 1000, -0.004)

            
        # calculate the Output power of the inverter, input dc power, east + west
        ac_power = pvlib.inverter.pvwatts(dc_power_south, 1000) # W
            

        # save the AC Power of the Inverter in the data DataFrame 
        data['PV-Energy [kWh]'] = ac_power / (6*1000) # kWh ;  Umwandlung von Leistung in Energie 

        # resample to 5 Min and decrease the energy per 10 min to the half in 5 min
        data['PV-Energy [kWh]'] = (data['PV-Energy [kWh]'].ffill() / 2).astype(self.str_datatype)

        pv_south = data['PV-Energy [kWh]'].copy()
        pv_south.to_csv(os.path.join(directory_precalculated, south_pv_file), sep=';')

        data['PV-Energy [kWh]'] = data['PV-Energy [kWh]']  * peak_power_pv
        

        # plot the PV-Power
        # self.plot.print_pv_energy(data)
        end_function = time.time()
        print(f"Das Berechnen der PV-Daten dauert: {(end_function - start_function)}\n")
        
        # -------------End PV-Generation --------------------------------------------------------
        return data    


    def load_energy_prices(self, data):
        start_function = time.time()
        prices_path = os.path.join(self.related_path_data, self.original_data_path, 'Energy_Prices')       
        prices = pd.DataFrame()        
        new_data = pd.DataFrame()
        filenames = sorted([filename for filename in os.listdir(os.path.join(prices_path)) if filename.endswith(".csv")])
        # Set understandable Header Names missleading header name kWh (Sum of one year 1,000,000.00) it have to be Wh! normalised to 1000 kWh 
        column_names = ['Datetime', 'Energy Price [Cent/kWh]']
        dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
        # load the files individually
        for filename in filenames:
            path_prices = os.path.join(prices_path, filename)
            new_data = pd.read_csv(os.path.join(path_prices), delimiter=',', header=0, skiprows=2, names=column_names, dtype=dtype_dict, on_bad_lines='skip')
            # convert from Euro per MWh to Cent per kWh
            new_data['Energy Price [Cent/kWh]'] *= 0.1                    
            # convert to datetime format
            new_data['Datetime'] = pd.to_datetime(new_data['Datetime'], format='%Y-%m-%dT%H:%M%z', errors='coerce', utc=True)
            new_data['Datetime'] = new_data['Datetime'].dt.tz_localize(None) - pd.Timedelta(hours=1)
            # new_data['Datetime'] = new_data['Datetime'].dt.tz_localize(None) - pd.Timedelta(hours=1)
            # Set Datetime to Index
            new_data.set_index('Datetime', inplace=True)
            # concatenate the individual files to Price Dataframe
            prices = pd.concat([prices,new_data], axis=0)
            
        # finished loading the original data

        # Check whether the index is unique and, if necessary, ensure that it is unique (got error without)
        if not prices.index.is_unique:   
            prices = prices[~prices.index.duplicated(keep='first')]  
        data = pd.concat([data, prices], axis=1)
        data['Energy Price [Cent/kWh]'] = data['Energy Price [Cent/kWh]'].astype('float64')
        data['Energy Price [Cent/kWh]'] = data['Energy Price [Cent/kWh]'].ffill()
        data['Energy Price [Cent/kWh]'] = data['Energy Price [Cent/kWh]'].astype(self.str_datatype)
        print("Finished to load the energy prices!")
        start_time = time.time()
        with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nLoaded the Energy Prices.\n\n'))
        
        end_time = time.time()
        print(f"Das schreiben ins Log dauert: {(end_time - start_time)}\n")
            
        
        # self.plot.print_energy_prices(data)
        end_function = time.time()
        print(f"Das Einlesen der Börsenstrompreise dauert: {(end_function - start_function)}\n")
        return data



    def load_direct_marketing_data(self, data):
        start_function = time.time()
        path_prices = os.path.join(self.related_path_data, self.original_data_path, 'Market_Values', 'Monthly_Average_market_values.csv')       
        new_data = pd.DataFrame()
        column_names = ['Datetime', 'Monthly Average Price [Cent/kWh]']
        dtype_dict = {col: self.str_datatype for col in column_names if col != 'Datetime'}
        new_data = pd.read_csv(path_prices, delimiter=';', header=0, names=column_names, dtype=dtype_dict, index_col='Datetime')
        new_data.index  = pd.to_datetime(new_data.index, format='%d.%m.%Y %H:%M')
        data = pd.concat([data, new_data], axis=1)
        print(f"Das Einlesen der Monatsmarktwerte dauert: {(time.time() - start_function)}\n")
        return data
    #     start_function = time.time()
    #     # Average monthly market value : Marktwert Solar 
    #     # source: https://www.netztransparenz.de/de-de/Erneuerbare-Energien-und-Umlagen/EEG/Transparenzanforderungen/Marktpr%C3%A4mie/Marktwert%C3%BCbersicht
    #     a_2018 = ( 3.440,  4.038,  3.698,  2.954,  3.186,  4.251,  4.900,  5.595,  5.210,  5.325,  5.976,  5.612)
    #     a_2019 = ( 5.906,  4.213,  3.075,  3.172,  3.530,  2.910,  3.917,  3.376,  3.345,  3.788,  4.383,  3.696)
    #     a_2020 = ( 3.831,  2.319,  1.618,  0.890,  1.413,  2.473,  2.623,  3.321,  3.981,  3.269,  3.998,  4.811)
    #     a_2021 = ( 5.543,  4.499,  4.105,  4.551,  4.187,  6.864,  7.409,  7.681, 11.715, 12.804, 18.307, 27.075)
    #     a_2022 = (17.838, 11.871, 20.712, 14.566, 15.132, 18.940, 26.093, 39.910, 31.673, 12.904, 15.374, 24.661)
    #     a_2023 = (12.291, 12.343,  8.883,  8.002,  5.356,  7.124,  5.173,  7.334,  7.447,  6.763,  8,525,  6.592)
    #     a_2024 = ( 7.535,  5.875,  4.965,  3.795,  3.161,  4.635,  3.554,  4.263,  4.512,  6.752, 10.076, 11.171)

    #     data['Monthly Average Price [Cent/kWh]'] = pd.Series(dtype=self.datatype)
            
    #     for timestamp, row in data.iterrows():
    #         self.add_average_prices(data, timestamp, 2018, a_2018)
    #         self.add_average_prices(data, timestamp, 2019, a_2019)
    #         self.add_average_prices(data, timestamp, 2020, a_2020)
    #         self.add_average_prices(data, timestamp, 2021, a_2021)
    #         self.add_average_prices(data, timestamp, 2022, a_2022)
    #         self.add_average_prices(data, timestamp, 2023, a_2023)
    #         self.add_average_prices(data, timestamp, 2024, a_2024)

    #     with open(os.path.join(self.related_path_data, self.log_file_name), 'a') as file:
    #         file.write(str(str(datetime.now())+'\nLoaded the montly average market prices.\n\n'))
    #     end_function = time.time()
    #     print(f"Das Einlesen der Monatsmarktwerte dauert: {(end_function - start_function)}\n")
    #     return data

    # def add_average_prices(self, data, timestamp, year, array_prices):    
    #     if timestamp.year == year:
    #         data.at[timestamp, 'Monthly Average Price [Cent/kWh]'] = array_prices[timestamp.month-1]