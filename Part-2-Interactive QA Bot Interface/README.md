# Interactive QA Bot with RAG Implementation
A Retrieval-Augmented Generation (RAG) based Question-Answering system with an interactive Streamlit interface.

## Project Overview

This project implements Part 2 of the RAG-based QA system, focusing on creating an interactive interface that allows users to upload documents and get real-time answers to their questions.

### Technical Architecture

```
Project Structure:
├── app.py              # Streamlit frontend interface
├── backend.py          # RAG implementation and core logic
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker compose configuration
├── requirements.txt    # Project dependencies
└── .env                # Environment variables
```

## Technical Approach & Design Decisions

### 1. Frontend Implementation (Streamlit)
- **Why Streamlit?**
  - Quick deployment and prototyping
  - Built-in components for file upload and user interaction
  - Easy integration with Python backend
  - Real-time updates and state management

- **Key Features**:
  - PDF document upload and processing
  - Real-time question answering interface
  - Context visualization
  - Progress indicators and error handling

### 2. Backend Architecture

#### Vector Database (Pinecone)
- **Design Choice**: Used Pinecone for vector storage
- **Rationale**:
  - Efficient similarity search
  - Scalable for large documents
  - Real-time querying capabilities
  - Managed service reducing operational overhead

#### Text Generation (Cohere)
- **Model Selection**: Cohere's 'command' model
- **Benefits**:
  - High-quality text generation
  - Context-aware responses
  - Good balance of speed and accuracy

### 3. Data Flow
```
1. Document Upload → PDF Processing → Text Extraction
2. Text → Embeddings Generation → Vector Storage
3. User Query → Query Embedding → Vector Search
4. Retrieved Context + Query → LLM → Generated Answer
```

## Challenges & Solutions

### 1. Document Processing
- **Challenge**: Handling large PDF documents efficiently
- **Solution**: 
  ```python
  def extract_text_from_pdf(pdf_file):
      reader = PdfReader(pdf_file)
      text = ""
      for page in reader.pages:
          text += page.extract_text()
      return text
  ```

### 2. Vector Database Integration
- **Challenge**: Managing document embeddings effectively
- **Solution**: Implemented chunking and efficient storage
  ```python
  def store_embeddings_in_pinecone(embedding, document_id):
      try:
          pinecone_index.upsert(
              vectors=[(document_id, embedding.tolist())]
          )
      except Exception as e:
          print(f"Error storing embeddings: {str(e)}")
          raise
  ```

### 3. Response Generation
- **Challenge**: Generating contextually relevant answers
- **Solution**: Enhanced prompt engineering
  ```python
  prompt = f"""Based on the following context, please answer the question.
      If the answer cannot be found in the context, say "I cannot find relevant information."
      
      Context: {retrieved_texts}
      Question: {question}
      Answer:"""
  ```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Cohere API key
- Pinecone API key

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file:
   ```
   COHERE_API_KEY=your_cohere_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   ```

### Docker Deployment

1. **Build the Container**
   ```bash
   docker-compose build
   ```

2. **Run the Application**
   ```bash
   docker-compose up
   ```

3. **Access the Interface**
   - Open browser
   - Navigate to: `http://localhost:8501`

## Usage Guide

### 1. Document Upload
1. Click "Upload a PDF Document"
2. Select your PDF file
3. Wait for processing confirmation

### 2. Asking Questions
1. Type your question in the input field
2. Click Enter or Submit
3. View the generated answer and source context

### 3. Viewing Results
- Main answer appears at the top
- Source context can be viewed in expandable section
- Processing time and statistics are displayed

## Performance Optimization

### 1. Caching Implementation
```python
@st.cache_data
def load_document(file):
    return extract_text_from_pdf(file)
```

### 2. Batch Processing
```python
def process_document_chunks(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

## Testing

### Manual Testing Checklist
1. Document Upload
   - [x] Various PDF sizes
   - [x] Different PDF formats
   - [x] Error handling

2. Query Processing
   - [x] Simple questions
   - [x] Complex queries
   - [x] Edge cases

3. Response Generation
   - [x] Accuracy
   - [x] Response time
   - [x] Context relevance

## Monitoring and Maintenance

### 1. Error Logging
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 2. Performance Metrics
- Response time tracking
- Memory usage monitoring
- Error rate logging

## Future Improvements

1. **Enhanced Document Processing**
   - Support for more file formats
   - Better text extraction
   - Document preprocessing

2. **UI Enhancements**
   - Advanced query interface
   - Better visualization of context
   - User feedback system

3. **Performance Optimization**
   - Improved caching
   - Better chunking strategies
   - Parallel processing

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License

## Contact

Your Name - Pijush Pathak
Email- pijushpathak94@gmail.com
Project Link: [https://github.com/PijushPathak07/Gen-AI-Engineer-Machine-Learning-Engineer-Assignment](https://github.com/PijushPathak07/Gen-AI-Engineer-Machine-Learning-Engineer-Assignment)