import re
import os

input_path = './raw'
output_path = './dataset'

def read_file(path: str) -> str:
    with open(path, encoding="shift_jis") as f:
        return f.read()

def save_file(path: str, text: str):
    with open(path, mode='x', encoding="shift_jis") as f:
        f.write(text)


def scan_dir(path, mode='folder') -> list[str]:
    try:
        with os.scandir(path) as entries:
            if mode == 'folder':
                items = [entry.name for entry in entries]
            else:
                items = [entry.name for entry in entries if entry.is_file()]
        return items
    except Exception as e:
        print(e)


def del_decoration(text) -> str:
    pattern_header = r'^.*?[-]+.*?[-]+\r?\n'
    pattern_bottom = r'底本：.*'
    pattern_rubi = r'《[^》]*》\n?'
    pattern_chu = r'［＃[^］]*］\n?'
    pattern_rubiStart = r'｜'
    text = re.sub(pattern_header, '', text, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(pattern_bottom, '', text, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(pattern_rubi, '', text, flags=re.MULTILINE)
    text = re.sub(pattern_chu, '', text, flags= re.MULTILINE)
    text = re.sub(pattern_rubiStart, '', text)
    result = text.strip('\n')
    return result


def run():
    folders = scan_dir(input_path)

    for folder in folders:
        print(folder)
        os.mkdir(f'{output_path}/{folder}')
        files = scan_dir(f'{input_path}/{folder}', mode='file')
        for file in files:
            print(file)
            text = read_file(f'{input_path}/{folder}/{file}')
            fixText =  del_decoration(text)
            save_file(f'{output_path}/{folder}/{file}', fixText)
            
            
run()