from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent,AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.lib.chat_histories import PostgresChatMessageHistoryStore
from app.tools import tools
# initialize the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")
# prompt 
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpfull assistant."
     "Remember my name is {user_name} and my email id is {user_email}. Respond greeting message with name."
     "Make sure to use `document_search` tool for searching information from PDF document."
     "If you can not find information from `document_search` tool then use `search_tool` to get the information from web."),
     ("placeholder","{chat_history}"),
     ("human","{input}"),
     ("placeholder","{agent_scratchpad}")
])

# create agent
agent = create_tool_calling_agent(llm=llm,tools=tools,prompt=prompt)

# create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# create agent with chat history
# history = PostgresChatMessageHistoryStore()

agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history=PostgresChatMessageHistoryStore.get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)