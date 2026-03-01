#!/usr/bin/env python3
"""Script para criar PDFs realistas com conteúdo gerado para testes."""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
from datetime import datetime


def create_business_report(filename):
    """Cria um relatório de negócios realista."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    story = []

    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        spaceAfter=30,
    )
    story.append(Paragraph("Relatório Anual de Performance 2024", title_style))
    story.append(Spacer(1, 12))

    # Subtítulo
    subtitle = Paragraph(
        "<b>Empresa Tech Solutions Ltda.</b><br/><br/>"
        "Preparado por: Departamento de Finanças<br/>"
        f"Data: {datetime.now().strftime('%d/%m/%Y')}",
        styles['Normal']
    )
    story.append(subtitle)
    story.append(Spacer(1, 24))

    # Sumário Executivo
    story.append(Paragraph("Sumário Executivo", styles['Heading2']))
    story.append(Spacer(1, 12))

    summary_text = (
        "Este relatório apresenta uma análise abrangente do desempenho financeiro "
        "e operacional da nossa empresa durante o ano fiscal de 2024. Os resultados "
        "demonstram um crescimento consistente em todos os principais indicadores, "
        "com destaque para o aumento de 34% na receita líquida e a expansão para "
        "três novos mercados internacionais."
    )
    story.append(Paragraph(summary_text, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Tabela de dados
    story.append(Paragraph("Indicadores Financeiros", styles['Heading2']))
    story.append(Spacer(1, 12))

    data = [
        ['Indicador', '2023', '2024', 'Variação'],
        ['Receita Líquida', 'R$ 12.5M', 'R$ 16.8M', '+34%'],
        ['Lucro Operacional', 'R$ 2.8M', 'R$ 4.1M', '+46%'],
        ['Margem de Lucro', '22.4%', '24.4%', '+2.0pp'],
        ['Clientes Ativos', '1,250', '1,890', '+51%'],
        ['Custo por Aquisição', 'R$ 450', 'R$ 380', '-16%'],
    ]

    table = Table(data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 24))

    # Conclusões
    story.append(Paragraph("Conclusões e Recomendações", styles['Heading2']))
    story.append(Spacer(1, 12))

    conclusions = (
        "Com base nos resultados apresentados, recomendamos:<br/><br/>"
        "• Continuar investindo em expansão internacional, focando nos mercados "
        "asiático e europeu.<br/>"
        "• Aumentar o orçamento de P&D em 20% para manter a vantagem competitiva.<br/>"
        "• Implementar novo sistema de CRM para melhorar retenção de clientes.<br/>"
        "• Considerar abertura de capital em 2025, dado o momento positivo da empresa."
    )
    story.append(Paragraph(conclusions, styles['BodyText']))

    doc.build(story)
    print(f"✅ Criado: {filename} (Relatório de Negócios)")


def create_technical_document(filename):
    """Cria um documento técnico realista."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Capa
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.darkgreen,
        alignment=TA_CENTER,
        spaceAfter=30,
    )
    story.append(Paragraph("Documentação Técnica", title_style))
    story.append(Paragraph("Sistema de Gestão Empresarial v2.0", styles['Heading2']))
    story.append(Spacer(1, 48))
    story.append(Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
    story.append(PageBreak())

    # Introdução
    story.append(Paragraph("1. Introdução", styles['Heading2']))
    story.append(Spacer(1, 12))

    intro_text = (
        "Este documento descreve a arquitetura, funcionalidades e especificações "
        "técnicas do Sistema de Gestão Empresarial (SGE) versão 2.0. O sistema foi "
        "desenvolvido utilizando as mais modernas tecnologias e práticas de "
        "desenvolvimento de software, garantindo escalabilidade, segurança e "
        "performance."
    )
    story.append(Paragraph(intro_text, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Arquitetura
    story.append(Paragraph("2. Arquitetura do Sistema", styles['Heading2']))
    story.append(Spacer(1, 12))

    arch_text = (
        "<b>2.1 Visão Geral</b><br/><br/>"
        "O SGE v2.0 adota uma arquitetura de microsserviços, permitindo "
        "escalabilidade independente de cada módulo. Os principais componentes são:"
    )
    story.append(Paragraph(arch_text, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Lista de componentes
    components = [
        ['Componente', 'Descrição', 'Tecnologia'],
        ['API Gateway', 'Roteamento e autenticação', 'Kong + JWT'],
        ['Serviço de Usuários', 'Gerenciamento de contas', 'Python + FastAPI'],
        ['Serviço de Pedidos', 'Processamento de vendas', 'Go + gRPC'],
        ['Serviço de Pagamentos', 'Integração bancária', 'Node.js + Stripe'],
        ['Database', 'Persistência de dados', 'PostgreSQL + Redis'],
    ]

    table = Table(components, colWidths=[2.5*inch, 3*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ]))
    story.append(table)
    story.append(Spacer(1, 24))

    # Especificações Técnicas
    story.append(Paragraph("3. Especificações Técnicas", styles['Heading2']))
    story.append(Spacer(1, 12))

    specs = [
        '• Requisitos mínimos: 4GB RAM, 2 CPU cores',
        '• Sistema operacional: Linux (Ubuntu 20.04 ou superior)',
        '• Banco de dados: PostgreSQL 14+',
        '• Cache: Redis 7.0+',
        '• Container: Docker 24.0+',
        '• Orquestração: Kubernetes 1.28+',
    ]

    for spec in specs:
        story.append(Paragraph(spec, styles['BodyText']))

    doc.build(story)
    print(f"✅ Criado: {filename} (Documento Técnico)")


def create_legal_document(filename):
    """Cria um documento jurídico realista."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Cabeçalho
    story.append(Paragraph("CONTRATO DE PRESTAÇÃO DE SERVIÇOS", styles['Heading1']))
    story.append(Spacer(1, 24))

    # Preamble
    preamble = (
        "<b>CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE DESENVOLVIMENTO DE SOFTWARE</b><br/><br/>"
        "Pelo presente instrumento, as partes a seguir qualificadas têm, entre si, "
        "justo e contratado o presente Contrato de Prestação de Serviços, nas "
        "condições abaixo estabelecidas:"
    )
    story.append(Paragraph(preamble, styles['Normal']))
    story.append(Spacer(1, 24))

    # Das Partes
    story.append(Paragraph("DAS PARTES", styles['Heading2']))
    story.append(Spacer(1, 12))

    partes = (
        "<b>CONTRATADA:</b> Tech Solutions Ltda., empresa com sede na Av. Paulista, "
        "1000, São Paulo/SP, inscrita no CNPJ sob o nº 12.345.678/0001-90.<br/><br/>"
        "<b>CONTRATANTE:</b> Indústria Brasileira de Produtos S.A., empresa com sede "
        "na Rua das Indústrias, 500, Rio de Janeiro/RJ, inscrita no CNPJ sob o nº "
        "98.765.432/0001-10."
    )
    story.append(Paragraph(partes, styles['BodyText']))
    story.append(Spacer(1, 24))

    # Do Objeto
    story.append(Paragraph("DO OBJETO", styles['Heading2']))
    story.append(Spacer(1, 12))

    objeto = (
        "O presente contrato tem como objeto a prestação de serviços de desenvolvimento "
        "e manutenção de sistemas de software, conforme especificações técnicas "
        "constantes no Anexo I, que passa a fazer parte integrante deste instrumento."
    )
    story.append(Paragraph(objeto, styles['BodyText']))
    story.append(Spacer(1, 24))

    # Do Valor
    story.append(Paragraph("DO VALOR E FORMA DE PAGAMENTO", styles['Heading2']))
    story.append(Spacer(1, 12))

    valor = (
        "Pelos serviços prestados, a CONTRATANTE pagará à CONTRATADA o valor total "
        "de R$ 150.000,00 (cento e cinquenta mil reais), conforme as seguintes "
        "condições:<br/><br/>"
        "• 30% na assinatura do contrato<br/>"
        "• 40% na entrega da versão beta<br/>"
        "• 30% na aprovação final"
    )
    story.append(Paragraph(valor, styles['BodyText']))
    story.append(Spacer(1, 24))

    # Cláusulas
    story.append(Paragraph("DAS DISPOSIÇÕES GERAIS", styles['Heading2']))
    story.append(Spacer(1, 12))

    clausulas = [
        "O prazo de vigência deste contrato é de 12 (doze) meses, contados a partir "
        "da data de sua assinatura.",

        "A CONTRATADA compromete-se a manter sigilo absoluto sobre todas as "
        "informações técnicas e comerciais a que tiver acesso em virtude da "
        "prestação dos serviços.",

        "Qualquer alteração nas condições deste contrato deverá ser formalizada "
        "por meio de termo aditativo, assinado pelas partes.",

        "As partes elegem o foro da comarca de São Paulo para dirimir quaisquer "
        "dúvidas ou controvérsias decorrentes deste contrato.",
    ]

    for i, clausula in enumerate(clausulas, 1):
        story.append(Paragraph(f"<b>Cláusula {i}.</b> " + clausula, styles['BodyText']))
        story.append(Spacer(1, 12))

    # Assinaturas
    story.append(PageBreak())
    story.append(Spacer(1, 200))
    story.append(Paragraph("São Paulo, " + datetime.now().strftime('%d de %B de %Y'), styles['Normal']))
    story.append(Spacer(1, 48))

    signature_table = [
        ['__________________________________', '__________________________________'],
        ['Tech Solutions Ltda.', 'Indústria Brasileira de Produtos S.A.'],
        ['Contratada', 'Contratante'],
    ]

    table = Table(signature_table, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table)

    doc.build(story)
    print(f"✅ Criado: {filename} (Documento Jurídico)")


def create_marketing_brochure(filename):
    """Cria um folheto de marketing realista."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Header colorido
    story.append(Spacer(1, -40))
    story.append(Paragraph(
        "<font name='Helvetica' size='28' color='white'>Produto Revolucionário 2024</font>",
        ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            backColor=colors.orange,
            spaceAfter=30,
        )
    ))

    # Subtítulo
    subtitle = Paragraph(
        "<b>Transforme sua empresa com nossa solução inovadora</b>",
        ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            spaceAfter=30,
        )
    )
    story.append(subtitle)

    # Destaques
    highlights = [
        "🚀 Aumente a produtividade em 300%",
        "💰 Reduza custos operacionais em até 50%",
        "⏱️ Implementação em menos de 30 dias",
        "🌟 Suporte 24/7 em português",
    ]

    for highlight in highlights:
        story.append(Paragraph(highlight, styles['Normal']))
        story.append(Spacer(1, 12))

    story.append(Spacer(1, 24))

    # Seção de benefícios
    story.append(Paragraph("Por que escolher nossa solução?", styles['Heading2']))
    story.append(Spacer(1, 12))

    benefits = [
        ('Facilidade de Uso',
         'Interface intuitiva que não requer treinamento extenso. '
         'Sua equipe estará produtiva desde o primeiro dia.'),

        ('Integração Completa',
         'Conecte-se com mais de 200 ferramentas que você já utiliza. '
         'API aberta para integrações customizadas.'),

        ('Segurança Máxima',
         'Certificação ISO 27001, criptografia de ponta a ponta, '
         'backup automático e compliance com LGPD.'),

        ('Suporte Excepcional',
         'Equipe dedicada de sucesso do cliente. '
         'Tempo médio de resposta: menos de 2 horas.'),
    ]

    for title, desc in benefits:
        benefit_style = ParagraphStyle(
            'Benefit',
            parent=styles['Heading3'],
            textColor=colors.darkblue,
            spaceAfter=6,
        )
        story.append(Paragraph(title, benefit_style))
        story.append(Paragraph(desc, styles['BodyText']))
        story.append(Spacer(1, 12))

    # CTA
    story.append(Spacer(1, 24))
    cta = Paragraph(
        "<font name='Helvetica-Bold' size='14' color='white'>"
        "📞 Entre em contato agora: (11) 99999-9999 | www.exemplo.com.br"
        "</font>",
        ParagraphStyle(
            'CTA',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            backColor=colors.darkblue,
            spaceAfter=30,
            spaceBefore=20,
        )
    )
    story.append(cta)

    doc.build(story)
    print(f"✅ Criado: {filename} (Folheto de Marketing)")


def create_research_paper(filename):
    """Cria um artigo científico realista."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Título
    title_style = ParagraphStyle(
        'PaperTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    story.append(Paragraph(
        "Análise Comparativa de Algoritmos de Machine Learning "
        "na Previsão de Séries Temporais Financeiras",
        title_style
    ))

    # Autores
    authors = Paragraph(
        "<b>Silva, J.A.</b>¹, <b>Santos, M.B.</b>², <b>Oliveira, P.R.</b>¹<br/>"
        "<font size='10'>¹Departamento de Ciência da Computação, Universidade de São Paulo</font><br/>"
        "<font size='10'>²Instituto de Matemática e Estatística, Universidade de São Paulo</font>",
        ParagraphStyle('Authors', parent=styles['Normal'], alignment=TA_CENTER, spaceAfter=30)
    )
    story.append(authors)

    # Resumo
    story.append(Paragraph("RESUMO", styles['Heading2']))
    story.append(Spacer(1, 12))

    abstract = (
        "Este trabalho apresenta uma análise comparativa de algoritmos de machine learning "
        "aplicados à previsão de séries temporais financeiras. Foram avaliados LSTM, "
        "GRU, Transformer e XGBoost utilizando dados de ações negociadas na B3. "
        "Os resultados demonstram que o modelo Transformer obteve o melhor desempenho, "
        "com RMSE 23% inferior ao modelo baseline. O estudo também identifica que a "
        "incorporação de características técnicas e indicadores macroeconômicos "
        "melhora significativamente a precisão das previsões."
    )
    story.append(Paragraph(abstract, styles['BodyText']))
    story.append(Spacer(1, 24))

    # 1. Introdução
    story.append(Paragraph("1. INTRODUÇÃO", styles['Heading2']))
    story.append(Spacer(1, 12))

    intro1 = (
        "A previsão de séries temporais financeiras representa um dos desafios mais "
        "significativos e lucrativos na área de finanças quantitativas. Nos últimos anos, "
        "o avanço das técnicas de aprendizado de máquina tem proporcionado novas "
        "ferramentas para abordar este problema clássico."
    )
    story.append(Paragraph(intro1, styles['BodyText']))
    story.append(Spacer(1, 12))

    intro2 = (
        "Este artigo contribui para a literatura ao: (i) realizar uma comparação "
        "sistemática de quatro arquiteturas state-of-the-art; (ii) propor uma metodologia "
        "para feature engineering específica para o mercado brasileiro; (iii) apresentar "
        "resultados empíricos robustos utilizando dados reais da B3."
    )
    story.append(Paragraph(intro2, styles['BodyText']))
    story.append(Spacer(1, 24))

    # 2. Metodologia
    story.append(Paragraph("2. METODOLOGIA", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("2.1 Coleta de Dados", styles['Heading3']))
    story.append(Spacer(1, 12))

    data_text = (
        "Foram coletados dados diários de 50 ações negociadas na B3 no período de "
        "janeiro de 2018 a dezembro de 2023. As variáveis incluem preço de abertura, "
        "fechamento, máxima, mínima, volume e indicadores técnicos (média móvel, "
        "RSI, MACD, Bollinger Bands)."
    )
    story.append(Paragraph(data_text, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Tabela de resultados
    story.append(Paragraph("3. RESULTADOS", styles['Heading2']))
    story.append(Spacer(1, 12))

    results_data = [
        ['Modelo', 'RMSE', 'MAE', 'R²', 'Tempo de Treino (min)'],
        ['LSTM', '0.0234', '0.0189', '0.87', '45'],
        ['GRU', '0.0251', '0.0198', '0.85', '38'],
        ['Transformer', '0.0178', '0.0142', '0.92', '67'],
        ['XGBoost', '0.0198', '0.0156', '0.89', '12'],
    ]

    results_table = Table(results_data, colWidths=[2*inch, 1*inch, 1*inch, 0.8*inch, 1.2*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 24))

    # Conclusão
    story.append(Paragraph("4. CONCLUSÃO", styles['Heading2']))
    story.append(Spacer(1, 12))

    conclusion = (
        "Os resultados demonstram que modelos baseados em attention mechanism "
        "(Transformer) apresentam superioridade na tarefa de previsão de séries "
        "temporais financeiras, embora com maior custo computacional. Trabalhos "
        "futuros devem investigar técnicas de compressão de modelos e otimização "
        "para deploy em ambientes de produção."
    )
    story.append(Paragraph(conclusion, styles['BodyText']))

    doc.build(story)
    print(f"✅ Criado: {filename} (Artigo Científico)")


if __name__ == "__main__":
    print("📄 Criando PDFs realistas para testes...\n")

    # Criar PDFs realistas
    create_business_report("examples/relatorio_negocios.pdf")
    create_technical_document("examples/documento_tecnico.pdf")
    create_legal_document("examples/contrato_juridico.pdf")
    create_marketing_brochure("examples/folheto_marketing.pdf")
    create_research_paper("examples/artigo_cientifico.pdf")

    # Criar versões menores para testes rápidos
    create_business_report("examples/relatorio_curto.pdf")
    create_technical_document("examples/tecnico_curto.pdf")

    print("\n✨ PDFs realistas criados com sucesso!")
    print("📁 Localização: pasta examples/")
    print(f"📊 Total: 7 arquivos PDF")
