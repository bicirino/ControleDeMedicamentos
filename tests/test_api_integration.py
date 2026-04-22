"""
tests/test_api_integration.py
Testes de integração para consumo de APIs externas.
Valida a comunicação com BrasilAPI.
"""

import pytest
from unittest.mock import patch, MagicMock
import requests

from api_integration import (
    buscar_medicamento_brasalapi,
    validar_conexao_api,
    APIError
)


class TestBrasilAPI:
    """Testes para integração com BrasilAPI."""

    @patch('api_integration.requests.get')
    def test_buscar_medicamento_sucesso(self, mock_get):
        """Testa busca bem-sucedida de medicamento."""
        # Mock da resposta da API
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "nome": "Dipirona",
                "principio_ativo": "Dipirona monoidratada",
                "cnpj": "12345678000123",
                "laboratorio": "Lab XYZ"
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Executa a função
        resultado = buscar_medicamento_brasalapi("Dipirona")

        # Valida resultado
        assert resultado is not None
        assert resultado["nome"] == "Dipirona"
        assert resultado["source"] == "BrasilAPI"
        assert "principio_ativo" in resultado

        # Valida que a requisição foi feita corretamente
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "dipirona" in call_args[1]["params"]["q"].lower()

    @patch('api_integration.requests.get')
    def test_buscar_medicamento_nao_encontrado(self, mock_get):
        """Testa busca de medicamento não encontrado."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        resultado = buscar_medicamento_brasalapi("MedicamentoInexistente")

        assert resultado is None

    @patch('api_integration.requests.get')
    def test_buscar_medicamento_timeout(self, mock_get):
        """Testa timeout na busca de medicamento."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")

        with pytest.raises(APIError, match="Timeout"):
            buscar_medicamento_brasalapi("Dipirona")

    @patch('api_integration.requests.get')
    def test_buscar_medicamento_erro_conexao(self, mock_get):
        """Testa erro de conexão."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Sem conexão")

        with pytest.raises(APIError, match="conexão"):
            buscar_medicamento_brasalapi("Dipirona")

    @patch('api_integration.requests.get')
    def test_buscar_medicamento_erro_http(self, mock_get):
        """Testa erro HTTP 500."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500")
        mock_get.return_value = mock_response

        with pytest.raises(APIError, match="HTTP"):
            buscar_medicamento_brasalapi("Dipirona")



class TestValidacaoConexao:
    """Testes para validação de conexão com APIs."""

    @patch('api_integration.requests.head')
    def test_validar_conexao_sucesso(self, mock_head):
        """Testa validação bem-sucedida de conexão."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        resultado = validar_conexao_api("https://brasilapi.com.br")

        assert resultado is True

    @patch('api_integration.requests.head')
    def test_validar_conexao_servidor_indisponivel(self, mock_head):
        """Testa validação quando servidor retorna erro 500+."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_head.return_value = mock_response

        resultado = validar_conexao_api("https://brasilapi.com.br")

        assert resultado is False

    @patch('api_integration.requests.head')
    def test_validar_conexao_erro_conexao(self, mock_head):
        """Testa validação com erro de conexão."""
        mock_head.side_effect = requests.exceptions.RequestException("Sem conexão")

        resultado = validar_conexao_api("https://brasilapi.com.br")

        assert resultado is False
