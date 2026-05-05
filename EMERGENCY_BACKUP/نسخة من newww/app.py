import streamlit as st
import pandas as pd
import os
from PIL import Image
from thefuzz import process, fuzz
import streamlit.components.v1 as components

# --- Page Config & Styling ---
try:
    page_icon_logo = Image.open('logo1_transparent.png')
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
        text-align: right;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 80%;
    }
    .bot-msg {
        background: rgba(15, 118, 110, 0.08);
        color: inherit;
        border: 1px solid rgba(15, 118, 110, 0.2);
        padding: 12px 16px;
        border-radius: 16px 16px 16px 0;
        margin-bottom: 1rem;
        text-align: left;
        display: inline-block;
        float: left;
        clear: both;
        max-width: 80%;
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
        doctors_old = pd.read_excel('doctors.xlsx')
        courses_old = pd.read_excel('courses.xlsx')
        rooms = pd.read_excel('rooms.xlsx')
        df_locations = pd.read_excel('navigation_updated.xlsx', sheet_name='locations')
        df_paths = pd.read_excel('navigation_updated.xlsx', sheet_name='paths')
        df_keywords = pd.read_excel('navigation_updated.xlsx', sheet_name='keywords')
        
        # New Excel Files
        df_docs = pd.read_excel('doctorsEE(1).xlsx')
        # Fill merged cells for doctor names and emails
        df_docs['Doctor name'] = df_docs['Doctor name'].ffill()
        df_docs['Email'] = df_docs['Email'].ffill()
        df_docs['Location'] = df_docs['Location'].ffill()
        
        df_level_core = pd.read_excel('level.xlsx', sheet_name=0)
        df_level_elec = pd.read_excel('level.xlsx', sheet_name=1)
        
        try:
            df_references = pd.read_excel('references.xlsx')
        except FileNotFoundError:
            df_references = pd.DataFrame(columns=['Course name', 'Reference'])

        
        # --- USER MANDATORY NAMING OVERRIDES ---
        room_replacements = {
            "Library": "Student Services / مكتب خدمات الطلاب",
            "Library / المكتبة": "Student Services / مكتب خدمات الطلاب",
            "Lab 1": "Machine Lab / معمل المشين",
            "Lab-1": "Machine Lab / معمل المشين",
            "Lab 2": "Electronics Lab / معمل الإلكترونيات",
            "Lab-2": "Electronics Lab / معمل الإلكترونيات",
            "Class 1": "Classroom A / قاعة A",
            "Classroom 1": "Classroom A / قاعة A",
            "Class 2": "Classroom B / قاعة B",
            "Classroom 2": "Classroom B / قاعة B",
            "Dr. Malek Office": "Dr. Malek Office / مكتب دكتور مالك الدهيمي",
            "Dr. Muhannad Office": "Dr. Muhannad Office / مكتب دكتور مهند الشتيوي"
        }
        rooms['Name'] = rooms['Name'].replace(room_replacements)
        if not df_keywords.empty:
            df_keywords['Keyword'] = df_keywords['Keyword'].replace(room_replacements)
            
        for i, row in df_locations.iterrows():
            en_val = str(row['Name_EN']).strip()
            if "Library" in en_val:
                df_locations.at[i, 'Name_EN'] = "Student Services"
                df_locations.at[i, 'Name_AR'] = "مكتب خدمات الطلاب"
            elif "Lab" in en_val and "1" in en_val:
                df_locations.at[i, 'Name_EN'] = "Machine Lab"
                df_locations.at[i, 'Name_AR'] = "معمل المشين"
            elif "Lab" in en_val and "2" in en_val:
                df_locations.at[i, 'Name_EN'] = "Electronics Lab"
                df_locations.at[i, 'Name_AR'] = "معمل الإلكترونيات"
            elif "Class" in en_val and "1" in en_val:
                df_locations.at[i, 'Name_EN'] = "Classroom A"
                df_locations.at[i, 'Name_AR'] = "قاعة A"
            elif "Class" in en_val and "2" in en_val:
                df_locations.at[i, 'Name_EN'] = "Classroom B"
                df_locations.at[i, 'Name_AR'] = "قاعة B"
            elif "Malek" in en_val or "مالك" in str(row['Name_AR']):
                df_locations.at[i, 'Name_EN'] = "Dr. Malek Office"
                df_locations.at[i, 'Name_AR'] = "مكتب دكتور مالك الدهيمي"
            elif "Muhannad" in en_val or "مهند" in str(row['Name_AR']):
                df_locations.at[i, 'Name_EN'] = "Dr. Muhannad Office"
                df_locations.at[i, 'Name_AR'] = "مكتب دكتور مهند الشتيوي"
                
        # Inject the new Admissions node to the pathfinding graph logically attached to the origin node
        if not df_locations.empty and not any(df_locations['Name_EN'].astype(str).str.contains("Admissions")):
            anchor = "N_M" if "N_M" in df_locations['Node_ID'].values else df_locations['Node_ID'].iloc[0]
            new_node = pd.DataFrame([{
                'Node_ID': 'N_ADMISSIONS',
                'Name_EN': 'Admissions & Registration Office',
                'Name_AR': 'مكتب القبول والتسجيل',
                'Type': 'Office',
                'Floor': 1,
                'Ref_RoomID': 'Admissions',
                'StartPoint': 'no'
            }])
            df_locations = pd.concat([df_locations, new_node], ignore_index=True)
            if not df_paths.empty and not any(df_paths['ToNode'] == 'N_ADMISSIONS'):
                new_path1 = pd.DataFrame([{'FromNode': anchor, 'ToNode': 'N_ADMISSIONS', 'Distance': 5, 'Direction': 'Turn Right'}])
                new_path2 = pd.DataFrame([{'FromNode': 'N_ADMISSIONS', 'ToNode': anchor, 'Distance': 5, 'Direction': 'Turn Left'}])
                df_paths = pd.concat([df_paths, new_path1, new_path2], ignore_index=True)
                
        return doctors_old, courses_old, rooms, df_docs, df_level_core, df_level_elec, df_locations, df_paths, df_keywords, df_references
    except Exception as e:
        st.error(f"Error loading data. {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_doctors_old, df_courses_old, df_rooms, df_docs, df_level_core, df_level_elec, df_locations, df_paths, df_keywords, df_references = load_data()

# Build search corpuses for fuzzy matching
doctor_names = df_docs['Doctor name'].dropna().unique().tolist() if not df_docs.empty else []
room_names = df_rooms['Name'].astype(str).tolist() if not df_rooms.empty else []
room_names.extend(df_keywords['Keyword'].dropna().astype(str).tolist() if not df_keywords.empty else [])

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
    if os.path.exists('logo1.png'):
        st.image('logo1.png', width=150)
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
        if os.path.exists('logo1_transparent.png'):
            try:
                st.image('logo1_transparent.png', use_container_width=True)
            except:
                st.image('logo1.png', use_container_width=True)
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
        if os.path.exists('logo1_transparent.png'):
            st.image('logo1_transparent.png', use_container_width=True)
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
        • "Who teaches Software Engineering?" <br>
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
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "bot" and not msg["content"].startswith("nav_trigger:"):
            st.markdown(f"<div class='bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
            
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
            
    query = st.text_input("Type your question here...")
    
    if st.button("Send") and query:
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Helper to format doctor response cleanly
        def format_doctor_card(doc_row, include_courses=True):
            name = doc_row['Doctor name']
            email = doc_row['Email']
            location = doc_row['Location']
            website = doc_row.get('Website', None) if 'Website' in doc_row else None
            
            card_html = f"<div class='data-card'><h4>👨‍🏫 Doctor: <b>{name}</b></h4><p>📧 <b>Email:</b> <a href='mailto:{email}'>{email}</a></p>"
            
            if pd.notna(location):
                card_html += f"<p>📍 <b>Office:</b> {location}</p>"
                
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
                        response = f"<div class='data-card'><h4>📖 Course: <b>{doc_info['Course name']}</b></h4><p>🔢 <b>Course Code:</b> {course_code}</p><p>👨‍🏫 <b>Doctor Name:</b> {doc_info['Doctor name']}</p><p>📧 <b>Email:</b> <a href='mailto:{doc_info['Email']}'>{doc_info['Email']}</a></p><p>📍 <b>Office:</b> {doc_info['Location'] if pd.notna(doc_info['Location']) else 'Coming soon'}</p></div>"
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
            elif any(w in query_norm for w in ['مسار', 'مسارات', 'تخصص', 'وش مسارات', 'track', 'tracks', 'specialization']):
                if any(w in query_norm for w in ['power', 'قوى', 'طاقة']):
                    response = "<div class='data-card'><h4>⚡ Power Track (مسار القوى والطاقة)</h4><p>Focuses on power systems, electrical machines, energy generation, transmission, and distribution.</p><p>يركز على أنظمة الطاقة، الآلات الكهربائية، وتوليد ونقل الكهرباء.</p><p><i>ملاحظة هامة: المسار لا يُكتب في وثيقة التخرج، جميع الطلاب يتخرجون بشهادة بكالوريوس في الهندسة الكهربائية.</i></p></div>"
                elif any(w in query_norm for w in ['communications', 'اتصالات', 'communication']):
                    response = "<div class='data-card'><h4>📡 Communications Track (مسار الاتصالات)</h4><p>Focuses on communication systems, signal processing, wireless communication, and networking technologies.</p><p>يركز على أنظمة الاتصالات، معالجة الإشارات والشبكات اللاسلكية.</p><p><i>ملاحظة هامة: المسار لا يُكتب في وثيقة التخرج، جميع الطلاب يتخرجون بشهادة بكالوريوس في الهندسة الكهربائية.</i></p></div>"
                else:
                    response = "<div class='data-card'><h4>🛤️ Electrical Engineering Tracks (مسارات القسم)</h4><p>يوجد مسارين رئيسيين في الخطة الدراسية:</p><p><b>1. Communications Track (مسار الاتصالات)</b></p><p><b>2. Power Track (مسار القوى)</b></p><br><p>الفروقات تتركز في بعض المواد المتقدمة وكذلك في <b>مشروع التخرج</b>.</p><p>الوثيقة النهائية للتخرج تصدر باسم <b>الهندسة الكهربائية</b> بشكل عام دون تحديد المسار.</p></div>"

        # 2. Check for Level Queries (English or Arabic)
        if not response and any(w in query_norm for w in ['level', 'lvl', 'مستوى', 'المستوى', 'لفل']):
            try:
                import re
                
                # Convert Arabic text numbers and numerals to digits for the regex reader
                arabic_to_num = {
                    'واحد': '1', 'الاول': '1', 'أول': '1', 'اول': '1', '١': '1',
                    'اثنين': '2', 'الثاني': '2', 'ثاني': '2', 'ثنتين': '2', '٢': '2',
                    'ثلاثة': '3', 'الثالث': '3', 'ثالث': '3', 'ثلاث': '3', '٣': '3',
                    'اربعة': '4', 'الرابع': '4', 'رابع': '4', 'اربع': '4', '٤': '4',
                    'خمسة': '5', 'الخامس': '5', 'خامس': '5', 'خمس': '5', '٥': '5',
                    'ستة': '6', 'السادس': '6', 'سادس': '6', 'ست': '6', '٦': '6',
                    'سبعة': '7', 'السابع': '7', 'سابع': '7', 'سبع': '7', 'سبعه': '7', '٧': '7',
                    'ثمانية': '8', 'الثامن': '8', 'ثامن': '8', 'ثمان': '8', '٨': '8'
                }
                
                q_mapped = query_norm
                for ar_word, digit in arabic_to_num.items():
                    q_mapped = re.sub(rf'\b{ar_word}\b', digit, q_mapped)
                
                # Find the first number in the mapped query
                numbers = re.findall(r'\d+', q_mapped)
                if numbers:
                    level_num = int(numbers[0])
                    level_str = f"Level {level_num}"
                    
                    is_elective = any(w in query_norm for w in ['اختياري', 'elective', 'electives'])
                    is_core = any(w in query_norm for w in ['اجباري', 'core', 'أساسي'])
                    
                    # If neither specific sub-type is requested, load BOTH by default for the user.
                    core_courses = []
                    elec_courses = []
                    
                    if not is_elective:
                        core_row = df_level_core[df_level_core['Level'].astype(str).str.lower() == level_str.lower()]
                        core_courses = [str(x) for x in core_row.iloc[0].values[1:] if pd.notna(x)] if not core_row.empty else []
                        
                    if not is_core:
                        elec_row = df_level_elec[df_level_elec['Level'].astype(str).str.lower() == level_str.lower()]
                        elec_courses = [str(x) for x in elec_row.iloc[0].values[1:] if pd.notna(x)] if not elec_row.empty else []
                        
                    elec_courses = []
                    # Check Elective Subjects
                    if not is_core:
                        elec_row = df_level_elec[df_level_elec['Level'].astype(str).str.lower() == level_str.lower()]
                        elec_courses = [str(x) for x in elec_row.iloc[0].values[1:] if pd.notna(x)] if not elec_row.empty else []
                    
                    # Remove duplicates and clean
                    core_courses = list(dict.fromkeys([c.strip() for c in core_courses if c.strip()]))
                    elec_courses = list(dict.fromkeys([c.strip() for c in elec_courses if c.strip()]))
                    
                    if core_courses or elec_courses or is_elective:
                        html_parts = [f"<div class='data-card'><h4>📚 {level_str.title()}</h4>"]
                        
                        if is_elective and not elec_courses:
                            html_parts.append("<p><i>There are no elective courses for this level.</i></p>")
                        else:
                            if core_courses:
                                html_parts.append("<p><b>Core subjects:</b><br>• " + "<br>• ".join(core_courses) + "</p>")
                            if elec_courses:
                                html_parts.append("<p><b>Elective subjects:</b><br>• " + "<br>• ".join(elec_courses) + "</p>")
                                
                        html_parts.append("</div>")
                        response = "".join(html_parts)
            except Exception:
                pass
                
        # 3. Extract Doctor/Subject Names with advanced matching (Fuzzy on Normalized Text)
        if not response and not df_docs.empty:
            clean_q = query_norm
            # Standard conversational fluff stripping to prevent false positive matching
            stops = ['مين', 'من', 'مادة', 'مقرر', 'ابحث', 'عن', 'في', 'الهندسة', 'كلية', 'الكلية', 'قسم', 'برنامج', 'يدرس', 'منهو']
            for s in stops:
                clean_q = re.sub(rf'\b{s}\b', '', clean_q).strip()

            clean_q = clean_q.replace('doctor', '').replace('dr ', '').replace('dr.', '').replace('دكتور', '').replace('د.', '').replace('د ', '').replace('م د', '').replace('ايميل', '').replace('email', '').replace('where is', '').replace('where', '').replace('وين', '').replace('مكان', '').replace('مكتب', '').replace('office of', '').replace('office', '').replace('how can i contact', '').replace('contact', '').replace('تواصل', '').replace('كيف اتواصل', '').replace('من يدرس', '').replace('who teaches', '').strip()
            
            # Fallback if stripping made it empty
            if not clean_q:
                clean_q = query_norm
                
            course_match_norm, course_score = process.extractOne(clean_q, list(course_map.keys()), scorer=fuzz.token_set_ratio) if course_map and len(clean_q) > 2 else (None, 0)
            doc_match_norm, doc_score = process.extractOne(clean_q, list(doc_map.keys()), scorer=fuzz.token_set_ratio) if doc_map and len(clean_q) > 2 else (None, 0)
            
            # Additional check for Course code
            code_matches = df_docs[df_docs['Course code'].astype(str).str.lower().str.contains(clean_q, na=False)]
            if not code_matches.empty and len(clean_q) > 2:
                course_score = 100
                orig_course = code_matches.iloc[0]['Course name']
            elif course_match_norm:
                orig_course = course_map[course_match_norm]
            else:
                orig_course = ""
                
            orig_doc = doc_map.get(doc_match_norm, "") if doc_match_norm else ""
            
            # Resolve collisions or pick best score
            if course_score >= doc_score and course_score > 75:
                doc_info = df_docs[df_docs['Course name'] == orig_course].iloc[0]
                
                is_reference_query = any(w in query_norm for w in ['مرجع', 'مراجع', 'ملف', 'reference', 'references', 'book', 'رابط'])
                
                if is_reference_query and not df_references.empty:
                    mask_ref = df_references['Course name'].astype(str).str.lower() == orig_course.lower()
                    refs_data = df_references[mask_ref][['Reference', 'Link']].dropna(subset=['Reference']).drop_duplicates().to_dict('records') if 'Link' in df_references.columns else []
                    
                    if not refs_data and 'Link' not in df_references.columns:
                         # fallback if link missing
                         refs_fallback = df_references[mask_ref]['Reference'].dropna().astype(str).unique().tolist()
                         refs_data = [{'Reference': r, 'Link': '#'} for r in refs_fallback]

                    if refs_data:
                        ref_html = ""
                        for r in refs_data:
                            rl = r['Link'] if pd.notna(r['Link']) else "#"
                            ref_html += f"<li><a href='{rl}' target='_blank'>{r['Reference']}</a></li>"
                        response = f"<div class='data-card'><h4>📚 References for <b>{orig_course}</b></h4><ul>{ref_html}</ul></div>"
                    else:
                        response = f"<div class='data-card'><h4>📚 References for <b>{orig_course}</b></h4><p>No external reference file associated with this course.</p></div>"
                
                else:
                    course_code = doc_info['Course code'] if pd.notna(doc_info['Course code']) else "N/A"
                    has_location = pd.notna(doc_info['Location'])
                    
                    nav_button_html = ""
                    if any(w in query_norm for w in ['where', 'location', 'مكتب', 'وين', 'مكان', 'office', 'قاعة', 'مبنى', 'building', 'room']): 
                        nav_target = doc_info['Doctor name']
                        
                    location_html = f"<p>📍 <b>Office:</b> {doc_info['Location']}</p>" if has_location else ""
                    response = f"<div class='data-card'><h4>📖 Course: <b>{doc_info['Course name']}</b></h4><p>🔢 <b>Course Code:</b> {course_code}</p><p>👨‍🏫 <b>Doctor Name:</b> {doc_info['Doctor name']}</p><p>📧 <b>Email:</b> <a href='mailto:{doc_info['Email']}'>{doc_info['Email']}</a></p>{location_html}</div>"
                
            elif doc_score > 75:
                doc_info = df_docs[df_docs['Doctor name'] == orig_doc].iloc[0]
                card_html, has_location = format_doctor_card(doc_info, include_courses=False)
                
                if any(w in query_norm for w in ['where', 'location', 'مكتب', 'وين', 'مكان', 'office', 'قاعة', 'مبنى', 'building', 'room']):
                    nav_target = doc_info['Doctor name']
                    
                response = card_html
                     
            # Partial Match Suggestion
            elif course_score > 60 and course_score >= doc_score:
                course_info_suggestion = df_docs[df_docs['Course name'] == orig_course].iloc[0]
                st.session_state.pending_suggestion = course_info_suggestion
                st.session_state.suggestion_type = 'course'
                response = f"<div class='data-card'><p>🤔 Did you mean the subject <b>{orig_course}</b>?</p></div>"
            elif doc_score > 60:
                doc_info_suggestion = df_docs[df_docs['Doctor name'] == orig_doc].iloc[0]
                st.session_state.pending_suggestion = doc_info_suggestion
                st.session_state.suggestion_type = 'doctor'
                response = f"<div class='data-card'><p>🤔 Did you mean <b>{orig_doc}</b>?</p></div>"
                    
         # 4. Room matching Fallback
        if not response:
             room_match_norm, room_score = process.extractOne(query_norm, list(room_map.keys()), scorer=fuzz.token_set_ratio) if room_map else (None, 0)
             if room_score > 85 and room_match_norm:
                 orig_room = room_map.get(room_match_norm, room_match_norm)
                 is_old_room = orig_room in df_rooms['Name'].astype(str).values if not df_rooms.empty else False
                 
                 if is_old_room:
                     room_info = df_rooms[df_rooms['Name'].astype(str) == str(orig_room)].iloc[0]
                     room_name = orig_room
                     floor = room_info['Floor']
                     rtype = room_info['Type']
                 else:
                     target_node = df_keywords.loc[df_keywords['Keyword'].astype(str) == str(orig_room), 'TargetNode'].values[0]
                     room_info = df_locations[df_locations['Node_ID'] == target_node].iloc[0]
                     room_name = f"{room_info['Name_EN']} ({room_info['Name_AR']})"
                     floor = room_info['Floor']
                     rtype = room_info['Type']
                     
                 response = f"<div class='data-card'><p>🚪 <b>{room_name}</b> is a {rtype} on Floor {floor}.</p></div>"
                 if any(w in query_norm for w in ['where', 'location', 'مكتب', 'وين', 'مكان', 'office', 'قاعة', 'مبنى', 'building', 'room']):
                     nav_target = room_name
             elif room_score > 60 and room_match_norm:
                 orig_room = room_map.get(room_match_norm, room_match_norm)
                 response = f"<div class='data-card'><p>Classroom not found. Did you mean Room <b>{orig_room}</b>?</p></div>"
                
        if not response:
             response = "<div class='data-card'><p>I'm sorry, I couldn't understand that. You can ask about a level (e.g. 'مواد لفل 8'), a subject, the EE tracks, or a doctor. 🎓</p></div>"
             
        # Append and rerun
        st.session_state.messages.append({"role": "bot", "content": response})
        if nav_target:
             st.session_state.messages.append({"role": "bot", "content": "nav_trigger:" + nav_target})
        st.rerun()

    # AR Navigation Button intercept logic is now integrated directly inside the chat display loop above.

elif st.session_state.current_page == "Doctor Finder":
    
    search_term = st.text_input("Search for a Doctor or Course:", placeholder="e.g. ahmed, math, or 1050")
    
    # Case-insensitive Smart Search
    if search_term:
        term = search_term.lower()
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
            
            location_html = f"<p><strong>📍 Office:</strong> {location}</p>" if pd.notna(location) else ""
            st.markdown(f"""
            <div class="data-card">
                <h4>👨‍🏫 Doctor: {doc_name}</h4>
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

elif st.session_state.current_page == "Building Navigation":
    room_search = st.text_input("📍 Search Room, Lab, or Doctor Office:", placeholder="e.g. 204, Library, Lab 1, المكتبة")
    
    if room_search:
        search_terms = room_search.lower().split()
        
        # 1. Match against classic rooms.xlsx (ALL terms must match for numeric rooms intuitively)
        mask_rooms = pd.Series([True] * len(df_rooms))
        for t in search_terms:
            mask_rooms &= df_rooms['Name'].astype(str).str.lower().str.contains(t, na=False)
        matched_rooms = df_rooms[mask_rooms]
        
        # 2. Match against New Navigation Keywords (ANY semantic term can match a keyword)
        matched_nodes = set()
        for t in search_terms:
            # Drop filler words like doctor to prevent dead matches
            if t not in ['دكتور', 'د', 'dr', 'doctor']:
                matches = df_keywords[df_keywords['Keyword'].astype(str).str.lower().str.contains(t, na=False)]
                matched_nodes.update(matches['TargetNode'].tolist())
        
        matched_locs = df_locations[df_locations['Node_ID'].isin(matched_nodes)] if len(matched_nodes) > 0 else pd.DataFrame()
        
        # Global tracker to prevent displaying the exact same physical room twice
        rendered_names = set()
        
        found_any = False
        
        # No restricted AR destinations; mapping allows universal nodes
        
        if not matched_rooms.empty:
            found_any = True
            for _, row in matched_rooms.iterrows():
                room_name = row['Name']
                rendered_names.add(room_name)
                
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
                    if st.button(f"Open Camera Navigation to {room_name}", key=f"cam_room_{str(room_name).replace(' ', '_')}"):
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
                if row['Name_EN'] in rendered_names:
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
        
        # Build search index explicitly from Node Names, not raw generic keywords!
        all_destinations_map = {}
        for _, row in df_rooms.iterrows():
            all_destinations_map[str(row['Name'])] = str(row['Name'])
            
        for _, row in df_locations.iterrows():
            full_name = f"{row['Name_EN']} / {row['Name_AR']}"
            all_destinations_map[full_name] = row['Node_ID']
            
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
    st.image("https://images.unsplash.com/photo-1590674899484-d564fae1ad81?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    # AI Parking Detection Logic
    import cv2
    import numpy as np
    import os
    from ultralytics import YOLO
    
    st.markdown("### Parking Detection Demo")
    st.markdown("This feature allows users to upload a parking lot image to test the AI parking detection system.")
    st.markdown("The goal of this demo is to demonstrate how the system can automatically identify available and occupied parking spaces using computer vision.")
    st.markdown("In the full implementation, this system can be connected to real parking cameras to detect available spaces in real time.")
    
    uploaded_file = st.file_uploader("Upload Parking Image", type=["png", "jpg", "jpeg", "webp"])
    
    if uploaded_file is not None:
        # Save temp file
        with open("temp_parking.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            # Load pretrained YOLO model safely
            model_path = "yolov8s_parking.pt"
            if not os.path.exists(model_path):
                st.error(f"❌ Missing Model: The parking detection model ('{model_path}') could not be found.")
                st.stop()
            model = YOLO(model_path)
            img = cv2.imread("temp_parking.jpg")
            
            # Run inference
            results = model("temp_parking.jpg", conf=0.25)
            detections = results[0].boxes
            
            occupied_slots = 0
            available_slots = 0
            
            # Process YOLO model boxes natively (Class 0: Empty, Class 1: Occupied)
            for box in detections:
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                if cls_id == 0:
                    available_slots += 1
                    # ONLY draw green boxes around available / free parking slots!
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                elif cls_id == 1:
                    occupied_slots += 1
                    # Do NOT flood image with red overlays; keep occupied subtle/unmarked
            
            col_a, col_o = st.columns(2)
            col_a.success(f"Empty Spaces: {available_slots}")
            col_o.error(f"Occupied Spaces: {occupied_slots}")
            
            # Convert BGR CV2 to RGB for Streamlit rendering; Image uses pristine overlay
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, caption="Processed AI Map (Available Free Slots in Green)", use_container_width=True)
            
        except Exception as e:
            st.error(f"Failed to process parking image. Details: {e}")

    st.markdown("---")
    if st.button("Open AR Direction", key="ar_parking"):
        navigate_to("AR Navigation")

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
