import random
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FILLER = "_"

def normalisasi_kata(kata, panjang_target):
    kata = kata.upper()
    if len(kata) >= panjang_target:
        return kata[:panjang_target]
    return kata + FILLER * (panjang_target - len(kata))

def bangkitkan_populasi_awal(daftar_kata, target, ukuran_populasi):
    panjang_target = len(target)

    if ukuran_populasi <= len(daftar_kata):
        kata_terpilih = random.sample(daftar_kata, ukuran_populasi)
    else:
        kata_terpilih = random.choices(daftar_kata, k=ukuran_populasi)

    populasi = []
    for kata in kata_terpilih:
        populasi.append({
            "asal": kata,
            "gen": normalisasi_kata(kata, panjang_target)
        })
    return populasi

def hitung_fitness(gen, target):
    target = target.upper()
    jumlah_benar = sum(1 for a, b in zip(gen, target) if a == b)
    return jumlah_benar / len(target)

def hitung_fitness_populasi(populasi, target):
    return [hitung_fitness(individu["gen"], target) for individu in populasi]

def hitung_total_fitness(daftar_fitness):
    return sum(daftar_fitness)

def hitung_probabilitas(daftar_fitness, total_fitness):
    if total_fitness == 0:
        n = len(daftar_fitness)
        return [1 / n for _ in daftar_fitness]
    return [f / total_fitness for f in daftar_fitness]

def hitung_probabilitas_kumulatif(daftar_probabilitas):
    kumulatif = []
    total = 0
    for p in daftar_probabilitas:
        total += p
        kumulatif.append(total)
    return kumulatif

def pilih_dengan_roulette(populasi, probabilitas_kumulatif):
    r = random.random()
    for index, batas_atas in enumerate(probabilitas_kumulatif):
        if r <= batas_atas:
            return populasi[index], r, index
    return populasi[-1], r, len(populasi) - 1

def crossover_satu_titik(gen_parent1, gen_parent2):
    panjang = len(gen_parent1)
    titik_potong = random.randint(1, panjang - 1)

    child1 = gen_parent1[:titik_potong] + gen_parent2[titik_potong:]
    child2 = gen_parent2[:titik_potong] + gen_parent1[titik_potong:]

    return child1, child2, titik_potong

def mutasi(gen, laju_mutasi=0.1):
    gen_list = list(gen)
    catatan_mutasi = []
    for posisi in range(len(gen_list)):
        if random.random() < laju_mutasi:
            gen_lama = gen_list[posisi]
            gen_baru = random.choice(ALPHABET)
            while gen_baru == gen_lama:
                gen_baru = random.choice(ALPHABET)
            gen_list[posisi] = gen_baru
            catatan_mutasi.append((posisi, gen_lama, gen_baru))
    return "".join(gen_list), catatan_mutasi