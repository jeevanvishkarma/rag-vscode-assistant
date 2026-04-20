import os
def prompt_loader(filename):
    path= os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()