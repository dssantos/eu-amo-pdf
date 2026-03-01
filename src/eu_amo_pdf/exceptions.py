"""Exceções customizadas para o aplicativo."""


class PDFProcessingError(Exception):
    """Exceção base para erros de processamento de PDF."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class FileValidationError(PDFProcessingError):
    """Exceção para erros de validação de arquivo."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class PDFMergeError(PDFProcessingError):
    """Exceção para erros na mesclagem de PDFs."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class PDFCompressError(PDFProcessingError):
    """Exceção para erros na compressão de PDFs."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class PDFConversionError(PDFProcessingError):
    """Exceção para erros na conversão de PDFs."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)
