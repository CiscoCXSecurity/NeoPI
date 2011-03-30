#What is NeoPI?
NeoPI is a Python script that uses a variety of statistical methods to detect obfuscated and encrypted content within text/script files. The intended purpose of NeoPI is to aid in the detection of hidden web shell code. The development focus of NeoPI was creating a tool that could be used in conjunction with other established detection methods such as Linux Malware Detect or traditional signature/keyword based searches.

NeoPI is platform independent and can be run on any system with Python 2.6 installed. The user running the script should have read access to all of the files that will be scanned.

NeoPI recursively scans through the file system from a base directory and will rank files based on the results of  a number of tests. It also presents a “general” score derived from file rankings within the individual tests.

#How to use it

NeoPI is platform independent and will run on both Linux and Windows.  To start using NeoPI first checkout the code from our github repository

	git clone ssh://git@github.com:Neohapsis/NeoPI.git

The small NeoPI script is now in your local directory.  We are going to go though a few examples on Linux and then switch over to Windows.  

Let’s run neopi.py with the -h flag to see the options.  

	[sbehrens@WebServer2 opt]$ ./neopi.py -h
	Usage: neopi.py [options] <start directory> <OPTIONAL: filename regex>

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -C FILECSV, --csv=FILECSV
							generate CSV outfile
	  -a, --all             Run all tests [Entropy, Longest Word, Compression
	  -e, --entropy         Run entropy Test
	  -l, --longestword     Run longest word test
	  -c, --ic              Run IC test
	  -A, --auto            Run auto file extension tests

Let’s break down the options into greater detail.

	-C FILECSV, --csv=FILECSV
This generates a CSV output file containing the results of the scan.  

	-a, --all
This runs all tests including entropy, longest word, and index of coincidence.  In general, we suggest running all tests to build the most comprehensive list of possible web shells.

	-e, --entropy
This flag can be set to run only the entropy test.  

	-l, --longestword
This flag can be set to run only the longest word test.  

	-c, --ic
This flag can be set to run only the Index of Coincidence test.  

	-A, --auto 
This flag runs an auto generated regular expression that contains many common web application file extensions.    This list is by no means comprehensive but does include a good ‘best effort’ scan if you are unsure of what web application languages your server is running.  The current list of  extensions are included below:

	valid_regex = re.compile('\.php|\.asp|\.aspx|\.sh|\.bash|\.zsh|\.csh|\.tsch|\.pl|\.py|\.txt|\.cgi|\.cfm')

Now that we are familiar with the flags and we have downloaded a copy of the script from GIT, let’s go head and run it on a web server we think may be infected with obfuscated web shells.    

	[sbehrens@WebServer2 opt]$ sudo ./neopi.py -C scan1.csv -a -A /var/www/

##Windows
The tool is cross compatible with windows as well.    In the example below we use a regular expressing to just search for php and text files.

	python neopi.py -a c:\temp\phpbb "php|txt"

