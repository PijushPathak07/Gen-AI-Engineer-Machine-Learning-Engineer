import cohere
from pinecone import Pinecone, ServerlessSpec
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import os

# Initialize Cohere and Pinecone API keys
COHERE_API_KEY = "jpOL27VdFb684lyOdK5ohvug3YEmDSaTNSGcpSoz"
PINECONE_API_KEY = "b14daa31-6e34-483d-a6db-bbe89dcc2aff"
PINECONE_ENVIRONMENT = "us-east-1"

# Initialize Cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

# Using a transformer model to create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone using the new API
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create or connect to a Pinecone index
index_name = "ragbot"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # 384 for 'all-MiniLM-L6-v2' model
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-1'
        )
    )
pinecone_index = pc.Index(index_name)

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_embeddings(text):
    """Generate embeddings for the given text using SentenceTransformer."""
    embeddings = model.encode([text], convert_to_tensor=False)
    return embeddings[0]

def store_embeddings_in_pinecone(embedding, document_id):
    """Store document embeddings in Pinecone with a unique ID."""
    try:
        pinecone_index.upsert(
            vectors=[(document_id, embedding.tolist())]
        )
    except Exception as e:
        print(f"Error storing embeddings: {str(e)}")
        raise

def query_pinecone(embedding, top_k=3):
    """Query Pinecone to find the most similar documents based on embedding."""
    try:
        results = pinecone_index.query(
            vector=embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        return results
    except Exception as e:
        print(f"Error querying Pinecone: {str(e)}")
        raise

def query_bot(question, document_text):
    """
    Embed the user question, store document embeddings in Pinecone, and query Pinecone for relevant information.
    Finally, generate a coherent answer using Cohere.
    """
    try:
        # Step 1: Embed the user's question
        question_embedding = generate_embeddings(question)

        # Step 2: Embed the document and store it in Pinecone (if not already stored)
        document_embedding = generate_embeddings(document_text)
        store_embeddings_in_pinecone(document_embedding, "doc-1")

        # Step 3: Query Pinecone for relevant document segments
        results = query_pinecone(question_embedding, top_k=3)

        # Step 4: Retrieve the most relevant segments
        if results and 'matches' in results:
            retrieved_texts = " ".join([match.get('metadata', {}).get('text', '') 
                                      for match in results['matches'] 
                                      if 'metadata' in match and 'text' in match['metadata']])
        else:
            retrieved_texts = ""

        # Step 5: Use Cohere to generate an answer based on the retrieved segments
        # Using 'command' model which is one of Cohere's current generation models
        response = cohere_client.generate(
            prompt=f"""Based on the following context, please answer the question. 
            If the answer cannot be found in the context, say "I cannot find relevant information to answer this question."
            
            Context: {retrieved_texts}
            
            Question: {question}
            
            Answer:""",
            model='command',  # Using command model instead of xlarge
            max_tokens=300,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )

        return response.generations[0].text.strip(), retrieved_texts

    except Exception as e:
        print(f"Error in query_bot: {str(e)}")
        return f"An error occurred: {str(e)}", ""

if __name__ == "__main__":
    # For testing purposes
    pdf_path = "sample_document.pdf"
    with open(pdf_path, 'rb') as f:
        document_text = extract_text_from_pdf(f)
    
    question = "What is the main focus of the document?"
    answer, segments = query_bot(question, document_text)

    print("Answer:", answer)
    print("Relevant Segments:", segments)