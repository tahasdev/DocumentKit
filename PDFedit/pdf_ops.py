from PyPDF2 import PdfReader, PdfWriter # pip install PyPDF2

def sil_sayfalar(pdf_path, bas, bit, cikti_yolu):
    reader = PdfReader(pdf_path)
    toplam = len(reader.pages)
    if bas < 1 or bit > toplam or bas > bit:
        raise ValueError(f"Sayfa aralığı 1 ile {toplam} arasında olmalıdır.")
    writer = PdfWriter()
    for i in range(toplam):
        if i+1 < bas or i+1 > bit:
            writer.add_page(reader.pages[i])
    with open(cikti_yolu, "wb") as f:
        writer.write(f)

def ekle_sayfalar(kaynak_path, hedef_path, k_bas, k_bit, h_bas, cikti_yolu):
    k_reader = PdfReader(kaynak_path)
    h_reader = PdfReader(hedef_path)
    if k_bas < 1 or k_bit > len(k_reader.pages) or k_bas > k_bit:
        raise ValueError("Kaynak sayfa aralığı geçersiz.")
    if h_bas < 1 or h_bas > len(h_reader.pages) + 1:
        raise ValueError("Hedef başlangıç sayfası geçersiz.")
    writer = PdfWriter()
    for i in range(h_bas - 1):
        writer.add_page(h_reader.pages[i])
    for i in range(k_bas - 1, k_bit):
        writer.add_page(k_reader.pages[i])
    for i in range(h_bas - 1, len(h_reader.pages)):
        writer.add_page(h_reader.pages[i])
    with open(cikti_yolu, "wb") as f:
        writer.write(f)

def degistir_sayfalar(kaynak_path, hedef_path, k_bas, k_bit, h_bas, h_bit, cikti_yolu):
    k_reader = PdfReader(kaynak_path)
    h_reader = PdfReader(hedef_path)
    if k_bas < 1 or k_bit > len(k_reader.pages) or k_bas > k_bit:
        raise ValueError("Kaynak sayfa aralığı geçersiz.")
    if h_bas < 1 or h_bit > len(h_reader.pages) or h_bas > h_bit:
        raise ValueError("Hedef sayfa aralığı geçersiz.")
    if (h_bit - h_bas) != (k_bit - k_bas):
        raise ValueError("Kaynak ve hedef aralık uzunlukları eşit olmalıdır.")
    writer = PdfWriter()
    for i in range(h_bas - 1):
        writer.add_page(h_reader.pages[i])
    for i in range(k_bas - 1, k_bit):
        writer.add_page(k_reader.pages[i])
    for i in range(h_bit, len(h_reader.pages)):
        writer.add_page(h_reader.pages[i])
    with open(cikti_yolu, "wb") as f:
        writer.write(f)
