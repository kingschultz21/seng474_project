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

	cars = pd.read_csv(fname, index_col=0, header=None, dtype = object).T		#transpose of csv for simpler usage
	attrs = [line.rstrip('\n') for line in open(attrname)]						#extract relevant attributes
	cars = cars[attrs]															#remove non-relevant attributes from df

	cars.to_csv(outname)														#export processed dataset