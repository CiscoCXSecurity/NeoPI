#!/usr/bin/python
# Name: neopi.py
# Description: Utility to scan a file path for encrypted and obfuscated files
# Authors: Ben Hagen (ben.hagen@neohapsis.com)
#		   Scott Behrens (scott.behrens@neohapsis.com)
#
# Date: 11/4/2010
# Copyright: Neohapsis Open Source blah Blah
#

# Try catch regular expressions/bad path/bad filename/bad regex/

# Library imports
import math
import sys
import os
import re
import zlib
import csv
from collections import defaultdict
from optparse import OptionParser

class LanguageIC:
	"""Class that calculates a file's Index of Coincidence as
	as well as a a subset of files average Index of Coincidence.
	""" 
	def __init__(self):
		"""Initialize results arrays as well as character counters."""
		self.char_count =  defaultdict(int)
		self.total_char_count = 0
		self.ic_results = []
		self.ic_total_results = ""
	
	def caculate_char_count(self,data):
		"""Method to calculate character counts for a particular data file."""
		if not data:
			return 0
		
		for x in range(256):
			char = chr(x)
			charcount = data.count(char)
			self.char_count[char] += charcount
			self.total_char_count += charcount
		
		return
	
	def caculate_IC(self):
		"""Calculate the Index of Coincidence for the self variables"""
		total = 0
		for val in self.char_count.values():

			if val == 0:
				continue
			total += val * (val-1)
		
		try:
			ic_total =	float(total)/(self.total_char_count * (self.total_char_count - 1))
		except:
			ic_total = 0
		self.ic_total_results = ic_total
		return
	
	def caculate(self,data,filename):
		"""Calculate the Index of Coincidence for a file and append to self.ic_results array"""
		if not data:
			return 0
		char_count = 0
		total_char_count = 0
		
		for x in range(256):
			char = chr(x)
			charcount = data.count(char)
			char_count += charcount * (charcount - 1)
			total_char_count += charcount
		
		ic = float(char_count)/(total_char_count * (total_char_count - 1))
		self.ic_results.append({"filename":filename, "IC":ic})
		# Call method to caculate_char_count and append to total_char_count
		self.caculate_char_count(data)
		return ic
	
	def printer(self):
		"""Print the average IC for searchpath and the top 10 lowest Index of Coincidence files."""
		self.ic_results.sort(key=lambda item: item["IC"])
		top_ten = self.ic_results[0:10]
		# Calculate the Total IC for a Search
		self.caculate_IC()
		ic_list = []
		print ""
		print "[[ Average IC for Search ]]"
		print self.ic_total_results
		print ""
		print "[[ Top 10 IC files ]]"
		x = 9
		for file in top_ten:
			print ' {0:>7.4f}	 {1}'.format(file["IC"], file["filename"])
			results = file["filename"], x
			ic_list.append(results)
			x = x - 1 
		return ic_list

class Entropy:
	"""Class that calculates a file's Entropy."""
	
	def __init__(self):
		"""Instantiate the entropy_results array."""
		self.entropy_results = []
	  
	def caculate(self,data,filename):
		"""Calculate the entropy for 'data' and append result to entropy_results array."""
		
		if not data:
			return 0
		entropy = 0
		for x in range(256):
			p_x = float(data.count(chr(x)))/len(data)
			if p_x > 0:
				entropy += - p_x * math.log(p_x, 2)
		self.entropy_results.append({"filename":filename, "entropy":entropy})
		return entropy
	
	def printer(self):
		"""Print the top 10 entropic files for a given search"""
		self.entropy_results.sort(key=lambda item: item["entropy"])
		top_ten = self.entropy_results[-10:]	
		top_ten.reverse()
		entropy_list = []
		
		print ""
		print "[[ Top 10 entropic files ]]"
		x = 9
		for file in top_ten:
			print ' {0:>7.4f}	 {1}'.format(file["entropy"], file["filename"])
			results = file["filename"], x
			entropy_list.append(results)
			x = x - 1 
		return entropy_list
	
class LongestWord:
	"""Class that determines the longest word for a particular file."""
	def __init__(self):
		"""Instantiate the longestword_results array."""
		self.longestword_results = []
	
	def caculate(self,data,filename):
		"""Find the longest word in a string and append to longestword_results array"""
	
		if not data:
			return "", 0
		
		longest = 0
		longest_word = ""
		words = re.split("[\s,\n,\r]", data)
		if words:
			for word in words:
				length = len(word)
				if length > longest:
					longest = length
					longest_word = word
		self.longestword_results.append({"filename":filename, "wordlongest":longest})
		return longest
	
	def printer(self):
		"""Print the top 10 longest word files for a given search"""
		self.longestword_results.sort(key=lambda item: item["wordlongest"])
		top_ten = self.longestword_results[-10:]
		top_ten.reverse()
		longestword_list = []
		
		print ""
		print "[[ Top 10 longest word files ]]"
		x = 9
		for file in top_ten:
			print ' {0:>7}	  {1}'.format(file["wordlongest"], file["filename"])
			results = file["filename"], x
			longestword_list.append(results)
			x = x - 1 
		return longestword_list
					 
