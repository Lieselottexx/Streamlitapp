import streamlit as st


st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")
st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """)
st.markdown(""":blue[Fragen und Anregungen gerne an l.weghake@gmail.com]""")
st.markdown("Auf dieser Seite werden alle Einstellmöglichkeiten sowie die Annahmen des Rechners erklärt. Des Weiteren sind auf dieser Seite der Optimierungsprozess und die Interpretation des Ergebnisses erklärt.")

# st.header("📌 Ziel der Berechnung")
# st.info("""
# Die Berechnung soll dazu dienen, für sich selbst eine Einschätzung zu bekommen, ob sich ein Wechsel auf einen dynamischen Stromtarif lohnen würde.
# Sie basiert auf dem Jahresdurchschnittsverbrauch des Haushalts, sowie Optional auf der Erzeugung einer vorhandenen PV-Anlage, die Nutzung einer Batteriekapazität in Kombination mit einem intelligenten Heim-Energiemanagement-System (HEMS) das den Energiefluss intelligent steuern kann.
# """)

# st.header("🔍 Annahmen & Grenzen der Betrachtung")
# with st.expander("Was ist berücksichtigt?"):
#     st.markdown("""
#     - Dynamischer Stromtarif von Tibber (stündliche Preisanpassungen)
#     - Vergleich zu dem Haushalt mit festem Stromtarif, optional mit Eigenverbrauchsoptimierung des HEMS
#     - Typische Lastverläufe für verschiedene Jahresdurchschnittsverbräuche
#     - Optimierung der Stromkosten des Haushalts
#     - Eigene PV-Erzeugung, sowie der flexible Einsatz einer Batterie
#     - Steuerbare Verbrauchseinrichtungen nach Energiewirtschaftsgesetz (EnWG) Paragraph 14a Modul 1 + 3 Zeitvariablen Netzentgelte (ZVNE) 
#     - EEG-Vergütung für PV-Anlagen mit fester Einspeisevergütung
#     - Optional: Entfall der EEG-Vergütung für Einspeisung, Einspeisung wird mit dem passenden Börsenstrompreis vergütet
#     """)

# with st.expander("Was ist **nicht** berücksichtigt?"):
#     st.markdown("""
#     - Bewusste Verhaltensänderungen in Verbindung mit einem dynamischen Stromtarif
#     - Flexible einsetzbare Verbraucher wie z. B. Elektroautos, Waschmaschinen etc. durch das HEMS
#     - Direktvermarktung der Einspeisung innerhalb des EEG
#     """)

# st.warning("""
# Die Berechnung geht davon aus, dass sich das individuelle Verbrauchsverhalten mit dem Wechsel des Stromtarifs **nicht ändert**.
# Es erfolgt nur eine **optimierte** Batterienutzung und der PV-Einspeisung.
# Eine bewusste Verhaltensänderung in Verbindung mit einem dynamischen Stromtarif kann zu einer weiteren Ersparnis führen.
# Dabei sollte bewusst sein, dass im gleichen Maße ein Verhalten ungünstig zum Börsenstrompreis auch zusätzliche Kosten verursachen.
# """)

# st.header("⚡ Beispiel für flexible Nutzung")
# st.markdown("""Ein Beispiel für die individuelle Flexibilität, die in dieser Rechnung nicht berücksichtigt ist, aber ausschlaggebend sein kann für eine zusätzliche Kosten oder Ersparnisse, ist die Nutzung eines Elektroautos.
# Ein Elektroauto könnte z. B. durch das HEMS automatisch bei günstigen Preisen, zum Beispiel nachts, geladen werden.
# Ein Fall der hingegen höhere Kosten verursachen kann ist die schnelle Beladung der Fahrzeugbatterie nach Feierabend in den Abendstunden, wo es aktuell häufig zu hohen Börsenstrompreisen kommt. 
# """)
# st.warning("""
#             Diese Flexibilität der individuellen Nutzung ist nur schwer zu simulieren.
#             Jeder der einen dynamischen Stromtarif in Betracht zieht sollte sich gegebenenfalls über die eigene Ambition der Verhaltensanpassung gegenüber zeitlich ändernden Stromtarifen hinterfragen, damit können zusätzliche Einsparungen erzielt werden. 
# """)

# st.success("""
# 👉 Wer einen dynamischen Stromtarif in Betracht zieht, sollte sich fragen, wie flexibel das eigene Verhalten gegenüber zeitlich schwankenden Preisen sein kann.
# """)

# st.header("🌱 Vorteile für das Energiesystem")
# st.markdown("""
# - Börsenstrompreise sind Abhängig von der Erzeugung und dem Verbrauch
# - **Niedrige Strompreise bedeuten Überschuss an erneuerbarer Energie.**
# - Jeder Verbrauch der in Zeiten niedriger Strompreise verschoben wird spart CO₂-Emissionen und fördert die Integrität Erneuerbarer Energien.
# - Weniger Verbrauch in Zeiten hoher Strompreise kann lokal das Netz entlasten.  
#                             → 
# """)

# st.header("📉 Voraussetzungen für dynamische Tarife")
# st.markdown("""
# Ein intelligentes Messsystem („Smart Meter“) ist Voraussetzung bei fast allen Anbietern.
# """)

