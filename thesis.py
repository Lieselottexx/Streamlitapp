import streamlit as st
import os


st.title("Erweiterte Ergebnisse")
st.markdown(""":blue[Entwickelt von Laura Weghake B. Eng.] """)
st.markdown(""":blue[Fragen und Anregungen gerne an l.weghake@gmail.com]""")


st.warning("Auf dieser Seite ist aktuell noch Baustelle!")

path_pictures = r'Bilder' # C:\Users\lwegh\Documents\Study\MasterThesis\Streamlitapp\

st.markdown("""EEG ohne Direktvermarktung """)
"""
Zu sehen: Dynamischer Stromtarif, nur dynamische Netzentgelte und die Kombination aus beiden

Für Batterie 3kWh, PV 5kWp : 
Jahresverbrauchsabhängig: 
Die Ersparnis des dynamischen Stromtarifs steigt leicht mit dem Verbrauch (beisp. 1,5 tkWh: 3,46€; 4,5tkWh: 16,15€: 7,5 tkWh: 23,65€)
Im zeitlichen Verlauf werden die Batterieentladungen in die teuereren Abendstunden verschoben, im Gegensatz zur Eigenverbrauchsoptimierung die möglichst früh die Batterie wieder entlädt. Hohe Ähnlichkeit zur Eigenverbrauchsoptimierung. 
Die Ersparnis der ZVNE steigt erst und fällt dann wieder rapide (Glockenkurve) (beisp. 1,5 tkWh: 8,37€; 4,5tkWh: 31,5€: 7,5 tkWh: 1€)
Die ZVNE verschieben die Entladung der Batterie ebenfalls in die festen teuren Abendstunden, die günstigen Morgenstunden sind so nicht ausnutzbar.
Die Kombination aus beiden zeigt einen hohen Start, steigt weiter und fällt ebenfalls wieder allerdings auf einem hohen niveau bleibend (beisp. 1,5 tkWh:5.35€; 4,5tkWh: 46,2€: 7,5 tkWh: 32,24€)


Für Verbrauch 7000 kWh, PV 5 kWp:
Batteriegrößenabhängig:
Alle drei Tarifkombis scheinen zu steigen und anschließend auf noch einem hohen aber nicht maximalen niveau zu stagnieren
Dynamisch 0 kWh: -35,18€; 3 kWh: 17,46€: 7 kWh: 22,1€;  12 kWh: 20,36€; 20 kWh: 20,36€
ZVNE      0 kWh: -28,55€; 3 kWh:  8,27€: 7 kWh: 10,95€; 12 kWh:  6,69€; 20 kWh:  6,69€
Kombi     0 kWh: -63,73€; 3 kWh: 32,79€: 7 kWh: 44,33€; 12 kWh: 34,6€; 20 kWh: 34,62€

Warum rasten die 0er so aus?
7000 kWh ohne Batterie und PV:
dynamisch -7,29€    scheint mit PV ne Vollkatstrophe zu sein.. aber warum? die günstigen Mittagstarife werden nicht bezogen! der Rest bleibt wie es ist, da ja keine Batterie da ist.
ZVNE     -44,64€    Ohne PV deutlich schlechter geworden... Eventuell hat die PV in den frühen Abendstunden ab und zu noch was von dem teueren Abendtarif weggeknabbert?
Kombi    -51,64€

Bei 4500 kWh ohne Batterie und PV: 
dynamisch  0,75€ 
ZVNE     -13,15€ 
Kombi    -13,91€
-> weniger schlimme Auswirkungen, passt dazu!

Könnte aber auch noch gut ein Fehler drin sein, das wirkt schon sehr heftig, der Preissprung ist aber auch heftig! Deckt sich aber noch gut mit der Graphik!

PV-Größenabhängig:
Bei 4500 kWh und 7kWh Batterie:
Dynamisch 5 kWp:  9,16€: 10 kWp:  7,1€;  15 kWhp: 9,59€
ZVNE      5 kWp: 15,5€;  10 kWp: 16,18€: 15 kWhp: 18,94€
Kombi     5 kWp: 19,27€; 10 kWp: 14,05€: 15 kWhp: 18,63€
-> Alles Relativ gleichbleibend besser, Gleiche Verschiebung gegenüber der Eigenverbrauchsoptimierung möglich mit gleichbleibender Batterie, ZVNE verlässlichere teuere Abendzeiten?. 





"""

