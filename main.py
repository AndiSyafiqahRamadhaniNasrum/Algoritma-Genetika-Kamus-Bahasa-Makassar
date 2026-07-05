from dataset import get_word_list
from kamus import tampilkan_kamus, menu_cari_kata
from utils import garis, judul, bulat, cetak_tabel_populasi
import genetic_algorithm as ga

TARGET = "MANGNGALLE"     
UKURAN_POPULASI = 6        
LAJU_MUTASI = 0.10         

hasil_ga = {
    "populasi_awal": None,
    "fitness_awal": None,
    "total_fitness": None,
    "probabilitas": None,
    "kumulatif": None,
    "proses_roulette": None,   
    "induk_terpilih": None,
    "proses_crossover": None,  
    "anak_sebelum_mutasi": None,
    "proses_mutasi": None,     
    "populasi_baru": None,
    "fitness_baru": None,
    "generasi": 0,
}

def jalankan_algoritma_genetika():
    judul(f"ALGORITMA GENETIKA - PENCARIAN KATA TARGET: '{TARGET}'")
    populasi = ga.bangkitkan_populasi_awal(get_word_list(), TARGET, UKURAN_POPULASI)
    hasil_ga["populasi_awal"] = populasi
    tampilkan_populasi(populasi, judul_tabel="POPULASI AWAL (Generasi ke-0)")

    fitness_awal = ga.hitung_fitness_populasi(populasi, TARGET)
    hasil_ga["fitness_awal"] = fitness_awal
    tampilkan_fitness(populasi, fitness_awal, judul_tabel="HASIL FITNESS - GENERASI KE-0")

    total_fitness = ga.hitung_total_fitness(fitness_awal)
    hasil_ga["total_fitness"] = total_fitness

    probabilitas = ga.hitung_probabilitas(fitness_awal, total_fitness)
    kumulatif = ga.hitung_probabilitas_kumulatif(probabilitas)
    hasil_ga["probabilitas"] = probabilitas
    hasil_ga["kumulatif"] = kumulatif
    tampilkan_tabel_roulette(populasi, fitness_awal, probabilitas, kumulatif, total_fitness)

    induk_terpilih = []
    proses_roulette = []
    judul("PROSES SELEKSI ROULETTE WHEEL (PEMILIHAN INDUK)")
    for i in range(UKURAN_POPULASI):
        individu, r, index = ga.pilih_dengan_roulette(populasi, kumulatif)
        induk_terpilih.append(individu)
        proses_roulette.append((i + 1, r, index + 1, individu["gen"]))
        print(f"  Pemilihan ke-{i+1}: bilangan acak r = {bulat(r)}  ->  "
              f"terpilih individu ke-{index+1} (gen = {individu['gen']})")
    hasil_ga["induk_terpilih"] = induk_terpilih
    hasil_ga["proses_roulette"] = proses_roulette

    judul("PROSES CROSSOVER (ONE POINT CROSSOVER)")
    anak_sebelum_mutasi = []
    proses_crossover = []
    for i in range(0, UKURAN_POPULASI, 2):
        parent1 = induk_terpilih[i]
        parent2 = induk_terpilih[i + 1]
        child1, child2, titik = ga.crossover_satu_titik(parent1["gen"], parent2["gen"])

        print(f"\n  Pasangan {i//2 + 1}:")
        print(f"    Parent 1        : {parent1['gen']}  (asal: {parent1['asal']})")
        print(f"    Parent 2        : {parent2['gen']}  (asal: {parent2['asal']})")
        print(f"    Titik Crossover : posisi ke-{titik}")
        print(f"    Child 1         : {child1}")
        print(f"    Child 2         : {child2}")

        anak_sebelum_mutasi.append(child1)
        anak_sebelum_mutasi.append(child2)
        proses_crossover.append({
            "parent1": parent1["gen"], "parent2": parent2["gen"],
            "titik": titik, "child1": child1, "child2": child2
        })
    hasil_ga["anak_sebelum_mutasi"] = anak_sebelum_mutasi
    hasil_ga["proses_crossover"] = proses_crossover

    judul("PROSES MUTASI (RANDOM MUTATION)")
    anak_setelah_mutasi = []
    proses_mutasi = []
    for i, anak in enumerate(anak_sebelum_mutasi, start=1):
        gen_baru, catatan = ga.mutasi(anak, LAJU_MUTASI)
        anak_setelah_mutasi.append(gen_baru)
        proses_mutasi.append((i, anak, gen_baru, catatan))

        print(f"\n  Individu anak ke-{i}:")
        print(f"    Sebelum mutasi : {anak}")
        if catatan:
            for posisi, lama, baru in catatan:
                print(f"    -> Mutasi pada posisi {posisi}: '{lama}' menjadi '{baru}'")
        else:
            print("    -> Tidak terjadi mutasi pada individu ini")
        print(f"    Sesudah mutasi : {gen_baru}")
    hasil_ga["proses_mutasi"] = proses_mutasi

    populasi_baru = [{"asal": "Hasil Crossover & Mutasi", "gen": gen} for gen in anak_setelah_mutasi]
    fitness_baru = ga.hitung_fitness_populasi(populasi_baru, TARGET)
    hasil_ga["populasi_baru"] = populasi_baru
    hasil_ga["fitness_baru"] = fitness_baru
    hasil_ga["generasi"] = hasil_ga["generasi"] + 1

    tampilkan_populasi(populasi_baru, judul_tabel=f"POPULASI BARU (Generasi ke-{hasil_ga['generasi']})")
    tampilkan_fitness(populasi_baru, fitness_baru, judul_tabel=f"HASIL FITNESS - GENERASI KE-{hasil_ga['generasi']}")

    fitness_terbaik = max(fitness_baru)
    individu_terbaik = populasi_baru[fitness_baru.index(fitness_terbaik)]
    judul("RINGKASAN HASIL GENERASI BARU")
    print(f"  Target                 : {TARGET}")
    print(f"  Individu terbaik       : {individu_terbaik['gen']}")
    print(f"  Fitness terbaik        : {bulat(fitness_terbaik)}")
    if individu_terbaik["gen"] == TARGET:
        print("  Status                 : TARGET DITEMUKAN! \U0001F389")
    else:
        print("  Status                 : Target belum ditemukan, perlu generasi berikutnya.")
    print()

