import os
import shutil
import glob
import cv2
from pdf2image import convert_from_path

def create_directory(f_path):
    if not os.path.exists(f_path):
        os.makedirs(f_path)



def convert_pdf_jpg(f_path, jpg_path):

	# split the file path from path and then split it from extension:
	# /Desktop/file.txt --> file.txt --> file
	f_name = os.path.splitext(os.path.split(f_path)[1])[0]
	out_folder = os.path.join(jpg_path, f_name)
	create_directory(out_folder)

	return convert_from_path(f_path,
		200, 
		output_folder = out_folder, 
		fmt = 'jpg', 
		grayscale=True, 
		thread_count = -1,
		output_file=f_name)

#def preprocess_image():


if __name__ == '__main__':

	# specify data path
	# use os to make it possible for other os file system types
	data_path = os.path.join('data', 'raw')
	jpg_path = os.path.join('data', 'jpg')

	# get list of paths
	list_pdf_names = glob.glob(os.path.join(data_path, '*.pdf'))

	for f_path in list_pdf_names:

		# check if pdf has already been converted or not
		# if not, don't do anything
		f_name = os.path.split(f_path)[1]
		out_jpg_path = os.path.join(jpg_path, f_name)

		f_name_noext = os.path.splitext(os.path.split(f_name)[1])[0]

		# regex string with filename
		re_str = f'{os.path.join(jpg_path, f_name_noext)}*.jpg'

		# if file hasn't been converted, then convert
		if len(glob.glob(re_str)) == 0:
			print(f'Converting {f_name} to .jpg')
			convert_pdf_jpg(f_path, jpg_path)
		else:
			print(f'{f_name} was converted previously!')



	

