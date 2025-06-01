import streamlit as st


st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")
st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """)
st.markdown(""":blue[Fragen und Anregungen gerne an l.weghake@gmail.com]""")
st.markdown("Auf dieser Seite werden alle Einstellmöglichkeiten sowie die Annahmen des Rechners erklärt. Des Weiteren sind auf dieser Seite der Optimierungsprozess und die Interpretation des Ergebnisses erklärt.")


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


st.header("⚙️ Optimierungen")
st.markdown("""
            Für die Erzeugung des Lastgangs je nach Stromtarif wird ein lineares Optimierungsverfahren angewendet, welches die Kosten für den Endkunden minimiert. Dafür ist die Python-Bibliothek Scipy mit der Linprog Optimierungsfunktion verwendet worden. In die Kosten-Zielfunktion gehen die Bezugskosten für Energie aus dem Netz, Einspeisevergütung sowie Kosten für die Nutzung der Batterie. Die Kosten für die Nutzung der Batterie ist mit 10 Cent/kWh angenommen. Optimiert werden die Be- und Entladung der Batterie, der Netzbezug und die Einspeiseleistung. In die Nebenbedingungen der Optimierung geht das Leistungsgleichgewicht ein, welches ebenfalls einen Batteriewirkungsgrad von 96% hinterlegt ist. Des Weiteren sind als Nebenbedingungen das Ausschließlichkeitsprinzip des EEGs und die Berechnung des State of charge (SoC) definiert. In der Limitierung der Zustandsvariablen ist die Netzanschlussleistung auf 22 kW begrenzt. Jeder Berechnungsschritt kennt Daten über 24 Stunden und optimiert auf Basis dieser. Diese Berechnung wiederholt sich alle 12 Stunden über das gesamte Jahr 2024.

            Diese Berechnungen werden gleichzeitig für mehrere Stromtarife (Bezugs- und Einspeisetarife) durchgeführt. Welcher Stromtarif berechnet wird, bestimmen die Angaben über den Haushalt. Die Möglichkeiten der Wahl des Stromtarifs wird von den Tatsachen beeinflusst, ob eine steuerbare Verbrauchseinrichtung und/oder eine PV-Anlage vorhanden sind und ob diese eine geförderte Einspeisevergütung aktuell bekommt.
    
            Doofe Frage... wie sehen die Richtlinien aus wenn es keine PV gibt aber ne Batterie? Die kann ja nie ne Einspeisevergütung erhalten, läuft die dann unter gar keine Einspeisevergütung? Oder Direktvermarktung? Warscheinlich keine entladung möglich?
            """)

st.header("📈 Ergebnisse")
st.markdown("""
            Die Kosten für den Endverbraucher jeder Optimierung werden mit einer Optimierung mit den üblichen Stromtarifen aus festem Bezugspreis und ggf. der festen Einspeisevergütung nach dem EEG verglichen. Das Ergebnis, welches im Anschluss der Berechnung angezeigt wird, ist die Ersparnis bei einem Wechsel über das gesamte Jahr 2024.

            Wenn mehrere Stromtarifarten für den Haushalt zur Wahl stehen, werden die Ergebnisse von der größten zu kleinsten Ersparnis sortiert und in einer Zeile mit der Beschreibung des Stromtarifs aufgelistet.

""")
