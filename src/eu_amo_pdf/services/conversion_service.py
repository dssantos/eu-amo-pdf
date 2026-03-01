"""Serviço para conversão de PDFs."""

import io
from werkzeug.datastructures import FileStorage
from pypdf import PdfReader
from docx import Document
from ..exceptions import PDFConversionError


class ConversionService:
    """Serviço responsável pela conversão de PDFs."""

    @staticmethod
    def pdf_to_docx(file: FileStorage) -> io.BytesIO:
        """
        Converte um PDF para DOCX extraindo o texto.

        Args:
            file: Arquivo PDF para converter

        Returns:
            BytesIO com o documento DOCX

        Raises:
            PDFConversionError: Se ocorrer erro na conversão
        """
        try:
            pdf_content = file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))

            # Criar documento DOCX
            doc = Document()

            # Extrair texto de cada página
            total_pages = len(pdf_reader.pages)
            text_extracted = False

            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()

                    if text and text.strip():
                        # Adicionar texto ao documento
                        doc.add_paragraph(text.strip())
                        text_extracted = True

                        # Adicionar quebra de página entre páginas do PDF
                        # (exceto na última)
                        if page_num < total_pages:
                            doc.add_page_break()

                except Exception:
                    # Se falhar extrair texto de uma página, continua
                    # mas registra um aviso (silencioso neste caso)
                    continue

            if not text_extracted:
                raise PDFConversionError(
                    "Não foi possível extrair texto do PDF. " "O PDF pode ser uma imagem escaneada."
                )

            # Criar bytes do DOCX
            docx_bytes = io.BytesIO()
            doc.save(docx_bytes)
            docx_bytes.seek(0)

            return docx_bytes

        except PDFConversionError:
            raise
        except Exception as e:
            raise PDFConversionError(f"Erro ao converter PDF para DOCX: {str(e)}")

    @staticmethod
    def extract_text_from_pdf(file: FileStorage) -> str:
        """
        Extrai todo o texto de um PDF.

        Args:
            file: Arquivo PDF

        Returns:
            String com todo o texto extraído

        Raises:
            PDFConversionError: Se ocorrer erro
        """
        try:
            pdf_content = file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))

            all_text = []
            for page in pdf_reader.pages:
                try:
                    text = page.extract_text()
                    if text and text.strip():
                        all_text.append(text.strip())
                except Exception:
                    continue

            return "\n\n".join(all_text)

        except Exception as e:
            raise PDFConversionError(f"Erro ao extrair texto: {str(e)}")