# Im Allgemeinen ist zu erkennen, wenn man eine große Batterie besitzt, hier ab rund 7 kWh ist immer eine Ersparnis vohanden, diese Überschreitet allerdings in den seltesten Fällen die 50 € Marke. 
# Trends erkennbar mit größerem Stromverbrauch mehr varianz, mit mehr Batteriekapazität besseres Ergebnis. 
# Kleine PV Anlagen helfen beim Lastverschieben, bei größeren ist die Autakie zu hoch das dort noch viel Lastverschiebung möglich ist, da diese bereits zu EE hochzeiten keinen günstigen Strom beziehen können. 

# Dynamische Stromtarife können sich lohnen wenn ein hoher Stromverbrauch da ist, die PV Autakie noch nicht zu hoch ist und eine Batterie vorhanden ist. 
# Mit Kosten in höhe von rund 50€ jährlich für n Smart meter ist es nicht wirtschaftlich den Smart meter auf Wunsch einzubauen. 

# Nur auf dynamische Netzentgelte, hier gekennzeichnet mit STBVE, umzusteigen kann sich bereits etwas mehr lohnen, für einige Haushalte allerdings auch ein minus Geschäft 

st.image(os.path.join(path_pictures, "Feed_in_battery", "EEG_ohne.png" ))



# -------------------------------------------------------------------------------------------------
st.markdown("""EEG mit Direktvermarktung """)
"""
Batteriegrößenabhängigkeit:
Graphik sagt: allesamt Steigend break even Point ungefähr 7kWh 

Bei Verbrauch 2000 kWh und 10 kWh PV:
Direktvermarktung   0 kWh: -87,30€; 3 kWh: -53,32€; 7 kWh: 38,00€; 12 kwh: 134,87€; 20 kWh: 272,62€;
Direkt + ZVNE       0 kWh: -73,77€; 3 kWh: -39,33€; 7 kWh: 37,78€; 12 kwh: 139,89€; 20 kWh: 277,61€;
Dyn + Direkt        0 kWh: -83,87€; 3 kWh: -44,67€; 7 kWh: 32,84€; 12 kwh: 140,12€; 20 kWh: 277,96€;
Direkt + ZVNE + Dyn 0 kWh: -69,79€; 3 kWh: -32,38€; 7 kWh: 40,95€; 12 kwh: 143,13€; 20 kWh: 280,75€;
-> Wie erwartend sehr nah an einander! Stark steigend. Break even point hierbei unter 7kWh. die Direktvermarktung macht den dicken bonus. bei 10kWp kann natürlich auch einiges an PV Strom von der Batterie aufgenommen werden, ich gehe von aus dass es irgendwann stagniert, vielleicht besser zu sehen bei 3kWp PV. 

Batterie- und Verbrauchs-Abhängigkeit:
Bei Verbrauch 8000 kWh und 10 kWh PV:
Direktvermarktung   0 kWh: -150,83€; 3 kWh: -119,99€; 7 kWh: -89,71€; 12 kwh: -27,79€; 20 kWh: €;
Direkt + ZVNE       0 kWh: -192,76€; 3 kWh: -118,30€; 7 kWh: -72,91€; 12 kwh: -27,27€; 20 kWh: €;
Dyn + Direkt        0 kWh: -160,23€; 3 kWh: -88,36€;  7 kWh: -57,80€; 12 kwh: -5,73€;  20 kWh: €;
Direkt + ZVNE + Dyn 0 kWh: -206,16€; 3 kWh: -88,24€;  7 kWh: -41,50€; 12 kwh: -4,38€;  20 kWh: €;
-> Der Verbrauch bringt mehr Varianz in die Ergebnisse rein. Höherer Verbrauch Break-Even-Point noch nach 12 kWh! Direktvermarktung ohne Batterie macht ja so keinen Sinn!

Mit mehr PV wird alles besser. 

Ohne Batterie und Ohne PV hat die Direktvermarktung ja eh keine Auswirkung drauf. gleiche wie oben!






"""
# Interesannt, Hier sinkt im Allgmeinen das Ergebnis mit dem steigenden Stromverbrauch. Direktvermarktung lehnt daran etwas zu verkaufen und nicht selbst zu nutzen. 
# Ohne PV macht auch keine Diektvermarktung Sinn. Die Ergebnisse bei 0 kWp sind die Anteile der anderen dynamischen Anteile am Tarif, und die richtigkeit ist an dem  vorhandenen Roten balken ohne varianz zu sehen. Die Ausreizer um 0€ bei 0 kWh sind auf die Kombination ohne PV Anlage zurückzuführen. 
# Einen sehr starken Einfluss hat die Batteriekapazität auf die Ersparnis. Unter der 7 kWh Kategorie ist eine Ersparnis höchst unwarscheinlich, da da die Jährlichen Fixkosten für die Direktvermarktung nicht von der Lastverschiebung durch die Batterie wieder reingeholt werden können. Darüber sind bis auf einzelfälle Ersparnisse mit einem Tarifwechsel zu erwarten. Die Einzelfälle werden Kombinationen aus einem hohen Stromverbrauch und einer kleinen PV-Anlage sein, abgeleitet aus den Tendenzen der anderen Kategorien. 
# Im Allgemeinen schneiden die Tarife mit dynamischen Stromtarifen etwas schlechter, und Tarife mit zeitvariablen Netzentgelten etwas besser ab. 

