from PIL import Image, ImageDraw, ImageFont
import os, shutil, argparse, sys, re

class PictureOrganizer:
    # Organizes pictures in directory
    # Process:
    # 1. Creates folders with numbers from picture_start_number to picture_end_number
    # 2. Let's user drop the pictures to proper folders
    # 3. Renames pictures in folders to format: [picture_file_prefix]-[folder_number]-[picture_number].jpg
    # 4. Moves files back to main directory and erase the folders

    def __init__(self, directory='./', picture_file_prefix= 'material', file_extension='.jpg', options={'picture_start_number':1, 'picture_end_number':29}):
        self.directory = directory
        self.options = options
        self.picture_file_prefix = picture_file_prefix
        self.file_extension = file_extension

    def organize(self):
        print "--- PictureOrganizer ---"
        self.create_directories()
        print raw_input('Organize your files to main folders and press any key:')
        self.rename_pictures_in_folders()
        self.move_files_back()
        print "Pictures organized."

    def create_directories(self):
        if not self.options:
            raise AttributeError("Start and End number for pictures need to be provided !")
        print "Creating directories..."
        for picture_number in range(self.options['picture_start_number'], self.options['picture_end_number'] + 1):
            directory = self.directory + str(picture_number)
            if not os.path.exists(directory):
                os.makedirs(directory)

    def rename_pictures_in_folders(self):
        print "Renaming moved files..."
        for picture_number in range(self.options['picture_start_number'], self.options['picture_end_number'] + 1):
            folder_path = self.directory + str(picture_number) + '/'
            if os.path.exists(folder_path):
                to_rename = filter(lambda file_name: file_name.endswith('.jpg'), os.listdir(folder_path))
                index = 1
                for picture_name in sorted(to_rename):
                    picture_path = folder_path + picture_name
                    new_picture_path = folder_path + self.new_picture_name(picture_number, index)
                    os.rename(picture_path, new_picture_path)
                    index += 1

    def move_files_back(self):
        print "Moving files back to main directory..."
        for picture_number in range(self.options['picture_start_number'], self.options['picture_end_number'] + 1):
            folder_path = self.directory + str(picture_number) + '/'
            for file_name in self.image_files_in_directory(folder_path):
                picture_path = folder_path + file_name
                if os.path.exists(picture_path):
                    main_dir_picture_path = self.directory + file_name
                    os.rename(picture_path, main_dir_picture_path)

            if os.path.exists(folder_path) and len(self.image_files_in_directory(folder_path)) == 0:
                shutil.rmtree(folder_path)

    def picture_path(self, picture_number, old=True):
        return self.directory + self.picture_name(picture_number)

    def new_picture_path(self, picture_number):
        return self.directory + str(picture_number) + '/' + self.picture_name(picture_number)

    def picture_name(self, picture_number):
        return self.picture_file_prefix + '-' + str(picture_number) + self.file_extension

    def new_picture_name(self, picture_number, index):
        return self.picture_file_prefix + '-' + str(picture_number) + '-' + str(index) + self.file_extension

    def image_files_in_directory(self, directory):
        return filter(lambda file_name: file_name.endswith('jpg'), os.listdir(directory))

class PictureWatermarker:
    # WatermarkPictures with number
    # Process:
    # 1. In given directory it goes through all the .jpg files with picture_file_prefix
    # 2. For each file:
    #   2.1 Fetches the picture_id from the file named in format [picture_file_prefix]-[picture_id].jpg or [picture_file_prefix]-[picture_id]-[picture_sub_id].jpg
    #   2.2 Applies the watermark to the picture with given number
    #   2.3 Saves picture in export directory

    def __init__(self, directory='./', picture_file_prefix='material', footer=None):
        self.directory = directory
        self.picture_file_prefix = picture_file_prefix
        self.footer = footer

    def process_image(self, image_file, number):
        # Watermark picture with number
        main = Image.open(image_file)
        watermark = Image.new("RGBA", main.size)
        waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
        waterdraw.text((40, 40), str(number), font=ImageFont.truetype("SignPainter.ttf", 85))
        if self.footer:
            waterdraw.text((1125, 980), self.footer, font=ImageFont.truetype("SignPainter.ttf", 65))
        main.paste(watermark, None, watermark)
        main.save("export/" + image_file, "JPEG")

    def watermark_number(self, file_name):
        # choose middle number from file name
        # '[picture_file_prefix]-1-2.jpg' or '[picture_file_prefix]-1.jpg' files
        l = file_name.split('-')
        if len(l) == 3:
            return l[1]
        elif len(l) == 2:
            return l[1].split('.')[0]

    def call(self):
        all_files = os.listdir(self.directory)
        image_files = [i for i in all_files if i.endswith('.jpg') and i.startswith(self.picture_file_prefix)]
        if not os.path.exists('export'):
            os.makedirs('export')
        for image_file in sorted(image_files):
            print "Processing image: " + image_file
            watermark = self.watermark_number(image_file)
            self.process_image(image_file, watermark)
        print 'Watermarked ' + str(len(image_files)) + ' files.'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Picture Watermarker')
    parser.add_argument('picture_start_number', metavar='start', nargs=1, help='picture start number i.e 1', type=int)
    parser.add_argument('picture_end_number', metavar='end', nargs=1, help='picture start number i.e 29', type=int)
    parser.add_argument('--dir', metavar='D', nargs='?', help='images directory', default='./')
    parser.add_argument('--file_prefix', metavar='prefix', nargs='?', help='picture file prefix. i.e: material', default='material')
    parser.add_argument('--image_extension', metavar='ext', nargs='?', help='pictures extension. i.e: .jpg', default='jpg', choices=['jpg', 'png'])
    parser.add_argument('--footer', metavar='footer', nargs='?', help='image footer i.e: www.example.com')

    args = parser.parse_args()

    print "-- Picture Watermarker v1.0 --"
    print "Use -h for help. \n"
    for k,v in sorted(args.__dict__.iteritems()):
        print "{0}: {1}".format(k,v)

    answer = raw_input('\nProceed with presented arguments? [y\\n]')
    if answer.strip().lower() == 'y':
        print args
        organizer = PictureOrganizer(
            directory = args.dir,
            picture_file_prefix = args.file_prefix,
            file_extension = '.' + args.image_extension,
            options={
                'picture_start_number': args.picture_start_number[0],
                'picture_end_number': args.picture_end_number[0]
            }
        )
        organizer.organize()

        watermarker_args = {
            'directory': args.dir,
            'picture_file_prefix': args.file_prefix
        }

        if args.footer:
            watermarker_args['footer'] = args.footer

        watermark = PictureWatermarker(**watermarker_args)
        watermark.call()
    else:
        sys.exit()
