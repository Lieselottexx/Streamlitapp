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
    st.session_state.static_ZVNE            = False
    st.session_state.has_pv                 = False
    st.session_state.pv_power               = 5
    st.session_state.pv_compass             = "Süd"
    st.session_state.has_eeg                = False
    st.session_state.installation_date      = pd.to_datetime("2018-01-01")
    st.session_state.has_battery            = False
    st.session_state.battery_capacity       = 3
    st.session_state.battery_usage          = "Energie einspeisen"
    st.session_state.direct_market          = False

# st.write("Session initialized:", st.session_state)



# Stromverbrauch
st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")

st.markdown("""Diese Seite bietet eine Möglichkeit Kosteneinsparungen eines Haushalts für einen Wechsel auf einen dynamischen Stromtarif zu berechnen. 
            Darüber hinaus werden Ergebnisse aus einer wissenschaftlichen Arbeit präsentiert, für wen sich ein ein Wechsel auf einen dynamischen Stromtarife lohnt und welche Tarifmodelle sich zur Kostensenkung eignen.""")
st.markdown("""Seit dem Jahresanfang 2025 werden vermehrt Smart-Meter-Gateways (SMGW) in Haushalts-Zählerschränken verbaut.
            Diese ermöglichen dem Haushalt ein Wechsel auf zeitlich variable Stromtarife, die sich sowohl an Schwankungen des Börsenstrompreises für elektrische Energie orientieren können, wie auch an zeitvariablen Netzentgelten.
            Im Folgenden werden zunächst die unterschiedlichen Stromtarif-Modelle aufgeführt sowie Hintergrundinformationen zu dem Wechsel. Bitte lesen Sie sich die folgenden Themenbereiche durch, da diese entscheidend für die Berechnung sind.
            Anschließend ist ein Rechner aufgeführt, der unter Angabe von den eigenen Haushaltsstrukturen eine Abschätzung bietet ob bei einem Wechsel unter den aktuellen Strukuren sich ein Wechsel lohnen kann.
            Auf der Seite Hintergrund Erklärungen sind Annahmen aufgeführt, die Grundlage der Berechnungsmöglichkeit sind und dort befinden sich ebenfalls Informationen zu den verwendeten Daten der Berechnung.
            """)
st.divider()

st.markdown("""##### Sie haben einen Smart-Meter-Gateway (SMGW) eingebaut bekommen oder interessieren sich dafür?""")
with st.expander("Was ist ein Smart-Meter-Gateway und welche Funktionen bietet es?"):
    st.markdown("""
                Ein Smart-Meter-Gateway (SMGW) gehört zur Messtechnik die vom Messstellenbetrieb und ist ein Bauteil was zusätzlich zum häufig genannten \"Stromzähler\" eingebaut wird. Das SMGW ist eine Kommunikationseinheit die zum intelligenten Messsystem (iMSys) gehört, welches aus einer modernen Messeinrichtung (einem digitalen Zähler) und einem SMGW besteht. 
                Diese Kommunikationseinheit empfängt Zählerdaten vom digitalen Zähler, speichert diese und kann zum Beispiel mit dem Energieversorger bezüglich der Abrechnung oder auch mit dem Netzbetreiber bezüglich Steuersignalen kommunizieren. Damit stellt der Besitz des SMGWs die Vorraussetzung für eine dynamische Abrechnung dar.
                Desweiteren bietet es auch einen Kommunikationsweg zum Haushalts-Endkunden und dessen kommunikationsfähigen Geräte. Letzteres kann über eine Steuerbox realisiert werden.\n 
                
                :small[Quelle: Bundesnetzagentur, „Intelligente Messsysteme und moderne Messeinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/Metering/start.html. [Zugriff am: 19. Mai 2025].]""")

with st.expander("Wer bekommt ein Smart-Meter-Gateway eingebaut?"):
    st.markdown("""
                Der Rollout von SMGWs ist mit einer Gesetzes Novelle im Mai 2023 beschleunigt worden. Seit 2025 beginnt der Pflichteinbau von SMGWs für Haushalte mit einem Jahresdurchschnittsverbrauch zwischen 6000 kWh und 100.000 kWh, mit einer Erzeugerleistung zwischen 7 kWp und 100 kWp, oder die im Besitz einer steuerbaren Verbrauchseinrichtung, nach Energiewirtschaftsgesetz (EnWG) §14a sind. Das Thema steuerbare Verbrauchseinrichtungen wird im Folgenden nochmal genauer erklärt. Ab 2028 beginnt ein weiter Pflichtrollout für Verbraucher über den zuvor genannten Energie und Leistungsmengen. Optional werden die übrigen Verbraucher ausgestattet. Ein SMGW kann auch auf Anfrage des Endkundens unabhängig des Pflichrollouts eingebaut werden, allerdings kann dies höhere Kosten für den Endkunden verursachen.  Die Kosten des Pflichrollouts sind gesetzlich gedeckelt auf rund 70€ - 100€ jährlich für Digitalen Zähler und SMGW. Die Einbauten neben dem Pflichtrollout können zusätzlich einmalige Kosten im 3-stelligen Bereich mit sich bringen. Der Einbau wird direkt vom Messstellenbetreiber geregelt.
                
                :small[Quelle: Haufe Online Redaktion, „Smart-Meter-Rollout: Das ist seit dem 1. Januar Pflicht“, Haufe.de, 2. Jan. 2025. [Online]. Verfügbar: https://www.haufe.de/immobilien/wirtschaft-politik/smart-meter-rollout_84342_638840.html. [Zugriff am: 25. Mai 2025].""")
