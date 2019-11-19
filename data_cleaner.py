#
# Exports a processed version of the 'fullspecs.csv' dataset
#
import pandas as pd
import os

if(__name__ == '__main__'):
	cwd = os.getcwd()							#get current working directory
	fname = cwd + "/car_data/fullspecs.csv"		#create car dataset filename
	attrname = cwd + "/car_data/attrs.txt"		#create car attributes filename
	outname = cwd + "/car_data/proc_cars.csv"
	print("Loading :"+fname)
	cars = pd.read_csv(fname, index_col=0, header=None, dtype = object).T		#transpose of csv for simpler usage
	cars = cars.apply(lambda x: x.astype(object).str.lower())
	print("Done Loading :"+fname)

	print("Processing and Creating: "+outname)
	attrs = [line.rstrip('\n') for line in open(attrname)]						#extract relevant attributes
	cars = cars[attrs]															#remove non-relevant attributes from df
	cars = cars.dropna()														#remove na values

	cars['MSRP'] = cars.MSRP.replace('\D', '', regex=True).astype(int)
	cars['Drivetrain'] = cars['Drivetrain'].replace('[^A-Za-z0-9]+','',regex=True)

	cars.to_csv(outname)														#export processed dataset
	print("Done Processing and Creating: "+outname)