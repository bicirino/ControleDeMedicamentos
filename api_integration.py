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

        prompt = (
            f"Forneça informações sobre o medicamento '{nome_medicamento}' "
            "em português, incluindo:\n"
            "1. Nome do medicamento\n"
            "2. Princípio ativo (ingrediente principal)\n"
            "3. Usos comuns\n"
            "4. Contraindicações principais\n\n"
            "Responda de forma concisa. Se o medicamento não for "
            "encontrado, responda com 'Medicamento não encontrado'."
        )

        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        resposta = message.choices[0].message.content

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
