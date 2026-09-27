import streamlit as st

from ee_mcp_demo.core.calculations import (
    calc_charge,
    calc_coulombs_law,
    calc_electrical_power,
    calc_ohms_law,
    calc_parallel_resistance,
    calc_series_resistance,
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
            result = calc_ohms_law(voltage=v_val, current=i_val, resistance=r_val)
            st.success("Result:")
            st.json(result)
        except (MissingParameterError, InvalidParameterError) as e:
            st.error(str(e))

elif page == "Series Resistance":
    st.header("Series Resistance Calculator")
    st.markdown("`R_eq = R1 + R2 + ... + Rn`")

    r_input = st.text_input("Enter resistance values separated by commas (e.g. 10, 20.5, 30):")
    if st.button("Calculate"):
        try:
            r_list = [float(x.strip()) for x in r_input.split(",") if x.strip()]
            result = calc_series_resistance(r_list)
            st.success("Result:")
            st.json(result)
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
            result = calc_parallel_resistance(r_list)
            st.success("Result:")
            st.json(result)
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")
        except Exception as e:
            st.error(str(e))

elif page == "Electrical Power":
    st.header("Electrical Power Calculator")
    st.markdown("`P = V × I`")

    col1, col2, col3 = st.columns(3)
    with col1:
        p = st.number_input("Power (W)", value=0.0, step=0.1)
    with col2:
        v = st.number_input("Voltage (V)", value=0.0, step=0.1)
    with col3:
        i = st.number_input("Current (A)", value=0.0, step=0.1)

    p_val = p if p != 0.0 else None
    v_val = v if v != 0.0 else None
    i_val = i if i != 0.0 else None

    if st.button("Calculate"):
        try:
            result = calc_electrical_power(power=p_val, voltage=v_val, current=i_val)
            st.success("Result:")
            st.json(result)
        except Exception as e:
            st.error(str(e))

elif page == "Coulomb's Law":
    st.header("Coulomb's Law Calculator")
    st.markdown("`F = k × (|q1 × q2|) / r²`")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        f = st.number_input("Force (N)", value=0.0, format="%.2e")
    with col2:
        q1 = st.number_input("Charge 1 (C)", value=0.0, format="%.2e")
    with col3:
        q2 = st.number_input("Charge 2 (C)", value=0.0, format="%.2e")
    with col4:
        r = st.number_input("Distance (m)", value=0.0, format="%.2e")

    f_val = f if f != 0.0 else None
    q1_val = q1 if q1 != 0.0 else None
    q2_val = q2 if q2 != 0.0 else None
    r_val = r if r != 0.0 else None

    if st.button("Calculate"):
        try:
            result = calc_coulombs_law(force=f_val, charge1=q1_val, charge2=q2_val, distance=r_val)
            st.success("Result:")
            st.json(result)
        except Exception as e:
            st.error(str(e))

elif page == "Capacitance Charge":
    st.header("Capacitance Charge Calculator")
    st.markdown("`Q = C × V`")

    col1, col2, col3 = st.columns(3)
    with col1:
        q = st.number_input("Charge (C)", value=0.0, format="%.2e")
    with col2:
        c = st.number_input("Capacitance (F)", value=0.0, format="%.2e")
    with col3:
        v = st.number_input("Voltage (V)", value=0.0, format="%.2e")

    q_val = q if q != 0.0 else None
    c_val = c if c != 0.0 else None
    v_val = v if v != 0.0 else None

    if st.button("Calculate"):
        try:
            result = calc_charge(charge=q_val, capacitance=c_val, voltage=v_val)
            st.success("Result:")
            st.json(result)
        except Exception as e:
            st.error(str(e))
