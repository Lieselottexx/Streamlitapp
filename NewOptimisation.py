# import Bibs
from datetime import datetime, timedelta
import pandas as pd
import os
from scipy.optimize import linprog
import numpy as np

# Import Python Files
import Param
import Plot_Data as plot

class Optimisation():

    def __init__(self):
        self.plot_data = plot.Plot_Data()
        # Name for the protocol of the current calculation, log file
        self.log_file_name = "log.txt"
        self.data_path = Param.data_path

        self.datatype       = Param.datatype
        self.str_datatype   = Param.str_datatype
        pass

    def __del__(self):
        pass


    def select_optimisation(self, data , input_optimisation, select_opti):

        # Do not forget to copy the data DataFrame
        '''Input self optimisation: 
        0 - optimise_time, input_self_optimisation[0]
        1 - step_time, input_self_optimisation[1]
        2 - var_battery_capacity, input_self_optimisation[2]
        3 - var_battery_costs, input_self_optimisation[3]
        4 - var_battery_power, input_self_optimisation[4]
        5 - var_grid_power, input_self_optimisation[5]
        6 - static_feed_in_price, input_self_optimisation[6]
        7 - static_feed_in_bonus, input_self_optimisation[7]'''

        ''' Select Opti: wird in control gesetzt
        0 - Number of Optimisation [0]
        1 - Energy price: 0 - static, 1 - dynamic [1
        2 - Einspeisung: 0 - static, 1 - dynamic [2]
        3 - EEG: 0 - no EEG System, 1 - EEG System [3] 
        4 - Name of the CSV of the Optimisation [4]
        5 - energy price name of the column[5] 
        6 - feed in name of the column[6]'''
        
        

        # Calculation of the Feed-in price 
        data['Dynamic Feed-in Price [Cent/kWh]'] = pd.Series(dtype=self.str_datatype)
        market_bonus = input_optimisation[7] - data['Monthly Average Price [Cent/kWh]']
        data['Dynamic Feed-in Price [Cent/kWh]'] = np.where( market_bonus > 0, # condition
        data['Energy Price [Cent/kWh]'] + market_bonus, # if condition is right
        data['Energy Price [Cent/kWh]']).astype(self.str_datatype) # otherwise and everytime store as datatype

        
        data['Static Feed-in Price [Cent/kWh]'] = pd.Series(dtype=self.str_datatype)
        # if the optimisation is in the EEG Regulation:
        if select_opti[3] == 1:
           data['Static Feed-in Price [Cent/kWh]'] = input_optimisation[6]
        # if the optimisation is out of the EEG Regulation
        elif select_opti[3] == 0:
            data['Static Feed-in Price [Cent/kWh]'] = 0

        with open(os.path.join(self.data_path,self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nStart of the calculation of the Optimisation Number'+ str(input_optimisation[0])+ '.\n'))
            file.write(str("Used Parameter: \nOptimise Time: "+ str(input_optimisation[0])+"\nStep Time: "+ str(input_optimisation[1])+"  \n"))
            file.write(str("Battery Capacity: "+ str(input_optimisation[2])+"\nVariable Battery Costs: "+ str(input_optimisation[3])+"\n"))
            file.write(str("Battery Power: "+ str(input_optimisation[4])+"\nGrid Power: "+ str(input_optimisation[5])+"  \n"))
            file.write(str("Static feed-in Price EEG: "+ str(input_optimisation[6])+"  \n"))
            file.write(str("Static feed-in Bonus EEG: "+ str(input_optimisation[7])+"  \n\n"))

        data_opti = self.optimisation(data.copy(), select_opti, input_optimisation)
        return data_opti


    def optimisation(self, data, select_opti, input_optimisation ):
        # initialise the result columns of the optimisation 
        result_column_names =   ['Battery Charge [kWh]', 'Battery Discharge[kWh]', 
                                'Battery SOC', 'Supply from Grid [kWh]', 
                                'Grid Feed-in [kWh]']
        for names in result_column_names:
            data[names] = pd.Series(dtype=self.str_datatype)

        # variable to store the last SoC of the Battery to get a continuous SoC other the Time 
        previous_SoC = 0

        '''Input self optimisation: 
        0 - optimise_time, input_self_optimisation[0]
        1 - step_time, input_self_optimisation[1]
        2 - var_battery_capacity, input_self_optimisation[2]
        3 - var_battery_costs, input_self_optimisation[3]
        4 - var_battery_power, input_self_optimisation[4]
        5 - var_grid_power, input_self_optimisation[5]
        6 - static_feed_in_price, input_self_optimisation[6]
        7 - static_feed_in_bonus, input_self_optimisation[7] 
        8 - energy price name of the column[8]
        9 - feed in name of the column[9]'''

        
        ''' Select Opti:
        0 - Number of Optimisation [0]
        1 - Energy price: 0 - static, 1 - dynamic [1
        2 - Einspeisung: 0 - static, 1 - dynamic [2]
        3 - EEG: 0 - no EEG System, 1 - EEG System [3] 
        4 - Name of the CSV of the Optimisation [4]
        5 - energy price name of the column[5] 
        6 - feed in name of the column[6]'''

        for date in pd.date_range(start=data.index.min(), end=data.index.max(),freq=timedelta(hours=input_optimisation[1])):
            # Collection Inputs over the Time duration of the optimisation step
            load_data = data.loc[date:date+timedelta(hours=input_optimisation[0]),'Load Energy [kWh]'].copy().values
            pv_generation = data.loc[date:date+timedelta(hours=input_optimisation[0]),'PV-Energy [kWh]'].copy().values
            energy_price =  data.loc[date:date+timedelta(hours=input_optimisation[0]),select_opti[5]].copy().values
            feed_in_price =  data.loc[date:date+timedelta(hours=input_optimisation[0]),select_opti[6]].copy().values
            # Duration of optimisation, for all for-loops
            len_opti = len(load_data)

            '''
            Decision variables:
            X1 = Battery Charge
            X2 = Battery Discharge
            X3 = Battery SOC
            X4 = Supply from Grid
            X5 = Grid Feed-in
            '''
           
            # bounds for            x1                                  x2         x3                   x4              x5
            bounds    = [(0, input_optimisation[4]), (0, input_optimisation[4]), (0, 1), (0, input_optimisation[5]), (0, None)]

            # objective function 
            # If input_self_optimisation[6] stored a String its the dynamic feed in price, 
            # if its a float its stored the value of the static feed in price variable
            c_val = [0,
                    input_optimisation[3],
                    0,
                    energy_price, 
                    -feed_in_price] 
            
            A_eq_1 = [-1,   0.96,    0, 1, -1]
            A_eq_2 = [1/input_optimisation[2], -1/input_optimisation[2], -1,  0, 0]
            
            A_eq_1_1 = [0, 0, 0, 0, 0]
            A_eq_2_1 = [0, 0, 1, 0, 0]
            
            # Vektor for equality constrain equation
            '''b_eq   = [load_data - pv_generation, 0 ]'''

            # Matrix for unequality constrain equation
            # current Step

            if select_opti[3] == 1:
                # EEG-System: Battery charge from the grid is allowed
                A_ub_3 =   [0, 0, 0, 0, 1] # Limitation of feed-in to PV-Generation
                # previous Step
                A_ub_3_1 = [0, 0, 0, 0, 0]
                
                # EEG-System: Battery feed-in allowed
                A_ub_1 =   [0, -1, 0, 0, 1] # Limitation of feed-in to PV-Gen. and Battery discharge
                A_ub_2 =   [1,  0, 0, 0, 0] # Limitation of the Battery charging energy to PV-Generation
                # previous Step
                A_ub_1_1 = [0, 0, 0, 0, 0]
                A_ub_2_1 = [0, 0, 0, 0, 0]
            elif select_opti[3] == 0:
                pass
            else:
                pass
            
            
            # Vektor for unequality constrain equation
            '''b_ub = [pv_generation]'''

            # Construct the deepthness of the optimisation Time 
            # # construction of the objective vector
            limits = []
            limits = self.append_array(len_opti,bounds)
            c = []
            c = self.append_array(len_opti,c_val)
            
            # construction of the Matrix for equality constrain equation
            A_eq   = []            
            A_eq   =  self.append_constrains(len_opti,A_eq_1,A_eq_1_1)
            A_eq_cache = self.append_constrains(len_opti,A_eq_2, A_eq_2_1)
            for i in range(len(A_eq_cache)): A_eq.append(A_eq_cache[i])

            # construction of the vector for equality constrain equation 
            b_eq   = []
            diff =  load_data - pv_generation
            b_eq   =  self.append_array(1,diff)
            b_eq.append(-previous_SoC)
            b_eq_cache = self.append_array(len_opti-1,[0])
            for i in range(len(b_eq_cache)): b_eq.append(b_eq_cache[i])

            if select_opti[3] == 1:
                # construction of the Matrix for unequality constrain equation
                '''EEG System: Battery charge from the Grid is allowed'''
                A_ub   =  []
                A_ub   =  self.append_constrains(len_opti,A_ub_3,A_ub_3_1)
                # construction of the vector for equality constrain equation 
                b_ub   =  []
                b_ub   =  self.append_array(1,pv_generation)

                '''EEG System: Battery feed-in allowed'''
                # A_ub   =  []
                # A_ub   =  self.append_constrains(len_opti,A_ub_1,A_ub_1_1)
                # A_ub   =  self.append_constrains(len_opti,A_ub_2,A_ub_2_1)
                    
                # # construction of the vector for equality constrain equation 
                # b_ub   =  []
                # b_ub   =  self.append_array(1,pv_generation)
                # b_ub   =  self.append_array(1,pv_generation)
            else: 
                A_ub   =  []
                A_ub_0 = [0, 0, 0, 0, 0]
                A_ub   =  self.append_constrains(len_opti,A_ub_0,A_ub_0)
                b_ub   =  []
                b_ub   =  self.append_array(len_opti,[0])

            # calculation of the Linear Optimisation
            result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=limits)

            # Help date array
            date_ind = [date + i * timedelta(minutes=5) for i in range(len_opti)]

            # store the results if the optimisation was successful  
            if result.success:
                x_values = result.x
                res_data = []
                # build a list with one row of output values
                res_data = [[date_ind[i], x_values[i], x_values[i + len_opti], x_values[i + len_opti * 2], 
                            x_values[i + len_opti * 3], x_values[i + len_opti * 4]] for i in range(len_opti)]
                # Store the result in a DataFrame, like the original data Dataframe
                results_data = pd.DataFrame(res_data, columns=['Datetime', result_column_names[0],
                                                                 result_column_names[1], result_column_names[2], 
                                                                 result_column_names[3], result_column_names[4]])
                
                # Set the index to the Datetime, same as data Dataframe
                results_data.set_index('Datetime', inplace=True)
                next_iteration_date = date+timedelta(hours=input_optimisation[1])
                # If its not the last Step in the optimisation, Save the SoC for the next Step as inital condition
                if next_iteration_date in results_data.index:
                    previous_SoC = results_data.loc[next_iteration_date, result_column_names[2]].copy().item()

                # Store Result in the data DataFrame
                data.update(results_data[result_column_names].astype(self.str_datatype))
                    
            else: # if the Optimisation does not converge or something else went wrong Print an error in Terminal
                print("Optimierung fehlgeschlagen. Datum: ", date)

                with open(os.path.join(self.data_path,self.log_file_name), 'a') as file:
                    file.write(str(str(datetime.now())+'\nOptimisation failed: Date' + str(date) + '\n\n'))

        with open(os.path.join(self.data_path,self.log_file_name), 'a') as file:
            file.write(str(str(datetime.now())+'\nFinished optimisation calculation.\n\n'))

        # # Save Data as Self Consumption optimised    
        data.to_csv(os.path.join( self.data_path, select_opti[4]), sep=';')

        # print the optimisation result 
        # self.plot_data.print_self_consumption_optimisation(data, price_column_name, result_column_names)
        return data
    

    def append_array(self, len_opti, values):
        array = []
        for val in values:
            # if the value is just a number or one variable
            if isinstance(val, (float,int,list)):
                # append the number over the length of optimisation
                for i in range(len_opti):
                    array.append(val)
            # if the value is an array which changed over time
            elif isinstance(val, np.ndarray):
                # append the right value dependend on the time
                for i in range(len_opti):
                    array.append(val[i])
            else:
                # append the right value dependend on the time
                for i in range(len_opti):
                    array.append(val)
        return array
            
            # get out of values in arrays (one for the actual step, one for the previous step) 
            # a Matrix row with the deepth of every value of len_opti 
    def append_constrains(self, len_opti, values, values_minus_one):
        complete_array = []
        for j in range(len_opti): # j = current row 
            array = [] # array to append the current row to the complete array
            for k in range(len(values)):    # k = current value
                for i in range(len_opti):   # i = current column
                        # column and row are equal
                    if j == i: # includes the actual decision variable into the calculation
                        if isinstance(values[k], (float,int)):
                            array.append(values[k])
                        elif isinstance(values[k], np.ndarray):
                            cache_value = values[k]
                            array.append(cache_value[i])
                    # one column befor the row
                    elif j == (i+1): # includes the decision variable one step before into the calculation
                        if isinstance(values_minus_one[k], (float,int)):
                            array.append(values_minus_one[k])
                        elif isinstance(values_minus_one[k], np.ndarray):
                            cache_value = values_minus_one[k]
                            array.append(cache_value[i])                            
                    else: # every other not considerd decision variable gets factor 0
                            array.append(0)
            # append the row to the complete array and return this
            complete_array.append(array)
        return complete_array