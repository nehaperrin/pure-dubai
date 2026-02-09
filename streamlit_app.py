import streamlit as st
import pandas as pd
import base64

# --- 1. VISUAL CONFIGURATION ---
st.set_page_config(
    page_title="SIFT KIDS | Safe Snacking",
    page_icon="👶",
    layout="wide"
)

# --- SVG HELPER FUNCTION ---
def render_svg(svg_string):
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" width="40"/>' % b64
    st.write(html, unsafe_allow_html=True)

# --- SMART SEARCH ENGINE (The Rosetta Stone) ---
def get_search_terms(query):
    """
    Converts a user query (e.g. 'yaourt') into a list of 
    database-friendly search terms (e.g. 'yog', 'petit filous').
    """
    q = query.lower().strip()
    
    # THE MAPPING DICTIONARY (US/UK/French/German -> Brand Targets)
    mappings = {
        # YOGHURT (Strict - No Milk)
        "yogurt": ["yog", "petit filous", "yeo", "nabta", "frubes", "actimel"],
        "yoghurt": ["yog", "petit filous", "yeo", "nabta", "frubes", "actimel"],
        "yog": ["yog", "petit filous", "yeo", "nabta", "frubes", "actimel"],
        "yaourt": ["yog", "petit filous", "yeo", "nabta", "frubes", "actimel"], # French
        
        # CHIPS/SNACKS
        "chips": ["crisps", "chips", "puffs", "popcorn"],
        "crisps": ["crisps", "chips", "puffs", "popcorn"],
        
        # MILK (Strict - No Yoghurt)
        "milk": ["milk", "soya", "oat", "koita", "alpro"],
        "lait": ["milk", "soya", "oat", "koita", "alpro"], # French
        
        # CHEESE
        "cheese": ["cheese", "cheestrings", "kiri", "babybel"],
        "fromage": ["cheese", "cheestrings", "kiri", "babybel"], # French
        
        # FRUIT SNACKS
        "fruit": ["fruit", "raisins", "mango", "apple", "bear", "yo yos", "paws"],
        "bear": ["bear", "yo yos", "paws"]
    }
    
    # 1. Direct Hit?
    if q in mappings:
        return mappings[q]
    
    # 2. Partial Hit? (e.g. "strawberry yoghurt")
    for key in mappings:
        if key in q:
            return mappings[key] + [q] # Search for specific flavor + category keywords
            
    # 3. No Match? Just search what they typed.
    return [q]

