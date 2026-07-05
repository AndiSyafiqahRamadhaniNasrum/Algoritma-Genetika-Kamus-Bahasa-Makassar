from dataset import get_dataset

def tampilkan_kamus():
    data = get_dataset()
    print("\n=== DAFTAR KAMUS BAHASA MAKASSAR ===")
    print(f"{'No':<4}{'Kata Makassar':<18}{'Arti':<20}{'Panjang':<8}")
    print("-" * 50)
    for i, (kata, arti) in enumerate(data, start=1):
        print(f"{i:<4}{kata:<18}{arti:<20}{len(kata):<8}")
    print("-" * 50)
    print(f"Total kata dalam kamus : {len(data)}\n")

def cari_kata(kata_dicari):
    data = get_dataset()
    kata_dicari = kata_dicari.strip().lower()
    for kata, arti in data:
        if kata.lower() == kata_dicari:
            return arti
    return None

def menu_cari_kata():
    kata = input("Masukkan kata yang ingin dicari: ")
    hasil = cari_kata(kata)
    if hasil:
        print(f"\nKata '{kata}' ditemukan! Arti: {hasil}\n")
    else:
        print(f"\nKata '{kata}' tidak ditemukan dalam kamus.\n")
