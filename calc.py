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



# Stromverbrauch
st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")
# st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """, help="Hi")
"""
Ob sich ein Wechsel auf dynamische Stromtarife für Haushalte lohnt, 
hängt von vielen verschiedenen Faktoren ab. Zudem gibt es die unterschiedlichsten Tarifmodelle, 
um den Bezugspreis zeitveränderlich zu nutzen. Dies kann in Summe für viel Intransparenz sorgen.

Diese Website soll Ihnen einen Überblick über die verschiedenen Möglichkeiten geben. 
Mithilfe des Berechnungstools soll aufzeigt werden, wie viel ein Haushalt 
gegenüber der normalen Tarifstruktur mindestens einsparen könnte. 
Die daraus resultiurenden Ergebnisse können Ihnene einen Überblick ermöglichen, 
welche Auswirkungen die einzelönen Tarifmodelle in kombination mit Ihrem individuellem Haushalt haben.
"""

with st.container(border=True):
    st.page_link("explain.py", label="Hintergrund Erklärungen")
st.divider()
# st.markdown(""" ##### Technischer Hinweis und Haftungsausschluss: """)
           
# st.info("""Die auf dieser Website durchgeführten Berechnungen erfolgen auf Grundlage vereinfachter Modelle, definierter Annahmen sowie idealisierter Randbedingungen. Abweichungen zwischen den berechneten Werten und realen Gegebenheiten sind möglich und systembedingt. Die Ergebnisse dienen ausschließlich der unverbindlichen Orientierung und stellen keine belastbare Planungs- oder Entscheidungsgrundlage dar. Es wird keine Haftung für die Richtigkeit, Vollständigkeit oder Anwendbarkeit der ausgegebenen Ergebnisse übernommen.
# """)
# st.divider()
# -------------------------- Calculation ---------------------------------------


