from fastapi import APIRouter,Body,Depends,UploadFile,File
from app.models.users import UserBase
from app.models.chat import Chat
from app.lib.agents import agent_with_history
from typing import Annotated
from app.auth import get_current_active_user
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
                
        response = response = agent_with_history.invoke(
            {"input": chat.message,"user_name":current_user.first_name, "user_email":current_user.email},
            config={"configurable": {"session_id": str(current_user.user_uuid)}},
        )
        return response



