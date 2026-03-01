"""Serviço para compressão de PDFs."""

import io
from werkzeug.datastructures import FileStorage
from pypdf import PdfReader, PdfWriter
from ..exceptions import PDFCompressError


class CompressService:
    """Serviço responsável pela compressão de PDFs."""

    COMPRESSION_LEVELS = {
        "low": 0,
        "medium": 1,
        "high": 2,
    }

    @staticmethod
    def compress_pdf(file: FileStorage, level: str = "medium") -> io.BytesIO:
        """
        Comprime um PDF removendo metadados desnecessários.

        Args:
            file: Arquivo PDF para comprimir
            level: Nível de compressão (low, medium, high)

        Returns:
            BytesIO com o PDF comprimido

        Raises:
            PDFCompressError: Se ocorrer erro na compressão
        """
        if level not in CompressService.COMPRESSION_LEVELS:
            levels = ', '.join(CompressService.COMPRESSION_LEVELS.keys())
            raise PDFCompressError(
                f"Nível de compressão inválido. Use: {levels}"
            )

        try:
            pdf_content = file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))

            writer = PdfWriter()

            # Adiciona páginas com compressão
            for page in pdf_reader.pages:
                writer.add_page(page)

            # Remove metadados para reduzir tamanho
            writer.add_metadata({})

            # Aplicar compressão baseada no nível
            # Nota: pypdf tem compressão limitada, mas podemos
            # remover elementos desnecessários
            if level == "high":
                # Remover metadados adicionais
                if "/Producer" in writer.metadata:
                    del writer.metadata["/Producer"]
                if "/Creator" in writer.metadata:
                    del writer.metadata["/Creator"]

            # Criar bytes do PDF comprimido
            compressed_pdf = io.BytesIO()
            writer.write(compressed_pdf)
            compressed_pdf.seek(0)

            return compressed_pdf

        except Exception as e:
            if isinstance(e, PDFCompressError):
                raise
            raise PDFCompressError(f"Erro ao comprimir PDF: {str(e)}")

    @staticmethod
    def calculate_compression_ratio(original_size: int, compressed_size: int) -> float:
        """
        Calcula a taxa de compressão.

        Args:
            original_size: Tamanho original em bytes
            compressed_size: Tamanho comprimido em bytes

        Returns:
            Porcentual de redução (0-100)
        """
        if original_size == 0:
            return 0.0
        return (1 - compressed_size / original_size) * 100
