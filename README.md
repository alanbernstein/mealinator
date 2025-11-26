![screenshot](screenshot.png)

## What

A static site generator that pulls content from your [Mealie](https://mealie.io/) ([github](https://github.com/mealie-recipes/mealie)) database, and renders it without depending on modern web technologies.

## Why
Motivated by using a very old iPad as a kitchen recipe viewer.

## How
Developed for my own circumstances, including:

- Mealie 2.4.1
- Running in Docker on Ubuntu
- Deployed to my cheap shared-host server over ftp with curl
- Focused on viewing recipes with main images, not any other use case

# Usage

`pip install -r requirements.txt`

define these somewhere:

```
export WEBSITE_FTP_URL="example.com"
export WEBSITE_FTP_USERNAME="duder"
export WEBSITE_FTP_PASSWORD="hunter2"
```

If you are using the ftp deployment, create the remote directories manually:

```
mkdir recipes && cd recipes
mkdir html
mkdir images
mkdir images/thumbnails
```

Then, if you are very lucky, you can run `make run` and everything will work. Or, check the `run` target in `Makefile` for more details on the steps you can use yourself.