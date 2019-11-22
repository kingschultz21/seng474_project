#
# Exports a processed version of the 'fullspecs.csv' dataset
#

import pandas as pd
import os
import numpy as np
pd.options.mode.chained_assignment = None #supress SettingWithCopyWarning (problematic?)
#
# process 'Drivetrain' attrs and rename column
#
def proc_drivetrain(df):
	df = df.replace('frontwheeldrive', 'fwd')
	df = df.replace('rearwheeldrive', 'rwd')
	df = df.replace('allwheeldrive', 'awd')
	df = df.replace('4wheeldrive', '4wd')
	df = df.replace('fourwheeldrive', '4wd')
	df = df.replace('2wheeldrive', '2wd')
	df.rename(columns = {'Drivetrain':'DRIVETRAIN'}, inplace = True)
	return df
#
# process 'Engine Type' attrs and rename column
#
def proc_engine(df):
	df = df.replace('regularunleadedv6','gasv6')
	df = df.replace('regularunleadedi4','gasi4')
	df.rename(columns = {'Engine Type':'ENGINE'}, inplace = True) 
	return df
#
# process inherent integer attrs and rename columns
#
def to_int(df):
	attrs = ['MSRP','Passenger Capacity', 'Passenger Doors']
	for attr in attrs:
		df[attr] = df[attr].astype(int)
	df.rename(columns = {attrs[1]:'PASSCAPACITY', attrs[2]:'DOORS'}, inplace = True) 
	return df
#
# process fuel system related attrs and rename columns
#
def proc_fuel(df):
	attrs = ['Fuel Tank Capacity, Approx (gal)','EPA Fuel Economy Est - City (MPG)', 'EPA Fuel Economy Est - Hwy (MPG)']
	for attr in attrs:
		df[attr] = pd.to_numeric(df[attr], errors='coerce')
		df = df.dropna(subset=[attr])
		df[attr] = df[attr].astype(int)
	df.rename(columns = {attrs[0]:'FUELCAPACITY', attrs[1]:'CITYMPG', attrs[2]:'HWYMPG'}, inplace = True) 
	return df
#
# process dimension related attrs and rename columns
# TODO: fix diz shit cuz it be fucky
#
def proc_measurements(df):
	attrs = ['Wheelbase (in)','Width, Max w/o mirrors (in)', 'Height, Overall (in)', 'Displacement']
	for attr in attrs:
		df[attr] = df[attr].replace('\D.','',regex=True)
		df[attr] = pd.to_numeric(df[attr], errors='coerce')
		df = df.dropna(subset=[attr])
		if(attr == 'Displacement'):
			df[attr] = (df[attr]/100.0).astype(float)
		else:
			df[attr] = df[attr].astype(float)
			
	df.rename(columns = {attrs[0]:'WHEELBASE', attrs[1]:'WIDTH', 
						 attrs[2]:'HEIGHT', attrs[3]: 'DISPLACEMENT'}, inplace = True) 
	return df
#
# process spec related attrs and rename columns
#
def proc_hptorq(df):
	attrs = ['SAE Net Horsepower @ RPM', 'SAE Net Torque @ RPM']
	for attr in attrs:
		df[attr] = pd.to_numeric(df[attr], errors='coerce')
		df = df.dropna(subset=[attr])
		df[attr] = df[attr].astype(str).apply(lambda x: x[:3]).astype(int)				
	df.rename(columns = {attrs[0]:'HORSEPOWER', attrs[1]:'TORQUE'}, inplace = True) 
	return df
#
# process misc attrs and rename columns
#
def proc_misc(df):
	attrs = ['Body Style', 'Transmission']
	df.rename(columns = {attrs[0]:'BODYSTYLE', attrs[1]:'TRANSMISSION'}, inplace = True)
	return df
