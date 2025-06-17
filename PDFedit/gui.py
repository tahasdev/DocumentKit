import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pdf_ops 

class PdfEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Düzenleyici")
        self.geometry("550x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self)
        self.tab_silme = ttk.Frame(self.tabControl)
        self.tab_ekleme = ttk.Frame(self.tabControl)
        self.tab_degistirme = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_silme, text='SİLME')
        self.tabControl.add(self.tab_ekleme, text='EKLEME')
        self.tabControl.add(self.tab_degistirme, text='DEĞİŞTİRME')
        self.tabControl.pack(expand=1, fill="both")

        self.silme_pdf_path = tk.StringVar()
        self.ekleme_kaynak_pdf_path = tk.StringVar()
        self.ekleme_hedef_pdf_path = tk.StringVar()
        self.degistirme_kaynak_pdf_path = tk.StringVar()
        self.degistirme_hedef_pdf_path = tk.StringVar()

        self.setup_silme_tab()
        self.setup_ekleme_tab()
        self.setup_degistirme_tab()

    def dosya_sec(self, path_var):
        path = filedialog.askopenfilename(title="PDF Dosyası Seç", filetypes=[("PDF Files", "*.pdf")])
        if path:
            path_var.set(path)

    def sayfa_araligi_olustur(self, parent):
        frame = tk.Frame(parent)
        tk.Label(frame, text="Başlangıç (1-based):").grid(row=0, column=0)
        bas = tk.Entry(frame, width=5)
        bas.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Bitiş (1-based):").grid(row=0, column=2)
        bit = tk.Entry(frame, width=5)
        bit.grid(row=0, column=3, padx=5)
        return bas, bit, frame

    def setup_silme_tab(self):
        f = self.tab_silme
        tk.Label(f, text="Silinecek PDF Dosyasını Seç").pack(pady=5)
        tk.Entry(f, textvariable=self.silme_pdf_path, width=50, state='readonly').pack(padx=5)
        tk.Button(f, text="Dosya Seç", command=lambda: self.dosya_sec(self.silme_pdf_path)).pack(pady=5)
        self.sil_bas, self.sil_bit, aralik_frame = self.sayfa_araligi_olustur(f)
        aralik_frame.pack(pady=5)
        tk.Button(f, text="Sayfaları Sil ve Kaydet", command=self.silme_islemi).pack(pady=10)

    def setup_ekleme_tab(self):
        f = self.tab_ekleme
        tk.Label(f, text="Kaynak PDF (Eklenecek Sayfalar)").pack(pady=5)
        tk.Entry(f, textvariable=self.ekleme_kaynak_pdf_path, width=50, state='readonly').pack(padx=5)
        tk.Button(f, text="Dosya Seç", command=lambda: self.dosya_sec(self.ekleme_kaynak_pdf_path)).pack(pady=5)
        tk.Label(f, text="Hedef PDF (Sayfaların Ekleneceği PDF)").pack(pady=5)
        tk.Entry(f, textvariable=self.ekleme_hedef_pdf_path, width=50, state='readonly').pack(padx=5)
        tk.Button(f, text="Dosya Seç", command=lambda: self.dosya_sec(self.ekleme_hedef_pdf_path)).pack(pady=5)
        self.ekle_bas, self.ekle_bit, aralik_frame = self.sayfa_araligi_olustur(f)
        aralik_frame.pack(pady=5)
        tk.Label(f, text="Eklenecek Sayfaların Hedef PDF'de Başlayacağı Sayfa (1-based):").pack()
        self.ekle_hedef_bas = tk.Entry(f, width=5)
        self.ekle_hedef_bas.pack(pady=5)
        tk.Button(f, text="Sayfaları Ekle ve Kaydet", command=self.ekleme_islemi).pack(pady=10)

    def setup_degistirme_tab(self):
        f = self.tab_degistirme
        tk.Label(f, text="Kaynak PDF (Değiştirilecek Sayfalar)").pack(pady=5)
        tk.Entry(f, textvariable=self.degistirme_kaynak_pdf_path, width=50, state='readonly').pack(padx=5)
        tk.Button(f, text="Dosya Seç", command=lambda: self.dosya_sec(self.degistirme_kaynak_pdf_path)).pack(pady=5)
        tk.Label(f, text="Hedef PDF (Değiştirilmek İstenen PDF)").pack(pady=5)
        tk.Entry(f, textvariable=self.degistirme_hedef_pdf_path, width=50, state='readonly').pack(padx=5)
        tk.Button(f, text="Dosya Seç", command=lambda: self.dosya_sec(self.degistirme_hedef_pdf_path)).pack(pady=5)
        tk.Label(f, text="Kaynak PDF Sayfa Aralığı").pack(pady=2)
        self.degistirme_kaynak_bas, self.degistirme_kaynak_bit, f1 = self.sayfa_araligi_olustur(f)
        f1.pack(pady=2)
        tk.Label(f, text="Hedef PDF Sayfa Aralığı").pack(pady=2)
        self.degistirme_hedef_bas, self.degistirme_hedef_bit, f2 = self.sayfa_araligi_olustur(f)
        f2.pack(pady=2)
        tk.Button(f, text="Sayfaları Değiştir ve Kaydet", command=self.degistirme_islemi).pack(pady=10)

    def silme_islemi(self):
        try:
            bas = int(self.sil_bas.get())
            bit = int(self.sil_bit.get())
            if not self.silme_pdf_path.get():
                raise ValueError("PDF dosyası seçilmedi.")
            kayit_yolu = filedialog.asksaveasfilename(title="Sonuç PDF'i Kaydet", defaultextension=".pdf",
                                                      filetypes=[("PDF Files", "*.pdf")])
            if not kayit_yolu:
                return
            pdf_ops.sil_sayfalar(self.silme_pdf_path.get(), bas, bit, kayit_yolu)
            messagebox.showinfo("Başarılı", "Sayfalar silindi ve yeni dosya kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def ekleme_islemi(self):
        try:
            k_bas = int(self.ekle_bas.get())
            k_bit = int(self.ekle_bit.get())
            h_bas = int(self.ekle_hedef_bas.get())
            if not self.ekleme_kaynak_pdf_path.get() or not self.ekleme_hedef_pdf_path.get():
                raise ValueError("Her iki PDF dosyası da seçilmeli.")
            kayit_yolu = filedialog.asksaveasfilename(title="Sonuç PDF'i Kaydet", defaultextension=".pdf",
                                                      filetypes=[("PDF Files", "*.pdf")])
            if not kayit_yolu:
                return
            pdf_ops.ekle_sayfalar(self.ekleme_kaynak_pdf_path.get(), self.ekleme_hedef_pdf_path.get(), k_bas, k_bit, h_bas, kayit_yolu)
            messagebox.showinfo("Başarılı", "Sayfalar eklendi ve yeni dosya kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def degistirme_islemi(self):
        try:
            k_bas = int(self.degistirme_kaynak_bas.get())
            k_bit = int(self.degistirme_kaynak_bit.get())
            h_bas = int(self.degistirme_hedef_bas.get())
            h_bit = int(self.degistirme_hedef_bit.get())
            if not self.degistirme_kaynak_pdf_path.get() or not self.degistirme_hedef_pdf_path.get():
                raise ValueError("Her iki PDF dosyası da seçilmeli.")
            kayit_yolu = filedialog.asksaveasfilename(title="Sonuç PDF'i Kaydet", defaultextension=".pdf",
                                                      filetypes=[("PDF Files", "*.pdf")])
            if not kayit_yolu:
                return
            pdf_ops.degistir_sayfalar(self.degistirme_kaynak_pdf_path.get(), self.degistirme_hedef_pdf_path.get(),
                                      k_bas, k_bit, h_bas, h_bit, kayit_yolu)
            messagebox.showinfo("Başarılı", "Sayfalar değiştirildi ve yeni dosya kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    app = PdfEditorApp()
    app.mainloop()
