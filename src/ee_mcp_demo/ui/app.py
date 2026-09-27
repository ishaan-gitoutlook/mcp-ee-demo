import streamlit as st

from ee_mcp_demo.core.calculations import (
    calculate_charge,
    calculate_coulombs_law,
    calculate_electrical_power,
    calculate_ohms_law,
    calculate_parallel_resistance,
    calculate_series_resistance,
)
from ee_mcp_demo.core.exceptions import InvalidParameterError, MissingParameterError

st.set_page_config(page_title="MCP Circuit Sandbox (UI)", page_icon="⚡", layout="wide")

st.title("⚡ EE Circuit Sandbox")
st.markdown(
    "Welcome to the visual interface for the enterprise **EE MCP Demo**. "
    "Choose a tool from the sidebar to perform electrical engineering calculations."
)

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Choose a Calculator",
    [
        "Ohm's Law",
        "Series Resistance",
        "Parallel Resistance",
        "Electrical Power",
        "Coulomb's Law",
        "Capacitance Charge",
    ],
)

if page == "Ohm's Law":
    st.header("Ohm's Law Calculator")
    st.markdown("`V = I × R`")

    col1, col2, col3 = st.columns(3)
    with col1:
        v = st.number_input("Voltage (V)", value=0.0, step=0.1, key="ohm_v")
    with col2:
        i = st.number_input("Current (A)", value=0.0, step=0.1, key="ohm_i")
    with col3:
        r = st.number_input("Resistance (Ω)", value=0.0, step=0.1, key="ohm_r")

    v_val = v if v != 0.0 else None
    i_val = i if i != 0.0 else None
    r_val = r if r != 0.0 else None

    if st.button("Calculate"):
        try:
            ohm_result = calculate_ohms_law(voltage=v_val, current=i_val, resistance=r_val)
            st.success("Result:")
            st.json(ohm_result)
        except (MissingParameterError, InvalidParameterError) as e:
            st.error(str(e))

elif page == "Series Resistance":
    st.header("Series Resistance Calculator")
    st.markdown("`R_eq = R1 + R2 + ... + Rn`")

    r_input = st.text_input("Enter resistance values separated by commas (e.g. 10, 20.5, 30):")
    if st.button("Calculate"):
        try:
            r_list = [float(x.strip()) for x in r_input.split(",") if x.strip()]
            series_res = calculate_series_resistance(r_list)
            st.success("Result:")
            st.json(series_res)
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")
        except Exception as e:
            st.error(str(e))

elif page == "Parallel Resistance":
    st.header("Parallel Resistance Calculator")
    st.markdown("`1/R_eq = 1/R1 + 1/R2 + ... + 1/Rn`")

    r_input = st.text_input("Enter resistance values separated by commas (e.g. 10, 20.5, 30):")
    if st.button("Calculate"):
        try:
            r_list = [float(x.strip()) for x in r_input.split(",") if x.strip()]
            parallel_res = calculate_parallel_resistance(r_list)
            st.success("Result:")
            st.json(parallel_res)
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")
        except Exception as e:
            st.error(str(e))

elif page == "Electrical Power":
    st.header("Electrical Power Calculator")
    st.markdown("`P = V × I`")

    col1, col2 = st.columns(2)
    with col1:
        v = st.number_input("Voltage (V)", value=0.0, step=0.1)
    with col2:
        i = st.number_input("Current (A)", value=0.0, step=0.1)

    v_val = v if v != 0.0 else None
    i_val = i if i != 0.0 else None

    if st.button("Calculate"):
        try:
            power_res = calculate_electrical_power(voltage=v_val, current=i_val)
            st.success("Result:")
            st.json(power_res)
        except Exception as e:
            st.error(str(e))

elif page == "Coulomb's Law":
    st.header("Coulomb's Law Calculator")
    st.markdown("`F = k × (|q1 × q2|) / r²`")

    col1, col2, col3 = st.columns(3)
    with col1:
        q1 = st.number_input("Charge 1 (C)", value=0.0, format="%.2e")
    with col2:
        q2 = st.number_input("Charge 2 (C)", value=0.0, format="%.2e")
    with col3:
        rad = st.number_input("Distance (m)", value=0.0, format="%.2e")

    if st.button("Calculate"):
        try:
            coulomb_res = calculate_coulombs_law(q1=q1, q2=q2, r=rad)
            st.success("Result:")
            st.json(coulomb_res)
        except Exception as e:
            st.error(str(e))

elif page == "Capacitance Charge":
    st.header("Capacitance Charge Calculator")
    st.markdown("`Q = C × V`")

    col1, col2 = st.columns(2)
    with col1:
        c = st.number_input("Capacitance (F)", value=0.0, format="%.2e")
    with col2:
        v = st.number_input("Voltage (V)", value=0.0, format="%.2e")

    if st.button("Calculate"):
        try:
            charge_res = calculate_charge(capacitance=c, voltage=v)
            st.success("Result:")
            st.json(charge_res)
        except Exception as e:
            st.error(str(e))
