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


# Stromverbrauch
st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")

st.markdown("""Diese Seite bietet eine Möglichkeit Kosteneinsparungen eines Haushalts für einen Wechsel auf einen dynamischen Stromtarif zu berechnen. 
            Darüber hinaus werden Ergebnisse aus einer wissenschaftlichen Arbeit präsentiert, für wen sich ein ein Wechsel auf einen dynamischen Stromtarife lohnt und welche Tarifmodelle sich zur Kostensenkung eignen.""")
st.markdown("""Seit dem Jahresanfang 2025 werden vermehrt Smart-Meter-Gateways (SMGW) in Haushaltszählerschränken verbaut.
            Diese ermöglichen dem Haushalt ein Wechsel auf zeitlich variable Stromtarife, die sich sowohl an Schwankungen des Börsenstrompreises für elektrische Energie orientieren können, wie auch an zeitvariablen Netzentgelten.
            Im Folgenden werden zunächst die unterschiedlichen Stromtarif-Modelle aufgeführt sowie Hintergrundinformationen zu dem Wechsel. Bitte lesen Sie sich die folgenden Themenbereiche durch, da diese entscheidend für das Verständnis der Berechnung sind.
            Anschließend ist ein Rechner aufgeführt, der unter Angabe von den eigenen Haushaltsstrukturen eine Abschätzung bietet, ob bei einem Wechsel unter den aktuellen Strukturen sich ein Wechsel lohnen kann.
            Auf der Seite Hintergrund Erklärungen sind Annahmen aufgeführt, die Grundlage der Berechnungsmöglichkeit sind und dort befinden sich ebenfalls Informationen zu den verwendeten Daten der Berechnung.
            """)
st.divider()

st.markdown("""##### Sie haben einen Smart-Meter-Gateway (SMGW) eingebaut bekommen oder interessieren sich dafür?""")
with st.expander("Was ist ein Smart-Meter-Gateway und welche Funktionen bietet es?"):
    st.markdown("""
                Ein Smart-Meter-Gateway (SMGW) gehört zur Messtechnik, die vom Messstellenbetrieb und ist ein Bauteil, was zusätzlich zum häufig genannten \"Stromzähler\" eingebaut wird. Das SMGW ist eine Kommunikationseinheit, die zum intelligenten Messsystem (iMSys) gehört, welches aus einer modernen Messeinrichtung (einem digitalen Zähler) und einem SMGW besteht.
                Diese Kommunikationseinheit empfängt Zählerdaten vom digitalen Zähler, speichert diese und kann zum Beispiel mit dem Energieversorger bezüglich der Abrechnung oder auch mit dem Netzbetreiber bezüglich Steuersignalen kommunizieren. Damit stellt der Besitz des SMGWs die Voraussetzung für eine dynamische Abrechnung dar.
                Des Weiteren bietet es auch einen Kommunikationsweg zum Haushaltsendkunden und dessen kommunikationsfähigen Geräte. Letzteres kann über eine Steuerbox realisiert werden. Anschließend ist ein Rechner aufgeführt, der unter Angabe von den eigenen Haushaltsstrukturen eine Abschätzung bietet, ob bei einem Wechsel unter den aktuellen Strukturen sich ein Wechsel lohnen kann.
                Auf der Seite Hintergrund Erklärungen sind Annahmen aufgeführt, die Grundlage der Berechnungsmöglichkeit sind und dort befinden sich ebenfalls Informationen zu den verwendeten Daten der Berechnung.
                
                :small[Quelle: Bundesnetzagentur, „Intelligente Messsysteme und moderne Messeinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/Metering/start.html. [Zugriff am: 19. Mai 2025].]""")