st.image(os.path.join(path_pictures, "Feed_in_battery", "EEG_mit.png" ))


# -------------------------------------------------------------------------------------------------

st.markdown("""Ü20 ohne Direktvermarktung """)
""" 
Extrem Ähnliches Ergebniss zu EEG! Gut die Base, Eigenverbrauchsoptimierung ist ja ebenfalls angepasst. Eventuell mit gleichen Achsenbeschriftungen gucken ob es einen gesamten Trend gibt... EEG eventuell im gesamten etwas besser. 
"""
st.image(os.path.join(path_pictures, "Feed_in_battery", "U20_ohne.png" ))


# -------------------------------------------------------------------------------------------------

st.markdown("""Ü20 mit Direktvermarktung """)
""" 
Beim Jahresverbrauch, auffällig das Grün, Direkt plus ZVNE gleichbleibt aber hoch und Dynamisch, direkt und ZVNE steigen und ebenfalls hoch, blau, dynamisch und direkt sinken und niedriges niveau, rot nur direkt bleibt gleich und hoch. 
Steuerbare Verbrauchseinrichtungen haben einen guten Impact auch in kombination. 
Die Kombi Kleine PV, Großer Verbrauch, und Große Batterie ereicht höchstwerte mit der Kombination aus allen dynamischen Anteilen. Direktverm. und STBVE bieten allerdings die sichersten höchsten Ersparnisse. 
Im Gegensatz zu der EEG Ergebnissen machen hier STBVE einen deutlicheren Vorteil. Im EEG waren ehr die dynamischen als Nachteil aufgefallen, dies kann die STBVE hier wieder mehr rausholen. 
Trotzdem nicht so schlau die miteinander zu vergleichen. 
"""
st.image(os.path.join(path_pictures, "Feed_in_battery", "U20_mit.png" ))


# -------------------------------------------------------------------------------------------------

st.markdown("""only Battery""")
"""
Ganz dicke zu sehen, alle drei dynamischen Anteile machen die größte Ersparnis. Hier mit batteriekosten entscheiden ob es sich lohnt. 
Im Allgemeinen sind die Zeitvariablen Netzentgelte ein vorteil. Bei Batterien über 4,2kwH und wie hier mit Netzbezug ohne hin Möglich, gehen aber auch noch mit Jährlichen Kosten der Steuerbox her, wobei dies bei Wallboxen oder Klimageräten im haushalt ohne hin nicht vermeidbar ist. 
"""
st.image(os.path.join(path_pictures, "Feed_in_battery", "only_battery.png" ))


# -------------------------------------------------------------------------------------------------

st.markdown("""Nur Batterie mit Batterienutzungskosten """)
"""
Unter der Berücksichtigung von den Batteriekosten von 10 Cent/kWh die unteranderem die Anschaffungskosten über die Zyklenlebensdauer abdecken ist die Ersparnis deutlich geringer. Mit großer Batteriekapazität, rund 12 kWh ist es wahrscheinlich das sich eine Batterie lohnt, insbesondere in Kombination mit den dynamischen Netzentgelten. Mit großen Jahresdurchschnitts verbräuchen kann sich ebenfalls ein eisatz lohnen. 
"""
st.image(os.path.join(path_pictures, "Feed_in_battery", "only_battery_battery_costs.png" ))


# -------------------------------------------------------------------------------------------------



