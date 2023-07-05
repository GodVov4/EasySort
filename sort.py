import re
import shutil
import sys
from pathlib import Path
from pyfiglet import Figlet


f = Figlet(font='standard')
user_path = Path(sys.argv[1])
NEW_FOLDERS = {
    'images': [],
    'video': [],
    'audio': [],
    'documents': [],
    'archives': []
}
EXTENSIONS = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG', 'HEIC', 'ICO'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV', 'GIF'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR', 'FLAC'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown': []
}
IGNORE_FOLDERS = {'archives', 'video', 'audio', 'documents', 'images'}
TRANSLIT = {
    1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
    1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'y', 1048: 'Y',
    1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
    1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
    1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH',
    1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
    1101: 'ye', 1069: 'YE', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i',
    1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
}


def normalize(path, translit):
    """
    Transliterate filename to english, remove problem symbols
    :param path: filename -> str
    :param translit: translit dict -> dict
    :return: normalized file -> str
    """
    file = path.name
    ext = file[file.rfind('.'):]
    normalized_file = file.removesuffix(ext)
    normalized_file = normalized_file.translate(translit)
    repl = re.findall(r'\W', normalized_file)
    for i in repl:
        normalized_file = normalized_file.replace(i, '_')
    normalized_file += ext
    new_path = path.parent / normalized_file
    if file != normalized_file:
        path.rename(new_path)
    return new_path


def sort_groups(path):
    """
    Unpack all folders in path and sort by extensions
    :param path: user path -> Path()
    :return: dict with new folders and files -> dict,
            list of known extensions -> list,
            list of unknown extensions -> list
    """
    known_list = set()
    unknown_list = set()
    for file in path.glob('**/*'):
        if file.is_file() and set(file.parts).isdisjoint(IGNORE_FOLDERS):
            ext = str(file)[str(file).rfind('.')+1:]
            for folder, ext_list in EXTENSIONS.items():
                if ext.upper() in ext_list:
                    NEW_FOLDERS[folder].append(normalize(file, TRANSLIT))
                    known_list.add(ext.upper())
                    break
                elif folder == 'unknown':
                    unknown_list.add(ext.upper())
                    break
    return NEW_FOLDERS, list(known_list), list(unknown_list)


def create_dirs(path, folders):  # Функція абсолют не працює, замінити
    for key, files in folders.items():
        new_folder = path / key
        if not new_folder.exists():
            new_folder.mkdir()
        for file in files:
            if key == 'archives':
                parent = file.parent
                file = parent / unpacker(file)
            new_file = new_folder / file.name
            suffix = 1
            while new_file.exists():
                text = file.name
                text += str(suffix)
                new_file = new_folder / text
                suffix += 1
            shutil.move(file, new_file)


def unpacker(archive):
    """
    Unpack archives
    :param archive: path of archive -> Path()
    :return: None
    """
    name = archive
    suffixes = len(name.suffixes)
    while suffixes:
        if Path(name).suffixes[-1][1:].upper() not in EXTENSIONS['archives']:
            break
        name = Path(name).stem
        suffixes = len(Path(name).suffixes)
    folder = archive.parent / name
    shutil.unpack_archive(archive, folder)
    return folder


def delete_empty(path):

    for item in path.glob('**/*'):
        if item.is_dir():
            try:
                item.rmdir()
            except OSError:
                pass


def readme(new_folders, known_list, unknown_list):
    path = Path(user_path) / 'Sort_result.txt'
    with open(path, 'w') as result:
        result.write(f.renderText('EasySort'))
        result.write('\nCongratulations! You used the EasySort Sorter. Here\'s a list of what\'s been done:\n\n')
        for key, value in new_folders.items():
            if len(value) == 0:
                result.write(f'- In folder "{key}" nothing was moved.\n')
            elif key != 'archives':
                result.write(f'- In folder "{key}" was moved: {[i.name for i in value]}.\n')
        for key, value in new_folders.items():
            if key == 'archives':
                result.write(f'- Your archives {[i.name for i in value]} was unpacked in folder "{key}".\n')
        result.write(f'\n- Known extensions: {known_list}.\n')
        result.write(f'\n- Unknown extensions: {unknown_list}.\n')
        result.write('\n- Your files have been transliterated.\n')
        result.write('\n\nProduced in Ukraine by Volodymyr Martyn.\n')


def main():
    new_folders, known_list, unknown_list = sort_groups(user_path)
    create_dirs(user_path, new_folders)
    delete_empty(user_path)
    readme(new_folders, known_list, unknown_list)


if __name__ == '__main__':
    main()
