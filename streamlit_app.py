import streamlit as st
import pandas as pd
import time

# --- 1. VISUAL CONFIGURATION ---
st.set_page_config(
    page_title="SIFT | Filter the Noise",
    page_icon="✨",
    layout="wide"
)

# Custom CSS - The "Apothecary" Aesthetic (Version 42)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400;500&family=Roboto+Mono:wght@400;500&display=swap');

    /* GLOBAL THEME */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #333333;
    }
    
    /* BACKGROUND: Subtle Paper Grain Texture */
    .stApp {
        background-color: #F9F9F7;
        background-image: url("https://www.transparenttextures.com/patterns/cream-paper.png");
        background-size: auto;
    }

    /* BURGUNDY ACCENTS (Overriding Streamlit Red) */
    /* 1. Active Tab Underline & Text */
    .stTabs [aria-selected="true"] {
        color: #5D0E1D !important; /* Deep Burgundy */
        border-bottom-color: #5D0E1D !important;
    }
    
    /* 2. Sidebar Selection & Toggles */
    .stRadio > div[role="radiogroup"] > label > div:first-child {
        background-color: #5D0E1D !important; /* Burgundy Radio Button */
        border-color: #5D0E1D !important;
    }
    
    /* 3. Input Focus Borders (The "Glow") */
    input:focus, textarea:focus, div[data-baseweb="select"]:focus-within {
        border-color: #5D0E1D !important;
        box-shadow: 0 0 0 1px #5D0E1D !important;
    }

    /* SIDEBAR styling */
    [data-testid="stSidebar"] {
        background-color: #F4F6F4;
        border-right: 1px solid #E0E6E0;
    }

    /* CUSTOM ALERTS (Sage & Charcoal) */
    .sage-alert {
        background-color: #E8F0E9;
        border: 1px solid #CFE0D1;
        color: #2E5C38;
        padding: 15px;
        border-radius: 0px;
        font-size: 14px;
        margin-bottom: 15px;
    }
    .charcoal-alert {
        background-color: #F0F0F0;
        border: 1px solid #E0E0E0;
        color: #444;
        padding: 15px;
        border-radius: 0px;
        font-size: 14px;
        margin-bottom: 15px;
    }

    /* TAG OVERRIDES (Sage Green Tags) */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #D8E2DC !important;
        color: #333 !important;
        border: 1px solid #BCCAC0;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        color: #1A1A1A;
        letter-spacing: -0.5px;
    }
    .brand-logo {
        font-family: 'Cormorant Garamond', serif;
        font-size: 60px;
        font-weight: 600;
        color: #1A1A1A;
        letter-spacing: 4px;
        line-height: 1.0;
    }
    .brand-tagline {
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #888;
        margin-top: 10px;
        margin-bottom: 40px;
    }

    /* FOUNDER NOTE */
    .founder-box {
        background-color: #F0F0EE;
        background-image: linear-gradient(rgba(249, 249, 247, 0.85), rgba(249, 249, 247, 0.85)), 
                          url('https://raw.githubusercontent.com/nehaperrin/pure-dubai/main/family.jpg');
        background-size: cover;
        background-position: top center;
        min-height: 800px;
        padding: 40px;
        border: 1px solid #E0E0E0;
        margin-bottom: 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .founder-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 20px;
        color: #1A1A1A;
        line-height: 1.8;
        font-style: italic;
        text-align: center;
        max-width: 700px;
        margin: 0 auto;
    }
    .founder-sig {
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 25px;
        color: #555;
        text-align: center;
    }

    /* KNOWLEDGE BOX */
    .knowledge-box {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 20px;
        border-radius: 0px;
        margin-bottom: 20px;
        color: #333;
    }
    .knowledge-link {
        font-size: 11px;
        text-transform: uppercase;
        color: #7FA182;
        text-decoration: none;
        font-weight: 600;
    }

    /* PRODUCT CARD (The "Muji" Grid) */
    .product-card {
        background-color: #FFFFFF;
        padding: 25px;
        border: 1px solid #D0D0D0; /* Darker, sharper border */
        border-radius: 0px; /* Zero radius = Clinical feel */
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .product-card:hover { border-color: #5D0E1D; } /* Burgundy Hover */
    
    .safe-tag { background-color: #E8F0E9; color: #2E5C38; padding: 4px 10px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; border: 1px solid #CFE0D1; }
    .avoid-tag { background-color: #F7EAE9; color: #8A3C34; padding: 4px 10px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; border: 1px solid #EBD5D3; }
    .warning-tag { background-color: #FAF5E6; color: #856404; padding: 4px 10px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; border: 1px solid #F0E6C8; }
    
    /* DATA FONT: The "Seed" Look */
    .nutrition-row {
        font-family: 'Roboto Mono', monospace; /* Typewriter font */
        font-size: 11px;
        color: #555;
        border-top: 1px solid #eee;
        border-bottom: 1px solid #eee;
        padding: 10px 0;
        margin: 15px 0;
        letter-spacing: -0.5px;
    }
    
    /* BUTTONS: Burgundy Primary */
    div.stButton > button {
        background-color: #333;
        color: white;
        border-radius: 0px;
        border: none;
        padding: 10px 20px;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 12px;
    }
    div.stButton > button:hover { background-color: #5D0E1D; color: white; }
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
    "Inflammatory Oils": ["palm", "canola", "rapeseed", "sunflower", "soybean", "vegetable oil", "hydrogenated", "margarine"]
}

# --- 4. REAL DATABASE LOADING ---
@st.cache_data(ttl=0)
def load_data():
    try:
        df = pd.read_csv("products.csv")
        cols = ['Total Sugar (g)', 'Salt (g)', 'Fat (g)', 'Carbs (g)']
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        return pd.DataFrame([{"Product": "Error", "Brand": "System", "Price": "0", "Ingredients": "Please upload products.csv", "Category": "None", "Total Sugar (g)": 0, "Salt (g)": 0, "Fat (g)": 0, "Carbs (g)": 0, "Image": ""}])

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
    st.markdown("### PREFERENCES")
    shopping_mode = st.radio("Mode", ["Manual Selection", "Saved Profile"], label_visibility="collapsed")
    
    active_filters = []
    
    if shopping_mode == "Manual Selection":
        st.caption("Active Filters:")
        active_filters = st.multiselect("Select:", options=list(FILTER_PACKS.keys()), label_visibility="collapsed")
        
    else: # Profile Mode
        st.caption("Active Profile:")
        profile_names = list(st.session_state['profiles'].keys())
        selected_profile = st.selectbox("Select:", profile_names, index=0, label_visibility="collapsed")
        
        current_defaults = st.session_state['profiles'][selected_profile]
        active_filters = st.multiselect("Filters Applied:", options=list(FILTER_PACKS.keys()), default=current_defaults)
        
        if st.button("Delete Profile"):
            if len(profile_names) > 1:
                del st.session_state['profiles'][selected_profile]
                st.rerun()
            else:
                st.toast("Cannot delete the last profile!")

    st.divider()
    with st.expander("Create Profile"):
        new_name = st.text_input("Name")
        new_defaults = st.multiselect("Filters", options=list(FILTER_PACKS.keys()), key="new_prof")
        if st.button("Save"):
            if new_name and new_defaults:
                st.session_state['profiles'][new_name] = new_defaults
                st.rerun()

    st.divider()
    st.markdown("### BASKET")
    if not st.session_state['basket']:
        st.caption("0 items.")
    else:
        st.caption(f"{len(st.session_state['basket'])} items.")

banned_ingredients = []
for pack in active_filters:
    banned_ingredients.extend(FILTER_PACKS[pack])




# --- 7. MAIN CONTENT ---

# BRAND HEADER
col_spacer, col_brand, col_spacer2 = st.columns([1, 2, 1])
with col_brand:
    st.markdown('<div class="brand-logo">SIFT.</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tagline">Search Once. Safe Everywhere.</div>', unsafe_allow_html=True)

# FOUNDER NOTE
with st.expander("The Founder's Note", expanded=True):
    st.markdown("""
    <div class="founder-box">
        <div class="founder-text">
        Food labels are often designed to sell, not to inform. The 'Yoghurt Aisle' is the perfect crime scene—where 'Healthy Kids Yoghurt' often has more sugar than a chocolate bar.
        <br><br>
        I built SIFT because I was tired of needing a chemistry degree just to buy snacks for my kids, not to mention my son who suffers from life-threatening food allergies. We are a food-sifting company dedicated to radical transparency.
        <br><br>
        SIFT acts as your digital scout, scanning Dubai’s shelves to separate the nutritious from the deceptive. No hidden nasties. No marketing fluff. Just an engine to find real, safe food.
        </div>
        <div class="founder-sig">NEHA &bull; FOUNDER</div>
    </div>
    """, unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["SEARCH", "KNOWLEDGE", "HOW IT WORKS", "FAVOURITES", "BASKET"])

# --- TAB 1: SEARCH ---
with tab1:
    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        search_options = ["All Categories", "Snacks", "Dairy", "Drinks", "Baby Food", "Pantry"]
        cat_select = st.selectbox("Category", search_options, label_visibility="collapsed")
        
    with col_s2:
        search_btn = st.button("SIFT", type="primary", use_container_width=True)

    if search_btn or cat_select != "All Categories":
        results = df.copy()
        if cat_select != "All Categories":
            search_term = cat_select.lower().rstrip('s') 
            results = results[results['Category'].str.contains(search_term, case=False, na=False) | 
                              results['Product'].str.contains(search_term, case=False, na=False)]
        
        st.divider()
        
        if results.empty:
            st.markdown(f'<div class="charcoal-alert">No matches found for <b>{cat_select}</b> in the demo database.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"**Found {len(results)} items**")
            
            for index, row in results.iterrows():
                ing_list = str(row['Ingredients'])
                sugar_g = row['Total Sugar (g)']
                salt_g = row['Salt (g)']
                
                found_dangers = []
                warnings = []
                
                # Ingredient Scan
                for bad in banned_ingredients:
                    if bad.lower() in ing_list.lower():
                        if bad.lower() == "salt":
                            if salt_g > 1.5: found_dangers.append(f"High Salt ({salt_g}g)")
                            else: warnings.append(f"Contains Salt ({salt_g}g)")
                        elif bad in FILTER_PACKS["Added Sugar & Syrups"]:
                            if sugar_g > 5: found_dangers.append(f"{bad} (High)")
                            else: warnings.append(f"Contains {bad} ({sugar_g}g)")
                        elif bad in FILTER_PACKS["High Natural Sugars (>15g)"]:
                            continue 
                        else:
                            found_dangers.append(bad)
                
                # 15g Rule
                if "High Natural Sugars (>15g)" in active_filters:
                    natural_keywords = FILTER_PACKS["High Natural Sugars (>15g)"]
                    has_natural_ingredients = any(k in ing_list.lower() for k in natural_keywords)
                    if has_natural_ingredients and sugar_g > 15:
                        found_dangers.append(f"High Natural Sugar ({sugar_g}g)")

                is_safe = len(found_dangers) == 0
                
                # PRODUCT CARD
                with st.container():
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    col_img, col_info, col_action = st.columns([1, 3, 1])
                    with col_img:
                        img_link = row['Image'] if pd.notna(row['Image']) and row['Image'].startswith('http') else "https://cdn-icons-png.flaticon.com/512/3081/3081967.png"
                        st.image(img_link, width=100)
                    with col_info:
                        st.markdown(f"### {row['Product']}")
                        st.caption(f"{row['Brand']} • {row['Category']}")
                        
                        st.markdown(f"""
                        <div class="nutrition-row">
                        SUGAR: {sugar_g}g | SALT: {salt_g}g
                        </div>
                        """, unsafe_allow_html=True)

                        if is_safe:
                            if warnings:
                                st.markdown('<span class="warning-tag">⚠️ CHECK LABEL</span>', unsafe_allow_html=True)
                                st.caption(f"Trace: {', '.join(warnings)}")
                            else:
                                st.markdown('<span class="safe-tag">✓ VERIFIED SAFE</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="avoid-tag">✕ AVOID</span>', unsafe_allow_html=True)
                            st.markdown(f":red[{', '.join(found_dangers)}]")
                        
                        with st.expander("Ingredients"):
                            st.caption(ing_list)
                    with col_action:
                        st.write("")
                        if is_safe:
                            if st.button("ADD", key=f"add_{index}"):
                                st.session_state['basket'].append(row)
                                st.toast("Added")
                            if st.button("FAVE", key=f"save_{index}"):
                                st.session_state['wishlist'].append(row)
                                st.toast("Saved")
                        else:
                            st.button("UNSAFE", disabled=True, key=f"bad_{index}")
                    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: KNOWLEDGE ---
with tab2:
    st.markdown("### 🧬 Science & Research")
    
    st.markdown("""
    <div class="knowledge-box">
    <b>Did you know?</b> 95% of your serotonin (the happiness hormone) is produced in your gut.
    </div>
    """, unsafe_allow_html=True)

    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown("""
        <div class="knowledge-box">
        <b>Why Gut Health Matters</b><br>
        Modern research connects our gut microbiome to everything from ADHD in children to immunity and mental health in adults.
        <br><br>
        <a href="#" class="knowledge-link">READ STUDY ↗</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="knowledge-box">
        <b>The Allergy Explosion</b><br>
        Food allergies in children have risen by 50% in the last decade. Why? Theories point to the "Hygiene Hypothesis" and the ultra-processing of our food supply.
        <br><br>
        <a href="#" class="knowledge-link">READ REPORT ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with col_n2:
        st.markdown("""
        <div class="knowledge-box">
        <b>The ADHD Link</b><br>
        Studies suggest that certain artificial colours (like Red 40 and Yellow 5) and preservatives (like Sodium Benzoate) can exacerbate hyperactivity in children.
        <br><br>
        <a href="#" class="knowledge-link">VIEW DATA ↗</a>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: HOW IT WORKS ---
with tab3:
    st.markdown("### 🧬 The SIFT Method")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**STEP 1: SELECT**")
        st.caption("You have two options: 1) Manually select filters in the sidebar (e.g. Sugar, Oils), or 2) Create/Use a pre-saved Profile (e.g. 'Max Allergy') for one-click setup.")
    with c2:
        st.markdown("**STEP 2: SCAN**")
        st.caption("Enter a product type (e.g. 'Yoghurt'). Our engine scans the database, reading every label for hidden ingredients and filtering to your requirements.")
    with c3:
        st.markdown("**STEP 3: DECIDE**")
        st.caption("We flag items as Safe, Warning (Check Label), or Avoid. Use the Traffic Light system to make quick, safe decisions.")
    
    st.divider()
    
    st.markdown("### 🚦 Traffic Light System")
    tl1, tl2, tl3 = st.columns(3)
    with tl1:
        st.success("✓ VERIFIED SAFE")
        st.caption("Clean. No active filters detected.")
    with tl2:
        st.warning("⚠️ CHECK LABEL")
        st.caption("Contains a filter (e.g. Salt) but in LOW safe amounts.")
    with tl3:
        st.error("✕ AVOID")
        st.caption("Contains active filters or high sugar/salt.")

    st.divider()
    st.markdown("### 🔍 Filter Glossary (The Rules)")
    st.caption("The thresholds we use to protect you:")
    
    for category, ingredients in FILTER_PACKS.items():
        with st.expander(f"📦 {category}"):
            if "Added Sugar" in category: st.markdown('<div class="sage-alert">⚠️ <b>Smart Scan:</b> Total sugar < 5g is allowed (Warning). > 5g is Avoid.</div>', unsafe_allow_html=True)
            if "High Natural Sugars" in category: st.markdown('<div class="sage-alert">⚠️ <b>Health Note:</b> Natural sugars (dates, fruit) capped at 15g.</div>', unsafe_allow_html=True)
            if "Sodium" in category: st.markdown('<div class="sage-alert">⚠️ <b>Medical Standard:</b> >1.5g Salt is High.</div>', unsafe_allow_html=True)
            if "Inflammatory Oils" in category: st.markdown('<div class="sage-alert">⚠️ <b>Strict Policy:</b> We flag ANY presence of seed oils.</div>', unsafe_allow_html=True)
            st.write(", ".join(ingredients))

# --- TAB 4: FAVOURITES ---
with tab4:
    if not st.session_state['wishlist']:
        st.markdown('<div class="charcoal-alert">No favourites yet.</div>', unsafe_allow_html=True)
    else:
        for idx, item in enumerate(st.session_state['wishlist']):
            st.markdown(f"**{item['Product']}**")
            st.caption(f"{item['Brand']}")
            if st.button(f"Add to Basket", key=f"move_{idx}"):
                st.session_state['basket'].append(item)
                st.session_state['wishlist'].pop(idx)
                st.rerun()
            st.divider()

# --- TAB 5: BASKET ---
with tab5:
    if not st.session_state['basket']:
        st.markdown('<div class="charcoal-alert">Your basket is empty.</div>', unsafe_allow_html=True)
    else:
        for item in st.session_state['basket']:
            st.markdown(f"**{item['Product']}**")
        st.divider()
        export_text = "SIFT Order:\n" + "\n".join([f"- {i['Product']}" for i in st.session_state['basket']])
        st.text_area("Export List for Retailer:", value=export_text, height=150)
