from PIL import Image, ImageDraw
from quickdraw.data import QuickDrawData
import svgwrite
import os
import random
from categories import categories_list

# Collect user's choice of category (repeat until valid category is selected)
print('What is your "Quick,Draw!" category of choice?')
while True:
    qd = QuickDrawData()

    # Generate 3 random Quick,draw categories as examples for the user
    random_categories = []
    for element in range(3):
        random_selection = random.choice(categories_list)
        while random_selection in random_categories:
            random_selection = random.choice(categories_list)
        random_categories.append(random_selection)

    # Prompt a reply from the user
    selected_category = str.lower((input(f"Some random categories are:"
                                         f" {random_categories[0]}, {random_categories[1]}, "
                                         f"{random_categories[2]}.\nYour choice is: ")))
    try:
        selected_item = qd.get_drawing(selected_category)
        break
    except ValueError:
        print(f"\n{selected_category} is not a valid category. Try another one.")

# Collect user's choice of number of columns and rows
rows = int(input("\nHow many rows do you want? "))
columns = int(input("How many columns do you want? "))
rows_columns = rows * columns
rows_count = 0
columns_count = 0

# Avoid file override
# Check for the next available name
file_index = 1
while os.path.exists(f"{selected_category}{file_index}.svg"):
    file_index += 1

# Setup the svg drawing, name and profile
dwg = svgwrite.Drawing(f'{selected_category}{file_index}.svg', profile='tiny')

# Get the specified number of drawing from QuickDraw's database
for image in range(rows_columns):
    row_offset = rows_count * 400
    column_offset = columns_count * 400
    qd = QuickDrawData()
    selected_item = qd.get_drawing(selected_category)
    item_image = Image.new("RGB", (255, 255), color=(255, 255, 255))
    item_drawing = ImageDraw.Draw(item_image)

    # Add each stroke of each selected drawing to the combined svg drawing
    for stroke in selected_item.strokes:
        for coordinate in range(len(stroke) - 1):
            x1 = stroke[coordinate][0]
            y1 = stroke[coordinate][1]
            x2 = stroke[coordinate + 1][0]
            y2 = stroke[coordinate + 1][1]
            item_drawing.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
            dwg.add(dwg.line((x1 + column_offset, y1 + row_offset),
                             (x2 + column_offset, y2 + row_offset),
                             stroke=svgwrite.rgb(10, 10, 16, '%')))

    # Increase rows / columns count
    if columns_count < columns - 1:
        columns_count += 1
    else:
        columns_count = 0
        rows_count += 1

# Export the completed .svg file
dwg.save(f"{selected_category}{file_index}.gif")

# Point the user to the .svg file location
print(f"Your file '{selected_category}{file_index}.svg' can be found here: {os.getcwd()}")
