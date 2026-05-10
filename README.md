<div align="center">

# 🎓 PSAU Smart University Assistant
### Your All-in-One Intelligent Campus Companion
---
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 🌟 Project Vision
**PSAU Chat** is a state-of-the-art web application developed for **Prince Sattam bin Abdulaziz University (PSAU)**. It leverages AI to bridge the gap between students, faculty, and campus services, providing a seamless, intelligent experience in both Arabic and English.

---

## 🚀 Core Features

<table align="center">
  <tr>
    <td align="center"><b>💬 AI Assistant</b><br>Intelligent bilingual chatbot for all your university queries.</td>
    <td align="center"><b>👨‍🏫 Doctor Finder</b><br>Quickly locate professors, emails, and office locations.</td>
  </tr>
  <tr>
    <td align="center"><b>📅 Smart Schedule Generator</b><br>Generate conflict-free academic schedules automatically.</td>
    <td align="center"><b>🏢 Building Navigation</b><br>Smart indoor navigation to every classroom and lab.</td>
  </tr>
  <tr>
    <td align="center"><b>📱 AR Navigation</b><br>Innovative Augmented Reality guidance via QR codes.</td>
    <td align="center"><b>🚗 AI Parking Availability Demo</b><br>AI-powered parking spot detection for a stress-free arrival.</td>
  </tr>
</table>

---

## 📂 Repository Structure
```text
PSAU-CHAT/
├── app.py                 # Core Application Engine (Streamlit)
├── LICENSE                # Usage Rights (MIT)
├── requirements.txt       # Dependencies (YOLO, Gemini, OpenCV)
├── data/                  # Knowledge Base (Courses, Doctors, Navigation Excel)
│   ├── level.xlsx         # Study Plans
│   ├── references.xlsx    # Course Materials
│   └── navigation_updated.xlsx # AR Graph Data
├── assets/images/         # UI Assets, Logos, and Backgrounds
├── models/                # Trained YOLOv8 AI Models for Parking
├── scripts/               # Utility scripts for data processing
├── archive/               # Project backups and temporary test files
└── docs/                  # Project Documentation & Reports
```

---

## ⚡ Technical Highlights
- **Gemini 1.5 Flash:** Powered by advanced LLM for natural language department-specific queries.
- **YOLOv8 Computer Vision:** Real-time analysis of parking lot occupancy.
- **Load Balancing (API Rotation):** Supports multiple Gemini API keys to ensure high availability and prevent rate-limiting during high-traffic presentations.
- **AR Pathfinding:** Implements Dijkstra's algorithm for optimal indoor routing.

---

## 🛠️ Getting Started

### 1️⃣ Clone & Install
```bash
git clone https://github.com/rubajk271-max/PSAU-CHAT.git
pip install -r requirements.txt
```

### 2️⃣ Environment Setup
Create a `.env` file from the provided template:
```bash
cp .env.example .env
# Edit .env with your GEMINI_API_KEY
```

### 3️⃣ Run Locally
```bash
streamlit run app.py
```

---

## 🌍 Deployment (Public Link)
Check out the live version here:
🔗 **[psau-chat.streamlit.app](https://psau-chat-8ckfwzbj9jvrdf3xjp6a83.streamlit.app/)**

---

## 🤝 The Team
*   **Ruba Salman** – Project Lead
*   **Ameera Fahad** – Reviewer & QA
*   **Muneera Abdulrahman** – Core Developer
*   **Nadine Ali** – Logic Programmer
*   **Nora Fahad** – UI/UX Designer

---

<div align="center">
  <p><i>Developed with ❤️ for PSAU Students and Faculty</i></p>
</div>
