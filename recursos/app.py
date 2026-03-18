from fastmcp import FastMCP
import random

mcp = FastMCP("ContaService")

contas_mdbank = {}
cartoes_mdbank = {}


@mcp.tool
async def criar_ou_buscar_conta(nome: str, cpf: str):
    cpf = cpf.strip()

    if cpf in contas_mdbank:
        return {
            "status": "existente",
            "conta": contas_mdbank[cpf]
        }

    numero_conta = random.randint(10000, 99999)

    conta = {
        "nome": nome,
        "numero": numero_conta,
        "saldo": 0.0,
    }

    contas_mdbank[cpf] = conta

    return {
        "status": "criada",
        "conta": conta
    }


@mcp.tool
async def solicitar_cartao(cpf: str, tipo: str):
    cpf = cpf.strip()

    if cpf not in contas_mdbank:
        return {
            "status": "erro",
            "mensagem": "Cliente não possui conta"
        }

    if cpf in cartoes_mdbank:
        return {
            "status": "existente",
            "cartao": cartoes_mdbank[cpf]
        }

    numero_cartao = random.randint(100000, 999999)

    cartao = {
        "numero": numero_cartao,
        "tipo": tipo,
        "limite": random.randint(1000, 5000)
    }

    cartoes_mdbank[cpf] = cartao

    return {
        "status": "criado",
        "cartao": cartao
    }
