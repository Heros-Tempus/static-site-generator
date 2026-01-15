import sys
from generate_page import generate_page_recursive, override_directory

def main():
    basepath = (sys.argv[1] or "/") if len(sys.argv) > 1 else "/"
    override_directory("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()