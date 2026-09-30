"""
api_integration.py
Módulo para integração com APIs públicas.
Fornece funções para buscar informações sobre medicamentos usando Groq AI.
"""

import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv
from groq import Groq

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


class APIError(Exception):
    """Exceção customizada para erros de API."""
    pass


# Groq descontinuou llama-3.1-8b-instant (ago/2026); substituto oficial.
DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"


def buscar_medicamento_groq(
    nome_medicamento: str
) -> Optional[Dict[str, Any]]:
    """
    Busca informações sobre um medicamento usando Groq AI.

    Args:
        nome_medicamento: Nome do medicamento a buscar.

    Returns:
        Dicionário com informações do medicamento ou None se erro.

    Raises:
        APIError: Se houver erro na comunicação com Groq.
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise APIError(
                "GROQ_API_KEY não configurada. "
                "Configure em .env (copie .env.example)"
            )

        client = Groq(api_key=api_key)
        model = os.getenv("GROQ_MODEL") or DEFAULT_GROQ_MODEL

        prompt = (
            f"Responda em português, de forma direta, sobre o medicamento "
            f"'{nome_medicamento}'. Escreva somente estas quatro linhas, "
            "sem introdução:\n"
            "1. Nome: ...\n"
            "2. Princípio ativo: ...\n"
            "3. Usos comuns: ...\n"
            "4. Contraindicações: ...\n"
            "Se não reconhecer o medicamento, responda apenas: "
            "Medicamento não encontrado."
        )

        pedido = {
            "model": model,
            "max_completion_tokens": 2048,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Você resume medicamentos em português. "
                        "Entregue só o texto final pedido, sem raciocínio."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        }
        # gpt-oss gasta o limite de tokens no raciocínio interno.
        # Com esforço alto e teto baixo, a resposta visível fica só no nome.
        if "gpt-oss" in model:
            pedido["reasoning_effort"] = "low"

        message = client.chat.completions.create(**pedido)

        resposta = (message.choices[0].message.content or "").strip()
        if not resposta:
            raise APIError(
                "A consulta não retornou texto. Tente novamente."
            )
        if getattr(message.choices[0], "finish_reason", None) == "length":
            raise APIError(
                "A resposta da IA foi cortada antes de terminar. "
                "Tente novamente."
            )

        if "não encontrado" in resposta.lower():
            return None

        return {
            "nome": nome_medicamento,
            "informacoes": resposta,
            "source": "Groq AI"
        }

    except Exception as e:
        if "GROQ_API_KEY" in str(e):
            raise APIError(str(e))
        msg = f"Erro ao consultar Groq AI: {str(e)}"
        raise APIError(msg)