def tampilkan_populasi(populasi, judul_tabel="POPULASI"):
    judul(judul_tabel)
    print(f"{'No':<4}{'Asal Kata':<25}{'Gen (dinormalisasi)':<22}")
    garis(55)
    for i, individu in enumerate(populasi, start=1):
        print(f"{i:<4}{individu['asal']:<25}{individu['gen']:<22}")
    garis(55)

def tampilkan_fitness(populasi, fitness_list, judul_tabel="HASIL FITNESS"):
    judul(judul_tabel)
    print(f"{'No':<4}{'Gen':<15}{'Target':<15}{'Fitness':<10}")
    garis(45)
    for i, (individu, fit) in enumerate(zip(populasi, fitness_list), start=1):
        print(f"{i:<4}{individu['gen']:<15}{TARGET:<15}{bulat(fit):<10}")
    garis(45)
    print(f"Total Fitness : {bulat(sum(fitness_list))}")

def tampilkan_tabel_roulette(populasi, fitness_list, probabilitas, kumulatif, total_fitness):
    judul("TABEL SELEKSI ROULETTE WHEEL")
    print(f"Total Fitness Populasi : {bulat(total_fitness)}\n")
    print(f"{'No':<4}{'Gen':<15}{'Fitness':<10}{'Probabilitas':<15}{'Prob. Kumulatif':<18}")
    garis(62)
    for i, (individu, fit, p, k) in enumerate(zip(populasi, fitness_list, probabilitas, kumulatif), start=1):
        print(f"{i:<4}{individu['gen']:<15}{bulat(fit):<10}{bulat(p):<15}{bulat(k):<18}")
    garis(62)

def menu_tampilkan_populasi():
    if hasil_ga["populasi_awal"] is None:
        print("\n[!] Jalankan menu 3 (Jalankan Algoritma Genetika) terlebih dahulu.\n")
        return
    tampilkan_populasi(hasil_ga["populasi_awal"], "POPULASI AWAL (Generasi ke-0)")
    tampilkan_populasi(hasil_ga["populasi_baru"], f"POPULASI BARU (Generasi ke-{hasil_ga['generasi']})")