st.header("📊 Erklärungen zu der Datengrundlage der Berechnung")
st.markdown("""Der Großteil der Annahmen und Daten die in der Berechnung verwendet werden sind bereits auf der Seite Berechnung im Vortext beschrieben. Auf dieser Seite befinden sich genaure Informationen zu einzelnen Datensätzen der Berechnung.""")

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
                Die Erzeugung der PV-Anlagen wird basierend auf Wetter- und Geodaten aus NRW (Raum Soest) und den angegebenen Daten aus Leistung und Ausrichtung berechnet. Die Wetterdaten stammen direkt vom Deutschen Wetterdienst aus einer Station in Werl. Diese Daten werden mit einer Python-Bibliothek, der **PV-Lib**-Bibliothek, https://pvlib-python.readthedocs.io, zu einem Erzeugungsprofil der entsprechenden Anlage weiterverarbeitet. 
    Noch raussuchen:
    - Konservativer Jahresdruchschnittsertrag in Südausrichtung von 700–800 kWh/kWp
    
    """)

with st.expander("Einspeisevergütung nach EEG"):
    st.markdown("""
    Die Einspeisevergütung ist seit der ersten EEG-Novelle 2000 festgelegt. Seit 2009 können PV-Anlagen in Teileinspeisung betrieben werden und die selbsterzeugte elektrische Energie kann direkt vom Haushalt verbraucht werden.
    Die feste Einspeisevergütung ist für den Installationszeitraum von Janunar 2012 bis Juli 2025 in der Berechnung hinterlegt.
    Hinterlegt sind Einspeisevergütungen für PV-Anlagen die als Teileinspeisungsanlage gemeldet sind und bei Unterscheidung die unter 10kWp liegen. Muss noch angepast werden im Code, dann kann dieser Absatz auch ganz raus!!!!
    """)


with st.expander("statischer und dynamischer Tarif"):
    st.markdown("""
                Die Erklärung wie sich der dynamische Tarif in der Berechnung zusammensetzt ist bereits auf der Seite Berechnung erklärt worden. Zusammenfassend besteht dieser aus dem zeitlich variablen Börsenstrompreis mit Steuern, Abgaben und einem Zuschlag des Energieversorgers. 

                Ein fester Stromtarif besteht im Wesentlichen aus den gleichen Komponenten, nur dass in dem Fall der Energieversorger die Energie nach dem Standardlastprofil möglichst kostengünstig beschafft. Im Mittel spiegeln die festen Tarife die Korrelation aus dem SLP und dem Börsenstrompreis wider, eventuell mit etwas Zeitverzögerung da die Energieversorger diese Anpassungen nur träge vornehmen. Für die Berechnung ist der dynamische Stromtarif mit dem SLP zeitlich übernander gelegt worden und ein Jahresmittel für den festen Strompreis gebildet worden.

                Da die Fixkosten der Stromtarife auf die Menge der bezogenen Energie umgerechnet werden müssten und bei den unterschiedlichen Optimierung unterschiedlich viel Energie bezogen wird, könnten diese eine Ungenauigkeit ins Ergebnis bringen. Aufgrund dessen wird nur die Differenz der Kosten, bzw. die Einsparungen betrachtet und die Fixkosten aus der Berechnung außen vor gelassen. 
                """)

# with st.expander("Zeitvariablen Netzentgelte"):
#     st.markdown("""
#     Mit der Novelle des Gesetzes zur Beschleunigung der Digitalisierung der Energiewende ist in dem Energiewirtschaftsgesetz (ENWG) der Paragraph 14a zur Regelung von steuerbaren Verbrauchseinrichtungen hinzugekommen.
#     Damit müssen steuerbare Verbrauchseinrichtungen (Wärmepumpen, Batteriespeicher, Wallboxen, Klimageräte) ab einer netzwirksamen Leistung von 4,2 kW die ab dem 01. Januar 2024 installiert worden sind, bei Netzengpässen steuerbar sein. 
#     Als Entschädigung sieht der Netzbetreiber eine Ermäßigung der Netzentgelte vor. 
#     Seit dem 01. April 2025 kann das Modul 3 für steuerbare Verbrauchseinrichtungen genutzt werden, mit dem zeitvariable Netzentgelte möglich sind.
#     Jeder Netzbetreiber kann im Zeitraum von 24h ein 3 stufiges Netzentgeld erheben. In diesem Fall sind die Bedingungen des Netzbetreibers Westnetz genutzt worden. 
#     """)

st.header("⚙️ Optimierungen")
st.markdown("""
            Linearer Optimierungsalgorithmus mit einer der bib und der zielfunktion ... und den aus den Tarifen ergebenen Nebenbedingungen. 
            
            Die Optimierungen die berechnet werden ergeben sich daraus welche Möglichkeiten dem Haushalt zur Verfügung stehen. Die Optionen sind abhängig ob der Haushalt eine PV, eine steuerbare Verbrauchseinrichtung besitzt oder die PV-Anlage sich noch in den ersten 20 Jahren nach der Installation befindet, sprich noch die geförderte Einspeisevergütung erhält.
            
            Doofe Frage... wie sehen die Richtlinien aus wenn es keine PV gibt aber ne Batterie? Die kann ja nie ne Einspeisevergütung erhalten, läuft die dann unter gar keine Einspeisevergütung? Oder Direktvermarktung?
            """)

st.header("📈 Ergebnisse")
st.markdown("""
.... Ergebnis = Eigenverbrauchsoptimierung - gewählter Stromtarif (Schon einmal auf der ersten seite erklärt)
            Auflistung von Wechseloptionen immer gegen 1 oder 5. Sortiert nach größt möglicher ersparnis.
""")
