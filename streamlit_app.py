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
        "Diane (Toddler Safe)": ["Added Sugar & Syrups", "Artificial Colors", "Inflammatory Oils"],
        "Grandpa (Heart Health)": ["Sodium & Salt Watch", "Inflammatory Oils", "Added Sugar & Syrups"],
        "Clean Eating (Gut Health)": ["Gut Irritants & Emulsifiers", "Artificial Sweeteners", "Inflammatory Oils"]
    }

if 'active_profile' not in st.session_state:
    st.session_state['active_profile'] = list(st.session_state['profiles'].keys())[0]

# --- 3. FILTER DEFINITIONS ---
FILTER_PACKS = {
    # KIDS & SUGAR
    "Added Sugar & Syrups": ["sugar", "sucrose", "glucose", "fructose", "corn syrup", "dextrose", "maltodextrin", "agave", "honey", "caramel"],
    "Artificial Sweeteners": ["aspartame", "sucralose", "saccharin", "acesulfame", "neotame"],
    "Artificial Colors": ["red 40", "yellow 5", "blue 1", "e102", "e110", "e129", "e133", "tartrazine"],

    # ALLERGIES
    "Tree Nuts & Peanuts": ["peanut", "almond", "cashew", "walnut", "pecan", "hazelnut", "pistachio", "macadamia"],
    "Sesame & Seeds": ["sesame", "tahini", "sunflower seed", "poppy seed"],
    "Dairy / Lactose": ["milk", "lactose", "whey", "casein", "butter", "cream", "yogurt", "cheese"],
    "Gluten / Wheat": ["wheat", "barley", "rye", "malt", "brewer's yeast"],
    "Soy": ["soy", "edamame", "tofu", "lecithin"],
    "Shellfish": ["shrimp", "crab", "lobster", "prawn", "shellfish"],

    # HEALTH & LIFESTYLE
    "Sodium & Salt Watch": ["salt", "sodium", "monosodium", "baking soda", "brine", "msg"],
    "Inflammatory Oils": ["palm oil", "canola oil", "rapeseed oil", "sunflower oil", "soybean oil", "vegetable oil", "hydrogenated", "margarine"],
    "Gut Irritants & Emulsifiers": ["carrageenan", "xanthan gum", "guar gum", "lecithin", "polysorbate", "cellulose gum"],
    "Preservatives": ["benzoate", "sorbate", "nitrate", "nitrite", "sulfite", "bha", "bht"]
}






