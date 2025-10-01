# TO BE USED LOCALLY ONLY

import sys, uuid

def genid():
  return uuid.uuid4().hex

def write_file(path, data):
  with open(path, "w") as fo:
    fo.writelines(data)

def main(path):
  with open(path, "r+") as fo:
    lines = []

    lines.append('---\n')
    lines.append( f"id: {genid()}\n" )
    lines.append('title:\n')
    lines.append('weight:\n')
    lines.append('---\n\n')

    write_file(path, lines)

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: script.py path/to/file")
  else:
    main(sys.argv[1])