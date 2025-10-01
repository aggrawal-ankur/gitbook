import os

ROOT_DIR = './content/'
OUT_FILE = './data/links.json'

def gen_mapping(dir):
  mapping = []

  for cur_dir, _, files in os.walk(dir):
    for f in files:
      if f.endswith('.md'):
        path = os.path.join(cur_dir, f)

        with open(path) as fo:
          id_line = fo.readline()    # ---
          id_line = fo.readline()    # id: .....
          id = id_line.split(": ")[1].split("\n")[0]

          rel_path = os.path.relpath(path, dir)
          rel_path = '/gitbook/' + os.path.splitext(rel_path)[0] + '/'
          mapping.append(f'  "{id}": "{rel_path}",\n')

  # Remove the trailing comma
  mapping[-1] = mapping[-1].split(",")[0] + '\n'

  with open("./data/links.json", "w") as fo:
    fo.write("{\n")
    fo.writelines(mapping)
    fo.write("}")

def main():
  gen_mapping(ROOT_DIR)

if __name__ == "__main__":
  main()