import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="Observa Terram", layout="wide")

# Initialize interactive state memory
if "zoom_sar" not in st.session_state:
    st.session_state.zoom_sar = 100
if "zoom_normal" not in st.session_state:
    st.session_state.zoom_normal = 100
if "pan_sar_idx" not in st.session_state:
    st.session_state.pan_sar_idx = 0

# ==============================================================================
# [PLACEHOLDER 1: SITE INFO] -> Replace these strings with your real details
# ==============================================================================
PROJECT_NAME = "[PLACEHOLDER] Project Name"
LAND_AREA = "[PLACEHOLDER] Land Area"
LOCATION = "[PLACEHOLDER] Location"

# ==============================================================================
# [PLACEHOLDER 2: 15 SAR IMAGES BY EXACT DATE] -> Replace dates & filenames
# ==============================================================================
SAR_IMAGES = {
    "01 April 2026":     "PLACEHOLDER_SAR_01",
    "15 April 2026":     "PLACEHOLDER_SAR_02",
    "01 May 2026":       "PLACEHOLDER_SAR_03",
    "15 May 2026":       "PLACEHOLDER_SAR_04",
    "01 June 2026":      "PLACEHOLDER_SAR_05",
    "15 June 2026":      "PLACEHOLDER_SAR_06",
    "01 July 2026":      "PLACEHOLDER_SAR_07",
    "15 July 2026":      "PLACEHOLDER_SAR_08",
    "01 August 2026":    "PLACEHOLDER_SAR_09",
    "15 August 2026":    "PLACEHOLDER_SAR_10",
    "01 September 2026": "PLACEHOLDER_SAR_11",
    "15 September 2026": "PLACEHOLDER_SAR_12",
    "01 October 2026":   "PLACEHOLDER_SAR_13",
    "15 October 2026":   "PLACEHOLDER_SAR_14",
    "01 November 2026":  "PLACEHOLDER_SAR_15",
}

# ==============================================================================
# [PLACEHOLDER 3: NORMAL OPTICAL VIEW(S) (NO SPECIFIC DATES)]
# ==============================================================================
NORMAL_IMAGES = {
    "Baseline Optical View 1": "PLACEHOLDER_NORMAL_01",
    "Baseline Optical View 2": "PLACEHOLDER_NORMAL_02",
}

# --- HELPER FUNCTION TO SHOW PLACEHOLDER OR REAL IMAGE ---
def render_image_box(image_ref, caption_text="", zoom_percent=None):
    if image_ref.startswith("PLACEHOLDER"):
        st.info(f"🖼️ **[{image_ref}]** {caption_text}")
    else:
        if zoom_percent is not None:
            pixel_width = int(750 * (zoom_percent / 100))
            st.image(image_ref, caption=caption_text, width=pixel_width)
        else:
            st.image(image_ref, caption=caption_text, use_container_width=True)

# --- MAIN LAYOUT: SLIM LEFT PANEL + WIDE VIEWING AREA ---
left_panel, main_panel = st.columns((1, 3.5), gap="large")

# --- LEFT PANEL: SITE INFORMATION & SAR LEGEND ---
with left_panel:
    st.subheader("Site Information & Legend")
    
    with st.container(border=True):
        st.markdown("ℹ️ **Site Info**")
        st.text_input("Project Name", value=PROJECT_NAME, disabled=True, label_visibility="collapsed")
        st.text_input("Land Area", value=LAND_AREA, disabled=True, label_visibility="collapsed")
        st.text_input("Location", value=LOCATION, disabled=True, label_visibility="collapsed")

    with st.container(border=True):
        st.markdown("**SAR Legend**")
        st.markdown("☀️ **Bright** = Rough / Buildings")
        st.markdown("🌑 **Dark** = Smooth / Water")

