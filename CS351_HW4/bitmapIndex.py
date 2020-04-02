''' name: Spencer Ross
 	program: 	CS 351 - assignment 4
 				bitmap compression using
 				WAH - Word-Aligned Hybrid 
 				or BBC - Byte-aligned Bitmap 
 				Compression
 	date: 3/30/2020
'''
import os

def main():
	textFile  = "animals.txt"
	bitmapDir = "./bitmaps"
	compreDir = "./compressed"
	wah 	  = "WAH"
	bbc 	  = "BBC"
	word_size = 32

	sorted = True
	bitmap_index = create_index(textFile, bitmapDir, sorted)
	compress_index(bitmap_index, compreDir, wah, word_size)

# os.path.splitext(os.path.basename(input_file))[0] 

''' ‘input_file’ is a file that you will use to create 	the bitmap index. 
	‘output_path’ is the destination for your output bitmap file. It must 
	be a regular file with no suffixes (.txt, .c, etc). ‘sorted’ is a 
	boolean value that specifies whether your data is sorted or not.'''
def create_index(input_file, output_path, sorted):
	textFile = open(input_file, "r") #get file name
	if sorted:
		templist = list()	#list to store changes to data
		templist = sort_file(textFile)
		output_path += '/' + os.path.splitext(os.path.basename(input_file))[0]  + '_sorted'
		bitmap_index	= open(output_path, 'w') #'' for sorted
		List_to_bitmap(templist, bitmap_index)
	else:
		output_path += '/' + os.path.splitext(os.path.basename(input_file))[0]
		bitmap_index = open(output_path, 'w')
		File_to_bitmap(textFile, bitmap_index)
	textFile.close()
	bitmap_index.close()
	return output_path
	

# sorts data in the file given and outputs a list
def sort_file(input_file):
	lines = list()
	for line in input_file:
		lines.append(line.strip())
	lines.sort()
	return lines

''' The two following functions are nearly identical except one takes data 
	from a list and the other takes data from a file, but they convert data 
	into the bitmap index '''
def List_to_bitmap(lines, output_path):
	for line in lines[:-1]:
		tupl = line.replace('\n', '').split(',') #split on comma
		output_path.write(convertTuple(tupl) + '\n')
	#gets rid of xtra \n
	output_path.write(convertTuple(lines[-1].replace('\n', '').split(','))) 

def File_to_bitmap(input_file, output_path):
	lines = input_file.readlines()
	for line in lines[:-1]:
		tupl = line.replace('\n', '').split(',') #split on comma
		output_path.write(convertTuple(tupl) + '\n')
	output_path.write(convertTuple(lines[-1].replace('\n', '').split(',')))



''' ‘bitmap_index’ is the input file that will be used in the compression. 
	‘output_path’is the path to a directory where the compressed version will 
	be written using the naming scheme specified above. ‘compression_method’ 
	is a String specifying which bitmap compression method you will be using 
	(WAH, BBC, PLWAH, etc). ‘word_size’ is an integer specifying the word 
	size to be used.'''
def compress_index(bitmap_index, output_path, compression_method, word_size):
	bitmapFile = open(bitmap_index, 'r')
	if compression_method == 'WAH':
		compress_file = open((output_path + 
								os.path.splitext(os.path.basename(bitmap_index))[0] + 
								'_' + compression_method + '_' + str(word_size)), 
							'w')
	elif compression_method == 'BBC':
		compress_file = open((output_path + 
								os.path.splitext(os.path.basename(bitmap_index))[0] + 
								'_' + compression_method), 
							'w') 
	myTuple = zip(*bitmapFile.readlines())
	rotated	= [''.join(i) for i in myTuple]
	lines 	= list()
	for column in rotated:
		if compression_method == "WAH":
			wah_compression(column, word_size, compress_file)
		elif compression_method == "BBC":
			bbc_compression(column.strip(), compress_file)
	

def wah_compression(column, word_size, output_path):
	literal = ""
	words = ""
	binary_size = "0" + str(word_size - 2) + 'b'
	count0 = 0
	count1 = 0
	runCount = 0 #this is only for assignment report
	litCount = 0 #ditto
	while column:
		word = ""
		if len(column) < word_size:
			litCount += 1
			if count1 > 0:
				word = makeRunWord(1, binary_size, count1)
				words += word
				count1 = 0
			elif count0 > 0:
				word = makeRunWord(0, binary_size, count0)
				words += word
				count0 = 0
			word = "0"
			word += str(''.join(column))
			word += ((word_size - 1) - len(column)) * "0"
			words += word
			break
		#get chunks for literals or runs
		literal = column[:(word_size - 1)]
		column = column[(word_size - 1):]
		if '0' in literal and '1' in literal:
			litCount += 1
			if count1 > 0:
				word = makeRunWord(1, binary_size, count1)
				words += word
				count1 = 0
			elif count0 > 0:
				word = makeRunWord(0, binary_size, count0)
				words += word
				count0 = 0
			word = "0"
			word += literal
			words += word
		else:
			runCount += 1
			if '0' in literal:
				count0 += 1 
				if count1 > 0:
					word = makeRunWord(1, binary_size, count1)
					words += word
					count1 = 0
			else:
				count1 += 1
				if count0 > 0:
					word = makeRunWord(0, binary_size, count0)
					words += word
					count0 = 0
			
	print('+' + str(runCount) + '\n+' + str(litCount) + '\n')
	output_path.write(words + '\n')

#compresses bitmap using bbc algorithm
def bbc_compression(column, output_path):
	pass

#make run or 0's or 1's word
def makeRunWord(type, word_size, count):
	word = "1"
	word += str(type)
	word += format(count, word_size)
	return word



#writes lines to file without additional newline
def listsToFile(lines, output_path):
	for line in lines:
		output_path.write(line + '\n')
	output_path.write(lines[-1])

#converts attributes into binary values
def convertTuple(tupl):
	species = tupl[0]
	age		= int(tupl[1])
	adopted = tupl[2]
	outString = ''
	#put animal attributes into bit value
	if species == 'cat':
		outString += '1000'
	elif species == 'dog':
		outString += '0100'
	elif species == 'turtle':
		outString += '0010'
	elif species == 'bird':
		outString += '0001'
	''' 
	bin ages into sets of 10 years
	1 is min, 100 is max. bin is in 
	1-10, 11-20, ..., 91-100 format'''
	if age in range(11):
		outString += '1000000000'
	elif age in range(11, 21):
		outString += '0100000000'
	elif age in range(21, 31):
		outString += '0010000000'
	elif age in range(31, 41):
		outString += '0001000000'
	elif age in range(41, 51):
		outString += '0000100000'
	elif age in range(51, 61):
		outString += '0000010000'
	elif age in range(61, 71):
		outString += '0000001000'
	elif age in range(71, 81):
		outString += '0000000100'
	elif age in range(81, 91):
		outString += '0000000010'
	elif age in range(91, 101):
		outString += '0000000001'
	#adopted is a boolean value
	if adopted == 'True':
		outString += '10'
	elif adopted == 'False':
		outString += '01'
	return outString


if __name__ == '__main__':
	main()
