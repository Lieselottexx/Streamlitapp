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
Im Allgemeinen ist zu erkennen, wenn man eine große Batterie besitzt, hier ab rund 7 kWh ist immer eine Ersparnis vohanden, diese Überschreitet allerdings in den seltesten Fällen die 50 € Marke. 
Trends erkennbar mit größerem Stromverbrauch mehr varianz, mit mehr Batteriekapazität besseres Ergebnis. 
Kleine PV Anlagen helfen beim Lastverschieben, bei größeren ist die Autakie zu hoch das dort noch viel Lastverschiebung möglich ist, da diese bereits zu EE hochzeiten keinen günstigen Strom beziehen können. 

Dynamische Stromtarife können sich lohnen wenn ein hoher Stromverbrauch da ist, die PV Autakie noch nicht zu hoch ist und eine Batterie vorhanden ist. 
Mit Kosten in höhe von rund 50€ jährlich für n Smart meter ist es nicht wirtschaftlich den Smart meter auf Wunsch einzubauen. 

Nur auf dynamische Netzentgelte, hier gekennzeichnet mit STBVE, umzusteigen kann sich bereits etwas mehr lohnen, für einige Haushalte allerdings auch ein minus Geschäft 
"""
st.image(os.path.join(path_pictures, "Feed_in_battery", "EEG_ohne.png" ))



# -------------------------------------------------------------------------------------------------
st.markdown("""EEG mit Direktvermarktung """)
"""
Interesannt, Hier sinkt im Allgmeinen das Ergebnis mit dem steigenden Stromverbrauch. Direktvermarktung lehnt daran etwas zu verkaufen und nicht selbst zu nutzen. 
Ohne PV macht auch keine Diektvermarktung Sinn. Die Ergebnisse bei 0 kWp sind die Anteile der anderen dynamischen Anteile am Tarif, und die richtigkeit ist an dem  vorhandenen Roten balken ohne varianz zu sehen. Die Ausreizer um 0€ bei 0 kWh sind auf die Kombination ohne PV Anlage zurückzuführen. 
Einen sehr starken Einfluss hat die Batteriekapazität auf die Ersparnis. Unter der 7 kWh Kategorie ist eine Ersparnis höchst unwarscheinlich, da da die Jährlichen Fixkosten für die Direktvermarktung nicht von der Lastverschiebung durch die Batterie wieder reingeholt werden können. Darüber sind bis auf einzelfälle Ersparnisse mit einem Tarifwechsel zu erwarten. Die Einzelfälle werden Kombinationen aus einem hohen Stromverbrauch und einer kleinen PV-Anlage sein, abgeleitet aus den Tendenzen der anderen Kategorien. 
Im Allgemeinen schneiden die Tarife mit dynamischen Stromtarifen etwas schlechter, und Tarife mit zeitvariablen Netzentgelten etwas besser ab. 
"""
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



