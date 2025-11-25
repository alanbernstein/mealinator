.phony: commit render render-index deploy deploy-quick view clean

commit:
	git add md/*.md
	git commit -m"Makefile commit $(date)"
	git push

HTML_DIR := html
FTP_BASE := ftp://${WEBSITE_FTP_URL}/recipes
FTP_AUTH := --user ${WEBSITE_FTP_USERNAME}:${WEBSITE_FTP_PASSWORD}
FTP_FLAGS := --ftp-ssl --ssl-reqd --insecure
CURL_UPLOAD := curl ${FTP_FLAGS} ${FTP_AUTH} -T

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

deploy:
	@echo "Deploying index.html..."
	${CURL_UPLOAD} index.html ${FTP_BASE}/index.html
	@echo "Deploying style.css..."
	${CURL_UPLOAD} style.css ${FTP_BASE}/style.css
	@echo "Deploying placeholder image..."
	${CURL_UPLOAD} images/placeholder.jpg ${FTP_BASE}/images/placeholder.jpg
	@echo "Deploying HTML files..."
	@for file in html/mealie-*.html; do \
		filename=$$(basename $$file); \
		echo "  Uploading $$filename..."; \
		${CURL_UPLOAD} $$file ${FTP_BASE}/html/$$filename; \
	done
	@echo "Deploying full-size images..."
	@for file in images/mealie-*.jpg; do \
		filename=$$(basename $$file); \
		echo "  Uploading $$filename..."; \
		${CURL_UPLOAD} $$file ${FTP_BASE}/images/$$filename; \
	done
	@echo "Deploying thumbnail images..."
	@for file in images/thumbnails/mealie-*.jpg; do \
		filename=$$(basename $$file); \
		echo "  Uploading $$filename..."; \
		${CURL_UPLOAD} $$file ${FTP_BASE}/images/thumbnails/$$filename; \
	done
	@echo "Deploy complete!"

deploy-quick:
	@echo "Quick deploy: index.html and style.css only..."
	${CURL_UPLOAD} index.html ${FTP_BASE}/index.html
	${CURL_UPLOAD} style.css ${FTP_BASE}/style.css

view-local:
	firefox index.html

view:
	firefox http://alanbernstein.net/recipes

