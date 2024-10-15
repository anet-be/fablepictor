from anet.core.base import yieldcsv

DATA_FILE = 'data.csv'

PUNCTUATION = {
    '!',
    '"',
    '#',
    '$',
    '%',
    '&',
    "'",
    '(',
    ')',
    '*',
    '+',
    ',',
    '-',
    '§',
    '.',
    '/',
    ':',
    ';',
    '<',
    '=',
    '>',
    '?',
    '@',
    '[',
    '\\',
    ']',
    '^',
    '_',
    '`',
    '{',
    '|',
    '}',
    '~',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
}

ANIMAL_TABLE = {
    'aap': 'monkey',
    'ezel': 'donkey',
    'kip': 'chicken',
    'slang': 'snake',
    'vos': 'fox',
    'pauw': 'peacock',
    'beer': 'bear',
    'geit': 'goat',
    'hond': 'dog',
    'kat': 'cat',
    'kikker': 'frog',
    'koe': 'cow',
    'konijn': 'rabbit',
    'leeuw': 'lion',
    'olifant': 'elephant',
    'paard': 'horse',
    'rat': 'rat',
    'schaap': 'sheep',
    'wolf': 'wolf',
    'zwijn': 'pig',
}


def split_to_index_words(data: str) -> list:
    if not data:
        return []
    result: list[str] = []
    for word in data.split(' '):
        word = word.strip().lower()
        for char in PUNCTUATION:
            word = word.replace(char, '', -1)
        if len(word) > 1:
            result.append(word)
    return result


for row in yieldcsv(DATA_FILE, delimiter=';'):

    # Gather data
    identifier = row['IIIF_Prent']
    if identifier in ['', ' ']:
        continue

    labels = []

    part = row['Onderdeel_EN']
    part_aat = row['Onderdeel_AAT']
    fable = row['Titel_Fabel']
    cloi = row['c:loi']
    oloi = row['o:loi']
    objecttype = row['Objecttype_EN']
    objecttype_aat = row['Objecttype_AAT']
    manifest = row['Manifest']
    summary = row['Korte_titel']
    page = row['Pagina']

    labels.append(summary)
    labels.append(fable)

    place1 = ''
    date1 = ''
    for number in [1, 2]:
        place = row[f'Impr{number}_Plaats']
        if number == 1:
            place1 = place
        labels.append(place)
        date = row[f'Impr{number}_Jaar']
        if number == 1:
            date1 = date
        labels.append(date)

    impressums = []
    for number in [1, 2]:
        impressum = row[f'Impr{number}_Presentatieweergave']
        if impressum:
            impressums.append(impressum)

    animals = []
    for animal in row['Dieren'].split(','):
        animal = animal.lower().strip()
        animal_code = ANIMAL_TABLE.get(animal)
        labels.append(animal)
        if animal_code:
            animals.append(animal_code)
            labels.append(animal_code)

    permalink = row['PermalinkAnet_Titel']
    if permalink.endswith('/N'):
        permalink = permalink[:-2] + '/E'

    authors_presentation, artists_presentation = ([], [])
    for key in row.keys():
        if key.startswith('Kunstenaar') or key.startswith('Auteur'):
            data = row[key].strip()
            if data:
                labels.append(data)
                if 'Presentatieweergave' in key:
                    if key.startswith('Kunstenaar'):
                        artists_presentation.append(data)
                    else:
                        authors_presentation.append(data)

    # Export data
    for animal in animals:
        print(identifier, ' tdn:A ', animal)
    for label in labels:
        for word in split_to_index_words(label):
            print(identifier, ' tdn:W ', word)
    export = {
        ' tdn:k ': ', '.join(artists_presentation),
        ' tdn:a ': ', '.join(authors_presentation),
        ' tdn:i ': ', '.join(impressums),
        ' tdn:S ': summary,
        ' tdn:M ': manifest,
        ' tdn:P ': permalink,
        ' tdn:F ': fable,
        ' tdn:C ': cloi,
        ' tdn:O ': oloi,
        ' tdn:L ': place1,
        ' tdn:D ': date1,
        ' tdn:X ': page,
        ' tdn:Y ': part,
        ' tdn:y ': part_aat,
        ' tdn:Z ': objecttype,
        ' tdn:z ': objecttype_aat,
    }
    for predicate, data_object in export.items():
        if data_object:
            print(identifier, predicate, data_object)
