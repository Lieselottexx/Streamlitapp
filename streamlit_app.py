import streamlit as st
import time
import pandas as pd
import NewControl as c


class Streamlit():

    def __init__(self):
        self.control = c.Control()
        self.create_app_interface()
        pass

    def __del__(self):
        pass

   


    def long_running_calculation(self):
        for i in range(101):
            time.sleep(0.05)  # Simulierte lange Berechnung
            yield i
        return round(1000 * (st.session_state.consumption / 8000))  # Beispielhafte Ersparnis-Berechnung
    
    
    def create_app_interface(self):

        st.title("Vergleich: Dynamische vs. Statische Energiepreise")
        
        # Stromverbrauch
        st.slider("Jährlicher Stromverbrauch (kWh)", 1000, 8000, key="consumption", step=500, disabled=st.session_state.get("calculating", False))
        
        # Steuerbare Verbrauchseinrichtung
        st.checkbox("Haben Sie eine steuerbare Verbrauchseinrichtung?", key="controllable_device", disabled=st.session_state.get("calculating", False))
        if st.session_state.controllable_device: 
            st.checkbox("Standard Stromtarif mit Zeitvariablen Netzentgelten im Vergleich", key="static_ZVNE", disabled=st.session_state.get("calculating", False))

        
        # PV-Anlage
        st.checkbox("Besitzen Sie eine PV-Anlage?", key="has_pv", disabled=st.session_state.get("calculating", False))
        if st.session_state.has_pv:
            st.slider("Installierte PV-Leistung (kWp)", 1, 25, 5, step=1, key="pv_power", disabled=st.session_state.get("calculating", False))
            direction_map = { "Nord": 0, 'Nord-Ost': 45, "Ost": 90, 'Süd-Ost': 135, "Süd": 180, "Süd-West": 225,  "West": 270}
            st.selectbox("Ausrichtung der PV-Anlage", list(direction_map.keys()), key="pv_compass", disabled=st.session_state.get("calculating", False))
            st.session_state.pv_direction = direction_map[st.session_state.pv_compass]

            # pv_direction_label = direction_map.get(pv_direction, f"{pv_direction} Grad")
            
            # EEG-Vergütung
            st.checkbox("Erhält die Anlage eine EEG-Vergütung?", key="has_eeg", disabled=st.session_state.get("calculating", False))
            if st.session_state.has_eeg:
                st.session_state.installation_date = pd.to_datetime(st.date_input("Installationsdatum der PV-Anlage"))
            else:
                st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")
        else:
            st.session_state.pv_power = 0
            st.session_state.pv_direction = 0
            st.session_state.has_eeg = 0
            st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")
        # Batterie
        st.checkbox("Haben Sie einen Batteriespeicher?", key="has_battery", disabled=st.session_state.get("calculating", False))
        if st.session_state.has_battery:
            st.slider("Batteriekapazität (kWh)", 1, 20, 5, step=1, key="battery_capacity", disabled=st.session_state.get("calculating", False))
            if st.session_state.has_eeg:
                st.selectbox("Batterieverhalten", ["Energie einspeisen", "Energie aus dem Netz beziehen"], 
                                                              key="battery_usage", disabled=st.session_state.get("calculating", False))
        else:
            st.session_state.battery_capacity = 0
            st.session_state.is_eeg_battery = 0


        # Berechnung starten
        if "results" not in st.session_state:
            st.session_state.results = []
        
        if st.button("Berechnung starten", disabled=st.session_state.get("calculating", False)):
            st.session_state.calculating = True
            
            st.session_state.progress_bar_loading = st.progress(0)
            st.session_state.status_text_loading = st.empty()

            st.session_state.progress_bar_Opti1 = st.progress(0)
            st.session_state.status_text_Opti1 = st.empty()

            st.session_state.progress_bar_Opti2 = st.progress(0)
            st.session_state.status_text_Opti2 = st.empty()
            
            for ben, st.session_state.progress_loading, st.session_state.progress_opti1, st.session_state.progress_opti2 in self.control.calculation():
                st.session_state.progress_bar_loading.progress(st.session_state.progress_loading)
                st.session_state.status_text_loading.text(f"Berechnung läuft... {st.session_state.progress_loading}% abgeschlossen")

                st.session_state.progress_bar_Opti1.progress(st.session_state.progress_opti1)
                st.session_state.status_text_Opti1.text(f"Berechnung läuft... {st.session_state.progress_opti1}% abgeschlossen")

                st.session_state.progress_bar_Opti2.progress(st.session_state.progress_opti2)
                st.session_state.status_text_Opti2.text(f"Berechnung läuft... {st.session_state.progress_opti2}% abgeschlossen")
            
            result = self.control.calculation()
            st.session_state.results.append(result)
            
            st.session_state.progress_bar_loading.empty()
            st.session_state.status_text_loading.text("Berechnung abgeschlossen!")

            st.session_state.progress_bar_Opti1.empty()
            st.session_state.status_text_Opti1.text("Berechnung abgeschlossen!")

            st.session_state.progress_bar_Opti2.empty()
            st.session_state.status_text_Opti2.text("Berechnung abgeschlossen!")

            st.session_state.calculating = False
        
        # Ergebnisse anzeigen
        st.write("### Ergebnisse")
        for i, res in enumerate(st.session_state.results, start=1):
            st.write(f"{i}. Ergebnis: {round(res,2)} Euro Ersparnis")