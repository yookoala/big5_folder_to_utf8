big5_folder_to_utf8
===================

Converts all files in the "from folder" to utf8 and store in the 
"to folder"



README
------

This script accept 2 arguments: from folder and to folder

 e.g. ./big5_folder_to_utf8.py from/folder to/folder

The script will:
1. walk the from folder
2. automatically convert text files in from folder from BIG5 to UTF8
3. put the resulting file in to folder, with the excact same folder 
   structure

In the convertion, there maybe some non-standard BIG5 files in between.
The script will warn you, then it will use the 'replace' (add U+FFFD, 
"REPLACEMENT CHARACTER") mode to handle them. It tries to work its best
to convert everyone of them.

Note that this script do not handle the filenames encoding yet.
It only handle the contents.


