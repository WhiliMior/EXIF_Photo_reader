import exifread
import csv
import os

filename = "shot_log.csv"
folder = 'PHOTO'

index = ['EXIF ExposureTime', 'EXIF FNumber', 'EXIF ISOSpeedRatings', 'EXIF BrightnessValue',
         'EXIF WhiteBalance', 'EXIF FocalLength', 'EXIF FocalLengthIn35mmFilm']
index_replaced = []
for element in index:
    key = element.replace('EXIF ', '')
    index_replaced.append(key)
header = ['FileName'] + index_replaced + ['Date', 'Time']
# delete the EXIF in index and write them into a header

with open(filename, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)


def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            return None
        try:
            leading, num = num.split(' ')
        except ValueError:
            return float(num) / float(denom)
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return float(leading) + sign_mult * (float(num) / float(denom))


g = os.walk(folder)

for path, dir_list, file_list in g:
    for file_name in file_list:
        file = os.path.join(path, file_name)
        # Open image file for reading (must be in binary mode)
        f = open(file, 'rb')

        # Return Exif tags
        tags = exifread.process_file(f)

        content = [file_name]

        for element in index:
            for tag in tags.keys():
                if tag == element:
                    value = tags[tag]
                    value = str(value)
                    if tag == 'EXIF ExposureTime':
                        value = ' ' + value
                    if tag == 'EXIF BrightnessValue':
                        value = '=' + value
                        # Add a '=' so excel will calculate the value instead of an error
                    if tag == 'EXIF FNumber':
                        value = convert_to_float(value)
                    content.append(str(value))
        # Walk through all elements in index and get information from EXIF

        for tag in tags.keys():
            if tag == 'EXIF DateTimeOriginal':
                value = tags[tag]
                value = str(value).replace(':', '/')[6:10]
                content.append(str(value))
        # Add Date, make it standard formatted

        for tag in tags.keys():
            if tag == 'EXIF DateTimeOriginal':
                value = tags[tag]
                value = str(value)[-8:]
                content.append(str(value))
        # Add Time

        # {content} is all information for one photo
        with open(filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(content)
