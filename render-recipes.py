#!/usr/bin/env python3
import sqlite3
import os
import jinja2

# Paths
DB_PATH = "mealie.db"
HTML_DIR = "html"
TEMPLATE_FILE = "recipe-template.html"

def render_recipes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the output directory exists
    os.makedirs(HTML_DIR, exist_ok=True)

    # Load Jinja template
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(TEMPLATE_FILE)

    # Get all recipes
    cursor.execute("SELECT id, name, slug, description, org_url FROM recipes")
    recipes = cursor.fetchall()

    for recipe in recipes:
        recipe_id, name, slug, description, org_url = recipe

        # Get instructions
        cursor.execute("SELECT text FROM recipe_instructions WHERE recipe_id=? ORDER BY position", (recipe_id,))
        instructions = [row[0] for row in cursor.fetchall()]

        # Get ingredients
        cursor.execute("SELECT note FROM recipes_ingredients WHERE recipe_id=? ORDER BY position", (recipe_id,))
        ingredients = [row[0] for row in cursor.fetchall()]

        # Get tags
        cursor.execute("""
            SELECT tags.name
            FROM tags
            JOIN recipes_to_tags ON tags.id = recipes_to_tags.tag_id
            WHERE recipes_to_tags.recipe_id=?
        """, (recipe_id,))
        tags = [row[0] for row in cursor.fetchall()]

        # Get categories
        cursor.execute("""
            SELECT categories.name
            FROM categories
            JOIN recipes_to_categories ON categories.id = recipes_to_categories.category_id
            WHERE recipes_to_categories.recipe_id=?
        """, (recipe_id,))
        categories = [row[0] for row in cursor.fetchall()]

        # Combine tags and categories
        all_tags = tags + categories

        # Get comments
        cursor.execute("""
            SELECT recipe_comments.text
            FROM recipe_comments
            WHERE recipe_comments.recipe_id=?
        """, (recipe_id,))
        comments = ", ".join(row[0] for row in cursor.fetchall())

        # Get timeline events
        cursor.execute("""
            SELECT rte.subject, rte.message, rte.update_at
            FROM recipe_timeline_events as rte
            WHERE event_type not like "%system"
            AND rte.recipe_id=?
        """, (recipe_id,))
        makes = ", ".join(f'{row[0]}: {row[1]} {row[2]}'  for row in cursor.fetchall())

        # Render the template
        rendered = template.render(
            name=name,
            slug=slug,
            description=description,
            org_url=org_url,
            ingredients=ingredients,
            instructions=instructions,
            tags=all_tags,
            comments=comments if comments else None,
            makes=makes if makes else None
        )

        # Save to HTML file
        file_path = os.path.join(HTML_DIR, f"mealie-{slug}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"Rendered: {file_path}")

    conn.close()
    print(f"Rendered {len(recipes)} recipes as HTML files in '{HTML_DIR}'.")

if __name__ == "__main__":
    render_recipes()
