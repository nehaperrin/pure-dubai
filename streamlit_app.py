import streamlit as st
import pandas as pd
import time

# --- 1. VISUAL CONFIGURATION ---
st.set_page_config(
    page_title="Pure Dubai | Search Once, Safe Everywhere",
    page_icon="🥗",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Lora:ital@0;1&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-color: #Fdfdfd;
    }

    /* Founder Note Styling (WITH TALLER WINDOW FOR FAMILY PHOTO) */
    .founder-box {
        background-color: #F9FBFD; /* Fallback color */
        
        /* 1. VISIBILITY: Kept at 75% white overlay so text is readable but photo is seen */
        background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), 
                          url('https://raw.githubusercontent.com/nehaperrin/pure-dubai/main/family.jpg');
        
        background-size: cover;
        
        /* 2. ALIGNMENT: 'center 35%' aims at the Upper-Middle (Best for Parents + Kids) */
        background-position: center 35%;
        
        /* 3. HEIGHT: Increased padding to 60px to show more of the vertical photo */
        padding: 60px;
        border-radius: 12px;
        border-left: 4px solid #A8D0E6;
        margin-bottom: 20px;
    }
    
    .founder-text {
        font-family: 'Lora', serif;
        font-size: 16px;
        color: #2C3E50;
        line-height: 1.8;
        font-weight: 600; 
    }
    .founder-sig {
        font-family: 'Lora', serif;
        font-style: italic;
        margin-top: 15px;
        color: #444;
    }

    /* Product Card Styling */
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        margin-bottom: 15px;
    }

    .safe-tag {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
    }

    .avoid-tag {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .warning-tag {
        background-color: #fff3cd;
        color: #856404;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .disclaimer-box {
        font-size: 12px;
        color: #777;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }
    
    .nutrition-row {
        font-size: 13px;
        color: #555;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 6px;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'basket' not in st.session_state:
    st.session_state['basket'] = []
if 'wishlist' not in st.session_state:
    st.session_state['wishlist'] = []

# Default Profiles
if 'profiles' not in st.session_state:
    st.session_state['profiles'] = {
        "Max (Strict Allergy)": ["Tree Nuts & Peanuts", "Sesame & Seeds", "Added Sugar & Syrups"],
        "Diane (Toddler Safe)": ["Added Sugar & Syrups", "High Natural Sugars (>15g)", "Artificial Colours", "Inflammatory Oils"],
        "Grandpa (Heart Health)": ["Sodium & Salt Watch", "Inflammatory Oils", "Added Sugar & Syrups"],
        "Clean Eating (Gut Health)": ["Gut Irritants & Emulsifiers", "Artificial Sweeteners", "Inflammatory Oils"]
    }

if 'active_profile' not in st.session_state:
    st.session_state['active_profile'] = list(st.session_state['profiles'].keys())[0]

# --- 3. FILTER DEFINITIONS ---
FILTER_PACKS = {
    # SUGAR & SWEETENERS
    "Added Sugar & Syrups": ["sugar", "sucrose", "glucose", "fructose", "corn syrup", "dextrose", "maltodextrin", "honey", "caramel"],
    "High Natural Sugars (>15g)": ["dates", "date syrup", "fruit juice concentrate", "apple juice", "grape juice", "pear juice", "agave", "maple syrup", "paste", "puree"],
    "Artificial Sweeteners": ["aspartame", "sucralose", "saccharin", "acesulfame", "neotame", "xylitol", "erythritol", "stevia"],
    
    # ADDITIVES
    "Artificial Colours": ["red 40", "yellow 5", "blue 1", "e102", "e110", "e129", "e133", "tartrazine"],
    "Gut Irritants & Emulsifiers": ["carrageenan", "xanthan gum", "guar gum", "lecithin", "polysorbate", "cellulose gum"],
    "Preservatives": ["benzoate", "sorbate", "nitrate", "nitrite", "sulfite", "bha", "bht"],

    # ALLERGIES & DIET
    "Tree Nuts & Peanuts": ["peanut", "almond", "cashew", "walnut", "pecan", "hazelnut", "pistachio", "macadamia"],
    "Sesame & Seeds": ["sesame", "tahini", "sunflower seed", "poppy seed"],
    "Dairy / Lactose": ["milk", "lactose", "whey", "casein", "butter", "cream", "yoghurt", "yogurt", "cheese"],
    "Gluten / Wheat": ["wheat", "barley", "rye", "malt", "brewer's yeast"],
    "Soy": ["soy", "edamame", "tofu", "lecithin"],
    "Shellfish": ["shrimp", "crab", "lobster", "prawn", "shellfish"],
    "Sodium & Salt Watch": ["salt", "sodium", "monosodium", "baking soda", "brine", "msg"],
    "Inflammatory Oils": ["palm oil", "canola oil", "rapeseed oil", "sunflower oil", "soybean oil", "vegetable oil", "hydrogenated", "margarine"]
}

# --- 4. REAL DATABASE LOADING ---
@st.cache_data(ttl=0)
def load_data():
    try:
        df = pd.read_csv("products.csv")
        df['Total Sugar (g)'] = pd.to_numeric(df['Total Sugar (g)'], errors='coerce').fillna(0)
        df['Salt (g)'] = pd.to_numeric(df['Salt (g)'], errors='coerce').fillna(0)
        df['Fat (g)'] = pd.to_numeric(df['Fat (g)'], errors='coerce').fillna(0)
        df['Carbs (g)'] = pd.to_numeric(df['Carbs (g)'], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        return pd.DataFrame([{"Product": "Error", "Brand": "System", "Price": "0", "Ingredients": "Please upload products.csv", "Total Sugar (g)": 0, "Salt (g)": 0, "Fat (g)": 0, "Carbs (g)": 0, "Image": ""}])

df = load_data()



# --- 5. SYNONYM ENGINE ---
SYNONYMS = {
    "snacks": ["chips", "crisps", "popcorn", "nuts", "bars", "bites", "crackers", "rice cakes"],
    "chips": ["crisps", "snacks", "popcorn"],
    "soda": ["drink", "juice", "cola", "beverage", "water"],
    "drinks": ["soda", "juice", "cola", "beverage", "water"],
    "yoghurt": ["yogurt", "dairy", "greek", "labneh", "pudding"],
    "pasta": ["spaghetti", "penne", "fusilli", "macaroni", "noodles"],
    "baby": ["toddler", "kids", "puree", "pouch", "formula"],
    "chocolate": ["cocoa", "cacao", "sweet", "treat"]
}

# --- 6. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", width=60)
    
    st.markdown("### 1. Start Shopping")
    shopping_mode = st.radio("How do you want to filter?", ["🖐️ Manual Selection", "👤 Use Saved Profile"], label_visibility="collapsed")
    
    active_filters = []
    
    if shopping_mode == "🖐️ Manual Selection":
        st.markdown("**Select filters manually:**")
        active_filters = st.multiselect("Avoiding:", options=list(FILTER_PACKS.keys()))
        
    else: # Saved Profile Mode
        st.markdown("**Choose a profile:**")
        profile_names = list(st.session_state['profiles'].keys())
        selected_profile = st.selectbox("Select:", profile_names, index=0)
        
        current_defaults = st.session_state['profiles'][selected_profile]
        st.markdown(f"**{selected_profile} avoids:**")
        st.multiselect("Avoiding:", options=list(FILTER_PACKS.keys()), default=current_defaults, disabled=True)
        active_filters = current_defaults

    st.divider()

    with st.expander("➕ Create New Profile"):
        new_name = st.text_input("Name (e.g. Grandma)")
        new_defaults = st.multiselect("Select Filters", options=list(FILTER_PACKS.keys()), key="new_prof_filters")
        if st.button("Save Profile"):
            if new_name and new_defaults:
                st.session_state['profiles'][new_name] = new_defaults
                st.success(f"Saved {new_name}!")
                time.sleep(1)
                st.rerun()

    st.success(f"🛒 Basket: {len(st.session_state['basket'])} items")

banned_ingredients = []
for pack in active_filters:
    banned_ingredients.extend(FILTER_PACKS[pack])

# --- 7. MAIN CONTENT ---

col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/9355/9355325.png", width=80)
with col_title:
    st.title("Pure Dubai")
    st.caption("SEARCH ONCE. SAFE EVERYWHERE.")

# UPDATED FOUNDER NOTE (WITH FADED BACKGROUND IMAGE)
with st.expander("❤️ From the Founder", expanded=True):
    st.markdown("""
    <div class="founder-box">
        <div class="founder-text">
        Hi, I'm Neha. A Dubai 80s kid, a recovering London banker, and a mom of two.<br><br>
        I created Pure Dubai to solve the 'Dubai Paradox': too many choices, not enough time.
        In today's world of free-from and healthy options, there are still way too many hidden ingredients.<br><br>
        <b>The 'Yoghurt Aisle' is one of the most deceptive places in the supermarket. You often see 'Healthy Kids Yoghurt' that has more sugar than a chocolate bar!</b><br><br>
        Moving back to Dubai with a food allergy child made the weekly shop a nightmare, so I built a solution. 
        <b>Pure Dubai isn't just an analyzer; it’s a scout.</b> We don't just scan your existing pantry; we help you find exactly what you need—clean, safe, and specific—across Dubai’s retailers in seconds.<br><br>
        I hope this helps you as much as it helped me.
        <div class="founder-sig">xo Neha</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Search Engine", "📚 News & Research", "ℹ️ How it Works", "❤️ Saved", "🛒 Basket"])

# --- TAB 1: SEARCH ---
with tab1:
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search_query = st.text_input("Search Ingredients or Products...", placeholder="e.g. Snacks, Soda, Yoghurt...")
    with col_s2:
        st.write("")
        st.write("")
        search_btn = st.button("Search", type="primary", use_container_width=True)

    if search_query or search_btn:
        clean_query = search_query.lower().replace("yogurt", "yoghurt").replace("flavor", "flavour").replace("color", "colour")
        
        # --- SYNONYM EXPANSION ---
        search_terms = [clean_query] 
        if clean_query in SYNONYMS:
            search_terms.extend(SYNONYMS[clean_query])
            
        search_pattern = "|".join(search_terms)

        results = df[df['Product'].str.contains(search_pattern, case=False, na=False) | 
                     df['Brand'].str.contains(search_pattern, case=False, na=False) | 
                     df['Category'].str.contains(search_pattern, case=False, na=False) |