st.markdown("""## Berechnung """)
st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """)
with st.container(border=True):
    st.markdown("##### Jährlicher Stromverbrauch")

    st.slider(
        "Haushalts-Stromverbrauch in kWh über ein Jahr",
        1000,
        8000,
        step=500,
        # value=st.session_state.consumption,
        key="consumption",
        help=(
            "Bitte wählen Sie Ihren jährlichen Haushaltsstromverbrauch aus. "
            "Bei Haushalten mit PV-Anlage ist der Gesamtverbrauch anzugeben, "
            "nicht nur der Netzbezug."
        ),
    )

# ----------------------------------------------------------------------------------------   
with st.container(border=True):

    st.markdown("##### Netzbetreiber")
    st.selectbox(
        "Auswahl des Netzbetreibers",
        ["Stadtwerke Soest", "Westnetz", "Stadtwerke Lippstadt", "Stadtwerke Werl"],
        key="netzbetreiber",
        # disabled=not st.session_state.has_battery,
        help="Der Netzbetreiber bestimmt die Höhe der Netzentgelte, die im Strompreis enthalten sind, die von Ihnen für die bezogenen " \
        "elektrische Energie gezahlt werden. Im Raum Soest liegt dies bei rund 7 - 12 Cent/kWh."
        )

    st.checkbox(
        "Ich besitze eine Wärmepumpe, einen Batteriespeicher, Klimaanlage oder eine Wallbox "
        "als sogenannte steuerbare Verbrauchseinrichtung.",
        # value=st.session_state.controllable_device,
        key="controllable_device",
        help=(
            """Steuerbare Verbrauchseinrichtungen können die aufgezählten Gerätetypen sein, die seit Jan. 2024
            mit einer Leistung größer 4,2 kW in Betrieb genommen wurden.
            Diese steuerbaren Verbrauchseinrichtungen ermöglichen die Nutzung zeitvariable Netzentgelte, die ggf. zusätzlich Ersparnisse bieten. """
            ),
        )

# ----------------------------------------------------------------------------------------  

direction_map = {
            "Nord": 0,
            "Nord-Ost": 45,
            "Ost": 90,
            "Süd-Ost": 135,
            "Süd": 180,
            "Süd-West": 225,
            "West": 270,
            }
# PV-Anlage
with st.container(border=True):
    st.markdown("##### Photovoltaik-Anlage")

    st.checkbox("Ich besitze eine PV-Anlage.", 
                # value=st.session_state.has_pv,
                key="has_pv"
                )
    if st.session_state.get("has_pv", False):
        st.slider(
            "Installierte PV-Leistung (kWp)",
            1,
            25,
            step=1,
            # value=st.session_state.pv_power,
            key="pv_power",
            disabled=not st.session_state.has_pv,
        )

        

        st.selectbox(
            "Ausrichtung der PV-Anlage",
            list(direction_map.keys()),
            index=list(direction_map.keys()).index(st.session_state.pv_compass),
            key="pv_compass",
            disabled=not st.session_state.has_pv,
        )



        st.checkbox(
            "Ich erhalte eine geförderte Einspeisevergütung nach EEG.",
            # value=st.session_state.has_eeg,
            key="has_eeg",
            #disabled=not st.session_state.has_eeg,
            )
        if st.session_state.get("has_eeg", False):
            st.date_input(
                "Installationsdatum der PV-Anlage",
                # value=st.session_state.installation_date,
                key="installation_date",
                min_value=datetime.date(2009, 1, 1),
                max_value=datetime.date(2025, 6, 1),
                help=(
                    "Das Installationsdatum bestimmt die Höhe der EEG-Einspeisevergütung "
                    "über einen Zeitraum von 20 Jahren."
                ),
            )
    

    pv_direction = direction_map.get(st.session_state.pv_compass, 180)
# ----------------------------------------------------------------------------------------  
# Batterie
with st.container(border=True):
    st.markdown("##### Angaben zum Batteriespeicher")

    st.checkbox("Ich besitze einen Batteriespeicher.", 
                # value=st.session_state.has_battery,
                key="has_battery"
                )
    if st.session_state.get("has_battery", False):
        st.slider(
            "Batteriekapazität (kWh)",
            1,
            20,
            step=1,
            # value=st.session_state.battery_capacity,
            key="battery_capacity",
            disabled=not st.session_state.has_battery,
        )

# ----------------------------------------------------------------------------------------  
with st.container(border=True):
    st.markdown("##### Optional: Direktvermarktung")

    st.checkbox("Ich möchte die Direktvermarktung an der Strombörse der ins Netz eingespeisten Energie in Betracht ziehen.", 
                # value=st.session_state.direct,
                key="direct",
                help="Erzeugungsanlagen oder Batteriespeicher haben die Möglichkeit zum " \
                "Bösenstrompreis Energie ins Netz einzuspeisen, und können so von den Schwankungen " \
                "des Bösenstrompreises profitieren. "
                )


# ----------------------------------------------------------------------------------------  

opti_numbers = []
ses = st.session_state
if ses.direct:
    #'''Mit Direktvermarktung '''
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
else:

    #'''Ohne Direktvermarktung '''
    if      not ses.has_pv and  not ses.controllable_device and not ses. has_eeg: 
        opti_numbers = [5, 7]
    elif    not ses.has_pv and  not ses.controllable_device and     ses. has_eeg:
        opti_numbers =[1, 3] 
    elif    not ses.has_pv and      ses.controllable_device and not ses. has_eeg: 
        opti_numbers =[5, 7, 13, 15]
    elif        ses.has_pv and  not ses.controllable_device and not ses. has_eeg: 
        opti_numbers =[5, 7]
    elif        ses.has_pv and  not ses.controllable_device and     ses. has_eeg: 
        opti_numbers =[1, 3]
    elif        ses.has_pv and      ses.controllable_device and not ses. has_eeg: 
        opti_numbers =[5, 7,13, 15]
    elif        ses.has_pv and      ses.controllable_device and     ses. has_eeg: 
        opti_numbers =[1, 3, 9, 11]
    else:
        pass


    # Falls nur eine Batterie vorhanden ist ohne PV
    # kann auch nur eine Direktvermarktung ohne EEG stattfinden. 
    # Mit 5 wird trotzdem verglichen, da sie dort nur einspeisen kann, sprich die batterie tut nix
    if st.session_state.has_pv == 0 and st.session_state.has_battery == 1:
        opti_numbers =[5, 21]





# Liste der opti_numbers, für die nur ein Eintrag erzeugt wird
exclude_numbers = [1, 5, 6, 8, 14, 16, 17, 18, 19, 20, 21]

opti_dict = {}
for i in opti_numbers:
    if i in exclude_numbers:
        # Nur ein Eintrag
        opti_dict[i] = {"select": control.select_optimisation_behaviour(i),
                        "battery_usage": "Energie aus dem Netz beziehen"}  # Standardwert
    else:
        # Zwei Einträge, man kann die Keys z.B. i*10+0 und i*10+1 verwenden, oder i+'_in' / i+'_out'
        opti_dict[i] = {"select": control.select_optimisation_behaviour(i),
                                        "battery_usage": "Energie einspeisen"}
        opti_dict[f"{i}_bezug"] = {"select": control.select_optimisation_behaviour(i),
                                  "battery_usage": "Energie aus dem Netz beziehen"}

st.divider()        
# Berechnung starten
if "results" not in st.session_state:
    st.session_state.results = []



"""
Die Berechnung wird mit einem Datensatz aus dem gesamten Jahr 2024 durchgeführt. 
Die darin enthaltene Daten beinhalten zum Beispiel das Wetter und den Börsenstrompreis des gesamten Jahres.

