# This is a module designed to filter CSV data provided by Alloy
# This script is written for the use of APIAVote-Michigan
# Thus, the code might have to be changed.


import csv # standard library module for reading CSV files

from sys import getsizeof

# Queries
def registered_voter(row : dict) -> bool:
	''' Checks the alloy_registration_status field to see if it has a "Active" value 
	'''
	return row['alloy_registration_status'] == "Active" if 'alloy_registration_status' in row.keys() else False 

def unregistered_voter(row : dict) -> bool:
	''' Checks the alloy_registration_status field to see if it has a "Not Registered" value 
	'''
	return row['alloy_registration_status'] != "Active" if 'alloy_registration_status' in row.keys() else False 

def aapi(row : dict, other : bool=True) -> bool:
	''' If Asian American and Pacific Islander'''
		
	ethnic_groups = ['B', 'C', 'D', 'H', 'N']		
		
	if other:
		ethnic_groups += ['Z', '']	

	return row['ethnic_group'] in ethnic_groups


def unregistered_aapi(row : dict) -> bool:
	''' If Asian American and Pacific Islander'''
	return aapi(row) and unregistered_voter(row)		
		


def registered_aapi(row : dict) -> bool:
	''' If Asian American and Pacific Islander'''
	return aapi(row) and registered_voter(row)		

# Wrapper for processing individual files...
def create_filtered_alloy(alloy_reader : csv.DictReader, file_name : str, field_names: [str],  query : callable):
	''' Essentially recreates an SQL query... 
		
		file_name - what you want to name the resultant file
		field_names - which fields you want in the data
		query - filter even further by checking the field values

		ex query: row['alloy_registration_status']
	'''
	print(alloy_reader)
	print(query)
	
	with open(file_name, 'w', newline='') as filtered_alloy_file:
		i = 0
		for row in alloy_reader:
			if i == 0:
				alloy_writer = csv.DictWriter(filtered_alloy_file, fieldnames=fieldnames, extrasaction='ignore')
				alloy_writer.writeheader()
			
			if query(row):
				alloy_writer.writerow(row)	
			
			print("Processed person {} for {}. Please wait.".format(i, file_name))
			i+=1

	print("Finished {}".format(file_name))
	print()	

if __name__ == '__main__':
	# Take a CSV file and filter out everyone except unregistered voters.
	# Make a new CSV file with only registered voters.
	filename = "API_20200911013006_core_vote_mi.csv"
	
	with open(filename, newline='') as alloy_csv:
		alloy_reader = csv.DictReader(alloy_csv)
	
		# added to reduce the columns in the excel chart of Alloy data to be more relevant
		# in this particular dataset, having three phone numbers seemed best
		# there were barely any second addresses provided...
		name = ['name_first', 'name_middle', 'name_last'] 
		phone_number = ['phone1_number', 'phone2_number', 'phone3_number']
		address = ['mailing_address_line_1', 'mailing_address_line_2', 'mailing_city', 'mailing_state', 'mailing_zip_code']
		ethnicity = ['ethnic_group']
		registration = ['alloy_registration_status']
		fieldnames = name + phone_number + address + ethnicity + registration	
		
		'''
		with open('filtered_alloy.csv', 'w', newline='') as filtered_alloy_csv:
			i = 0
	
			for row in alloy_reader:
				if i == 0:			
					alloy_writer = csv.DictWriter(filtered_alloy_csv, fieldnames=row.keys())
					alloy_writer.writeheader()
			
				if registered_voter(row):
					alloy_writer.writerow(row)	
			
				print("Processed person {}. Please wait.".format(i))
				i+=1
		'''
		# creates a spreadsheet of all registered voters
		# create_filtered_alloy(alloy_reader, 'registered_all.csv', fieldnames, registered_voter)
		
		# creates a spreadsheet of all unregistered voters
		# create_filtered_alloy(alloy_reader, 'unregistered_all.csv', fieldnames, unregistered_voter)

		# creates a spreadsheet of all unregistered AAPI voters
		# create_filtered_alloy(alloy_reader, 'unegistered_aapi.csv', fieldnames, unregistered_aapi)

		# creates a spreadsheet of all registed AAPI voters
		# create_filtered_alloy(alloy_reader, 'registered_aapi.csv', fieldnames, registered_aapi)

	
		


