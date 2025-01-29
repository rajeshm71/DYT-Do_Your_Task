# app.py

import streamlit as st
from agents import AgentManager
from utils.logger import logger
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()
st.set_page_config(
        page_title="MedAI Suite",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
# Custom CSS for styling
st.markdown("""
    <style>
        .main {padding: 2rem;}
        .stTextArea textarea {border-radius: 10px;}
        .stButton button {border-radius: 8px; transition: all 0.3s ease;}
        .stButton button:hover {transform: scale(1.02);}
        .success-box {padding: 1rem; border-radius: 10px; background-color: #e6f4ea;}
        .error-box {padding: 1rem; border-radius: 10px; background-color: #ffe6e6;}
        .header-icon {font-size: 1.5rem; vertical-align: middle;}
    </style>
""", unsafe_allow_html=True)

def main():
   
    st.title("🏥 MedAI Suite - Intelligent Medical Assistant")
    st.caption("Powered by Collaborative AI Agents")

    with st.sidebar:
        st.header("⚙️ Task Configuration")
        task = st.selectbox(
            "Select Medical Task:",
            [
                "Summarize Medical Text",
                "Write and Refine Research Article",
                "Sanitize Medical Data (PHI)"
            ],
            index=0
        )
        st.markdown("---")
        st.markdown("**Note:** All AI operations include validation checks for accuracy and safety.")
        st.markdown("---")
        st.markdown("Developed by Rajesh")

    agent_manager = AgentManager(max_retries=2, verbose=True)

    if task == "Summarize Medical Text":
        summarize_section(agent_manager)
    elif task == "Write and Refine Research Article":
        write_and_refine_article_section(agent_manager)
    elif task == "Sanitize Medical Data (PHI)":
        sanitize_data_section(agent_manager)

def summarize_section(agent_manager):
    st.header("📝 Medical Text Summarization")
    st.markdown("_Generate concise summaries from complex medical texts_")
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        with st.expander("📥 Input Text", expanded=True):
            text = st.text_area("Enter medical text:", height=300, label_visibility="collapsed")
            
    with col2:
        st.markdown("### Parameters")
        summary_length = st.selectbox("Summary Length:", ["Short", "Medium", "Detailed"], index=1)
        technical_level = st.selectbox("Technical Level:", ["Patient-Friendly", "Clinical", "Research"], index=1)

    if st.button("🚀 Generate Summary", use_container_width=True):
        if text:
            with st.status("🧠 Processing...", expanded=True) as status:
                try:
                    st.write("🔍 Analyzing text structure...")
                    main_agent = agent_manager.get_agent("summarize")
                    
                    st.write("📄 Generating summary...")
                    summary = main_agent.execute(
                        text, 
                        length=summary_length,
                        technical_level=technical_level
                    )
                    
                    st.write("✅ Validation in progress...")
                    validator_agent = agent_manager.get_agent("summarize_validator")
                    validation = validator_agent.execute(original_text=text, summary=summary)
                    
                    status.update(label="Process Complete", state="complete", expanded=False)
                    
                    with st.container():
                        st.subheader("📋 Generated Summary")
                        st.markdown(f"<div class='success-box'>{summary.content}</div>", unsafe_allow_html=True)
                        
                        st.subheader("🔍 Validation Results")
                        if "PASS" in validation.content:
                            st.success("✅ Summary validation passed all quality checks")
                        else:
                            st.error("❌ Validation issues detected")
                        st.markdown(f"<div class='info-box'>{validation.content}</div>", unsafe_allow_html=True)
                        
                except Exception as e:
                    status.update(label="Process Failed", state="error")
                    st.error(f"⛔ Critical Error: {e}")
                    logger.error(f"SummarizeAgent Error: {e}")
        else:
            st.warning("⚠️ Please input medical text to summarize")

def write_and_refine_article_section(agent_manager):
    st.header("📚 Research Article Composition")
    st.markdown("_AI-assisted medical writing with collaborative refinement_")
    
    col1, col2 = st.columns([3, 1], gap="large")
    
    with col1:
        topic = st.text_input("✏️ Research Topic", placeholder="Enter primary research focus...")
        with st.expander("📝 Optional Outline", expanded=False):
            outline = st.text_area("Provide structure guidelines:", height=150, label_visibility="collapsed")
    
    if st.button("🖨️ Generate Article", use_container_width=True):
        if topic:
            progress_bar = st.progress(0, text="Initializing AI Agents...")
            
            try:
                # Article Generation
                progress_bar.progress(25, text="Drafting initial content...")
                writer_agent = agent_manager.get_agent("write_article")
                draft = writer_agent.execute(topic, outline)
                
                # Refinement
                progress_bar.progress(50, text="Enhancing article quality...")
                refiner_agent = agent_manager.get_agent("refiner")
                refined_article = refiner_agent.execute(draft)
                
                # Validation
                progress_bar.progress(75, text="Running quality checks...")
                validator_agent = agent_manager.get_agent("validator")
                validation = validator_agent.execute(topic=topic, article=refined_article)
                
                progress_bar.progress(100, text="Process Complete!")
                st.success("✅ Article generation completed successfully")
                
                # Display Results
                with st.expander("📄 Final Article", expanded=True):
                    st.markdown(refined_article.content)
                
                with st.expander("🔍 Quality Report", expanded=False):
                    if "CRITICAL" in validation.content:
                        st.error("❌ Validation Issues Detected")
                    else:
                        st.success("✅ All Quality Checks Passed")
                    st.markdown(validation.content)
                
            except Exception as e:
                progress_bar.empty()
                st.error(f"⛔ Process Failed: {e}")
                logger.error(f"Article Generation Error: {e}")
        else:
            st.warning("⚠️ Please specify a research topic")

def sanitize_data_section(agent_manager):
    st.header("🔒 PHI Sanitization")
    st.markdown("_Secure sensitive health information removal_")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.expander("🔓 Original Data Input", expanded=True):
            medical_data = st.text_area("Input sensitive data:", height=300, label_visibility="collapsed")
    
    if st.button("🛡️ Sanitize Data", use_container_width=True):
        if medical_data:
            with st.spinner("🔍 Scanning for sensitive information..."):
                try:
                    main_agent = agent_manager.get_agent("sanitize_data")
                    sanitized_data = main_agent.execute(medical_data)
                    
                    validator_agent = agent_manager.get_agent("sanitize_data_validator")
                    validation = validator_agent.execute(
                        original_data=medical_data,
                        sanitized_data=sanitized_data
                    )
                    
                    with col2:
                        with st.expander("🔐 Sanitized Output", expanded=True):
                            st.markdown(f"<div class='success-box'>{sanitized_data.content}</div>", unsafe_allow_html=True)
                        
                        with st.expander("🛡️ Security Report", expanded=False):
                            if "PASS" in validation.content:
                                st.success("✅ No PHI Detected")
                            else:
                                st.error("❌ Potential PHI Found")
                            st.markdown(validation.content)
                            
                except Exception as e:
                    st.error(f"⛔ Sanitization Error: {e}")
                    logger.error(f"Sanitization Error: {e}")
        else:
            st.warning("⚠️ Please input data for sanitization")

if __name__ == "__main__":
    main()