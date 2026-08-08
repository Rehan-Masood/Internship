import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PixelMetrics Studio — Image Analytics & Processing",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM DARK DASHBOARD STYLES ---
st.markdown(
    """
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; }
    .stButton>button { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: #000; font-weight: bold; border: none; border-radius: 6px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("🖼️ PixelMetrics.Studio")
st.sidebar.caption("Image Processing & Feature Extraction Workbench")

# --- SIDEBAR CONTROL PANEL ---
uploaded_file = st.sidebar.file_uploader(
    "Upload Source Image", type=["jpg", "jpeg", "png"]
)

filter_mode = st.sidebar.selectbox(
    "Select Processing Filter",
    [
        "Original Image",
        "Grayscale Conversion",
        "Canny Edge Detection",
        "Gaussian Blur",
        "Binary Thresholding",
    ],
)

# Filter Parameter Controls
blur_kernel = 5
canny_thresh1 = 100
canny_thresh2 = 200
threshold_val = 127

if filter_mode == "Gaussian Blur":
  blur_kernel = st.sidebar.slider("Blur Kernel Size", 1, 25, 5, step=2)
elif filter_mode == "Canny Edge Detection":
  canny_thresh1 = st.sidebar.slider("Threshold 1", 10, 300, 100)
  canny_thresh2 = st.sidebar.slider("Threshold 2", 10, 300, 200)
elif filter_mode == "Binary Thresholding":
  threshold_val = st.sidebar.slider("Threshold Value", 0, 255, 127)

# --- MAIN DASHBOARD WORKSPACE ---
st.title("⚡ Image Analytics & Feature Profiler")

if uploaded_file is None:
  st.info("👈 Upload an image from the sidebar to start processing.")
else:
  # Load Image into PIL and OpenCV formats
  image_pil = Image.open(uploaded_file)
  img_np = np.array(image_pil)

  # Convert RGB to BGR for OpenCV processing
  if len(img_np.shape) == 3:
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
  else:
    img_bgr = img_np

  # Apply Image Processing Filters
  if filter_mode == "Grayscale Conversion":
    processed_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
  elif filter_mode == "Gaussian Blur":
    processed_bgr = cv2.GaussianBlur(
        img_bgr, (blur_kernel, blur_kernel), cv2.BORDER_DEFAULT
    )
  elif filter_mode == "Canny Edge Detection":
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    processed_bgr = cv2.Canny(gray, canny_thresh1, canny_thresh2)
  elif filter_mode == "Binary Thresholding":
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, processed_bgr = cv2.threshold(
        gray, threshold_val, 255, cv2.THRESH_BINARY
    )
  else:
    processed_bgr = img_bgr

  # Convert processed result back for Streamlit rendering
  if len(processed_bgr.shape) == 2:  # Single channel / Gray
    processed_rgb = cv2.cvtColor(processed_bgr, cv2.COLOR_GRAY2RGB)
  else:
    processed_rgb = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)

  # --- TOP METRICS CARDS ---
  height, width = img_np.shape[0], img_np.shape[1]
  channels = img_np.shape[2] if len(img_np.shape) == 3 else 1
  aspect_ratio = round(width / height, 2)

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Width x Height", f"{width} x {height} px")
  col2.metric("Color Channels", channels)
  col3.metric("Aspect Ratio", f"{aspect_ratio}:1")
  col4.metric(
      "Pixel Mean Intensity", f"{round(np.mean(img_np), 2)} / 255"
  )

  st.markdown("---")

  # --- VISUAL PREVIEW ---
  col_left, col_right = st.columns(2)

  with col_left:
    st.subheader("Source Input")
    st.image(image_pil, use_container_width=True)

  with col_right:
    st.subheader(f"Processed Output ({filter_mode})")
    st.image(processed_rgb, use_container_width=True)

  st.markdown("---")

  # --- DATA SCIENCE & ANALYTICS SECTION ---
  st.subheader("📊 RGB Color Channel Intensity Distribution")

  if len(img_np.shape) == 3:
    fig = go.Figure()
    colors = ["red", "green", "blue"]

    for i, color in enumerate(colors):
      hist, bins = np.histogram(img_np[:, :, i], bins=256, range=[0, 256])
      fig.add_trace(
          go.Scatter(
              x=bins[:-1],
              y=hist,
              name=f"{color.capitalize()} Channel",
              line=dict(color=color, width=2),
          )
      )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Pixel Value (0-255)",
        yaxis_title="Pixel Count Frequency",
        margin=dict(l=20, r=20, t=30, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)
  else:
    st.info("Single-channel image uploaded. Color distribution chart omitted.")