with st.expander("Wer bekommt ein Smart-Meter-Gateway eingebaut?"):
    st.markdown("""
                Der Rollout von SMGWs ist mit einer Gesetzesnovelle im Mai 2023 beschleunigt worden. Seit 2025 beginnt der Pflichteinbau von SMGWs für Haushalte mit einem Jahresdurchschnittsverbrauch zwischen 6000 kWh und 100.000 kWh mit einer Erzeugerleistung zwischen 7 kWp und 100 kWp, oder die im Besitz einer steuerbaren Verbrauchseinrichtung nach Energiewirtschaftsgesetz (EnWG) §14a sind. Das Thema steuerbare Verbrauchseinrichtungen wird im Folgenden nochmal genauer erklärt.
                Ab 2028 beginnt ein weiter Pflichtrollout für Verbraucher über den zuvor genannten Energie und Leistungsmengen. Optional werden die übrigen Verbraucher ausgestattet. Ein SMGW kann auch auf Anfrage des Endkunden unabhängig des Pflichtrollouts eingebaut werden, allerdings kann dies höhere Kosten für den Endkunden verursachen.  Die Kosten des Pflichtrollouts sind gesetzlich gedeckelt auf rund 70€ - 100€ jährlich für digitalen Zähler und SMGW. Die Einbauten neben dem Pflichtrollout können zusätzlich einmalige Kosten im 3-stelligen Bereich mit sich bringen. Der Einbau wird direkt vom Messstellenbetreiber geregelt.

                :small[Quelle: Haufe Online Redaktion, „Smart-Meter-Rollout: Das ist seit dem 1. Januar Pflicht“, Haufe.de, 2. Jan. 2025. [Online]. Verfügbar: https://www.haufe.de/immobilien/wirtschaft-politik/smart-meter-rollout_84342_638840.html. [Zugriff am: 25. Mai 2025].""")
with st.expander("Warum muss ich ein Smart-Meter-Gateway bei mir einbauen lassen?"):
    st.markdown("""
                Der Einbau von SMGW in Haushalten ist essenziell wichtig, um die elektrische Energieversorgung klimafreundlicher und zukunftssicher zu gestalten.
                Primär bieten die Daten, die das SMGW an die Netzbetreiber bzw. Energieversorger sendet mehr Transparenz wie der Zustand der Netze und der Hausverbrauch wirklich aussieht. Die Netzbetreiber können aus den Daten ermitteln, ob es zu Überlastungen der Betriebsmittel des Netzes kommen kann und die Energieversorger können mit den Daten aus Verbrauchs- und Erzeugeranlagen besser den Haushalten die Energie vorhalten, die sie wirklich benötigen.
                Ebenfalls können durch die Möglichkeit der zeitgenauen Abrechnung Anreize zur Lastverschiebung gesetzt werden, die wiederum den Anteil der elektrischen Energie aus erneuerbaren Erzeugeranlagen verbessern können.
                Ebenso wichtig zur Erhaltung der Zuverlässigkeit ist die Steuerbarkeit von Erzeugeranlagen und großen Verbrauchseinrichtungen, sollte sich das Netz in einem kritischen Zustand befinden.

                :small[Quelle: Bundesnetzagentur, „Intelligente Messsysteme und moderne Messeinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/Metering/start.html. [Zugriff am: 19. Mai 2025].]""")

