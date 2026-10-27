import csv
import sqlite3
from pathlib import Path


# Localiza a pasta do projeto, independentemente de onde o comando for executado.
BASE_DIR = Path(__file__).resolve().parent

ARQUIVO_CSV = BASE_DIR / "data" / "vendas.csv"
ARQUIVO_SQL = BASE_DIR / "sql" / "resumo_vendas.sql"
ARQUIVO_RESULTADO = BASE_DIR / "data" / "resumo_vendas.csv"
BANCO_DADOS = BASE_DIR / "data" / "vendas.db"


def executar_pipeline():
    print("Iniciando pipeline de vendas...")

    # 1. Lê os dados do CSV.
    with open(ARQUIVO_CSV, newline="", encoding="utf-8") as arquivo:
        vendas = list(csv.DictReader(arquivo))

    if not vendas:
        raise ValueError("O arquivo de vendas está vazio.")

    print(f"Dados lidos: {len(vendas)} vendas.")

    # 2. Cria uma tabela no SQLite e carrega os dados.
    with sqlite3.connect(BANCO_DADOS) as conexao:
        conexao.execute("DROP TABLE IF EXISTS vendas")

        conexao.execute("""
            CREATE TABLE vendas (
                id_venda INTEGER,
                produto TEXT,
                quantidade INTEGER,
                preco_unitario REAL
            )
        """)

        conexao.executemany(
            """
            INSERT INTO vendas (
                id_venda, produto, quantidade, preco_unitario
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    int(venda["id_venda"]),
                    venda["produto"],
                    int(venda["quantidade"]),
                    float(venda["preco_unitario"]),
                )
                for venda in vendas
            ],
        )

        # 3. Lê e executa o SQL que criamos na etapa anterior.
        consulta_sql = ARQUIVO_SQL.read_text(encoding="utf-8")
        cursor = conexao.execute(consulta_sql)
        resultados = cursor.fetchall()
        colunas = [coluna[0] for coluna in cursor.description]

    # 4. Salva o resultado em um novo CSV.
    with open(
        ARQUIVO_RESULTADO, "w", newline="", encoding="utf-8"
    ) as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(colunas)
        escritor.writerows(resultados)

    print(f"Resumo gerado: {ARQUIVO_RESULTADO.name}")
    print("Pipeline concluído com sucesso!")


if __name__ == "__main__":
    executar_pipeline()
