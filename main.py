import argparse
import os

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


def validate_txt_file(file_path: str) -> str:
    if not file_path.lower().endswith('.txt'):
        raise argparse.ArgumentTypeError("File must have a .txt extension")
    
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"File does not exist: {file_path}")
    
    return file_path

def main():
    parser = argparse.ArgumentParser(description="Compare two text files and save results.")
    parser.add_argument('file1', type=validate_txt_file, help='First input text file')
    parser.add_argument('file2', type=validate_txt_file, help='Second input text file')
    parser.add_argument('--same', default='same.txt', help='Output file for common lines')
    parser.add_argument('--diff', default='diff.txt', help='Output file for different lines')

    args = parser.parse_args()
    
    lines1 = read_unique_lines(args.file1)
    lines2 = read_unique_lines(args.file2)
    
    if lines1 is None or lines2 is None:
        print("Error: Could not read one or both files.")
        return
    
    common_lines = lines1.intersection(lines2)
    different_lines = lines1.symmetric_difference(lines2)

    if write_unique_lines(args.same, common_lines):
        print(f"Common lines written to {args.same}")
    else:
        print(f"Error: Could not write to {args.same}")
    
    if write_unique_lines(args.diff, different_lines):
        print(f"Unique lines written to {args.diff}")
    else:
        print(f"Error: Could not write to {args.diff}")

if __name__ == '__main__':
    main()
