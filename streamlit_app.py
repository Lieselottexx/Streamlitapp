import streamlit as st
import time
import pandas as pd
import datetime
import NewControl as c
import multiprocessing


class Streamlit():

    def __init__(self):
        self.control = c.Control()
        self.page_calculation()
        pass

    def __del__(self):
        pass


    def progress_update(self, progress_bar, status_text, progress):
        if progress <= 1:
            progress_bar.progress(progress)
            status_text.text(f"Berechnung läuft... {round(progress*100)}% abgeschlossen")
        return progress_bar, status_text

    
    def page_calculation(self):
        # Notiz an mich: eine Pages mit Navigation
        # sieht zwar schöner aus aber beim pages wechseln reset die Berechnungsseite
        # mit Sidebar Radio nicht!
        # grade mit Radio auch nicht... :(

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
            # st.write("Session initialized:", st.session_state)

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

                
                
                progress_bar_loading, status_text_loading = self.progress_update(progress_bar_loading, status_text_loading, 0.05)

                loadprofiles = {2000: 3,  3000: 5,  4000: 12,
                        5000: 13, 6000: 17, 7000: 15, 8000: 16}
                
                st.session_state.loadprofile = loadprofiles[st.session_state.consumption]
                print(f"Lastprofil: {st.session_state.loadprofile}")
                del(loadprofiles)

                progress_bar_loading, status_text_loading = self.progress_update(progress_bar_loading, status_text_loading,0.10)

                self.data, averageEnergyHousehold = self.control.data_generator.loadData(st.session_state.loadprofile,
                                                                                 st.session_state.pv_direction, 
                                                                                 st.session_state.pv_power,
                                                                                 st.session_state.battery_capacity) 
                
                progress_bar_loading, status_text_loading = self.progress_update(progress_bar_loading, status_text_loading, 0.70)
                
                self.data = self.control.price_generator.calculate_energy_prices(self.data, averageEnergyHousehold,
                                                                         st.session_state.controllable_device)


                progress_bar_loading, status_text_loading = self.progress_update(progress_bar_loading, status_text_loading, 1)

                progress_bar_Opti1, status_text_Opti1 = self.progress_update(progress_bar_Opti1, status_text_Opti1, 0)

                progress_bar_Opti2, status_text_Opti2 = self.progress_update(progress_bar_Opti2, status_text_Opti2, 0)

                '''Wenn das True ist, dann wird nur statisch mit Zeitvariablen Netzentgelten gerechnet'''
                if st.session_state.static_ZVNE == 1:
                    select_opti1 = self.control.select_optimisation_behaviour(9)
                else:
                    if st.session_state.has_eeg:
                        select_opti1 = self.control.select_optimisation_behaviour(3)
                        if st.session_state.controllable_device:
                            select_opti1 = self.control.select_optimisation_behaviour(10)
                    else:
                        select_opti1 = self.control.select_optimisation_behaviour(8)
                        if st.session_state.controllable_device:
                            select_opti1 = self.control.select_optimisation_behaviour(11)


                month_pv_installation = st.session_state.installation_date.month
                year_pv_installation  = st.session_state.installation_date.year
                self.static_feed_in_price, self.static_bonus_feed_in = self.control.get_eeg_prices(year_pv_installation,month_pv_installation)

                battery_power = st.session_state.battery_capacity * self.control.min_data/60 

                input_optimisation =    [self.control.optimise_time, self.control.step_time, st.session_state.battery_capacity,
                                            self.control.battery_costs,  battery_power, 
                                            self.control.grid_power, self.static_feed_in_price, self.static_bonus_feed_in]
                battery_usage = st.session_state.battery_usage

                select_opti2 = self.control.select_optimisation_behaviour(1)

                queue = multiprocessing.Queue()

                # Prozesse starten
                process_1 = multiprocessing.Process(target=self.control.opimisation.select_optimisation, args=(self.data, input_optimisation, select_opti1, battery_usage, queue, 1))
                process_2 = multiprocessing.Process(target=self.control.opimisation.select_optimisation, args=(self.data, input_optimisation, select_opti2, battery_usage, queue, 2))

                process_1.start()
                process_2.start()

                
                while process_1.is_alive() or process_2.is_alive():
                    while not queue.empty():
                        task_id, progress = queue.get()
                        if task_id == 1:
                            progress_bar_Opti1, status_text_Opti1 = self.progress_update(progress_bar_Opti1, status_text_Opti1, progress)
                        elif task_id == 2:
                            progress_bar_Opti2, status_text_Opti2 = self.progress_update(progress_bar_Opti2, status_text_Opti2, progress)
                        elif task_id == f"Result 1:":
                            result1 = progress 
                            print("Result 1 stored.")
                        elif task_id == f"Result 2:":
                            result2 = progress 
                            print("Result 2 stored.")
                
                # Wait for processes to finish
                process_1.join()
                process_2.join()

                costs_selected = self.control.analysis.single_cost_batterycycle_calculation(result1, select_opti1)
                costs_evo      = self.control.analysis.single_cost_batterycycle_calculation(result2, select_opti2)

                benefit = costs_evo['2024-12-31'] - costs_selected['2024-12-31']
                st.write(f"{benefit} = {costs_evo['2024-12-31']} - {costs_selected['2024-12-31']}")
                st.session_state.results.append(benefit)  

                st.success("Berechnung abgeschlossen!")
                st.session_state.calculating = False
                
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
                st.write(f"{i}. Ergebnis: {round(res,2)} Euro Ersparnis")

        # =====================================
        # SEITE 2: ERKLÄRUNG
        # =====================================
        elif page == "Erklärungen zum Rechner":
            st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")
            st.markdown("Auf dieser Seite werden alle Einstellmöglichkeiten sowie die Annhamen des Rechners erklärt. Des Weiteren sind auf dieser Seite der Optimierungsprozess und die Interpretation des Ergebnisses erklärt.")

            st.header("📌 Ziel der Berechnung")
            st.info("""
            Die Berechnung soll dazu dienen, für sich selbst eine Einschätzung zu bekommen, ob sich ein Wechsel auf einen dynamischen Stromtarif lohnen würde.
            Sie basiert auf dem Jahresdurchschnittsverbrauch des Haushalts, sowie Optional auf der Erzeugung einer vorhandenen PV-Anlage, die Nutzung einer Batteriekapazität in Kombination mit einem intelligenten Heim-Energiemanagement-System (HEMS) der den Energiefluss intelligent steuern kann.
            """)

            st.header("🔍 Annahmen & Grenzen der Betrachtung")
            with st.expander("Was ist berücksichtigt?"):
                st.markdown("""
                - Dynamischer Stromtarif von Tibber (stündliche Preisanpassungen)
                - Vergleich zu dem Haushalt mit **normalen** festem Stromtarif, optional mit Eigenverbrauchsoptimierung des HEMS
                - Typische Lastverläufe für verschiedene Jahresdurchschnittsverbräuche
                - Optimierung der Stromkosten des Haushalts
                - Eigene PV-Erzeugung, sowie der flexible Einsatz einer Batterie
                - Steuerbare Verbrauchseinrichtungen nach Energiewirtschaftsgesetz (EnWG) Paragraph 14a Modul 1 + 3 Zeitvariablen Netzentgelte (ZVNE) 
                - EEG-Vergütung für PV-Anlagen mit fester Einspeisevergütung
                - Optional: Entfall der EEG-Vergütung für Einspeisung, Einspeisung wird mit dem passenden Börsenstrompreis vergütet
                """)
                
            with st.expander("Was ist **nicht** berücksichtigt?"):
                st.markdown("""
                - Bewusste Verhaltensänderungen in Verbindung mit einem dynamischen Stromtarif
                - Flexible einsetzbare Verbraucher wie z. B. Elektroautos, Waschmaschinen etc. durch das HEMS
                - Direktvermarktung der Einspeisung innerhalb des EEG
                """)

            st.warning("""
            Die Berechnung geht davon aus, dass sich das individuelle Verbrauchsverhalten mit dem Wechsel des Stromtarifs **nicht ändert**.
            Es erfolgt nur eine **optimierte** Batterienutzung und der PV-Einspeisung.
            Eine bewusste Verhaltensänderung in Verbindung mit einem dynamischen Stromtarif kann zu einer weiteren Ersparnis führen.
            Dabei sollte bewusst sein, dass im gleichen Maße ein Verhalten ungünstig zum Börsenstrompreis auch zusätzliche Kosten verursachen.
            """)

            # st.header("⚡ Beispiel für flexible Nutzung")
            st.markdown("""Ein Beispiel für die individuelle Flexibilität, die in dieser Rechnung nicht berücksichtigt ist, aber ausschlaggebend sein kann für eine zusätzliche Kosten oder Ersparnisse, ist die Nutzung eines Elektroautos.
            Ein Elektroauto könnte z. B. durch das HEMS automatisch bei günstigen Preisen, zum Beispiel nachts, geladen werden.
            Ein Fall der hingegen höhere Kosten verursachen kann ist die schnelle Beladung der Fahrzeugbatterie nach Feierabend in den Abendstunden, wo es aktuell häufig zu hohen Börsenstrompreisen kommt. 
            """)
            st.warning("""
                       Diese Flexibilität der individuellen Nutzung ist nur schwer zu simulieren. ^
                       Jeder der einen dynamischen Stromtarif in Betracht zieht sollte sich gegebenenfalls über die eigene Ambition der Verhaltensanpassung gegenüber zeitlich ändernden Stromtarifen hinterfragen, damit können zusätzliche Einsparungen erzielt werden. 
            """)

            # st.success("""
            # 👉 Wer einen dynamischen Stromtarif in Betracht zieht, sollte sich fragen, wie flexibel das eigene Verhalten gegenüber zeitlich schwankenden Preisen sein kann.
            # """)

            st.header("🌱 Vorteile für das Energiesystem")
            st.markdown("""
            - Börsenstrompreise sind Abhängig von der Erzeugung und dem Verbrauch
            - **Niedrige Strompreise bedeuten Überschuss an erneuerbarer Energie.**
            - Jeder Verbrauch der in Zeiten niedriger Strompreise verschoben wird spart CO₂-Emissionen und fördert die Integrität Erneuerbarer Energien.
            - Weniger Verbrauch in Zeiten hoher Strompreise kann lokal das Netz entlasten.  
                                     → 
            """)

            st.header("📉 Voraussetzungen für dynamische Tarife")
            st.markdown("""
            Ein intelligentes Messsystem („Smart Meter“) ist Voraussetzung bei fast allen Anbietern.
            """)

            st.header("📊 Erklärungen zu den Modellannahmen")

            with st.expander("Lastgänge"):
                st.markdown("""
                Der Lastgang ist der **Rohverbrauch des Haushalts** ohne PV und Batterie.
                Die Lastgänge sind generiert mit dem *Load Profile Generator*, www.https://www.loadprofilegenerator.de/ developed by Noah Pflugradt.
                Die verwendeten representativen Profile für jeden Jahresdurchschnittsverbrauch basierend auf 1000 Profilen, die eine durchschnittliche Haushaltsverteilung in Deutschland abdecken.
                Der angegebene Verbrauch spiegelt den typischen Verbrauch von Haushalten zwischen der letzten Stufe und der angegebenen Stufe wieder. 
                """)

            with st.expander("Standardlastprofil (SLP)"):
                st.markdown("""
                Das Standardlastprofil (SLP) wird vom Energieversorgungsunternehmen, für jeden Haushalt ohne Lastgangmessung, verwendet und bestimmt die Menge der Beschaffung der Energie zu jedem Zeitpunkt im Jahr.
                Damit beeinflusst das SLP den Preis des festen Stromtarifs. 
                Das bisher verwendete Standardlastprofil basiert auf dem Verbrauchsverhalten vor dem Jahr 2000. 
                Im März 2025 sind neue Standardlastprofile des BDEWs Veröffentlicht worden. Diese basieren nicht nur auf die veränderten Verhaltensweisen sondern sind auch seperate SLP für Haushalte mit PV-Anlagen und mit PV-Batterie-Kombinationen erstellt worden. 
                Welchen Einfluss die unterschiedlichen SLPs auf das Ergebnis der Berechnung hat wird auf der Seite der Erweiterten Ergebnisse dargestellt. 
                """)

            with st.expander("PV-Erzeugung"):
                st.markdown("""
                - Basierend auf Wetter- und Geodaten aus NRW (Raum Soest)
                - Berechnet mit der **PV-Lib**-Bibliothek, https://pvlib-python.readthedocs.io/en/stable/#
                - Konservativer Jahresdruchschnittsertrag in Südausrichtung von 700–800 kWh/kWp
                
                """)

            with st.expander("Einspeisevergütung nach EEG"):
                st.markdown("""
                Die Einspeisevergütung ist seit der ersten EEG-Novelle 2000 festgelegt. Seit 2009 können PV-Anlagen in Teileinspeisung betrieben werden und die selbsterzeugte elektrische Energie kann direkt vom Haushalt verbraucht werden.
                Die feste Einspeisevergütung ist für den Installationszeitraum von Janunar 2012 bis Juli 2025 in der Berechnung hinterlegt.
                Hinterlegt sind Einspeisevergütungen für PV-Anlagen die als Teileinspeisungsanlage gemeldet sind und bei Unterscheidung die unter 10kWp liegen.
                """)

            with st.expander("Börsenstrompreise"):
                st.markdown("""
                - Bezogen von **Energycharts**, https://energy-charts.info/, 23.01.2025
                - Dayahead-Strompreise (Strombörse EEX) DE-LU oder Intraday-Strompreise (Strombörse EEX) DE-LU im Stündlichen Intervall
                - mehr infos noch hinzufügen
                """)

            with st.expander("statischer und dynamischer Tarif"):
                st.markdown("""
                Dynamischer Stromtarif:
                - Preisänderung alle 60 Minuten
                - Tibber-Tarif üblicher Preisaufschlag
                - beinhaltet Steuern, Abgaben und Netzentgelte (alles bezogen auf das Jahr 2025, Netzentgelte bezogen auf eine Anschluss im Gebiet von Westnetz)
                            
                Fester Stromtarif: 
                - zur Berechnung des aktuell Üblichen Stromtarifmodells
                - jährlicher fester Strompreis, berechnet aus dem dynamischen Stromtarif und dem Standardlastprofil des Haushalts
    
                """)

            with st.expander("Zeitvariablen Netzentgelte"):
                st.markdown("""
                Mit der Novelle des Gesetzes zur Beschleunigung der Digitalisierung der Energiewende ist in dem Energiewirtschaftsgesetz (ENWG) der Paragraph 14a zur Regelung von steuerbaren Verbrauchseinrichtungen hinzugekommen.
                Damit müssen steuerbare Verbrauchseinrichtungen (Wärmepumpen, Batteriespeicher, Wallboxen, Klimageräte) ab einer netzwirksamen Leistung von 4,2 kW die ab dem 01. Januar 2024 installiert worden sind, bei Netzengpässen steuerbar sein. 
                Als Entschädigung sieht der Netzbetreiber eine Ermäßigung der Netzentgelte vor. 
                Seit dem 01. April 2025 kann das Modul 3 für steuerbare Verbrauchseinrichtungen genutzt werden, mit dem zeitvariable Netzentgelte möglich sind.
                Jeder Netzbetreiber kann im Zeitraum von 24h ein 3 stufiges Netzentgeld erheben. In diesem Fall sind die Bedingungen des Netzbetreibers Westnetz genutzt worden. 
                """)

            st.header("⚙️ Optimierungen")
            st.markdown("""
            Während der Berechnung wird angezeigt, welche Optimierung gerade läuft und welche Wirkung sie hat.
            Relevante Optimierungsschritte: **1, 3, 8, 9, 10, 11**
            """)

            st.header("📈 Ergebnisse")
            st.markdown("""
            Die Ergebnisse zeigen, wie viel bei einem Wechsel auf einen dynamischen Tarif gespart werden kann.
            Dabei gilt:
            - **Ohne Verhaltensänderung**: Nur durch intelligente Steuerung.
            - **Mit Verhaltensänderung**: Noch größere Einsparpotenziale – aber auch Risiken.
            """)


        # =====================================
        # SEITE 3: ERWEITERTE ERGEBNISSE
        # =====================================
        elif page == "Erweiterte Ergebnisse":
            st.title("Erweiterte Ergebnisse")


        
