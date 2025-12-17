import streamlit as st



st.title("🔌 Einschätzung zum Wechsel auf einen dynamischen Stromtarif")
st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """)
st.markdown(""":blue[Fragen und Anregungen gerne an l.weghake@gmail.com]""")
st.markdown("Auf dieser Seite werden alle Einstellmöglichkeiten sowie die Annahmen des Rechners erklärt. " \
            "Des Weiteren sind auf dieser Seite der Optimierungsprozess und die Interpretation des Ergebnisses erklärt.")


with st.container(border=True):
    st.markdown("### Inhaltsverzeichnis")
    st.markdown(
        """
        - [Voraussetzungen für den Wechsel auf einen dynamischen Tarif](#voraussetzungen)
        - [Annahmen und Erklärung der Berechnung](#annahmen)
        """,
        unsafe_allow_html=True
    )


# st.markdown("""Seit dem Jahresanfang 2025 werden vermehrt Smart-Meter-Gateways (SMGW) in Haushaltszählerschränken verbaut.
#             Diese ermöglichen dem Haushalt ein Wechsel auf zeitlich variable Stromtarife, die sich sowohl an Schwankungen 
#             des Börsenstrompreises für elektrische Energie orientieren können, wie auch an zeitvariablen Netzentgelten.
#             Im Folgenden werden zunächst die unterschiedlichen Stromtarif-Modelle aufgeführt sowie Hintergrundinformationen 
#             zu dem Wechsel. Bitte lesen Sie sich die folgenden Themenbereiche durch, da diese entscheidend für das Verständnis der Berechnung sind.
#             Anschließend ist ein Rechner aufgeführt, der unter Angabe von den eigenen Haushaltsstrukturen eine 
#             Abschätzung bietet, ob sich unter den aktuellen Strukturen sich ein Wechsel lohnen kann.
#             Auf der Seite Hintergrund Erklärungen sind Annahmen aufgeführt, die Grundlage der Berechnungsmöglichkeit 
#             sind und dort befinden sich ebenfalls Informationen zu den verwendeten Daten der Berechnung.
#             """)

st.markdown('<a id="voraussetzungen"></a>', unsafe_allow_html=True)
st.divider()

st.markdown("## Voraussetzungen für den Wechsel auf einen dynamischen Tarif")

st.markdown("""##### Sie haben einen Smart-Meter-Gateway (SMGW) eingebaut bekommen oder interessieren sich dafür?""")
with st.expander("Was ist ein Smart-Meter-Gateway und welche Funktionen bietet es?"):
    st.markdown("""
                Ein Smart-Meter-Gateway (SMGW) gehört zur Messtechnik, die vom Messstellenbetrieb eingebaut wird. 
                Dies ist ein Bauteil, was zusätzlich zum häufig genannten \"Stromzähler\" eingebaut wird. 
                Das SMGW ist eine Kommunikationseinheit, die zum intelligenten Messsystem (iMSys) gehört, 
                welches aus einer modernen Messeinrichtung (einem digitalen Zähler) und einem SMGW besteht.
                Diese Kommunikationseinheit empfängt Zählerdaten vom digitalen Zähler, speichert diese und 
                kann zum Beispiel mit dem Energieversorger bezüglich der Abrechnung oder auch mit dem Netzbetreiber 
                bezüglich Steuersignalen kommunizieren. Damit stellt der Besitz des SMGWs die Voraussetzung für eine 
                dynamische Abrechnung dar.
                Des Weiteren bietet es auch einen Kommunikationsweg zum Haushaltsendkunden und dessen 
                kommunikationsfähigen Geräte. Letzteres kann über eine Steuerbox realisiert werden.
                
                
                :small[Quelle: Bundesnetzagentur, „Intelligente Messsysteme und moderne Messeinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/Metering/start.html. [Zugriff am: 19. Mai 2025].]""")

with st.expander("Wer bekommt ein Smart-Meter-Gateway eingebaut?"):
    st.markdown("""
                Der Rollout von SMGWs ist mit einer Gesetzesnovelle im Mai 2023 beschleunigt worden. 
                Seit 2025 beginnt der Pflichteinbau von SMGWs für Haushalte mit einem Jahresdurchschnittsverbrauch 
                zwischen 6000 kWh und 100.000 kWh mit einer Erzeugerleistung zwischen 7 kWp und 100 kWp, oder die 
                im Besitz einer steuerbaren Verbrauchseinrichtung nach Energiewirtschaftsgesetz (EnWG) §14a sind. 
                Das Thema steuerbare Verbrauchseinrichtungen wird im Folgenden nochmal genauer erklärt.
                Ab 2028 beginnt ein weiter Pflichtrollout für Verbraucher über den zuvor genannten Energie und 
                Leistungsmengen. Optional werden die übrigen Verbraucher ausgestattet. Ein SMGW kann auch auf 
                Anfrage des Endkunden unabhängig des Pflichtrollouts eingebaut werden, allerdings kann dies 
                höhere Kosten für den Endkunden verursachen.  Die Kosten des Pflichtrollouts sind gesetzlich 
                gedeckelt auf rund 70€ - 100€ jährlich für digitalen Zähler und SMGW. Die Einbauten neben dem 
                Pflichtrollout können zusätzlich einmalige Kosten im 3-stelligen Bereich mit sich bringen. 
                Der Einbau wird direkt vom Messstellenbetreiber geregelt.

                :small[Quelle: Haufe Online Redaktion, „Smart-Meter-Rollout: Das ist seit dem 1. Januar Pflicht“
                , Haufe.de, 2. Jan. 2025. [Online]. Verfügbar: https://www.haufe.de/immobilien/wirtschaft-politik/smart-meter-rollout_84342_638840.html. 
                [Zugriff am: 25. Mai 2025].""")
    
with st.expander("Warum muss ich ein Smart-Meter-Gateway bei mir einbauen lassen?"):
    st.markdown("""
                Der Einbau von SMGW in Haushalten ist essenziell wichtig, um die elektrische Energieversorgung 
                klimafreundlicher und zukunftssicher zu gestalten.
                Primär bieten die Daten, die das SMGW an die Netzbetreiber bzw. Energieversorger sendet mehr 
                Transparenz wie der Zustand der Netze und der Hausverbrauch wirklich aussieht. Die Netzbetreiber 
                können aus den Daten ermitteln, ob es zu Überlastungen der Betriebsmittel des Netzes kommen kann 
                und die Energieversorger können mit den Daten aus Verbrauchs- und Erzeugeranlagen besser den 
                Haushalten die Energie vorhalten, die sie wirklich benötigen.
                Ebenfalls können durch die Möglichkeit der zeitgenauen Abrechnung Anreize zur Lastverschiebung 
                gesetzt werden, die wiederum den Anteil der elektrischen Energie aus 
                erneuerbaren Erzeugeranlagen verbessern können.
                Ebenso wichtig zur Erhaltung der Zuverlässigkeit der Energieversorgung ist die 
                Steuerbarkeit von Erzeugeranlagen und großen Verbrauchseinrichtungen, sollte sich das Netz in einem kritischen Zustand befinden.

                :small[Quelle: Bundesnetzagentur, „Intelligente Messsysteme und moderne Messeinrichtungen“, 
                Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/Metering/start.html. [Zugriff am: 19. Mai 2025].]""")

st.divider()
st.markdown("""##### Was sind Dynamische Stromtarife?""")
with st.expander("Welche Arten von dynamischen Stromtarifen gibt es?"):
    st.markdown("""
                Neben den festen Stromtarifen können Energieversorger auch zeitlich flexible Stromtarife anbieten. 
                Diese können sich an unterschiedlichen Modellen orientieren. Alle Stromtarife basieren mehr 
                oder weniger dynamisch auf die Schwankungen des Börsenstrompreises. Zum einen können sich 
                Tarife zu festen Tageszeiten auf festgelegte Preise verändern, wie beispielsweise 
                Nachtstromtarife. Andere wiederum sind direkt mit dem Börsenstrompreis gekoppelt 
                und passen sich an den durchschnittlichen Preis beispielsweise monatlich oder täglich an. 
                Die im Folgenden diskutierten dynamischen Stromtarife passen sich auf die in Echtzeit 
                gehandelten Börsenstrompreise an. Die Börsenstrompreise werden in stündlichen bzw. 
                viertelstündlichen Auktionen gehandelt. Aktuell sind in der folgenden Berechnung 
                für die dynamischen Stromtarife die stündlich gehandelte Day-Ahead Auktion der 
                europäischen Strombörse EPEX Spot hinterlegt. Die Daten sind bezogen worden von 
                der Website Energy Charts https://energy-charts.info/ am 23.01.2025. 
                Da mit einem dynamischen Stromtarif ein Anreiz zur Lastverschiebung seitens 
                des Endkunden geschaffen wird, muss seit 2025 jeder Energieversorger einen 
                dynamischen Stromtarif anbieten. Ebenfalls können durch die Möglichkeit der 
                zeitgenauen Abrechnung Anreize zur Lastverschiebung gesetzt werden, die wiederum 
                den Anteil der elektrischen Energie aus erneuerbaren Erzeugeranlagen verbessern können.
                Ebenso wichtig zur Erhaltung der Zuverlässigkeit ist die Steuerbarkeit von 
                Erzeugeranlagen und großen Verbrauchseinrichtungen, 
                sollte sich das Netz in einem kritischen Zustand befinden.

                :small[Quelle: Forschungsstelle für Energiewirtschaft e. V. (FfE), 
                „Dynamische Stromtarife - Tarifarten, Vor- und Nachteile, technische Anforderungen“, 
                FfE, 18. Aug. 2023. [Online]. Verfügbar: https://www.ffe.de/veroeffentlichungen/beitragsreihe-dynamische-stromtarife-tarifarten-vor-und-nachteile-technische-anforderungen/. [Zugriff am: 19. Mai 2025].]
                """)

with st.expander("Welchen Nutzen erfüllen dynamische Stromtarife?"):
    st.markdown("""
                Da dynamische Stromtarife auf den Börsenstrompreisen basieren, spiegeln diese 
                das Gleichgewicht aus Erzeugung und Verbrauch von elektrischer Energie im System wider. 
                Dies hat den Effekt, einen monetären Anreiz für den Kunden zu bilden, wenn mehr 
                Erzeugung aus erneuerbaren Energien vorhanden ist als von den Verbrauchern abgenommen wird.
                Eine Verschiebung von Lasten in Zeiten niedriger Börsenstrompreise fördert die 
                Integrität erneuerbaren Energien, spart CO2 Emissionen der Kraftwerke, die zum 
                regulären Zeitpunkt die Energie bereitgestellt hätten. Ebenso sinkt die Auslastung der 
                Netz-Betriebsmittel in Zeiten hoher Nachfrage und so können Netzausbaumaßnahmen 
                auf das Nötigste reduziert werden.

                Ein Wechsel auf einen dynamischen Stromtarif in Kombination mit Verbrauchsspitzen 
                in den preislich hohen Zeitpunkten kann gleichermaßen einen Kostennachteil für den Endkunden bedeuten.

                Da diese individuelle Lastverschiebung nur schwer akkurat zu simulieren ist, 
                geht die Berechnung vom Fall aus, dass der Endkunde sein Verhalten mit dem Wechsel 
                auf einen dynamischen Stromtarif nicht verändert. Die monetären Vorteile durch eine 
                Lastverschiebung können nach eigenem Interesse individuell abgeschätzt werden.

                :small[Quelle: Forschungsstelle für Energiewirtschaft e. V. (FfE), 
                „Dynamische Stromtarife - Tarifarten, Vor- und Nachteile, technische Anforderungen“, FfE, 18. Aug. 2023. [Online]. 
                Verfügbar: https://www.ffe.de/veroeffentlichungen/beitragsreihe-dynamische-stromtarife-tarifarten-vor-und-nachteile-technische-anforderungen/. 
                [Zugriff am: 19. Mai 2025].]

                """)
with st.expander("Wie ist ein dynamischer Stromtarif aufgebaut?"):
    st.markdown("""
                Wie jeder feste Stromtarif auch besteht auch ein dynamischer Stromtarif immer aus 
                einem monatlichen Fixpreis und einem variablen Anteil je kWh elektrischer Energie.
                 Nur der variable Anteil verändert sich dynamisch mit den Schwankungen des Börsenstrompreises. 
                Zu dem variablen Anteil gehören fix die Netzentgelte, Konzessionsabgaben, Stromsteuer, 
                Offshore-Umlage, KWKG-Umlage, NEV-Umlage und ein Energieversorger spezifischer Aufschlag ein. 
                Stündlich oder viertelstündlich verändern sich die Energiekosten, die dem Börsenstrompreis 
                entsprechen und die Mehrwertsteuer, die sich dafür ergibt. Letzteres verstärkt die Schwankungen im Endpreis erheblich.
                In der Berechnung ist ein dynamischer Stromtarif von Tibber verwendet worden Stand Januar 2025. Tibber erhob 
                zu dem Zeitpunkt eine monatliche Gebühr von 5,99 € und einen variablen Anteil pro kWh von 2,15 Cent/kWh.
                """)
st.divider()

st.markdown("""##### Was muss ich über steuerbare Verbrauchseinrichtungen wissen?""")
with st.expander("Warum sollen Haushaltsgeräte vom Netzbetreiber aus steuerbar sein?"):
    st.markdown("""
                Durch die voranschreitende Sektorenkopplung, sprich der Versorgung der Sektoren 
                Haushaltswärme und Individualverkehr mit elektrischer Energie, gelangen immer mehr 
                elektrische Verbraucher mit hoher Leistungsaufnahme in die Haushalte, die häufig zu 
                ähnlichen Zeiten verwendet werden. Nicht alle Versorgungsnetze sind gewiss auf die 
                bevorstehenden Lasten ausgelegt und müssen in Zukunft ausgebaut und digitalisiert werden. 
                Daher ist es das Ziel, all diese flexiblen Verbraucher mit hoher Leistungsaufnahme vom 
                Netzbetreiber aus steuerbar zu machen. Der Netzbetreiber darf bei einer nachgewiesenen 
                Netzüberlastung die Leistungsaufnahme dieser Geräte reduzieren. Als Entschädigung für 
                die Steurungsmöglichkeit werden die Netzentgelte für den Endkunden reduziert und 
                nach einer Steuerung ist der Netzbetreiber verpflichtet sein Netz auszubauen.
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, 
                Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]""")
with st.expander("Was ist eine steuerbare Verbrauchseinrichtung?"):
    st.markdown("""
                Für die Umsetzung des Ziels ist in dem Energiewirtschaftsgesetz (EnWG) geregelt, 
                welche Geräte als eine steuerbare Verbrauchseinrichtung betitelt werden. 
                Dabei handelt es sich um Stromspeicher, Klimageräte, Wärmepumpen und Wallboxen mit einer 
                Netzanschlussleistung größer 4,2 kW, die nach dem 01.01.2024 in Betrieb genommen worden sind. 
                Temporär muss sich diese vom Netzbetreiber auf 4,2 kW dimmen lassen können.
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Welchen Nutzen kann ich aus meinen steuerbaren Verbrauchseinrichungen ziehen?"):
    st.markdown("""
                Die Entschädigung der Steuerungsmöglichkeit wird in drei frei wählbaren Modulen geregelt. 
                Das erste Modul enthält eine pauschale Entschädigung zwischen 110 und 190 €, je nach Netzbetreiber. 
                Das Modul kann mit dem Modul drei kombiniert werden, diese Module benötigen keine eigene Messung 
                der Energie der steuerbaren Verbrauchseinrichtung. Für das zweite Modul muss die Energie der 
                steuerbaren Verbrauchseinrichtung separat zum Haushaltsstrom gemessen werden. Dafür erhält der 
                Endkunde auf die von der steuerbaren Verbrauchseinrichtung verbrauchten elektrischen Energie 
                eine prozentuale Netzentgeltreduzierung von 40%. Das dritte Modul, welches nur in Kombination 
                mit Modul 1 gewählt werden kann, beinhaltet zeitvariable Netzentgelte. Dieses Modul ist wählbar 
                seit April 2025. Die Netzbetreiber können selbst ein dreistufigen Netzentgeltplan bestimmen. 
                Dabei müssen sich in 24 h mindestens einmal ein Hochtarif, Standardtarif und Niedrigtarif wiederholen.
                
                :small[Quelle: Bundesnetzagentur, „Integration von steuerbaren Verbrauchseinrichtungen“, Bundesnetzagentur, [Online]. Verfügbar: https://www.bundesnetzagentur.de/DE/Vportal/Energie/SteuerbareVBE/artikel.html. [Zugriff am: 21. Mai 2025].]
                
                """)
st.divider()

st.markdown("""##### Was muss ich alles über die EEG-Vergütung wissen?""")
with st.expander("Was ist die Feste Einspeisevergütung für den eingespeiste elektrische Energie aus Erneuerbaren Energieanlagen?"):
    st.markdown("""
                In dem Erneuerbaren-Energien-Gesetz ist die vorrangige Abnahme von elektrischer Energie aus 
                erneuerbaren Energieanlagen geregelt. Ebenfalls ist dort die Einspeisevergütung geregelt, 
                die sich nach Installationsdatum, Leistung der Anlage und Art der Einspeisung (Voll- oder 
                Teileinspeisung ins Netz) bemisst.

                Für Anlagen, die älter als 20 Jahre sind, erhalten aktuell bis 2032 so geregelt weiterhin 
                eine vorrangige Abnahme der Energie und eine Einspeisevergütung, die sich an den 
                Börsenstrompreis orientiert und Jahresmarktwert Solar heißt.
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Was ist die Direktvermarktung?"):
    st.markdown("""
                 Bei der Direktvermarktung wird 
                die eingespeiste Energie der PV-Anlage direkt von einem Dienstleister an der 
                Strombörse verkauft. Eine Förderung wird dabei mit der so genannten Marktprämie umgesetzt, 
                die auf den Börsenstrompreis hinzugerechnet wird und sicherstellt dass förderfähige 
                Anlagen Erlöse im Bereich der festen Einspeisevergütung erhalten. Diese Art der Vermarktung 
                von eigenerzeugten Energie bringt ähnliche Vorteile für das Energiesystem mit, die bereits 
                für variable Bezugspreise aufgeführt sind. Je nach externem Direktvermarkter kommen
                 unterschiedlich hohe Dienstleistungsgebühren hinzu, da die elektrische Energie manuell 
                an der Börse gehandelt werden muss. 

                In der Berechnung sind Dienstleistungskosten des Energieversorgers Luox Energy 
                (Stand Mai 2025) mit 3% variablen Kosten und einem Fixen Anteil in Abhängigkeit 
                der Größe der PV-Anlage zwischen 74€ und 130€ pro Jahr eingerechnet. 
                Zu dem muss eine Gebühr von 200€ einmalig als Einrichtungsgebühr verrichtet werden.
                
                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                """)
with st.expander("Was ist bei einer Kombination aus Batteriespeichern und der PV-Anlage zu berücksichtigen?"):
    st.markdown("""
                Ein weiterer Punkt im EEG ist die Behandlung von Speichern. Dieses Gesetz regelt 
                die Einspeisevergütung der Energie, die von der Batterie ins Netz abgegeben werden 
                kann. Das dort definierte Ausschließlichkeitsprinzip besagt, dass die Batterien ausschließlich 
                aus dem Netz beziehen, oder ausschließlich ins Netz mit EEG-Vergütung einspeisen dürfen.
                Damit soll vermieden werden, dass Energie die aus dem Netz bezogen und 
                gespeichert worden ist, zu höhen Einspeisevergütungen ins Netz zurückgespeist wird.

                :small[Quelle: Bundesministerium für Wirtschaft und Klimaschutz (BMWK), „Das Solarpaket I im Überblick“, BMWK, 26. Apr. 2024. [Online]. Verfügbar: https://www.bmwk.de/Redaktion/DE/Downloads/S-T/solarpaket-im-ueberblick.pdf?__blob=publicationFile&v=14. [Zugriff am: 21. Mai 2025].]
                
                Aktuell kann ein freies Verhalten von Einspeisung und Netzbezug der Batterien nur 
                in Kombination der Direktvermarktung ohne Marktprämie genutzt werden. 
                Damit in Zukunft die Batterien mehr Spielraum haben auf die Anreize des Strommarkts 
                zu reagieren, soll in Zukunft das Ausschließlichkeitsprinzip für die förderfähige 
                Direktvermarktung angepasst werden. 
                
                """)
                
st.markdown('<a id="annahmen"></a>', unsafe_allow_html=True)
st.divider()

st.markdown("## Annahmen und Erklärung der Berechnung")
st.markdown("""##### Welche Annahmen trifft die Berechnung und welche Grenzen weißt diese auf?""")
st.markdown("""
            Die Berechnung soll dazu dienen, für sich selbst eine Einschätzung zu bekommen, 
            ob sich ein Wechsel auf einen dynamischen Stromtarif lohnen würde.
            Die Berechnung basiert auf dem Jahresdurchschnittsverbrauch des Haushalts sowie 
            optional auf der Erzeugung einer vorhandenen PV-Anlage, die Nutzung einer 
            Batteriekapazität in Kombination mit einem intelligenten Heim-Energiemanagement-System (HEMS), 
            das den Energiefluss intelligent steuern kann. Die Datengrundlage basiert auf dem Jahr 2024.
            
            Das Ergebnis der Berechnung bezieht sich bei allen unterschiedlichen Tarifen immer auf den
            Vergleich der Eigenverbrauchsoptimierung, sprich einem festen Stromtarif, ggf. 
            einer festen Einspeisevergütung nach dem EEG und ggf. einer Batterie, die unter den 
            Bedingungen kostensenkend eingesetzt wird. Der kosteneffiziente Einsatz der Batterie 
            setzt immer ein Heim-Energiemanagement System (HEMS) voraus. 

            Die hinterlegten Lastverläufe sind synthetische Lastverläufe für den 
            ausgewählten Jahresdurchschnittsverbrauch. Bitte betrachten Sie bei der Auswahl 
            Ihren tatsächlichen Haushaltsverbrauch, falls bereits ein PV-Eigenverbauch stattfindet, 
            entspricht dies nicht dem Netzbezug.

            Die Berechnung setzt voraus, dass sich das individuelle Verbrauchsverhalten 
            mit dem Wechsel des Stromtarifs **nicht ändert**. Es erfolgt nur eine **optimierte** 
            Batterienutzung und der PV-Einspeisung. Eine bewusste Verhaltensänderung in Verbindung 
            mit einem dynamischen Stromtarif kann zu einer weiteren Ersparnis führen. Dabei sollte 
            bewusst sein, dass im gleichen Maße ein Verhalten ungünstig zum Börsenstrompreis auch 
            zusätzliche Kosten verursachen. Ebenfalls positiv auf Kosteneinsparungen tragen flexiblen 
            Verbraucher gesteuert über ein HEMS bei, wie zum Beispiel Wärmepumpen und Wallboxen, 
            die ebenfalls nicht in der Berechnung berücksichtigt werden.
            """)
st.divider()



st.header("📊 Erklärungen zu der Datengrundlage der Berechnung")
st.markdown("""Der Großteil der Annahmen und Daten die in der Berechnung verwendet werden sind 
            bereits auf der Seite Berechnung im Vortext beschrieben. Auf dieser Seite befinden 
            sich genaure Informationen zu einzelnen Datensätzen der Berechnung.""")

with st.expander("Lastgänge"):
    st.markdown("""
                Der Lastgang ist der **Rohverbrauch des Haushalts**.
                Die Lastgänge sind generiert mit dem *Load Profile Generator*, https://www.loadprofilegenerator.de/ entwickelt von Noah Pflugradt.
                Die verwendeten representativen Profile für jeden Jahresdurchschnittsverbrauch ist mit diesem Tool erstellt worden.
                """)

with st.expander("Standardlastprofil (SLP)"):
    st.markdown("""
                Das Standardlastprofil (SLP) wird vom Energieversorgungsunternehmen, 
                für jeden Haushalt ohne Lastgangmessung, verwendet und bestimmt die
                Menge der Beschaffung der Energie zu jedem Zeitpunkt im Jahr.
                Damit beeinflusst das SLP den Preis des festen Stromtarifs. 
                Das bisher für Haushalte verwendete Standardlastprofil basiert auf dem Verbrauchsverhalten vor dem Jahr 2000. 
                Im März 2025 sind neue Standardlastprofile des BDEWs veröffentlicht worden und werden in dieser Berechnung 
                bereits genutzt. 
                Diese basieren nicht nur auf den veränderten Verhaltensweisen, sondern auch beziehen die 
                haushalts-individuellen PV-Anlagen und Batteriespeicher mit ein.
                """)

with st.expander("PV-Erzeugung"):
    st.markdown("""
                Die Erzeugung der PV-Anlagen wird basierend auf Wetter- und Geodaten aus NRW (Raum Soest) 
                und den angegebenen Daten aus Leistung und Ausrichtung berechnet. Die Wetterdaten stammen 
                direkt vom Deutschen Wetterdienst aus einer Station in Werl. Diese Daten werden mit einer 
                Python-Bibliothek, der **PV-Lib**-Bibliothek, https://pvlib-python.readthedocs.io, zu einem 
                Erzeugungsprofil der entsprechenden Anlage weiterverarbeitet.    
    """)

    # Noch raussuchen:
    # - Konservativer Jahresdruchschnittsertrag in Südausrichtung von 700–800 kWh/kWp
with st.expander("Einspeisevergütung nach EEG"):
    st.markdown("""
                Die Einspeisevergütung ist seit der ersten EEG-Novelle 2000 festgelegt. Seit 2009 können PV-Anlagen in 
                Teileinspeisung betrieben werden und die selbsterzeugte elektrische Energie 
                kann direkt vom Haushalt verbraucht werden.
                Die feste Einspeisevergütung ist für den Installationszeitraum von Janunar 2009 bis 
                Juli 2025 in der Berechnung hinterlegt.
    """)


with st.expander("Statische und dynamische Tarifoptionen"):
    st.markdown("""
                Die Erklärung wie sich der dynamische Tarif in der Berechnung zusammensetzt ist bereits 
                zuvor erklärt worden. Zusammenfassend besteht dieser aus dem zeitlich 
                variablen Börsenstrompreis mit Steuern, Abgaben und einem Zuschlag des Energieversorgers. 

                Ein fester Stromtarif besteht im Wesentlichen aus den gleichen Komponenten, nur dass in 
                dem Fall der Energieversorger die Energie nach dem Standardlastprofil möglichst kostengünstig 
                beschafft. Im Mittel spiegeln die festen Tarife die Korrelation aus dem SLP und dem Börsenstrompreis wider, 
                eventuell mit etwas Zeitverzögerung da die Energieversorger diese Anpassungen nur träge vornehmen. 
                Für die Berechnung des festen Stromtarifs wird der dynamische Stromtarif mit dem SLP zeitlich übernander gelegt und 
                ein Jahresmittel gebildet .

                Die Fixkosten beider Tarifoptionen sind identisch und werden in der Berechnung vernachlässigt, 
                da das Ergebnis die Differenzkosten beschreibt. 

                Die zeitvariablen Netzentgelte und standard Netzentgelte für die auswählbaren Netzbetreiber sind den 
                Preisblättern von 2025 des jeweiligen Netzbetreibers entnommen worden. Zufinden sind diese unter
                dem Stichpunkt Modul 3 nach § 14a EnWG. 
                """)


st.header("⚙️ Optimierungen")
st.markdown("""
            Für die Erzeugung des Lastgangs je nach Stromtarif wird ein lineares Optimierungsverfahren angewendet, 
            welches die Kosten für den Endkunden minimiert. Dafür ist die Python-Bibliothek Scipy mit 
            der Linprog Optimierungsfunktion verwendet worden. In die Kosten-Zielfunktion gehen 
            die Bezugskosten für Energie aus dem Netz, Einspeisevergütung sowie Kosten für 
            die Nutzung der Batterie. Die Kosten für die Nutzung der Batterie ist mit 7 Cent/kWh angenommen. 
            Optimiert werden die Be- und Entladung der Batterie, der Netzbezug und die Einspeiseleistung. 
            In die Nebenbedingungen der Optimierung geht das Leistungsgleichgewicht ein, in welchem bereits 
            einen Batteriewirkungsgrad von 96% hinterlegt ist. Des Weiteren sind als Nebenbedingungen das 
            Ausschließlichkeitsprinzip des EEGs und die Berechnung des State of charge (SoC) definiert. 
            In der Limitierung der Zustandsvariablen ist die Netzanschlussleistung auf 22 kW begrenzt. 
            Jeder Optimierungsschritt hat eine Vorhersage über die nächsten 24 Stunden zur Verfügung und 
            wird alle 12 Stunden neu berechnet, über das gesamte Jahr 2024.

            Diese Berechnungen werden gleichzeitig für mehrere Stromtarife (Bezugs- und Einspeisetarife) 
            durchgeführt. Welcher Stromtarif berechnet wird, bestimmen die Angaben über den Haushalt. 
            Die Möglichkeiten der Wahl des Stromtarifs wird von den Tatsachen beeinflusst, ob eine 
            steuerbare Verbrauchseinrichtung, Batteriespeicher und/oder eine PV-Anlage vorhanden sind und ob diese 
            eine geförderte Einspeisevergütung aktuell bekommt.
            """)


    

st.header("📈 Ergebnisse")
st.markdown("""
            Ein Großteil der Informationen zu den Ergebnissen ist bereits auf der Hauptseite der Berechnung
            ganz unten mit aufgelistet. 
            Die angezeigte Ersparnis ergibt sich aus Differenz der Kosten der jeweiligen Tarifoption 
            zu den Kosten mit festen Stromtarifen. Dargestellt wird die Ersparnis bei einem Wechsel des 
            Tarifs über ein ganzes Jahr. Mit einbezogen sind Zusatzkosten der jeweiligen Tarifoption, bspw. 
            die Kosten der Direktvermarktung durch den externen Dienstleister. Unter anderem sind 
            bereits Batteriekosten miteinbezogen. Kosten die bei einem Zähleraustausch auf ein 
            intelligentes Messsystem anfallen sind nicht miteinbezogen, da ein Pflichteinbau stattfinden 
            wird, unabhängig vom Wechsel auf einen dynamischen Tarif. 

            Wenn mehrere Stromtarifarten für den Haushalt zur Wahl stehen, werden 
            die Ergebnisse von der größten zu kleinsten Ersparnis sortiert und in 
            einer Zeile mit der Beschreibung des Stromtarifs aufgelistet.
""")
