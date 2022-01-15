from PIL import Image, ImageDraw
import colorsys

colors = {}

def grey(rgb):
    return sum(rgb) / len(rgb)

def common_colors(colors):
    final = [colors[0]]

    for color in colors:
        for final_color in final:
            if abs(grey(color) - grey(final_color)) < 40:
                break
        else:
            final.append(color)          

    final.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))

    return final[::-1]
        

with Image.open("image.png") as image:
    pixels = image.load()

    for x in range(image.width):
        for y in range(image.height):
            pixel = pixels[x, y]

            if not pixel in colors:
                colors[pixel] = 1
            else:
                colors[pixel] += 1

    common = common_colors(sorted(colors, key=colors.get))

    new = Image.new("RGB", (image.width, image.height + image.width//5))

    x = image.width//5
    y1 = image.height
    y2 = image.height + image.width//5

    new.paste(image)
    draw = ImageDraw.Draw(new)

    for i, rgb in enumerate(common):
        draw.rectangle((x * i, y1, x * i + x, y2), fill=rgb)

    new.show()
    new.save("final.png")