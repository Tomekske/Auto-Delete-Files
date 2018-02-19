#=======================================================================#
#Title				:Auto-Delete										#
#Description		:This is a small script where unnecessary			#
#					files and folders are getting deleted				#
#					within a certain folder.							#
# 					All deleted filenames being saved in a file.		#
#					So it's easy to get track of deleted files.			#
#Author				:joostenstomek@gmail.com							#
#Date				:19/02/2016											#
#Version			:1.2												#
#Usage				:Python												#
#Python version		:3.5												#
#=======================================================================#

import glob			#import glob module
import os			#import os module
import pathlib		#import filesystem module
import configparser
import re
import logging
import shutil

##
## @brief      Get filenames in directory 
## @param      root        The root folder where deletion takes place
## @param      folders     Check for folder deletion
## @param      extensions  The file extensions which have to be deleted
## @return     None
##
def getFilesNames(root, folders, extensions):
	for name in os.listdir(root): #searching for all files with specific extension
		#Check if folder have to be delted
		if folders == 'yes':
			if os.path.isdir(name):
				writeToFile('INFO','[{0}] - [{1}]'.format(root, name)) #write foldername to log file
				print('[{0}] - [{1}]'.format(root, name))
				shutil.rmtree(name) #remove folder
		#Loop over every extension
		for extension in extensions:
			if name.endswith(extension): #check for that specific extension
				writeToFile('INFO','[{0}] - [{1}]'.format(root, name)) #write filename to log file
				print('[{0}] - [{1}]'.format(root, name))
				os.unlink(name) #remove filename

##
## @brief      Obtain and format extensions from file
## @param      raw   The raw string containing all the extensions
## @return     List of extensions
##
def formatExtension(raw):
	formated = re.split(r'[,\s]+|,', raw) #split on ',' and space
	#get index via enumerate function and add '.' to extension
	for i, extension in enumerate(formated):
		formated[i] = ".{0}".format(extension) 
	return formated

## @brief      Obtain and format extensions from file
## @param      raw   The raw string containing all the extensions
## @return     List of extensions
##
def formatRootFolder(raw):
	formated = re.split(r'[,\s]+|,', raw) #split on ',' and space
	return formated

##
## @brief      Write log messege to a file
## @param      err   error code
## @param      msg   The message you want to write
## @return     None
##
def writeToFile(err,msg):
	save = config['save']['location'] #get loction where log file is saved
	logging.basicConfig(filename=save,format='[%(levelname)s]%(asctime)s - %(message)s', datefmt='[%d/%m/%Y][%H:%M:%S]',level=logging.DEBUG) #config logfile

	if err == 'INFO':
		logging.info(msg)
	elif err == 'WARNING':
		logging.warning(msg)


#Configure config parser
config = configparser.ConfigParser()
config.read('D:\Programs\Finished\Auto-Delete-Files\config.ini')

#Check if section exsist in config file
check_section_rootfolder = config.has_section('rootfolder')
check_section_fileExtensions = config.has_section('file_extensions')

#section don't exsist and exit program
if not (check_section_rootfolder and check_section_fileExtensions):
	print("Config file doesn't exsist")
	writeToFile('WARNING', "Config file doesn't exsist")
	exit()
#delete folders and files
else:
	root = config['rootfolder']['rootpath']
	print(root)
	root = formatRootFolder(root)
	print(root)
	extensions = config['file_extensions']['extensions']
	folders = config['rootfolder']['folders']
	extensions = formatExtension(extensions)

	#loop over all directories you want to delete
	for r in root:
		os.chdir(r) #change current directory
		getFilesNames(r, folders, extensions)

		