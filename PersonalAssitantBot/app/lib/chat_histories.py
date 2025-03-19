import psycopg
from langchain_postgres import PostgresChatMessageHistory
from app.config import Config
from typing import Sequence
from langchain_core.messages import BaseMessage
from app.lib.vectorestore import VectorStore
# from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

class CustomPostgresChatMessageHistory(PostgresChatMessageHistory):
    def __init__(self, table_name, session_id, sync_connection):
        self._session_id = session_id
        super().__init__(
            table_name, 
            session_id, 
            sync_connection=sync_connection
            )

    def add_messages(self, messages: Sequence[BaseMessage])-> None:
        super().add_messages(messages)
        
        docs = []
        for message in messages:
            metadata = message['uuid'] = self._session_id
            doc = Document(page_content=message.content,metadata=metadata)
            print(doc)
            docs.append(doc)
        if len(docs) > 0:
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vector_store = VectorStore(
                connection=Config.PG_CONNECTION,
                collection_name=Config.CHAT_COLLECTION_NAME,
                embeddings=embeddings,
                use_jsonb=True,
            )
            vector_store.vectorestore.add_documents(docs)




class PostgresChatMessageHistoryStore:
    def __init__(self):
        pass
        
    def get_session_history(session_id):
        chat_history = CustomPostgresChatMessageHistory(
            Config.CHAT_HISTORY_TABLE_NAME,
            session_id,
            sync_connection=psycopg.connect(Config.PG1_CONNECTION)
        )
        return chat_history
