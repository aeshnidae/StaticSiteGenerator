import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception("Invalid markdown - No title")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown_text = file.read()

    with open(template_path, "r") as file:
        template_text = file.read()

    title = extract_title(markdown_text)

    markdown_nodes = markdown_to_html_node(markdown_text)
    markdown_html = markdown_nodes.to_html()

    output = template_text.replace("{{ Title }}", title)
    output = output.replace("{{ Content }}", markdown_html)
    output = output.replace('href="/', f'href="{basepath}')
    output = output.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as file:
        file.write(output)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        file_path = f"{dir_path_content}/{filename}"
        dest_path = f"{dest_dir_path}/{filename}"
        if os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path, basepath)
        elif file_path.endswith(".md"):
            if not os.path.exists(dest_dir_path):
                os.makedirs(dest_dir_path)
            dest_path = dest_path.replace(".md", ".html")   
            generate_page(file_path, template_path, dest_path, basepath)

