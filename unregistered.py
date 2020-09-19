# This is a module designed to filter CSV data provided by Alloy
# This script is written for the use of APIAVote-Michigan
# Thus, the code might have to be changed.


import csv # standard library module for reading CSV files


# Take a CSV file and filter out everyone except unregistered voters.
# Make a new CSV file with only registered voters.
filename = "API_20200911013006_core_vote_mi.csv"

with open(filename, newline='') as alloy_csv:
	alloy_reader = csv.DictReader(alloy_csv)
	
	with open('filtered_alloy.csv', 'w', newline='') as filtered_alloy_csv:
		i = 0
	
		for row in alloy_reader:
			if i == 0:			
				alloy_writer = csv.DictWriter(filtered_alloy_csv, fieldnames=row.keys())
				alloy_writer.writeheader()
			
			if row['alloy_registration_status'] == "Not Registered":
				alloy_writer.writerow(row)	
			
			print("Processed person {}. Please wait.".format(i))
			i+=1
			
print("Done")	
		


