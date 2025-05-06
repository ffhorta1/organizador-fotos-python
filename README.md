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
