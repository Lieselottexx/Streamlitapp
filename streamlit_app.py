import streamlit as st
import time
import pandas as pd
import datetime
import NewControl as c


class Streamlit():

    def __init__(self):
        self.control = c.Control()
        self.page_calculation()
        pass

    def __del__(self):
        pass

    
    def page_calculation(self):
        # Notiz an mich: eine Pages mit Navigation
        # sieht zwar schöner aus aber beim pages wechseln reset die Berechnungsseite
        # mit Sidebar Radio nicht!

        # Sidebar Navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Seite auswählen", ["Berechnung", "Erklärung", "Erweiterte Ergebnisse"])

        # =====================================
        # SEITE 1: BERECHNUNG
        # =====================================
        if page == "Berechnung":
            if "calculating" not in st.session_state:
                st.session_state.calculating = False
                st.session_state.consumption = 3000
                st.session_state.controllable_device = False
                st.session_state.static_ZVNE = False
                st.session_state.has_pv = False
                st.session_state.pv_power = 5
                st.session_state.pv_compass = "Süd"
                st.session_state.has_eeg = False
                st.session_state.installation_date = pd.to_datetime("2018-01-01")
                st.session_state.has_battery = False
                st.session_state.battery_capacity = 3
                st.session_state.battery_usage = "Energie einspeisen"

            st.title("Vergleich: Dynamische vs. Statische Energiepreise")
            
            # Stromverbrauch
            st.slider("Jährlicher Stromverbrauch (kWh)", 2000, 8000, key="consumption", step=1000) #, disabled=st.session_state.get("calculating"))
            
            # Steuerbare Verbrauchseinrichtung
            st.checkbox("Haben Sie eine steuerbare Verbrauchseinrichtung?", key="controllable_device") #, disabled=disable_settings)

            if st.session_state.get("controllable_device", False): 
                st.checkbox("Standard Stromtarif mit Zeitvariablen Netzentgelten im Vergleich", key="static_ZVNE") #, disabled=st.session_state.get("calculating", False))

            
            # PV-Anlage
            st.checkbox("Besitzen Sie eine PV-Anlage?", key="has_pv") #, disabled=st.session_state.get("calculating", False))
            if st.session_state.get("has_pv", False):
                st.slider("Installierte PV-Leistung (kWp)", 1, 25, 5, step=1, key="pv_power") #, disabled=st.session_state.get("calculating", False))
                direction_map = { "Nord": 0, 'Nord-Ost': 45, "Ost": 90, 'Süd-Ost': 135, "Süd": 180, "Süd-West": 225,  "West": 270}
                if "pv_compass" not in st.session_state:
                    st.session_state.pv_compass = "Süd"
                st.selectbox("Ausrichtung der PV-Anlage", list(direction_map.keys()), key="pv_compass") #, disabled=st.session_state.get("calculating", False))
                st.session_state.pv_direction = direction_map[st.session_state.pv_compass]

                # pv_direction_label = direction_map.get(pv_direction, f"{pv_direction} Grad")
                
                # EEG-Vergütung
                st.checkbox("Erhält die Anlage eine EEG-Vergütung?", key="has_eeg") #, disabled=st.session_state.get("calculating", False))
                if st.session_state.get("has_eeg", False):
                    st.session_state.installation_date = pd.to_datetime(st.date_input("Installationsdatum der PV-Anlage", 
                                                                                      value=datetime.date(2024, 1, 1), 
                                                                                      min_value=datetime.date(2012, 1, 1), 
                                                                                      max_value=datetime.date.today())) #, disabled=st.session_state.get("calculating", False)))
                else:
                    st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")
            else:
                st.session_state.pv_power = 0
                st.session_state.pv_direction = 0
                st.session_state.has_eeg = 0
                st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")
            # Batterie
            st.checkbox("Haben Sie einen Batteriespeicher?", key="has_battery") #, disabled=st.session_state.get("calculating", False))

            if st.session_state.get("has_battery", False):
                st.slider("Batteriekapazität (kWh)", 1, 20, 5, step=1, key="battery_capacity") #, disabled=st.session_state.get("calculating", False))
                if st.session_state.get("has_eeg", False):
                    st.selectbox("Batterieverhalten", ["Energie einspeisen", "Energie aus dem Netz beziehen"], 
                                                                key="battery_usage") #, disabled=st.session_state.get("calculating", False))
            else:
                st.session_state.battery_capacity = 0
                st.session_state.is_eeg_battery = 0


            # Berechnung starten
            if "results" not in st.session_state:
                st.session_state.results = []


            if st.button("Alle Berechnungen stoppen"):
                st.session_state.calculating = False
                st.rerun()

            if st.button("Berechnung starten", disabled=st.session_state.get("calculating", False)):
                st.session_state.calculating = True
                
                progress_bar_loading = st.progress(0)
                status_text_loading = st.empty()

                progress_bar_Opti1 = st.progress(0)
                status_text_Opti1 = st.empty()

                progress_bar_Opti2 = st.progress(0)
                status_text_Opti2 = st.empty()
                
                result = self.control.calculation(st.session_state, progress_bar_loading, status_text_loading, progress_bar_Opti1, status_text_Opti1, 
                                                progress_bar_Opti2, status_text_Opti2)
                
                st.session_state.results.append(result)
                
                progress_bar_loading.empty()
                status_text_loading.text("Berechnung abgeschlossen!")

                progress_bar_Opti1.empty()
                status_text_Opti1.text("Berechnung abgeschlossen!")

                progress_bar_Opti2.empty()
                status_text_Opti2.text("Berechnung abgeschlossen!")

                st.session_state.calculating = False
            
            # Ergebnisse anzeigen
            st.write("### Ergebnisse")
            for i, res in enumerate(st.session_state.results, start=1):
                st.write(f"{i}. Ergebnis: {round(res[0],2)} Euro Ersparnis")

        # =====================================
        # SEITE 2: ERKLÄRUNG
        # =====================================
        elif page == "Erklärung":
            st.title("Erklärung zur Berechnung")
            st.markdown("""
            # Lastgänge provisorich bis die Liste größer ist:\n
            2000 kWh : 1957 kWh Single Woman with work 30-64  (3)\n
            3000 kWh : 3050 kWh Single woman over 65 with parttime job (5)\n
            4000 kWh : 3496 kWh (12)\n
            5000 kWh : 4512 kWh (13)\n
            6000 kWh : 5847 kWh (17)\n
            7000 kWh : 6300 kWh (15)\n
            8000 kWh : 8349 kWh (16)\n\n
                        
            # Einspeisevergütung aktuell nur von PV Anlagen < 10kWp\n
            
            """)


        # =====================================
        # SEITE 3: ERWEITERTE ERGEBNISSE
        # =====================================
        elif page == "Erweiterte Ergebnisse":
            st.title("Erweiterte Ergebnisse")


        
