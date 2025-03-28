def read_unique_lines(file_path:str) -> set[str] | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return {line.strip() for line in f}
    except:
        return None


def main():
    print("")

if __name__ == '__main__':
    main()
