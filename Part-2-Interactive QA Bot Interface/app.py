import streamlit as st
import time
from backend import extract_text_from_pdf, query_bot
import os

def main():
    st.set_page_config(
        page_title="Interactive QA Bot",
        page_icon="🤖",
        layout="wide"
    )

    st.title("📚 Interactive Document QA Bot")
    
    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.info("""
        This QA Bot uses RAG (Retrieval-Augmented Generation) to answer questions about your documents.
        
        Features:
        - PDF document upload
        - Real-time question answering
        - Context-aware responses
        - View source segments
        """)
        
        st.header("Usage Instructions")
        st.markdown("""
        1. Upload your PDF document
        2. Wait for processing
        3. Ask questions about the content
        4. View both the answer and source context
        """)

        st.header("Created By:")
        st.markdown("""
        - Name: Pijush Pathak
        - Email: pijushpathak94@gmail.com
        - linkedin: https://www.linkedin.com/in/pijush-pathak/
        """)


    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload a PDF Document", type="pdf")
        
        if uploaded_file:
            try:
                with st.spinner("Processing document..."):
                    document_text = extract_text_from_pdf(uploaded_file)
                    st.session_state['document_text'] = document_text
                    st.success("✅ Document processed successfully!")
                    
                    # Display document statistics
                    word_count = len(document_text.split())
                    st.info(f"Document Statistics:\n- Word Count: {word_count}")
            
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                return

    # Question input area
    if 'document_text' in st.session_state:
        st.markdown("---")
        question = st.text_input("Ask a question about your document:", key="question_input")
        
        if question:
            try:
                with st.spinner("Generating answer..."):
                    start_time = time.time()
                    answer, retrieved_segments = query_bot(question, st.session_state['document_text'])
                    end_time = time.time()
                    
                    # Display answer
                    st.markdown("### 🤖 Answer:")
                    st.write(answer)
                    
                    # Display metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"Response time: {(end_time - start_time):.2f} seconds")
                    with col2:
                        st.info(f"Retrieved segments: {len(retrieved_segments.split())} words")
                    
                    # Display source segments in an expander
                    with st.expander("View Source Segments"):
                        st.markdown("### 📑 Retrieved Segments:")
                        st.write(retrieved_segments)
            
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")

if __name__ == "__main__":
    main()