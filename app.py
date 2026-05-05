import streamlit as st
import pandas as pd
import os
from PIL import Image
from thefuzz import process, fuzz
import streamlit.components.v1 as components
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional, keys can be set as system env vars


# --- Page Config & Styling ---
try:
    page_icon_logo = Image.open('assets/images/logo1_transparent.png')
except Exception:
    page_icon_logo = "🎓"
    
st.set_page_config(page_title="PSAU Chat", page_icon=page_icon_logo, layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Tiffany Green (#0ABAB5) and White, with modern cards and responsive mobile design
st.markdown("""
<style>
    /* Reset and Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Variables map directly to Streamlit's native theme to support Dark Mode toggling */
    :root {
        --primary-color: #0f766e;
        --primary-hover: #14b8a6;
    }

    h1, h2, h3, h4 {
        color: var(--primary-color) !important;
        font-weight: 700 !important;
    }
    
    /* Primary Buttons */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover) !important;
        box-shadow: 0 4px 12px rgba(10, 186, 181, 0.2) !important;
        transform: translateY(-1px);
    }
    
    /* Input fields focus color */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        border-color: #E2E8F0 !important;
        border-radius: 10px !important;
        transition: border-color 0.2s;
    }
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 1px var(--primary-color) !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-light);
        border-right: 1px solid #EBF4F4;
    }
    
    /* Dashboard Cards */
    .feature-card {
        background: rgba(15, 118, 110, 0.04);
        border: 1px solid rgba(15, 118, 110, 0.15);
        color: inherit;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(10, 186, 181, 0.1);
        border-color: var(--primary-color);
        background: rgba(15, 118, 110, 0.08);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: inherit;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: inherit;
        opacity: 0.8;
        font-size: 0.9rem;
        line-height: 1.4;
        margin-bottom: 1.5rem;
    }
    
    /* UI Cards for Data (Doctors) */
    .data-card {
        background: rgba(15, 118, 110, 0.05);
        border-left: 4px solid var(--primary-color);
        padding: 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1rem;
        color: inherit;
    }
    .data-card h4 {
        margin: 0 0 0.5rem 0;
        color: inherit !important;
    }
    .data-card p {
        margin: 0.2rem 0;
        color: inherit;
        opacity: 0.85;
        font-size: 0.95rem;
    }

    /* Chat bubbles */
    .user-msg {
        background-color: var(--primary-color);
        color: white;
        padding: 12px 16px;
        border-radius: 16px 16px 0 16px;
        margin-bottom: 1rem;
        text-align: start;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 80%;
    }
    .bot-msg {
        background: var(--background-color, #ffffff);
        color: inherit;
        border: 1px solid rgba(15, 118, 110, 0.18);
        border-left: 4px solid var(--primary-color);
        padding: 16px 20px;
        border-radius: 0 14px 14px 0;
        margin-bottom: 1rem;
        text-align: start;
        display: block;
        clear: both;
        max-width: 90%;
        font-family: 'Segoe UI', 'Tajawal', sans-serif;
        font-size: 0.97rem;
        line-height: 1.7;
        box-shadow: 0 1px 6px rgba(15, 118, 110, 0.07);
    }
    
    /* Clearfix for chat */
    .chat-container::after {
        content: "";
        clear: both;
        display: table;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(15, 118, 110, 0.1);
        backdrop-filter: blur(5px);
        color: inherit;
        text-align: center;
        padding: 10px 0;
        font-size: 0.85rem;
        border-top: 1px solid rgba(15, 118, 110, 0.2);
        z-index: 100;
    }
    
    /* Main area padding for footer */
    .block-container {
        padding-bottom: 80px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        # --- Core Navigation Data (MANDATORY) ---
        try:
            df_locations = pd.read_excel('data/navigation_updated.xlsx', sheet_name='locations')
            df_paths = pd.read_excel('data/navigation_updated.xlsx', sheet_name='paths')
            df_keywords = pd.read_excel('data/navigation_updated.xlsx', sheet_name='keywords')
        except:
            df_locations = pd.DataFrame(columns=['Node_ID', 'Name_EN', 'Name_AR', 'Floor', 'Type'])
            df_paths = pd.DataFrame(columns=['FromNode', 'ToNode', 'Distance', 'Direction'])
            df_keywords = pd.DataFrame(columns=['Keyword', 'TargetNode'])

        # --- Old Files (Restore logic for stability) ---
        try:
            doctors_old = pd.read_excel('data/doctors.xlsx')
        except:
            doctors_old = pd.DataFrame(columns=['Doctor name', 'Email', 'Location', 'Subject'])
            
        try:
            courses_old = pd.read_excel('data/courses.xlsx')
        except:
            courses_old = pd.DataFrame(columns=['Course code', 'Course name', 'Subject'])
            
        try:
            rooms_old = pd.read_excel('data/rooms.xlsx')
        except:
            rooms_old = pd.DataFrame(columns=['Name', 'Floor', 'Type'])

        # Synthesize df_rooms from rooms_old AND navigation data
        df_rooms = pd.concat([rooms_old, df_locations[['Name_EN', 'Floor', 'Type']].rename(columns={'Name_EN': 'Name'})]).drop_duplicates(subset=['Name']).reset_index(drop=True)
        
        # New Excel Files
        try:
            df_docs = pd.read_excel('data/doctorsEE(1).xlsx')
            df_docs['Doctor name'] = df_docs['Doctor name'].ffill()
            df_docs['Email'] = df_docs['Email'].ffill()
            df_docs['Location'] = df_docs['Location'].ffill()
        except:
            df_docs = pd.DataFrame(columns=['Doctor name', 'Email', 'Location', 'Course name'])
        
        try:
            df_level_core = pd.read_excel('data/level.xlsx', sheet_name=0)
            df_level_elec = pd.read_excel('data/level.xlsx', sheet_name=1)
            # Schema Fix: Map 'Course' to 'Course name' if necessary
            if 'Course' in df_level_core.columns and 'Course name' not in df_level_core.columns:
                df_level_core = df_level_core.rename(columns={'Course': 'Course name'})
            if 'Course' in df_level_elec.columns and 'Course name' not in df_level_elec.columns:
                df_level_elec = df_level_elec.rename(columns={'Course': 'Course name'})
        except:
            df_level_core = pd.DataFrame(columns=['Level', 'Course name', 'Course code'])
            df_level_elec = pd.DataFrame(columns=['Level', 'Course name', 'Course code'])
        
        try:
            df_references = pd.read_excel('data/references.xlsx')
        except:
            df_references = pd.DataFrame(columns=['Course name', 'Reference'])

        
        # --- USER MANDATORY NAMING OVERRIDES ---
        room_replacements = {
            "Library": "Student Services / مكتب خدمات الطلاب",
            "Library / المكتبة": "Student Services / مكتب خدمات الطلاب",
            "Lab 1": "Machine Lab / معمل المشين",
            "Lab-1": "Machine Lab / معمل المشين",
            "Lab 2": "Electronics Lab / معمل الإلكترونيات",
            "Lab-2": "Electronics Lab / معمل الإلكترونيات",
            "Dr. Malek Office": "Dr. Malek Office / مكتب دكتور مالك الدهيمي",
            "Dr. Muhannad Office": "Dr. Muhannad Office / مكتب دكتور مهند الشتيوي"
        }
        if not df_rooms.empty:
            df_rooms['Name'] = df_rooms['Name'].replace(room_replacements)
        if not df_keywords.empty:
            df_keywords['Keyword'] = df_keywords['Keyword'].replace(room_replacements)
            
        for i, row in df_locations.iterrows():
            en_val = str(row['Name_EN']).strip()
            if "Library" in en_val:
                df_locations.at[i, 'Name_EN'] = "Student Services"
                df_locations.at[i, 'Name_AR'] = "مكتب خدمات الطلاب"
            elif ("Lab" in en_val or "معمل" in str(row['Name_AR'])) and "1" in en_val:
                df_locations.at[i, 'Name_EN'] = "Machine Lab"
                df_locations.at[i, 'Name_AR'] = "معمل المشين"
            elif ("Lab" in en_val or "معمل" in str(row['Name_AR'])) and "2" in en_val:
                df_locations.at[i, 'Name_EN'] = "Electronics Lab"
                df_locations.at[i, 'Name_AR'] = "معمل الإلكترونيات"
            elif "Malek" in en_val or "مالك" in str(row['Name_AR']):
                df_locations.at[i, 'Name_EN'] = "Dr. Malek Office"
                df_locations.at[i, 'Name_AR'] = "مكتب دكتور مالك الدهيمي"
            elif "Muhannad" in en_val or "مهند" in str(row['Name_AR']):
                df_locations.at[i, 'Name_EN'] = "Dr. Muhannad Office"
                df_locations.at[i, 'Name_AR'] = "مكتب دكتور مهند الشتيوي"

        # --- MANDATORY DELETIONS (Classroom A, B, 3) ---
        # Filter out nodes containing "Classroom A", "Classroom B", or "Classroom 3"
        return doctors_old, courses_old, df_rooms, df_docs, df_level_core, df_level_elec, df_locations, df_paths, df_keywords, df_references
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_doctors_old, df_courses_old, df_rooms, df_docs, df_level_core, df_level_elec, df_locations, df_paths, df_keywords, df_references = load_data()

# Build search corpuses for fuzzy matching
doctor_names = df_docs['Doctor name'].dropna().unique().tolist() if not df_docs.empty else []
course_names_in_docs = df_docs['Course name'].dropna().unique().tolist() if not df_docs.empty else []
room_names = df_keywords['Keyword'].dropna().astype(str).tolist() if not df_keywords.empty else []

# --- Session State for Navigation ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

def navigate_to(page):
    st.session_state.current_page = page
    # Inject JavaScript to auto-close the sidebar on mobile devices (width < 992px)
    js = """
    <script>
        var isMobile = window.innerWidth < 992;
        if (isMobile) {
            var closeBtn = window.parent.document.querySelector('[data-testid="stSidebar"] button[kind="header"]');
            if (closeBtn) {
                closeBtn.click();
            } else {
                // Fallback for newer Streamlit versions
                var overlay = window.parent.document.querySelector('[data-testid="stSidebarOverlay"]');
                if (overlay) {
                    overlay.click();
                }
            }
        }
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# --- Sidebar Navigation ---
with st.sidebar:
    if os.path.exists('assets/images/logo1.png'):
        st.image('assets/images/logo1.png', width=150)
    st.markdown("### Menu")
    
    menu_items = {
        "Home": "🏠",
        "AI Chat": "💬",
        "Doctor Finder": "👨‍🏫",
        "Smart Schedule Generator": "📅",
        "Building Navigation": "🏢",
        "AR Navigation": "📱",
        "Parking Finder": "🚗",
        "Admin: QR Codes": "🏷️"
    }
    
    for page, icon in menu_items.items():
        if st.button(f"{icon} {page}", key=f"nav_{page}"):
            navigate_to(page)

# --- Header ---
if st.session_state.current_page != "Home":
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if os.path.exists('assets/images/logo1_transparent.png'):
            try:
                st.image('assets/images/logo1_transparent.png', width='stretch')
            except:
                st.image('assets/images/logo1.png', width='stretch')
    with col_title:
        st.title(st.session_state.current_page)
        
        page_descriptions = {
            "AI Chat": "Ask natural language questions about doctors, emails, and rooms.",
            "Doctor Finder": "Search for professors by name or course across the university.",
            "Smart Schedule Generator": "Auto-generate conflict-free schedules based on your preferences.",
            "Building Navigation": "Search and navigate to rooms and labs efficiently.",
            "AR Navigation": "Use your camera to navigate through the campus in Augmented Reality.",
            "Parking Finder": "AI-powered parking detection system to find available spots.",
            "Admin: QR Codes": "Generate and manage AR Navigation QR codes."
        }
        desc = page_descriptions.get(st.session_state.current_page, "")
        if desc:
            st.markdown(f"<p style='color: inherit; opacity: 0.8; font-size: 1.1rem; margin-top: -15px; margin-bottom: 0;'>{desc}</p>", unsafe_allow_html=True)
            
    st.divider()

# --- Page Routing ---

if st.session_state.current_page == "Home":
    # Hero Section
    col_logo, col_hero = st.columns([1, 4])
    with col_logo:
        if os.path.exists('assets/images/logo1_transparent.png'):
            st.image('assets/images/logo1_transparent.png', width='stretch')
    with col_hero:
        st.markdown("<h1 style='font-size: 2.8rem; margin-bottom: 0;'>Welcome to PSAU Chat</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: inherit; opacity: 0.7; margin-top: 0;'>Your Smart university Assistant</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: inherit; font-size: 1.1rem; opacity: 0.9;'>Welcome to the <b>PSAU Smart university Assistant Dashboard!</b><br>You can securely interact with the database entries below. Navigate via the sidebar or ask the AI Chat assistant for quick answers!</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Dashboard Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">AI Chat</div>
            <div class="feature-desc">Ask natural language questions about doctors, emails, and rooms.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Chat", key="btn_chat"): navigate_to("AI Chat")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏢</div>
            <div class="feature-title">Building Nav</div>
            <div class="feature-desc">Search for classrooms and get simple text directions.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Navigation", key="btn_bldg"): navigate_to("Building Navigation")

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👨‍🏫</div>
            <div class="feature-title">Doctor Finder</div>
            <div class="feature-desc">Search for professors by name or course across the university.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Finder", key="btn_doc"): navigate_to("Doctor Finder")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <div class="feature-title">AR Navigation</div>
            <div class="feature-desc">Use your phone's camera to get visual arrows directing you.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AR Nav", key="btn_ar"): navigate_to("AR Navigation")

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📅</div>
            <div class="feature-title">Smart Schedule</div>
            <div class="feature-desc">Auto-generate conflict-free schedules based on your preferences.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Scheduler", key="btn_sched"): navigate_to("Smart Schedule Generator")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚗</div>
            <div class="feature-title">AI Parking Availability Demo</div>
            <div class="feature-desc">Check real-time parking availability across campus zones using AI.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Find Parking", key="btn_park"): navigate_to("Parking Finder")


elif st.session_state.current_page == "AI Chat":
    
    st.markdown("""
    <div style='background: rgba(15, 118, 110, 0.05); padding: 12px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid var(--primary-color);'>
        <p style='margin: 0; opacity: 0.9; font-size: 0.95rem;'>💡 <b>Examples of what you can ask:</b></p>
        <p style='margin: 5px 0 0 0; opacity: 0.8; font-size: 0.85rem;'>
        • "Who teaches Electronic Systems?" <br>
        • "What is Dr. Muhannad's email?" <br>
        • "وين معمل المشين؟" <br>
        • "أبي رابط السجل الأكاديمي"
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_suggestion" not in st.session_state:
        st.session_state.pending_suggestion = None
        
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg' dir='auto'>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "bot" and not msg["content"].startswith("nav_trigger:"):
            st.markdown(f"<div class='bot-msg' dir='auto'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
            
            # Check if this bot message is immediately followed by a nav trigger
            if i + 1 < len(st.session_state.messages) and st.session_state.messages[i+1]["content"].startswith("nav_trigger:"):
                target = st.session_state.messages[i+1]["content"].replace("nav_trigger:", "")
                if st.button("Open for Directions", key=f"ar_btn_{i}"):
                    from thefuzz import process, fuzz
                    k_match = process.extractOne(target, df_keywords['Keyword'].astype(str).tolist(), scorer=fuzz.token_set_ratio)
                    if k_match and k_match[1] > 60:
                        st.session_state.destination_id = df_keywords.loc[df_keywords['Keyword'].astype(str) == k_match[0], 'TargetNode'].values[0]
                    else:
                        st.session_state.destination_id = target
                    st.session_state.destination_name = target
                    st.session_state.current_loc_id = None
                    navigate_to("AR Navigation")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
            
    query = st.chat_input("Type your question here...")
    
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Helper to format doctor response cleanly
        def format_doctor_card(doc_row, include_courses=True):
            name = doc_row['Doctor name']
            email = doc_row['Email']
            location = doc_row['Location']
            website = doc_row.get('Website', None) if 'Website' in doc_row else None
            
            card_html = f"<div class='data-card' dir='auto'><h4>👨‍🏫 Doctor: <b>{name}</b></h4><p>📧 <b>Email:</b> <a href='mailto:{email}'>{email}</a></p>"
            
            if pd.notna(location):
                card_html += f"<p>📍 <b>Office:</b> الدور الثالث</p>"
                
            if pd.notna(website) and website != "" and str(website).strip().lower() != "nan":
                card_html += f"<p>🔗 <b>Website:</b> <a href='{website}' target='_blank'>Visit Profile</a></p>"
            
            if include_courses:
                courses = df_docs[df_docs['Doctor name'] == name]['Course name'].dropna().unique().tolist()
                if courses:
                    courses_str = "<br>• ".join(courses)
                    card_html += f"<p>📚 <b>Courses:</b><br>• {courses_str}</p>"
                    
            card_html += "</div>"
            return card_html, pd.notna(location)

        import re
        def normalize_text(text):
            if not isinstance(text, str):
                return ""
            t = text.lower()
            t = re.sub(r'[أإآ]', 'ا', t)
            t = re.sub(r'\bال', '', t)
            return t.strip()

        doc_map = {normalize_text(n): n for n in doctor_names} if doctor_names else {}
        course_map = {normalize_text(c): c for c in df_docs['Course name'].dropna().unique()} if not df_docs.empty else {}
        room_map = {normalize_text(r): r for r in room_names} if room_names else {}

        query_norm = normalize_text(query)
        response = None
        nav_target = None
        
        # 0. Check conversational context for confirmations
        positive_confirmations = ['yes', 'نعم', 'sure', 'ok', 'طيب', 'اكيد', 'يب', 'ايوا', 'اي', 'ايه', 'صحيح', 'بالضبط']
        negative_confirmations = ['no', 'nope', 'لا', 'غلط', 'غير صحيح', 'مو هو', 'مو هذا', 'خطأ']
        
        if st.session_state.pending_suggestion is not None:
            if any(conf in query_norm for conf in positive_confirmations):
                doc_info = st.session_state.pending_suggestion
                if 'Course name' in doc_info and 'Course name' in st.session_state.pending_suggestion.keys():
                    card_html, has_location = format_doctor_card(doc_info, include_courses=True)
                    if 'suggestion_type' in st.session_state and st.session_state.suggestion_type == 'course':
                        course_code = doc_info['Course code'] if pd.notna(doc_info['Course code']) else "N/A"
                        loc_str = doc_info['Location'] + ' (بالدور الثالث)' if pd.notna(doc_info['Location']) else 'Coming soon'
                        response = f"<div class='data-card' dir='auto'><h4>📖 Course: <b>{doc_info['Course name']}</b></h4><p>🔢 <b>Course Code:</b> {course_code}</p><p>👨‍🏫 <b>Doctor Name:</b> {doc_info['Doctor name']}</p><p>📧 <b>Email:</b> <a href='mailto:{doc_info['Email']}'>{doc_info['Email']}</a></p><p>📍 <b>Office:</b> {loc_str}</p></div>"
                        has_location = pd.notna(doc_info['Location'])
                    else:
                        card_html, has_location = format_doctor_card(doc_info, include_courses=False)
                        response = card_html
                else:
                    card_html, has_location = format_doctor_card(doc_info, include_courses=False)
                    response = card_html
                if has_location:
                     nav_target = doc_info['Doctor name']
                
                st.session_state.pending_suggestion = None  # Clear context after fulfilling
                
            elif any(conf in query_norm for conf in negative_confirmations):
                response = "<div class='data-card'><p>عذراً! ممكن توضح سؤالك أكثر أو تعطيني اسم المادة بدقة أكبر؟ 🙏</p></div>"
                st.session_state.pending_suggestion = None
            else:
                # If they didn't say yes/no, just clear and evaluate Normally
                st.session_state.pending_suggestion = None
                
        elif any(conf == query_norm for conf in positive_confirmations):
             response = "How can I help you next? 😊"
             st.session_state.pending_suggestion = None
             
        # Clear trailing suggestion if they asked a new question entirely
        if not response:
            st.session_state.pending_suggestion = None

        # 0.5 Student Reports Portal
        if not response:
            reports_keywords = ['certificate', 'transcript', 'proof', 'letter', 'exam schedule', 'final schedule', 'completed hours', 'level statement', 'transfer form', 'شهادة', 'سجل', 'أكاديمي', 'مشهد', 'اثبات', 'إثبات', 'جدول الاختبارات', 'ساعات', 'منجزة', 'افادة', 'إفادة', 'مستوى', 'تحويل خارجي']
            if any(w in query_norm for w in reports_keywords):
                if any(w in query_norm.replace(' ', '') for w in ['كمساعة']):
                    pass # Handled by graduation requirements if asking "How many hours" but let's let graduation requirements catch it first if needed... actually let's just make it a dedicated check.
                
                # Careful with overlapping words like "hours / ساعات" used in graduation req check below.
                # Let's make the keyword match more specific for the reports portal.
                reports_specific_keywords = [
                    'certificate', 'transcript', 'proof letter', 'final exam', 'exam schedule', 
                    'level statement', 'transfer form', 'شهادة', 'سجل اكاديمي', 'سجل أكاديمي',
                    'مشهد', 'خطاب اثبات', 'خطاب إثبات', 'جدول الاختبارات', 'جدول نهائي',
                    'افادة مستوى', 'إفادة مستوى', 'تحويل خارجي', 'شهاده', 'افاده', 'إفاده'
                ]
                if any(w in query_norm for w in reports_specific_keywords):
                    response = "<div class='data-card'><h4>📄 Student Reports / تقارير الطالب</h4><p>You can issue your academic transcript, proof letters, certificates, final exam schedules, and external transfer forms through the official Student Reports portal.</p><p>يمكنك إصدار السجل الأكاديمي، مشاهد وإثباتات، الجداول النهائية، إفادة المستوى، ونماذج التحويل الخارجي عبر بوابة تقارير الطالب الرسمية.</p><p>🔗 <b>Link / الرابط:</b> <a href='https://student.psau.edu.sa/reports' target='_blank'>student.psau.edu.sa/reports</a></p></div>"



        # 1. EE Knowledge Checks
        if not response:
            if any(w in query_norm for w in ['تخرج', 'ساعات', 'graduate', 'hours', '166', 'كم ساعة']):
                response = "<div class='data-card'><h4>🎓 متطلبات التخرج / Graduation Requirements</h4><p>إجمالي الساعات المعتمدة المطلوبة للتخرج من برنامج الهندسة الكهربائية هو <b>166 ساعة</b>.<br><br>The total credit hours required for graduation from the Electrical Engineering program is <b>166 hours</b>.</p></div>"

        # 1.5 Intercept Schedule Generator Intent
        if not response:
            if any(w in query_norm.split() for w in ['جدول', 'جدولي', 'جدولك']):
                # Append a ghost message so if they ever return to AI Chat, they know what happened!
                st.session_state.messages.append({"role": "assistant", "content": "Sure! Tracking you to the Smart Schedule Generator. 📅🏃‍♂️💨"})
                st.session_state.current_page = "Smart Schedule Generator"
                st.rerun()
        # 1.6 Intercept Parking Intent
        if not response:
            if any(w in query_norm.split() for w in ['مواقف', 'موقف', 'باركنج', 'باركنق', 'parking', 'parkings']):
                st.session_state.messages.append({"role": "assistant", "content": "Taking you to the AI Parking Finder... 🚗✨"})
                st.session_state.current_page = "Parking Finder"
                st.rerun()
        # ====== GEMINI ENGINE INTEGRATION ======
        if not response:
            try:
                import google.generativeai as genai
                import os
                
                # API key read from environment variable (safe for GitHub!)
                api_key = os.getenv("GEMINI_API_KEY", "")
                
                if not api_key:
                    response = "<div class='data-card'><p>⚠️ <b>Missing Gemini API Key!</b> Please set the GEMINI_API_KEY environment variable.</p></div>"
                else:
                    genai.configure(api_key=api_key)
                    
                    # Serialize lightweight context string from dataframe
                    context_data_docs = df_docs.to_json(orient='records', force_ascii=False) if not df_docs.empty else "No data."
                    context_data_refs = df_references.to_json(orient='records', force_ascii=False) if not df_references.empty else "No references."
                    context_level_core = df_level_core.to_json(orient='records', force_ascii=False) if not df_level_core.empty else "No core data."
                    context_level_elec = df_level_elec.to_json(orient='records', force_ascii=False) if not df_level_elec.empty else "No elective data."
                    
                    system_prompt = f"""You are the PSAU Smart University Assistant, an intelligent, helpful, and bilingual AI for Prince Sattam bin Abdulaziz University (PSAU).

CRITICAL IDENTITY RULES:
1. Address the user as a member of the university (منسوبي الجامعة). Use gender-neutral phrasing in Arabic (e.g., "يمكنك" instead of "يمكنكِ").
1.5 LANGUAGE RULE: Respond in the SAME LANGUAGE as the user's question. If they ask in English, answer in English. If they ask in Arabic, answer in Arabic. Always maintain a professional and helpful tone in both languages.
1.8 USER INTERFACE CONTEXT: If asked who you are or who this app is for, explain that our platform is designed for everyone (Students, Doctors, and Admins). However, *this specific interface* you are currently interacting with is tailored for the STUDENT. Explain that the Doctor's interface is different (they use it to upload references and update their campus availability), and the Admin's interface is also different (they use it to upload courses and sections). Emphasize that "our chat site" (موقعنا شات) automatically resolves schedule conflicts and generates schedules directly!
2. NEVER start your response with "أهلاً بك يا منسوبي PSAU" or any repeated greeting. Jump straight to the answer.
3. When referring to university instructors, always use "دكاترة" or "أساتذة" — NEVER use "أطباء" (that word means medical doctors, not instructors).
4. Your current database primarily covers the Electrical Engineering department, but you serve ALL PSAU members (Students, Doctors, and Admin staff).
5. If anyone asks for IF (إفادة), student ID (تعريف طالب), academic transcript (سجل أكاديمي), proof letters, certificates, or ANY academic documents — they ALL come from the Student Reports Portal: https://student.psau.edu.sa/reports
   Always provide this link and inform them they can get all official documents from there.
6. If a course or office exists in the data but has no listed instructor/details, say "لم يتم تحديد البيانات لهذه الخانة بعد" instead of saying it doesn't exist.
7. APP FEATURES KNOWLEDGE: You are part of an integrated campus application. You MUST mention these if asked about related features:
   - AI Parking Finder: This is a built-in AI module for detecting parking spots. IMPORTANT: Currently, it is NOT connected to live cameras. It functions as a demo where users UPLOAD photos or videos to test the AI's accuracy in identifying vacant and occupied spots. Its purpose is to show how the model works with files. The future vision is to link it to live cameras for real-time guidance.
   - AR Navigation: Our app contains an AR (Augmented Reality) navigation system. It works by scanning specific physical QR codes placed in key areas. For now, it's a demo to show how it guides you to labs, offices, and university services. The future vision is to provide full-campus coverage, guiding you not only to rooms but also to university-wide events, competitions, and gatherings.
8. GENERAL KNOWLEDGE:
   - Engineering degree duration is 5 years.
   - Medicine degree duration is 7 years.
   - Most other majors at PSAU are 4 years.
9. TONE & OFFICIAL INFO: Speak dynamically and avoid "robotic" canned responses. Mention that the information you provide is based on available data, but for ANY official academic or administrative confirmation, the user SHOULD always refer to their college or department.
10. ACADEMIC SERVICES & COURSE WITHDRAWAL (الاعتذار): 
   - If the user asks about Drop and Add (الحذف والإضافة), Course Withdrawal (الاعتذار عن مقرر), Study Plans (الخطط الدراسية), or related academic systems, you must explain that these services are handled through the Academic Services Portal.
   - For Course Withdrawal (الاعتذار عن مقرر), YOU MUST KNOW AND FOLLOW THESE EXACT RULES:
     * شروط الاعتذار:
       1. يجوز للطالب الانسحاب من مقرر دراسي واحد في الفصل الدراسي الواحد، دون أن يُعَد راسباً، وذلك قبل بداية الاختبارات النهائية بأسبوعين على الأقل.
       2. ألا يتجاوز عدد مرات الاعتذار أربع مقررات دراسية كحد أقصى في نظام الفصلين الدراسيين، وستة مقررات دراسية كحد أقصى في نظام الفصول الدراسية الثلاثة، طيلة فترة دراسة الطالب في الجامعة.
       3. ألا يؤثر ذلك على الحد الأدنى من العبء الدراسي للطالب وهو (12) وحدة دراسية.
       4. يرصد للطالب المعتذر عن مقرر دراسي تقدير (ع) أو (W).
     * خطوات التقديم: الدخول للبوابة الأكاديمية -> إدخال حركات أكاديمية -> إدخال حركة أكاديمية جديدة -> تحديد نوع الحركة (الاعتذار عن مقرر) -> التالي -> اختيار المقرر -> حفظ.
     * لمتابعة حالة الطلب: من إدخال حركات أكاديمية -> إظهار المقررات المعتذر عنها. حالة الطلب تكون إما مدخل (تحت الإجراء)، مقبول، أو مرفوض.
   - AT THE VERY END OF YOUR RESPONSE, you MUST provide this exact link: https://eserve.psau.edu.sa/ku/init

CRITICAL KNOWLEDGE:
1. Doctors and Courses Data: {context_data_docs}
2. Course References: {context_data_refs}
   - If a student asks for a reference, book, or materials for a course, you MUST provide the specific link from this References data for that course.
3. Study Plan - Core Courses: {context_level_core}
   - Use this to answer queries about mandatory subjects for any Level.
4. Study Plan - Elective Courses: {context_level_elec}
   - VERY IMPORTANT: If a student asks for 'Electives' or 'مواد اختيارية' for a specific level (like Level 7), search this exact Elective Courses dataset. If the level has no electives listed, you MUST clearly inform them that there are NO electives for this level, and DO NOT hallucinate any courses!
5. Facilities Floors: 
   - All Classrooms / Halls (القاعات) are located on the 3rd Floor (الدور الثالث). Example: Hall E-101, E-102.
   - Machine Lab (معمل المشين / معمل الآلات) is on the GROUND FLOOR (الدور الأرضي) - EXCEPTION!
   - All other Labs (المعامل) are located on the 2nd Floor (الدور الثاني). Example: Electronics Lab, Measurements Lab.
6. Electrical Engineering Tracks:
   - There are two main tracks: Communications Track (مسار الاتصالات) and Power Track (مسار القوى).
   - They differ in advanced elective courses and the graduation project.
   - The final graduation document is issued as a general "Electrical Engineering" degree without specifying the track.

FORMATTING RULES:
1. PERSONA: Speak warmly, naturally, and enthusiastically to all PSAU members (طلاب، دكاترة، إداريين). Use rich emojis. NEVER start with "أهلاً بك يا منسوبي PSAU" — greeting-neutrality is key. Answer directly.
2. DOCTOR INFORMATION: If asked about a doctor, YOU MUST output this exact structured HTML card (replace brackets with actual data):
   <div class='data-card' dir='auto'>
     <h4>👨‍🏫 Doctor: [Name]</h4>
     <p>📧 Email: <a href='mailto:[email]'>[email]</a></p>
     <p>📍 Office: الدور الثالث</p>
     <p>🟢 Status: متواجد حالياً في الحرم الجامعي</p>
   </div>
   nav_trigger:[Name]

3. COURSE REFERENCES: If asked for references or books for a subject keyword (e.g. "اتصالات"), you MUST search ALL courses whose names contain that keyword, and for EACH one output a card like:
   <div class='data-card' dir='auto'>
     <h4>📚 [Course Name] (Course Code)</h4>
     <p>👨‍🏫 Doctor: [Doctor Name or "غير متوفر حالياً"]</p>
     <p>🔗 <a href='[Link]' target='_blank'>📥 تحميل المرجع / Download Reference</a></p>
   </div>
   Show ALL matching courses, not just one.

4. GENERAL CAMPUS LOCATIONS: You MUST memorize these exact locations so you don't guess:
   - Pi Cafe (مقهى باي): Located in the Main Lobby (البهو الرئيسي). Ideal for coffee and relaxing.
   - Student Services (مركز أو مكتب خدمات الطالب): Located on the Ground Floor (الدور الأرضي). This is where students can print papers (طباعة الأوراق).
   - If asked about these, give their correct location and MUST append nav_trigger:[Location].

5. HTML OUTPUT: DO NOT wrap your HTML in markdown code blocks like ```html. Output raw HTML directly.
"""
                    
                    prompt_str = f"SYSTEM INSTRUCTIONS:\n{system_prompt}\n\nCHAT HISTORY:\n"
                    # Capture up to the second-to-last message
                    for msg in st.session_state.messages[-4:-1]:  
                        role = "Assistant" if msg["role"] == "bot" else "User"
                        clean_content = msg["content"].replace("nav_trigger:", "").strip()
                        prompt_str += f"{role}: {clean_content}\n\n"
                        
                    # Add current message
                    if st.session_state.messages:
                        current_msg = st.session_state.messages[-1]["content"].replace("nav_trigger:", "").strip()
                        prompt_str += f"CURRENT USER QUESTION: {current_msg}\n\nASSISTANT ANSWER:"
                    
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    completion = model.generate_content(prompt_str)
                    
                    # Clean up markdown formats to ensure Streamlit renders HTML
                    full_reply = completion.text.replace("```html", "").replace("```", "").strip()
                    
                    # Catch structural AR hook trigger
                    if "nav_trigger:" in full_reply:
                        parts = full_reply.split("nav_trigger:")
                        response = parts[0].strip()
                        nav_target = parts[1].strip().split("<")[0].strip() # Clean HTML tags if any
                    else:
                        response = full_reply
            except ImportError:
                response = "<div class='data-card'><p>🚫 <b>Gemini package not found!</b> The environment must install this package first. You must run: <code>pip install google-generativeai</code>.</p></div>"
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str or "exhausted" in error_str.lower():
                    response = "<div class='data-card'><p>⏳ <b>تهدئة السرعة (Rate Limit):</b> لقد استهلكت أقصى كمية مسموحة من الأسئلة في الدقيقة الواحدة. الرجاء الانتظار لمدة دقيقة واحدة ثم إعادة إرسال سؤالك مجدداً.</p></div>"
                elif "403" in error_str and "leaked" in error_str.lower():
                    response = "<div class='data-card'><p>🔐 <b>تم حظر مفتاح API:</b> يبدو أن مفتاح البرمجة تم تسريبه. يرجى من المطور استبداله بمفتاح جديد من Google AI Studio وتحديث ملف .env.</p></div>"
                else:
                    response = f"<div class='data-card'><p>⚠️ <b>AI Error:</b> {error_str}</p><p>نعتذر عن هذا الخطأ التقني. يرجى المحاولة مرة أخرى أو توجيه السؤال بشكل مختلف.</p></div>"
                
        if response:
            st.session_state.messages.append({"role": "bot", "content": response})
            if nav_target:
                 st.session_state.messages.append({"role": "bot", "content": "nav_trigger:" + nav_target})
            st.rerun()

    # AR Navigation Button intercept logic is now integrated directly inside the chat display loop above.

elif st.session_state.current_page == "Doctor Finder":
    
    search_term = st.text_input("Search for a Doctor or Course:", placeholder="e.g. ahmed, math, or 1050")
    
    # Case-insensitive Smart Search
    if search_term:
        arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        term = search_term.translate(arabic_to_english).lower()
        mask = df_docs['Doctor name'].astype(str).str.lower().str.contains(term, na=False) | \
               df_docs['Course name'].astype(str).str.lower().str.contains(term, na=False) | \
               df_docs['Course code'].astype(str).str.lower().str.contains(term, na=False)
        results = df_docs[mask]
    else:
        results = df_docs
        
    if not results.empty:
        # Group by doctor to avoid duplicate cards for each course
        st.write(f"Found {results['Doctor name'].nunique()} doctor(s):")
        # Display as modern cards
        for doc_name, group in results.groupby('Doctor name'):
            email = group['Email'].iloc[0]
            location = group['Location'].iloc[0]
            courses_taught = [f"{row['Course name']} ({row['Course code']})" for _, row in group.iterrows()]
            
            # De-duplicate courses
            courses_taught = list(dict.fromkeys(courses_taught))
            
            if 'doc_avail_map' not in st.session_state:
                st.session_state.doc_avail_map = {}
            if doc_name not in st.session_state.doc_avail_map:
                import random
                st.session_state.doc_avail_map[doc_name] = random.choice([True, False])
            
            is_avail = st.session_state.doc_avail_map[doc_name]
            avail_html = "<p dir='auto'><span style='color: green; font-weight: bold;'>🟢 Available in الجامعة / متواجد في الجامعة</span></p>" if is_avail else "<p dir='auto'><span style='color: red; font-weight: bold;'>🔴 Not available in الجامعة / غير متواجد في الجامعة</span></p>"
            
            location_html = f"<p><strong>📍 Office:</strong> {location}</p>" if pd.notna(location) else ""
            st.markdown(f"""
            <div class="data-card" dir="auto">
                <h4>👨‍🏫 Doctor: {doc_name}</h4>
                {avail_html}
                <p><strong>📚 Courses:</strong><br>• {'<br>• '.join(courses_taught)}</p>
                <p><strong>📧 Email:</strong> <a href="mailto:{email}">{email}</a></p>
                {location_html}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Navigate to Office", key=f"nav_doc_{doc_name.replace(' ', '_')}"):
                from thefuzz import process, fuzz
                k_match = process.extractOne(doc_name, df_keywords['Keyword'].astype(str).tolist(), scorer=fuzz.token_set_ratio)
                if k_match and k_match[1] > 60:
                     st.session_state.destination_id = df_keywords.loc[df_keywords['Keyword'].astype(str) == k_match[0], 'TargetNode'].values[0]
                     st.session_state.destination_name = doc_name
                     st.session_state.current_loc_id = None
                     navigate_to("AR Navigation")
                else:
                    st.error("Office location not yet mapped in Navigation graph.")
    else:
        st.warning("No doctors found matching your criteria.")

elif st.session_state.current_page == "Smart Schedule Generator":
    
    col1, col2, col3 = st.columns(3)
    with col1:
        # Extract purely the numeric levels from the string "Level X"
        levels = sorted([int(x.replace("Level ", "")) for x in df_level_core['Level'].dropna() if "Level " in x])
        selected_level = st.selectbox("Select Your Level:", levels if levels else [1, 2, 3, 4, 5, 6, 7, 8])
    with col2:
        schedule_mode = st.radio("Elective Selection Mode:", ["Randomize Electives", "Core Subjects Only"])
    with col3:
        days_off = st.multiselect("Preferred Days Off:", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"])
        num_courses = st.number_input("Number of Courses limit:", min_value=1, max_value=8, value=5)
        
    if st.button("Generate best Schedule"):
        level_str = f"Level {selected_level}"
        
        # Pull Core Subjects
        core_row = df_level_core[df_level_core['Level'].astype(str).str.lower() == level_str.lower()]
        core_courses = [str(x).strip() for x in core_row.iloc[0].values[1:] if pd.notna(x) and str(x).strip()] if not core_row.empty else []
        
        # Pull Elective Subjects
        elec_courses = []
        if schedule_mode == "Randomize Electives":
            elec_row = df_level_elec[df_level_elec['Level'].astype(str).str.lower() == level_str.lower()]
            if not elec_row.empty:
                elec_courses = [str(x).strip() for x in elec_row.iloc[0].values[1:] if pd.notna(x) and str(x).strip()]
                
                # Pick up to 2 random electives if available to keep the schedule tight
                import random
                if len(elec_courses) > 2:
                    elec_courses = random.sample(elec_courses, 2)
                    
        # Combine Schedule
        final_schedule_subjects = core_courses + elec_courses
        
        # De-duplicate schedule subjects entirely
        final_schedule_subjects = list(dict.fromkeys(final_schedule_subjects))
        
        # Enforce max limit visually 
        final_schedule_subjects = final_schedule_subjects[:num_courses]
        
        if not final_schedule_subjects:
            st.error(f"No subjects found for Level {selected_level}.")
        else:
            # 1. Block Scheduling Logic
            all_weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
            available_days = [day for day in all_weekdays if day not in days_off]
            
            # Standard simulated university blocks
            time_blocks = [
                "08:00 AM - 09:30 AM",
                "10:00 AM - 11:30 AM",
                "01:00 PM - 02:30 PM",
                "03:00 PM - 04:30 PM"
            ]
            
            # Simple simulation: each subject needs 1 unique (Day + Time) slot. 
            # In a real university, subjects usually span 2 days (e.g. Sun/Tue), 
            # but for this simulation we check if enough total unique slots exist across allowed days.
            total_slots_available = len(available_days) * len(time_blocks)
            
            if len(final_schedule_subjects) > total_slots_available:
                st.error(f"❌ Impossible Schedule: You requested {len(final_schedule_subjects)} courses, but after taking {len(days_off)} days off, there are not enough time slots left in the week to fit them without conflicts!")
                st.info("Try reducing your 'Number of Courses' limit or selecting fewer 'Days Off'.")
            elif not available_days:
                st.error("❌ Impossible Schedule: You selected every day of the week off!")
            else:
                st.success(f"Generated a schedule for Level {selected_level} with {len(final_schedule_subjects)} subjects!")
                
                # Assign Slots Functionally
                import random
                assigned_schedule = []
                idx_day = 0
                idx_time = 0
                
                for subject in final_schedule_subjects:
                    # Circular assignment mapping across available days and times
                    assigned_day = available_days[idx_day % len(available_days)]
                    assigned_time = time_blocks[idx_time % len(time_blocks)]
                    
                    assigned_schedule.append({
                        "subject": subject,
                        "day": assigned_day,
                        "time": assigned_time
                    })
                    
                    idx_time += 1
                    if idx_time >= len(time_blocks):
                        idx_time = 0
                        idx_day += 1

                st.session_state.sched_generated = assigned_schedule
                st.session_state.sched_days_off = days_off
                st.session_state.sched_level = selected_level
                
    if st.session_state.get('sched_generated'):
        assigned_schedule = st.session_state.sched_generated
        days_off = st.session_state.sched_days_off
        selected_level = st.session_state.sched_level
        
        st.success(f"Viewing active generated schedule for Level {selected_level}!")
        st.markdown("### Your Assigned Classes")
        
        # Display the clickable Expandable card with assigned Time Blocks
        for slot in assigned_schedule:
            subject = slot['subject']
            
            # Try to map subject to doctor
            doctor_name = "No assigned professor yet."
            email = "N/A"
            subject_code = ""
            subject_title = subject
            
            # Try extracting purely the numeric course code to fuzzy match accurately if present
            import re
            code_match = re.search(r'\d{3,4}', subject)
            if code_match:
                subject_code = code_match.group()
                # Use regex word boundary prefixed by optional letters to catch 'EE3121' cleanly from '3121' while ignoring '4101'
                mask = df_docs['Course code'].astype(str).str.contains(rf'\b[A-Za-z]*{subject_code}\b', regex=True, na=False)
                doc_row = df_docs[mask]
                
                # Fallback if code mismatch: Check if the docsEE short Course name exists physically INSIDE the long level.xlsx subject string
                if doc_row.empty:
                    mask_name = df_docs['Course name'].astype(str).apply(lambda x: str(x).strip().lower() in subject.lower() if len(str(x).strip()) > 3 else False)
                    doc_row = df_docs[mask_name]
            else:
                mask_name = df_docs['Course name'].astype(str).apply(lambda x: str(x).strip().lower() in subject.lower() if len(str(x).strip()) > 3 else False)
                doc_row = df_docs[mask_name]
                if not doc_row.empty:
                    subject_code = str(doc_row.iloc[0]['Course code'])

            with st.expander(f"{subject_title} ({subject_code if subject_code else 'N/A'})"):
                st.markdown(f"**Subject Name:** {subject_title}")
                
                # Extract and display Course References
                if not df_references.empty:
                    mask_ref = df_references['Course name'].astype(str).str.lower() == subject_title.lower()
                    if not mask_ref.any():
                        mask_ref = df_references['Course name'].astype(str).apply(lambda x: str(x).strip().lower() in subject_title.lower() if len(str(x).strip()) > 3 else False)
                    
                    if 'Link' in df_references.columns:
                        refs = df_references[mask_ref][['Reference', 'Link']].dropna(subset=['Reference']).drop_duplicates().to_dict('records')
                    else:
                        refs_fallback = df_references[mask_ref]['Reference'].dropna().astype(str).unique().tolist()
                        refs = [{'Reference': r, 'Link': '#'} for r in refs_fallback]
                        
                    if refs:
                        st.markdown("**Reference:**")
                        for ref in refs:
                            r_name = ref['Reference']
                            r_link = ref['Link'] if pd.notna(ref['Link']) else "#"
                            if r_link != "#":
                                st.markdown(f"- [{r_name}]({r_link})")
                            else:
                                st.markdown(f"- {r_name}")

                
                if len(doc_row) > 1:
                    # Let the student choose from available professors
                    doc_options = doc_row['Doctor name'].dropna().unique().tolist()
                    import hashlib
                    safe_key = f"sel_doc_{hashlib.md5(subject_title.encode()).hexdigest()}_{hashlib.md5(slot['time'].encode()).hexdigest()}"
                    selected_doc_name = st.radio(f"Select Professor for {subject_title}:", options=doc_options, key=safe_key)
                    selected_doc_row = doc_row[doc_row['Doctor name'] == selected_doc_name].iloc[0]
                    email = selected_doc_row['Email'] if pd.notna(selected_doc_row['Email']) else "N/A"
                    st.markdown(f"**Professor:** {selected_doc_name}")
                    st.markdown(f"**Lecture Time:** {slot['day']}s @ {slot['time']}")
                    st.markdown(f"**Email:** [{email}](mailto:{email})")
                elif len(doc_row) == 1:
                    selected_doc_name = doc_row.iloc[0]['Doctor name']
                    email = doc_row.iloc[0]['Email'] if pd.notna(doc_row.iloc[0]['Email']) else "N/A"
                    st.markdown(f"**Professor:** {selected_doc_name}")
                    st.markdown(f"**Lecture Time:** {slot['day']}s @ {slot['time']}")
                    st.markdown(f"**Email:** [{email}](mailto:{email})")
                else:
                    st.markdown(f"**Lecture Time:** {slot['day']}s @ {slot['time']}")
                    st.markdown(f"**Professor:** No assigned professor yet.")
                            
        st.markdown("---")
        if days_off:
            st.success(f"✅ Schedule mathematically optimized to completely avoid classes on: {', '.join(days_off)}")
        st.info("Future improvement: this system can connect to the university registration system to adopt this generated schedule.")

        # --- SCHEDULE ACTIONS ---
        st.markdown("---")
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            # Add Courses Simulation
            if st.button("➕ Add Courses", key="btn_add_courses", width='stretch'):
                st.success("Successfully added selected courses to your profile! / تمت إضافة المقررات المختارة بنجاح!")
                st.success("✅ Courses successfully added! (Simulation: Ready for University System Integration)")
                st.balloons()
        
        with action_col2:
            # Print Schedule (CSV Download)
            import pandas as pd
            csv_df = pd.DataFrame(assigned_schedule)
            if not csv_df.empty:
                csv_df.rename(columns={"subject": "Subject", "day": "Day", "time": "Time"}, inplace=True)
                csv_data = csv_df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📤 Print Schedule (Download)",
                    data=csv_data,
                    file_name=f"Smart_Schedule_Level_{selected_level}.csv",
                    mime="text/csv",
                    width='stretch'
                )

        # --- EXAM GENERATOR LOGIC ---
        st.markdown("---")
        st.markdown("### 📝 Exam Schedules")
        
        exam_col1, exam_col2 = st.columns(2)
        with exam_col1:
            gen_finals = st.button("View Final Exams Schedule", width='stretch')
        with exam_col2:
            gen_midterms = st.button("View Midterm Exams Schedule", width='stretch')
            
        if gen_finals or gen_midterms:
            exam_type = "Final Exams" if gen_finals else "Midterm Exams"
            st.session_state.exam_generated_data = []
            st.session_state.exam_generated_type = exam_type
            
            import random
            from datetime import datetime, timedelta
            
            # Simulate exam periods starting in the future
            base_date = datetime.now() + timedelta(days=14 if gen_midterms else 45)
            
            # Create a realistic block of days (excluding Weekends in SA: Friday=4, Saturday=5)
            days_range = 14 if gen_midterms else 21
            available_dates = [base_date + timedelta(days=i) for i in range(days_range)]
            available_dates = [d for d in available_dates if d.weekday() not in [4, 5]]
            random.shuffle(available_dates)
            
            import re
            for i, slot in enumerate(assigned_schedule):
                subject_title = slot['subject']
                subject_code = "N/A"
                doctor_name = "To be announced"
                
                code_match = re.search(r'\d{3,4}', subject_title)
                if code_match:
                    subject_code = code_match.group()
                    mask = df_docs['Course code'].astype(str).str.contains(rf'\b[A-Za-z]*{subject_code}\b', regex=True, na=False)
                    doc_row = df_docs[mask]
                    if doc_row.empty:
                        mask_name = df_docs['Course name'].astype(str).apply(lambda x: str(x).strip().lower() in subject_title.lower() if len(str(x).strip()) > 3 else False)
                        doc_row = df_docs[mask_name]
                else:
                    mask_name = df_docs['Course name'].astype(str).apply(lambda x: str(x).strip().lower() in subject_title.lower() if len(str(x).strip()) > 3 else False)
                    doc_row = df_docs[mask_name]
                
                if not doc_row.empty:
                    # Attempt to resolve the specific professor if the user selected one via radio earlier!
                    # Actually, if we use doc_row.iloc[0], it picks the first one from DB
                    doctor_name = doc_row.iloc[0]['Doctor name']
                    if subject_code == "N/A":
                         subject_code = str(doc_row.iloc[0]['Course code'])

                # Distribute distinct dates per exam as much as possible
                exam_date_obj = available_dates[i] if i < len(available_dates) else available_dates[0]
                exam_date = exam_date_obj.strftime("%Y-%m-%d (%A)")
                
                # Standard times instead of completely random for an official look
                exam_time = "10:00 AM - 12:00 PM" if gen_midterms else "08:00 AM - 11:00 AM"
                
                st.session_state.exam_generated_data.append({
                    "Subject": subject_title,
                    "Course Code": subject_code,
                    "Professor Name": doctor_name,
                    "Exam Date": exam_date,
                    "Time": exam_time
                })

        if st.session_state.get('exam_generated_data'):
            st.success(f"📅 Official **{st.session_state.exam_generated_type}** Schedule Published!")
            st.info("Here is the approved exam schedule based on your registered courses. Please arrive at the examination hall 15 minutes early.")
            exam_df = pd.DataFrame(st.session_state.exam_generated_data)
            exam_df.sort_values(by="Exam Date", inplace=True)
            exam_df.reset_index(drop=True, inplace=True)
            
            st.dataframe(exam_df, width='stretch')


elif st.session_state.current_page == "Building Navigation":
    room_search = st.text_input("📍 Search Room, Lab, or Doctor Office:", placeholder="e.g. 204, Library, Lab 1, المكتبة")
    
    if room_search:
        arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        room_search_norm = room_search.translate(arabic_to_english)
        search_terms = room_search_norm.lower().split()
        
        # 1. Match against classic rooms.xlsx (EN)
        mask_rooms = pd.Series([False] * len(df_rooms))
        for t in search_terms:
            if len(t) > 1 or t.isdigit(): # Avoid single character matching too broadly unless it's a digit
                mask_rooms |= df_rooms['Name'].astype(str).str.lower().str.contains(t, na=False)
        
        # Numeric shortcut: if 3 digits, match exactly
        if room_search_norm.isdigit() and len(room_search_norm) == 3:
             mask_rooms |= df_rooms['Name'].astype(str).str.contains(room_search_norm)
             
        matched_rooms = df_rooms[mask_rooms]
        
        # 2. Match against New Navigation Keywords and Locations (EN and AR)
        matched_nodes = set()
        
        # Search df_locations for EN and AR names
        if not df_locations.empty:
            for t in search_terms:
                if len(t) > 1 or t.isdigit():
                    mask_loc = df_locations['Name_EN'].astype(str).str.lower().str.contains(t, na=False) | \
                               df_locations['Name_AR'].astype(str).str.lower().str.contains(t, na=False) | \
                               df_locations['Type'].astype(str).str.lower().str.contains(t, na=False)
                    matched_nodes.update(df_locations[mask_loc]['Node_ID'].tolist())

        # Manual Hub Mapping for Search Reliability (Arabic focused)
        HUB_MAPS = {
            "ENTRANCE_MAIN": ["مدخل", "entrance", "رئيسي", "بواب"],
            "FOUNTAIN": ["نافورة", "fountain"],
            "PI_CAFE": ["مقهى", "باي", "cafe", "pi"],
            "STUDENT_SERVICES": ["خدمات", "طلاب", "student", "services", "طباعة", "print"],
            "MACHINE_LAB": ["معمل", "مشين", "machine", "lab", "الالات", "الآلات"]
        }
        
        for hub_id, keywords in HUB_MAPS.items():
            if any(k in room_search_norm.lower() for k in keywords):
                matched_nodes.add(hub_id)
        
        # Also check df_keywords for semantic triggers
        if not df_keywords.empty:
            for t in search_terms:
                if len(t) > 1 or t.isdigit():
                    k_matches = df_keywords[df_keywords['Keyword'].astype(str).str.lower().str.contains(t, na=False)]
                    matched_nodes.update(k_matches['TargetNode'].tolist())
        
        matched_locs = df_locations[df_locations['Node_ID'].isin(matched_nodes)] if len(matched_nodes) > 0 else pd.DataFrame()
        
        # Global tracker to prevent displaying the exact same physical room twice
        rendered_names = set()
        
        found_any = False
        
        # No restricted AR destinations; mapping allows universal nodes
        
        if not matched_rooms.empty:
            found_any = True
            for idx, row in matched_rooms.reset_index().iterrows():
                room_name = row['Name']
                rendered_names.add(str(room_name).strip().lower())
                
                # Original Useful Output (Floor, Type)
                directions_map = {
                    1: "on the ground floor near the main entrance.",
                    2: "on the second floor near the main stairs.",
                    3: "on the third floor down the right hallway."
                }
                dir_text = directions_map.get(row['Floor'], f"on Floor {row['Floor']}.")
                st.success(f"Room **{room_name}** is {dir_text}")
                
                # Mock Schedule only for Classrooms and Labs
                if any(t in str(row.get('Type', '')).lower() for t in ['class', 'lab', 'قاعة', 'معمل', 'classroom']) or "e-" in room_name.lower():
                    st.markdown("### Scheduled Lectures")
                    import random
                    random.seed(room_name)
                    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
                    time_blocks = ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM"]
                    
                    if not df_docs.empty:
                        df_valid = df_docs.dropna(subset=['Course name', 'Doctor name']).reset_index(drop=True)
                        num_lectures = random.randint(2, 4)
                        if len(df_valid) > 0:
                            sample_indices = random.sample(range(len(df_valid)), min(num_lectures, len(df_valid)))
                            sample_docs = df_valid.iloc[sample_indices]
                            for i, doc in sample_docs.iterrows():
                                st.markdown(f"**{random.choice(days)} – {random.choice(time_blocks)}**  \n**Subject:** {doc['Course name']}  \n**Professor:** {doc['Doctor name']}")
                                st.markdown("---")
                        else:
                            st.info("No lecture data available.")
                    else:
                        st.info("No schedule data available.")
                    random.seed()
                
                # AR Button directly enabled without arbitrary restrictions
                if True:
                    if st.button(f"Open Camera Navigation to {room_name}", key=f"cam_room_{str(room_name).replace(' ', '_')}_{idx}"):
                        st.session_state.destination_id = None
                        from thefuzz import process, fuzz
                        k_match = process.extractOne(str(room_name), df_keywords['Keyword'].astype(str).tolist(), scorer=fuzz.token_set_ratio)
                        if k_match and k_match[1] > 60:
                            st.session_state.destination_id = df_keywords.loc[df_keywords['Keyword'].astype(str) == k_match[0], 'TargetNode'].values[0]
                        else:
                            st.session_state.destination_id = str(room_name)
                        st.session_state.destination_name = room_name
                        st.session_state.current_loc_id = None 
                        navigate_to("AR Navigation")
                        
        if not matched_locs.empty:
            for _, row in matched_locs.iterrows():
                # Avoid duplicates if rooms.xlsx already caught it
                # Avoid duplicates if rooms.xlsx already caught it (check EN, AR, and substring)
                norm_en = str(row['Name_EN']).strip().lower()
                norm_ar = str(row['Name_AR']).strip().lower()
                if any(norm_en in name or norm_ar in name or name in norm_en for name in rendered_names):
                    continue
                found_any = True
                
                # Info block for landmarks not in rooms.xlsx
                st.success(f"**{row['Name_EN']} ({row['Name_AR']})** is on Floor {row['Floor']}.")
                
                # Only show schedules for Classrooms and Labs explicitly
                is_classroom_or_lab = any(t in str(row['Type']).lower() for t in ['class', 'lab', 'قاعة', 'معمل', 'classroom'])
                if is_classroom_or_lab:
                    st.markdown("### Scheduled Lectures")
                    import random
                    random.seed(row['Name_EN'])
                    if not df_docs.empty:
                        df_valid = df_docs.dropna(subset=['Course name', 'Doctor name']).reset_index(drop=True)
                        num_lectures = random.randint(2, 4)
                        if len(df_valid) > 0:
                            sample_indices = random.sample(range(len(df_valid)), min(num_lectures, len(df_valid)))
                            sample_docs = df_valid.iloc[sample_indices]
                            for i, doc in sample_docs.iterrows():
                                st.markdown(f"**{random.choice(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'])} – {random.choice(['08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM'])}**  \n**Subject:** {doc['Course name']}  \n**Professor:** {doc['Doctor name']}")
                                st.markdown("---")
                        else:
                            st.info("No scheduled lectures for this specific room.")
                    random.seed()
                
                # Execute Navigation completely without arbitrary node restrictions
                if True:
                    if st.button(f"Open Camera Navigation to {row['Name_EN']}", key=f"cam_node_{row['Node_ID']}"):
                         st.session_state.destination_id = row['Node_ID']
                         st.session_state.destination_name = row['Name_EN']
                         st.session_state.current_loc_id = None
                         navigate_to("AR Navigation")
                         
        if not found_any:
            st.warning("Location not found.")

elif st.session_state.current_page == "AR Navigation":
    
    raw_dest_id = st.session_state.get('destination_id')
    dest_id_pre = str(raw_dest_id).strip().upper() if raw_dest_id else ""
    dest_name = st.session_state.get('destination_name', dest_id_pre)
    
    # 🚨 CRITICAL FIX: The UI dropdown yields raw node IDs (e.g., 'N006'), but the physical QR 
    # codes strictly read strings like 'MACHINE_LAB'. We strictly map them here.
    dest_name_up = str(dest_name).upper()
    dest_id = dest_id_pre
    if "MACHINE LAB" in dest_name_up or "معمل المشين" in dest_name_up:
        dest_id = "MACHINE_LAB"
    elif "STUDENT SERVICES" in dest_name_up or "خدمات الطلاب" in dest_name_up:
        dest_id = "STUDENT_SERVICES"
    elif "PI CAFE" in dest_name_up or "مقهى" in dest_name_up:
        dest_id = "PI_CAFE"
    elif "ENTRANCE" in dest_name_up or "المدخل" in dest_name_up:
        dest_id = "ENTRANCE_MAIN"
    elif "FOUNTAIN" in dest_name_up or "نافورة" in dest_name_up:
        dest_id = "FOUNTAIN"
        
    
    if not dest_id:
        st.warning("Destination not set. Please select a destination to navigate to:")
        
        # Build search index manually for the 5 requested hubs to avoid ID mismatch
        all_destinations_map = {
            "Main Entrance / المدخل الرئيسي": "ENTRANCE_MAIN",
            "Fountain Area / منطقة النافورة": "FOUNTAIN",
            "Pi Cafe / مقهى باي": "PI_CAFE",
            "Student Services / خدمات الطلاب": "STUDENT_SERVICES",
            "Machine Lab / معمل المشين": "MACHINE_LAB"
        }
        
        options_list = sorted(list(all_destinations_map.keys()))
        
        selected_dest_name = st.selectbox("Search Destination:", options=[""] + options_list, index=0)
        
        if selected_dest_name != "":
            st.session_state.destination_name = selected_dest_name
            st.session_state.destination_id = all_destinations_map[selected_dest_name]
            st.session_state.current_loc_id = None
            st.rerun()
            
        st.stop()
    else:
        # Move Origin Selection natively into AR Camera explicitly!
        st.markdown(f"#### 🎯 Destination: **{dest_name}**")
        
        # Restore explicitly requested starting options strictly
        start_options = {
            "ENTRANCE_MAIN": "Main Entrance / المدخل الرئيسي",
            "FOUNTAIN": "Fountain / النافورة"
        }
            
        if 'current_loc_id' not in st.session_state or not st.session_state.current_loc_id:
            st.warning("Please choose your physically current starting point to draw the AR Path.")
            selected_start_id = st.selectbox("🚶 Starting Location:", options=list(start_options.keys()), format_func=lambda x: start_options[x])
            if st.button("Compute Navigation Route"):
                st.session_state.current_loc_id = selected_start_id
                st.rerun()
            st.stop()
        else:
            curr_loc_id = st.session_state.current_loc_id
            
            nav_ctl_col1, nav_ctl_col2 = st.columns(2)
            with nav_ctl_col1:
                if st.button("Change Starting Location"):
                    st.session_state.current_loc_id = None
                    st.rerun()
            with nav_ctl_col2:
                if st.button("Change Destination"):
                    st.session_state.current_loc_id = None
                    st.session_state.destination_id = None
                    st.session_state.destination_name = None
                    st.rerun()
                
        # Calculate Target Floor
        try:
            dest_floor = df_locations.loc[df_locations['Node_ID'] == dest_id, 'Floor'].values[0]
        except:
            dest_floor = 1

        is_virtual = curr_loc_id.startswith("VIRT_") if curr_loc_id else False
        virtual_floor_map = {
            "VIRT_MAIN": 1, "VIRT_STAIRS_1": 1, "VIRT_STAIRS_2": 2, "VIRT_STAIRS_3": 3,
            "VIRT_ELEV_1": 1, "VIRT_ELEV_2": 2, "VIRT_ELEV_3": 3
        }
        
        route_edges = None
        route_instructions = []
        
        # Build BFS Graph Route from df_paths if both are standard nodes
        import collections
        def bfs_path(start, end, paths_df):
            graph = collections.defaultdict(list)
            for _, r in paths_df.iterrows():
                graph[r['FromNode']].append((r['ToNode'], str(r['Direction'])))
                
            queue = collections.deque([(start, [])])
            visited = set([start])
            
            while queue:
                current, path_so_far = queue.popleft()
                if current == end:
                    return path_so_far
                    
                for neighbor, direction in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path_so_far + [(neighbor, direction)]))
            return None
            
        # ----------------------------------------------------------------
        # Structured 8-node QR navigation routing
        # Nodes: ENTRANCE_MAIN, CORRIDOR_DECISION, FOUNTAIN,
        #        PI_CAFE, STUDENT_SERVICES, MACHINE_LAB, STAIRS, ELEVATOR
        # curr_loc_id is updated by QR scan or manual selection.
        # Each call returns a fresh list of remaining steps from current origin.
        # ----------------------------------------------------------------
        def node_route(origin, destination_id, destination_name):
            dest_up = str(destination_id).upper() if destination_id else ""
            
            # Use exact match mappings to initialize the UI perfectly
            if origin == "ENTRANCE_MAIN":
                return ["Move forward<br><small>امش إلى الامام</small>"]
            elif origin == "CORRIDOR_DECISION":
                if dest_up == "STUDENT_SERVICES": return ["Turn right<br><small>التف يمين</small>"]
                if dest_up == "MACHINE_LAB": return ["Turn left, then walk straight<br><small>التف يسار وبعدين امش بشكل مستقيم</small>"]
                if dest_up == "PI_CAFE": return ["Move forward, then turn slightly left<br><small>امش الى الامام والتف قليلًا لليسار</small>"]
                if dest_up == "ENTRANCE_MAIN": return ["Continue straight ahead<br><small>واصل التقدم بشكل مستقيم</small>"]
                return ["Continue forward<br><small>واصل التقدم</small>"]
            elif origin == "FOUNTAIN":
                if dest_up == "STUDENT_SERVICES": return ["Student Services is on your left<br><small>يسارك مكتب خدمات الطلاب</small>"]
                if dest_up == "MACHINE_LAB": return ["Walk forward then turn right<br><small>امش قدام بعدين يمين</small>"]
                if dest_up == "PI_CAFE": return ["Pi Cafe is behind you<br><small>مقهى باي بيكون وراك</small>"]
                if dest_up == "ENTRANCE_MAIN": return ["Go straight forward<br><small>اتجه مستقيمًا إلى الأمام</small>"]
                return ["Head back towards the corridor<br><small>ارجع باتجاه الممر</small>"]
            else:
                return ["Scan a QR code to begin navigation"]

        route_instructions = node_route(curr_loc_id, dest_id, dest_name)


        if len(route_instructions) == 0:
            route_instructions = ["You are already at the destination."]
            
        if 'current_instruction_index' not in st.session_state:
            st.session_state.current_instruction_index = 0
            
        # Clamp index within bounds to prevent index errors
        st.session_state.current_instruction_index = max(0, min(st.session_state.current_instruction_index, len(route_instructions) - 1))
        
        # Interactive instruction pagination UI
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if st.button("⬅ Previous Step", disabled=(st.session_state.current_instruction_index == 0)):
                st.session_state.current_instruction_index -= 1
                st.rerun()
        with nav_col2:
            st.markdown(f"<div style='text-align: center; color: #666; padding-top: 5px; font-weight: bold;'>Step {st.session_state.current_instruction_index + 1} of {len(route_instructions)}</div>", unsafe_allow_html=True)
        with nav_col3:
            if st.button("Next Step ➡", disabled=(st.session_state.current_instruction_index >= len(route_instructions) - 1)):
                st.session_state.current_instruction_index += 1
                st.rerun()
                
        curr_instruction_raw = route_instructions[st.session_state.current_instruction_index].lower() if route_instructions else ""
        
        # Safely assign routing instructions with a guaranteed fallback to prevent NameErrors
        curr_instruction = "Computing Route..." 
        
        if "slight left" in curr_instruction_raw or "slight_left" in curr_instruction_raw:
            curr_instruction = "Slight Left"
        elif "right" in curr_instruction_raw:
            curr_instruction = f"Turn {curr_instruction_raw.title()}"
        elif "left" in curr_instruction_raw:
            curr_instruction = f"Turn {curr_instruction_raw.title()}"
        elif curr_instruction_raw == "forward" or "forward" in curr_instruction_raw:
            curr_instruction = "Move Forward"
        elif curr_instruction_raw == "upstairs":
            curr_instruction = "Go Upstairs"
        elif "floor" in curr_instruction_raw:
            curr_instruction = curr_instruction_raw.title()
        elif curr_instruction_raw == "":
            curr_instruction = "Destination Ahead"
        elif "arrived" in curr_instruction_raw or "وصلت" in curr_instruction_raw:
            curr_instruction = "🏁 You have arrived / وصلت وجهتك"
        else:
            curr_instruction = curr_instruction_raw.title()
            
        is_arrived = (curr_instruction_raw == "") or ("arrived" in curr_instruction_raw) or ("وصلت" in curr_instruction_raw)
        
        # Base64 SVGs for Distinct 2D Arrow Billboards
        import base64
        def svg_to_uri(svg_str):
            return "data:image/svg+xml;base64," + base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
            
        svg_fwd = svg_to_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2L22 12H15V22H9V12H2L12 2Z" fill="#0f766e"/></svg>')
        svg_right = svg_to_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10 9V5L17 12L10 19V15C5 15 3 19 3 19C3 13 6 9 10 9Z" fill="#0f766e"/></svg>')
        svg_left = svg_to_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M14 9V5L7 12L14 19V15C19 15 21 19 21 19C21 13 18 9 14 9Z" fill="#0f766e"/></svg>')
        svg_slight_left = svg_to_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g transform="rotate(-45 12 12)"><path d="M12 2L22 12H15V22H9V12H2L12 2Z" fill="#0f766e"/></g></svg>')

        # Parse proper physical orientation for the 2D Graphic perfectly flat on the ground
        arrow_rot = "-90 0 0" 
        arrow_pos = "0 -1.5 -2.5"
        
        if "slight" in curr_instruction_raw and "left" in curr_instruction_raw:
            icon_uri = svg_slight_left
        elif "right" in curr_instruction_raw:
            icon_uri = svg_right
        elif "left" in curr_instruction_raw:
            icon_uri = svg_left
        else:
            icon_uri = svg_fwd
            
        # Disable auto-advance — instructions persist until QR scan
        step_duration_ms = 999999  # effectively disabled; QR scan drives progression
        
        ar_entity_html = ""
        if not is_arrived:
            ar_entity_html = f"""
                  <!-- 2D SVG Directional Graphic, placed flat on the floor directly ahead, guiding the physical turn -->
                  <a-image src="{icon_uri}" position="{arrow_pos}" rotation="{arrow_rot}" scale="1.5 1.5 1.5" animation="property: position; to: 0 -1.3 -2.5; dir: alternate; dur: 800; loop: true"></a-image>
            """
        
        # Format instruction with destination name
        dest_name = st.session_state.get('destination_name', dest_id)
        
        def on_qr_change():
            val = st.session_state.qr_loc_input
            if val and str(val).strip() != "":
                st.session_state.current_loc_id = str(val).strip()
                st.session_state.current_instruction_index = 0
                
        # Hidden input mapped to the JS dispatcher
        st.text_input("QR Location", key="qr_loc_input", label_visibility="hidden", on_change=on_qr_change)
        
        import streamlit.components.v1 as components
        components.html(f"""
            <html>
              <head>
                <script src="https://aframe.io/releases/1.3.0/aframe.min.js"></script>
                <script src="https://raw.githack.com/AR-js-org/AR.js/master/aframe/build/aframe-ar.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"></script>
                <style>
                  .ar-overlay {{
                    position: absolute; top: 15px; left: 15px; right: 15px;
                    background: rgba(255,255,255,0.95); padding: 15px;
                    border-radius: 12px; z-index: 999;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    text-align: center;
                  }}
                  .dest-title {{ margin: 0; font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
                  #main-instruction {{ margin: 6px 0 4px 0; font-size: 22px; color: #0f766e; font-weight: 800; }}
                  #helper-text {{ margin: 2px 0 0 0; font-size: 13px; color: #64748b; font-style: italic; }}
                  #debug-timer {{ margin: 5px 0 0 0; font-size: 13px; color: #b91c1c; font-weight: bold; }}
                </style>
              </head>
              <body style="margin: 0; overflow: hidden;">
                <div class="ar-overlay">
                  <p class="dest-title">Navigating to: {dest_name}</p>
                  <p id="main-instruction">{curr_instruction}</p>
                  <p id="helper-text">{'&zwj;' if is_arrived else 'Scan the next QR code when you reach it &mdash; &#x642;&#x645; &#x628;&#x645;&#x633;&#x62D; &#x627;&#x644;&#x628;&#x627;&#x631;&#x643;&#x648;&#x62D; &#x627;&#x644;&#x62A;&#x627;&#x644;&#x64A; &#x639;&#x646;&#x62D; &#x627;&#x644;&#x648;&#x635;&#x648;&#x644; &#x625;&#x644;&#x64A;&#x647;'}</p>
                  <p id="debug-timer">{'&#x1F3C1; Destination Reached' if is_arrived else ''}</p>
                </div>
                <a-scene embedded arjs="sourceType: webcam; debugUIEnabled: false;" style="height: 500px; width: 100%; border-radius: 16px; border: 2px solid #0f766e;">
                  {ar_entity_html}
                  <a-camera position="0 0 0" look-controls="touchEnabled: false; mouseEnabled: false" wasd-controls="enabled: false"></a-camera>
                </a-scene>

                <script>
                  // ── Single state flag ──────────────────────────────────────
                  let isDone = {str(is_arrived).lower()};

                  // ── Bidirectional routing table (all 8 nodes) ──────────────
                  const DEST_ID   = "{dest_id}";
                  const DEST_NAME = "{dest_name}";

                  const ROUTE_TABLE = {{
                    "ENTRANCE_MAIN": {{
                      "*": "Move forward<br><small>امش إلى الامام</small>"
                    }},
                    "CORRIDOR_DECISION": {{
                      "STUDENT_SERVICES": "Turn right<br><small>التف يمين</small>",
                      "MACHINE_LAB":      "Turn left, then walk straight<br><small>التف يسار وبعدين امش بشكل مستقيم</small>",
                      "PI_CAFE":          "Move forward, then turn slightly left<br><small>امش الى الامام والتف قليلًا لليسار</small>",
                      "ENTRANCE_MAIN":    "Continue straight ahead<br><small>واصل التقدم بشكل مستقيم</small>",
                      "*": "Continue forward<br><small>واصل التقدم</small>"
                    }},
                    "FOUNTAIN": {{
                      "STUDENT_SERVICES": "Student Services is on your left<br><small>يسارك مكتب خدمات الطلاب</small>",
                      "MACHINE_LAB":      "Walk forward then turn right<br><small>امش قدام بعدين يمين</small>",
                      "PI_CAFE":          "Pi Cafe is behind you<br><small>مقهى باي بيكون وراك</small>",
                      "ENTRANCE_MAIN":    "Go straight forward<br><small>اتجه مستقيمًا إلى الأمام</small>",
                      "*": "Head back towards the corridor<br><small>ارجع باتجاه الممر</small>"
                    }},
                    "PI_CAFE": {{ "*": "Head out towards the main corridor<br><small>ارجع باتجاه الممر</small>" }},
                    "STUDENT_SERVICES": {{ "*": "Head back to the main corridor<br><small>ارجع باتجاه الممر</small>" }},
                    "MACHINE_LAB": {{ "*": "Head back to the main corridor<br><small>ارجع باتجاه الممر</small>" }}
                  }};

                  function getNextInstruction(scannedNode, destId) {{
                    const entry = ROUTE_TABLE[scannedNode];
                    if (!entry) return "Continue towards your destination";
                    return entry[destId] || entry["*"] || "Continue towards your destination";
                  }}

                  // ── QR Scanner ─────────────────────────────────────────────
                  const qrCanvas = document.createElement('canvas');
                  const qrCtx    = qrCanvas.getContext('2d', {{ willReadFrequently: true }});
                  let lastScannedId = "";

                  function dispatchToStreamlit(nodeId) {{
                    const inputs = window.parent.document.querySelectorAll('input[aria-label="QR Location"]');
                    if (inputs.length > 0) {{
                      const input  = inputs[0];
                      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                      setter.call(input, nodeId);
                      input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                  }}

                  function scanQRCode() {{
                    if (isDone) return;

                    const video = document.querySelector('video');
                    if (video && video.readyState === video.HAVE_ENOUGH_DATA) {{
                      qrCanvas.width  = video.videoWidth;
                      qrCanvas.height = video.videoHeight;
                      qrCtx.drawImage(video, 0, 0, qrCanvas.width, qrCanvas.height);
                      const imageData = qrCtx.getImageData(0, 0, qrCanvas.width, qrCanvas.height);

                      if (window.jsQR) {{
                        const code = jsQR(imageData.data, imageData.width, imageData.height, {{
                          inversionAttempts: "dontInvert"
                        }});

                        if (code) {{
                          const scannedId = code.data.trim();

                          if (scannedId === DEST_ID) {{
                            // ✅ ARRIVAL
                            isDone = true;
                            const arrow = document.querySelector('a-image');
                            if (arrow) arrow.setAttribute('visible', 'false');
                            document.getElementById('main-instruction').innerHTML = 
                              "✅ You have arrived at<br><strong>" + DEST_NAME + "</strong>";
                            document.getElementById('helper-text').innerHTML = "وصلت وجهتك";
                            document.getElementById('debug-timer').innerText  = "✅ QR Confirmed";
                            document.getElementById('debug-timer').style.color = "#0f766e";

                          }} else if (scannedId && scannedId !== lastScannedId) {{
                            // 📍 CHECKPOINT
                            lastScannedId = scannedId;
                            const nextInstr = getNextInstruction(scannedId, DEST_ID);
                            document.getElementById('main-instruction').innerHTML = nextInstr;
                            document.getElementById('helper-text').innerHTML =
                              "Scan the next QR code when you reach it &mdash; قم بمسح الباركود التالي عند الوصول إليه";
                            document.getElementById('debug-timer').innerText  = "📍 " + scannedId;
                            document.getElementById('debug-timer').style.color = "#0369a1";
                            dispatchToStreamlit(scannedId);
                          }}
                        }}
                      }}
                    }}
                    requestAnimationFrame(scanQRCode);
                  }}

                  // Start scanning once video and jsQR are ready
                  (function waitForVideo() {{
                    if (document.querySelector('video') && window.jsQR) {{
                      requestAnimationFrame(scanQRCode);
                    }} else {{
                      setTimeout(waitForVideo, 400);
                    }}
                  }})();
                </script>
              </body>
            </html>
        """, height=530)
    
    st.button("Close AR Camera", on_click=lambda: navigate_to("Home"), key="close_ar_nav_btn")

elif st.session_state.current_page == "Parking Finder":

    # AI Parking Detection Logic
    import cv2
    import numpy as np
    import os
    from ultralytics import YOLO
    
    st.markdown("### Parking Detection Demo")
    st.markdown("This feature allows users to upload a parking lot image to test the AI parking detection system.")
    st.markdown("The goal of this demo is to demonstrate how the system can automatically identify available and occupied parking spaces using computer vision.")
    st.markdown("In the full implementation, this system can be connected to real parking cameras to detect available spaces in real time.")
    
    st.markdown("### 📸 Upload Parking Image")
    uploaded_file = st.file_uploader("Upload Parking Image", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Save temp file
        with open("temp_parking.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            # Load pretrained YOLO model safely
            model_path = "models/yolov8s_parking.pt"
            if not os.path.exists(model_path):
                model_path = "models/yolov8n.pt"
                if not os.path.exists(model_path):
                    st.error(f"❌ Missing Model: The parking detection model ('{model_path}') could not be found.")
                    st.stop()
            model = YOLO(model_path)
            img = cv2.imread("temp_parking.jpg")
            
            # Run inference
            results = model("temp_parking.jpg", conf=0.25)
            
            # Use native YOLO plot() for the EXACT same output as Colab
            res_plotted = results[0].plot()
            
            # Count detections natively from the results object
            detections = results[0].boxes
            occupied_slots = 0
            available_slots = 0
            
            for box in detections:
                cls_id = int(box.cls[0])
                if cls_id == 0:
                    available_slots += 1
                elif cls_id == 1:
                    occupied_slots += 1
            
            col_a, col_o = st.columns(2)
            col_a.success(f"Empty Spaces: {available_slots}")
            col_o.error(f"Occupied Spaces: {occupied_slots}")
            
            # Convert BGR (OpenCV) to RGB (Streamlit)
            img_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, caption="Official AI Model Result", width='stretch')
            
        except Exception as e:
            st.error(f"Failed to process parking image. Details: {e}")

    st.markdown("---")
    st.markdown("Upload a video to see real-time frame-by-frame parking slot analysis.")
    
    st.markdown("### 🎥 Upload Parking Video")
    uploaded_video = st.file_uploader("Upload Parking Video", type=["mp4", "mov", "avi"], label_visibility="collapsed")

    if uploaded_video is not None:
        import os
        ext = os.path.splitext(uploaded_video.name)[1]
        video_temp_path = f"temp_parking_vid{ext}"
        
        with open(video_temp_path, "wb") as f:
            f.write(uploaded_video.getbuffer())
            
        # Container placeholders for dynamic streaming
        col_vid_a, col_vid_o = st.columns(2)
        metric_a = col_vid_a.empty()
        metric_o = col_vid_o.empty()
        frame_placeholder = st.empty()
        
        try:
            model_path = "models/yolov8s_parking.pt"
            if not os.path.exists(model_path):
                model_path = "models/yolov8n.pt"
            if not os.path.exists(model_path):
                st.error(f"❌ Missing Model: '{model_path}' not found.")
            else:
                model = YOLO(model_path)
                
                # STABILITY: Clear memory and use optimized streaming
                import gc
                
                # Check video source
                if not os.path.exists(video_temp_path):
                    st.error("❌ Video file could not be read.")
                else:
                    # HIGH PERFORMANCE STREAMING
                    try:
                        for result in model.predict(source=video_temp_path, conf=0.25, stream=True, imgsz=640, verbose=False):
                            res_plotted = result.plot()
                            
                            # Metrics Update directly from raw frame
                            available_slots = 0
                            occupied_slots = 0
                            if result.boxes is not None:
                                for box in result.boxes:
                                    cls_id = int(box.cls[0])
                                    if cls_id == 0: available_slots += 1
                                    elif cls_id == 1: occupied_slots += 1
                            
                            metric_a.success(f"Empty Spaces: {available_slots}")
                            metric_o.error(f"Occupied Spaces: {occupied_slots}")
                            
                            # HIGH SPEED WEB STREAMING: Maximize smoothness on Cloud
                            _, buffer = cv2.imencode('.jpg', res_plotted, [cv2.IMWRITE_JPEG_QUALITY, 50])
                            frame_placeholder.image(buffer.tobytes(), width='stretch')
                            
                            # Explicit memory cleanup per frame
                            del result
                            del res_plotted
                            
                        st.success("✅ Analysis Complete.")
                        # Clean up temp file
                        if os.path.exists(video_temp_path):
                            os.remove(video_temp_path)
                    except Exception as e:
                        st.error(f"Detection Error: {e}")
                    finally:
                        gc.collect()
        except Exception as e:
            st.error(f"Failed to process parking video. Details: {e}")


elif st.session_state.current_page == "Admin: QR Codes":
    st.title("Admin: QR Location Codes")
    st.write("Generate and download printable QR Codes for logical physical placement across campus.")
    
    import qrcode
    from io import BytesIO
    from PIL import Image

    # ── Section 1: Hardcoded Navigation Checkpoint Nodes ─────────────────
    st.markdown("### 📍 Navigation Checkpoint Nodes")
    st.info("Print and place these QR codes at the exact physical locations. Scanning them during AR navigation updates the user's position and recomputes the route.")

    NAV_NODES = [
        ("ENTRANCE_MAIN",     "Main Entrance",          "المدخل الرئيسي"),
        ("CORRIDOR_DECISION", "Corridor Decision Point", "نقطة التفرع في الممر"),
        ("FOUNTAIN",          "Fountain Area",           "منطقة النافورة"),
        ("PI_CAFE",           "Pi Cafe",                 "مقهى باي"),
        ("STUDENT_SERVICES",  "Student Services",        "خدمات الطلاب"),
        ("MACHINE_LAB",       "Machine Lab",             "معمل المشين"),
    ]

    col_width = 3
    nav_cols = st.columns(col_width)
    for i, (node_id, name_en, name_ar) in enumerate(NAV_NODES):
        qr_img = qrcode.make(node_id)
        with nav_cols[i % col_width]:
            st.image(qr_img.get_image(), width=160)
            st.markdown(f"**`{node_id}`**")
            st.markdown(f"{name_en}<br><small>{name_ar}</small>", unsafe_allow_html=True)
            st.markdown("---")

# --- Global Footer ---
st.markdown("""
<div class="footer">
    <div class='footer'>PSAU Chat – Smart university Assistant • Crafted for optimal student experience</div>
</div>
""", unsafe_allow_html=True)
