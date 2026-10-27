import csv
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_RESULTADO = BASE_DIR / "data" / "resumo_vendas.csv"
ARQUIVO_PIPELINE = BASE_DIR / "pipeline.py"


def test_pipeline_gera_resumo_correto():
    # Executa o pipeline como se fosse um processo separado.
    resultado = subprocess.run(
        [sys.executable, str(ARQUIVO_PIPELINE)],
        capture_output=True,
        text=True,
        check=True,
    )

    # Confirma que o pipeline terminou com sucesso.
    assert "Pipeline concluído com sucesso!" in resultado.stdout

    # Confirma que o arquivo de saída foi criado.
    assert ARQUIVO_RESULTADO.exists()

    # Lê o arquivo gerado e verifica os valores calculados.
    with open(
        ARQUIVO_RESULTADO, newline="", encoding="utf-8"
    ) as arquivo:
        linhas = list(csv.DictReader(arquivo))

    assert len(linhas) == 4

    produtos = {linha["produto"]: linha for linha in linhas}

    assert float(produtos["Notebook"]["faturamento_total"]) == 10500.0
    assert float(produtos["Monitor"]["faturamento_total"]) == 2700.0
    assert float(produtos["Teclado"]["faturamento_total"]) == 1050.0
    assert float(produtos["Mouse"]["faturamento_total"]) == 560.0