#
# process binary attrs and rename columns
#
def proc_binary(df):
	attrs = ['Air Bag-Frontal-Driver','Air Bag-Frontal-Passenger','Air Bag-Passenger Switch (On/Off)',
				'Air Bag-Side Body-Front', 'Air Bag-Side Body-Rear', 'Air Bag-Side Head-Front',
				'Air Bag-Side Head-Rear', 'Brakes-ABS', 'Child Safety Rear Door Locks',
				'Daytime Running Lights', 'Traction Control', 'Night Vision',
				'Rollover Protection Bars', 'Fog Lamps', 'Parking Aid','Tire Pressure Monitor',
				'Back-Up Camera', 'Stability Control']
	df = df.replace('yes', '1')
	df = df.replace('no', '0')

	for attr in attrs:
		df[attr] = pd.to_numeric(df[attr], errors='coerce')
		df = df.dropna(subset=[attr])
		df[attr] = df[attr].astype(int)

	df.rename(columns = {attrs[0]:'AIRBAGFRONTDRIVER', attrs[1]:'AIRBAGFRONTPASS',
						 attrs[2]:'AIRBAGSWITCH', attrs[3]:'AIRBAGSIDEBODYFRONT',
						 attrs[4]:'AIRBAGSIDEBODYREAR', attrs[5]:'AIRBAGSIDEHEADFRONT',
						 attrs[6]:'AIRBAGSIDEHEADREAR', attrs[7]:'ABS',
						 attrs[8]:'CHILDSAFETYLOCK', attrs[9]:'DAYTIMERUNLIGHTS',
						 attrs[10]:'TRACCONTROL', attrs[11]:'NIGHTVISION',
						 attrs[12]:'ROLLOVERBARS', attrs[13]:'FOGLAMPS',
						 attrs[14]:'PARKINGAID', attrs[15]:'TPS',
						 attrs[16]:'BACKUPCAM', attrs[17]:'STABCONTROL'}, inplace = True) 
	return df
#
# main controller
#
def process_cars(df):
	df = proc_drivetrain(df)
	df = proc_engine(df)
	df = to_int(df)
	df = proc_measurements(df) #TODO: fix!
	df = proc_fuel(df)
	df = proc_hptorq(df)
	df = proc_misc(df)
	df = proc_binary(df)
	return df
#
# creates a new binary column for each value of each attribute:
#	-> ie: DRIVETRAIN becomes:
#			-> DRIVETRAIN_fwd (0, 1)
#			-> DRIVETRAIN_rwd (0, 1)
#			-> DRIVETRAIN_awd (0, 1)
#				etc ...
#
def binary_encode(df):
	cat_attrs = ['DRIVETRAIN','BODYSTYLE','TRANSMISSION','ENGINE']
	df = pd.get_dummies(df, columns=cat_attrs, prefix=cat_attrs)
	return df
#
# creates a new label column for each attribute:
#	-> ie: DRIVETRAIN becomes:
#			-> DRIVETRAIN_CAT (0, 1, ... , n)
#				where n is the number of unique values for a given attribute
#
def label_encode(df):
	cat_attrs = ['DRIVETRAIN','BODYSTYLE','TRANSMISSION','ENGINE']
	for attr in cat_attrs:
		df[attr] = df[attr].astype('category')
		df[attr+'_CAT'] = df[attr].cat.codes
	return df
#
# remove infrequent values
#
def threshold(df, t):
	for col in df.columns:
		value_counts = df[col].value_counts()
		to_remove = value_counts[value_counts <= t].index.values
		df[col].loc[df[col].isin(to_remove)] = np.nan
		df = df.dropna()
	return df
#
# print basic info about dateframes (csv's)
#
def info_print(ftype, df):
	print("number of rows in "+ftype+" file: "+ str(len(df)))
	print("number of columns in "+ftype+" file: "+str(len(df.columns)))
	print("number of na values in "+ftype+" file: "+str(df.isna().sum().sum()))
#
# 
# data_cleaner.py: converts the original 'fullspecs.csv' dataset into a usable format for regression
#
#
def main():
	cwd = os.getcwd()																#get current working directory
	fname = "/car_data/fullspecs.csv"												#create car dataset filename
	attrname = "/car_data/attrs.txt"												#create car attributes filename
	outname = "/car_data/proc_cars.csv"												#create output dataset filename

	print("LOADING :"+fname)
	cars = pd.read_csv((cwd+fname), index_col=0, header=None, dtype = object).T		#transpose of csv for simpler usage
	cars = cars.apply(lambda x: x.astype(object).str.lower())						#convert everything to lower case
	print("DONE LOADING :"+fname)

	info_print("input",cars)
	print("PROCESSING: "+fname+" and CREATING: "+outname)
	attrs = [line.rstrip('\n') for line in open(cwd+attrname)]						#extract relevant attributes
	cars = cars[attrs]																#remove non-relevant attributes from df
	cars = cars.dropna()															#remove na values
	cars = cars.replace('[^A-Za-z0-9.]+','',regex=True)								#remove special characters

	cars = process_cars(cars)														#process cars!
	print("DONE PROCESSING: "+fname)

	print("ENCODING: "+outname)
	#cars = binary_encode(cars)														#binary encoding scheme
	cars = label_encode(cars)														#label endcoding scheme
	print("DONE ENCODING: "+outname)

	cars = threshold(cars, 2)														#threshold based on value
	cars.to_csv(cwd+outname)														#export processed dataset
	print("DONE CREATING: "+outname)
	info_print("output",cars)

if(__name__ == '__main__'):
	main()