# folderizer
Create a manageable directory structure for large amounts of files.

## Features

### folderize by creation date
Create a one-level deep folder tree with the following format:
```
.
├── _2018.04
│   ├── my_waifu.png
│   └── chin_chin_sacrifice.mp4
├── _2018.07
│   ├── fun_vacation.m4v
│   └── lonely_holiday.webm
├── _2019.12
└───└── more_pics.zip
```
I created this to make it easier to deal with the several thousand images I had in my photo gallery.

### snapshot a directory structure
Save a snapshot of how a given folder tree to a .JSON file and restore from one.\
**Warning**: The file names (`Path.stem(filepath)`) are used as IDs, so if you use it on a folder tree with more than one file with the same file name, you'll lose all files sharing that name except for one of them.

### flatten a nested directory structure
Recursively select all files below a given folder and move them to the root of that folder.

### rename files with their creation date
Get all files inside a folder (non-recursively) and change their names to their creation date in the format: `yyyy.mm.dd HHmm.ext`

## CLI
This is very work-in-progress, but you can use `python script-name.py --help` to check which arguments you need. 
