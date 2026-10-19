import streamlit as st

# Set page config for a mobile-friendly view
st.set_page_config(page_title="Mobile Tithe Calculator", layout="centered")

# --- CUSTOM CSS FOR MOBILE KEYBOARD OPTIMIZATION ---
# This forces columns to stay side-by-side on mobile instead of stacking in a straight line
st.markdown(
    """
    <style>
    /* Force columns to sit side-by-side on mobile without wrapping */
    [data-testid="column"] {
        width: calc(25% - 6px) !important;
        flex: 1 1 calc(25% - 6px) !important;
        min-width: calc(25% - 6px) !important;
    }
    
    /* Ensure the row container handles flex properly */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 8px !important;
        margin-bottom: 8px;
    }
    
    /* Make buttons large, tap-friendly, and look like a real calculator app */
    button {
        height: 70px !important;  /* Changed from 5px to 70px for mobile fingers */
        width: 100% !important;
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important; /* Smooth rounded corners */
        background-color: #f0f2f6 !important; /* Soft neutral button background */
        border: none !important;
        transition: background-color 0.1s ease;
        
        /* Prevent annoying mobile zoom/double-tap highlights */
        touch-action: manipulation;
        -webkit-user-select: none;
        user-select: none;
    }

    /* Subtle tap effect for mobile */
    button:active {
        background-color: #e0e2e6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🧮 Tithe Calculator")
st.write("Tap the screen buttons below to type your income amount.")

# --- Custom Number-to-Words Engine (Replaces num2words) ---
def number_to_words(n):
    if n == 0: 
        return "zero"
    
    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", 
             "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", 
             "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    words = []
    
    if n >= 1000000:
        words.append(f"{number_to_words(n // 1000000)} million")
        n %= 1000000
    if n >= 1000:
        words.append(f"{number_to_words(n // 1000)} thousand")
        n %= 1000
    if n >= 100:
        words.append(f"{units[n // 100]} hundred")
        n %= 100
    if n >= 20:
        words.append(tens[n // 10])
        n %= 10
    if n > 0:
        words.append(units[n])
        
    return " ".join([w for w in words if w])

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
keys = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    [".", "0", "C"]
]

# Render the grid layout
for row in keys:
    cols = st.columns(3)
    for i, key in enumerate(row):
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

    # Convert figures to text words using our custom engine
    words_format = number_to_words(naira_part) + " naira"
    if kobo_part > 0:
        words_format += f" and {number_to_words(kobo_part)} kobo"

    # Display clean analytics cards with results
    st.metric(label="Calculated Tithe (10%)", value=f"₦{fina:,.2f}")
    st.info(f"**Tithe in Words:** {words_format.capitalize()}")
else:
    st.warning("Please tap numbers on the onscreen keyboard to compute.")
