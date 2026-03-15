import httpx
from a2a.client import A2ACardResolver

AGENT_ENDPOINTS = [
    "http://cartao_credito_agent:8000",
    "http://abrir_conta_agent:8000"
]


async def discover_agents():

    registry = {}

    async with httpx.AsyncClient(timeout=10) as client:

        for url in AGENT_ENDPOINTS:

            try:
                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=url
                )

                card = await resolver.get_agent_card()

                for skill in card.skills:

                    registry[skill.id] = {
                        "agent_url": url,
                        "name": skill.name,
                        "description": skill.description,
                        "tags": skill.tags,
                        "examples": skill.examples,
                    }

            except Exception as e:
                print(f"Erro descobrindo agente {url}: {e}")

    return registry
