import streamlit as st
import tempfile
from pathlib import Path
import sys
import os
import json

# Add src to path for imports
dir_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(dir_path, 'src')
sys.path.append(src_path)

from surveillanceCam import process_video

# --- Sidebar ---
st.set_page_config(page_title="AI-Powered CCTV Surveillance", layout="wide")
with st.sidebar:
    st.markdown(
        "<h2 style='color:#30cfd0; font-family:Poppins;'>🎥 AI-Powered CCTV Surveillance</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#fff; font-family:Poppins;'>Upload and analyze videos for object and person detection using YOLOv8.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        "<p style='color:#ccc; font-size:13px;'>Developed by Riya A Amipara</p>",
        unsafe_allow_html=True
    )

# --- Main Area ---
st.markdown(
    "<h1 style='color:#30cfd0; font-family:Poppins; text-align:center;'>AI-Powered CCTV Surveillance</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#fff; font-family:Poppins;'>"
    "Upload a video to analyze objects and people using YOLOv8.<br>"
    "Supported formats: MP4, AVI, MOV. Max size: 500MB."
    "</p>",
    unsafe_allow_html=True
)

# --- Navigation ---
SAVED_ANALYSIS_DIR = os.path.join(dir_path, "static", "saved-test")

page = st.sidebar.radio(
    "Navigation",
    ["Analyze Video", "Live Recording", "Saved Analyses"],
    index=0,
    help="Choose a page",
    key="navigation_radio"
)

if page == "Analyze Video":
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov"],
        help="Supported formats: MP4, AVI, MOV. Max size: 500MB.",
        key="video_uploader"
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_video:
            temp_video.write(uploaded_file.read())
            temp_video_path = Path(temp_video.name)

        with st.spinner("Processing video, please wait..."):
            results = process_video(str(temp_video_path))

        if results and results.get('output_file') and os.path.exists(results['output_file']):
            st.success("✅ Analysis complete!")
            st.video(results['output_file'])
            st.markdown("#### 🎯 Detection Results")

            if results.get('detections'):
                st.table([
                    {"Object": obj, "Count": count}
                    for obj, count in results['detections'].items()
                ])

            if results.get('person_detected', 0) > 0:
                st.markdown(
                    f"<span style='color:#ffcc00; font-size:18px;'>⚠️ Persons detected: {results['person_detected']}</span>",
                    unsafe_allow_html=True
                )

            st.markdown(f"**Total frames:** {results.get('total_frames', 0)}")
            st.markdown(f"**Objects found:** {', '.join(results.get('objects_found', []))}")

            with open(results['output_file'], 'rb') as f:
                st.download_button("⬇️ Download analyzed video", f, file_name=Path(results['output_file']).name, key="download_analyzed_video")
        else:
            st.error("❌ Failed to process video. Please try another file.")

        # Clean up temp file
        try:
            temp_video_path.unlink()
        except Exception:
            pass

elif page == "Live Recording":
    st.markdown("### 🎥 Live Recording from Webcam/CCTV")
    st.write("Record a live video from your webcam or CCTV system, and then goto analyze video page select your live recorded file and analyze it.")

    from src.WebCam import record_live_video

    # Use a unique key
    # Use a key that is guaranteed unique for this widget and page
    duration = st.number_input(
        "Recording duration (seconds)",
        min_value=5,
        max_value=120,
        value=30,
        step=1,
        key="live_recording_duration_page_only"
    )

    if st.button("Start Recording", key="start_recording_btn"):
        with st.spinner(f"Recording for {duration} seconds..."):
            video_path = record_live_video(recording_duration=duration, show_window=False)

        if video_path and os.path.exists(video_path):
            st.success(f"Recording complete! Saved to: {video_path}")
            st.video(video_path)

            if st.button("Analyze Recorded Video", key="analyze_recorded_video_btn"):
                with st.spinner("Analyzing recorded video..."):
                    results = process_video(str(video_path))

                if results and results.get('output_file') and os.path.exists(results['output_file']):
                    st.success("✅ Analysis complete!")
                    st.video(results['output_file'])
                    st.markdown("#### 🎯 Detection Results")

                    if results.get('detections'):
                        st.table([
                            {"Object": obj, "Count": count}
                            for obj, count in results['detections'].items()
                        ])

                    if results.get('person_detected', 0) > 0:
                        st.markdown(
                            f"<span style='color:#ffcc00; font-size:18px;'>⚠️ Persons detected: {results['person_detected']}</span>",
                            unsafe_allow_html=True
                        )

                    st.markdown(f"**Total frames:** {results.get('total_frames', 0)}")
                    st.markdown(f"**Objects found:** {', '.join(results.get('objects_found', []))}")

                    with open(results['output_file'], 'rb') as f:
                        st.download_button("⬇️ Download analyzed video", f, file_name=Path(results['output_file']).name, key="download_btn_live")
                else:
                    st.error("❌ Failed to process video. Please try again.")

elif page == "Saved Analyses":
    st.markdown(
        "<h1 style='color:#30cfd0; font-family:Poppins; text-align:center;'>📁 Saved Analyses</h1>",
        unsafe_allow_html=True
    )
    st.write("Browse your previous video analyses below:")

    saved_dir = Path(SAVED_ANALYSIS_DIR)
    if not saved_dir.exists():
        st.info("No saved analyses found.")
    else:
        analysis_folders = sorted([d for d in saved_dir.iterdir() if d.is_dir()], reverse=True)
        if not analysis_folders:
            st.info("No saved analyses found.")
        else:
            for i, folder in enumerate(analysis_folders):
                meta_file = folder / "metadata.json"
                if meta_file.exists():
                    with open(meta_file, "r") as f:
                        meta = json.load(f)

                    st.markdown(f"### {meta.get('test_name', 'Analysis')}")
                    st.write(f"**Date:** {meta.get('timestamp', '')}")
                    st.write(f"**Summary:** {meta.get('analysis_summary', '')}")
                    st.write(f"**Objects found:** {', '.join(meta.get('objects_found', []))}")
                    st.write(f"**Persons detected:** {meta.get('person_detected', 0)}")

                    analyzed_video = meta.get('analyzed_video')
                    if analyzed_video:
                        video_path = folder / analyzed_video
                        if video_path.exists():
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                with open(video_path, 'rb') as f:
                                    st.download_button(
                                        "⬇️ Download analyzed video",
                                        f,
                                        file_name=analyzed_video,
                                        key=f"download_{folder.name}"
                                    )
                            with col2:
                                if st.button(f"🗑️ Delete analyzed video", key=f"delete_{folder.name}"):
                                    try:
                                        video_path.unlink()
                                        st.success("Analyzed video deleted.")
                                    except Exception as e:
                                        st.error(f"Failed to delete: {e}")
                    st.markdown("---")

# --- Footer ---
st.markdown(
    "<hr style='border:1px solid #30cfd0; margin-top:40px;'>"
    "<div style='text-align:center; color:#ccc; font-size:14px;'>"
    "&copy; 2025 Riya A Amipara &mdash; AI-Powered CCTV Surveillance System"
    "</div>",
    unsafe_allow_html=True
)
