.phony: commit render render-index deploy deploy-all deploy-quick view view-local clean clean-deploy

commit:
	git add md/*.md
	git commit -m"Makefile commit $(date)"
	git push

HTML_DIR := html
DEPLOY_DIR := .deploy
FTP_BASE := ftp://${WEBSITE_FTP_URL}/recipes
FTP_AUTH := --user ${WEBSITE_FTP_USERNAME}:${WEBSITE_FTP_PASSWORD}
FTP_FLAGS := -s --ftp-ssl --ssl-reqd --insecure
CURL_UPLOAD := curl ${FTP_FLAGS} ${FTP_AUTH} -T

# Collect all files that should be deployed
HTML_FILES := $(wildcard html/mealie-*.html)
IMAGE_FILES := $(wildcard images/mealie-*.jpg)
THUMBNAIL_FILES := $(wildcard images/thumbnails/mealie-*.jpg)

# Create corresponding timestamp files in .deploy directory
DEPLOY_HTML := $(patsubst html/%.html,$(DEPLOY_DIR)/html/%.deployed,$(HTML_FILES))
DEPLOY_IMAGES := $(patsubst images/%.jpg,$(DEPLOY_DIR)/images/%.deployed,$(IMAGE_FILES))
DEPLOY_THUMBNAILS := $(patsubst images/thumbnails/%.jpg,$(DEPLOY_DIR)/thumbnails/%.deployed,$(THUMBNAIL_FILES))

run:
	$(MAKE) get_mealie_db
	$(MAKE) extract_images
	$(MAKE) convert_images
	$(MAKE) extract_mealie_recipes
	$(MAKE) render
	$(MAKE) render-index
	$(MAKE) deploy

get_mealie_db:
	docker cp mealie:/app/data/mealie.db .

extract_images:
	python3 extract_images.py

convert_images:
	python3 convert_images_to_jpg.py

extract_mealie_recipes:
	python3 db_to_md.py

render:
	python3 render-recipes.py

render-index:
	python3 render-index.py

clean:
	rm -f $(HTML_DIR)/mealie-*.html
	rm -f index.html

clean-deploy:
	rm -rf $(DEPLOY_DIR)

# Incremental deploy - only uploads files that have changed
deploy: $(DEPLOY_DIR)/index.deployed $(DEPLOY_DIR)/style.deployed $(DEPLOY_DIR)/placeholder.deployed $(DEPLOY_HTML) $(DEPLOY_IMAGES) $(DEPLOY_THUMBNAILS)
	@echo "Deploy complete! (only changed files were uploaded)"

# Force full deploy (clears timestamps first)
deploy-all: clean-deploy deploy

# Pattern rules for deploying individual files
# These use Make's dependency tracking - file is only uploaded if source is newer than .deployed timestamp

$(DEPLOY_DIR)/index.deployed: index.html
	@mkdir -p $(DEPLOY_DIR)
	@echo "Uploading index.html..."
	@${CURL_UPLOAD} $< ${FTP_BASE}/index.html
	@touch $@

$(DEPLOY_DIR)/style.deployed: style.css
	@mkdir -p $(DEPLOY_DIR)
	@echo "Uploading style.css..."
	@${CURL_UPLOAD} $< ${FTP_BASE}/style.css
	@touch $@

$(DEPLOY_DIR)/placeholder.deployed: images/placeholder.jpg
	@mkdir -p $(DEPLOY_DIR)
	@echo "Uploading placeholder.jpg..."
	@${CURL_UPLOAD} $< ${FTP_BASE}/images/placeholder.jpg
	@touch $@

$(DEPLOY_DIR)/html/%.deployed: html/%.html
	@mkdir -p $(DEPLOY_DIR)/html
	@echo "Uploading html/$*.html..."
	@${CURL_UPLOAD} $< ${FTP_BASE}/html/$*.html
	@touch $@

$(DEPLOY_DIR)/images/%.deployed: images/%.jpg
	@mkdir -p $(DEPLOY_DIR)/images
	@echo "Uploading images/$*.jpg..."
	@${CURL_UPLOAD} $< ${FTP_BASE}/images/$*.jpg
	@touch $@

$(DEPLOY_DIR)/thumbnails/%.deployed: images/thumbnails/%.jpg
	@mkdir -p $(DEPLOY_DIR)/thumbnails
	@echo "Uploading thumbnails/$*.jpg..."
	@${CURL_UPLOAD} $< ${FTP_BASE}/images/thumbnails/$*.jpg
	@touch $@

# Quick deploy for index and CSS only
deploy-quick:
	@echo "Quick deploy: index.html and style.css only..."
	@${CURL_UPLOAD} index.html ${FTP_BASE}/index.html
	@${CURL_UPLOAD} style.css ${FTP_BASE}/style.css

view-local:
	firefox index.html

view:
	firefox http://alanbernstein.net/recipes

