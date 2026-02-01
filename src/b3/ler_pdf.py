import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import sys

def pdf_para_txt(pdf_path, txt_path=None, idioma='por'):
    if txt_path is None:
        nome_base = os.path.splitext(pdf_path)[0]
        txt_path = f"{nome_base}.txt"
    
    print(f"🔄 Convertendo: {pdf_path}")
    print(f"💾 Salvando em: {txt_path}")
    
    try:
        print("📄 Convertendo PDF para imagens...")
        imagens = convert_from_path(pdf_path)
        
        texto_completo = []
        
        for i, imagem in enumerate(imagens, 1):
            print(f"📖 Processando página {i}/{len(imagens)}...")
            config = f'--oem 3 --psm 6 -l {idioma}'
            texto_pagina = pytesseract.image_to_string(imagem, config=config)
            texto_completo.append(f"\n--- PÁGINA {i} ---\n")
            texto_completo.append(texto_pagina)
            texto_completo.append("\n" + "="*50 + "\n")
        
        texto_final = "".join(texto_completo)
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(texto_final)
        
        print(f"✅ CONVERSÃO CONCLUÍDA!")
        print(f"📄 {len(imagens)} páginas processadas")
        print(f"💾 Arquivo salvo: {txt_path}")
        
        return texto_final
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return None

if __name__ == "__main__":
    # ← CAMINHO DO SEU PDF NA PASTA pdf/
    PDF_ARQUIVO = "pdf/BDI_00_20251015.pdf"  # MUDA AQUI!
    IDIOMA = "por"
    
    if not os.path.exists(PDF_ARQUIVO):
        print(f"❌ Arquivo '{PDF_ARQUIVO}' não encontrado!")
        print("💡 Coloque seu PDF na pasta ../pdf/")
        sys.exit(1)
    
    resultado = pdf_para_txt(PDF_ARQUIVO, idioma=IDIOMA)