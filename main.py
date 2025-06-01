import streamlit as st

if __name__ == "__main__":
        calc = st.Page("calc.py", title="Berechnung") #, icon="")
        expl = st.Page("explain.py", title="Hintergrund Erklärungen") #, icon="")
        info = st.Page("thesis.py", title="Weitere Erkenntnisse") #, icon="")

        pages = st.navigation([calc, expl, info])
        pages.run()    
        st.sidebar.info("""Bei einem Seitenwechsel gehen die Einstellungen und die laufenden Berechnungen verlohren.""")
