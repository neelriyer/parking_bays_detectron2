import re
import json
import pandas as pd
import numpy as np 
import ast
import uuid
import os

existing_csv = '/Users/neeliyer/Documents/SPOT/parking_bay_detection/train/export-2020-01-13T00-58-16.590Z.csv'
new_data_path = '/Users/neeliyer/Documents/SPOT/parking_bay_detection/train/generated_data/data.json'
output_path = '/Users/neeliyer/Documents/SPOT/parking_bay_detection/train/detectron2_labels_with_new_data_added.csv'


def form_geometry_dict(Bays, Disabled):

	if(Bays == [] and Disabled == []):
		geometry_dict = {}

	elif (Bays != [] and Disabled == []):
		geometry_dict = {'Bay': Bays}

	elif (Bays == [] and Disabled != []):
		geometry_dict = {'Disabled Bay': Disabled}

	else:
		geometry_dict = {'Bay': Bays, 'Disabled Bay': Disabled}

	return geometry_dict 


# takes in poly list and category list and reformats data appropriately
def poly_list_to_geometry_dict(poly_list, category_list):	

	Bays = []
	Disabled = []
	
	# iterate over parking space
	for i in range(len(poly_list)):

		bay = poly_list[i]

		# reinit geometry list
		geometry_list = []

		# get category
		category = category_list[i]

		# iterate over points in parking space
		for x,y in bay:
			
			# create dict
			point_dict = {'x':x, 'y':y}

			# append to geometry list
			geometry_list.append(point_dict)

		# once space is completed read into geometry dict
		geometry_dict = {\
			'geometry': geometry_list
		}

		if(category == 'Parking Bay'):
			Bays.append(geometry_dict)
		elif(category == 'Disabled Parking'):
			Disabled.append(geometry_dict)
		else:
			sys.exit( str(category)+" is invalid. Expected Parking Bay or Disabled Parking")

	# print(Bays)
	# print(Disabled)

	# form geometry dict
	geometry_dict = form_geometry_dict(Bays, Disabled)

	return geometry_dict

def groupby_geometry_dict(df):

	df['geometry_dict'] = df['geometry_dict'].apply(lambda text: [text])
	df = df.groupby(['filename', 'category']).agg({'geometry_dict': 'sum', \
									'filename': 'first', \
									'category': 'first'})

	return df

def add_bay_prefix(df):

	for index, row in df.iterrows():

		category = row['category']
		geometry_dict = row['geometry_dict']

		# print(category)
		# print(geometry_dict)

		if (category == 'Bay'):

			return_dict = {'Bay': geometry_dict}

		elif(category == 'Disabled'):

			return_dict = {'Disabled': geometry_dict}

		row['geometry_dict'] = return_dict

	return df


def combined_bay_disabled(df):

	# convert to str
	df['geometry_dict'] = df['geometry_dict'].astype(str)

	# groupy filename and str concat geometry dict col
	df = df.groupby('filename').agg({'geometry_dict':'sum'})

	# copy filename
	df['filename'] = df.index

	# reindex
	df.index = range(len(df))

	# combined bay and disabled bay dicts
	df['geometry_dict'] = df['geometry_dict'].apply(lambda text: text.replace('}{', ', '))

	return df


data_dict = pd.read_json(new_data_path)


df = pd.DataFrame()

for i in data_dict['annotations']:
	# print(i)

	# get filename
	filename = i['file_name']

	# get poly list and category
	poly_list = i['poly']
	category = i['category']

	# convert poly list to geometry dict
	geometry_dict = poly_list_to_geometry_dict(poly_list, category)
	print(geometry_dict)

	# form df2
	df2 = pd.DataFrame({
			'filename': filename, 
			'geometry_dict': str(geometry_dict)
			}, index = [0])

	# append to final df
	df = df.append(df2, ignore_index = True)

print(df.head())


# groupby
# df = groupby_geometry_dict(df)
# df.index = range(len(df))
# # print(df)

# # add Bay or Disabled Bay prefix
# df = add_bay_prefix(df)

# # combined bay and disabled in one dict
# df = combined_bay_disabled(df)
# # print(df['geometry_dict'][0])
# # print(df.head())


# covnert to json
df['geometry_dict'] = df['geometry_dict'].apply(lambda text: ast.literal_eval(text))
df['Label'] = df['geometry_dict'].apply(lambda x: json.dumps(x))
print(df.head())

# make new cols
df['ID'] = 'test'
df['ID'] = df['ID'].apply(lambda text: uuid.uuid4())
df['External ID'] = df['filename']

# drop cols
df = df.drop(['geometry_dict', 'filename'], axis = 1)

# read existing csv file
df2 = pd.read_csv(existing_csv)
df2 = df2[['Label', 'ID', 'External ID']]

# append existing csv with additional csv
df = df.append(df2, ignore_index = True)
print(df.head())

df = df[['ID', 'Label', 'External ID']]

# remove csv if file exists
if os.path.exists(output_path):
	os.remove(output_path)

# write to csv
print(df['Label'].head(50))
# df.to_csv('dataset_with_json_column_and_id_added.csv', header=True, index=None, sep=',', mode='a', quoting = csv.QUOTE_NONE,escapechar='\\')
df.to_csv(output_path, header=True, index=None, sep=',', mode='a')

check = df[df['Label']!='Skip']
print(len(check))