st.divider()
st.markdown("""##### Was sind Dynamische Stromtarife?""")
with st.expander("Welche Arten von dynamischen Stromtarifen gibt es?"):
    st.markdown("""
                Neben den festen Stromtarifen können Energieversorger auch zeitlich flexible Stromtarife anbieten. Diese können sich an unterschiedlichen Modellen orientieren. Alle Stromtarife basieren mehr oder weniger dynamisch auf den Schwankungen des Börsenstrompreises. Zum einen können sich Tarife zu festen Tageszeiten auf festgelegte Preise verändern, wie beispielsweise Nachtstromtarife. Andere wiederum sind direkt mit dem Börsenstrompreis gekoppelt und passen sich an den durchschnittlichen Preis beispielsweise monatlich oder täglich an. Die im Folgenden diskutierten dynamischen Stromtarife passen sich auf die in Echtzeit gehandelten Börsenstrompreise an. Die Börsenstrompreise werden in stündlichen bzw. viertelstündlichen Auktionen gehandelt. Aktuell sind in der folgenden Berechnung für die dynamischen Stromtarife die stündlich gehandelten Börsenstrompreise der EPEX Spot Day-Ahead Auktion hinterlegt. Die Daten sind bezogen worden von der Website Energy Charts https://energy-charts.info/ am 23.01.2025. 
                Da mit einem dynamischen Stromtarif ein Anreiz zur Lastverschiebung seitens des Endkunden geschaffen wird, muss seit 2025 jeder Energieversorger einen dynamischen Stromtarif anbieten. Ebenfalls können durch die Möglichkeit der zeitgenauen Abrechnung Anreize zur Lastverschiebung gesetzt werden, die wiederum den Anteil der elektrischen Energie aus erneuerbaren Erzeugeranlagen verbessern können.
                Ebenso wichtig zur Erhaltung der Zuverlässigkeit ist die Steuerbarkeit von Erzeugeranlagen und großen Verbrauchseinrichtungen, sollte sich das Netz in einem kritischen Zustand befinden.

                :small[Quelle: Forschungsstelle für Energiewirtschaft e. V. (FfE), „Dynamische Stromtarife - Tarifarten, Vor- und Nachteile, technische Anforderungen“, FfE, 18. Aug. 2023. [Online]. Verfügbar: https://www.ffe.de/veroeffentlichungen/beitragsreihe-dynamische-stromtarife-tarifarten-vor-und-nachteile-technische-anforderungen/. [Zugriff am: 19. Mai 2025].]
                """)

with st.expander("Welchen Nutzen erfüllen dynamische Stromtarife?"):
    st.markdown("""
                Da dynamische Stromtarife auf den Börsenstrompreisen basieren, spiegeln diese das Gleichgewicht aus Erzeugung und Verbrauch von elektrischer Energie im System wider. Dies hat den Effekt, einen monetären Anreiz für den Kunden zu bilden, wenn mehr Erzeugung aus erneuerbaren Energien vorhanden ist als von den Verbrauchern abgenommen wird.
                Eine Verschiebung von Lasten in Zeiten niedriger Börsenstrompreise fördert die Integrität erneuerbaren Energien, spart CO2 Emissionen der Kraftwerke, die zum regulären Zeitpunkt die Energie bereitgestellt hätten, die Auslastung der Netz-Betriebsmittel in Zeiten hoher Nachfrage sinkt, so können Netzausbaumaßnahmen auf das Nötigste reduziert werden und gleichzeitig kann der Endverbraucher Kosten sparen.

                Ein Wechsel auf einen dynamischen Stromtarif in Kombination mit Verbrauchsspitzen in den preislich hohen Zeitpunkten kann gleichermaßen einen Kostennachteil für den Endkunden bedeuten. Ein Wechsel auf einen dynamischen Stromtarif in Kombination mit Verbrauchsspitzen in den preislich hohen Zeitpunkten kann gleichermaßen einen Kostennachteil für den Endkunden bedeuten.

                Da diese individuelle Lastverschiebung nur schwer akkurat zu simulieren ist, geht die Berechnung vom Fall aus, dass der Endkunde sein Verhalten mit dem Wechsel auf einen dynamischen Stromtarif nicht verändert. Die monetären Vorteile durch eine Lastverschiebung können nach eigenem Interesse individuell abgeschätzt werden.

                :small[Quelle: Forschungsstelle für Energiewirtschaft e. V. (FfE), „Dynamische Stromtarife - Tarifarten, Vor- und Nachteile, technische Anforderungen“, FfE, 18. Aug. 2023. [Online]. Verfügbar: https://www.ffe.de/veroeffentlichungen/beitragsreihe-dynamische-stromtarife-tarifarten-vor-und-nachteile-technische-anforderungen/. [Zugriff am: 19. Mai 2025].]

                """)
