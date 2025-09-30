import os
import uuid
import json

ROOT_DIR = './content/'
OUT_FILE = './data/links.json'

def gen_id():
  return f"id: {uuid.uuid4().hex}\n"

def update_file(filename, data):
  with open(filename, 'w') as fo:
    fo.writelines(data)

def add_id(pathname):
  with open(pathname) as fo:
    lines = fo.readlines()

  if not lines or lines[0].strip() != '---':
    # create fresh frontmatter
    new_id = gen_id()
    lines.insert(0, '---\n')
    lines.insert(1, new_id)
    lines.insert(2, '---\n\n')
    update_file(pathname, lines)
    return new_id.strip().split(": ")[1]

  # find end of frontmatter
  fm_end = None
  for i in range(1, len(lines)):
    if lines[i].strip() == '---':
      fm_end = i
      break

  # check existing id
  for i in range(1, fm_end):
    if lines[i].startswith('id:'):
      return lines[i].split(": ")[1].strip()

  # add missing id
  new_id = gen_id()
  lines.insert(1, new_id)
  update_file(pathname, lines)
  return new_id.strip().split(": ")[1]

def gen_mapping(root):
  mapping = {}
  for cur_dir, _, files in os.walk(root):
    for f in files:
      if f.endswith('.md'):
        path = os.path.join(cur_dir, f)

        file_id = add_id(path)
        rel_path = os.path.relpath(path, root)
        rel_path = '/gitbook/' + os.path.splitext(rel_path)[0] + '/'
        mapping[file_id] = rel_path

  with open(OUT_FILE, 'w') as fo:
    json.dump(mapping, fo, indent=2)
  print(f"Mappings generated in {OUT_FILE}")

def main():
  gen_mapping(ROOT_DIR)

if __name__ == "__main__":
  main()
