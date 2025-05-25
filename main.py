import re
from colorama import Fore, Style, init


init()

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="ascii", errors="ignore") as f:
            return f.readlines()
    except FileNotFoundError:
        print("Файл не найден.")
        return []

def highlight_keywords(line, keywords):
    highlighted = line
    for word in keywords:
        highlighted = re.sub(
            rf"({re.escape(word)})",
            Fore.YELLOW + r"\1" + Style.RESET_ALL,
            highlighted,
            flags=re.IGNORECASE
        )
    return highlighted

def search_lines(lines, include_words, exclude_words, regex_patterns):
    results = []
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        
        if all(word.lower() in line_clean.lower() for word in include_words if word):
            
            if not any(word.lower() in line_clean.lower() for word in exclude_words if word):
                
                if all(re.search(pattern, line_clean, re.IGNORECASE) for pattern in regex_patterns if pattern):
                    results.append(line_clean)
    return results

def main():
    file_path = input("Путь к .txt файлу: ").strip()
    lines = read_file(file_path)
    if not lines:
        return

    include = input("Слова для включения (через запятую): ").strip().lower().split(",")
    exclude = input("Слова для исключения (через запятую): ").strip().lower().split(",")
    regex = input("Регулярные выражения (через запятую): ").strip().split(",")

    found = search_lines(lines, include, exclude, regex)

    if not found:
        print(Fore.RED + "Совпадений не найдено." + Style.RESET_ALL)
        return

    print(f"\nНайдено {len(found)} строк:\n")
    for line in found:
        print("→", highlight_keywords(line, include))

    
    if input("\nИскать конкретное слово бинарно? (y/n): ").strip().lower() == 'y':
        key = input("Введите ключевое слово: ").strip().lower()
        sorted_lines = sorted(found, key=lambda x: x.lower())
        left, right = 0, len(sorted_lines) - 1
        found_line = None
        while left <= right:
            mid = (left + right) // 2
            if key in sorted_lines[mid].lower():
                found_line = sorted_lines[mid]
                break
            elif key < sorted_lines[mid].lower():
                right = mid - 1
            else:
                left = mid + 1
        if found_line:
            print("\nНайдено:")
            print("→", highlight_keywords(found_line, [key]))
        else:
            print(Fore.RED + "Слово не найдено." + Style.RESET_ALL)

main()
