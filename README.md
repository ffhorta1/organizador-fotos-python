# organizador-fotos-python
# Organizador de Arquivos por Data (Fotos e Outros)

Script em Python para organizar arquivos em pastas por **ano** ou **ano/mês**, com base na data de criação, modificação ou dados EXIF (no caso de fotos).

## 📌 Funcionalidades

- Organiza arquivos por:
  - 📅 Data de criação
  - ✏️ Data de modificação
  - 📷 Data EXIF de fotos (quando disponível)

- Estrutura de pastas:
  - `2024/`
  - `2024/04-Abril/`

- Ação:
  - 📂 Copiar (default)
  - ✂️ Mover arquivos

## 🛠️ Requisitos

- Python 3.6+
- Biblioteca `Pillow` (para ler dados EXIF de imagens)

Instale com:

```bash
pip install Pillow


## 🚀 Como usar
python organizador_fotos.py CAMINHO_DA_PASTA [--data exif|modificacao|criacao] [--acao mover|copiar] [--estrutura ano|ano/mes]

## 📚 Exemplos:
Fotos por data EXIF:
python organizador_fotos.py ./minhas_fotos --data exif --acao copiar --estrutura ano/mes

Documentos por data de modificação:
python organizador_fotos.py ./documentos --data modificacao --acao mover --estrutura ano

## 🧠 Observações
- Para fotos, recomenda-se usar --data exif.

- Arquivos sem data válida são ignorados com aviso no terminal.

- Os nomes dos meses estão em português e podem ser ajustados no código-fonte, se necessário.

## 💻 Autor
Desenvolvido por Fernando Horta como parte de um projeto pessoal de automação com Python.

