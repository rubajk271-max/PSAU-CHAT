# 🎓 PSAU Smart University Assistant

An intelligent, interactive university assistant developed for Prince Sattam bin Abdulaziz University (PSAU).

This system is designed to enhance the university experience by providing a unified platform that integrates multiple academic and campus services using AI.

---

## 📌 Project Overview

PSAU Chat is a smart web-based application built using **Streamlit** and **Google Gemini AI**. It combines multiple university systems into a single, intuitive interface.

The system allows students, faculty, and staff to interact with university data using natural language and specialized smart tools.

### Key Capabilities:
* **AI-Powered Conversations**: Support for Arabic & English.
* **Academic Info Retrieval**: Doctors, courses, and references.
* **Smart Schedule Generation**: Automated conflict-free scheduling.
* **Indoor Campus Navigation**: Search for rooms and offices.
* **AR Navigation (Prototype)**: Augmented Reality guidance using QR codes.
* **AI Parking Finder (Prototype)**: Real-time parking detection demo.

---

## ⚙️ Key Features

### 💬 AI Chat Assistant
A smart chatbot powered by **Google Gemini AI**.
* **Multilingual**: Understands and responds in Arabic and English.
* **Knowledgeable**: Answers questions about faculty, courses, and services.
* **Integrated**: Can redirect users to specific features like Navigation or Scheduling.

### 👨‍🏫 Doctor Finder System
A dedicated search system for university instructors.
* **Searchable**: Find by name, course name, or course code.
* **Comprehensive**: Displays emails, office locations, and taught courses.
* **Smart Navigation**: Includes a direct link to navigate to the doctor's office.

### 📅 Smart Schedule Generator
An intelligent scheduling system to simplify academic planning.
* **Automated**: Generates schedules based on level and preferences.
* **Conflict-Free**: Automatically avoids time overlaps.
* **Exportable**: Save your generated schedule as a CSV file.

### 🏢 Building Navigation & AR
Smart indoor navigation to find rooms, labs, and offices.
* **Floor-Aware**: Provides specific floor and direction details.
* **AR Prototype**: Uses QR code scanning for precise step-by-step guidance in Augmented Reality.

### 🚗 AI Parking Finder (Prototype)
A Computer Vision demo for parking management.
* **Detection**: Identifies available vs. occupied spots.
* **AI-Driven**: Uses YOLOv8 for accurate object detection from images/videos.

---

## 📂 Project Structure

```text
PSAU-CHAT/
│
├── app.py                      # Main Streamlit application
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (GEMINI_API_KEY)
│
├── data/                       # Excel database files
│   ├── doctors.xlsx
│   ├── courses.xlsx
│   ├── rooms.xlsx
│   ├── navigation_updated.xlsx
│   ├── level.xlsx
│   └── references.xlsx
│
├── assets/                     # UI Assets and Logos
│   ├── logo1.png
│   └── logo1_transparent.png
│
└── yolov8s_parking.pt          # AI Model for parking detection
```

---

## ▶️ How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Create a `.env` file and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Launch the App**:
   ```bash
   streamlit run app.py
   ```

---

## 👩‍💻 The Team
* **Ruba Salman** – Team Leader (Electrical Engineering)
* **Ameera Fahad** – Reviewer
* **Muneera Abdulrahman** – Developer
* **Nadine Ali** – Programmer
* **Nora Fahad** – Designer

---

## 📧 Contact
For inquiries, please contact: [rubajk271@gmail.com](mailto:rubajk271@gmail.com)

---
*Note: This project was developed as a prototype to demonstrate the potential of AI in enhancing the university environment.*
