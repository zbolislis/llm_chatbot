import psycopg
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_postgres import PostgresChatMessageHistory

# Establishes connection to PostgreSQL
conn_info = "postgresql://chatbot_user:chatbot_pass@localhost:5432/chatbot_db"
sync_connection = psycopg.connect(conn_info)

# Ensures the memory table exists
table_name = "chat_history"
PostgresChatMessageHistory.create_tables(sync_connection, table_name)

# Initializes the local LLM via Ollama
model = OllamaLLM(model="mistral:7b")

# Defines the prompt template with memory support
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Combines prompt and model into a runnable chain
chain = prompt | model


# Function to retrieve message history for a given session
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        sync_connection=sync_connection
    )


# Wraps the chain with session-specific message history support
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="input",
    history_messages_key="history"
)
