def read_unique_lines(file_path:str) -> set[str] | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return {line.strip() for line in f}
    except:
        return None

def write_unique_lines(file_path: str, lines: set[str]) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line)
                f.write("\n")
        return True
    except OSError:
        return False

def main():
    print("")

if __name__ == '__main__':
    main()
