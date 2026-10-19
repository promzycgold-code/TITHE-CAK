import streamlit as st
from num2words import num2words

# Set page config for a mobile-friendly view
st.set_page_config(page_title="Mobile Tithe Calculator", layout="centered")

st.title("🧮 Tithe Calculator")
st.write("Tap the screen buttons below to type your income amount.")

# Initialize session state for income text if it doesn't exist
if "income_str" not in st.session_state:
    st.session_state.income_str = ""

# --- Keyboard Action Logic ---
def press_key(key):
    if key == "C":
        st.session_state.income_str = ""
    elif key == ".":
        # Prevent adding more than one decimal point
        if "." not in st.session_state.income_str:
            if st.session_state.income_str == "":
                st.session_state.income_str = "0."
            else:
                st.session_state.income_str += "."
    else:
        # Prevent multiple leading zeros
        if st.session_state.income_str == "0":
            st.session_state.income_str = key
        else:
            st.session_state.income_str += key

# --- Digital Display ---
display_val = st.session_state.income_str if st.session_state.income_str else "0"
try:
    formatted_display = f"₦ {float(display_val):,.2f}" if "." in display_val or float(display_val) > 0 else f"₦ {float(display_val):,.0f}"
except ValueError:
    formatted_display = "₦ 0.00"

st.markdown(
    f"""
    <div style="
        background-color: #EEF8CD; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: right; 
        font-size: 2.2rem; 
        font-weight: bold; 
        color: #1A312C;
        border: 2px solid #333;
        margin-bottom: 15px;
    ">
        {display_val if display_val != "" else "0"}
    </div>
    """, 
    unsafe_allow_html=True
)

# --- Responsive On-Screen Keyboard Grid ---
# Using pure Streamlit buttons layout so it is 100% reliable across all devices
keys = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    [".", "0", "C"]
]

# Render the grid layout layout
for row in keys:
    cols = st.columns(3)
    for i, key in enumerate(row):
        # Apply distinct styling to Clear button
        if key == "C":
            if cols[i].button(key, key=f"btn_{key}", use_container_width=True, type="primary"):
                press_key(key)
                st.rerun()
        else:
            if cols[i].button(key, key=f"btn_{key}", use_container_width=True):
                press_key(key)
                st.rerun()

st.markdown("---")

# --- Mathematical Processing & Calculations ---
try:
    income = float(st.session_state.income_str) if st.session_state.income_str else 0.0
except ValueError:
    income = 0.0

if income > 0:
    # Safe rounding to 2 decimal places (10% tithe calculation)
    fina = round(income * 0.10, 2)

    naira_part = int(fina)
    kobo_part = round((fina - naira_part) * 100)

    # Convert figures to text words
    words_format = num2words(naira_part).replace("-", " ") + " naira"
    if kobo_part > 0:
        words_format += f" and {num2words(kobo_part).replace('-', ' ')} kobo"

    # Display clean analytics cards with results
    st.metric(label="Calculated Tithe (10%)", value=f"₦{fina:,.2f}")
    st.info(f"**Tithe in Words:** {words_format.capitalize()}")
else:
    st.warning("Please tap numbers on the onscreen keyboard to compute.")
