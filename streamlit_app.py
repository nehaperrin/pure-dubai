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

    /* Founder Note Styling */
    .founder-box {
        background-color: #F9FBFD;
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid #A8D0E6;
        margin-bottom: 20px;
    }
    .founder-text {
        font-family: 'Lora', serif;
        font-size: 16px;
        color: #2C3E50;
        line-height: 1.7;
        font-weight: 400;
    }
    .founder-sig {
        font-family: 'Lora', serif;
        font-style: italic;
        margin-top: 15px;
        color: #555;
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



# --- 5. SYNONYM ENGINE (THE SMART SEARCH) ---
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
        search_terms = [clean_query] # Start with what user typed
        
        # If the user typed "snacks", add ["chips", "crisps", etc] to the search list
        if clean_query in SYNONYMS:
            search_terms.extend(SYNONYMS[clean_query])
            
        # Create a giant search pattern: "snacks|chips|crisps|popcorn..."
        search_pattern = "|".join(search_terms)

        results = df[df['Product'].str.contains(search_pattern, case=False, na=False) | 
                     df['Brand'].str.contains(search_pattern, case=False, na=False) | 
                     df['Category'].str.contains(search_pattern, case=False, na=False) |
                     df['Ingredients'].str.contains(search_pattern, case=False, na=False)]
        
        if results.empty:
            st.warning(f"No matches found for '{search_query}'. Try broader terms like 'Snacks' or 'Dairy'.")
        else:
            st.write(f"Found {len(results)} items matching '{search_query}' (and synonyms)")
            for index, row in results.iterrows():
                ing_list = str(row['Ingredients'])
                sugar_g = row['Total Sugar (g)']
                salt_g = row['Salt (g)']
                fat_g = row['Fat (g)']
                
                # --- LOGIC CORE ---
                found_dangers = []
                warnings = []
                
                # 1. Ingredient Scan
                for bad in banned_ingredients:
                    if bad.lower() in ing_list.lower():
                        if bad.lower() == "salt":
                            if salt_g > 1.5:
                                found_dangers.append(f"High Salt ({salt_g}g)")
                            else:
                                warnings.append(f"Contains Salt ({salt_g}g)")
                        elif bad in FILTER_PACKS["Added Sugar & Syrups"]:
                            if sugar_g > 5:
                                found_dangers.append(f"{bad} (High)")
                            else:
                                warnings.append(f"Contains {bad} ({sugar_g}g)")
                        elif bad in FILTER_PACKS["High Natural Sugars (>15g)"]:
                            continue 
                        else:
                            found_dangers.append(bad)
                
                # 2. High Natural Sugar Logic (15g Rule)
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
                        st.image(img_link, width=80)
                    with col_info:
                        st.markdown(f"**{row['Product']}**")
                        st.caption(f"{row['Brand']} | {row['Price']}")
                        
                        st.markdown(f"""
                        <div class="nutrition-row">
                        🍬 <b>Sugar:</b> {sugar_g}g &nbsp;|&nbsp; 
                        🧂 <b>Salt:</b> {salt_g}g &nbsp;|&nbsp; 
                        🥓 <b>Fat:</b> {fat_g}g
                        </div>
                        """, unsafe_allow_html=True)

                        if is_safe:
                            if warnings:
                                st.markdown('<span class="warning-tag">⚠️ CHECK LABEL</span>', unsafe_allow_html=True)
                                st.caption(f"Allowed (Low Dose): {', '.join(warnings)}")
                            else:
                                st.markdown('<span class="safe-tag">✅ SAFE FOR YOU</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="avoid-tag">❌ AVOID</span>', unsafe_allow_html=True)
                            st.markdown(f":red[**Reason:** {', '.join(found_dangers)}]")
                        
                        with st.expander("Ingredients"):
                            st.write(ing_list)
                    with col_action:
                        if is_safe:
                            if st.button("🛒 Add", key=f"add_{index}"):
                                st.session_state['basket'].append(row)
                                st.toast("Added!")
                        else:
                            st.button("🚫 Unsafe", disabled=True, key=f"bad_{index}")
                    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2, 3, 4, 5 (Same as before) ---
with tab2:
    st.markdown("### 🧠 The Gut-Brain Connection")
    st.info("Did you know that 95% of your serotonin (the happiness hormone) is produced in your gut?")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown("**Why Gut Health Matters**\nModern research connects our gut microbiome to everything from **ADHD in children** to immunity and mental health in adults.\nThe food chain has changed. Emulsifiers, preservatives, and artificial dyes disrupt the gut lining, leading to inflammation.")
    with col_n2:
        st.markdown("**The ADHD Link**\nStudies suggest that certain artificial colours (like Red 40 and Yellow 5) and preservatives (like Sodium Benzoate) can exacerbate hyperactivity in children.\n\n**Our Mission**\nWe built this tool because we believe consciousness is the first step to health.")

with tab3:
    st.markdown("### 🎯 Aim of the Game")
    st.markdown("We reduce 'Label Fatigue' by scanning for hundreds of hidden ingredients so you don't have to.")
    
    st.divider()
    st.markdown("### 🚦 How to Read Results")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("✅ SAFE FOR YOU")
        st.caption("Clean. No filters detected.")
    with c2:
        st.warning("⚠️ WARNING / CHECK LABEL")
        st.caption("Contains a filter (e.g. Salt, Sugar) but in **LOW** amounts. Safe for most, but depends on your personal tolerance.")
    with c3:
        st.error("❌ AVOID")
        st.caption("Contains high amounts of filters or dangerous allergens.")
    st.divider()
    
    st.subheader("🔍 Filter Glossary")
    for category, ingredients in FILTER_PACKS.items():
        with st.expander(f"📦 {category}"):
            if "Added Sugar" in category:
                 st.info("⚠️ **Smart Scan:** If a product contains added sugar but the total is **< 5g (Low)**, we will warn you but not ban it. Above 5g, we flag it as Avoid.")
            if "High Natural Sugars" in category:
                 st.info("⚠️ **Health Note:** Even natural sugars (date syrup, fruit concentrates) spike insulin. We allow up to **15g** (natural). Above that, we flag as Avoid.")
            if "Sodium" in category:
                 st.info("⚠️ **Medical Standard:** We follow the NHS 'Traffic Light' system. Products with **>1.5g of Salt** are flagged as High. Lower amounts show a Warning.")
            if "Inflammatory Oils" in category:
                 st.info("⚠️ **Strict Policy:** Food labels don't list exact oil amounts. Since cheap oils (Palm, Sunflower) are often used as the main cooking medium (e.g. in chips), even a 'small' mention usually means a high dose. We flag ANY presence.")
            if "Artificial Sweeteners" in category:
                 st.info("⚠️ **Metabolic Health:** We have a Zero Tolerance policy. Sweeteners like Aspartame and Sucralose can disrupt the gut microbiome and trigger insulin responses, even if they are '0 Calories'.")
            if "Artificial Colours" in category:
                 st.info("⚠️ **Hyperactivity:** We specifically target dyes like Red 40, Yellow 5, and Blue 1 (The 'Southampton Six'), which are linked to hyperactivity in children.")
            if "Gut Irritants" in category:
                 st.info("⚠️ **Gut Lining:** Emulsifiers (like Carrageenan and Gums) thicken food but can strip the protective mucus layer of the gut. We flag these for digestive sensitivity.")
            st.write(", ".join(ingredients))
            
    st.markdown("""
    <div class="disclaimer-box">
    <b>⚠️ DISCLAIMER:</b><br>
    The content on Pure Dubai is for informational purposes only. We are not professional nutritionists or medical doctors. 
    Product ingredients are subject to change by manufacturers at any time. 
    While we strive for accuracy, we rely on data provided by suppliers and cannot guarantee that every product is free from traces of allergens. 
    <b>Always read the physical label on the product before consumption.</b>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    if not st.session_state['wishlist']:
        st.info("No favorites yet.")
    else:
        for idx, item in enumerate(st.session_state['wishlist']):
            st.markdown(f"**{item['Product']}**")
            if st.button(f"Move to Basket", key=f"move_{idx}"):
                st.session_state['basket'].append(item)
                st.session_state['wishlist'].pop(idx)
                st.rerun()
            st.divider()

with tab5:
    if not st.session_state['basket']:
        st.info("Basket is empty.")
    else:
        for item in st.session_state['basket']:
            st.markdown(f"✅ **{item['Product']}** - {item['Brand']} ({item['Price']})")
        st.divider()
        st.markdown("**Option 1: Send to Partner**")
        export_text = "Hi! Order these:\n" + "\n".join([f"- {i['Product']}" for i in st.session_state['basket']])
        st.text_area("Copy Text:", value=export_text, height=150)

