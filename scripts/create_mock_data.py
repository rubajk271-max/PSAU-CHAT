import pandas as pd
import os

# Create data for Doctors
doctors_data = {
    'Name': ['Dr. Ahmed', 'Dr. Sarah', 'Dr. Khalid', 'Dr. Reem', 'Dr. Fahad'],
    'Course': ['Programming 101', 'Data Structures', 'Database Systems', 'Software Engineering', 'AI & Machine Learning'],
    'Email': ['ahmed@psau.edu.sa', 'sarah@psau.edu.sa', 'khalid@psau.edu.sa', 'reem@psau.edu.sa', 'fahad@psau.edu.sa'],
    'Room': ['E-101', 'E-102', 'E-201', 'E-205', 'E-301']
}

# Create data for Courses
courses_data = {
    'Name': ['Programming 101', 'Data Structures', 'Database Systems', 'Software Engineering', 'AI & Machine Learning', 'Calculus I', 'Physics II'],
    'Level': [1, 3, 5, 7, 8, 1, 2],
    'Days': ['Mon-Wed', 'Sun-Tue', 'Mon-Wed', 'Thu', 'Sun-Tue', 'Sun-Tue-Thu', 'Mon-Wed'],
    'Time': ['08:00-10:00', '10:00-12:00', '13:00-15:00', '08:00-11:00', '13:00-15:00', '08:00-09:00', '10:00-12:00'],
    'Professor': ['Dr. Ahmed', 'Dr. Sarah', 'Dr. Khalid', 'Dr. Reem', 'Dr. Fahad', 'Dr. Omar', 'Dr. Yasser']
}

# Create data for Rooms
rooms_data = {
    'Name': ['E-101', 'E-102', 'E-201', 'E-205', 'E-301', 'Lab-1', 'Lab-2'],
    'Floor': [1, 1, 2, 2, 3, 1, 2],
    'Type': ['Office', 'Office', 'Office', 'Office', 'Office', 'Laboratory', 'Laboratory']
}

# DataFrames
df_doctors = pd.DataFrame(doctors_data)
df_courses = pd.DataFrame(courses_data)
df_rooms = pd.DataFrame(rooms_data)

# Save to Excel
df_doctors.to_excel('doctors.xlsx', index=False)
df_courses.to_excel('courses.xlsx', index=False)
df_rooms.to_excel('rooms.xlsx', index=False)

# Create Mock References with Links
references_data = {
    'Course name': [
        'Programming 101', 'Data Structures', 'Database Systems', 
        'Software Engineering', 'AI & Machine Learning', 'Calculus I', 'Physics II'
    ],
    'Reference': [
        'Programming 101 Official Book.pdf', 'Data Structures Notes.pdf', 'Database Systems Slide Deck.pptx',
        'SE Reference Manual.pdf', 'AI Fundamentals Slides.pdf', 'Calculus I Handout.pdf', 'Physics II Lab Manual.pdf'
    ],
    'Link': [
        'https://drive.google.com/file/d/mock1/view', 'https://drive.google.com/file/d/mock2/view', 'https://drive.google.com/file/d/mock3/view',
        'https://drive.google.com/file/d/mock4/view', 'https://drive.google.com/file/d/mock5/view', 'https://drive.google.com/file/d/mock6/view', 'https://drive.google.com/file/d/mock7/view'
    ]
}
df_references_mock = pd.DataFrame(references_data)
df_references_mock.to_excel('references.xlsx', index=False)

print("Mock data files created successfully: doctors.xlsx, courses.xlsx, rooms.xlsx")
