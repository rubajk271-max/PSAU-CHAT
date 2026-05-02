from PIL import Image

def make_transparent(input_path, output_path):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    # threshold for considering a color "white" or close to white
    for item in datas:
        # Check if the pixel is very light (white background)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            # Change all white (also shades of whites) to transparent
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    make_transparent('logo1.png', 'logo1_transparent.png')
    print("Done")
