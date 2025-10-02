# TO BE RUN BY WORKFLOW ONLY
# LOCAL ONLY FOR TESTING

import os, json

ROOT_DIR = 'content/docs/'
# ROOT_DIR = '/home/username_anna/Desktop/my-site/content'
mappings = {
  "nodes": [],
  "edges": []
}

def xfm(path):
  with open(path) as fo:
    lines = fo.readlines()
    id = lines[1].split("id: ")[1].rstrip('\n')
    title = lines[2].split("title: ")[1].rstrip('\n')
    return (id, title)

def update_json(mapp, path):
  with open(path, "w") as fo:
    json.dump(mapp, fo, indent=2)

def main():
  for cur_dir, _, files in os.walk(ROOT_DIR):
    if 'extra' not in cur_dir:
      for f in files:
        if f.endswith(".md"):

          # Populate node per file
          path = os.path.join(cur_dir, f)
          id, title = xfm(path)

          if path.endswith("_index.md"):
            path_ = '..' + path.lstrip('content').rstrip('_index.md')
          else:
            path_ = '..' + path.lstrip('content').rstrip('.md')

          node_ = {"id": id, "label": title, "path": path_}
          mappings["nodes"].append(node_)

          # Populate edges per file, if any
          with open(path) as fo:
            lines = fo.readlines()
            for line in lines:
              if 'doclink' in line:
                dest_id = line.split("doclink")[1].split('"')[1]
                edge_ = {"source": id, "target": dest_id}
                mappings["edges"].append(edge_)

  update_json(mappings, 'static/graph/graph.json')

main()