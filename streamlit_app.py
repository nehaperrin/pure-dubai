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
    
    .disclaimer-box {
        font-size: 12px;
        color: #777;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
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
        "Diane (Toddler Safe)": ["Added Sugar & Syrups", "High Natural Sugars (>15g)", "Artificial Colors", "Inflammatory Oils"],
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
    "Artificial Colors": ["red 40", "yellow 5", "blue 1", "e102", "e110", "e129", "e133", "tartrazine"],
    "Gut Irritants & Emulsifiers": ["carrageenan", "xanthan gum", "guar gum", "lecithin", "polysorbate", "cellulose gum"],
    "Preservatives": ["benzoate", "sorbate", "nitrate", "nitrite", "sulfite", "bha", "bht"],

    # ALLERGIES & DIET
    "Tree Nuts & Peanuts": ["peanut", "almond", "cashew", "walnut", "pecan", "hazelnut", "pistachio", "macadamia"],
    "Sesame & Seeds": ["sesame", "tahini", "sunflower seed", "poppy seed"],
    "Dairy / Lactose": ["milk", "lactose", "whey", "casein", "butter", "cream", "yogurt", "cheese"],
    "Gluten / Wheat": ["wheat", "barley", "rye", "malt", "brewer's yeast"],
    "Soy": ["soy", "edamame", "tofu", "lecithin"],
    "Shellfish": ["shrimp", "crab", "lobster", "prawn", "shellfish"],
    "Sodium & Salt Watch": ["salt", "sodium", "monosodium", "baking soda", "brine", "msg"],
    "Inflammatory Oils": ["palm oil", "canola oil", "rapeseed oil", "sunflower oil", "soybean oil", "vegetable oil", "hydrogenated", "margarine"]
}

