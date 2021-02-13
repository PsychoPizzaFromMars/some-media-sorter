# some-media-sorter
## Description
Simple script, that you can use from command-line to sort photos using date info from EXIF metadata (or system metadata, if it hasn't one).
## Dependencies
```piexif==1.1.3```
## Usage
- ```python sorter.py "\path\to\media\folder\" "\path\to\output\folder\"``` - sorts photos or other files from ```\path\to\media\folder\``` into ```\path\to\output\folder\```
- ``` python sorter.py -e ".ext1 .ext2 .ext3" -s "\path\to\media\folder\" "\path\to\output\folder\" ``` - sorts files that end with ```".ext1", ".ext2", ".ext3"``` from ```\path\to\media\folder\``` into ```\path\to\output\folder\``` in a safemode (copying, not moving files)
