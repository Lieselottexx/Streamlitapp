# Import Bibs
import matplotlib.pyplot as plt
import pickle as pl
import seaborn as sns
import pandas as pd


class Plot_Data():

    def __init__(self):
        
        pass

    def __del__(self):
        pass

    def average_load_profiles(self, list_plot_data, name_beh):
        fig, ax = plt.subplots()
        str_color = ['tab:gray', 'tab:green', 'tab:purple', 'tab:orange', 'tab:pink', 'tab:cyan']
        for number in range(len(name_beh)):
            data = pd.DataFrame()
            data = list_plot_data[number] 
            data = data * 60/15
            ax.plot(data, color=str_color[number],label=name_beh[number],  linewidth=1, drawstyle='steps')
        ax.plot((list_plot_data[len(name_beh)]* 60/15), color='tab:blue',label='Load Profiles',  linewidth=2, drawstyle='steps')
        ax.plot((list_plot_data[(len(name_beh)+1)]* 60/15), color='tab:red',label='SLP Profile',  linewidth=1, drawstyle='steps')
        ax.set_ylabel('Power in kW', color='k')
        ax.legend(loc='upper left')
        ax.grid()
        ax.set_xticks(['00:00', '02:00', '04:00', '06:00','08:00', '10:00', '12:00','14:00', '16:00','18:00', '20:00','22:00', '24:00'])



    def diff_behaviour_analysis(self, costs):
        fig, ((ax1, ax2, ax3)) = plt.subplots(1, 3, sharey='all')
        sns.boxplot(data=costs, x='Category Load', y='Gesamtkosten', ax=ax1)
        ax1.set_xlabel("Jahresdurchschnittsverbrauch des Haushalts")
        ax1.set_ylabel("Ersparnis durch den dynamischen Stromtarif")
        ax1.set_xticklabels(['< 2000 kWh', '< 3000 kWh', '< 4000 kWh', '< 8000 kWh']) 

        sns.boxplot(data=costs, x='Category PV', y='Gesamtkosten', ax=ax2)
        ax2.set_xlabel("Photovoltaik Anlagengröße")
        ax2.set_ylabel("Ersparnis durch den dynamischen Stromtarif")
        ax2.set_xticklabels(['0 kWp', '5 kWp', '10 kWp', '15 kWp']) 

        sns.boxplot(data=costs, x='Category Battery', y='Gesamtkosten', ax=ax3)
        ax3.set_xlabel("Batteriekapazität")
        ax3.set_ylabel("Ersparnis durch den dynamischen Stromtarif")
        ax3.set_xticklabels(['0 kWh', '3 kWh', '7 kWh', '12 kWh']) 
        
        ax1.set_title('Nach Jahresdurchschnittsverbrauch sortiert')
        ax2.set_title('Nach PV Anlagengröße sortiert')
        ax3.set_title('Nach Batteriekapazität sortiert')

        y_range = (-400, 400)
        # ax1.set_ylim(y_range)
        # ax2.set_ylim(y_range)
        # ax3.set_ylim(y_range)

        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)

    def print_self_consumption_optimisation(self, data, select_opti, result_column_names):
        y1_1_1_data = data['Load Energy [kWh]'].copy()
        y1_1_2_data = data['PV-Energy [kWh]'].copy()
        y1_2_1_data = data[select_opti[5]].copy()
        y1_2_2_data = data['Energy Price [Cent/kWh]'].copy()
        y1_3_1_data = data[result_column_names[0]].copy() # Battery Charge [kWh] 
        y1_3_2_data = data[result_column_names[1]].copy() # Battery Discharge [kWh] 
        y1_3_2_1_data = data['Load Energy [kWh]'].copy() # just store a default load energy to rewrite it
        y1_3_3_data = data[result_column_names[4]].copy() # Grid Feed-in [kWh]
        y1_3_4_data = data[result_column_names[3]].copy() # Supply from Grid [kWh]
        y1_4_1_data = data[result_column_names[2]].copy() # Battery SoC [%]


        y1_3_2_1_data[:] = 0
        y1_3_2_1_data[ y1_3_4_data > y1_1_1_data] = y1_3_1_data

        y1_1_1_data   = y1_1_1_data      * 60/5 # Load Energy [kWh] zu kW
        y1_1_2_data   = y1_1_2_data      * 60/5 # PV Energy [kWh] zu kW
        y1_3_1_data   = y1_3_1_data      * 60/5 # Battery Charge [kWh] zu kW
        y1_3_2_data   = y1_3_2_data      * 60/5 # Battery Discharge [kWh] zu kW
        y1_3_2_1_data = y1_3_2_1_data    * 60/5 # Battery Charge from Grid [kWh] zu kW
        y1_3_3_data   = y1_3_3_data      * 60/5 # Grid Feed-in [kWh] zu kW
        y1_3_4_data   = y1_3_4_data      * 60/5 # Supply from Grid [kWh] zu kW
    

        fig, (ax1, ax2, ax4, ax5) = plt.subplots(4, 1, sharex='all')
        ax1.plot(y1_1_1_data, color='tab:red', label='Total Consumption [kW]', linewidth=2 , drawstyle='steps')
        ax1.plot(y1_1_2_data, color='tab:orange',label='PV-Generation [kW]', drawstyle='steps')
        ax1.legend(loc='upper left')
        ax1.set_ylabel('Power in kW',color='k')


        ax2.plot(y1_4_1_data, color='tab:red', label='OPT: Battery SOC', linewidth=2)
        ax2.legend(loc='upper left')
        ax2.set_ylabel('SOC',color='r')
        ax3 = ax2.twinx()
        ax3.plot(y1_2_1_data, color='tab:green', label='Grid Supply Price [Cent/kWh]',  linewidth=2, drawstyle='steps')
        ax3.plot(y1_2_2_data, color='tab:cyan', label='Market Energy Price [Cent/kWh]',  linewidth=2, drawstyle='steps')
        ax3.legend(loc='upper right')
        ax3.set_ylabel('Price in Cent/kWh',color='g')


        ax4.plot(y1_3_1_data, color='tab:blue',label='OPT: Battery Charge [kW]',  linewidth=4, drawstyle='steps')
        ax4.plot(y1_3_2_data, color='tab:orange',label='OPT: Battery Discharge[kW]',  linewidth=3, drawstyle='steps')
        ax4.plot(y1_3_2_1_data, color='tab:green',label='OPT: Battery Charge from Grid [kW]',  linewidth=3, drawstyle='steps')
        ax4.legend(loc='upper left')
        ax4.set_ylabel('Power in kW',color='k')

        ax5.plot(y1_3_3_data, color='tab:pink',label='OPT: Grid Feed-in [kW]',  linewidth=2, drawstyle='steps')
        ax5.plot(y1_3_4_data, color='tab:green',label='OPT: Supply from Grid [kW]',  linewidth=1, drawstyle='steps')
        ax5.legend(loc='upper left')
        ax5.set_ylabel('Power in kW',color='k')

        ax1.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)
        ax2.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)
        ax4.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)
        ax5.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)
        # plt.show()
        

    def show(self):
        plt.show()
