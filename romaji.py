def change_word(read_data):
    from pykakasi import kakasi
    kakasi = kakasi()

    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')
    conv = kakasi.getConverter()

    return conv.do(read_data)
