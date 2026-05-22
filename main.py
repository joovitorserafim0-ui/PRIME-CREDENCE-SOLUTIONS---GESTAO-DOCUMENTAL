import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
import json

class RelatorioFinanceiro(FPDF):
    def header(self):
        # Cabeçalho corporativo com nome de credibilidade
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "PRIME CREDENCE SOLUTIONS - GESTAO DOCUMENTAL", 0, 1, "C")
        self.set_font("Arial", "", 10)
        self.cell(0, 5, f"Relatorio de Monitoramento | {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()} | CONFIDENCIAL - USO INTERNO", 0, 0, "C")

def gerar_arquivos():
    # 1. Carregamento dos dados
    try:
        df = pd.read_csv('base_diaria_financeira.csv')
    except FileNotFoundError:
        print("Erro: O arquivo 'base_diaria_financeira.csv' não foi localizado.")
        return

    # 2. Exportação JSON (Integração sistêmica)
    dados_dict = df.to_dict(orient='records')
    resumo_meta = {
        "timestamp": datetime.now().isoformat(),
        "total_casos": len(df),
        "status_contagem": df['status'].value_counts().to_dict()
    }
    
    with open('relatorio_integracao.json', 'w', encoding='utf-8') as f:
        json.dump({"metadata": resumo_meta, "detalhes": dados_dict}, f, indent=4, ensure_ascii=False)

    # 3. Geração do PDF
    pdf = RelatorioFinanceiro()
    pdf.add_page()
    
    # Resumo Executivo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "RESUMO OPERACIONAL DE RISCO", 0, 1, "L")
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Total de processos na esteira: {len(df)}", ln=True)
    pdf.cell(0, 7, f"Casos Concluidos: {len(df[df['status'] == 'Concluído'])}", ln=True)
    pdf.cell(0, 7, f"Casos Parados: {len(df[df['status'] == 'Parado'])}", ln=True)
    pdf.cell(0, 7, f"Casos em Andamento: {len(df[df['status'] == 'Em Andamento'])}", ln=True)
    pdf.ln(10)

    # Tabela com cores condicionais
    pdf.set_font("Arial", "B", 9)
    cols = ['ID', 'LOJA', 'VALOR R$', 'STATUS', 'DIAS', 'RISCO']
    widths = [12, 50, 30, 30, 20, 30]
    
    # Cabeçalho da tabela (Fundo Escuro / Texto Branco)
    pdf.set_fill_color(50, 50, 50) 
    pdf.set_text_color(255, 255, 255)
    for i, col in enumerate(cols):
        pdf.cell(widths[i], 8, col, 1, 0, 'C', True)
    pdf.ln()

    # Linhas de dados
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 8)
    
    for _, row in df.iterrows():
        if pdf.get_y() > 260: pdf.add_page()
            
        # Lógica de cores (Semáforo de Risco)
        if row['status'] == 'Concluído': pdf.set_fill_color(200, 255, 200) # Verde
        elif row['status'] == 'Parado' and row['dias_parado'] > 15: pdf.set_fill_color(255, 150, 150) # Vermelho
        elif row['status'] == 'Parado': pdf.set_fill_color(255, 255, 200) # Amarelo
        else: pdf.set_fill_color(255, 255, 255) # Branco
        
        pdf.cell(widths[0], 8, str(row['id']), 1, 0, 'C', True)
        pdf.cell(widths[1], 8, str(row['loja']), 1, 0, 'L', True)
        pdf.cell(widths[2], 8, f"{row['valor']:,.2f}", 1, 0, 'R', True)
        pdf.cell(widths[3], 8, str(row['status']), 1, 0, 'C', True)
        pdf.cell(widths[4], 8, str(row['dias_parado']), 1, 0, 'C', True)
        pdf.cell(widths[5], 8, str(row['margem_risco']), 1, 1, 'C', True)

    # Salvamento (Sempre sobrescreve o arquivo atual)
    nome_pdf = "relatorio_final_completo.pdf"
    if os.path.exists(nome_pdf):
        try: os.remove(nome_pdf)
        except PermissionError: 
            print("Aviso: Feche o arquivo PDF antes de rodar o script.")
    
    pdf.output(nome_pdf)
    print("Sucesso! Relatórios PDF e JSON atualizados com êxito.")

if __name__ == "__main__":
    gerar_arquivos()