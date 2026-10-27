SELECT
    produto,
    SUM(quantidade) AS total_unidades,
    SUM(quantidade * preco_unitario) AS faturamento_total
FROM vendas
GROUP BY produto
ORDER BY faturamento_total DESC;