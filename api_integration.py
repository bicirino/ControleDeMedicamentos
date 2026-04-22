"""
api_integration.py
Módulo para integração com APIs públicas (BrasilAPI e OpenWeather).
Fornece funções para buscar informações sobre medicamentos e clima.
"""

import requests
import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()

# Configurações de APIs
BRASIL_API_URL = "https://brasilapi.com.br/api/cnes/v1/medicamentos"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Timeouts para requisições (em segundos)
REQUEST_TIMEOUT = 5


class APIError(Exception):
    """Exceção customizada para erros de API."""
    pass


def buscar_medicamento_brasalapi(nome_medicamento: str) -> Optional[Dict[str, Any]]:
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
        raise APIError(f"Erro HTTP da BrasilAPI: {e}")
    except requests.exceptions.RequestException as e:
        raise APIError(f"Erro ao chamar BrasilAPI: {str(e)}")


def buscar_clima(cidade: str, pais_codigo: str = "BR") -> Optional[Dict[str, Any]]:
    """
    Busca informações de clima da OpenWeather API.

    Args:
        cidade: Nome da cidade.
        pais_codigo: Código do país (padrão: BR).

    Returns:
        Dicionário com informações de clima ou None se erro.

    Raises:
        APIError: Se houver erro na comunicação com a API.
    """
    if not OPENWEATHER_API_KEY:
        raise APIError("OPENWEATHER_API_KEY não configurada")

    try:
        params = {
            "q": f"{cidade},{pais_codigo}",
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }

        response = requests.get(
            OPENWEATHER_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()

        return {
            "cidade": data.get("name", cidade),
            "pais": data.get("sys", {}).get("country", pais_codigo),
            "temperatura": data.get("main", {}).get("temp", "N/A"),
            "descricao": data.get("weather", [{}])[0].get("description", "N/A"),
            "umidade": data.get("main", {}).get("humidity", "N/A"),
            "velocidade_vento": data.get("wind", {}).get("speed", "N/A"),
            "source": "OpenWeather"
        }

    except requests.exceptions.Timeout:
        raise APIError("Timeout ao conectar com OpenWeather")
    except requests.exceptions.ConnectionError:
        raise APIError("Erro de conexão com OpenWeather")
    except requests.exceptions.HTTPError as e:
        raise APIError(f"Erro HTTP da OpenWeather: {e}")
    except requests.exceptions.RequestException as e:
        raise APIError(f"Erro ao chamar OpenWeather: {str(e)}")


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
