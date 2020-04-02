DESCRIPTION:

	bitmapindex.py will create a bitmap index of a comma separated file of tuples of the schema
				(animal_type, age, adopted)
	The attributes have the following domains: 
		- Animal: [’cat’, ’dog’, ’turtle’, ’bird’] 
		- Age: [1,100]
		- Adopted: [True, False]

	The create_index(input_path, output_path, sorted) function takes in a file of the format above
	and changes the data on each line into bit values for each attribute and outputs a bitmap index
	file. The file is in the following format
		inputFile_<sorted>		where sorted is present if sorted is True.

	The compress_index(bitmap_index, output_path, compression_method, word_size) function takes in a
	bitmap file and compresses it using the specified compression method and word size. 
	**Currently only WAH compression is supported
	The output file is in the following format
		inputFile_<sorted>_<compression>_<wordSize>		where the suffixes are whatever is specified
														by the compression method, word size.


HOW TO RUN:

	add "import bitmapindex.py" to import the function from this file.
	
	This program can take in files from the any directory and will strip the file given of its 
	path