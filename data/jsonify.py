from copy import deepcopy
import json
import os
import shutil

# Constants

DB = 'db.txt'
IDENTIFIERS_DB = 'identifiers.json'
INDEX_DB = 'index.json'
METADATA_DB = 'metadata.json'


# Functions


def ToAscii85(number: int) -> str:
    table = {
        0: '0',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F',
        16: 'G',
        17: 'H',
        18: 'I',
        19: 'J',
        20: 'K',
        21: 'L',
        22: 'M',
        23: 'N',
        24: 'O',
        25: 'P',
        26: 'Q',
        27: 'R',
        28: 'S',
        29: 'T',
        30: 'U',
        31: 'V',
        32: 'W',
        33: 'X',
        34: 'Y',
        35: 'Z',
        36: 'a',
        37: 'b',
        38: 'c',
        39: 'd',
        40: 'e',
        41: 'f',
        42: 'g',
        43: 'h',
        44: 'i',
        45: 'j',
        46: 'k',
        47: 'l',
        48: 'm',
        49: 'n',
        50: 'o',
        51: 'p',
        52: 'q',
        53: 'r',
        54: 's',
        55: 't',
        56: 'u',
        57: 'v',
        58: 'w',
        59: 'x',
        60: 'y',
        61: 'z',
        62: '!',
        63: '#',
        64: '$',
        65: '%',
        66: '&',
        67: '(',
        68: ')',
        69: '*',
        70: '+',
        71: '-',
        72: ';',
        73: '<',
        74: '=',
        75: '>',
        76: '?',
        77: '@',
        78: '^',
        79: '_',
        80: '`',
        81: '{',
        82: '|',
        83: '}',
        84: '~',
    }
    return ToBase(number, 85, table)


def ToBase(number: int, base: int, table: dict) -> str:
    if number < base:
        return table[number]

    result = ''
    while True:
        division = int(number / base)
        remainder = number % base
        number = division
        result = table[remainder] + result
        if division == 0:
            break
    return result


# Make identifiers JSON db


def make_identifiers():
    count = 0
    identifiers = {}

    with open(DB, 'r') as reader:
        for line in reader:
            identifier = line.split(' ')[0].strip()
            if identifier in identifiers:
                continue
            count += 1
            hashvalue = ToAscii85(count)
            identifiers[identifier] = hashvalue
            identifiers[ToAscii85(count)] = identifier

    with open(IDENTIFIERS_DB, 'w') as writer:
        writer.write(json.dumps(identifiers))


# Replace indentifier URLs with identifiers


def replace_identifiers():
    with open(IDENTIFIERS_DB, 'r') as reader:
        identifiers = json.loads(reader.read())

    with open(DB, 'r') as reader, open('tmp.txt', 'w') as writer:
        for line in reader:
            line = line.strip()
            identifier = line.split(' ')[0].strip()
            line = line.replace(identifier, identifiers[identifier])
            writer.write(line + '\n')
    shutil.copy(DB, 'original_db.txt')
    os.remove(DB)
    os.rename('tmp.txt', DB)


# Make index JSON db


def make_index():
    index = {}
    with open(DB, 'r') as reader:
        for line in reader:
            for label in ['W', 'D']:
                label = 'tdn:' + label
                if label not in line:
                    continue
                identifier = line.partition(label)[0].strip()
                index_term = line.partition(label)[2].strip()
                # conversion to string to get strings in JSON keys!
                index_term = str(index_term)
                if index_term == '':
                    continue
                if index_term not in index:
                    index[index_term] = []
                index[index_term].append(identifier)

    for word, values in index.items():
        index[word] = list(set(values))

    with open(INDEX_DB, 'w') as writer:
        writer.write(json.dumps(index))


# Make metadata JSON db


def make_metadata():
    metadata = {}
    with open(DB, 'r') as reader:
        for line in reader:
            if 'tdn:W' in line:
                continue
            for label in [
                'L',
                'S',
                'M',
                'A',
                'P',
                'D',
                'F',
                'C',
                'X',
                'Y',
                'y',
                'Z',
                'z',
            ]:
                key = 'tdn:' + label
                if key in line:
                    identifier = line.partition(key)[0].strip()
                    if identifier not in metadata:
                        metadata[identifier] = {}
                    data = line.partition(key)[2].strip()
                    if data == '':
                        continue
                    metadata[identifier][key.strip('tdn:')] = data
    with open(METADATA_DB, 'w') as writer:
        writer.write(json.dumps(metadata))


# Remove identifiers from identifiers db
# (only hashes are necessary for index.js!)


def remove_identifiers():
    with open(IDENTIFIERS_DB, 'r') as reader:
        identifiers = json.loads(reader.read())
        new_identifiers = deepcopy(identifiers)
        for item in identifiers:
            if item.startswith('http') and '://' in item:
                del new_identifiers[item]
    with open(IDENTIFIERS_DB, 'w') as writer:
        writer.write(json.dumps(new_identifiers))


if __name__ == '__main__':
    make_identifiers()
    replace_identifiers()
    make_index()
    make_metadata()
    remove_identifiers()
