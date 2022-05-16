from PIL import Image, ImageDraw
from quickdraw.data import QuickDrawData
import svgwrite

rows = int(input("How many rows do you want? "))
columns = int(input("How many columns do you want? "))
rows_columns = rows * columns
rows_count = 0
columns_count = 0

while True:
    qd = QuickDrawData()
    selected_category = str.lower((input("What is your category of choice? ")))
    try:
        selected_item = qd.get_drawing(selected_category)
        break
    except ValueError:
        print(f"{selected_category} is not a valid category. Try another one.")

dwg = svgwrite.Drawing(f'{selected_category}_01.svg', profile='tiny')

for image in range(rows_columns):
    row_offset = rows_count * 500
    column_offset = columns_count * 500
    qd = QuickDrawData()
    selected_item = qd.get_drawing(selected_category)
    item_image = Image.new("RGB", (255, 255), color=(255, 255, 255))
    item_drawing = ImageDraw.Draw(item_image)

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

    if columns_count < columns - 1:
        columns_count += 1
    else:
        columns_count = 0
        rows_count += 1
dwg.save(f"{selected_category}_01.gif")
