import streamlit as st


class Streamlit():

    def __init__(self):
        self.create_app_interface()
        pass

    def __del__(self):
        pass

    def create_app_interface(self):


        st.title("Dynamic Energy Price Benefit Calculator")
    
        # Checkbox for PV system
        check_pv = st.checkbox("Do you have a PV system?")
        
        if check_pv:
            # PV Power Selection
            pv_power = st.slider("Select your PV system power (kWp)", 1, 25, 5)
            
            # PV Direction Selection
            direction_options = {
                0: "North",
                20: "20°",
                40: "40°",
                60: "60°",
                80: "80°",
                90: "East",
                100: "100°",
                120: "120°",
                140: "140°",
                160: "160°",
                180: "South",
                200: "200°",
                220: "220°",
                240: "240°",
                260: "260°",
                280: "280°",
                300: "300°",
                320: "320°",
                340: "340°"
            }
            pv_direction = st.select_slider("Select PV system direction", options=list(direction_options.keys()), format_func=lambda x: direction_options[x])
            
            # Display selected values
            st.write(f"### Selected PV System Configuration")
            st.write(f"**Power:** {pv_power} kWp")
            st.write(f"**Direction:** {direction_options[pv_direction]}")
