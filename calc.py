import streamlit as st
import time
import pandas as pd
import datetime
import NewControl as c
import multiprocessing


control = c.Control()



def progress_update( progress_bar, status_text, progress, text):
    if progress <= 1:
        progress_bar.progress(progress)
        status_text.text(f"{text} läuft... {round(progress*100)}% abgeschlossen")
    return progress_bar, status_text



st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """, help="Hi")
if "calculating" not in st.session_state:
    st.session_state.calculating            = False
    st.session_state.consumption            = 3000
    st.session_state.controllable_device    = False
    st.session_state.dyn_cost               = False
    st.session_state.has_pv                 = False
    st.session_state.pv_power               = 5
    st.session_state.pv_compass             = "Süd"
    st.session_state.has_eeg                = False
    st.session_state.installation_date      = pd.to_datetime("2018-01-01")
    st.session_state.has_battery            = False
    st.session_state.battery_capacity       = 3
    st.session_state.battery_usage          = "Energie einspeisen"
    st.session_state.direct_market          = False


# Ergebnis-Speicher initialisieren
if "result_tables" not in st.session_state:
    st.session_state.result_tables = []

if "active_result_tab" not in st.session_state:
    st.session_state.active_result_tab = 0


# st.write(st.session_state)


# Stromverbrauch
st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")

st.markdown("""Diese Seite bietet eine Möglichkeit Kosteneinsparungen eines Haushalts für einen Wechsel auf einen dynamischen Stromtarif zu berechnen. 
            Darüber hinaus werden Ergebnisse aus einer wissenschaftlichen Arbeit präsentiert, für wen sich ein ein Wechsel auf einen dynamischen Stromtarif lohnt und welche Tarifmodelle sich zur Kostensenkung eignen.""")

st.markdown("""
                Weitere Informationen zu dem Rechner erhalten Sie auf der Seite Hintergrund Erklärungen in der Seitenleiste und unterhalb auswählbar. Beachten Sie, dass laufende Berechnungen gestoppt werden, wenn die Seite gewechselt wird. """)
st.page_link("explain.py", label="Hintergrund Erklärungen")
st.divider()
st.markdown(""" ##### Technischer Hinweis und Haftungsausschluss: """)
           
st.info("""Die auf dieser Website durchgeführten Berechnungen erfolgen auf Grundlage vereinfachter Modelle, definierter Annahmen sowie idealisierter Randbedingungen. Abweichungen zwischen den berechneten Werten und realen Gegebenheiten sind möglich und systembedingt. Die Ergebnisse dienen ausschließlich der unverbindlichen Orientierung und stellen keine belastbare Planungs- oder Entscheidungsgrundlage dar. Es wird keine Haftung für die Richtigkeit, Vollständigkeit oder Anwendbarkeit der ausgegebenen Ergebnisse übernommen.
""")
st.divider()
# -------------------------- Calculation ---------------------------------------

st.divider()
st.markdown("""## Berechnung """)

with st.container(border=True):
    st.markdown("""##### Jährlicher Stromverbrauch""")
    st.slider("Haushalts-Stromverbrauch in kWh über ein Jahr", 1000, 8000, key="consumption", step=500, help="Bitte wählen Sie ihren jährlichen Haushaltsstromverbrauch aus. Bei Haushalten mit PV-Anlagen mit Eigenverbauch ist der gesamte Verbrauch anzugeben, nicht nur der Netzbezug.") #, disabled=st.session_state.get("calculating"))

with st.container(border=True):
    st.markdown("""##### Steuerbare Verbrauchseinrichtungen nach EnWG 14a """)
    st.checkbox("Ich besitze eine Wärmepumpe, einen Batteriespeicher oder eine Wallbox die als steuerbare Verbrauchseinrichtung gilt.", key="controllable_device", help="Zu steuerbaren Verbrauchseinrichtungen zählen Wärmepumpen, Batteriespeicher und Wallboxen die nach Januar 2024 installiert worden sind und eine elektrische Anschlussleistung von 4,2 kWh überschreiten. Diese Angabe ist besonders interessant da damit die Möglichkeit auf zeitvariable Netzentgelte besteht.")  

