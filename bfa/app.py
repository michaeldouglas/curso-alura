from fastapi import FastAPI
from contextlib import asynccontextmanager

from registry import AGENT_REGISTRY
from discovery import discover_agents


@asynccontextmanager
async def lifespan(app: FastAPI):
    agents = await discover_agents()

    AGENT_REGISTRY.update(agents)

    print("Agents discovered:", AGENT_REGISTRY)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/skills")
def listar_skills():
    return AGENT_REGISTRY


@app.get("/skills/{skill}")
def buscar_skill(skill: str):

    agent = AGENT_REGISTRY.get(skill)

    if not agent:
        return {"error": "skill not found"}

    return {
        "skill": skill,
        "agent_url": agent
    }


@app.get("/")
async def health():
    return {"status": "ok"}
