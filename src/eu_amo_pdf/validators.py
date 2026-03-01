"""Validadores para entrada de dados."""

import os
from werkzeug.datastructures import FileStorage
from typing import List
from .exceptions import FileValidationError


class FileValidator:
    """Validador para arquivos enviados."""

    ALLOWED_EXTENSIONS = {"pdf"}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

    @classmethod
    def validate_pdf_file(cls, file: FileStorage) -> None:
        """
        Valida se o arquivo é um PDF válido.

        Args:
            file: Arquivo enviado

        Raises:
            FileValidationError: Se o arquivo for inválido
        """
        if not file:
            raise FileValidationError("Nenhum arquivo enviado")

        if file.filename == "":
            raise FileValidationError("Arquivo sem nome")

        if not cls._has_allowed_extension(file.filename):
            raise FileValidationError("O arquivo deve ser um PDF")

        if not cls._is_valid_size(file):
            raise FileValidationError(
                f"Arquivo muito grande. Máximo: {cls.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

    @classmethod
    def validate_pdf_files(cls, files: List[FileStorage], min_count: int = 1) -> None:
        """
        Valida múltiplos arquivos PDF.

        Args:
            files: Lista de arquivos enviados
            min_count: Quantidade mínima de arquivos

        Raises:
            FileValidationError: Se a validação falhar
        """
        if not files or len(files) < min_count:
            raise FileValidationError(f"É necessário enviar pelo menos {min_count} arquivo(s)")

        for file in files:
            cls.validate_pdf_file(file)

    @classmethod
    def _has_allowed_extension(cls, filename: str) -> bool:
        """Verifica se o arquivo tem extensão permitida."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in cls.ALLOWED_EXTENSIONS

    @classmethod
    def _is_valid_size(cls, file: FileStorage) -> bool:
        """Verifica se o arquivo tem tamanho válido."""
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size <= cls.MAX_FILE_SIZE
