# Rede de administradores compartilhados entre S.A. abertas brasileiras

Projeto final da disciplina OPT108 (Análise de Redes Sociais Utilizando Grafos, UTFPR Campo Mourão).
Grupo 7: Kaike Carvalho, Victor Almeida e Alex Magalhães.

Duas S.A. abertas ficam ligadas quando dividem pelo menos um diretor, conselheiro ou presidente no Quadro de Sócios e Administradores (QSA) da Receita Federal. O peso da aresta é o número de administradores em comum.

## Como reproduzir

```bash
pip install pandas networkx matplotlib scipy
python 01_preparar_dados.py   # baixa ~4 GB de zips da Receita (snapshot 2024-09) e gera data/
jupyter notebook 02_analise.ipynb
```

A pasta `data/` não é versionada. O script `01_preparar_dados.py` gera os arquivos a partir dos dados abertos do CNPJ.

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `01_preparar_dados.py` | Baixa os arquivos Empresas, Sócios e Estabelecimentos e filtra as S.A. abertas (natureza jurídica 2046) |
| `02_analise.ipynb` | Grafo bipartido, projeção, estatísticas descritivas, centralidades, Louvain, evolução temporal |
| `figuras/` | Distribuição de graus, rede colorida por comunidade e evolução temporal |
| `tabelas/` | Estatísticas descritivas, top 10 por centralidade, comunidades e evolução temporal |
| `rede_sa_abertas.gexf` | Rede de empresas com as métricas, para abrir no Gephi |

## Fonte dos dados

Dados abertos do CNPJ, Receita Federal: https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/
Espelho usado (snapshot 2024-09): https://github.com/jonathands/dados-abertos-receita-cnpj

## Plano das 3 semanas finais

| Tarefa | Responsável | Prazo |
|---|---|---|
| Discussão | Alex | 24/11 |
| Conclusão e resumo final | Kaike | 24/11 |
| Repositório no GitHub e revisão das tabelas e figuras | Victor | 24/11 |
| Revisão cruzada do artigo | Todos | 01/12 |
| Slides da apresentação (10 a 15 min) | Kaike | 01/12 |
| Ensaio da apresentação | Todos | 05/12 |
| Entrega final | Victor | 08/12 |
