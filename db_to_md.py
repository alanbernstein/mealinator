import sqlite3
import os

# Path to your Mealie SQLite database
DB_PATH = "mealie.db"
OUTPUT_DIR = "md"

# todo
# - original url
# - image

def extract_recipes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all recipes
    cursor.execute("SELECT id, name, slug, description, org_url FROM recipes")
    recipes = cursor.fetchall()

    for recipe in recipes:
        recipe_id, name, slug, description, org_url = recipe

        # instructions
        cursor.execute("SELECT text FROM recipe_instructions WHERE recipe_id=?", (recipe_id,))
        instructions = "\n".join(f"- {row[0]}" for row in cursor.fetchall())

        # ingredients
        cursor.execute("SELECT note FROM recipes_ingredients WHERE recipe_id=?", (recipe_id,))
        ingredients = "\n".join(f"- {row[0]}" for row in cursor.fetchall())

        # tags
        cursor.execute("""
            SELECT tags.slug 
            FROM tags 
            JOIN recipes_to_tags ON tags.id = recipes_to_tags.tag_id 
            WHERE recipes_to_tags.recipe_id=?
        """, (recipe_id,))
        tags = ", ".join(row[0] for row in cursor.fetchall())

        # categories
        cursor.execute("""
            SELECT categories.slug 
            FROM categories 
            JOIN recipes_to_categories ON categories.id = recipes_to_categories.category_id 
            WHERE recipes_to_categories.recipe_id=?
        """, (recipe_id,))
        categories = ", ".join(row[0] for row in cursor.fetchall())

        cursor.execute("""
            SELECT recipe_comments.text, recipe_comments.user_id 
            FROM recipe_comments
            WHERE recipe_comments.recipe_id=?
        """, (recipe_id,))
        #comments = ", ".join(f'{row[1]}: {row[0]}' for row in cursor.fetchall())
        # TODO: get username from user id
        comments = ", ".join(f'{row[0]}' for row in cursor.fetchall())

        cursor.execute("""
            SELECT rte.subject, rte.message, rte.update_at
            FROM recipe_timeline_events as rte
            WHERE event_type not like "%system"
            AND rte.recipe_id=?
        """, (recipe_id,))
        makes = ", ".join(f'{row[0]}: {row[1]} {row[2]}'  for row in cursor.fetchall())

        # generate markdown
        markdown_content = f"""% {name}

## {name}

tags: {tags}

categories: {categories}

### Description
{description}

[original site]({org_url})

### Ingredients
{ingredients}

### Instructions
{instructions}

### Comments
{comments}

### Makes
{makes}
"""

        # Save to a Markdown file
        file_path = os.path.join(OUTPUT_DIR, f"mealie-{slug}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"Saved: {file_path}")

    conn.close()
    print(f"Extracted {len(recipes)} recipes as Markdown files in '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    extract_recipes()