# PV-Anlage
with st.container(border=True):
    st.markdown("""##### Photovoltaik Anlage""")
            
    st.checkbox("Ich besitze eine PV-Anlage.", key="has_pv") #, disabled=st.session_state.get("calculating", False))
    if st.session_state.get("has_pv", False):
        st.slider("Installierte PV-Leistung (kWp)", 1, 25, step=1, key="pv_power") #, disabled=st.session_state.get("calculating", False))
        direction_map = { "Nord": 0, 'Nord-Ost': 45, "Ost": 90, 'Süd-Ost': 135, "Süd": 180, "Süd-West": 225,  "West": 270}
        if "pv_compass" not in st.session_state:
            st.session_state.pv_compass = "Süd"
        st.selectbox("Ausrichtung der PV-Anlage", list(direction_map.keys()), key="pv_compass") #, disabled=st.session_state.get("calculating", False))
        st.session_state.pv_direction = direction_map[st.session_state.pv_compass]
        st.checkbox("Ich bekomme eine geförderte Einspeisevergütung nach dem EEG.", key="has_eeg")  

        # EEG-Vergütung
        # st.checkbox("Ist Ihre Anlage noch innerhalb der 20 Jahren garantierter EEG-geförderter Einspeisevergütung?", key="has_eeg", help="Sollte Ihre PV-Anlage bereits ausgefördert sein, könnte sich in der Zukunft ein netzdienliches Verhalten auszahlen, welches in dem Fall der Nicht-Auswahl berechnet wird.")
        if st.session_state.get("has_eeg", False):
            st.session_state.installation_date = pd.to_datetime(st.date_input("Installationsdatum der PV-Anlage", 
                                                                                value=datetime.date(2025, 6, 1), 
                                                                                min_value=datetime.date(2009, 1, 1), 
                                                                                max_value=datetime.date(2025, 6, 1), help="Das Installationsdatum gibt an wie hoch die Einspeisevergütung zu dem Zeitpunkt war, die Sie über 20 Jahre zugesichtert bekommen haben. Das früheste Installationsdatum welches ausgewählt werden kann beträgt Jan. 2009, da ab diesem Zeitpunkt der Eigenverbrauch vom selbsterzeugtem Strom ermöglicht wurde. Sollte Ihr Installationsdatum vor 2009 liegen, wählen Sie die Einspeisevergütung ab und können sich so ausrechnen welchen Vorteil der Eigenverbauch hat, nach Ablauf der 20 Jahre fester Einspeisevergütung.")) #, disabled=st.session_state.get("calculating", False)))
        else:
            st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")
    else:
        st.session_state.pv_power = 0
        st.session_state.pv_direction = 0
        # st.session_state.has_eeg = 0
        st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")


# Batterie
with st.container(border=True):
    st.markdown("""##### Angaben zum Batteriespeicher""")

    st.checkbox("Ich besitze einen Batteriespeicher.", key="has_battery") #, disabled=st.session_state.get("calculating", False))

    if st.session_state.get("has_battery", False):
        st.slider("Batteriekapazität (kWh)", 1, 20, 5, step=1, key="battery_capacity") #, disabled=st.session_state.get("calculating", False))
        st.selectbox("Batterieverhalten zum Netz", ["Energie einspeisen", "Energie aus dem Netz beziehen"], 
                                                        key="battery_usage") #, disabled=st.session_state.get("calculating", False))
    else:
        st.session_state.battery_capacity = 0
        st.session_state.is_eeg_battery = 0


opti_numbers = []
ses = st.session_state
if      not ses.has_pv and  not ses.controllable_device and not ses. has_eeg: 
    opti_numbers = [5, 7]
elif    not ses.has_pv and  not ses.controllable_device and     ses. has_eeg:
    opti_numbers =[1, 3] 
elif    not ses.has_pv and      ses.controllable_device and not ses. has_eeg: 
    opti_numbers =[5, 7, 13, 15]
elif        ses.has_pv and  not ses.controllable_device and not ses. has_eeg: 
    opti_numbers =[5, 6, 7, 8]
elif        ses.has_pv and  not ses.controllable_device and     ses. has_eeg: 
    opti_numbers =[1, 2, 3, 4]
elif        ses.has_pv and      ses.controllable_device and not ses. has_eeg: 
    opti_numbers =[5, 6, 7, 8, 13, 14, 15, 16]
elif        ses.has_pv and      ses.controllable_device and     ses. has_eeg: 
    opti_numbers =[1, 2, 3, 4, 9, 10, 11, 12]
else:
    pass

# Falls nur eine Batterie vorhanden ist ohne PV
# kann auch nur eine Direktvermarktung ohne EEG stattfinden. 
# Mit 5 wird trotzdem verglichen, da sie dort nur einspeisen kann, sprich die batterie tut nix
if st.session_state.has_pv == 0 and st.session_state.has_battery == 1:
    opti_numbers =[5, 17, 18, 19, 20, 21]





opti_dict = {i: {"select": None} for i in opti_numbers}

for key in opti_dict:
    opti_dict[key]["select"] = control.select_optimisation_behaviour(key)



st.divider()        
# Berechnung starten
if "results" not in st.session_state:
    st.session_state.results = []