# Custom CSS - The "Earthy Apothecary" Aesthetic (Version 56)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');

    /* GLOBAL THEME */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #333333;
    }
    .stApp { background-color: #F9F9F7; }

    /* --- NUCLEAR RED KILLER --- */
    input:focus, textarea:focus, select:focus, div[data-baseweb="select"]:focus-within, div[data-baseweb="input"]:focus-within {
        border-color: #5D0E1D !important;
        box-shadow: 0 0 0 1px #5D0E1D !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { color: #5D0E1D !important; }
    .stTabs [data-baseweb="tab"]:hover { color: #5D0E1D !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #5D0E1D !important; }
    button:hover, div[role="button"]:hover { border-color: #5D0E1D !important; color: #5D0E1D !important; }
    
    /* Sidebar Toggle */
    div[role="radiogroup"] > label > div:first-child { border: 2px solid #555 !important; background-color: transparent !important; }
    div[role="radiogroup"] > label[data-checked="true"] > div:first-child { background-color: #F3E5AB !important; border: 2px solid #333 !important; }
    .stRadio > div[role="radiogroup"] > label { color: #333 !important; font-weight: 600 !important; }

    /* LAYOUT */
    [data-testid="stSidebar"] { background-color: #F4F6F4; border-right: 1px solid #E0E6E0; }
    
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif; font-weight: 600; color: #1A1A1A; letter-spacing: -0.5px; }
    .brand-logo { font-family: 'Cormorant Garamond', serif; font-size: 70px; font-weight: 600; color: #1A1A1A; letter-spacing: 6px; line-height: 1.0; text-align: center; }
    .brand-tagline { font-family: 'Montserrat', sans-serif; font-size: 10px; text-transform: uppercase; letter-spacing: 3px; color: #888; text-align: center; margin-top: 10px; margin-bottom: 30px; }
    .fancy-divider { height: 1px; background-color: #D0D0D0; margin: 40px 0; position: relative; }
    .fancy-divider:after { content: "✦"; position: absolute; left: 50%; top: -12px; background: #F9F9F7; padding: 0 10px; color: #999; }

    /* COMPONENTS */
    .founder-box { background-color: #F0F0EE; background-image: linear-gradient(rgba(249, 249, 247, 0.85), rgba(249, 249, 247, 0.85)), url('https://raw.githubusercontent.com/nehaperrin/pure-dubai/main/family.jpg'); background-size: cover; background-position: top center; min-height: 800px; padding: 40px; border: 1px solid #E0E0E0; margin-bottom: 40px; display: flex; flex-direction: column; justify-content: center; }
    .founder-text { font-family: 'Cormorant Garamond', serif; font-size: 20px; color: #1A1A1A; line-height: 1.8; font-style: italic; text-align: center; max-width: 700px; margin: 0 auto; }
    .founder-sig { font-family: 'Montserrat', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-top: 25px; color: #555; text-align: center; }

    .knowledge-card { background-color: #FFFFFF; border: 1px solid #E6E6E6; padding: 25px; margin-bottom: 20px; transition: 0.3s; }
    .knowledge-card:hover { border-color: #5D0E1D; }
    .knowledge-title { font-family: 'Cormorant Garamond', serif; font-size: 22px; color: #5D0E1D; margin-bottom: 10px; }
    .knowledge-body { font-size: 13px; line-height: 1.6; color: #555; }

    .product-card { background-color: #FFFFFF; padding: 25px; border: 1px solid #999999; border-radius: 0px; margin-bottom: 20px; }
    
    .verified-seal { border: 1px solid #8FBC8F; background: #F4F9F4; color: #2F4F2F; font-size: 10px; text-transform: uppercase; padding: 5px 10px; letter-spacing: 1px; display: inline-block; margin-bottom: 10px; }

    .sage-alert { background-color: #E8F0E9; border: 1px solid #CFE0D1; color: #2E5C38; padding: 15px; font-size: 13px; }
    .charcoal-alert { background-color: #F0F0F0; border: 1px solid #E0E0E0; color: #444; padding: 15px; font-size: 13px; }
    .stMultiSelect [data-baseweb="tag"] { background-color: #D8E2DC !important; color: #333 !important; border: 1px solid #BCCAC0; }
    
    .earthy-green { background-color: #E6F2E6; border: 1px solid #8FBC8F; color: #2F4F2F; padding: 15px; text-align: center; }
    .earthy-yellow { background-color: #FFF8E1; border: 1px solid #E4C06F; color: #4B3621; padding: 15px; text-align: center; }
    .earthy-red { background-color: #F9EBEB; border: 1px solid #CD5C5C; color: #4A0404; padding: 15px; text-align: center; }
    
    div.stButton > button { background-color: #333; color: white; border-radius: 0px; border: none; padding: 10px 20px; font-family: 'Montserrat', sans-serif; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; }
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
        "Toddler Safe (No Nasties)": ["The Nasties (Nitrates/Preservatives)", "Artificial Colours", "Added Sugar & Syrups"],
        "Clean Weaning": ["Added Sugar & Syrups", "Salt Watch", "Thickeners & Gums"]
    }

if 'active_profile' not in st.session_state:
    st.session_state['active_profile'] = list(st.session_state['profiles'].keys())[0]

# --- 3. FILTER DEFINITIONS ---
FILTER_PACKS = {
    "Added Sugar & Syrups": ["sugar", "sucrose", "glucose", "fructose", "corn syrup", "dextrose", "maltodextrin", "honey", "caramel", "cane juice"],
    "High Natural Sugars (>15g)": ["dates", "date syrup", "fruit juice concentrate", "apple juice", "grape juice", "pear juice", "agave", "maple syrup", "paste", "puree"],
    "Artificial Sweeteners": ["aspartame", "sucralose", "saccharin", "acesulfame", "neotame", "xylitol", "erythritol", "stevia"],
    "Artificial Colours": ["red 40", "yellow 5", "blue 1", "e102", "e110", "e129", "e133", "tartrazine", "sunset yellow", "allura red"],
    "The Nasties (Nitrates/Preservatives)": ["nitrate", "nitrite", "sodium nitrite", "sodium nitrate", "benzoate", "sorbate", "sulphite", "sulfite", "bha", "bht", "potassium sorbate"],
    "Thickeners & Gums": ["carrageenan", "xanthan gum", "guar gum", "lecithin", "polysorbate", "cellulose gum", "modified starch"],
    "Tree Nuts & Peanuts": ["peanut", "almond", "cashew", "walnut", "pecan", "hazelnut", "pistachio", "macadamia"],
    "Sesame & Seeds": ["sesame", "tahini", "sunflower seed", "poppy seed"],
    "Dairy / Lactose": ["milk", "lactose", "whey", "casein", "butter", "cream", "yoghurt", "yogurt", "cheese"],
    "Gluten / Wheat": ["wheat", "barley", "rye", "malt", "brewer's yeast", "flour"],
    "Soy": ["soy", "edamame", "tofu", "lecithin"],
    "Salt Watch": ["salt", "sodium", "monosodium", "baking soda", "brine", "msg"],
    "Inflammatory Oils": ["palm", "canola", "rapeseed", "sunflower", "soybean", "vegetable oil", "hydrogenated", "margarine", "palmolein"]
}

# --- 4. REAL DATABASE (THE KID LIST) ---
kids_db = [
    {"Product": "Kiddylicious Wafers (Blueberry)", "Brand": "Kiddylicious", "Category": "Baby Snacking", "Ingredients": "Jasmine rice flour, tapioca starch, apple juice concentrate, blueberry powder, natural flavour", "Total Sugar (g)": 4.0, "Salt (g)": 0.05, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Kiddylicious Fruity Bakes", "Brand": "Kiddylicious", "Category": "Baby Snacking", "Ingredients": "Wholemeal wheat flour, fruit filling (apple, strawberry), palm oil (sustainable), baking powder", "Total Sugar (g)": 12.0, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Nabta Plant Based Yoghurt", "Brand": "Nabta", "Category": "Dairy & Alt", "Ingredients": "Oat base, water, starch, pectin, live cultures", "Total Sugar (g)": 3.5, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Petit Filous (Strawberry)", "Brand": "Yoplait", "Category": "Dairy & Alt", "Ingredients": "Milk, sugar, fruit puree, fructose, modified starch, calcium phosphate, vitamin D", "Total Sugar (g)": 9.8, "Salt (g)": 0.12, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Yeo Valley Little Yeos", "Brand": "Yeo Valley", "Category": "Dairy & Alt", "Ingredients": "Organic Milk, organic fruit puree, organic sugar, milk protein", "Total Sugar (g)": 8.5, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Soft Biscotti", "Brand": "Kiddylicious", "Category": "Baby Snacking", "Ingredients": "Wheat flour, apple juice concentrate, sunflower oil, rice flour, baking powder", "Total Sugar (g)": 14.0, "Salt (g)": 0.05, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Fruity Puffs", "Brand": "Kiddylicious", "Category": "Baby Snacking", "Ingredients": "Corn flour, strawberry powder, banana powder, sunflower oil", "Total Sugar (g)": 3.0, "Salt (g)": 0.01, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Melty Buttons", "Brand": "Kiddylicious", "Category": "Baby Snacking", "Ingredients": "Jasmine rice flour, banana powder, pumpkin powder", "Total Sugar (g)": 5.0, "Salt (g)": 0.01, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Raisins Lunchbox", "Brand": "Supervalu", "Category": "Lunchbox", "Ingredients": "Raisins, sunflower oil", "Total Sugar (g)": 69.0, "Salt (g)": 0.05, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Oat Bars (Apple & Raisin)", "Brand": "Deliciously Ella", "Category": "Lunchbox", "Ingredients": "Gluten free oats, brown rice syrup, coconut oil, raisins, apple pieces", "Total Sugar (g)": 18.0, "Salt (g)": 0.02, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Squishy Little Fruit Bars", "Brand": "Bright Bites", "Category": "Lunchbox", "Ingredients": "Date paste, oat flour, coconut oil, natural flavour", "Total Sugar (g)": 22.0, "Salt (g)": 0.01, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Bear Yo Yos (Mango)", "Brand": "Bear", "Category": "Lunchbox", "Ingredients": "Apples, pears, mango, black carrot extract", "Total Sugar (g)": 42.0, "Salt (g)": 0.0, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Oat Bars (Fig)", "Brand": "Bobo's", "Category": "Lunchbox", "Ingredients": "Oats, brown rice syrup, fig paste, coconut oil, cane sugar", "Total Sugar (g)": 19.0, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Animal Crackers", "Brand": "Happy Snacks", "Category": "Lunchbox", "Ingredients": "Wheat flour, sugar, palm oil, cocoa powder, high fructose corn syrup", "Total Sugar (g)": 24.0, "Salt (g)": 0.3, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "10 Calorie Raspberry Jelly", "Brand": "Hartley's", "Category": "Pantry", "Ingredients": "Water, gelling agents, citric acid, aspartame, acesulfame K, sodium citrate, potassium sorbate", "Total Sugar (g)": 0.5, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Super Creamy Yoghurt (Avo & Granola)", "Brand": "Bright Bites", "Category": "Dairy & Alt", "Ingredients": "Yoghurt, avocado puree, oats, honey, sunflower seeds", "Total Sugar (g)": 8.0, "Salt (g)": 0.05, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Bear Paws (Apple & Blackcurrant)", "Brand": "Bear", "Category": "Lunchbox", "Ingredients": "Apples, pears, blackcurrant", "Total Sugar (g)": 38.0, "Salt (g)": 0.0, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Organic Crispy Sticks (Cocoa)", "Brand": "Piccolo", "Category": "Baby Snacking", "Ingredients": "Chickpea flour, cocoa butter, date syrup, hazelnut paste", "Total Sugar (g)": 11.0, "Salt (g)": 0.01, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Freeze Dried Crunchy Jackfruit", "Brand": "Kooky", "Category": "Lunchbox", "Ingredients": "100% Jackfruit", "Total Sugar (g)": 60.0, "Salt (g)": 0.0, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Raw Choco Almond Bar", "Brand": "Freakin' Healthy", "Category": "Lunchbox", "Ingredients": "Dates, almonds, cocoa powder, coconut oil", "Total Sugar (g)": 28.0, "Salt (g)": 0.02, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Strawberry Fruit Wriggles", "Brand": "Kiddylicious", "Category": "Baby Snacking", "Ingredients": "Apple puree, strawberry puree, pectin, apple juice concentrate", "Total Sugar (g)": 55.0, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Pro Heroes Corn Puff (Salt & Vinegar)", "Brand": "Prolife", "Category": "Lunchbox", "Ingredients": "Corn grits, sunflower oil, salt, vinegar powder, natural flavour", "Total Sugar (g)": 1.0, "Salt (g)": 1.2, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Wonky Apple Crisps (Mango)", "Brand": "Scrapples", "Category": "Lunchbox", "Ingredients": "Dried Apple, Mango juice", "Total Sugar (g)": 50.0, "Salt (g)": 0.0, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Blueberry Muffin Bar", "Brand": "Nakd", "Category": "Lunchbox", "Ingredients": "Dates, cashews, raisins, almonds, blueberries, natural flavour", "Total Sugar (g)": 48.0, "Salt (g)": 0.01, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Caramel Almond Bites", "Brand": "Freakin' Healthy", "Category": "Lunchbox", "Ingredients": "Dates, almonds, caramel flavour (natural), cocoa butter", "Total Sugar (g)": 30.0, "Salt (g)": 0.05, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
    {"Product": "Cheestrings Twisted", "Brand": "Strings & Things", "Category": "Dairy & Alt", "Ingredients": "Milk, salt, acidity regulator, rennet, annatto (colour)", "Total Sugar (g)": 0.5, "Salt (g)": 1.8, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Kiri Spreadable Cheese", "Brand": "Kiri", "Category": "Dairy & Alt", "Ingredients": "Cheese, cream, water, milk proteins, emulsifiers (polyphosphates), salt", "Total Sugar (g)": 2.0, "Salt (g)": 1.6, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Oat No Added Sugar Milk", "Brand": "Koita", "Category": "Dairy & Alt", "Ingredients": "Water, oats, sunflower oil, sea salt", "Total Sugar (g)": 4.5, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Original Soya Milk", "Brand": "Alpro", "Category": "Dairy & Alt", "Ingredients": "Soya base, sugar, calcium carbonate, sea salt, vitamins", "Total Sugar (g)": 2.5, "Salt (g)": 0.1, "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050158.png"},
    {"Product": "Freeze Dried Strawberry", "Brand": "La Lushe", "Category": "Lunchbox", "Ingredients": "100% Strawberry", "Total Sugar (g)": 50.0, "Salt (g)": 0.0, "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
]

@st.cache_data(ttl=0)
def load_data():
    return pd.DataFrame(kids_db)

df = load_data()




# --- 7. MAIN CONTENT ---

# BRAND HEADER
col_center = st.columns([1])[0]
with col_center:
    st.markdown('<div class="brand-logo">SIFT KIDS.</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tagline">The Digital Food Guard for Modern Mums.</div>', unsafe_allow_html=True)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

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
    col_s1, col_s2, col_s3 = st.columns([2, 2, 1])
    with col_s1:
        search_options = ["All Categories", "Baby Snacking", "Lunchbox", "Dairy & Alt", "Pantry"]
        cat_select = st.selectbox("Category", search_options, label_visibility="collapsed")
    with col_s2:
        text_search = st.text_input("Search Product...", placeholder="e.g. Bear, Yoghurt...", label_visibility="collapsed")
    with col_s3:
        search_btn = st.button("SIFT", type="primary", use_container_width=True)

    if search_btn or cat_select != "All Categories" or text_search:
        results = df.copy()
        
        # 1. Category Filter
        if cat_select != "All Categories":
            results = results[results['Category'] == cat_select]
            
        # 2. Smart Text Search
        if text_search:
            search_terms = get_search_terms(text_search)
            # Create regex pattern from all smart terms
            pattern = "|".join(search_terms)
            results = results[results['Product'].str.contains(pattern, case=False, na=False) |
                              results['Category'].str.contains(pattern, case=False, na=False) | 
                              results['Brand'].str.contains(pattern, case=False, na=False)]
        
        st.divider()
        if results.empty:
            st.markdown(f'<div class="charcoal-alert">No matches found. Try "Lunchbox" or "Yoghurt".</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"**Found {len(results)} items**")
            for index, row in results.iterrows():
                ing_list = str(row['Ingredients'])
                sugar_g = row['Total Sugar (g)']
                salt_g = row['Salt (g)']
                
                found_dangers = []
                warnings = []
                
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
                
                if "High Natural Sugars (>15g)" in active_filters:
                    natural_keywords = FILTER_PACKS["High Natural Sugars (>15g)"]
                    has_natural_ingredients = any(k in ing_list.lower() for k in natural_keywords)
                    if has_natural_ingredients and sugar_g > 15:
                        found_dangers.append(f"High Natural Sugar ({sugar_g}g)")

                is_safe = len(found_dangers) == 0
                
                with st.container():
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    col_img, col_info, col_action = st.columns([1, 3, 1])
                    with col_img:
                        img_link = row['Image'] if pd.notna(row['Image']) and row['Image'].startswith('http') else "https://cdn-icons-png.flaticon.com/512/3081/3081967.png"
                        st.image(img_link, width=100)
                    with col_info:
                        if is_safe:
                            if warnings:
                                st.markdown('<span class="warning-tag">⚠️ CHECK LABEL</span>', unsafe_allow_html=True)
                            else:
                                st.markdown('<span class="safe-tag">✓ VERIFIED SAFE</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="avoid-tag">✕ AVOID</span>', unsafe_allow_html=True)

                        st.markdown(f"### {row['Product']}")
                        st.caption(f"{row['Brand']} • {row['Category']}")
                        st.markdown(f'<div style="font-family: monospace; color: #666; font-size: 11px;">SUGAR: {sugar_g}g | SALT: {salt_g}g</div>', unsafe_allow_html=True)

                        if is_safe and warnings:
                            st.caption(f"Trace: {', '.join(warnings)}")
                        elif not is_safe:
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
    # Header with Journal SVG
    c_icon, c_text = st.columns([1, 10])
    with c_icon:
        render_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#333333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M12 2v20"/><path d="M12 12h8"/><path d="M12 7h8"/><path d="M12 17h8"/></svg>')
    with c_text:
        st.markdown("### Research Journal")
    
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown("""
        <div class="knowledge-card">
            <div class="knowledge-title">The Nitrate Problem</div>
            <div class="knowledge-body">
            Commonly found in processed meats, Nitrates are linked to cell damage. We scan for Sodium Nitrite and Potassium Nitrate automatically.
            <br><br>
            <a href="#" class="knowledge-link">READ THE STUDY ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="knowledge-card">
            <div class="knowledge-title">Red 40 & Hyperactivity</div>
            <div class="knowledge-body">
            The "Southampton Six" colours (including Red 40) increase hyperactivity in children. The EU requires a warning label; we just ban them.
            <br><br>
            <a href="#" class="knowledge-link">VIEW DATA ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_n2:
        st.markdown("""
        <div class="knowledge-card">
            <div class="knowledge-title">The Allergy Explosion</div>
            <div class="knowledge-body">
            Food allergies have risen by 50% in a decade. The leading theories? The Hygiene Hypothesis and the ultra-processing of our global food supply.
            <br><br>
            <a href="#" class="knowledge-link">READ REPORT ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: HOW IT WORKS ---
with tab3:
    st.markdown("### The SIFT Method")
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
        st.markdown('<div class="earthy-green"><b>✓ VERIFIED SAFE</b><br><small>Clean. No active filters detected.</small></div>', unsafe_allow_html=True)
    with tl2:
        st.markdown('<div class="earthy-yellow"><b>⚠️ CHECK LABEL</b><br><small>Contains a filter (e.g. Salt) but in LOW safe amounts.</small></div>', unsafe_allow_html=True)
    with tl3:
        st.markdown('<div class="earthy-red"><b>✕ AVOID</b><br><small>Contains active filters or high sugar/salt.</small></div>', unsafe_allow_html=True)

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
    render_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#333333" stroke-width="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>')
    st.caption("Your Shortlist")
    
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
    render_svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#333333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m5 11 4-7"></path><path d="m19 11-4-7"></path><path d="M2 11h20"></path><path d="m3.5 11 1.6 7.4a2 2 0 0 0 2 1.6h9.8c.9 0 1.8-.7 2-1.6l1.7-7.4"></path><path d="m9 11 1 9"></path><path d="m4.5 11 4 9"></path><path d="m15 11-1 9"></path></svg>')
    
    if not st.session_state['basket']:
        st.markdown('<div class="charcoal-alert">Your basket is empty.</div>', unsafe_allow_html=True)
    else:
        for item in st.session_state['basket']:
            st.markdown(f"**{item['Product']}**")
        st.divider()
        
        st.markdown("### Checkout via Retailer")
        st.caption("Export your safe list directly to your preferred store:")
        c1, c2, c3 = st.columns(3)
        with c1: st.button("KIBSONS ↗", use_container_width=True)
        with c2: st.button("CARREFOUR ↗", use_container_width=True)
        with c3: st.button("SPINNEYS ↗", use_container_width=True)
        
        st.text_area("Or Copy List:", value="SIFT Order:\n" + "\n".join([f"- {i['Product']}" for i in st.session_state['basket']]), height=100)