class SearchFile:
	"""Generator that searches a given filepath with an optional regular
	expression and returns the filepath and filename"""	   
	def search_file_path(self, args, valid_regex):
		for root, dirs, files in os.walk(args[0]):
			for file in files:
				filename = os.path.join(root, file)
				if (valid_regex.search(file) and os.path.getsize(filename) > 60):
					try:
						data = open(root + "/" + file, 'rb').read()
					except:
						data = False
						print "Could not read file :: %s/%s" % (root, file)
					yield data, filename 
class PrintRank:
	"""bob"""
	def print_rank(self, top_ten):	
		
		files = defaultdict(int)
		for list in top_ten:
			for file, rank in list:
				files[str(file)] += int(rank)
	
		sorted_top_ten =  sorted(files.items(), key=lambda k: k[1], reverse=True)
		top_ten = sorted_top_ten[0:10]
		print "[[ Highest Rank Files Based on test results ]]"
		# print ' {0:>7}	{1}'.format("Rank", "Filename")
		
		for file in top_ten:
			#print file[0], "%" + 
			print ' {0:>7}	  {1}'.format(str(int((float(file[1])/30) * 100)) + "%", file[0])
			
		return
			  
if __name__ == "__main__":
	"""Parse all the options"""
	parser = OptionParser(usage="usage: %prog [options] <start directory> <OPTIONAL: filename regex>",
						  version="%prog 1.0")
	parser.add_option("-C", "--csv",
					  action="store",
					  dest="is_csv",
					  default=False,
					  help="generate CSV outfile",
					  metavar="FILECSV")
	parser.add_option("-a", "--all",
					  action="store_true",
					  dest="is_all",
					  default=False,
					  help="Run all tests [Entropy, Longest Word, Compression]",)
	parser.add_option("-e", "--entropy",
					  action="store_true",
					  dest="is_entropy",
					  default=False,
					  help="Run entropy Test",)
	parser.add_option("-l", "--longestword",
					  action="store_true",
					  dest="is_longest",
					  default=False,
					  help="Run longest word test",)
	parser.add_option("-c", "--ic",
					  action="store_true",
					  dest="is_ic",
					  default=False,
					  help="Run IC test",)
	parser.add_option("-A", "--auto",
					  action="store_true",
					  dest="is_auto",
					  default=False,
					  help="Run auto file extension tests",)  
			
	(options, args) = parser.parse_args()

	# Error on invalid number of arguements
	if len(args) < 1:
		parser.error("wrong number of arguments")  

	# Error on an invalid path
	if os.path.exists(args[0]) == False:
		parser.error("invalid path")

	valid_regex = ""
	if (len(args) == 2 and options.is_auto is False):
		valid_regex = re.compile(args[1])
	else:
		valid_regex = re.compile('.*')
	tests = []	

	if options.is_auto:
		valid_regex = re.compile('\.php|\.asp|\.aspx|\.sh|\.bash|\.zsh|\.csh|\.tsch|\.pl|\.py|\.txt|\.cgi|\.cfm')

	if options.is_all:
		tests.append(LanguageIC())
		tests.append(Entropy())
		tests.append(LongestWord())		   
	else:
		if options.is_entropy:
			tests.append(Entropy())
		
		if options.is_longest:
			tests.append(LongestWord())
			
		if options.is_ic:
			tests.append(LanguageIC())

	# Instantiate the Generator Class used for searching, opening, and reading files		
	locator = SearchFile()
	
	# CSV file output array
	csv_array = []
	csv_header = ["filename"]

	# Grab the file and calculate each test against file
	for data,filename in locator.search_file_path(args, valid_regex):		 
		if data:
			# a row array for the CSV
			csv_row = []
			csv_row.append(filename)
			for test in tests:
				calculated_value = test.caculate(data,filename)
				# Make the header row if it hasn't been fully populated, +1 here to account for filename column
				if len(csv_header) < len(tests) + 1:
					csv_header.append(test.__class__.__name__)
				csv_row.append(calculated_value)
			csv_array.append(csv_row)

			if options.is_csv:
				csv_array.insert(0,csv_header)
				fileOutput = csv.writer(open(options.is_csv, "wb"))
				fileOutput.writerows(csv_array)

	top_ten = []
	# For each test print the top ten results for that test.  
	for test in tests:
		top_ten.append(test.printer())		
	print ""
	
	printer = PrintRank()
	
	printer.print_rank(top_ten)
	