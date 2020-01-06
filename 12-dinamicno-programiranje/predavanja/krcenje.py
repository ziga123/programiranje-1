import itertools
import png


def nalozi_sliko(ime_datoteke):
    reader = png.Reader(filename=ime_datoteke)
    sirina, visina, rows, _ = reader.asRGBA()
    piksli = [[None for _ in range(sirina)] for _ in range(visina)]
    for vrstica, row in enumerate(rows):
        for stolpec, (r, g, b) in enumerate(zip(row[::4], row[1::4], row[2::4])):
            piksli[vrstica][stolpec] = (r, g, b)
    return piksli


def shrani_sliko(slika, ime_datoteke):
    vrstice = [list(itertools.chain(*vrstica)) for vrstica in slika]
    with open(ime_datoteke, 'wb') as datoteka:
        png.Writer(len(slika[0]), len(slika),
                   greyscale=False).write(datoteka, vrstice)


def razdalja(piksel1, piksel2):
    r1, g1, b1 = piksel1
    r2, g2, b2 = piksel2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def energije_vrstice(vrstica):
    sirina = len(vrstica)
    energije = [0] * sirina
    for i in range(sirina - 1):
        r = razdalja(vrstica[i], vrstica[i + 1])
        energije[i] += r
        energije[i + 1] += r
    energije[0] *= 2
    energije[-1] *= 2
    return energije


def energije_slike(slika):
    return [energije_vrstice(vrstica) for vrstica in slika]

def dimenzije(slika):
    return len(slika), len(slika[0])

def siv_po_tockah(slika):
    energije = energije_slike(slika)
    siv = []
    for vrstica in energije:
        siv.append(vrstica.index(min(vrstica)))
    return siv

def navpicni_siv(slika):
    visina, sirina = dimenzije(slika)
    energije = energije_slike(slika)
    energije_stolpcev = [
        sum(energije[i][j] for i in range(visina))
        for j in range(sirina)
    ]
    min_stolpec = energije_stolpcev.index(min(energije_stolpcev))
    siv = [min_stolpec for _ in range(visina)]
    return siv

def zavijajoci_siv(slika):
    visina, sirina = dimenzije(slika)
    energije = energije_slike(slika)
    sivi = [[(energije[0][x], [x]) for x in range(sirina)]]
    for y in range(1, visina):
        sivi_vrstice = []
        for x in range(sirina):
            zacetki = []
            if x > 0:
                zacetki.append(sivi[-1][x - 1])
            zacetki.append(sivi[-1][x])
            if x < sirina - 1:
                zacetki.append(sivi[-1][x + 1])
            energija_zacetka, siv_zacetka = min(zacetki)
            sivi_vrstice.append((energije[y][x] + energija_zacetka, siv_zacetka + [x]))
        sivi.append(sivi_vrstice)
    return min(sivi[-1])[1]

def pokazi_siv(slika, siv):
    nova_slika = []
    for vrstica, i in zip(slika, siv):
        nova_vrstica = vrstica[:]
        nova_vrstica[i] = (255, 0, 0)
        nova_slika.append(nova_vrstica)
    return nova_slika


def odstrani_siv(slika, siv):
    nova_slika = []
    for vrstica, i in zip(slika, siv):
        nova_slika.append(vrstica[:i] + vrstica[i + 1:])
    return nova_slika


slika = nalozi_sliko('/workspaces/programiranje-1/12-dinamicno-programiranje/predavanja/kuza.png')
for i in range(len(slika[0])):
    print(i)
    siv = zavijajoci_siv(slika)
    shrani_sliko(pokazi_siv(slika, siv), f'korak-{i}.png')
    slika = odstrani_siv(slika, siv)
