import streamlit as st
from PyPDF2 import PdfReader
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.ai_service import AIService
from model.ai_chat.conversation import Conversation
import time
from langchain.text_splitter import CharacterTextSplitter

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    #st.write(text)
    return text

def get_metadata(pdf_docs):
    all_metadata = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        metadata = pdf_reader.metadata
        all_metadata.append("Metadata = " + str(metadata))
    return "\n".join(all_metadata)

    

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
        )
    
    chunks = text_splitter.split_text(text)
    return chunks

def display_messages():
    st.empty()
    # Display all past messages from your custom Messages class
    for msg in st.session_state.conversation.get_messages():
        role = msg["role"]
        with st.chat_message(role):
            st.markdown(msg["content"])



def main():
    

    st.set_page_config(page_title="AI Service TEST", page_icon=":battery:")
    ai_service = AIService()
    
    st.header("AI SERVICE:battery:")
    

        
        

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None


    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("upload your PDFs here and click process.", accept_multiple_files = True)
        
        if st.button("process") and pdf_docs:
            start = time.perf_counter()
            with st.spinner("Parsing Text"):                    
                #get pdf text
                raw_text = get_pdf_text(pdf_docs)
                words = raw_text.split(" ")
                st.write(f"number of words {len(words)}")
                st.write(f"number of characters {len(raw_text)}")
                text_parsed = time.perf_counter()
                st.write(f"Text parsed in {(text_parsed-start):.2f}s")

            with st.spinner("Splitting Text into chunks"):
                #get the text chunks
                metadata = get_metadata(pdf_docs=pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                text_chunks.insert(0,metadata)
                text_chunked = time.perf_counter()
                st.write(f"Text split into chunks in {(text_chunked-text_parsed):.4f}s")     

            with st.spinner("Embedding"):           
                #create vector store
                st.session_state.vector_store = ai_service.get_vector_store(text_chunks=text_chunks)    
                st.session_state.conversation = Conversation(conversation_id="penisman", vector_store=st.session_state.vector_store)
                ai_service.send_system_message(system_message= """You are a helpful AI Assistant Arc AI 
                                               you assist with answering questions for documents users upload, you will get the relevant part of the document with each question""",
                                                 conversation=st.session_state.conversation)

                
                embedding_time = time.perf_counter()
                st.write(f"Embedding Complete in {(embedding_time-text_chunked):.2f}s")

            with st.spinner("Creating Summary"):    
                placeholder = st.empty()
                #create and print summary
                summary_response = ai_service.summarize(vector_store=st.session_state.vector_store)
                
                summary_time = time.perf_counter()

                
                tldr = ai_service.output_streaming_response(response=summary_response, output_function=placeholder.markdown, mode="generate")
                placeholder.markdown(tldr)

                st.write(f"Summary completed in {(summary_time-embedding_time):.2f}s")
                st.write(f"Processing complete in {(summary_time-start):.2f}s")
                document_processed = True

    
    if st.session_state.vector_store and st.session_state.conversation:
        question = st.chat_input("Ask anything")
        if question:
            display_messages()
            st.session_state.conversation.add_user_message(question)
            with st.chat_message("user"):
                st.markdown(question)
            response = ai_service.send_chat_message(question=question, conversation=st.session_state.conversation)
            with st.chat_message("assistant"):
                placeholder = st.empty()
                answer = ai_service.output_streaming_response(response=response, output_function=placeholder.markdown)
                st.session_state.conversation.add_ai_message(answer)
                placeholder.markdown(answer)
        




if __name__ == "__main__":
    main()
            