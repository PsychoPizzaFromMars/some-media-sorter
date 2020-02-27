import os
import sys
import time
import piexif
import shutil
import argparse

class MediaSortObj:
    def __init__(self, ext):
        self.extension = ext
        self.items_list = []
    
    def _date_format(self, date, style):  
        if style == 'month':
            if date[5:7] == '00':
                date = date[:5] + 'undated'
            else:
                pass
            # "2019-01"

        elif style == 'year':
            if date[5:7] == '00':
                date = date[:5] + 'undated'
            else:
                date = date[:4]
            # "2019"
        return date

    def sort(self, files, targetname='Sorted', style='year', outputdir=None):
        if __name__ == '__main__' and outputdir == None:
            outputdir = os.getcwd() + f'\\{targetname}'
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
        os.chdir(outputdir)
        for file in files:
            print(file, '                                        ', end='\r')
            if os.path.isfile(file):
                try:
                    pic = piexif.load(file)
                except Exception:
                    date_exif = None
                else:
                    date_exif = None

                    for i in ("0th", "Exif", "GPS", "1st"):
                        for tag in pic[i]:

                            if ((piexif.TAGS[i][tag]["name"]=="DateTime") or ((piexif.TAGS[i][tag]["name"]=="DateTimeOriginal"))):
                                date_exif=pic[i][tag]
                        
                if date_exif == None:
                    t = time.localtime(os.path.getmtime(file))
                    date = time.strftime('%Y-%m-%d', t)
                    date = date[:7]
                    date = self._date_format(date, style)
                else:
                    date_exif = date_exif.decode("utf-8")
                    date_exif = date_exif[:7]
                    date_exif = date_exif.replace(":", "-")
                    date = date_exif
                    date = self._date_format(date, style)
                    
                # Copy files to sorting directories
                if not os.path.exists(date):
                    os.mkdir(date)
                if not os.path.exists(date + "/" + os.path.basename(file)):
                    shutil.move(file, date + "/" + os.path.basename(file))

if __name__ == '__main__':
    descStr = "This program sorts media files of different extensions by EXIF and system date tags"
    parser = argparse.ArgumentParser(description=descStr)

    parser.add_argument('extensions', help='extensions you want to sort as \".ext1 .ext2 .ext3 ... .extN\"')
    parser.add_argument('inputDir', help='Path to target media files')
    parser.add_argument('outputDir', help='Path to sorted media files')  
    parser.add_argument('--dformat', dest='dateFormat', required=False, help='defines sorting dirs - \"year\"(default) or \"month\"')

    args = parser.parse_args()

    directory = args.inputDir
    outputdir = args.outputDir
    extensions = tuple(args.extensions.split())

    target_items = MediaSortObj(extensions)
    media_list = target_items.items_list
   
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(target_items.extension):
                media_list.append(os.path.join(root, file))
    target_items.sort(media_list, outputdir=outputdir, style=args.dateFormat)


