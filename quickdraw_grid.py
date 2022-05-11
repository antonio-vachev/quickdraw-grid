from PIL import Image, ImageDraw
from quickdraw.data import QuickDrawData
import svgwrite

name_var = 1
dwg = svgwrite.Drawing(f'duck_{name_var}.svg', profile='tiny')
rows = int(input("How many rows do you want? "))
columns = int(input("How many columns do you want? "))
rows_columns = rows * columns
rows_count = 0
columns_count = 0

for image in range(rows_columns):
    row_offset = rows_count * 500
    column_offset = columns_count * 500
    qd = QuickDrawData()
    duck = qd.get_drawing("helicopter")
    duck_image = Image.new("RGB", (255, 255), color=(255, 255, 255))
    duck_drawing = ImageDraw.Draw(duck_image)

    for stroke in duck.strokes:
        for coordinate in range(len(stroke) - 1):
            x1 = stroke[coordinate][0]
            y1 = stroke[coordinate][1]
            x2 = stroke[coordinate + 1][0]
            y2 = stroke[coordinate + 1][1]
            duck_drawing.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
            dwg.add(dwg.line((x1 + column_offset, y1 + row_offset), (x2 + column_offset, y2 + row_offset), stroke=svgwrite.rgb(10, 10, 16, '%')))

    if columns_count < columns - 1:
        columns_count += 1
    else:
        columns_count = 0
        rows_count += 1
    # duck_image.show()
dwg.save(f"my_duck{name_var}.gif")