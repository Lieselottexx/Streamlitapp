import streamlit as st
import datetime

if __name__ == "__main__":
        calc = st.Page("calc.py", title="Berechnung") #, icon="")
        expl = st.Page("explain.py", title="Hintergrund Erklärungen") #, icon="")
        info = st.Page("thesis.py", title="Weitere Erkenntnisse") #, icon="")


        pages = st.navigation([calc, expl])#, info])

        # Initialisierung von Session_states:
        # st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """, help="Hi")
        DEFAULTS = {
        "calculating": False,
        "consumption": 3000,
        "controllable_device": False,
        "dyn_cost": False,
        "has_pv": False,
        "pv_power": 5,
        "pv_compass": "Süd",
        "has_eeg": False,
        "installation_date": datetime.date(2018, 1, 1),
        "has_battery": False,
        "battery_capacity": 6,
        "battery_usage": "Energie einspeisen",
        "direct_market": False,
        "netzbetreiber": "Westnetz",
        "direct": False
        }

        for key, value in DEFAULTS.items():
                if key not in st.session_state:
                        st.session_state[key] = value


                # Ergebnis-Speicher initialisieren
                if "result_tables" not in st.session_state:
                        st.session_state.result_tables = []

                if "active_result_tab" not in st.session_state:
                        st.session_state.active_result_tab = 0



        pages.run()    
        # st.sidebar.info("""Bei einem Seitenwechsel gehen die Einstellungen und die laufenden Berechnungen verlohren.""")
