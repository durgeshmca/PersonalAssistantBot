from langchain.embeddings import init_embeddings
from langgraph.store.postgres import PostgresStore
from typing import Optional
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.store.base import BaseStore
from langgraph.graph import START,StateGraph,MessagesState
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import Connection
import uuid
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import InjectedStore
from langgraph.store.base import  BaseStore
from typing_extensions import Annotated
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages,BaseMessage
from langchain_core.runnables.config import RunnableConfig
from app.tools import search_tool
from langgraph.managed import RemainingSteps

load_dotenv()
embedding = init_embeddings(model="all-MiniLM-L6-v2",provider="huggingface")

llm = init_chat_model(model="llama-3.3-70b-versatile",model_provider="groq")

class CustomState(TypedDict):
        user_id: uuid.UUID
        messages: Annotated[list[BaseMessage], add_messages]
        remaining_steps: RemainingSteps
        
def prepare_messages(state: StateGraph,config: RunnableConfig, store:BaseStore):
    # search based on user's last message
    user_id = config.get("configurable", {}).get("user_id")
    items = store.search(
        (user_id, "memories"),
        query=state["messages"][-1].content,
        limit=2
        )
    memories = "\n".join(item.value["text"] for item in items)
    memories = f"## Memories of user\n{memories}" if memories else ""
    # if state["messages"] length is greater than 5 then only 5 messages are considered
    if len(state["messages"]) > 5:
         state["messages"] = state["messages"][-5:]
    
    return [
        {"role": "system", "content": f"You are a helpful assistant.\n{memories}"}
    ] + state["messages"]

# You can also use the store directly within a tool!
def upsert_memory(
    content: str,
    *,
    config: RunnableConfig,
    memory_id: Optional[uuid.UUID] = None,
    store: Annotated[BaseStore, InjectedStore],
):
    """Upsert a memory in the database."""
    # The LLM can use this tool to store a new memory
    user_id = config.get("configurable", {}).get("user_id")
    mem_id = memory_id or uuid.uuid4()
    store.put(
        (user_id, "memories"),
        key=str(mem_id),
        value={"text": content},
    )
    return f"Stored memory {mem_id}"

# create agent
def get_agent(store:BaseStore, checkpointer):
    # trim messages

    agent_with_history = create_react_agent(
        init_chat_model(model="llama-3.3-70b-versatile",model_provider="groq"),
        tools=[upsert_memory,search_tool],
        # The 'prompt' function is run to prepare the messages for the LLM. It is called
        # right before each LLM call
        prompt=prepare_messages,
        store=store,
        state_schema=CustomState,
        checkpointer = checkpointer,
    )
    agent_with_history
    return agent_with_history


