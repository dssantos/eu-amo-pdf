# 📄 Eu Amo PDF

Ferramentas web simples para manipulação de PDFs.

![Tests](https://img.shields.io/badge/tests-15%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Flask](https://img.shields.io/badge/flask-3.0+-red)

## ✨ Funcionalidades

- **📋 Mesclar PDFs** - Junte múltiplos arquivos PDF em um único documento
- **🗜️ Comprimir PDFs** - Reduza o tamanho de seus arquivos PDF
- **🔄 PDF para DOCX** - Converta PDFs para documentos Word editáveis

## 🚀 Demonstração

A aplicação está disponível em: [https://eu-amo-pdf.vercel.app](https://eu-amo-pdf.vercel.app) (exemplo)

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Docker (opcional, para execução em container)

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/dssantos/eu-amo-pdf.git
cd eu-amo-pdf
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -e ".[dev]"
```

Isso instalará:
- Flask - Framework web
- pypdf - Manipulação de PDFs
- python-docx - Criação de documentos DOCX
- pytest - Framework de testes
- black - Formatador de código
- flake8 - Linter de código

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto (baseado em `.env.example`):

```bash
cp .env.example .env
```

Variáveis de ambiente disponíveis:

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `FLASK_APP` | Módulo da aplicação Flask | `src.eu_amo_pdf` |
| `FLASK_ENV` | Ambiente (`development`/`production`) | `development` |
| `SECRET_KEY` | Chave secreta para sessões | `change-me` |
| `MAX_UPLOAD_SIZE` | Tamanho máximo de upload (bytes) | `16777216` (16MB) |
| `DEBUG` | Modo debug | `True` |

## 🎯 Como usar

### Modo de desenvolvimento

```bash
flask run
```

A aplicação estará disponível em [http://localhost:5000](http://localhost:5000)

### Com Docker

```bash
docker-compose up
```

A aplicação estará disponível em [http://localhost:5000](http://localhost:5000)

## 📚 Funcionalidades Detalhadas

### 1. Mesclar PDFs

**Rota:** `GET /merge`

**Endpoint da API:** `POST /api/merge`

**Como usar:**

1. Acesse `/merge`
2. Selecione 2 ou mais arquivos PDF
3. Clique em "Mesclar PDFs"
4. Baixe o PDF mesclado

**Validações:**
- Mínimo de 2 arquivos
- Apenas arquivos PDF são aceitos
- Limite de 16MB por upload

### 2. Comprimir PDFs

**Rota:** `GET /compress`

**Endpoint da API:** `POST /api/compress`

**Como usar:**

1. Acesse `/compress`
2. Selecione um arquivo PDF
3. Escolha o nível de compressão (baixa/média/alta)
4. Clique em "Comprimir PDF"
5. Veja o percentual de redução e baixe o PDF

**Níveis de compressão:**
- **Baixa** - Melhor qualidade, menor compressão
- **Média** - Balanceado (recomendado)
- **Alta** - Menor tamanho, maior compressão

### 3. PDF para DOCX

**Rota:** `GET /pdf-to-doc`

**Endpoint da API:** `POST /api/pdf-to-doc`

**Como usar:**

1. Acesse `/pdf-to-doc`
2. Selecione um arquivo PDF
3. Clique em "Converter para DOCX"
4. Baixe o documento Word

**Limitações:**
- Apenas texto é extraído
- Imagens não são convertidas
- Formatação complexa pode não ser preservada
- Tabelas podem não ser mantidas

## 🧪 Testes

### Executar todos os testes

```bash
pytest tests/ -v
```

### Executar testes com cobertura

```bash
pytest --cov=src/eu_amo_pdf tests/
```

### Executar testes de um arquivo específico

```bash
pytest tests/test_merge_pdf.py -v
```

**Suíte de testes atual:** 15 testes passando

- `test_app.py` - Testes básicos da aplicação (2 testes)
- `test_merge_pdf.py` - Testes de mesclagem (5 testes)
- `test_compress_pdf.py` - Testes de compressão (4 testes)
- `test_pdf_to_doc.py` - Testes de conversão (4 testes)

## 📁 Estrutura do Projeto

```
eu-amo-pdf/
├── src/
│   └── eu_amo_pdf/
│       ├── __init__.py          # Fábrica da aplicação Flask
│       ├── routes.py            # Rotas e endpoints da API
│       ├── static/
│       │   ├── css/             # Estilos CSS
│       │   └── uploads/         # Arquivos temporários
│       └── templates/           # Templates HTML
│           ├── base.html
│           ├── index.html
│           ├── merge.html
│           ├── compress.html
│           └── pdf-to-doc.html
├── tests/                       # Testes automatizados
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_merge_pdf.py
│   ├── test_compress_pdf.py
│   └── test_pdf_to_doc.py
├── Dockerfile                   # Imagem Docker
├── docker-compose.yml           # Compose Docker
├── pyproject.toml              # Dependências do projeto
├── .env.example                # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```

## 🐳 Docker

### Build da imagem

```bash
docker build -t eu-amo-pdf .
```

### Executar container

```bash
docker run -p 5000:5000 eu-amo-pdf
```

### Com docker-compose

```bash
docker-compose up
```

## 🔄 Desenvolvimento

### Executar com auto-reload

```bash
flask run --reload
```

### Formatar código

```bash
black src/ tests/
```

### Verificar estilo do código

```bash
flake8 src/ tests/
```

## 📝 API Endpoints

### Mesclar PDFs

```http
POST /api/merge
Content-Type: multipart/form-data

files: <arquivo1.pdf>
files: <arquivo2.pdf>
```

**Response:**
- `200` - PDF mesclado (application/pdf)
- `400` - Erro de validação
- `500` - Erro interno

### Comprimir PDF

```http
POST /api/compress
Content-Type: multipart/form-data

file: <arquivo.pdf>
level: <low|medium|high>
```

**Response:**
- `200` - PDF comprimido (application/pdf)
- `400` - Erro de validação
- `500` - Erro interno

### Converter PDF para DOCX

```http
POST /api/pdf-to-doc
Content-Type: multipart/form-data

file: <arquivo.pdf>
```

**Response:**
- `200` - Documento DOCX (application/vnd.openxmlformats-officedocument.wordprocessingml.document)
- `400` - Erro de validação
- `500` - Erro interno

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Padrões de commit

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças na documentação
- `test:` - Adição de testes
- `refactor:` - Refatoração de código
- `chore:` - Mudanças de manutenção

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Danilo Santos**

- GitHub: [@dssantos](https://github.com/dssantos)

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [pypdf](https://pypdf.readthedocs.io/) - Manipulação de PDFs
- [python-docx](https://python-docx.readthedocs.io/) - Criação de DOCX
- [Bootstrap](https://getbootstrap.com/) - Framework CSS

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
