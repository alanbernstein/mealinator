.phony: commit render render-index deploy view

commit:
	git add md/*.md
	git commit -m"Makefile commit $(date)"
	git push

MD_DIR := md
HTML_DIR := html
CSS_FILE := style.css
MD_FILES := $(wildcard $(MD_DIR)/*.md)
HTML_FILES := $(patsubst $(MD_DIR)/%.md,$(HTML_DIR)/%.html,$(MD_FILES))

run:
	get_mealie_db
	extract_mealie_recipes
	render
	render-index
	deploy

render: $(HTML_FILES)

# Rule to convert each .md to .html
$(HTML_DIR)/%.html: $(MD_DIR)/%.md $(CSS_FILE)
	@echo "Converting $< to $@"
	pandoc $< --standalone --css $(CSS_FILE) --output $@

render-manual:
	# pandoc md/na-bao-coconut-jam.md --standalone --css style.css --embed-resources --output html/na-bao-coconut-jam.html
	pandoc md/02-18-chocolate-covered-strawberry-mousse-cake.md --standalone --css style.css --output html/02-18-chocolate-covered-strawberry-mousse-cake.html
	pandoc md/cauliflower-cashew-curry.md --standalone --css style.css --output html/cauliflower-cashew-curry.html

render-index:
	python3 render-index.py

deploy:
	# curl -T index.html ftp://${WEBSITE_FTP_URL}/recipes/index.html --user ${WEBSITE_FTP_USERNAME}:${WEBSITE_FTP_PASSWORD}
	curl -T html/02-18-chocolate-covered-strawberry-mousse-cake.html ftp://${WEBSITE_FTP_URL}/recipes/02-18-chocolate-covered-strawberry-mousse-cake.html --user ${WEBSITE_FTP_USERNAME}:${WEBSITE_FTP_PASSWORD}

view:
	firefox http://alanbernstein.net/recipes

get_mealie_db:
	docker cp mealie:/app/data/mealie.db .

extract_mealie_recipes:
	python3 db_to_md.py
