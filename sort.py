import shutil
import sys
import re
from constants import NEW_FOLDERS, IGNORE_FOLDERS, EXTENSIONS
from transliterate import get_translit_function
from pyfiglet import Figlet
from pathlib import Path


f = Figlet(font='standard')
try:
    user_path = Path(sys.argv[1])
except IndexError:
    print('You did\'t specify a folder path.\nTry again.')
    exit()
if not user_path.exists():
    print('Invalid folder.\nTry again.')
    exit()


def normalize(path: Path) -> Path:
    """
    Transliterate filename to english, remove problem symbols
    """
    file = path.name
    ext = file[file.rfind('.'):]
    normalized_file = file.removesuffix(ext)
    if normalized_file[normalized_file.rfind('.')+1:].lower() == 'tar':
        ext = file[normalized_file.rfind('.'):]
        normalized_file = file.removesuffix(ext)
    normalized_file = re.sub(r'\W', '_', normalized_file)
    translit = get_translit_function('uk')
    normalized_file = translit(normalized_file, reversed=True)
    normalized_file += ext
    new_path = path.parent / normalized_file
    if file != normalized_file:
        path.rename(new_path)
    return new_path


def sort_groups(path: Path) -> tuple:
    """
    Unpack all folders in path and sort by extensions
    :return: new folders and files dict -> dict,
             known extensions list -> list,
             unknown extensions list -> list
    """
    known_list = set()
    unknown_list = set()
    for file in path.glob('**/*'):
        if file.is_dir() or not set(file.parts).isdisjoint(IGNORE_FOLDERS):
            continue
        ext = str(file)[str(file).rfind('.')+1:]
        for folder, ext_list in EXTENSIONS.items():
            if ext.upper() in ext_list:
                NEW_FOLDERS[folder].append(normalize(file))
                known_list.add(ext.upper())
                break
            elif folder == 'unknown':
                unknown_list.add(ext.upper())
                break
    return NEW_FOLDERS, list(known_list), list(unknown_list)


def create_dirs(path: Path, folders: dict) -> None:
    """
    Create folders and move files
    """
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
                text = 'copy_' + str(suffix) + '_' + text
                new_file = new_folder / text
                suffix += 1
            shutil.move(file, new_file)


def unpacker(archive: Path) -> Path:
    """
    Unpack archives
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


def delete_empty(path: Path) -> None:
    """
    Delete empty folders
    """
    for item in path.glob('**/*'):
        if item.is_dir():
            try:
                item.rmdir()
            except OSError:
                pass


def readme(new_folders: dict, known_list: list, unknown_list: list) -> None:
    """
    Create text file with results description
    """
    path = Path(user_path) / 'SORT_RESULT.txt'
    with open(path, 'w') as result:
        result.write(f.renderText('EasySort'))
        result.write('\nCongratulations! You used the EasySort Sorter. Here\'s a list of what\'s been done:\n\n')
        for key, value in new_folders.items():
            if not value:
                result.write(f'* In folder "{key}" nothing was moved.\n')
            elif key != 'archives':
                result.write(f'* In folder "{key}" was moved: {[i.name for i in value]}.\n')
        for key, value in new_folders.items():
            if key == 'archives':
                result.write(f'* Your archives {[i.name for i in value]} was unpacked in folder "{key}".\n\n')
        result.write(f'* Known extensions: {known_list}.\n')
        result.write(f'* Unknown extensions: {unknown_list}.\n')
        result.write('\n* Your files have been transliterated.\n')
        result.write('\n\nProduced in Ukraine by Volodymyr Martyn.\n')


def main():
    new_folders, known_list, unknown_list = sort_groups(user_path)
    create_dirs(user_path, new_folders)
    delete_empty(user_path)
    readme(new_folders, known_list, unknown_list)
    print('\nDone! Your files was sorted. Open "SORT_RESULT.txt" for see results.\n')


if __name__ == '__main__':
    main()
