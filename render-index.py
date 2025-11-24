#!/usr/bin/env python3
import jinja2
import datetime
import glob
import os

from ipdb import iex, set_trace as db

db_file = 'mealie.db'
TEMPLATE_FILE = "index-template.html"
output_file = "index.html"

time_fmt = '%Y/%m/%d %H:%M:%S'
now = datetime.datetime.now()
now_str = datetime.datetime.strftime(now, time_fmt)
db_exported_epoch = os.stat(db_file).st_mtime
db_exported_dt = datetime.datetime.fromtimestamp(db_exported_epoch)
db_exported_str = datetime.datetime.strftime(db_exported_dt, time_fmt)

def read_tags_from_html(fname):
    with open(fname, 'r') as f:
        lines = f.read().strip().split('\n')

    tags = []
    categories = []
    for l in lines:
        if l.startswith("<p>tags:"):
            tags_str = l.replace('<p>tags:', '').replace('</p>', '').strip()
            if tags_str != '':
                tags = tags_str.split(', ')
            #db()
            #if 'keto' in fname:
            #    db()
        if l.startswith("<p>categories:"):
            cats_str = l.replace('<p>categories:', '').replace('</p>', '').strip()
            if cats_str != '':
                categories = cats_str.split(', ')
    #db()
    #if 'keto' in fname:
    #    db()
    return list(set(tags + categories))

def main():
    # read recipe files
    all = glob.glob("html/*.html")
    nonmealie = []
    mealie = []
    for fname in all:
        slug = fname.replace('html/', '').replace('.html', '')
        tags = read_tags_from_html(fname)
        print('%s %s' % (slug, tags))
        if 'mealie' in fname:
            slug = slug.replace('mealie-', '')
            mealie.append({"title": slug, "tags": ", ".join(tags)})
        else:
            nonmealie.append({"title": slug, "tags": ", ".join(tags)})

    # render template
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)
    rendered = template.render(recipes=nonmealie, mealie_recipes=mealie, db_exported=db_exported_str, now=now_str)

    with open(output_file, 'w') as f:
        f.write(rendered)

    print('wrote %d bytes to %s' % (len(rendered), output_file))


main()
