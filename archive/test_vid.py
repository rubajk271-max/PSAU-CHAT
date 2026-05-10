import streamlit as st
import cv2
import numpy as np

img = np.zeros((100, 100, 3), dtype=np.uint8)
try:
    st.image(img, width='stretch')
    print("SUCCESS width='stretch'")
except Exception as e:
    print(f"ERROR: {e}")
