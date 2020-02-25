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
                date = date[:5] + 'без даты'
            else:
                pass
            # "2019-01"

        elif style == 'year':
            if date[5:7] == '00':
                date = date[:5] + 'без даты'
            else:
                date = date[:4]
            # "2019"
        return date

    def _copysortedfiles(self, dirname, filename, targetfiles='files'):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        if not os.path.exists(dirname + "/" + os.path.basename(filename)):
            shutil.copy2(filename, dirname + "/" + os.path.basename(filename))

    def sort(self, files, targetname='Sorted', style='year', outputdir=None):
        if __name__ == '__main__' and outputdir == None:
            outputdir = os.getcwd() + f'\\{targetname}'
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
        os.chdir(outputdir)
        for file in files:
            print(file, '                 ', end='\r')
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
                    
                self._copysortedfiles(date, file, targetname)

if __name__ == '__main__':
    descStr = "This program sorts media files of different extensions by EXIF and system date tags"
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    # parser.add_argument('--ext', dest='mediaExtensions', required=True)
    # parser.add_argument('--dir', dest='inputDir', required=True)
    # parser.add_argument('--out', dest='outputDir', required=False)
    # parser.add_argument('--dformat', dest='dateFormat', required=False)

    parser.add_argument('extensions')
    parser.add_argument('inputDir')
    parser.add_argument('outputDir')  
    parser.add_argument('--dformat', dest='dateFormat', required=False, help='\'year\' or \'month\'')

    args = parser.parse_args()

    directory = args.inputDir
    outputdir = args.outputDir
    extensions = tuple(args.extensions.split())

    test_item = MediaSortObj(extensions)
    media_list = test_item.items_list
   
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(test_item.extension):
                media_list.append(os.path.join(root, file))
    test_item.sort(media_list, targetname='Test dir 2', outputdir=outputdir)