if st.button("Berechnung starten", disabled=st.session_state.get("calculating", False)):
    st.session_state.calculating = True
    if st.session_state.calculating == True:
        st.info("Die Berechnung kann je nach Haushaltstyp  1 bis 2 Minuten dauern, bitte haben Sie Geduld.")
    
    st.toast("Berechnung läuft")
    
    
    st.session_state.loadprofile = st.session_state.consumption # loadprofiles[st.session_state.consumption]

    data, averageEnergyHousehold =  control.data_generator.loadData(st.session_state.loadprofile,
                                                                        st.session_state.pv_direction, 
                                                                        st.session_state.pv_power,
                                                                        st.session_state.battery_capacity) 
    
    
    data = control.price_generator.calculate_energy_prices( data, averageEnergyHousehold,
                                                                st.session_state.controllable_device)



    month_pv_installation = st.session_state.installation_date.month
    year_pv_installation  = st.session_state.installation_date.year
    static_feed_in_price,  static_bonus_feed_in =  control.get_eeg_prices(year_pv_installation,month_pv_installation, st.session_state.pv_power)

    battery_power = st.session_state.battery_capacity *  control.min_data/60 

    input_optimisation =    [ control.optimise_time,  control.step_time, st.session_state.battery_capacity,
                                 control.battery_costs,  battery_power, 
                                 control.grid_power,  static_feed_in_price,  static_bonus_feed_in]
    battery_usage = st.session_state.battery_usage
    peak_power_pv = st.session_state.pv_power

    # Falls nur eine Batterie vorhanden ist ohne PV
    # kann auch nur eine Direktvermarktung ohne EEG stattfinden. 
    # Mit 5 wird trotzdem verglichen, da sie dort nur einspeisen kann, sprich die batterie tut nix
    if st.session_state.has_pv == 0 and st.session_state.has_battery == 1:
        battery_usage = "Energie einspeisen"

    st.toast("Das optimierte Lastverhalten wird berechnet.")
    queue = multiprocessing.Queue()
    processes = {}
    for key in opti_dict:
        processes[key] = multiprocessing.Process(
        target=control.opimisation.select_optimisation,
        args=(data, input_optimisation, opti_dict[key]["select"], battery_usage, peak_power_pv, queue, key)
        )
        processes[key].start()

    
    with st.spinner("Ihr Lastverhalten wird berechnet..."):
        while any(p.is_alive() for p in processes.values()):
            while not queue.empty():
                task_id, progress = queue.get()

                if isinstance(task_id, str) and task_id.startswith("Result"):
                    try:
                        _, key_str = task_id.split()
                        key = int(key_str.replace(":", ""))
                        opti_dict[key]["result"] = progress
                        print(f"Result {key} stored.")
                    except Exception as e:
                        print(f"Fehler beim Parsen von Result-ID {task_id}: {e}")



    st.toast("Die Jahreskosten werden berechnet.")
    for key in opti_dict:
        processes[key].join()
    
    for key in opti_dict:
        opti_dict[key]["cost"], opti_dict[key]["co2"] = control.analysis.single_cost_batterycycle_calculation(opti_dict[key]["result"], opti_dict[key]["select"], input_optimisation, peak_power_pv)
        if key == 1 or key == 5:
            origin_key = key
        else:
            if opti_dict[key]["select"][2] == "Direktvermarktung": 
                # Fixkosten der Direktvermarktung von LUOX die nicht zu vernachlässigen sind:
                # knapp unter 2 x Peakleistung "Vermarktungskosten"
                # 72 bzw 90 Euro jährliche fixe Kosten
                zusatzkosten = 72 if st.session_state.pv_power < 10 else 90
                print("Zusatzkosten: ", zusatzkosten, "\n+ ", (st.session_state.pv_power * 2) )
                opti_dict[key]["benefit"] = opti_dict[origin_key]["cost"]['2024-12-31'] - opti_dict[key]["cost"]['2024-12-31'] - st.session_state.pv_power * 2 - zusatzkosten
            else:
                opti_dict[key]["benefit"] = opti_dict[origin_key]["cost"]['2024-12-31'] - opti_dict[key]["cost"]['2024-12-31']
            opti_dict[key]["co2_benefit"] = opti_dict[origin_key]["co2"]['2024-12-31'] - opti_dict[key]["co2"]['2024-12-31']
            # st.write(f"{benefit} = {costs_evo['2024-12-31']} - {costs_selected['2024-12-31']}")
        print(opti_dict[key], opti_dict[key]["cost"])
    st.toast("Fertig, die Ergebnisse sind da!")




    # Ergebnis-Daten aus opti_dict in DataFrame umwandeln
    try:
        benefit_rows = []
        for key in opti_dict:
            if "benefit" not in opti_dict[key] or key in (1, 5):
                continue
            
            opti_sel = opti_dict[key].get("select", ["", "Tarif N/A", "EEG N/A"])
            benefit_rows.append({
                "Nr.": key,
                "Stromtarif": opti_sel[1],
                "Einspeisetarif": opti_sel[2],
                "Ersparnis (€)": round(opti_dict[key]["benefit"], 2),
                "CO2 Ersparnis (kg)": round(opti_dict[key]["co2_benefit"], 2)
            })

        # DataFrame erzeugen
        df_results = pd.DataFrame(benefit_rows)

        # Tabelle im SessionState speichern
        st.session_state.result_tables.append(df_results)

        # Neuen Tab aktiv setzen
        st.session_state.active_result_tab = len(st.session_state.result_tables) - 1

    except Exception as e:
        st.error(f"Fehler beim Erstellen der Ergebnistabelle: {e}")

    st.session_state.calculating = False


