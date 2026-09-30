"""
tests/test_api_integration.py
Testes de integração para consumo de APIs externas.
Valida a comunicação com Groq AI.
"""

import pytest
from unittest.mock import patch, MagicMock

from api_integration import buscar_medicamento_groq, APIError


class TestGroqAPI:
    """Testes para integração com Groq AI."""

    @patch('api_integration.os.getenv')
    @patch('api_integration.Groq')
    def test_buscar_medicamento_sucesso(self, mock_groq_class, mock_getenv):
        """Testa busca bem-sucedida de medicamento."""
        def _getenv(chave, default=None):
            if chave == "GROQ_API_KEY":
                return "test_api_key"
            if chave == "GROQ_MODEL":
                return None
            return default

        mock_getenv.side_effect = _getenv

        # Mock da resposta do Groq (nova API)
        mock_client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = (
            "Paracetamol é usado para dor e febre. "
            "Princípio ativo: Paracetamol. "
            "Contraindicações: hipersensibilidade."
        )
        mock_client.chat.completions.create.return_value.choices = [
            mock_choice
        ]
        mock_groq_class.return_value = mock_client

        # Executa a função
        resultado = buscar_medicamento_groq("Paracetamol")

        # Valida resultado
        assert resultado is not None
        assert resultado["nome"] == "Paracetamol"
        assert resultado["source"] == "Groq AI"
        assert "informacoes" in resultado
        assert "Paracetamol" in resultado["informacoes"]

        # Valida que Groq foi chamado com orçamento para a resposta visível
        mock_groq_class.assert_called_once_with(api_key="test_api_key")
        mock_client.chat.completions.create.assert_called_once()
        pedido = mock_client.chat.completions.create.call_args.kwargs
        assert pedido["model"] == "openai/gpt-oss-20b"
        assert pedido["reasoning_effort"] == "low"
        assert pedido["max_completion_tokens"] == 2048
        assert "max_tokens" not in pedido

    @patch('api_integration.os.getenv')
    @patch('api_integration.Groq')
    def test_buscar_medicamento_nao_encontrado(self, mock_groq_class,
                                               mock_getenv):
        """Testa busca de medicamento não encontrado."""
        mock_getenv.return_value = "test_api_key"

        mock_client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = (
            "Medicamento não encontrado no banco de dados."
        )
        mock_client.chat.completions.create.return_value.choices = [
            mock_choice
        ]
        mock_groq_class.return_value = mock_client

        resultado = buscar_medicamento_groq("MedicamentoInexistente")

        assert resultado is None

    @patch('api_integration.os.getenv')
    def test_buscar_medicamento_sem_api_key(self, mock_getenv):
        """Testa erro quando API key não está configurada."""
        mock_getenv.return_value = None

        with pytest.raises(APIError, match="GROQ_API_KEY"):
            buscar_medicamento_groq("Paracetamol")

    @patch('api_integration.os.getenv')
    @patch('api_integration.Groq')
    def test_buscar_medicamento_erro_conexao(self, mock_groq_class,
                                             mock_getenv):
        """Testa erro na conexão com Groq."""
        mock_getenv.return_value = "test_api_key"

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = \
            Exception("Erro na conexão com Groq")
        mock_groq_class.return_value = mock_client

        with pytest.raises(APIError, match="Erro ao consultar Groq"):
            buscar_medicamento_groq("Paracetamol")

    @patch('api_integration.os.getenv')
    @patch('api_integration.Groq')
    def test_buscar_medicamento_timeout(self, mock_groq_class, mock_getenv):
        """Testa timeout na busca de medicamento."""
        mock_getenv.return_value = "test_api_key"

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = \
            TimeoutError("Timeout na requisição")
        mock_groq_class.return_value = mock_client

        with pytest.raises(APIError, match="Erro ao consultar Groq"):
            buscar_medicamento_groq("Paracetamol")
