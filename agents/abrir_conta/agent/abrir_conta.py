from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
import os

load_dotenv()

_llm = init_chat_model(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
)

client = MultiServerMCPClient(
    {
        "conta": {
            "transport": "http",
            "url": "http://recursos:8000/mcp_gateway",
        }  # type: ignore
    }
)

memory = InMemorySaver()


async def build_agent():
    tools = await client.get_tools()

    agent = create_agent(
        _llm,
        tools=tools,
        system_prompt=(
            "Você é um especialista em abertura de contas do banco MDBank. "
            "Colete nome e CPF do cliente e use as tools disponíveis para criar ou consultar contas."
        ),
        checkpointer=memory,
    )

    return agent


async def run_agent(mensagem: str, thread_id: str = "1"):
    agent = await build_agent()

    resultado = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content=mensagem)
            ]
        },
        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return resultado["messages"][-1].content