with st.expander("Warum muss ich ein Smart-Meter-Gateway bei mir einbauen lassen?"):
    st.markdown("""
                Der Einbau von SMGW in Haushalten ist essentiell wichtig um die elektrische Energieversorgung klimafreudlicher und zukunftssicher zu gestalten. 
                Primär bieten die Daten die das SMGW an die Netzbetreiber bzw Energieversorger sendet mehr transparenz wie der Zustand der Netze und der Hausverbrauch wirklich aussieht. Die Netzbetreiber können aus den Daten ermitteln ob es zu Überlastungen der Betriebsmittel des Netzes kommen kann und die Energieversorger können mit den Daten aus Verbrauchs- und Erzeugeranlagen, besser den Haushalten die Energie vorhalten die sie wirklich benötigen. Ebenfalls können durch die Möglichkeit der zeitgenauen Abrechnung Anreize zur Lastverschiebung gesetzt werden, die wiederum den Anteil der Elektrischen Energie aus Erneuerbaren Erzeugeranlagen verbessern können.
                Ebenso wichtig zur Erhaltung der Zuverlässigkeit ist die Steuerbarkeit von Erzeugeranlagen und großen Verbrauchseinrichtungen, sollte sich das Netz in einem kritischen Zustand befinden. 
                
                :small[Quelle: Bundesnetzagentur, „Intelligente Messsysteme und moderne Messeinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/Metering/start.html. [Zugriff am: 19. Mai 2025].]""")

st.divider()
st.markdown("""##### Was sind Dynamische Stromtarife?""")
with st.expander("Welche Arten von dynamischen Stromtarifen gibt es?"):
    st.markdown("""
                Neben den festen Stromtarifen können Energieversorger auch zeitlich flexible Stromtarife anbieten. Diese können sich an unterschiedlichen Modellen orientieren. Alle Stromtarife basieren mehr oder weniger dynamisch auf den Schwankungen des Börsenstrompreises. Zum einen können sich Tarife zu festen Tageszeiten auf festgelegte Preise verändern, wie beispielsweise Nachtstromtarife. Andere wiederum sind direkt mit dem Börsenstrompreis gekoppelt und passen sich and den durchschnittlichen Preis, beispielsweise monatlich oder täglich, an. Die im Folgenden diskutierten dynamischen Stromtarife passen sich auf die in Echtzeit gehandelten Börsenstrompreise an. Die Börsenstrompreise werden in stündlichen bzw. viertelstündlichen Auktionen gehandelt. Aktuell sind in der folgenden Berechnung für die dynamischen Stromtarife die stündlich gehandelten Börsenstrompreise der EPEX Spot Day-Ahead Auktion hinterlegt. Die Daten sind bezogen worden von der Website Energy Charts https://energy-charts.info/ am 23.01.2025. 
                Da mit einem dynamische Stromtarif ein Anreiz zur Lastverschiebung seitens des Endkundens geschaffen wird, muss seit 2025 jeder Energieversorger einen dynamischen Stromtarif anbieten.
                
                :small[Quelle: Forschungsstelle für Energiewirtschaft e. V. (FfE), „Dynamische Stromtarife - Tarifarten, Vor- und Nachteile, technische Anforderungen“, FfE, 18. Aug. 2023. [Online]. Verfügbar: https://www.ffe.de/veroeffentlichungen/beitragsreihe-dynamische-stromtarife-tarifarten-vor-und-nachteile-technische-anforderungen/. [Zugriff am: 19. Mai 2025].]
                """)

with st.expander("Welchen Nutzen erfüllen dynamische Stromtarife?"):
    st.markdown("""
                Da dynamische Stromtarife auf den Börsenstrompreisen basieren, spiegeln diese das Gleichgewicht aus Erzeugung und Verbrauch von elektrischer Energie im System wider. Dies hat den Effekt einen monitären Anreiz für den Kunden zu bilden wenn mehr Erzeugung aus Erneuerbaren Energien vorhanden ist als von den Verbrauchern abgenommen wird. 
                Eine Verschiebung von Lasten in Zeiten niedriger Börsenstrompreise fördert die Integrität Erneuerbaren Energien, spart CO2 Emissionen der Kraftwerke die zum regulären Zeitpunkt die Energie bereitgestellt hätten, die Auslastung der Netz-Betriebsmittel in Zeiten hoher Nachfrage sinkt, so können Netzausbaumaßnahmen auf das nötigste reduziert werden und gleichzeitig kann der Endverbraucher Kosten sparen. 
                
                Ein Wechsel auf einen dynamischen Stromtarif in Kombination mit Verbrauchsspitzen in den preislich hohen Zeitpunken kann gleichermaßen einen Kostennachteil für den Endkunden bedeuten. 
                
                Da diese individuelle Lastverschiebung nur schwer akurat zu simulieren ist geht die Berechnung vom Fall aus, dass der Endkunde sein Verhalten mit dem Wechsel auf einen dynamischen Stromtarif nicht verändert. Die monitären Vorteile durch eine Lastverschiebung können nach eigenem Interesse individuell abgeschätzt werden. 

                :small[Quelle: Forschungsstelle für Energiewirtschaft e. V. (FfE), „Dynamische Stromtarife - Tarifarten, Vor- und Nachteile, technische Anforderungen“, FfE, 18. Aug. 2023. [Online]. Verfügbar: https://www.ffe.de/veroeffentlichungen/beitragsreihe-dynamische-stromtarife-tarifarten-vor-und-nachteile-technische-anforderungen/. [Zugriff am: 19. Mai 2025].]

                """)
