#!/usr/bin/env python3
"""Script para iniciar o servidor Flask."""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from eu_amo_pdf import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📄 Acesse: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para parar")
    app.run(host='0.0.0.0', port=5000, debug=True)
