import os
import uuid

def gen_id():
  return f"id: {uuid.uuid4().hex}\n"

def update_file(filename, data):
  with open(filename, 'w') as fo:
    fo.writelines(data)

def add_id(pathname):
  with open(pathname) as fo:
    lines = fo.readlines()

    """ Check the presence of frontmatter """
    # If not
    if lines[0].strip() != '---':
      print(f"  FM not found in {pathname}!\n  Proceeding with creation of frontmatter with `id`.")      

      new_id = gen_id()
      lines.insert(0, '---\n')
      lines.insert(1, new_id)
      lines.insert(2, '---\n\n')

      update_file(pathname, lines)
      print(f'  {pathname} processed.')

    # If yes
    else:
      print(f"  FM found in {pathname}. Checking for existing `id`.");

      # Extract the end of frontmatter
      fm_end = None
      for i in range(1, len(lines)):
        if lines[i].strip() == '---':
          fm_end = i
          break

      # Check the presence of an id
      for i in range(0, fm_end):
        if lines[i].startswith('id:'):
          print(f'  Found id for {pathname}. No need to append `id`.\n')
          return

      # id not found, assign a new id
      print("  id not found. Appending new id.")
      new_id = gen_id()
      lines.insert(1, new_id)
      update_file(pathname, lines)
      print(f'  {pathname} processed.\n')

def check_id(dir):
  print(f"Working inside: {dir}")

  count = 0
  for cur_dir, sub_dirs, files in os.walk(dir):
    for f in files:
      if f.endswith('.md'):
        path = os.path.join(cur_dir, f)
        print(f"File {count+1}: {path}")
        add_id(path)
        count = count+1
  
  print(f"Processes {count} files in {dir}")

def gen_mapping(dir):
  mapping = []

  for cur_dir, sub_dirs, files in os.walk(dir):
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

  print("Mappings generated successfully.\n")

def main():
  root_dir = './content/'

  # check_id(root_dir)

  gen_mapping(root_dir)

main()