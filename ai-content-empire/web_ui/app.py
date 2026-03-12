import streamlit as st
import os
import json
import yaml
import asyncio
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

# Use wide layout
st.set_page_config(page_title="ACE Control Center", layout="wide", page_icon="👑")

# Update working directory to project root if running from web_ui
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if os.getcwd() != project_root:
    os.chdir(project_root)

# Load config and DB
@st.cache_resource
def get_supabase():
    try:
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        supabase_url = config.get('supabase_url')
        supabase_key = config.get('supabase_anon_key')
        if supabase_url and supabase_key:
            return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.sidebar.error(f"DB Connect Error: {e}")
    return None

db = get_supabase()

def load_characters():
    bibles_dir = os.path.join(project_root, 'content', 'character_bibles')
    characters = []
    if os.path.exists(bibles_dir):
        for f in os.listdir(bibles_dir):
            if f.endswith('.json'):
                path = os.path.join(bibles_dir, f)
                try:
                    with open(path, 'r') as file:
                        c_data = json.load(file).get('character', {})
                        characters.append((f, c_data))
                except Exception:
                    pass
    return characters

st.title("👑 AI Content Empire (ACE) - Control Center")

tab_dash, tab_studio, tab_setup, tab_queue, tab_atlas = st.tabs([
    "📊 Dashboard", 
    "🎭 Character Studio", 
    "🔗 Account Setup", 
    "🕒 Content Queue", 
    "🤖 Chat with Atlas"
])

# --- DASHBOARD TAB ---
with tab_dash:
    st.header("Platform Overview")
    if db:
        # Mocking Dashboard Data for UI visualization when db is empty
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Active Influencers", len(load_characters()))
        col2.metric("Today's Projected Content", "12 items")
        col3.metric("Est. Daily Revenue", "$145.50", "+12%")
        
        st.subheader("Revenue by Platform (Simulation)")
        data = pd.DataFrame({
            "Platform": ["OnlyFans", "X (Twitter)", "TikTok", "Affiliate"],
            "Revenue": [1200, 300, 450, 150]
        })
        fig = px.pie(data, values="Revenue", names="Platform", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Database not connected. Please check config.yaml.")

# --- CHARACTER STUDIO TAB ---
with tab_studio:
    st.header("Character Studio")
    chars = load_characters()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Active Influencers")
        for fname, cdata in chars:
            st.button(cdata.get('name', fname.split('.')[0]).capitalize(), key=f"btn_{fname}")
            
    with col2:
        st.subheader("Create / Edit Persona")
        with st.form("character_form"):
            c_name = st.text_input("Character Name")
            c_style = st.selectbox("Content Style", ["flirty", "professional", "tech", "fitness", "lifestyle"])
            c_is_nsfw = st.checkbox("Allow NSFW Content (Requires uncensored models)", value=False)
            c_traits = st.text_area("Personality Traits (comma separated)")
            c_visuals = st.text_area("Visual Identity (Prompt modifiers for Pixel)")
            
            submit = st.form_submit_button("Save Character")
            if submit and c_name:
                new_char = {
                    "character": {
                        "name": c_name.lower(),
                        "style": c_style,
                        "is_nsfw": c_is_nsfw,
                        "personality": {"traits": [t.strip() for t in c_traits.split(",")]},
                        "visual_identity": c_visuals
                    }
                }
                bibles_dir = os.path.join(project_root, 'content', 'character_bibles')
                os.makedirs(bibles_dir, exist_ok=True)
                path = os.path.join(bibles_dir, f"{c_name.lower()}.json")
                with open(path, 'w') as f:
                    json.dump(new_char, f, indent=4)
                st.success(f"Saved {c_name}!")
                st.rerun()

# --- ACCOUNT SETUP TAB ---
with tab_setup:
    st.header("Guided Account Setup Wizard")
    st.write("Use this wizard to manually configure and store social media handles for your AI Influencers, avoiding automated bot detection.")
    
    chars = load_characters()
    char_names = [c[1].get('name', c[0].split('.')[0]).capitalize() for c in chars]
    
    if not char_names:
        st.info("Please create a character in the Character Studio first.")
    else:
        selected_char_name = st.selectbox("Select Influencer to Setup", char_names)
        # Find the actual char data
        selected_char_data = None
        selected_char_file = None
        for fname, cdata in chars:
            if cdata.get('name', fname.split('.')[0]).capitalize() == selected_char_name:
                selected_char_data = cdata
                selected_char_file = fname
                break
                
        if selected_char_data:
            socials = selected_char_data.get("socials", {})
            
            st.markdown("### Step-by-Step Creation Guide")
            with st.expander("Step 1: Create an Email Account", expanded=True):
                st.write(f"1. Go to ProtonMail or Gmail.\n2. Create an email like `{selected_char_name.lower()}_ai@proton.me`.")
                
            with st.expander("Step 2: Create a Twitter / X Account"):
                st.write("1. Use an anti-detect browser or a fresh mobile device if possible.\n2. Create a Twitter account using the email from Step 1.\n3. Verify via SMS if prompted.")
                
            with st.expander("Step 3: Create a TikTok Account"):
                st.write("1. Create a TikTok account using a mobile device (requires app for best results).\n2. Sync contacts OFF, link to the email from Step 1.")
                
            st.markdown("### Store Handles")
            with st.form("socials_form"):
                x_handle = st.text_input("X (Twitter) Handle", value=socials.get("x", ""))
                tiktok_handle = st.text_input("TikTok Handle", value=socials.get("tiktok", ""))
                onlyfans_handle = st.text_input("OnlyFans Handle", value=socials.get("onlyfans", ""))
                email_address = st.text_input("Recovery Email", value=socials.get("email", ""))
                
                save_socials = st.form_submit_button("Save Connected Accounts")
                if save_socials:
                    # Update JSON
                    bibles_dir = os.path.join(project_root, 'content', 'character_bibles')
                    path = os.path.join(bibles_dir, selected_char_file)
                    
                    # Read current
                    with open(path, 'r') as f:
                        full_data = json.load(f)
                        
                    full_data['character']['socials'] = {
                        "x": x_handle,
                        "tiktok": tiktok_handle,
                        "onlyfans": onlyfans_handle,
                        "email": email_address
                    }
                    
                    with open(path, 'w') as f:
                        json.dump(full_data, f, indent=4)
                        
                    st.success("Successfully linked accounts to persona profile!")
                    st.rerun()

# --- CONTENT QUEUE TAB ---
with tab_queue:
    st.header("Content Approval Queue")
    st.info("This feature will integrate directly with Nova and Pixel output before Echo publishes.")
    
    # Mock visual of a queue
    st.markdown("""
    | Status | Character | Platform | Time | Text | Image |
    |---|---|---|---|---|---|
    | 🟡 Pending | Luna | X (Twitter) | 14:00 | 'Just finished my morning run! 🏃‍♀️✨' | [View Image] |
    | 🟢 Approved | Luna | OnlyFans | 18:00 | 'New exclusive set dropping tonight... 🤫' | [View Image] |
    | 🔴 Rejected | Zoe | TikTok | 15:30 | 'Reviewing the new mechanical keyboard...' | [View Image] |
    """)

# --- CHAT WITH ATLAS TAB ---
with tab_atlas:
    st.header("Chat with Atlas (Manager Agent)")
    st.write("Give high-level directives to the ACE Task Force.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command Atlas (e.g., 'Pause Luna's X account today')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Mocking Atlas response for now until full LLM integration
        response = f"Atlas: Acknowledged directive '{prompt}'. Updating task queue and informing Echo and Nova."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
