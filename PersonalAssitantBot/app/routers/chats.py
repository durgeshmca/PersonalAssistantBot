from fastapi import APIRouter,Body,Depends,UploadFile,File
from app.models.users import UserBase
from app.models.chat import Chat
from app.lib.agents import agent_with_history
from app.lib.langgraph_agents import get_agent,embedding
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import Connection
from typing import Annotated
from app.auth import get_current_active_user
from app.config import Config
import os
from app.lib.doc_tools import vectore_store

chat_router = APIRouter()
@chat_router.post("/chat",tags=["chat"])
async def chat_message( 
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    chat: Annotated[Chat, Body()],
    file: Annotated[UploadFile,File()] |None = None
    ):
        if file:
                # save file to three level up data directory
                file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"data",file.filename)
                if file.content_type == 'application/pdf':
                        # create vectore and store file in database

                        with open(file_path,'wb') as fp:
                            fp.write(file.file.read())
                            vectore_store.add_doc_to_store(doc_type="pdf",doc_location=file_path)
                            return file_path
                        
                else:
                        raise Exception("Only PDF files are supported at the moment.")
                
        with PostgresStore.from_conn_string(
            conn_string=Config.PG1_CONNECTION,index={
                "embed": embedding,
                "dims": 384,
                "fields": ["text"]  # specify which fields to embed. Default is the whole serialized valu
            }
        ) as store :
            with Connection.connect(Config.PG1_CONNECTION) as conn:
                checkpointer = PostgresSaver(conn=conn)
                # checkpointer.setup()
                agent_with_history = get_agent(store,checkpointer)
                response = agent_with_history.invoke(input={"messages": [{"role": "user", "content": chat.message}],"user_id":str(current_user.user_uuid)},
                                                    config={"configurable": {"thread_id": "1","user_id": str(current_user.user_uuid)}},
                                                    stream_mode="values"
                                            )
                return response['messages'][-1]
   



