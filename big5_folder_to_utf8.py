#!/usr/bin/env python

"""

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

"""

import sys
import os
import re
import time


class Converter:

  
  def __init__(self):
    self.subdirs = list()


  def storeSubdir(self, subdir):
    
    if subdir != '' and self.subdirs.count(subdir) == 0:
      
      # store the subdirectory
      self.subdirs.append(subdir)
      
      # split the subdirectory and try to store
      # any unstored ones
      head, tail = os.path.split(subdir)
      self.storeSubdir(head)


  def convertDir(self, from_folder, to_folder):
    
    regex = re.compile('^(' + re.escape(from_folder) + ')[' + os.sep + ']?(.*?)$')
    
    # modify the files, and store all subdirectories names
    for dirname, dirnames, filenames in os.walk(from_folder):
      
      # store directory name
      subdirname = regex.sub('\\2', dirname)
      self.storeSubdir(subdirname)
      
      # store files
      for filename in filenames:
        to_dirname = os.path.join(to_folder, subdirname)
        from_filename = os.path.join(dirname, filename)
        to_filename = os.path.join(to_dirname, filename)

        from_dirstat = os.stat(os.path.join(from_folder, subdirname))
        from_filestat = os.stat(from_filename)
     
        # create directory structure accordingly
        if not os.path.isdir(to_dirname):
          os.makedirs(to_dirname)
          os.chmod(to_dirname, from_dirstat.st_mode)
          if os.getuid() == 0:
            os.chown(to_dirname, from_dirstat.st_uid, from_dirstat.st_gid)

        from_file = open(from_filename, "r")
        to_file = open(to_filename, "w")
        
        from_file_contents = from_file.read()

        try:
          converted = unicode(from_file_contents, 'cp950')
        except Exception as e:
          
          try:
            print "Used 'replace mode' in %s" % from_filename
            converted = unicode(from_file_contents, 'cp950', 'replace')
            pass
          except Exception as e:
            print from_filename, e

          
        to_file.write(converted.encode('utf-8'))
        
        from_file.close()
        to_file.close()

        # modify the permission of new file to match the old one
        os.chmod(to_filename, from_filestat.st_mode)
        os.utime(to_filename, (from_filestat.st_atime, from_filestat.st_mtime))
        if os.getuid() == 0:
          os.chown(to_filename, from_filestat.st_uid, from_filestat.st_gid)

    
    # change all the targeted subfolder names
    for subdirname in self.subdirs: 
      from_dirstat = os.stat(os.path.join(from_folder, subdirname))
      to_dirname = os.path.join(to_folder, subdirname)
      os.utime(to_dirname, (from_dirstat.st_atime, from_dirstat.st_mtime))
    
    # reset the subdirs parameter
    # in case user wants to reuse this instance
    self.subdirs = list()


if __name__ == "__main__":
  from_folder = sys.argv[1]
  to_folder = sys.argv[2]
  converter = Converter()
  converter.convertDir(from_folder, to_folder)



