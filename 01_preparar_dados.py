"""
Etapa 1 do pipeline: baixa os dados abertos do CNPJ (Receita Federal) e filtra
só o que interessa pro projeto.

Recorte: Sociedades Anônimas Abertas (natureza jurídica 2046), que são as
empresas com conselho de administração e diretoria registrados no QSA.

Saída em data/:
  empresas.csv          razão social, capital social e porte das S.A. abertas
  socios.csv            quadro de sócios e administradores (QSA) dessas empresas
  estabelecimentos.csv  dados da matriz (situação cadastral, CNAE, UF, data de início)

Uso:
  python 01_preparar_dados.py            # baixa (se precisar) e filtra
  python 01_preparar_dados.py --raw DIR  # usa zips que já estão em DIR

Fonte: espelho no GitHub dos arquivos da Receita (snapshot 2024-09),
https://github.com/jonathands/dados-abertos-receita-cnpj
Original: https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/
"""
import argparse
import csv
import io
import os
import urllib.request
import zipfile

BASE = "https://github.com/jonathands/dados-abertos-receita-cnpj/releases/download/2024.09/"
NATUREZA = b'"2046"'  # Sociedade Anônima Aberta

COLS_EMPRESAS = ["cnpj", "razao_social", "natureza", "qual_responsavel",
                 "capital_social", "porte", "ente_federativo"]
COLS_SOCIOS = ["cnpj", "tipo_socio", "nome_socio", "doc_socio", "qualificacao",
               "data_entrada", "pais", "doc_representante", "nome_representante",
               "qual_representante", "faixa_etaria"]
COLS_ESTAB = ["cnpj", "ordem", "dv", "matriz_filial", "nome_fantasia", "situacao",
              "data_situacao", "motivo_situacao", "cidade_exterior", "pais",
              "data_inicio", "cnae_principal", "cnae_secundaria", "tipo_logradouro",
              "logradouro", "numero", "complemento", "bairro", "cep", "uf",
              "municipio", "ddd1", "tel1", "ddd2", "tel2", "ddd_fax", "fax",
              "email", "situacao_especial", "data_situacao_especial"]


def baixar(raw, nome):
    destino = os.path.join(raw, nome)
    if os.path.exists(destino) and zipfile.is_zipfile(destino):
        return destino
    print(f"  baixando {nome} ...", flush=True)
    urllib.request.urlretrieve(BASE + nome, destino)
    return destino


def linhas(caminho_zip):
    """Itera as linhas (bytes) do CSV dentro do zip, sem descompactar no disco."""
    with zipfile.ZipFile(caminho_zip) as z:
        with z.open(z.namelist()[0]) as f:
            for linha in f:
                yield linha


def escrever(caminho, cabecalho, linhas_bytes):
    with open(caminho, "w", encoding="utf-8", newline="") as out:
        w = csv.writer(out, delimiter=";")
        w.writerow(cabecalho)
        for lb in linhas_bytes:
            campos = next(csv.reader(io.StringIO(lb.decode("latin-1").rstrip("\r\n")), delimiter=";"))
            w.writerow(campos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="raw", help="pasta com os zips da Receita")
    ap.add_argument("--out", default="data")
    a = ap.parse_args()
    os.makedirs(a.raw, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)

    # 1) Empresas: filtra natureza jurídica 2046
    print("Empresas (natureza 2046)...")
    emp = []
    for i in range(10):
        for l in linhas(baixar(a.raw, f"Empresas{i}.zip")):
            if l.split(b";", 3)[2] == NATUREZA:
                emp.append(l)
    ids = {l[1:9] for l in emp}
    escrever(os.path.join(a.out, "empresas.csv"), COLS_EMPRESAS, emp)
    print(f"  {len(ids)} empresas")

    # 2) Sócios dessas empresas
    print("Socios...")
    soc = []
    for i in range(10):
        for l in linhas(baixar(a.raw, f"Socios{i}.zip")):
            if l[1:9] in ids:
                soc.append(l)
    escrever(os.path.join(a.out, "socios.csv"), COLS_SOCIOS, soc)
    print(f"  {len(soc)} vinculos")

    # 3) Estabelecimento matriz (ordem 0001) dessas empresas
    print("Estabelecimentos (matriz)... (demora alguns minutos)")
    est = []
    for i in range(10):
        for l in linhas(baixar(a.raw, f"Estabelecimentos{i}.zip")):
            if l[1:9] in ids and l[12:16] == b"0001":
                est.append(l)
    escrever(os.path.join(a.out, "estabelecimentos.csv"), COLS_ESTAB, est)
    print(f"  {len(est)} matrizes")
    print("Pronto.")


if __name__ == "__main__":
    main()
