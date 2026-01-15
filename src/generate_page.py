import re
import os
import shutil
from markdown_to_blocks import markdown_to_html_node

def extract_header(md):
    pattern = r"^#(?!#)\s+(.+?)\s*$"
    match = re.search(pattern, md, re.MULTILINE)
    if not match:
        raise ValueError("No h1 header found in markdown")
    return match.group(1)

def list_all_items(path):
    items:list[tuple] = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        rel_path = os.path.join(*full_path.split(os.sep)[1:])
        item = (rel_path, "dir") if os.path.isdir(full_path) else (rel_path, "file", full_path)
        items.append(item)
        if os.path.isdir(full_path):
            items.extend(list_all_items(full_path))
    return items

def override_directory(source, destination):
    if not os.path.isdir(source):
        return
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    items = list_all_items(source)
    for item in items:
        if item[1] == "dir":
            os.mkdir(os.path.join(destination, item[0]))
        if item[1] == "file":
            shutil.copy(item[2], os.path.join(destination, item[0]))

def generate_page(from_path, template_path, dest_path, base_path = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as source:
        with open(template_path) as template:
            read_source = source.read()
            read_template = template.read()
            title = extract_header(read_source)
            html_source = markdown_to_html_node(read_source).to_html()
            read_template = read_template.replace("{{ Title }}", title)
            read_template = read_template.replace("{{ Content }}", html_source)
            if base_path != "/":
                read_template = read_template.replace('href="/', f'href="{base_path}')
                read_template = read_template.replace('src="/', f'src="{base_path}')


            dir_path = os.path.dirname(dest_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(dest_path, "w") as dest:
                dest.write(read_template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path = "/"):
    if not os.path.isdir(dir_path_content):
        return
    items = list_all_items(dir_path_content)
    for item in items:
        if item[1] == "dir":
            os.makedirs(os.path.join(dest_dir_path, item[0]), exist_ok=True)
        if item[1] == "file":
            generate_page(item[2], template_path, os.path.join(dest_dir_path, item[0][:-2] + "html"), base_path)
        

if __name__ =="__main__":
    generate_page_recursive("content", "template.html", "test1")


