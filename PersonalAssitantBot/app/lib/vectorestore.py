# Implementing PDF Search
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools.retriever import create_retriever_tool
from enum import Enum


class DocType(Enum):
    pdf  = "pdf"
    docx = "docx"
    web  = "web_url"


class VectorStore:
    def __init__(self, connection:str, collection_name:str,embeddings):
        self.vectorestore = PGVector(
            embeddings=embeddings,
            connection=connection,
            collection_name=collection_name,
            use_jsonb=True,
        )

    # add pdf to store
    def add_doc_to_store(self,doc_type:DocType,doc_location:str):
            if doc_type == DocType.pdf.value:
                loader = PyPDFLoader(doc_location)
                # text splitter
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                # split the document
                split_docs = loader.load_and_split(text_splitter=text_splitter)
                self.vectorestore.add_documents(split_docs)
            
    def get_retriver_tool(self):
        retriver = self.vectorestore.as_retriever()
        # create retriver tool
        retriver_tool = create_retriever_tool(
            retriever=retriver,
            name="document_search",
            description="Use this tool to search information from the pdf document"
        )
        return retriver_tool
    
    def get_chat_retriever_tool(self):
         retriver = self.vectorestore.as_retriever()
         # create retriver tool
         chat_retriever_tool = create_retriever_tool(
            retriever=retriver,
            name="chat_search",
            description="Use this tool to search information from previous chat history"
        )
         return chat_retriever_tool