# --- 4. REAL DATABASE LOADING ---
@st.cache_data
def load_data():
    try:
        # Load the CSV
        df = pd.read_csv("products.csv")
        # Ensure Total Sugar is a number
        df['Total Sugar (g)'] = pd.to_numeric(df['Total Sugar (g)'], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        return pd.DataFrame([{"Product": "Error", "Brand": "System", "Price": "0", "Category": "Error", "Ingredients": "Please upload products.csv to GitHub", "Total Sugar (g)": 0, "Image": ""}])

df = load_data()



# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", width=60)
    
    # --- STEP 1: MODE SWITCHER ---
    st.markdown("### 1. Start Shopping")
    shopping_mode = st.radio("How do you want to filter?", ["🖐️ Manual Selection", "👤 Use Saved Profile"], label_visibility="collapsed")
    
    # --- STEP 2: DYNAMIC FILTERING ---
    active_filters = []
    
    if shopping_mode == "🖐️ Manual Selection":
        st.markdown("**Select filters manually:**")
        active_filters = st.multiselect("Avoiding:", options=list(FILTER_PACKS.keys()))
        
    else: # Saved Profile Mode
        st.markdown("**Choose a profile:**")
        profile_names = list(st.session_state['profiles'].keys())
        selected_profile = st.selectbox("Select:", profile_names, index=0)
        
        # Load the filters from the profile
        current_defaults = st.session_state['profiles'][selected_profile]
        st.markdown(f"**{selected_profile} avoids:**")
        st.multiselect("Avoiding:", options=list(FILTER_PACKS.keys()), default=current_defaults, disabled=True)
        active_filters = current_defaults

    st.divider()

    # --- STEP 3: CREATE PROFILE ---
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

# Flatten the active filters into a list of banned ingredients
banned_ingredients = []
for pack in active_filters:
    banned_ingredients.extend(FILTER_PACKS[pack])

# --- 6. MAIN CONTENT ---

col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/9355/9355325.png", width=80)
with col_title:
    st.title("Pure Dubai")
    st.caption("SEARCH ONCE. SAFE EVERYWHERE.")

# THE FOUNDER STORY
with st.expander("❤️ From the Founder", expanded=True):
    st.markdown("""
    <div class="founder-box">
        <div class="founder-text">
        Hi, I'm Neha. A Dubai 80s kid, a recovering London banker, and a mom of two.<br><br>
        I created Pure Dubai to solve the 'Dubai Paradox': too many choices, not enough time.<br>
        And I created it to make your life of online grocery shopping much easier.<br><br>
        In today's world of free-from and healthy options, there are still way too many hidden ingredients. 
        Moving back to Dubai with a food allergy child made the weekly shop a nightmare, so I built a solution. 
        <b>Pure Dubai isn't just an analyzer; it’s a scout.</b> We don't just scan your existing pantry; we help you find exactly what you need—clean, safe, and specific—across Dubai’s retailers in seconds.<br><br>
        I hope this helps you as much as it helped me.
        <div class="founder-sig">xo Neha</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Search Engine", "📚 News & Research", "ℹ️ How it Works", "❤️ Saved", "🛒 Basket"])

# --- TAB 1: SEARCH ---
with tab1:
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search_query = st.text_input("Search Ingredients or Products...", placeholder="e.g. Fade Fit, Pasta, Kids...")
    with col_s2:
        st.write("")
        st.write("")
        search_btn = st.button("Search", type="primary", use_container_width=True)

    if search_query or search_btn:
        # Search in the real dataframe
        results = df[df['Product'].str.contains(search_query, case=False, na=False) | df['Brand'].str.contains(search_query, case=False, na=False) | df['Category'].str.contains(search_query, case=False, na=False)]
        
        if results.empty:
            st.warning("No matches found. Try 'Fade Fit' or 'Barilla'.")
        else:
            st.write(f"Found {len(results)} items matching '{search_query}'")
            for index, row in results.iterrows():
                ing_list = str(row['Ingredients'])
                total_sugar = row['Total Sugar (g)']
                
                # 1. Text Search for Bad Ingredients
                found_dangers = [bad for bad in banned_ingredients if bad.lower() in ing_list.lower()]
                
                # 2. Logic Check for Natural Sugars (>15g)
                if "High Natural Sugars (>15g)" in active_filters:
                    # Only flag if >15g sugar AND contains natural sugar keywords
                    natural_keywords = FILTER_PACKS["High Natural Sugars (>15g)"]
                    has_natural_ingredients = any(k in ing_list.lower() for k in natural_keywords)
                    
                    if has_natural_ingredients and total_sugar > 15:
                        found_dangers.append(f"High Sugar ({total_sugar}g)")

                is_safe = len(found_dangers) == 0
                
                with st.container():
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    col_img, col_info, col_action = st.columns([1, 3, 1])
                    with col_img:
                        img_link = row['Image'] if pd.notna(row['Image']) and row['Image'].startswith('http') else "https://cdn-icons-png.flaticon.com/512/3081/3081967.png"
                        st.image(img_link, width=80)
                    with col_info:
                        st.markdown(f"**{row['Product']}**")
                        st.caption(f"{row['Brand']} | {row['Price']} | Sugar: {total_sugar}g")
                        if is_safe:
                            st.markdown('<span class="safe-tag">✅ SAFE FOR YOU</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="avoid-tag">❌ AVOID</span>', unsafe_allow_html=True)
                            st.markdown(f":red[**Contains:** {', '.join(found_dangers)}]")
                        with st.expander("Ingredients"):
                            st.write(ing_list)
                    with col_action:
                        if is_safe:
                            if st.button("🛒 Add", key=f"add_{index}"):
                                st.session_state['basket'].append(row)
                                st.toast("Added!")
                            if st.button("❤️ Save", key=f"fav_{index}"):
                                st.session_state['wishlist'].append(row)
                                st.toast("Saved!")
                        else:
                            st.button("🚫 Unsafe", disabled=True, key=f"bad_{index}")
                    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: NEWS & RESEARCH ---
with tab2:
    st.markdown("### 🧠 The Gut-Brain Connection")
    st.info("Did you know that 95% of your serotonin (the happiness hormone) is produced in your gut?")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown("**Why Gut Health Matters**\nModern research connects our gut microbiome to everything from **ADHD in children** to immunity and mental health in adults.\nThe food chain has changed. Emulsifiers, preservatives, and artificial dyes disrupt the gut lining, leading to inflammation.")
    with col_n2:
        st.markdown("**The ADHD Link**\nStudies suggest that certain artificial colors (like Red 40 and Yellow 5) and preservatives (like Sodium Benzoate) can exacerbate hyperactivity in children.\n\n**Our Mission**\nWe built this tool because we believe consciousness is the first step to health.")

# --- TAB 3: HOW IT WORKS & GLOSSARY (UPDATED) ---
with tab3:
    st.markdown("### 🎯 Aim of the Game")
    st.markdown("We reduce 'Label Fatigue' by scanning for hundreds of hidden ingredients so you don't have to.")
    
    st.info("💡 **Pro Tip:** You can customize your filters each time! Saved profiles are just there to make your life easier.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("#### 1. Set Profile or Edit Filters")
        st.caption("Choose your filters manually, create a new profile, or pick a saved profile like 'Max (Allergy)' or 'Grandpa (Heart)' from the sidebar.")
    with c2:
        st.caption("#### 2. Search")
        st.caption("Type 'Fade Fit' or 'Barilla'. We scan ingredients against your profile or your active filters.")
    with c3:
        st.caption("#### 3. Shop Safe")
        st.caption("Add safe items to your basket and export the list to your retailer.")

    st.divider()
    st.subheader("🔍 Filter Glossary: What are we scanning for?")
    st.markdown("Click below to see exactly which ingredients are hidden inside each filter.")
    
    for category, ingredients in FILTER_PACKS.items():
        with st.expander(f"📦 {category}"):
            # Special explanation for High Natural Sugars
            if "High Natural Sugars" in category:
                 st.info("⚠️ **Health Note:** Even natural sugars (like date syrup or fruit concentrates) can spike insulin. We flag products with **>15g of sugar per serving** because high natural sugar intake should be monitored for diabetic concerns and weight loss.")
            st.write(", ".join(ingredients))

    st.divider()
    st.markdown("""
    <div class="disclaimer-box">
    <b>⚠️ DISCLAIMER:</b><br>
    The content on Pure Dubai is for informational purposes only. We are not professional nutritionists or medical doctors. 
    Product ingredients are subject to change by manufacturers at any time. 
    While we strive for accuracy, we rely on data provided by suppliers and cannot guarantee that every product is free from traces of allergens. 
    <b>Always read the physical label on the product before consumption.</b>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 4 & 5 (Favorites & Basket) ---
with tab4:
    if not st.session_state['wishlist']:
        st.info("No favorites yet.")
    else:
        for idx, item in enumerate(st.session_state['wishlist']):
            st.markdown(f"**{item['Product']}** ({item['Brand']})")
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
        export_text = "Hi! Please order these safe items:\n" + "\n".join([f"- {i['Product']} ({i['Brand']})" for i in st.session_state['basket']])
        st.text_area("Copy Text:", value=export_text, height=150)