with st.expander("Wie ist ein dynamischer Stromtarif aufgebaut?"):
    st.markdown("""
                Wie jeder feste Stromtarif auch besteht auch ein dynamischer Stromtarif immer aus einem monatlichen Fixpreis und einem variablen Anteil je kWh elektrischer Energie. Nur der variable Anteil verändert sich dynamisch mit den Schwankungen des Börsenstrompreises. Zu dem variablen Anteil gehören fix die Netzentgelte, Konzessionsabgaben, Stromsteuer, Offshore-Umlage, KWKG-Umlage, NEV-Umlage und ein Energieversorger spezifischer Aufschlag ein. Stündlich, oder viertelstündlich veränderen sich die Energiekosten die dem Börsenstrompreis entsprechen und die Mehrwertsteuer die sich dafür ergibt. Letzteres verstärkt die Schwankungen im Endpreis erheblich. 
                In der Berechnung ist ein dynamischer Stromtarif von Tibber verwendet worden, mit Netzentgelten des Netzbetreibers Westnetz, Stand Januar 2025. Tibber erhob zu dem Zeitpunkt eine monatliche Gebühr von 5,99€ und einen variablen Anteil pro kWh von 2,15 Cent/kWh.
                """)
st.divider()

st.markdown("""##### Was muss ich über steuerbare Verbrauchseinrichtungen wissen?""")
with st.expander("Warum sollen Haushaltsgeräte vom Netzbetreiber aus steuerbar sein?"):
    st.markdown("""
                Durch die voranschreitende Sekorenkopplung, sprich der Versorgung der Sektoren Haushaltswärme und Individualverkehr mit elektrischer Energie, gelangen immer mehr elektrische Verbraucher mit hoher Leistungsaufnahme in die Haushalte, die häufig zu ähnlichen Zeiten verwendet werden. Nicht alle Versorgungsnetze sind gewiss auf die bevorstehenden Lasten ausgelegt und müssen in Zukunft ausgebaut und digitalisiert werden. Daher ist es das Ziel all diese flexiblen Verbraucher mit hoher Leistungsaufnahme vom Netzbetreiber aus steuerbar zu machen. Der Netzbetreiber darf bei einer nachgewiesenen Netzüberlastung die Leistungsaufnahme dieser Geräte reduzieren. Als Entschädigung werden die Netzentgelte für den Endkunden reduziert.
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]""")
with st.expander("Was ist eine steuerbare Verbrauchseinrichtung?"):
    st.markdown("""
                Für die Umsetzung des Ziels ist in dem Energiewirtschaftsgesetz (EnWG) geregelt welche Geräte als eine steuerbare Verbrauchseinrichtung betitelt werden. Dabei handelt es sich um Stromspeicher, Klimageräte, Wärmepumpen und Wallboxen mit einer Netzanschlussleistung größer 4,2 kW die nach dem 01.01.2024 inbetrieb genommen worden sind. Temporär muss sich diese vom Netzbetreiber auf 4,2 kW dimmen lassen können.
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Welchen Nutzen kann ich aus meinen steuerbaren Verbrauchseinrichungen ziehen?"):
    st.markdown("""
                Die Entschädigung der Steuerungsmöglichkeit wird in drei frei wählbaren Modulen geregelt. Das erste Modul enthält eine pauschale Entschädigung zwischen 110 und 190 €, je nach Netzbetreiber. Das Modul kann mit dem Modul drei kombiniert werden, diese Module benötigen keine eigene Messung der Energie der steuerbaren Verbrauchseinrichtung. Für das zweite Modul muss die Energie der steuerbaren Verbrauchseinrichtung separat zum Haushaltsstrom gemessen werden. Dafür erhält der der Endkunde auf die von der steuerbaren Verbrauchseinrichtung verbrauchten elektrischen Energie eine prozentuale Netzentgeltreduzierung von 40%. Das dritte Modul, welches nur in Kombination mit Modul 1 gewählt werden kann, beinhaltet zeitvariable Netzentgelte. Dieses Modul ist wählbar seit April 2025. Die Netzbetreiber können selbst ein dreistufigen Netzentgelt Plan bestimmen. Dabei mussen sich in 24 h mindestens einmal ein Hochtarif, Standardtarif und Niedrigtarif wiederholen. 
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]
                
                In der Berechnung wird ein zeitvariables Netzentgelt von dem Verteilnetzbetreiber Westnetz verwendet. Dieser hat ein Niedertarifpreis von 1,19 Cent/kWh, ein Standardtarifpreis von 11,88 Cent/kWh und einen Hochtarifpreis von 17,75 Cent/kWh in 2025. Der festgelegte Zeitplan von Westnetz entspricht zwischen 0 – 6 Uhr den Niedertarif und zwischen 15 – 20 Uhr den Hochtarif. Zu jeder anderen Zeit wird der Standardtarif berechnet. Damit wird die Kombination aus Modul 1 und 3 zu Grunde gelegt.
                
                :small[Quelle: Westnetz GmbH, „Preisblätter Westnetz Strom 2025“, Westnetz GmbH, 2025. [Online]. Verfügbar: https://www.westnetz.de/content/dam/revu-global/westnetz/documents/ueber-westnetz/unser-netz/netzentgelte-strom/preisblaetter-westnetz-strom-01-01-2025.pdf. [Zugriff am: 21. Mai 2025].]
                """)
st.divider()

st.markdown("""##### Was muss ich alles über die EEG-Vergütung wissen?""")
with st.expander("Was ist die Feste Einspeisevergütung für den eingespeiste elektrische Energie aus Erneuerbaren Energieanlagen?"):
    st.markdown("""
                In dem Erneuerbaren Energiengesetz ist die vorranige Abnahme von elektrischer Energie aus Erneuerbaren Energieanlagen geregelt. Ebenfalls ist dort die Einspeisevergütung geregelt, die sich nach Installationsdatum, Leistung der Anlage und Art der Einspeiung (Voll- oder Teileinspeisung ins Netz) bemisst. 
                
                Für Anlagen die älter als 20 Jahre sind erhalten, aktuell bis 2032 so geregelt, weiterhin eine vorranige Abnahme der Energie und eine Einspeisevergütung die sich an den Börsenstrompreis orientiert und Jahresmarktwert Solar heißt. 
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Was ist die Direktvermarktung?"):
    st.markdown("""
                In dem Solarpaket 1 von April 2025, in dem auch die weitere Einspeisevergütung nach 20 Jahren erweitert worden ist, ist auf eine Vereinfachung von der Direktvermarktung von kleinen Anlagen kleiner 25 kWp hingewiesen worden. Diese Art der Vermarktung von eigenerzeugten Energie bringt ähnliche Vorteile für das Energiesystem mit, die bereits für variable Bezugspreise aufgeführt sind. Je nach externem Direktvermarkter kommen unterschiedlich Hohe Dienstleistungsgebühren hinzu, da die elektrische Energie manuell an der Börse gehandelt werden muss. 
                
                In der Berechnung sind Dienstleistungskosten des Energieversorgers Luox Energy des Stands Mai 2025 mit 3% variablen Kosten einberechnet. Zu dem muss eine Gebühr von 200€ einmalig als Einrichtungsgebühr verrichtet werden. (Wieder mit in die Betrachtung, Thomas kontaktieren!)
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Was ist bei einer Kombination aus Batteriespeichern und der PV-Anlage zu berücksichtigen?"):
    st.markdown("""
                Ein weiterer Punkt im EEG ist die Behandlung von Speichern. Dieses Gesetz regelt die Einspeisevergütung der Energie die von der Batterie ins Netz abgegeben werden kann. Das dort definierte Ausschließlichkeitsprinzip, besagt dass der Speicher ausschließlich mit elektrischer Energie aus Erneuerbaren Energieanlagen stammen darf und kein Netzbezug erfolgen darf, auch wenn der zugehörige Stromtarif auf 100% Erneuerbaren Energien ausgelegt ist. 
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                
                Deshalb muss in den folgenden Einstellungen bei einer Batterie und EEG-Vergütung ausgewählt werden ob die Batterie ausschließlich aus dem Netz beziehen darf oder ausschließlich ins Netz mit EEG-Vergütung einspeisen darf. 
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „FAQs zum Solarpaket I“, BMWK, [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/FAQ/Solarpaket/faq-solarpaket.html. [Zugriff am: 21. Mai 2025].]
                
                Um die Batteriespeicher in Haushalten in Zukunft netzdienlich einsetzen zusetzen wird über die Definition des Ausschließlichkeitsprinzips diskutiert. Dies würde zusätzliche Freiheiten in der Nutzung ermöglichen, die in der folgenden Berechnung mit einfließen können. Eine alternative (Worst-Case) Betrachtung für Altanlagen die dem aktuell denklichen netzdienlichen Gedanken verfolgt, also Anlage die bereits 20 Jahre eine Einspeisevergütung gefördert aus dem EEG erhaltben haben, könnte sein zum zeitlich aktuellen Börsenstrompreis einzuspeisen. Diese Betrachtung kann ebenfalls in der Berechnung ausgewählt werden. Diese Betrachtung dient dazu abzuschätzen in wie fern Aufdach PV-Anlagen von Privatbesitzern im Markt stehen und ohne Förderungen auskommen können. (Naja vergleich bezieht sich noch immer auf Einspeisevergütung… nicht abschätzbar grade)
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)

st.divider()
st.markdown("""##### Welche Annahmen trifft die Berechnung und welche Grenzen weißt diese auf?""")
st.markdown("""
            Die Berechnung soll dazu dienen, für sich selbst eine Einschätzung zu bekommen, ob sich ein Wechsel auf einen dynamischen Stromtarif lohnen würde.
            Die Berechnung basiert auf dem Jahresdurchschnittsverbrauch des Haushalts, sowie Optional auf der Erzeugung einer vorhandenen PV-Anlage, die Nutzung einer Batteriekapazität in Kombination mit einem intelligenten Heim-Energiemanagement-System (HEMS) das den Energiefluss intelligent steuern kann. Die Datengrundlage basiert auf dem Jahr 2024. 
            
            Das Ergebnis der Berechnung bezieht sich, bei allen unterschiedlichen Tarifen, immer auf den Vergleich der Eigenverbrauchsoptimierung, sprich einem normalen festen Stromtarif, ggf. einer festen Einspeisevergütung nach dem EEG und ggf. eine Batterie die unter den Bedingungen kostensenkend eingesetzt wird. Der Kosteneffiziente Einsatz der Batterie setzt immer ein Heim-Energiemanagement System (HEMS) voraus. Der Optimierungsalgoritmus bei der Berechnung soll immer die Kosten für den Kunden minimieren. 

            Die hinterlegten Lastverläufe sind durchschnittliche Lastverläufe für den ausgewählten Jahresdurchschnittsverbrauch, auf der Grundlage von typischen Haushaltsverteilungen in Deutschland. Bitte betrachten Sie bei der Auswahl Ihren tatsächlichen Haushaltsverbrauch, falls bereits eine PV-Eigenverbauch stattfindet entspricht dies nicht dem Netzbezug.

            Die Berechnung setzt voraus, dass sich das individuelle Verbrauchsverhalten mit dem Wechsel des Stromtarifs **nicht ändert**. Es erfolgt nur eine **optimierte** Batterienutzung und der PV-Einspeisung. Eine bewusste Verhaltensänderung in Verbindung mit einem dynamischen Stromtarif kann zu einer weiteren Ersparnis führen. Dabei sollte bewusst sein, dass im gleichen Maße ein Verhalten ungünstig zum Börsenstrompreis auch zusätzliche Kosten verursachen. Ebenfalls positiv auf Kosteneinsparungen tragen flexiblen Verbraucher gesteuert über ein HEMS bei, wie zum Beispiel Wärmepumpen und Wallboxen, die ebenfalls nicht in der Berechnung berücksichtigt werden.
            """)
st.divider()
st.markdown("""
                Weitere Informationen zu dem Rechner erhalten Sie auf der Seite Hintergrund Erklärungen, in der Seitenleiste und unterhalb auswählbar. Beachten Sie dass laufende Berechnungen gestoppt werden, wenn die Seite gewechelt wird.
            """)
st.page_link("explain.py", label="Hintergrund Erklärungen")
st.divider()
st.markdown(""" ##### Technischer Hinweis und Haftungsausschluss: """)
           
st.warning("""Die auf dieser Website durchgeführten Berechnungen erfolgen auf Grundlage vereinfachter Modelle, definierter Annahmen sowie idealisierter Randbedingungen. Abweichungen zwischen den berechneten Werten und realen Gegebenheiten sind möglich und systembedingt. Die Ergebnisse dienen ausschließlich der unverbindlichen Orientierung und stellen keine belastbare Planungs- oder Entscheidungsgrundlage dar. Es wird keine Haftung für die Richtigkeit, Vollständigkeit oder Anwendbarkeit der ausgegebenen Ergebnisse übernommen. Die Nutzung erfolgt auf eigenes Risiko.
""")
st.divider()
# -------------------------- Calculation ---------------------------------------

st.divider()
st.markdown("""##### Auf welchen Tarif wollen Sie wechseln?""")
# st.toggle("💡 EEG-Vergütung EIN / Ü20-Anlage AUS", key="has_eeg", help="Erhalten Sie die Einspeisevergütung gefördert vom EEG für eigenproduzierte elektrische Energie die ins Netz eingespeist wird? Oder ist ihre Anlage bereits 20 Jahre lang gefördert worden und erhalten Sie nun den Jahresmittelwert Solar für ihre eingespeiste Energie? ")

# Drei gleich breite Spalten für die Buttons
col1, col2 = st.columns(2)


with col1:
    st.toggle("Dynamischer Stromtarif", key="dyn_cost")


with col2:
    st.toggle("Direktvermarktung", key="direct_market")    

col3, col4 = st.columns(2)

with col3:
    st.toggle("steuerbare Verbrauchseinrichtung", key="controllable_device")  

with col4:
    st.toggle("EEG-Vergütung EIN / Ü20-Anlage AUS", key="has_eeg")  

st.markdown("""##### Lastgangauswahl über dem durchschnittlichen Stromverbrauch eines Jahres""", help="Bitte wählen Sie ihren jährlichen Haushaltsstromverbrauch aus. Der selbstverbrauchte Photovoltaikstrom und die Batterieladung wird seperat betrachtet.")
st.slider("Jährlicher Stromverbrauch (kWh)", 1000, 8000, key="consumption", step=1000, help="Bitte wählen Sie ihren jährlichen Haushaltsstromverbrauch aus. Der selbstverbrauchte Photovoltaikstrom und die Batterieladung wird seperat betrachtet.") #, disabled=st.session_state.get("calculating"))

# Steuerbare Verbrauchseinrichtung
# st.markdown("""##### Steuerbare Verbrauchseinrichtung nach EnWG 14a""", help=
#         """Darunter fallen alle steuerbaren Verbraucher, Wallboxen, Batteriespeicher, Wärmepumpen und Klimageräte, ab einer Leistung von 4,2 kW die nach dem 01.01.2024 installiert worden sind.
#         Seit dem 01.04.2025 besteht die Möglichkeit zusätzlich zum Modul 1 das Modul 3 zu wählen, welches zeitvariable Netzentgelte ermöglicht.
#         \n **Bei Wahl der folgenden Einstellung wird die Berechnung mit zeitvariablen Netzentgelten vorgenommen.**""")
# with st.expander("Informationen: Haben Sie eine steuerbare Verbrauchseinrichtungen nach dem §14a im Energiewirtschaftsgesetzes? "):
#     st.info("""
#         Darunter fallen alle steuerbaren Verbraucher, Wallboxen, Batteriespeicher, Wärmepumpen und Klimageräte, ab einer Leistung von 4,2 kW die nach dem 01.01.2024 installiert worden sind.
#         Seit dem 01.04.2025 besteht die Möglichkeit zusätzlich zum Modul 1 das Modul 3 zu wählen, welches zeitvariable Netzentgelte ermöglicht.
#         \n **Bei Wahl der folgenden Einstellung wird die Berechnung mit zeitvariablen Netzentgelten vorgenommen.**""")
# st.checkbox("Berechnung mit zeitvariablen Netzentgelten nach EnWG 14a Modul 3", key="controllable_device") #, disabled=disable_settings)
# Statischer Stromtarif nur mit zeitvariablen Netzentgelten
# with st.expander("Informationen: Möchten Sie eine Berechnung durchführen nur mit zeitvariablen Netzentgelten mit dem normalen statischen Stromtarif? "):
#     st.info("""Wählen Sie die Folgende Möglichkeit aus wenn sie keinen dynamischen Stromtarif berechnen wollen, aber die zeitvariablen Netzentgelte ihrer steuerbaren Verbrauchseinrichtung mit dem normalen Stromtarif kombinieren wollen. 
#             """)
# if st.session_state.get("controllable_device", False): 
#     st.checkbox("Zeitvariable Netzentgelte mit normalen Stromtarif", key="static_ZVNE", help="""Wählen Sie die Folgende Möglichkeit aus wenn sie keinen dynamischen Stromtarif berechnen wollen, aber die zeitvariablen Netzentgelte ihrer steuerbaren Verbrauchseinrichtung mit dem normalen Stromtarif kombinieren wollen. """) #, disabled=st.session_state.get("calculating", False))


# PV-Anlage
st.markdown("""##### Angaben zur installierten Photovoltaik Anlage""", help="Wenn Sie eine PV-Anlage besitzen die in der Teileinspeisung läuft, sprich die erzeugte Energie im Haushalt genutzt werden kann, geben Sie bitte die Peak-Leistung Ihrer Anlage an die Ausrichtung der Module.")
# with st.expander("Informationen: Besitzen Sie eine PV-Anlage?"):
#     st.info("""Wenn Sie eine PV-Anlage besitzen die in der Teileinspeisung läuft, sprich die erzeugte Energie im Haushalt genutzt werden kann, geben Sie bitte die Peak-Leistung Ihrer Anlage an die Ausrichtung der Module.
#         """)            
st.checkbox("Ich besitze eine PV-Anlage.", key="has_pv") #, disabled=st.session_state.get("calculating", False))
if st.session_state.get("has_pv", False):
    st.slider("Installierte PV-Leistung (kWp)", 1, 25, step=1, key="pv_power") #, disabled=st.session_state.get("calculating", False))
    direction_map = { "Nord": 0, 'Nord-Ost': 45, "Ost": 90, 'Süd-Ost': 135, "Süd": 180, "Süd-West": 225,  "West": 270}
    if "pv_compass" not in st.session_state:
        st.session_state.pv_compass = "Süd"
    st.selectbox("Ausrichtung der PV-Anlage", list(direction_map.keys()), key="pv_compass") #, disabled=st.session_state.get("calculating", False))
    st.session_state.pv_direction = direction_map[st.session_state.pv_compass]
    # with st.expander("Informationen: Bekommen Sie auf die eingespeiste Energie ins Netz eine Einspeisevergütung die aus dem EEG gefördert ist?"):
    #     st.info("""Wenn Sie eine feste Einspeisevergütung über 20 Jahre gefördert aus dem Erneuerbaren Energiengesetz (EEG) erhalten, geben Sie bitte das Installationsdatum Ihrer PV-Anlage an.
    #         Wichtig ist die passende Angabe von Jahr und Monat des Installationsdatums. 
    #     """)            
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
st.markdown("""##### Angaben zum Batteriespeicher""", help="Wenn Sie einen Batteriespeicher in Kombination mit Ihrer Photovoltaikanlage haben geben Sie bitte die Kapazität des Batteriespeichers an. Eine Angabe auch ohne PV-Anlage ist zulässig. Sollten Sie eine aus dem EEG geförderte Anlage besitzen, können Sie für den Batteriespeicher angegeben haben ob dieser nur Energie ans Netz abgeben oder aufnehmen darf. Eine Anlage die keine Förderung erhält, kann gegebenfalls beliebig Energie aus dem Netz in die Batterie speichern und auch ans Netz abgeben.")
# with st.expander("Informationen: Batteriespeicher"):
#     st.info("""Wenn Sie einen Batteriespeicher in Kombination mit Ihrer Photovoltaikanlage haben geben Sie bitte die Kapazität des Batteriespeichers an. 
#             Eine Angabe auch ohne PV-Anlage ist zulässig.
#             Sollten Sie eine aus dem EEG geförderte Anlage besitzen, können Sie für den Batteriespeicher angegeben haben ob dieser nur Energie ans Netz abgeben oder aufnehmen darf.
#             Eine Anlage die keine Förderung erhält, kann gegebenfalls beliebig Energie aus dem Netz in die Batterie speichern und auch ans Netz abgeben.
#             """)  
st.checkbox("Besitzen Sie einen Batteriespeicher?", key="has_battery") #, disabled=st.session_state.get("calculating", False))

if st.session_state.get("has_battery", False):
    st.slider("Batteriekapazität (kWh)", 1, 20, 5, step=1, key="battery_capacity") #, disabled=st.session_state.get("calculating", False))
    if st.session_state.get("has_eeg", False):
        st.selectbox("Batterieverhalten zum Netz bei EEG-Förderung", ["Energie einspeisen", "Energie aus dem Netz beziehen"], 
                                                    key="battery_usage") #, disabled=st.session_state.get("calculating", False))
else:
    st.session_state.battery_capacity = 0
    st.session_state.is_eeg_battery = 0







# st.markdown("""##### Auf welchen Tarif wollen Sie wechseln?""")


# # Daten für Tarife, mit Tarifnamen als Index
# tarif_data = pd.DataFrame({
#     "Dyn. Stromtarif":          ["✅", "❌", "❌", "✅"],
#     "Direktvermarktung":        ["❌", "✅", "❌", "❌"],
#     "Steuerb. Verbrauchsein.":  ["❌", "❌", "✅", "✅"]
# }, index=[f"Tarif {i+1}" for i in range(4)])

# # Optionen für das Segment-Control = Indexnamen
# tarif_options = tarif_data.index.tolist()

# # Segment Control zur Auswahl
# selected_tarif = st.segmented_control("Wähle deinen Tarif:", options=tarif_options)

# # Sicherstellen, dass Auswahl gültig ist (optional)
# if selected_tarif not in tarif_options:
#     selected_tarif = tarif_options[0]

# # Index ist jetzt der Tarifname direkt
# selected_index = selected_tarif

# # Styling-Funktion für Hervorhebung
# def highlight_selected(row):
#     return ['background-color: lightblue' if row.name == selected_index else '' for _ in row]

# # Tabelle mit Hervorhebung anzeigen
# st.markdown("### Tarifvergleich")
# styled_df = tarif_data.style.apply(highlight_selected, axis=1)
# st.dataframe(styled_df, use_container_width=True)

# # Ausgabe der Auswahl
# st.markdown(f"👉 Du hast **{selected_tarif}** gewählt")

# if selected_tarif == "Tarif 1":
#     st.session_state.static_ZVNE            = False 
#     st.session_state.controllable_device    = False
#     st.session_state.direct_market          = False
#     pass
# elif selected_tarif == "Tarif 2":
#     st.session_state.static_ZVNE            = False 
#     st.session_state.controllable_device    = False
#     st.session_state.direct_market          = True
#     pass
# elif selected_tarif == "Tarif 3":
#     st.session_state.static_ZVNE            = True 
#     st.session_state.controllable_device    = True
#     st.session_state.direct_market          = False
#     pass
# elif selected_tarif == "Tarif 4":
#     st.session_state.static_ZVNE            = False 
#     st.session_state.controllable_device    = True
#     st.session_state.direct_market          = False
#     pass




text_info_optimisation = st.empty()
if st.session_state.static_ZVNE == 1:
    select_opti1 =  control.select_optimisation_behaviour(9)
    text_info_optimisation.info("Die aktuelle Auswahl berechnet die Ersparnis wenn man den normalen Stromtarif mit zeitvariablen Netzentgelten kombiniert, die durch eine **Steuerbare Verbrauchseinrichtung** ermöglicht werden, die nach dem Energiewirtschaftsgesetz §14a als solche definiert ist. ") 
elif st.session_state.direct_market == 1:
    select_opti1 =  control.select_optimisation_behaviour(2)
    text_info_optimisation.info("Die aktuelle Auswahl berechnet die Ersparnis wenn man den normalen Stromtarif mit einer Direktvermarktung der Einspeisung aus der PV-Anlage kombiniert.") 
else:
    if st.session_state.has_eeg:
        select_opti1 =  control.select_optimisation_behaviour(3)
        text_info_optimisation.info("Die aktuelle Auswahl berechnet die Ersparnis bei einem Wechsel auf einen dynamischen Stromtarif, mit einer bestehenden Einspeisevergütung gefördert aus dem EEG.") 
        if st.session_state.controllable_device:
            select_opti1 =  control.select_optimisation_behaviour(10)
            text_info_optimisation.info("Die aktuelle Auswahl berechnet die Ersparnis bei einem Wechsel auf einen dynamischen Stromtarif in Kombination mit zeitvariablen Netzentgelten, mit einer bestehenden Einspeisevergütung gefördert aus dem EEG.") 
    else:
        select_opti1 =  control.select_optimisation_behaviour(8)
        text_info_optimisation.info("Die aktuelle Auswahl berechnet die Ersparnis bei einem Wechsel auf einen dynamischen Stromtarif, die eingespeiste elektrische Energie ins Netz wird mit dem aktuellen Börsenstrompreis vergütet.") 
        if st.session_state.controllable_device:
            select_opti1 =  control.select_optimisation_behaviour(11)
            text_info_optimisation.info("Die aktuelle Auswahl berechnet die Ersparnis bei einem Wechsel auf einen dynamischen Stromtarif in Kombination mit zeitvariablen Netzentgelten, die eingespeiste elektrische Energie ins Netz wird mit dem aktuellen Börsenstrompreis vergütet.") 


st.divider()        
# Berechnung starten
if "results" not in st.session_state:
    st.session_state.results = []


if st.button("Berechnung stoppen"):
    st.session_state.calculating = False
    st.rerun()

if st.button("Berechnung starten", disabled=st.session_state.get("calculating", False)):
    st.session_state.calculating = True

    st.warning("Die Berechnung kann 1 bis 2 Minuten dauern.")
    
    progress_bar_loading = st.progress(0)
    status_text_loading = st.empty()

    progress_bar_Opti1 = st.progress(0)
    status_text_Opti1 = st.empty()

    progress_bar_Opti2 = st.progress(0)
    status_text_Opti2 = st.empty()

    
    
    progress_bar_loading, status_text_loading = progress_update(progress_bar_loading, status_text_loading, 0.05, "Daten einladen")

    # loadprofiles = {2000: 3,  3000: 5,  4000: 12,
    #         5000: 13, 6000: 17, 7000: 15, 8000: 16}
    
    st.session_state.loadprofile = st.session_state.consumption # loadprofiles[st.session_state.consumption]
    #print(f"Lastprofil: {st.session_state.loadprofile}")
    #del(loadprofiles)

    progress_bar_loading, status_text_loading = progress_update(progress_bar_loading, status_text_loading,0.10, "Daten einladen")

    data, averageEnergyHousehold =  control.data_generator.loadData(st.session_state.loadprofile,
                                                                        st.session_state.pv_direction, 
                                                                        st.session_state.pv_power,
                                                                        st.session_state.battery_capacity) 
    
    progress_bar_loading, status_text_loading =  progress_update(progress_bar_loading, status_text_loading, 0.70, "Daten einladen")
    
    data = control.price_generator.calculate_energy_prices( data, averageEnergyHousehold,
                                                                st.session_state.controllable_device)


    progress_bar_loading, status_text_loading =  progress_update(progress_bar_loading, status_text_loading, 1, "Daten einladen")

    progress_bar_Opti1, status_text_Opti1 =  progress_update(progress_bar_Opti1, status_text_Opti1, 0, "Berechnung des ausgewählten Stromtarifs")

    progress_bar_Opti2, status_text_Opti2 =  progress_update(progress_bar_Opti2, status_text_Opti2, 0, "Berechnung des Vergleich-Stromtarifs")
    
    # '''Wenn das True ist, dann wird nur statisch mit Zeitvariablen Netzentgelten gerechnet'''
    # if st.session_state.static_ZVNE == 1:
    #     select_opti1 =  control.select_optimisation_behaviour(9)
    # else:
    #     if st.session_state.has_eeg:
    #         select_opti1 =  control.select_optimisation_behaviour(3)
    #         if st.session_state.controllable_device:
    #             select_opti1 =  control.select_optimisation_behaviour(10)
    #     else:
    #         select_opti1 =  control.select_optimisation_behaviour(8)
    #         if st.session_state.controllable_device:
    #             select_opti1 =  control.select_optimisation_behaviour(11)


    month_pv_installation = st.session_state.installation_date.month
    year_pv_installation  = st.session_state.installation_date.year
    static_feed_in_price,  static_bonus_feed_in =  control.get_eeg_prices(year_pv_installation,month_pv_installation)

    battery_power = st.session_state.battery_capacity *  control.min_data/60 

    input_optimisation =    [ control.optimise_time,  control.step_time, st.session_state.battery_capacity,
                                 control.battery_costs,  battery_power, 
                                 control.grid_power,  static_feed_in_price,  static_bonus_feed_in]
    battery_usage = st.session_state.battery_usage

    select_opti2 =  control.select_optimisation_behaviour(1)

    queue = multiprocessing.Queue()

    # Prozesse starten
    process_1 = multiprocessing.Process(target= control.opimisation.select_optimisation, args=( data, input_optimisation, select_opti1, battery_usage, queue, 1))
    process_2 = multiprocessing.Process(target= control.opimisation.select_optimisation, args=( data, input_optimisation, select_opti2, battery_usage, queue, 2))

    process_1.start()
    process_2.start()

    
    while process_1.is_alive() or process_2.is_alive():
        while not queue.empty():
            task_id, progress = queue.get()
            if task_id == 1:
                progress_bar_Opti1, status_text_Opti1 =  progress_update(progress_bar_Opti1, status_text_Opti1, progress, "Berechnung des ausgewählten Stromtarifs")
            elif task_id == 2:
                progress_bar_Opti2, status_text_Opti2 =  progress_update(progress_bar_Opti2, status_text_Opti2, progress, "Berechnung des Vergleich-Stromtarifs")
            elif task_id == f"Result 1:":
                result1 = progress 
                print("Result 1 stored.")
            elif task_id == f"Result 2:":
                result2 = progress 
                print("Result 2 stored.")
    
    # Wait for processes to finish
    process_1.join()
    process_2.join()

    costs_selected =  control.analysis.single_cost_batterycycle_calculation(result1, select_opti1)
    costs_evo      =  control.analysis.single_cost_batterycycle_calculation(result2, select_opti2)

    benefit = costs_evo['2024-12-31'] - costs_selected['2024-12-31']
    # st.write(f"{benefit} = {costs_evo['2024-12-31']} - {costs_selected['2024-12-31']}")
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
st.markdown("""Die Ergbenisse der Berechnungen geben die Kosteneinsparung an, die angefallen wären, hätte man im Jahr 2024 den Stromtarif gewechselt. Ist das Ergebnis negativ, wären höhere Kosten angefallen bei einem Wechsel gegenüber dem festen Stromtarif in Kombination mit der festen EEG-Vergütung für die ins Netz eingespeiste Energie. """)
for i, res in enumerate(st.session_state.results, start=1):
    st.write(f"{i}. Ergebnis: {selected_tarif} -> {round(res,2)} Euro Ersparnis")
