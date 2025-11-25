.phony: commit render render-index deploy view clean

commit:
	git add md/*.md
	git commit -m"Makefile commit $(date)"
	git push

HTML_DIR := html

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
	# curl -T index.html ftp://${WEBSITE_FTP_URL}/recipes/index.html --user ${WEBSITE_FTP_USERNAME}:${WEBSITE_FTP_PASSWORD}
	echo "${WEBSITE_FTP_URL}, ${WEBSITE_FTP_USERNAME}, ${WEBSITE_FTP_PASSWORD}"
	curl --ftp-ssl --ssl-reqd --insecure -T html/02-18-chocolate-covered-strawberry-mousse-cake.html ftp://${WEBSITE_FTP_URL}/recipes/02-18-chocolate-covered-strawberry-mousse-cake.html --user ${WEBSITE_FTP_USERNAME}:${WEBSITE_FTP_PASSWORD}

view-local:
	firefox index.html

view:
	firefox http://alanbernstein.net/recipes

