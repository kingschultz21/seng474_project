#
# Exports a processed version of the 'fullspecs.csv' dataset
#
import pandas as pd
import os

def info_print(ftype, df):
	print("number of rows in "+ftype+" file: "+ str(len(df)))
	print("number of columns in "+ftype+" file: "+str(len(df.columns)))
	print("number of na values in "+ftype+" file: "+str(df.isna().sum().sum()))

def main():
	cwd = os.getcwd()						#get current working directory
	fname = "/car_data/fullspecs.csv"		#create car dataset filename
	attrname = "/car_data/attrs.txt"		#create car attributes filename
	outname = "/car_data/proc_cars.csv"

	print("loading :"+fname)
	cars = pd.read_csv((cwd+fname), index_col=0, header=None, dtype = object).T		#transpose of csv for simpler usage
	cars = cars.apply(lambda x: x.astype(object).str.lower())
	print("done loading :"+fname)
	info_print("input",cars)

	print("processing "+fname+" and creating "+outname)
	attrs = [line.rstrip('\n') for line in open(cwd+attrname)]						#extract relevant attributes
	cars = cars[attrs]																#remove non-relevant attributes from df
	cars = cars.dropna()															#remove na values

	cars['MSRP'] = cars.MSRP.replace('\D', '', regex=True).astype(int)
	cars = cars.replace('[^A-Za-z0-9]+','',regex=True)

	cars.to_csv(cwd+outname)														#export processed dataset
	print("done processing "+fname+" and done creating "+outname)
	info_print("output",cars)

if(__name__ == '__main__'):
	main()