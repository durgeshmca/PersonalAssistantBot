# Implementing PDF Search
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from app.config import Config
from app.lib.vectorestore import VectorStore

# create vectore store        
vectore_store = VectorStore(
    connection=Config.PG_CONNECTION,
    collection_name=Config.PG_COLLECTION_NAME,
    embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
)

chat_retriever_tool = vectore_store.get_chat_retriever_tool()