# --- RIGHT MAIN PANEL: OBSERVA TERRAM ---
with main_panel:
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Observa Terram</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #CBD5E1;'>Observe the Ebb and Tide of Change</p>", unsafe_allow_html=True)

    active_tab = st.radio(
        "Navigation",
        (
            "SAR-Normal",
            "Side-by-Side",
            "SAR Only",
            "Normal Only",
            "Pan-SAR Views"
        ),
        horizontal=True,
        label_visibility="collapsed"
    )

    st.write("")

    sar_dates_list = list(SAR_IMAGES.keys())
    normal_keys_list = list(NORMAL_IMAGES.keys())

    # TAB 1: SAR-NORMAL
    if active_tab == "SAR-Normal":
        col_sar, col_norm = st.columns(2, gap="medium")
        with col_sar:
            st.subheader("SAR View (Baseline)")
            first_sar_key = next(iter(SAR_IMAGES))
            render_image_box(SAR_IMAGES[first_sar_key], "Baseline Radar Sensor View")
        with col_norm:
            st.subheader("Normal View (Baseline)")
            first_norm_key = next(iter(NORMAL_IMAGES))
            render_image_box(NORMAL_IMAGES[first_norm_key], "Baseline Optical Sensor View")

    # TAB 2: SIDE-BY-SIDE
    elif active_tab == "Side-by-Side":
        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            st.subheader("SAR View A")
            date_a = st.selectbox("Select Date (Left)", options=sar_dates_list, index=0, key="date_a")
            render_image_box(SAR_IMAGES[date_a], f"SAR Radar Pass: {date_a}")
        with col_b:
            st.subheader("SAR View B")
            default_b = len(sar_dates_list) - 1
            date_b = st.selectbox("Select Date (Right)", options=sar_dates_list, index=default_b, key="date_b")
            render_image_box(SAR_IMAGES[date_b], f"SAR Radar Pass: {date_b}")

    # TAB 3: SAR ONLY
    elif active_tab == "SAR Only":
        head_col, z_in, z_out = st.columns((4, 1, 1))
        with head_col:
            st.subheader("SAR View")
        with z_in:
            if st.button("Zoom In +", key="sar_zoom_in", use_container_width=True):
                st.session_state.zoom_sar = min(200, st.session_state.zoom_sar + 25)
        with z_out:
            if st.button("Zoom Out -", key="sar_zoom_out", use_container_width=True):
                st.session_state.zoom_sar = max(50, st.session_state.zoom_sar - 25)

        sel_sar_date = st.selectbox("Select Exact SAR Date", options=sar_dates_list, key="sar_only_date")
        st.caption(f"Current Zoom: {st.session_state.zoom_sar}%")
        render_image_box(SAR_IMAGES[sel_sar_date], f"SAR Radar Pass: {sel_sar_date}", zoom_percent=st.session_state.zoom_sar)

    # TAB 4: NORMAL ONLY
    elif active_tab == "Normal Only":
        head_col, z_in, z_out = st.columns((4, 1, 1))
        with head_col:
            st.subheader("Normal Optical View")
        with z_in:
            if st.button("Zoom In +", key="norm_zoom_in", use_container_width=True):
                st.session_state.zoom_normal = min(200, st.session_state.zoom_normal + 25)
        with z_out:
            if st.button("Zoom Out -", key="norm_zoom_out", use_container_width=True):
                st.session_state.zoom_normal = max(50, st.session_state.zoom_normal - 25)

        if len(normal_keys_list) > 1:
            sel_norm_key = st.selectbox("Select Optical Reference", options=normal_keys_list, key="norm_only_sel")
        else:
            sel_norm_key = next(iter(NORMAL_IMAGES))

        st.caption(f"Current Zoom: {st.session_state.zoom_normal}%")
        render_image_box(NORMAL_IMAGES[sel_norm_key], sel_norm_key, zoom_percent=st.session_state.zoom_normal)

    # TAB 5: PAN-SAR VIEWS (Sideways Shorts-Style Carousel)
    elif active_tab == "Pan-SAR Views":
        total_sar = len(sar_dates_list)
        curr_idx = st.session_state.pan_sar_idx
        curr_date = sar_dates_list[curr_idx]

        st.subheader(f"Pan-SAR Timeline Reel ({curr_idx + 1} of {total_sar})")
        st.progress((curr_idx + 1) / total_sar)

        prev_btn_col, img_col, next_btn_col = st.columns((1, 6, 1), vertical_alignment="center")
        with prev_btn_col:
            if st.button("◀", key="pan_prev", use_container_width=True, help="Previous SAR Pass"):
                st.session_state.pan_sar_idx = (curr_idx - 1) % total_sar
                st.rerun()
        with img_col:
            st.markdown(f"<h4 style='text-align: center;'>📅 {curr_date}</h4>", unsafe_allow_html=True)
            render_image_box(SAR_IMAGES[curr_date], f"Pass {curr_idx + 1}/{total_sar} — {curr_date}")
        with next_btn_col:
            if st.button("▶", key="pan_next", use_container_width=True, help="Next SAR Pass"):
                st.session_state.pan_sar_idx = (curr_idx + 1) % total_sar
                st.rerun()

    st.write("")

    # --- BOTTOM: NON-INTERACTIVE LIGHT BLUE TIME BAR (APRIL 2026 - NOVEMBER 2026) ---
    t_start, t_end = st.columns(2)
    with t_start:
        st.markdown("**April 2026**")
    with t_end:
        st.markdown("<p style='text-align: right; font-weight: bold;'>November 2026</p>", unsafe_allow_html=True)

    st.markdown(
        "<div style='height: 10px; background-color: #38BDF8; border-radius: 5px; margin-top: -10px; margin-bottom: 10px;'></div>",
        unsafe_allow_html=True
    )
