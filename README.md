![screenshot](screenshot.png)

## What

A static site generator that pulls content from your [Mealie](https://mealie.io/) ([github](https://github.com/mealie-recipes/mealie)) database, and renders it without depending on modern web technologies.

## Why
Motivated by using a very old iPad as a kitchen recipe viewer.

## How
Developed for my own circumstances, including:

- Mealie 2.4.1
- Running in Docker on Ubuntu
- Static content deployed to my cheap shared-host server over ftp with curl
- Focused on viewing recipes with main images, not any other use case

# Usage

`pip install -r requirements.txt`

If you are using the ftp deployment:

```
export WEBSITE_FTP_URL="example.com"
export WEBSITE_FTP_USERNAME="duder"
export WEBSITE_FTP_PASSWORD="hunter2"

mkdir recipes && cd recipes
mkdir html
mkdir images
mkdir images/thumbnails
```

Then, if you are very lucky, you can run `make run` and everything will work. Or, check the `run` target in `Makefile` for more details on the steps you can use yourself.

The deployment works on changed files only, in theory, so it might be ok to run nightly (at your own risk).


## TODO
- list view in addition to card view
- make the cards show up in 2x or 3x grid on ipad
- add a "source" tag: [mealie, secret-layer-cakes]
- search (that works on ipad?)
- comments, makes
- show domain name of original url
- link to cooked.wiki/archive.is if its a nyt recipe
x extract images
x link to cooked.wiki page
x deploy over ftp from desktop
x export changes only
x deploy changes only