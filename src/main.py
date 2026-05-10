from gencontent import generate_pages_recursive
from copystatic import copyFromTo

import shutil
import os

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"





def main():
    print("Deleting public directory...")
    shutil.rmtree(dir_path_public , ignore_errors=True)
    os.mkdir(dir_path_public)

    copyFromTo(dir_path_static,dir_path_public)

    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public
        )


main()