with st.expander("Wie ist ein dynamischer Stromtarif aufgebaut?"):
    st.markdown("""
                Wie jeder feste Stromtarif auch besteht auch ein dynamischer Stromtarif immer aus einem monatlichen Fixpreis und einem variablen Anteil je kWh elektrischer Energie. Nur der variable Anteil verändert sich dynamisch mit den Schwankungen des Börsenstrompreises. Zu dem variablen Anteil gehören fix die Netzentgelte, Konzessionsabgaben, Stromsteuer, Offshore-Umlage, KWKG-Umlage, NEV-Umlage und ein Energieversorger spezifischer Aufschlag ein. Stündlich oder viertelstündlich verändern sich die Energiekosten, die dem Börsenstrompreis entsprechen und die Mehrwertsteuer, die sich dafür ergibt. Letzteres verstärkt die Schwankungen im Endpreis erheblich.
                In der Berechnung ist ein dynamischer Stromtarif von Tibber verwendet worden, mit Netzentgelten des Netzbetreibers Westnetz, Stand Januar 2025. Tibber erhob zu dem Zeitpunkt eine monatliche Gebühr von 5,99 € und einen variablen Anteil pro kWh von 2,15 Cent/kWh.
                """)
st.divider()

st.markdown("""##### Was muss ich über steuerbare Verbrauchseinrichtungen wissen?""")
with st.expander("Warum sollen Haushaltsgeräte vom Netzbetreiber aus steuerbar sein?"):
    st.markdown("""
                Durch die voranschreitende Sektorenkopplung, sprich der Versorgung der Sektoren Haushaltswärme und Individualverkehr mit elektrischer Energie, gelangen immer mehr elektrische Verbraucher mit hoher Leistungsaufnahme in die Haushalte, die häufig zu ähnlichen Zeiten verwendet werden. Nicht alle Versorgungsnetze sind gewiss auf die bevorstehenden Lasten ausgelegt und müssen in Zukunft ausgebaut und digitalisiert werden. Daher ist es das Ziel, all diese flexiblen Verbraucher mit hoher Leistungsaufnahme vom Netzbetreiber aus steuerbar zu machen. Der Netzbetreiber darf bei einer nachgewiesenen Netzüberlastung die Leistungsaufnahme dieser Geräte reduzieren. Als Entschädigung werden die Netzentgelte für den Endkunden reduziert.
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]""")
with st.expander("Was ist eine steuerbare Verbrauchseinrichtung?"):
    st.markdown("""
                Für die Umsetzung des Ziels ist in dem Energiewirtschaftsgesetz (EnWG) geregelt, welche Geräte als eine steuerbare Verbrauchseinrichtung betitelt werden. Dabei handelt es sich um Stromspeicher, Klimageräte, Wärmepumpen und Wallboxen mit einer Netzanschlussleistung größer 4,2 kW, die nach dem 01.01.2024 in Betrieb genommen worden sind. Temporär muss sich diese vom Netzbetreiber auf 4,2 kW dimmen lassen können.
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Welchen Nutzen kann ich aus meinen steuerbaren Verbrauchseinrichungen ziehen?"):
    st.markdown("""
                Die Entschädigung der Steuerungsmöglichkeit wird in drei frei wählbaren Modulen geregelt. Das erste Modul enthält eine pauschale Entschädigung zwischen 110 und 190 €, je nach Netzbetreiber. Das Modul kann mit dem Modul drei kombiniert werden, diese Module benötigen keine eigene Messung der Energie der steuerbaren Verbrauchseinrichtung. Für das zweite Modul muss die Energie der steuerbaren Verbrauchseinrichtung separat zum Haushaltsstrom gemessen werden. Dafür erhält der Endkunde auf die von der steuerbaren Verbrauchseinrichtung verbrauchten elektrischen Energie eine prozentuale Netzentgeltreduzierung von 40%. Das dritte Modul, welches nur in Kombination mit Modul 1 gewählt werden kann, beinhaltet zeitvariable Netzentgelte. Dieses Modul ist wählbar seit April 2025. Die Netzbetreiber können selbst ein dreistufigen Netzentgeltplan bestimmen. Dabei müssen sich in 24 h mindestens einmal ein Hochtarif, Standardtarif und Niedrigtarif wiederholen.
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]
                
                In der Berechnung wird ein zeitvariables Netzentgelt von dem Verteilnetzbetreiber Westnetz verwendet. Dieser hat ein Niedertarifpreis von 1,19 Cent/kWh, ein Standardtarifpreis von 11,88 Cent/kWh und einen Hochtarifpreis von 17,75 Cent/kWh in 2025. Der festgelegte Zeitplan von Westnetz entspricht zwischen 0 – 6 Uhr den Niedertarif und zwischen 15 – 20 Uhr den Hochtarif. Zu jeder anderen Zeit wird der Standardtarif berechnet. Damit wird die Kombination aus Modul 1 und 3 zugrunde gelegt.
                
                :small[Quelle: Westnetz GmbH, „Preisblätter Westnetz Strom 2025“, Westnetz GmbH, 2025. [Online]. Verfügbar: https://www.westnetz.de/content/dam/revu-global/westnetz/documents/ueber-westnetz/unser-netz/netzentgelte-strom/preisblaetter-westnetz-strom-01-01-2025.pdf. [Zugriff am: 21. Mai 2025].]
                """)
st.divider()

st.markdown("""##### Was muss ich alles über die EEG-Vergütung wissen?""")
with st.expander("Was ist die Feste Einspeisevergütung für den eingespeiste elektrische Energie aus Erneuerbaren Energieanlagen?"):
    st.markdown("""
                In dem Erneuerbaren-Energien-Gesetz ist die vorrangige Abnahme von elektrischer Energie aus erneuerbaren Energieanlagen geregelt. Ebenfalls ist dort die Einspeisevergütung geregelt, die sich nach Installationsdatum, Leistung der Anlage und Art der Einspeisung (Voll- oder Teileinspeisung ins Netz) bemisst.

                Für Anlagen, die älter als 20 Jahre sind, erhalten aktuell bis 2032 so geregelt weiterhin eine vorrangige Abnahme der Energie und eine Einspeisevergütung, die sich an den Börsenstrompreis orientiert und Jahresmarktwert Solar heißt.
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Was ist die Direktvermarktung?"):
    st.markdown("""
                In dem Solarpaket 1 von April 2025, in dem auch die weitere Einspeisevergütung nach 20 Jahren erweitert worden ist, ist auf eine Vereinfachung von der Direktvermarktung von kleinen Anlagen kleiner 25 kWp hingewiesen worden. Diese Art der Vermarktung von eigenerzeugten Energie bringt ähnliche Vorteile für das Energiesystem mit, die bereits für variable Bezugspreise aufgeführt sind. Je nach externem Direktvermarkter kommen unterschiedlich hohe Dienstleistungsgebühren hinzu, da die elektrische Energie manuell an der Börse gehandelt werden muss. 
                
                In der Berechnung sind Dienstleistungskosten des Energieversorgers Luox Energy (Stand Mai 2025) mit 3% variablen Kosten einberechnet. Zu dem muss eine Gebühr von 200€ einmalig als Einrichtungsgebühr verrichtet werden.
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Was ist bei einer Kombination aus Batteriespeichern und der PV-Anlage zu berücksichtigen?"):
    st.markdown("""
                Ein weiterer Punkt im EEG ist die Behandlung von Speichern. Dieses Gesetz regelt die Einspeisevergütung der Energie, die von der Batterie ins Netz abgegeben werden kann. Das dort definierte Ausschließlichkeitsprinzip besagt dass der Speicher ausschließlich mit elektrischer Energie aus erneuerbaren Energieanlagen stammen darf und kein Netzbezug erfolgen darf, auch wenn der zugehörige Stromtarif auf 100% erneuerbaren Energien ausgelegt ist.

                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                
                Deshalb muss in den folgenden Einstellungen bei einer Batterie und EEG-Vergütung ausgewählt werden, ob die Batterie ausschließlich aus dem Netz beziehen darf oder ausschließlich ins Netz mit EEG-Vergütung einspeisen darf.
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „FAQs zum Solarpaket I“, BMWK, [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/FAQ/Solarpaket/faq-solarpaket.html. [Zugriff am: 21. Mai 2025].]
                """)
                # Um die Batteriespeicher in Haushalten in Zukunft netzdienlich einsetzen zusetzen wird über die Definition des Ausschließlichkeitsprinzips diskutiert. Dies würde zusätzliche Freiheiten in der Nutzung ermöglichen, die in der folgenden Berechnung mit einfließen können. Eine alternative (Worst-Case) Betrachtung für Altanlagen die dem aktuell denklichen netzdienlichen Gedanken verfolgt, also Anlage die bereits 20 Jahre eine Einspeisevergütung gefördert aus dem EEG erhaltben haben, könnte sein zum zeitlich aktuellen Börsenstrompreis einzuspeisen. Diese Betrachtung kann ebenfalls in der Berechnung ausgewählt werden. Diese Betrachtung dient dazu abzuschätzen in wie fern Aufdach PV-Anlagen von Privatbesitzern im Markt stehen und ohne Förderungen auskommen können. (Naja vergleich bezieht sich noch immer auf Einspeisevergütung… nicht abschätzbar grade)
                
                # :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                

st.divider()
st.markdown("""##### Welche Annahmen trifft die Berechnung und welche Grenzen weißt diese auf?""")
st.markdown("""
            Die Berechnung soll dazu dienen, für sich selbst eine Einschätzung zu bekommen, ob sich ein Wechsel auf einen dynamischen Stromtarif lohnen würde.
            Die Berechnung basiert auf dem Jahresdurchschnittsverbrauch des Haushalts sowie optional auf der Erzeugung einer vorhandenen PV-Anlage, die Nutzung einer Batteriekapazität in Kombination mit einem intelligenten Heim-Energiemanagement-System (HEMS), das den Energiefluss intelligent steuern kann. Die Datengrundlage basiert auf dem Jahr 2024.
            
            Das Ergebnis der Berechnung bezieht sich bei allen unterschiedlichen Tarifen immer auf den Vergleich der Eigenverbrauchsoptimierung, sprich einem normalen festen Stromtarif, ggf. einer festen Einspeisevergütung nach dem EEG und ggf. eine Batterie, die unter den Bedingungen kostensenkend eingesetzt wird. Der kosteneffiziente Einsatz der Batterie setzt immer ein Heim-Energiemanagement System (HEMS) voraus. Der Optimierungsalgorithmus bei der Berechnung soll immer die Kosten für den Kunden minimieren.

            Die hinterlegten Lastverläufe sind durchschnittliche Lastverläufe für den ausgewählten Jahresdurchschnittsverbrauch auf der Grundlage von typischen Haushaltsverteilungen in Deutschland. Bitte betrachten Sie bei der Auswahl Ihren tatsächlichen Haushaltsverbrauch, falls bereits eine PV-Eigenverbauch stattfindet, entspricht dies nicht dem Netzbezug.

            Die Berechnung setzt voraus, dass sich das individuelle Verbrauchsverhalten mit dem Wechsel des Stromtarifs **nicht ändert**. Es erfolgt nur eine **optimierte** Batterienutzung und der PV-Einspeisung. Eine bewusste Verhaltensänderung in Verbindung mit einem dynamischen Stromtarif kann zu einer weiteren Ersparnis führen. Dabei sollte bewusst sein, dass im gleichen Maße ein Verhalten ungünstig zum Börsenstrompreis auch zusätzliche Kosten verursachen. Ebenfalls positiv auf Kosteneinsparungen tragen flexiblen Verbraucher gesteuert über ein HEMS bei, wie zum Beispiel Wärmepumpen und Wallboxen, die ebenfalls nicht in der Berechnung berücksichtigt werden.
            """)
st.divider()
st.markdown("""
                Weitere Informationen zu dem Rechner erhalten Sie auf der Seite Hintergrund Erklärungen in der Seitenleiste und unterhalb auswählbar. Beachten Sie, dass laufende Berechnungen gestoppt werden, wenn die Seite gewechselt wird. """)
st.page_link("explain.py", label="Hintergrund Erklärungen")
st.divider()
st.markdown(""" ##### Technischer Hinweis und Haftungsausschluss: """)
           
st.warning("""Die auf dieser Website durchgeführten Berechnungen erfolgen auf Grundlage vereinfachter Modelle, definierter Annahmen sowie idealisierter Randbedingungen. Abweichungen zwischen den berechneten Werten und realen Gegebenheiten sind möglich und systembedingt. Die Ergebnisse dienen ausschließlich der unverbindlichen Orientierung und stellen keine belastbare Planungs- oder Entscheidungsgrundlage dar. Es wird keine Haftung für die Richtigkeit, Vollständigkeit oder Anwendbarkeit der ausgegebenen Ergebnisse übernommen. Die Nutzung erfolgt auf eigenes Risiko.
""")
st.divider()
# -------------------------- Calculation ---------------------------------------

st.divider()
st.markdown("""##### Berechnung von Ersparnissen bei einem Wechsel des Stromtarifmodels unter Angaben Ihrer Haushaltsstruktur""")


st.markdown("""##### Lastgangauswahl über dem durchschnittlichen Stromverbrauch eines Jahres""")
st.slider("Jährlicher Stromverbrauch (kWh)", 1000, 8000, key="consumption", step=500, help="Bitte wählen Sie ihren jährlichen Haushaltsstromverbrauch aus. Der selbstverbrauchte Photovoltaikstrom und die Batterieladung wird seperat betrachtet.") #, disabled=st.session_state.get("calculating"))

st.markdown("""##### Steuerbare Verbrauchseinrichtungen nach EnWG 14a """)
st.checkbox("Ich besitze eine steuerbare Verbrauchseinrichtung.", key="controllable_device")  

# PV-Anlage
st.markdown("""##### Angaben zur installierten Photovoltaik Anlage""")
           
st.checkbox("Ich besitze eine PV-Anlage.", key="has_pv") #, disabled=st.session_state.get("calculating", False))
if st.session_state.get("has_pv", False):
    st.slider("Installierte PV-Leistung (kWp)", 1, 25, step=1, key="pv_power") #, disabled=st.session_state.get("calculating", False))
    direction_map = { "Nord": 0, 'Nord-Ost': 45, "Ost": 90, 'Süd-Ost': 135, "Süd": 180, "Süd-West": 225,  "West": 270}
    if "pv_compass" not in st.session_state:
        st.session_state.pv_compass = "Süd"
    st.selectbox("Ausrichtung der PV-Anlage", list(direction_map.keys()), key="pv_compass") #, disabled=st.session_state.get("calculating", False))
    st.session_state.pv_direction = direction_map[st.session_state.pv_compass]
    st.toggle("Ü20-Anlage AUS / EEG-Vergütung EIN", key="has_eeg")  

    # EEG-Vergütung
    # st.checkbox("Ist Ihre Anlage noch innerhalb der 20 Jahren garantierter EEG-geförderter Einspeisevergütung?", key="has_eeg", help="Sollte Ihre PV-Anlage bereits ausgefördert sein, könnte sich in der Zukunft ein netzdienliches Verhalten auszahlen, welches in dem Fall der Nicht-Auswahl berechnet wird.")
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
    # st.session_state.has_eeg = 0
    st.session_state.installation_date = pd.to_datetime("2024.01.01", format="%Y.%m.%d")

# Batterie
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
        
opti_dict = {i: {"select": None} for i in opti_numbers}

for key in opti_dict:
    opti_dict[key]["select"] = control.select_optimisation_behaviour(key)



st.divider()        
# Berechnung starten
if "results" not in st.session_state:
    st.session_state.results = []


if st.button("Berechnung stoppen"):
    st.session_state.calculating = False
    st.rerun()

if st.button("Berechnung starten", disabled=st.session_state.get("calculating", False)):
    st.session_state.calculating = True

    st.warning("Die Berechnung kann je nach Haushaltstyp  1 bis 2 Minuten dauern, bitte haben Sie Geduld.")
    
    
    st.session_state.loadprofile = st.session_state.consumption # loadprofiles[st.session_state.consumption]

    data, averageEnergyHousehold =  control.data_generator.loadData(st.session_state.loadprofile,
                                                                        st.session_state.pv_direction, 
                                                                        st.session_state.pv_power,
                                                                        st.session_state.battery_capacity) 
    
    
    data = control.price_generator.calculate_energy_prices( data, averageEnergyHousehold,
                                                                st.session_state.controllable_device)



    month_pv_installation = st.session_state.installation_date.month
    year_pv_installation  = st.session_state.installation_date.year
    static_feed_in_price,  static_bonus_feed_in =  control.get_eeg_prices(year_pv_installation,month_pv_installation)

    battery_power = st.session_state.battery_capacity *  control.min_data/60 

    input_optimisation =    [ control.optimise_time,  control.step_time, st.session_state.battery_capacity,
                                 control.battery_costs,  battery_power, 
                                 control.grid_power,  static_feed_in_price,  static_bonus_feed_in]
    battery_usage = st.session_state.battery_usage

    queue = multiprocessing.Queue()
    processes = {}
    for key in opti_dict:
        processes[key] = multiprocessing.Process(
        target=control.opimisation.select_optimisation,
        args=(data, input_optimisation, opti_dict[key]["select"], battery_usage, queue, key)
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




    for key in opti_dict:
        processes[key].join()
    
    for key in opti_dict:
        opti_dict[key]["cost"] = control.analysis.single_cost_batterycycle_calculation(opti_dict[key]["result"], opti_dict[key]["select"])
        if key == 1 or key == 5:
            origin_key = key
        else:
            opti_dict[key]["benefit"] = opti_dict[origin_key]["cost"]['2024-12-31'] - opti_dict[key]["cost"]['2024-12-31']
            # st.write(f"{benefit} = {costs_evo['2024-12-31']} - {costs_selected['2024-12-31']}")
    print(opti_dict[key]["benefit"])
    print(opti_dict[origin_key])
    print(opti_dict[key])


    st.session_state.calculating = False

# Ergebnisse anzeigen
st.write("### Ergebnisse")
st.markdown("""Die Ergebnisse der Berechnungen geben die Kosteneinsparung an, die angefallen wären, hätte man im Jahr 2024 den Stromtarif gewechselt. Ist das Ergebnis negativ, wären höhere Kosten angefallen bei einem Wechsel gegenüber dem festen Stromtarif in Kombination mit fester Einspeisevergütung für die ins Netz eingespeiste Energie. """)

benefit_keys = [key for key in opti_dict if "benefit" in opti_dict[key]]
header_cols = st.columns(4)
header_cols[0].markdown("**Interne Nummer**")
header_cols[1].markdown("**Stromtarif**")
header_cols[2].markdown("**Einspeisetarif**")
header_cols[3].markdown("**Ersparnis**")
if not benefit_keys:
    st.info("Es wurden noch keine Optimierungsergebnisse berechnet.")
else:
    try:
        # Keys sortieren nach Benefit-Wert, absteigend
        sorted_keys = sorted(benefit_keys, key=lambda k: opti_dict[k]["benefit"], reverse=True)

        for key in sorted_keys:
            if key in (1, 5):  # Diese ggf. ausblenden
                continue

            opti_sel = opti_dict[key].get("select", ["", "Tarif N/A", "EEG N/A"])
            opti_ben = opti_dict[key]["benefit"]

            col1, col2, col3, col4 = st.columns([1, 3, 3, 2])

            col1.write(f"**{key}.**")
            col2.write(f"**{opti_sel[1]}**")
            col3.write(f"**{opti_sel[2]}**")
            col4.write(f"**{round(opti_ben, 2)} €**")
    except Exception as e:
        st.error(f"Fehler bei der Ergebnisanzeige: {e}")

