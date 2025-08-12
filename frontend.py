
import streamlit as st
from PIL import Image, ImageDraw
import time
import numpy as np
from backend import (
    byte_to_pil,
    remove_background_with_rembg,
    composite_with_color,
    validate_upload,
    prepare_download_image
)


st.set_page_config(
    page_title="Background Removal Pro | Hassan Ali",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
/* Main App Background - Sophisticated neutral */
.stApp {
    background-color: #f5f7fa;
}

/* Premium Sidebar - Dark elegant theme */
[data-testid="stSidebar"] {
    background: linear-gradient(195deg, #1e293b 0%, #0f172a 100%);
    padding-bottom: 2.5rem;
    padding-top: 0;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    box-shadow: 8px 0 25px rgba(0,0,0,0.15);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Luxury Card Design */
.card {
    background: white;
    border-radius: 14px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    padding: 2rem;
    margin-bottom: 2rem;
    margin-top: 2rem;
    border: 1px solid rgba(0,0,0,0.03);
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    border-color: rgba(0,0,0,0.05);
}

/* Executive Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    width: 100%;
    box-shadow: 0 4px 6px rgba(79, 70, 229, 0.15);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #6d28d9);
    transform: translateY(-2px);
    box-shadow: 0 7px 14px rgba(79, 70, 229, 0.25);
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #0891b2, #06b6d4);
    box-shadow: 0 4px 6px rgba(8, 145, 178, 0.15);
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0e7490, #0d9488);
    box-shadow: 0 7px 14px rgba(8, 145, 178, 0.25);
}

/* Premium Input Fields */
.stFileUploader > div > div {
    border: 2px dashed #e2e8f0;
    border-radius: 10px;
    background: rgba(226, 232, 240, 0.15);
    transition: all 0.3s ease-out;
}

.stFileUploader > div > div:hover {
    border-color: #818cf8;
    background: rgba(129, 140, 248, 0.05);
}

/* Refined Slider */
.stSlider .st-ae {
    color: #4f46e5 !important;
}

.stSlider .st-af {
    background-color: #4f46e5 !important;
    height: 4px !important;
}

.stSlider .st-bh {
    height: 16px !important;
    width: 16px !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}

/* Premium Typography */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMarkdown li {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #1e293b;
    font-weight: 700;
    letter-spacing: -0.5px;
}

h1 {
    font-size: 2.5rem !important;
    line-height: 1.2 !important;
}

/* Luxury Image Styling */
.stImage img {
    border-radius: 14px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    transition: all 0.4s ease;
    border: 1px solid rgba(0,0,0,0.03);
    background: white;
    padding: 4px;
}

.stImage img:hover {
    transform: scale(1.02);
    box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}

/* Executive Progress Bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    height: 6px !important;
    border-radius: 3px !important;
}

/* Premium Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    padding: 0 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    font-weight: 600 !important;
    background: rgba(226, 232, 240, 0.5) !important;
    color: #64748b !important;
    margin: 0 2px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2) !important;
}

/* Elegant Checkbox */
.stCheckbox [data-baseweb="checkbox"] {
    margin-right: 10px;
    border-radius: 4px !important;
    border-color: #cbd5e1 !important;
}

.stCheckbox [data-baseweb="checkbox"]:hover {
    border-color: #818cf8 !important;
}

.stCheckbox [aria-checked="true"] {
    background-color: #4f46e5 !important;
    border-color: #4f46e5 !important;
}

/* Status Messages */
.stAlert {
    border-radius: 10px !important;
}

.stSuccess {
    background-color: #f0fdf4 !important;
    color: #166534 !important;
    border-left: 4px solid #22c55e !important;
}

.stWarning {
    background-color: #fffbeb !important;
    color: #854d0e !important;
    border-left: 4px solid #f59e0b !important;
}

.stError {
    background-color: #fef2f2 !important;
    color: #991b1b !important;
    border-left: 4px solid #ef4444 !important;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .card {
        padding: 1.5rem;
    }
    
    h1 {
        font-size: 2rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


def create_gradient_background(size, start_color, end_color):
    """Create a vertical gradient background image"""
    width, height = size
    gradient = Image.new('RGB', size)
    draw = ImageDraw.Draw(gradient)
    
    for y in range(height):
        
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return gradient


with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem; margin-top:0; min-width: fit-content;">
        <svg width="46" height="46" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin:0 auto 0.5rem;">
            <path d="M4 8L8 4M8 4L12 8M8 4V16M20 16L16 20M16 20L12 16M16 20V8" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1 style="color:white; font-size:0.5 rem; margin-bottom:2rem;">BackGround Removal Pro</h1>
        <p style="color:white; font-size:0.9rem; letter-spacing:0.5px;">Professional Grade Background Removal</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
     <div style="background:rgba(255,255,255,0.08); padding:0.75rem; border-radius:8px; margin-bottom:1.5rem; border:1px solid rgba(255,255,255,0.05);">
        <h4 style="color:white; margin-bottom:0.5rem; font-size:0.9rem;">✨ Pro Tips</h4>
        <ul style="color:#94a3b8; font-size:0.75rem; padding-left:1rem; line-height:1.4; margin-bottom:0;">
            <li style="margin-bottom:0.25rem;">Use high-contrast images</li>
            <li style="margin-bottom:0.25rem;">PNG for transparency</li>
                <li style="margin-bottom:0.25rem;">Mark on Replace Background  </li>
            <li style="margin-bottom:0.25rem;">Try different backgrounds</li>
            <li>1000px+ resolution recommended</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top:2rem; text-align:center; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.1);">
        <p style="color:white; font-size:0.8rem; letter-spacing:0.5px;">Background Removal Pro </p>
        <p style="color:white; font-size:0.75rem;">© 2025 Synctom Technologies</p>
    </div>
    """, unsafe_allow_html=True)


col1, col2 = st.columns([1, 2], gap="large")


if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'final_img' not in st.session_state:
    st.session_state.final_img = None
if 'original' not in st.session_state:
    st.session_state.original = None
if 'removed' not in st.session_state:
    st.session_state.removed = None

with col1:
    st.markdown("<h2 style='margin-bottom:0.5rem;'>BackGround Removal </h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:1.1rem; margin-bottom:2.5rem;'>Professional-grade background removal for designers, marketers, and content creators.</p>", unsafe_allow_html=True)
    
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 1️⃣ Upload Image")
        uploaded_file = st.file_uploader("**Drag and drop or click to browse**", 
                                       type=["png", "jpg", "jpeg"], 
                                       help="Supported formats: PNG, JPG, JPEG up to 20MB",
                                       label_visibility="collapsed")
        
        if uploaded_file:
            st.success("Image uploaded successfully", icon="✅")
            with Image.open(uploaded_file) as img:
                st.image(img, caption="Original Image", use_container_width=True)
                st.session_state.original = img.copy()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Settings Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 2️⃣ Processing Settings")
        
        preview_width = st.slider("**Preview width**", min_value=200, max_value=1200, value=600, )
                               
        
        output_format = st.selectbox("**Output format**", 
                                   ["PNG (transparent)", "JPEG (high quality)", "WEBP (balanced)"], 
                                   index=0,
                                   
        )
        
        st.markdown("---")
        
        replace_toggle = st.checkbox("**Replace background**", value=False,
                            )
        
        if replace_toggle:
            replace_mode = st.radio("**Replacement type:**", 
                                  ["Solid color", "Custom image", "Gradient"], 
                                  horizontal=True,
                                  help="Choose how to replace the background")
            
            if replace_mode == "Solid color":
                bg_color = st.color_picker("**Background color**", "#FFFFFF",
                                          help="Select a solid color for the new background")
            elif replace_mode == "Custom image":
                bg_image = st.file_uploader("**Upload background image**", 
                                          type=["png", "jpg", "jpeg"],
                                          help="Use your own image as the new background")
            else:
                col1a, col2a = st.columns(2)
                with col1a:
                    gradient_start = st.color_picker("**Gradient start**", "#4f46e5")
                with col2a:
                    gradient_end = st.color_picker("**Gradient end**", "#06b6d4")
        
        st.markdown("---")
        
        remove_btn = st.button("**Process Image**", 
                             use_container_width=True,
                             type="primary",
                             help="Remove background with AI processing")
        st.markdown('</div>', unsafe_allow_html=True)


def process_image_flow():
    if not uploaded_file:
        st.warning("Please upload an image to process", icon="⚠️")
        return
    
    err = validate_upload(uploaded_file)
    if err:
        st.error(err, icon="❌")
        return
    
    with st.spinner("Processing your image with AI..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
        
            status_text.markdown("**Loading image...**")
            if st.session_state.original is None:
                st.session_state.original = byte_to_pil(uploaded_file.read())
            progress_bar.progress(15)
            time.sleep(0.3)
            
            
            status_text.markdown("**Removing background...**")
            st.session_state.removed = remove_background_with_rembg(st.session_state.original)
            progress_bar.progress(50)
            time.sleep(0.5)
            
            
            status_text.markdown("**Applying effects...**")
            st.session_state.final_img = st.session_state.removed
            if replace_toggle:
                if replace_mode == "Solid color":
                    hexcol = bg_color.lstrip("#")
                    rgb = tuple(int(hexcol[i:i+2], 16) for i in (0, 2, 4))
                    bg_pil = Image.new("RGB", st.session_state.removed.size, rgb)
                    st.session_state.final_img = composite_with_color(st.session_state.removed, bg_pil)
                elif replace_mode == "Custom image":
                    if bg_image:
                        bg_pil = byte_to_pil(bg_image.read())
                        
                        if bg_pil.size != st.session_state.removed.size:
                            bg_pil = bg_pil.resize(st.session_state.removed.size)
                        st.session_state.final_img = composite_with_color(st.session_state.removed, bg_pil)
                    else:
                        st.warning("No background image provided - using transparent", icon="⚠️")
                else: 
                   
                    start_rgb = tuple(int(gradient_start.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                    end_rgb = tuple(int(gradient_end.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                    bg_pil = create_gradient_background(st.session_state.removed.size, start_rgb, end_rgb)
                    st.session_state.final_img = composite_with_color(st.session_state.removed, bg_pil)
            
            progress_bar.progress(85)
            time.sleep(0.5)
            
           
            status_text.markdown("**Finalizing output...**")
            fmt = "PNG" if "PNG" in output_format else "JPEG" if "JPEG" in output_format else "WEBP"
            st.session_state.image_bytes, st.session_state.mime, st.session_state.filename = prepare_download_image(st.session_state.final_img, fmt)
            progress_bar.progress(100)
            time.sleep(0.2)
            
            st.session_state.processed = True
            
        except Exception as e:
            st.error(f"Processing error: {str(e)}", icon="❌")
            st.session_state.processed = False
            return


if remove_btn:
    process_image_flow()


if st.session_state.processed and st.session_state.final_img is not None:
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎉 Processing Results")
        
        tab1, tab2, tab3 = st.tabs(["Original", "Background Removed", "Final Result"])
        
        with tab1:
            st.image(st.session_state.original, caption="Original Image", width=preview_width)
            st.caption("Uploaded image before processing")
        
        with tab2:
            st.image(st.session_state.removed, caption="Background Removed", width=preview_width)
            st.caption("AI-processed with transparent background")
        
        with tab3:
            st.image(st.session_state.final_img, caption="Final Result", width=preview_width)
            st.caption("Ready for download with your selected options")
            
            st.markdown("---")
            
         
            col1b, col2b = st.columns([3, 1])
            with col1b:
                st.markdown("**Download Options**")
                st.caption("Save your processed image in the selected format")
            with col2b:
                st.download_button(
                    label="Download",
                    data=st.session_state.image_bytes,
                    file_name=st.session_state.filename,
                    mime=st.session_state.mime,
                    use_container_width=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
   
    with col2:
        st.markdown('<div class="card" style="min-height:600px;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:4rem 1rem;">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin:0 auto 1.5rem; opacity:0.8;">
                <path d="M4 16L8 20M8 20L12 16M8 20V8M20 8L16 4M16 4L12 8M16 4V16" stroke="#4f46e5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3 style="color:#475569; margin-bottom:1rem;">Ready to Transform Your Images?</h3>
            <p style="color:#64748b; max-width:400px; margin:0 auto 2rem;">Upload an image and click <strong>Process Image</strong> to remove the background with our premium  technology</p>
            <div style="font-size:2rem; color:#c7d2fe; margin-top:1rem;">✂️</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)