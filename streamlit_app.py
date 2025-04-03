import streamlit as st
import time


class Streamlit():

    def __init__(self):
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
        st.session_state.consumption = st.slider("Jährlicher Stromverbrauch (kWh)", 1000, 8000, 4000, step=500)
        
        # Steuerbare Verbrauchseinrichtung
        controllable_device = st.checkbox("Haben Sie eine steuerbare Verbrauchseinrichtung?")
        
        # PV-Anlage
        has_pv = st.checkbox("Besitzen Sie eine PV-Anlage?")
        if has_pv:
            pv_power = st.slider("Installierte PV-Leistung (kWp)", 1, 25, 5, step=1)
            direction_map = {0: "Norden", 90: "Osten", 180: "Süden", 270: "Westen"}
            pv_direction = st.slider("Ausrichtung der PV-Anlage", options=list(direction_map.keys()), format_func=lambda x: direction_map[x])
            pv_direction_label = direction_map.get(pv_direction, f"{pv_direction} Grad")
            
            # EEG-Vergütung
            has_eeg = st.checkbox("Erhält die Anlage eine EEG-Vergütung?")
            if has_eeg:
                installation_date = st.date_input("Installationsdatum der PV-Anlage")
        
        # Batterie
        has_battery = st.checkbox("Haben Sie einen Batteriespeicher?")
        if has_battery:
            battery_capacity = st.slider("Batteriekapazität (kWh)", 1, 20, 5, step=1)
            is_eeg_battery = st.checkbox("Ist der Speicher eine EEG-Anlage?")
            if is_eeg_battery:
                battery_usage = st.selectbox("Batterieverhalten", ["Energie einspeisen", "Energie aus dem Netz beziehen"])
        
        # Berechnung starten
        if "results" not in st.session_state:
            st.session_state.results = []
        
        if st.button("Berechnung starten", disabled=st.session_state.get("calculating", False)):
            st.session_state.calculating = True
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for progress in self.long_running_calculation():
                progress_bar.progress(progress)
                status_text.text(f"Berechnung läuft... {progress}% abgeschlossen")
            
            result = self.long_running_calculation()
            st.session_state.results.append(result)
            
            progress_bar.empty()
            status_text.text("Berechnung abgeschlossen!")
            st.session_state.calculating = False
        
        # Ergebnisse anzeigen
        st.write("### Ergebnisse")
        for i, res in enumerate(st.session_state.results, start=1):
            st.write(f"{i}. Ergebnis: {res} Euro Ersparnis")