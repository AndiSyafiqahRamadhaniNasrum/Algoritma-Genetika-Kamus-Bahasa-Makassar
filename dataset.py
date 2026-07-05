KAMUS_MAKASSAR = [
    ("mangngalle",     "mengambil"),
    ("akkalimbuang",   "mengelilingi"),
    ("appilajara",     "belajar"),
    ("akkaraeng",      "menjadi raja"),
    ("tumakkaraeng",   "kaum bangsawan"),
    ("pakkio",         "panggilan"),
    ("passampeang",    "kesempatan"),
    ("gassingang",     "kekuatan"),
    ("kalumannyang",   "kekayaan"),
    ("ammoterang",     "pulang"),
    ("ammempo",        "duduk"),
    ("akkelong",       "bernyanyi"),
    ("akjeknek",       "mandi"),
    ("akkarena",       "bermain"),
    ("accini",         "melihat"),
    ("allangngere",    "mendengar"),
    ("akkana",         "berbicara"),
    ("attunrung",      "memukul"),
    ("akkio",          "memanggil"),
    ("anrong",         "ibu"),
    ("burane",         "laki-laki"),
    ("balla",          "rumah"),
    ("jenne",          "air"),
    ("kanre",          "nasi / makan"),
    ("inung",          "minum"),
    ("battu",          "datang"),
    ("lampa",          "pergi"),
    ("tinro",          "tidur"),
    ("bangung",        "bangun"),
    ("gassing",        "kuat"),
    ("lammoro",        "lembut"),
    ("lompo",          "besar"),
    ("cakdi",          "kecil"),
    ("sanging",        "selalu"),
    ("sikola",         "sekolah"),
    ("gurutta",        "guru kita"),
    ("karaeng",        "raja / bangsawan"),
    ("parasangang",    "kampung / negeri"),
    ("sallo",          "lama"),
    ("sannaq",         "sangat"),
    ("doeq",           "uang"),
    ("barang",         "barang"),
    ("sallang",        "nanti / kelak"),
    ("lopi",           "perahu"),
    ("kasiasi",        "miskin / kasihan"),
    ("ajjappa",        "berjalan"),
    ("accera",         "berkurban"),
    ("attoana",        "bertani"),
    ("akbayao",        "bertelur"),
    ("akkanre",        "makan"),
    ("accalla",        "berteriak"),
]


def get_dataset():
    """Mengembalikan seluruh isi kamus dalam bentuk list of tuple (kata, arti)."""
    return KAMUS_MAKASSAR


def get_word_list():
    """Mengembalikan hanya daftar kata (tanpa arti), digunakan untuk populasi GA."""
    return [pasangan[0] for pasangan in KAMUS_MAKASSAR]
