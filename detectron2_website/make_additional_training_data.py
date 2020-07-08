"""
script to make additional training data from dataset given
run convert_predictions_to_useable_training_data.py first


TODO: make modular
add facility for disabled parkinglots
"""
import cv2
import glob
import pandas as pd
import json
import uuid
import os
import shutil


X_MOVE = 100
Y_MOVE = 0

data_path = '/Users/neeliyer/Documents/SPOT/parking_bay_detection/train/detectron2_labels_with_new_data_added.csv'
img_dir = '/Users/neeliyer/Documents/SPOT/parking_bay_detection/train/'

images = glob.glob(img_dir+'*.*g')
# print(images)

df = pd.read_csv(data_path)
final_df = pd.DataFrame()
# print(df.head())


# delete entire augmented images folder
try:
	shutil.rmtree(img_dir+'augmented_data')
except:
	pass
try:
	os.mkdir(img_dir+'augmented_data')
except:
	pass

for image in images:

	# get particular image name
	image_name = image.split('/')[-1]
	new_df = df[df['External ID']==image_name].reset_index()

	# if empty move one
	if(new_df.empty or new_df['Label'][0] == 'Skip'):
		continue

	# print(image_name)

	img = cv2.imread(image)
	crop_img = img[:, X_MOVE:]
	cv2.waitKey(0)

	print(new_df)

	# get json payload
	data = json.loads(new_df['Label'][0])

	if('Bay' in data.keys()):

		# copy data cross 
		new_data = {'Bay': []}
		# print(new_data)

		# reduce all x coords by X_MOVE
		for i in range(len(data['Bay'])):

			bay = data['Bay'][i]

			geometry_list = []

			for j in range(len(bay['geometry'])):

				coords = bay['geometry'][j]

				x = coords['x']
				y = coords['y']

				# change x coord
				new_x = x - X_MOVE
				new_y = y - Y_MOVE

				# print(new_x)

				# point dict
				point_dict = {'x':new_x, 'y':new_y}

				# append to geometry_list
				if(new_x > 0 and new_y > 0):
					geometry_list.append(point_dict)

				else:

					geometry_list = []
					print('we break here')
					print(str(i)+' vs ' + str(len(data['Bay'])))

					# got to next parking bay
					break
			
			if(len(geometry_list)>0):
				geometry_dict = {'geometry': geometry_list}	

			# append to new_data
			new_data['Bay'] = new_data['Bay'] + [geometry_dict]

	# print(new_data['Bay'])		


	# convert to json again
	new_data_json = json.dumps(new_data)

	# get unique filename
	filename = str(uuid.uuid4()) + '.png'
	destination_location = img_dir+'augmented_data/'+filename

	# save image
	cv2.imwrite(destination_location, crop_img)

	# put label back in existing df
	df2 = pd.DataFrame({
				'ID': str(uuid.uuid4()),
				'Label': str(new_data_json), 
				'External ID': filename 
				}, index = [0])

	# append to df
	final_df = final_df.append(df2, ignore_index = True)


print(final_df.tail())


output_path = img_dir +'augmented_data/detectron2_labels_with_new_data_added_with_augmentation.csv'

# remove csv if file exists
if os.path.exists(output_path):
	os.remove(output_path)

final_df.to_csv(output_path, header=True, index=None, sep=',', mode='a')

check = final_df[final_df['Label']!='Skip']
print(len(check))