if st.button("Berechnung stoppen"):
    st.session_state.calculating = False
    st.rerun()
st.write("### Ergebnisse")

if len(st.session_state.result_tables) == 0:
    st.info("Noch keine Berechnungen durchgeführt.")
else:
    tab_labels = [f"Berechnung {i+1}" for i in range(len(st.session_state.result_tables))]
    active = st.session_state.active_result_tab

    tabs = st.tabs(tab_labels)

    for i, tab in enumerate(tabs):
        with tab:
            st.write(f"### Ergebnis {i+1}")

            st.dataframe(
                st.session_state.result_tables[i],
                use_container_width=True
            )

            st.markdown(
                ":deciduous_tree: Zum Vergleich, eine Buche nimmt durchschnittlich **35 kg CO₂/Jahr** auf."
            )



# # Ergebnisse anzeigen
# st.write("### Ergebnisse")
# st.markdown("""Die Ergebnisse der Berechnungen geben die Kosteneinsparung an, die angefallen wären, hätte man im Jahr 2024 den Stromtarif gewechselt. Ist das Ergebnis negativ, wären höhere Kosten angefallen bei einem Wechsel gegenüber dem festen Stromtarif in Kombination mit fester Einspeisevergütung für die ins Netz eingespeiste Energie. """)

# benefit_keys = [key for key in opti_dict if "benefit" in opti_dict[key]]
# header_cols = st.columns([1, 3, 3, 2, 2])
# header_cols[0].markdown("**Nr.**")
# header_cols[1].markdown("**Stromtarif**")
# header_cols[2].markdown("**Einspeisetarif**")
# header_cols[3].markdown("**Ersparnis**")
# header_cols[4].markdown("**CO2 Ersparnis**")
# if not benefit_keys:
#     st.info("Es wurden noch keine Optimierungsergebnisse berechnet.")
# else:
#     try:
#         # Keys sortieren nach Benefit-Wert, absteigend
#         sorted_keys = sorted(benefit_keys, key=lambda k: opti_dict[k]["benefit"], reverse=True)

#         for key in sorted_keys:
#             if key in (1, 5):  # Diese ggf. ausblenden
#                 continue

#             opti_sel = opti_dict[key].get("select", ["", "Tarif N/A", "EEG N/A"])
#             opti_ben = opti_dict[key]["benefit"]
#             opti_co2 = opti_dict[key]["co2_benefit"]

#             col1, col2, col3, col4, col5 = st.columns([1, 3, 3, 2, 2])

#             col1.write(f"**{key}.**")
#             col2.write(f"**{opti_sel[1]}**")
#             col3.write(f"**{opti_sel[2]}**")
#             col4.write(f"**{round(opti_ben, 2)} €**")
#             col5.write(f"**{round((opti_co2), 2)} kg CO2**")

#         st.markdown(":deciduous_tree: Zum Vergleich, eine Buche nimmt durchschnittlich 35 kg CO2 pro Jahr auf. ")
#         st.markdown(" :small[Stiftung Unternehmen Wald, \"Wie viel Kohlendioxid (CO2) speichert der Baum bzw. der Wald\", [Online]. Verfügbar:https://www.wald.de/waldwissen/wie-viel-kohlendioxid-co2-speichert-der-wald-bzw-ein-baum/. [Zugriff am: 10. Juni 2025]. ]")
#         # Bund naturschutz hat auch auf diese Quelle verwiesen.. https://traunstein.bund-naturschutz.de/wald/baeume-pflanzen-gegen-den-klimawandel-1
#     except Exception as e:
#         st.error(f"Fehler bei der Ergebnisanzeige: {e}")
    


