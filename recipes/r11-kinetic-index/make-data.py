"""Writes assets/data.js from titles.txt, one title per line, for the Kinetic Index film.
Swap titles.txt for your own list (posts, products, a menu, a changelog), then change the three search
words in Q in index.html to words that appear in your list.
Usage: python make-data.py"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "titles.txt"), encoding="utf-8") as f:
    titles = [line.strip() for line in f if line.strip()]
assert len(titles) >= 12, "add at least 12 titles so the rows don't repeat too often"
with open(os.path.join(HERE, "assets", "data.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.BLOG_TITLES = " + json.dumps(titles, ensure_ascii=False, indent=1) + ";\n")
print("titles:", len(titles))
