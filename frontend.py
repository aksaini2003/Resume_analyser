import streamlit as st 
import fitz 
import io
from backend import resume_analyzer 
try:
    
    # -------------------- PDF Extractor --------------------
    def extract_text(uploaded_file):
        file_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(file_bytes)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")

        text = ""
        for page in doc:
            page_text = page.get_text("text")
            if not page_text.strip():
                page_text = page.get_text("blocks")  # fallback
            text += page_text
        return text.strip()


    # -------------------- Streamlit UI --------------------
    st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered")

    # Custom CSS for styling
    st.markdown("""
        <style>
            /* Center content */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            /* Header */
            h1, h2, h3 {
                text-align: center;
                font-family: 'Segoe UI', sans-serif;
            }

            /* Upload section */
            .stFileUploader label {
                font-size: 16px;
                font-weight: bold;
            }

            /* Buttons */
            div.stButton > button:first-child {
                background-color: #0066cc;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 30px;
                margin-top: 15px;
            }
            div.stButton > button:hover {
                background-color: #004080;
                color: yellow;
            }

            /* Result box */
            .result-box {
                background-color: #f9f9f9;
                border: 2px solid #0066cc;
                border-radius: 12px;
                padding: 20px;
                margin-top: 20px;
                font-size: 16px;
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)

    # -------------------- App Layout --------------------
    st.title("📄 Resume vs Job Description Analyzer")
    st.write("Upload your **resume** and the **job description (JD)** to get a smart analysis of how well they match.")

    # Upload section
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Upload Your Resume")
        uploaded_resume = st.file_uploader("Choose Resume PDF", type=["pdf"], key="resume")
    with col2:
        st.subheader("Upload Job Description")
        uploaded_job_description = st.file_uploader("Choose JD PDF", type=["pdf"], key="job_desc")

    resume = job_desc = None
    if uploaded_resume:
        resume = extract_text(uploaded_resume)
    if uploaded_job_description:
        job_desc = extract_text(uploaded_job_description)

    # -------------------- Analyze Button --------------------
    if resume and job_desc:
        if st.button("🚀 Analyze Resume Against JD"):
            with st.spinner("Analyzing... Please wait ⏳"):
                output_state = resume_analyzer.invoke({
                    'resume_text': resume,
                    'job_description': job_desc
                })

                    # Display result in styled box
           
            # Display heading properly
            st.markdown("###  Analysis Report")  # Markdown works here

            # Display LLM content in styled div (won't interpret Markdown, preserves formatting)
            st.markdown(f"{output_state['review']}", unsafe_allow_html=False)



            # Download option
            st.download_button(
                "📥 Download Analysis",
                data=output_state['review'],
                file_name="resume_analysis.txt",
                mime="text/plain"
            )

except Exception as e:
    st.error('Please check that you have uploaded correct file')