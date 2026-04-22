"""
api_integration.py
Módulo para integração com APIs públicas.
Fornece funções para buscar informações sobre medicamentos.
"""

import requests
from typing import Dict, Optional, Any

# Configurações da API
BRASIL_API_URL = "https://brasilapi.com.br/api/cnes/v1/medicamentos"

# Timeouts para requisições (em segundos)
REQUEST_TIMEOUT = 5


class APIError(Exception):
    """Exceção customizada para erros de API."""
    pass


def buscar_medicamento_brasalapi(
    nome_medicamento: str
) -> Optional[Dict[str, Any]]:
    """
    Busca informações sobre um medicamento na BrasilAPI.

    Args:
        nome_medicamento: Nome do medicamento a buscar.

    Returns:
        Dicionário com informações do medicamento ou None se não encontrado.

    Raises:
        APIError: Se houver erro na comunicação com a API.
    """
    try:
        params = {"q": nome_medicamento}
        response = requests.get(
            BRASIL_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()

        # BrasilAPI retorna uma lista de resultados
        if isinstance(data, list) and len(data) > 0:
            return {
                "nome": data[0].get("nome", nome_medicamento),
                "principio_ativo": data[0].get("principio_ativo", "N/A"),
                "cnpj": data[0].get("cnpj", "N/A"),
                "laboratorio": data[0].get("laboratorio", "N/A"),
                "source": "BrasilAPI"
            }

        return None

    except requests.exceptions.Timeout:
        raise APIError("Timeout ao conectar com BrasilAPI")
    except requests.exceptions.ConnectionError:
        raise APIError("Erro de conexão com BrasilAPI")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return None
        msg = f"Erro HTTP da BrasilAPI: {e}"
        raise APIError(msg)
    except requests.exceptions.RequestException as e:
        msg = f"Erro ao chamar BrasilAPI: {str(e)}"
        raise APIError(msg)


def validar_conexao_api(url: str) -> bool:
    """
    Valida se uma API está acessível.

    Args:
        url: URL da API a validar.

    Returns:
        True se acessível, False caso contrário.
    """
    try:
        response = requests.head(url, timeout=3)
        return response.status_code < 500
    except requests.exceptions.RequestException:
        return False