# --- 4. MOCK DATABASE ---
def get_mock_database():
    return pd.DataFrame([
        {"Product": "Bear YoYo Strawberry", "Brand": "Kibsons", "Price": "25 AED", "Category": "Snacks", "Ingredients": "Apples, Pears, Strawberries, Black Carrot Extract", "Image": "https://cdn-icons-png.flaticon.com/512/3081/3081967.png"},
        {"Product": "Fade Fit Kids Cocoa", "Brand": "Carrefour", "Price": "12 AED", "Category": "Snacks", "Ingredients": "Dates, Cocoa Powder, Hazelnut", "Image": "https://cdn-icons-png.flaticon.com/512/3050/3050268.png"},
        {"Product": "Hunter's Gourmet Chips", "Brand": "Spinneys", "Price": "15 AED", "Category": "Pantry", "Ingredients": "Potatoes, Sunflower Oil, Truffle Flavor, MSG, E621, Salt", "Image": "https://cdn-icons-png.flaticon.com/512/2553/2553691.png"},
        {"Product": "Almarai Strawberry Milk", "Brand": "Union Coop", "Price": "8 AED", "Category": "Dairy", "Ingredients": "Fresh Cow's Milk, Sugar, Red 40, Artificial Flavor, Carrageenan", "Image": "https://cdn-icons-png.flaticon.com/512/9708/9708548.png"},
        {"Product": "Kibsons Organic Hummus", "Brand": "Kibsons", "Price": "18 AED", "Category": "Fridge", "Ingredients": "Chickpeas, Tahini (Sesame), Lemon Juice, Sea Salt", "Image": "https://cdn-icons-png.flaticon.com/512/8743/8743994.png"},
        {"Product": "Oreo Original", "Brand": "Carrefour", "Price": "5 AED", "Category": "Treats", "Ingredients": "Wheat Flour, Sugar, Palm Oil, Cocoa, Glucose-Fructose Syrup", "Image": "https://cdn-icons-png.flaticon.com/512/541/541732.png"},
        {"Product": "RxBar Chocolate Sea Salt", "Brand": "Spinneys", "Price": "12 AED", "Category": "Snacks", "Ingredients": "Dates, Egg Whites, Cashews, Almonds, Cacao, Sea Salt", "Image": "https://cdn-icons-png.flaticon.com/512/1792/1792947.png"},
        {"Product": "Campbell's Tomato Soup", "Brand": "Waitrose", "Price": "10 AED", "Category": "Pantry", "Ingredients": "Tomato Puree, High Fructose Corn Syrup, Wheat Flour, Salt, Potassium Chloride", "Image": "https://cdn-icons-png.flaticon.com/512/2405/2405451.png"},
    ])

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", width=60)

    # Profile Selection
    st.markdown("### 👤 Select Profile")
    profile_names = list(st.session_state['profiles'].keys())
    if st.session_state['active_profile'] not in profile_names:
        st.session_state['active_profile'] = profile_names[0]

    selected_profile = st.selectbox("Who are we shopping for?", profile_names, index=profile_names.index(st.session_state['active_profile']))
    st.session_state['active_profile'] = selected_profile

    st.divider()
    st.markdown(f"### 🛡️ Filters: {selected_profile.split('(')[0]}")

    current_defaults = st.session_state['profiles'][selected_profile]
    active_filters = st.multiselect("Avoiding:", options=list(FILTER_PACKS.keys()), default=current_defaults)

    st.divider()
    with st.expander("➕ Create New Profile"):
        new_name = st.text_input("Name (e.g. Grandma)")
        new_defaults = st.multiselect("Select Filters", options=list(FILTER_PACKS.keys()))
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
        I created Pure Dubai to solve the 'Dubai Paradox': too many choices, not enough time. In today's world of free-from and healthy groceries, there are still way too many hidden ingredients.<br><br>
        Moving back to Dubai with a food allergy child made the weekly shop a nightmare, so I built a solution. <b>Pure Dubai isn't just an analyzer; it’s a scout.</b> We don't just scan your existing pantry; we help you find exactly what you need—clean, safe, and specific—across Dubai’s retailers in seconds.
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
        search_query = st.text_input("Search Ingredients or Products...", placeholder="e.g. Chips, Soup, Snacks...")
    with col_s2:
        st.write("")
        st.write("")
        search_btn = st.button("Search", type="primary", use_container_width=True)

    if search_query or search_btn:
        df = get_mock_database()
        results = df[df['Product'].str.contains(search_query, case=False) | df['Category'].str.contains(search_query, case=False)]

        if results.empty:
            st.warning("No matches found. Try 'Soup' or 'Snacks'.")
        else:
            st.write(f"Found {len(results)} items matching '{search_query}'")
            for index, row in results.iterrows():
                ing_list = row['Ingredients']
                found_dangers = [bad for bad in banned_ingredients if bad.lower() in ing_list.lower()]
                is_safe = len(found_dangers) == 0

                with st.container():
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    col_img, col_info, col_action = st.columns([1, 3, 1])
                    with col_img:
                        st.image(row['Image'], width=80)
                    with col_info:
                        st.markdown(f"**{row['Product']}**")
                        st.caption(f"{row['Brand']} | {row['Price']}")
                        if is_safe:
                            st.markdown('<span class="safe-tag">✅ SAFE FOR YOU</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="avoid-tag">❌ AVOID</span>', unsafe_allow_html=True)
                            st.markdown(f":red[**Contains:** {', '.join(found_dangers)}]")
                        with st.expander("Ingredients"):
                            st.write(row['Ingredients'])
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

# --- TAB 3: HOW IT WORKS & GLOSSARY (FIXED) ---
with tab3:
    st.markdown("### 🎯 Aim of the Game")
    st.markdown("We reduce 'Label Fatigue' by scanning for hundreds of hidden ingredients so you don't have to.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 1. Set Profile")
        st.caption("Choose 'Max (Allergy)' or 'Grandpa (Heart)' from the sidebar.")
    with c2:
        st.markdown("#### 2. Search")
        st.caption("Type 'Chips' or 'Yogurt'. We scan ingredients against your profile.")
    with c3:
        st.markdown("#### 3. Shop Safe")
        st.caption("Add safe items to your basket and export the list to your retailer.")

    st.divider()
    st.subheader("🔍 Filter Glossary: What are we scanning for?")
    st.markdown("Click below to see exactly which ingredients are hidden inside each filter.")

    for category, ingredients in FILTER_PACKS.items():
        with st.expander(f"📦 {category}"):
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

# --- TAB 4: FAVORITES ---
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

# --- TAB 5: BASKET ---
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
