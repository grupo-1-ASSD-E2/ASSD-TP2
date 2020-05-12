""" This compile.py script is intended to automatically compile all *.ui and *.qrc files created with QtDesigner
    into the python files needed.
"""

# Python modules
import os


def log(text: str):
    print(f'QtDesigner Compiler >> {text}')


if __name__ == "__main__":
    CURRENT_PATH = os.getcwd()
    DESIGNER_PATH = "designer"
    RESOURCES_PATH = "resources"
    DESIGNER_COMPILED_PATH = os.path.join("src", "ui")
    RESOURCES_COMPILED_PATH = os.path.join("src", "resources")

    # Compiling the .qrc files, getting their names and running the command ony by one
    resources_files = os.listdir(os.path.join(CURRENT_PATH, RESOURCES_PATH))
    compiled_resources = []
    log(f'{len(resources_files)} resource files were found!')
    for resource_file in resources_files:
        log(f'Compiling "{resource_file}"...')
        compiled_resource = os.path.join(RESOURCES_COMPILED_PATH, f"{resource_file[:-4]}_rc.py")
        compiled_resources.append(f"{resource_file[:-4]}_rc.py")
        os.system(f'pyrcc5 {os.path.join(RESOURCES_PATH, resource_file)} -o {compiled_resource}')

    # Compiling the .ui files, getting their names and running the command one by one
    designer_files = os.listdir(os.path.join(CURRENT_PATH, DESIGNER_PATH))
    log(f'{len(designer_files)} ui files were found!')
    for designer_file in designer_files:
        log(f'Compiling "{designer_file}"...')
        os.system(f'pyuic5 -x {os.path.join(DESIGNER_PATH, designer_file)} -o {os.path.join(DESIGNER_COMPILED_PATH, f"{designer_file[:-3]}.py")}')

    # Fixing bad resource importing, opening each compiled design file and searching bad resource importing...
    for designer_file in designer_files:
        filename = os.path.join(CURRENT_PATH, DESIGNER_COMPILED_PATH, f"{designer_file[:-3]}.py")
        content = ""
        rewrite = False

        file = open(filename, 'r')
        for line in file:
            if '\n' in line:
                line = line[:-1]

            for resource in compiled_resources:
                if line == f'import {resource[:-3]}':
                    content += f'from FrontEnd.src.resources import {resource[:-3]}\n'
                    rewrite = True
                    break
            else:
                content += f'{line}\n'
        file.close()

        if rewrite:
            file = open(filename, 'w')
            file.write(content)
            file.close()
