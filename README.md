# DNASU-Sequence-extractor
Python code to extract many plasmid sequences providing the ID of the plasmid in a CSV file.


"""
Version 1.0 - 5 of september 2016.

This script extracts plasmids sequences from DNASU. Takes a CSV file with a plasmid ID
in each row, and returns a new file with each plasmid sequence in the same position.

The script is far from error-proof. It considers blank spaces in the csv, but other than that,
it doesn't consider the possibility of various results in the DNASU Search, for example.

By default the input file name is "DNASU_IDS.csv" (Place it in the Python working directory before
exceuting the script). 
In line 77 you can modify the input file name. The output file name is DNASU_out.csv, again,you can 
modify it in line 79.

"""
