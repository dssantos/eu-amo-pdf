"""Serviço para mesclagem de PDFs."""

import io
from typing import List
from werkzeug.datastructures import FileStorage
from pypdf import PdfReader, PdfWriter
from ..exceptions import PDFMergeError


class MergeService:
    """Serviço responsável pela mesclagem de PDFs."""

    @staticmethod
    def merge_pdfs(files: List[FileStorage]) -> io.BytesIO:
        """
        Mescla múltiplos PDFs em um único arquivo.

        Args:
            files: Lista de arquivos PDF para mesclar

        Returns:
            BytesIO com o PDF mesclado

        Raises:
            PDFMergeError: Se ocorrer erro na mesclagem
        """
        try:
            merger = PdfWriter()
            total_pages = 0

            for file in files:
                pdf_content = file.read()
                pdf_reader = PdfReader(io.BytesIO(pdf_content))

                # Adiciona todas as páginas do PDF
                for page in pdf_reader.pages:
                    merger.add_page(page)
                    total_pages += 1

            if total_pages == 0:
                raise PDFMergeError("Os PDFs não contêm páginas")

            # Criar bytes do PDF mesclado
            merged_pdf = io.BytesIO()
            merger.write(merged_pdf)
            merged_pdf.seek(0)

            return merged_pdf

        except Exception as e:
            if isinstance(e, PDFMergeError):
                raise
            raise PDFMergeError(f"Erro ao mesclar PDFs: {str(e)}")

    @staticmethod
    def get_page_count(files: List[FileStorage]) -> int:
        """
        Conta o total de páginas dos PDFs.

        Args:
            files: Lista de arquivos PDF

        Returns:
            Número total de páginas
        """
        total = 0
        for file in files:
            pdf_content = file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            total += len(pdf_reader.pages)
            file.seek(0)  # Resetar ponteiro
        return total