Das Ergebnis der Berechnung zeigt die minimale Ersparnis, da alle erdenklichen Zusatzkosten bereits eingerechnet werden 
und sich Ihr Verbrauchsverhalten nicht ändert. Beispielsweise sind die Kosten für die 
verstärkte Nutzung der Batterie bereits mit einbezogen. 
Zusätzliche zeitliche Verschiebungen des Verbrauchsverhaltens, bspw. Wärmepumpen oder Elektroautos,
sind noch nicht mit einbezogen und können bei vorteilhaftem Einsatz zusätzliche Ersparnisse bringen.


"""


st.divider()


if st.button("Berechnung starten", disabled=st.session_state.get("calculating", True)):
    st.session_state.calculating = True
    st.toast("Berechnung läuft")

    # Voreinstellung zurücksetzen
    if not st.session_state.has_pv :
        st.session_state.pv_power = 0
    if not st.session_state.has_battery:
        st.session_state.battery_capacity = 0


    # ===================== SNAPSHOT =====================
    snapshot = {
        "consumption": st.session_state.consumption,
        "controllable_device": st.session_state.controllable_device,
        "has_pv": st.session_state.has_pv,
        "pv_power": st.session_state.pv_power,
        "pv_compass": st.session_state.pv_compass,
        "pv_direction": pv_direction,
        "installation_date": st.session_state.installation_date,
        "has_battery": st.session_state.has_battery,
        "battery_capacity": st.session_state.battery_capacity,
        "netzbetreiber": st.session_state.netzbetreiber,
        "direct": st.session_state.direct,
        # "battery_usage": st.session_state.battery_usage,
    }



    st.session_state.result_tables.append(
        {"settings": snapshot, "results": None}
    )
    run_id = len(st.session_state.result_tables) - 1
    st.session_state.active_result_tab = run_id


    
    s = st.session_state.result_tables[run_id]["settings"]

    month_pv_installation = s["installation_date"].month
    year_pv_installation = s["installation_date"].year

    static_feed_in_price, static_bonus_feed_in = control.get_eeg_prices(
        year_pv_installation,
        month_pv_installation,
        s["pv_power"],
    )

    battery_power = s["battery_capacity"] * control.min_data / 60

    input_optimisation = [
        control.optimise_time,
        control.step_time,
        s["battery_capacity"],
        control.battery_costs,
        battery_power,
        control.grid_power,
        static_feed_in_price,
        static_bonus_feed_in,
    ]

    # battery_usage = s["battery_usage"]
    peak_power_pv = s["pv_power"]

    # if not s["has_pv"] and s["has_battery"]:
    #     battery_usage = "Energie einspeisen"


    data, averageEnergyHousehold = control.data_generator.loadData(
        s["consumption"],
        s["pv_direction"],
        s["pv_power"],
        s["battery_capacity"],
        )

    data = control.price_generator.calculate_energy_prices(
        data,
        averageEnergyHousehold,
        s["controllable_device"],
        s["netzbetreiber"],
        )

    st.toast("Das optimierte Lastverhalten wird berechnet.")

    queue = multiprocessing.Queue()
    processes = {}

    for key in opti_dict:
        processes[key] = multiprocessing.Process(
            target=control.opimisation.select_optimisation,
            args=(
                data,
                input_optimisation,
                opti_dict[key]["select"],
                opti_dict[key]["battery_usage"],
                peak_power_pv,
                queue,
                key,
            ),
        )
        processes[key].start()

    with st.spinner("Ihr Lastverhalten wird berechnet..."):
        while any(p.is_alive() for p in processes.values()):
            while not queue.empty():
                task_id, progress = queue.get()
                if isinstance(task_id, str) and task_id.startswith("Result"):
                    key_str = task_id.split()[1].replace(":", "")
                    if key_str in opti_dict:
                        dict_key = key_str
                    elif key_str.isdigit() and int(key_str) in opti_dict:
                        dict_key = int(key_str)
                    else:
                        # Für Keys mit '_bezug'
                        dict_key = key_str
                    
                    opti_dict[dict_key]["result"] = progress



    st.toast("Die Jahreskosten werden berechnet.")
    for key in opti_dict:
        processes[key].join()

    for key in opti_dict:
        opti_dict[key]["cost"], opti_dict[key]["co2"] = (
            control.analysis.single_cost_batterycycle_calculation(
                opti_dict[key]["result"],
                opti_dict[key]["select"],
                input_optimisation,
                peak_power_pv,
            )
        )

        if key in (1, 5):
            origin_key = key
            continue

        benefit = opti_dict[origin_key]["cost"]["2024-12-31"] - opti_dict[key]["cost"]["2024-12-31"]

        if opti_dict[key]["select"][2] == "Direktvermarktung":
            zusatzkosten = 72 if s["pv_power"] < 10 else 90
            benefit -= s["pv_power"] * 2 + zusatzkosten

        opti_dict[key]["benefit"] = benefit
        opti_dict[key]["co2_benefit"] = (
            opti_dict[origin_key]["co2"]["2024-12-31"]
            - opti_dict[key]["co2"]["2024-12-31"]
        )
    
    try:
        BATTERY_USAGE_FALLBACK_LABEL = "Einspeisen und Netzbezug"

        BATTERY_USAGE_OVERRIDE_OPTIS = {
            6, 8, 14, 16, 17, 18, 19, 20
            }

        BATTERY_USAGE_OVERRIDE = {
            opti: BATTERY_USAGE_FALLBACK_LABEL
            for opti in BATTERY_USAGE_OVERRIDE_OPTIS
            }
        benefit_rows = []

        for key in opti_dict:
            if key in (1, 5) or "benefit" not in opti_dict[key]:
                continue

            opti_sel = opti_dict[key]["select"]
            # Originalnummer extrahieren (z.B. "7_bezug" → 7)
            opti_number = int(str(key).split("_")[0])

            # Batterie-Text bestimmen
            if opti_number in BATTERY_USAGE_OVERRIDE:
                battery_usage_label = BATTERY_USAGE_OVERRIDE[opti_number]
            else:
                battery_usage_label = opti_dict[key]["battery_usage"]

            benefit_rows.append({
                "opti_key": key, # ref welche optimierung das war
                "Stromtarif": opti_sel[1],
                "Einspeisetarif": opti_sel[2],
                "Batterienutzung": battery_usage_label,
                "Ersparnis": opti_dict[key]["benefit"],
                "CO2 Ersparnis": opti_dict[key]["co2_benefit"],
                })

        df_results = pd.DataFrame(benefit_rows)
        # Originalnummer extrahieren (falls Key z.B. '3' oder '3_bezug')
        df_results["opti_number"] = df_results["opti_key"].apply(lambda x: int(str(x).split("_")[0]))

        # Für jede Originalnummer den Eintrag mit höchster Ersparnis behalten
        df_results = df_results.loc[df_results.groupby("opti_number")["Ersparnis"].idxmax()]

        df_results = df_results.sort_values(by="Ersparnis", ascending=False)
        st.session_state.result_tables[run_id]["results"] = df_results
        st.session_state.calculating = False
        st.toast("Fertig, die Ergebnisse sind da!")


    except Exception as e:
        st.error(f"Fehler beim Erstellen der Ergebnistabelle: {e}")

    st.session_state.calculating = False


# if st.button("Berechnung stoppen"):
#     st.session_state.calculating = False
#     st.rerun()


def format_setting_value(key, value):
    if isinstance(value, bool):
        return "Ja" if value else "Nein"
    return value


st.write("### Ergebnisse")


if len(st.session_state.result_tables) == 0:
    st.info("Noch keine Berechnungen durchgeführt.")
else:

    tab_labels = [f"Berechnung {i+1}" for i in range(len(st.session_state.result_tables))]
    reversed_indices = list(reversed(range(len(tab_labels))))

    # Tabs erzeugen
    tabs = st.tabs([tab_labels[i] for i in reversed_indices])
    with st.container(border=True):
        for i, tab in zip(reversed_indices, tabs):
            with tab:
                
                entry = st.session_state.result_tables[i]
                if entry["settings"].get("direct", False):
                    display_df = entry["results"].drop(columns=["opti_key", "opti_number"],
                                                   errors="ignore")
                else:
                    display_df = entry["results"].drop(columns=["opti_key", "Einspeisetarif", "opti_number" ,"Batterienutzung"],#
                                                   errors="ignore")

                if entry["results"] is None:
                    st.info("Noch keine Ergebnisse zur Darstellung vorhanden...")
                else:
                    st.subheader("Einsparungen durch den Tarifwechsel")
                    if entry["settings"].get("direct", False):
                        st.dataframe(
                            display_df,
                            row_height=70,
                            column_config={
                                "Ersparnis": st.column_config.NumberColumn("Ersparnis", format="%.2f €"),
                                "CO2 Ersparnis": st.column_config.NumberColumn("CO₂ Ersparnis", format="%.2f kg"),
                                "Stromtarif": st.column_config.TextColumn(width="medium"),
                                "Batterienutzung": st.column_config.TextColumn(width="small")
                            },
                            hide_index=True,
                        )
                    else:
                        st.dataframe(
                            display_df,
                            row_height=70,
                            column_config={
                                "Ersparnis": st.column_config.NumberColumn("Ersparnis", format="%.2f €"),
                                "CO2 Ersparnis": st.column_config.NumberColumn("CO₂ Ersparnis", format="%.2f kg"),
                                "Stromtarif": st.column_config.TextColumn(width="medium"),
                                # "Batterienutzung": st.column_config.TextColumn(width="small")
                            },
                            hide_index=True,
                        )
                    st.markdown(
                        ":deciduous_tree: Zum Vergleich, eine Buche nimmt durchschnittlich **35 kg CO₂/Jahr** auf."
                    )

                st.divider()

                SETTINGS_LABELS = {
                    "consumption": "Jährlicher Stromverbrauch [kWh]",
                    "controllable_device": "Steuerbare Verbrauchseinrichtungen (§14a EnWG)",
                    "has_pv": "Photovoltaik-Anlage vorhanden",
                    "pv_power": "Installierte PV-Leistung [kWp]",
                    "pv_direction": "Ausrichtung der PV-Anlage",
                    "installation_date": "Installationsdatum der PV-Anlage",
                    "has_battery": "Batteriespeicher vorhanden",
                    "battery_capacity": "Batteriekapazität [kWh]",
                    "netzbetreiber": "Netzbetreiber",
                    "direct": "Direktvermarktung"
                    }
                SETTINGS_DEPENDENCIES = {
                    "pv_power": "has_pv",
                    "pv_direction": "has_pv",
                    "installation_date": "has_pv",
                    "battery_capacity": "has_battery",
                    }
                settings_rows = []

                for key, value in entry["settings"].items():
                    if key not in SETTINGS_LABELS:
                        continue  # nur anzeigen, was gemappt ist


                    if key in SETTINGS_DEPENDENCIES:
                        dependency_key = SETTINGS_DEPENDENCIES[key]
                        if not entry["settings"].get(dependency_key, False):
                            continue  # Voraussetzung nicht erfüllt → nicht anzeigen

                    settings_rows.append({
                        "Einstellung": SETTINGS_LABELS[key],
                        "Wert": format_setting_value(key, value),
                    })

                settings_df = pd.DataFrame(settings_rows)

                st.subheader("Ausgewählte Einstellungen")
                st.dataframe(
                    settings_df,
                    hide_index=True,
                    use_container_width=True,
                )

                


st.divider()
st.write("### Informationen zu den Tarif-Optionen")
with st.expander("Dynamische Stromtarife"):
    st.markdown("""Wie jeder feste Stromtarif besteht auch ein dynamischer Stromtarif 
                immer aus einem monatlichen Fixpreis und einem variablen Anteil je kWh 
                elektrischer Energie. Nur der variable Anteil verändert sich dynamisch mit den 
                Schwankungen des Börsenstrompreises. """)
    st.markdown("""Der Börsenstrompreis bezieht sich in diesem Fall auf einen stündlich 
                gehandelten Preis. Für den Energieversorger, in diesem Fall Tibber, 
                wird eine monatliche Gebühr von 5,99 € und einem variablen Anteil von 
                2,16 Cent/kWh angenommen (Preisblatt Jan. 2025).
                """)
with st.expander("Zeitvariable Netzentgelte"):
    st.markdown("""Zu dem fixen Anteil des Strompreises gehören die Netzentgelte, 
                Konzessionsabgaben, Stromsteuer, Offshore-Umlage, KWKG-Umlage, NEV-Umlage 
                und ein energieversorger-spezifischer Aufschlag. Zur Entschädigung der 
                Steuerungsmöglichkeit von bestimmten Verbrauchseinrichtungen 
                erhält der Haushalt Netzentgeltreduzierungen. Neben pauschalen Reduzierungen 
                gibt es zusätzlich die Option zu zeitvariablen Netzentgelten. Dieses Modul ist 
                wählbar seit April 2025. Die Netzbetreiber können selbst ein dreistufigen 
                Netzentgeltplan bestimmen. Dabei müssen sich in 24 h mindestens einmal 
                ein Hochtarif, Standardtarif und Niedrigtarif wiederholen. """)

    st.markdown("""Am Beispiel des Netzbetreibers Westnetz liegt der Standardtarif 
                bei 11,88 Cent/kWh. Mit zeitvariablen Netzentgelten ist ein Niedrigtarif 
                von 0 - 6 Uhr von 1,19 Cent/kWh und ein Hochtarif zwischen 15 - 20 Uhr 
                von 17,75 Cent/kWh für 2025 festgelegt worden. Zu jeder anderen Zeit wird 
                der Standardtarif berechnet. Beispielsweise eine Kombination aus Batteriespeicher 
                und PV-Anlage kann den Netzbezug des Haushalts zeitlich passend verschieben.
                """)
with st.expander("Direktvermarktung"):
    st.markdown("""Die Direktvermarktung bietet neben der üblichen festen Einspeisevergütung 
                die Option, zu Börsenstrompreisen einzuspeisen. Eine Förderung wird dabei mit der 
                so genannten Marktprämie umgesetzt, die auf den Börsenstrompreis hinzugerechnet wird
                 und sicherstellt, dass förderfähige Anlagen Erlöse im Bereich der festen 
                Einspeisevergütung erhalten. Hinzu kommen Dienstleistungskosten, die in der 
                Berechnung beispielhaft von dem Energieversorgers Luxor Energy  
                mit 3% variablen Kosten und einem fixen Anteil (in Abhängigkeit von der Größe 
                der PV-Anlage) zwischen 74 € und 130 € pro Jahr eingerechnet werden. (Stand Mai 2025)""")
with st.expander("Batterieverhalten zum Netz"):
    st.markdown("""Speicher in Kombination mit förderfähigen Erneuerbaren Energie-Anlagen 
                dürfen aktuell wählen ob die Batterien ausschließlich aus dem Netz beziehen, 
                oder ausschließlich ins Netz mit EEG-Vergütung einspeisen dürfen. Die jeweils 
                profitablere Option wird in der Ergebnistabelle aufgelistet, wobei bei fester Einspeisevergütung
                aktuell immer die Option der Speicherung des Netzbezugs 
                profitabler ist. """)

    st.markdown("""In der Direktvermarktung ohne die Marktprämie können die Batterien sowohl 
                aus dem Netz beziehen, wie auch einspeisen. In Zukunft soll dies auch mit 
                der Marktprämie möglich sein. 
                """)
with st.expander("CO2-Einsparung"):
    st.markdown("""Für die Berechnung wird die CO2-Emission der gesamten elektrischen Energieerzeugung in Deutschland 
                verwendet. Wenn ein Haushalt beispielsweise vorher einem Netzbezug zu Zeiten hoher CO2-Emissionen
                getätigt hat und durch den Wechsel des Tarifs und der Reaktion darauf, den Verbrauch in Zeiten 
                geringerer CO2-Emissionen verschoben hat, zählt dies als CO2-Ersparnis. Die Höhe der Ersparnis
                bestimmt die Differenz des CO2-Ausstoßes zu diesen Zeitpunkten von ganz Deutschland.""")
    
    st.markdown("""Dieses Ergebnis ist durch die Berechnung mit dem gesamten Strommix, aus konventionellen und 
                erneuerbaren Kraftwerken, ein Hinweis darauf wie die Korrelation zwischen Ihrer Verbrauchsverschiebung 
                und dem CO2-Ausstoß der Energieversorgung generell ist. 
                In unserem aktuellen Energieversorgungssystem werden Schwankungen des Verbrauchs in der Regel mit 
                steuerbaren konventionellen Kraftwerken ausgeglichen, da erneuerbare Energien vorranig einspeisen 
                dürfen. Wenn der Haushaltsverbrauch sich erhöht würde aktuell ein konventionelles Kraftwerk die 
                Leistung anheben oder absenken. """)

