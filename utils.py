
def garis(panjang=60, karakter="-"):
    """Mencetak garis pemisah agar output terminal lebih rapi."""
    print(karakter * panjang)

def judul(teks):
    """Mencetak judul tahapan dengan format seragam."""
    print("\n" + "=" * 60)
    print(teks)
    print("=" * 60)

def bulat(nilai, digit=4):
    """Membulatkan nilai float agar tabel di terminal lebih rapi."""
    return round(nilai, digit)

def cetak_tabel_populasi(populasi, header="Individu"):
    """Mencetak daftar populasi (list of string) dengan nomor urut."""
    for i, individu in enumerate(populasi, start=1):
        print(f"  {i}. {header} = {individu}")