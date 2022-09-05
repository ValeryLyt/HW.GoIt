import re
import sys
from shutil import unpack_archive
from pathlib import Path


IMAGES = []
VIDEO = []
DOCUMENTS = []
AUDIO = []
ARCHIVES = []
OTHERS = []
KNOWN_EXT = []
UNKNOWN_EXT = []
FOLDERS = []

IMAGES_EXT = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXT = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENTS_EXT = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO_EXT = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES_EXT = ('ZIP', 'GZ', 'TAR')

EXT = [IMAGES_EXT, VIDEO_EXT, DOCUMENTS_EXT, AUDIO_EXT, ARCHIVES_EXT]

REGISTER_EXTENSIONS = {
    IMAGES_EXT: IMAGES,
    VIDEO_EXT: VIDEO,
    DOCUMENTS_EXT: DOCUMENTS,
    AUDIO_EXT: AUDIO,
    ARCHIVES_EXT: ARCHIVES
}

EXCLUSION_SET = ('archives', 'video', 'audio', 'documents', 'images', 'others')


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ts', 'ch',
               'sh', 'sch', '', 'y', '', 'e', 'yu', 'u', 'ja', 'je', 'ji', 'g')

TRANS = {}

for cyrylic, trans in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrylic)] = trans
    TRANS[ord(cyrylic.upper())] = trans.upper()


def translate(file_name: str):
    translate_name = ''
    for char in file_name:
        translate_name += TRANS.get(ord(char), char)
    return translate_name


def normalize(ukr_string: str):
    eng_string = ukr_string.translate(TRANS)
    eng_string = re.sub(r"\W", "_", eng_string)
    return eng_string


def pick_ext(file: Path):
    ext = file.suffix[1:].upper()
    if not ext:
        OTHERS.append(file)
        return
    for item in EXT:
        if ext in item:
            REGISTER_EXTENSIONS[item].append(file)
            KNOWN_EXT.append(ext)
            return
    OTHERS.append(file)
    UNKNOWN_EXT.append(ext)
    return


def scan_folder(folder: Path):
    if not folder.exists():
        print(f'No folder "{folder}" in current directory')
        return None
    for file in folder.iterdir():
        if file.is_dir():
            if file.name not in EXCLUSION_SET:
                scan_folder(file)
                FOLDERS.append(file)
            continue
        if file.is_file():
            pick_ext(file)
    return None


def print_lst():
    if IMAGES:
        print('IMAGES:')
        for image in IMAGES:
            print(f'\t{image.name}')

    if VIDEO:
        print(f'VIDEO:')
        for video in VIDEO:
            print(f'\t{video.name}')

    if DOCUMENTS:
        print(f'DOCUMENTS:')
        for doc in DOCUMENTS:
            print(f'\t{doc.name}')

    if AUDIO:
        print(f'AUDIO:')
        for audio in AUDIO:
            print(f'\t{audio.name}')

    if ARCHIVES:
        print(f'ARCHIVES:')
        for arch in ARCHIVES:
            print(f'\t{arch.name}')

    if OTHERS:
        print(f'OTHERS:')
        for other in OTHERS:
            print(f'\t{other.name}')

    if FOLDERS:
        print(f'FOLDERS:')
        for folder in FOLDERS:
            print(f'\t{folder.name}')
    print()
    if KNOWN_EXT:
        print(f'Known extensions: {" ".join(set(KNOWN_EXT))}')
    if UNKNOWN_EXT:
        print(f'Unknown extensions: {" ".join(set(UNKNOWN_EXT))}')


def handle_files(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    normalized_name = normalize(normalize(file_name.stem)) + file_name.suffix
    print(f'...replacing {file_name.name}')
    file_name.replace(target_folder / normalized_name)


def handle_archives(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    name = normalize(file_name.stem)
    normalized_name = name + file_name.suffix
    full_name = target_folder / normalized_name
    file_name.replace(full_name)
    target_folder.mkdir(exist_ok=True, parents=True)
    new_dir = target_folder / name
    new_dir.mkdir(exist_ok=True, parents=True)
    print(f'...unpacking archive {file_name.name}')
    unpack_archive(full_name, new_dir)


def handle_folder(file_name: Path):
    print(f'...deleting {file_name.name}')
    file_name.rmdir()


def main(folder: Path):
    scan_folder(folder)
    for file in IMAGES:
        handle_files(file, folder / 'images')
    for file in VIDEO:
        handle_files(file, folder / 'video')
    for file in AUDIO:
        handle_files(file, folder / 'audio')
    for file in DOCUMENTS:
        handle_files(file, folder / 'documents')
    for file in OTHERS:
        handle_files(file, folder / 'others')
    for file in ARCHIVES:
        handle_archives(file, folder / 'archives')
    for file in FOLDERS:
        handle_folder(file)
    print_lst()


if __name__ == '__main__':
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Work with "{folder_for_scan}" folder...')
        main(folder_for_scan.resolve())
    else:
        print('Not enough arguments')

