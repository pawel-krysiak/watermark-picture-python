from PIL import Image, ImageDraw, ImageFont
import os

def process_image(image_name, number):
    # watermark picture with number
    font = ImageFont.truetype("SignPainter.ttf", 85)
    main = Image.open(image_name)
    watermark = Image.new("RGBA", main.size)
    waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
    waterdraw.text((40, 40), str(number), font=font)
    main.paste(watermark, None, watermark)
    main.save("export/" + image_name, "JPEG")

def watermark_number(file_name):
    # choose middle number from file name
    # 'material-1-2.jpg' or 'material-1.jpg' files
    l = file_name.split('-')
    if len(l) == 3:
        return l[1]
    elif len(l) == 2:
        return l[1].split('.')[0]

def main(directory='.'):
    all_files = os.listdir(directory)
    image_files = [i for i in all_files if i.endswith('.jpg') and i.startswith('material')]
    if not os.path.exists('export'):
        os.makedirs('export')
    for image_name in image_files:
        print "processing image: " + image_name
        watermark = watermark_number(image_name)
        process_image(image_name, watermark)
    print 'processing finished.'

main()