def menu_hasil_fitness():
    if hasil_ga["fitness_awal"] is None:
        print("\n[!] Jalankan menu 3 (Jalankan Algoritma Genetika) terlebih dahulu.\n")
        return
    tampilkan_fitness(hasil_ga["populasi_awal"], hasil_ga["fitness_awal"], "HASIL FITNESS - GENERASI KE-0")
    tampilkan_fitness(hasil_ga["populasi_baru"], hasil_ga["fitness_baru"],
                       f"HASIL FITNESS - GENERASI KE-{hasil_ga['generasi']}")

def menu_seleksi_roulette():
    if hasil_ga["probabilitas"] is None:
        print("\n[!] Jalankan menu 3 (Jalankan Algoritma Genetika) terlebih dahulu.\n")
        return
    tampilkan_tabel_roulette(hasil_ga["populasi_awal"], hasil_ga["fitness_awal"],
                              hasil_ga["probabilitas"], hasil_ga["kumulatif"], hasil_ga["total_fitness"])
    judul("LOG PEMILIHAN INDUK (ROULETTE WHEEL)")
    for ke, r, index, gen in hasil_ga["proses_roulette"]:
        print(f"  Pemilihan ke-{ke}: r = {bulat(r)} -> individu ke-{index} (gen = {gen})")

def menu_crossover():
    if hasil_ga["proses_crossover"] is None:
        print("\n[!] Jalankan menu 3 (Jalankan Algoritma Genetika) terlebih dahulu.\n")
        return
    judul("LOG PROSES CROSSOVER")
    for i, log in enumerate(hasil_ga["proses_crossover"], start=1):
        print(f"\n  Pasangan {i}:")
        print(f"    Parent 1        : {log['parent1']}")
        print(f"    Parent 2        : {log['parent2']}")
        print(f"    Titik Crossover : posisi ke-{log['titik']}")
        print(f"    Child 1         : {log['child1']}")
        print(f"    Child 2         : {log['child2']}")

def menu_mutasi():
    if hasil_ga["proses_mutasi"] is None:
        print("\n[!] Jalankan menu 3 (Jalankan Algoritma Genetika) terlebih dahulu.\n")
        return
    judul("LOG PROSES MUTASI")
    for i, sebelum, sesudah, catatan in hasil_ga["proses_mutasi"]:
        print(f"\n  Individu anak ke-{i}:")
        print(f"    Sebelum mutasi : {sebelum}")
        if catatan:
            for posisi, lama, baru in catatan:
                print(f"    -> Mutasi posisi {posisi}: '{lama}' -> '{baru}'")
        else:
            print("    -> Tidak ada mutasi")
        print(f"    Sesudah mutasi : {sesudah}")

def menu_generasi_baru():
    if hasil_ga["populasi_baru"] is None:
        print("\n[!] Jalankan menu 3 (Jalankan Algoritma Genetika) terlebih dahulu.\n")
        return
    tampilkan_populasi(hasil_ga["populasi_baru"], f"POPULASI BARU (Generasi ke-{hasil_ga['generasi']})")
    tampilkan_fitness(hasil_ga["populasi_baru"], hasil_ga["fitness_baru"],
                       f"HASIL FITNESS - GENERASI KE-{hasil_ga['generasi']}")

def tampilkan_menu():
    print("\n=== KAMUS BAHASA DAERAH (BASA MANGKASARA') ===")
    print("1. Tampilkan Kamus")
    print("2. Cari Kata")
    print("3. Jalankan Algoritma Genetika")
    print("4. Tampilkan Populasi")
    print("5. Hasil Fitness")
    print("6. Seleksi Roulette")
    print("7. Cross Over")
    print("8. Mutasi")
    print("9. Generasi Baru")
    print("10. Keluar")

def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-10): ").strip()

        if pilihan == "1":
            tampilkan_kamus()
        elif pilihan == "2":
            menu_cari_kata()
        elif pilihan == "3":
            jalankan_algoritma_genetika()
        elif pilihan == "4":
            menu_tampilkan_populasi()
        elif pilihan == "5":
            menu_hasil_fitness()
        elif pilihan == "6":
            menu_seleksi_roulette()
        elif pilihan == "7":
            menu_crossover()
        elif pilihan == "8":
            menu_mutasi()
        elif pilihan == "9":
            menu_generasi_baru()
        elif pilihan == "10":
            print("\nTerima kasih. Program selesai.\n")
            break
        else:
            print("\n[!] Pilihan tidak valid, silakan pilih 1-10.\n")

if __name__ == "__main__":
    main()