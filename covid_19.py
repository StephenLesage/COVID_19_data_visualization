'''

Data source:

https://ourworldindata.org/coronavirus-data

'''

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Functions taken from https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python/13032755
def is_leap_year(year):
    """ if year is a leap year return True
        else return False """
    if year % 100 == 0:
        return year % 400 == 0
    return year % 4 == 0

def doy(Y,M,D):
    """ given year, month, day return day of year
        Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """
    if is_leap_year(Y):
        K = 1
    else:
        K = 2
    N = int((275 * M) / 9.0) - K * int((M + 9) / 12.0) + D - 30
    return N

def ymd(Y,N):
    """ given year = Y and day of year = N, return year, month, day
        Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """    
    if is_leap_year(Y):
        K = 1
    else:
        K = 2
    M = int((9 * (K + N)) / 275.0 + 0.98)
    if N < 32:
        M = 1
    D = N - int((275 * M) / 9.0) + K * int((M + 9) / 12.0) + 30
    return Y, M, D

def plot_queue( covid_data, header, category, specific_category, data_category, x_average ):

	x_axis = []
	x_axis_2019 = []
	x_axis_2020 = []
	x_axis_2021 = []
	y_axis = []
	y_axis_2019 = []
	y_axis_2020 = []
	y_axis_2021 = []

	# Fill arrays to be plotted
	for i in range( len(covid_data) ):
	
		if covid_data[i][ header.index(category) ] == specific_category:
	
			# Manually transform date into DOY
			# NOTE: I could not use "import datetime" because of the weird way the array was read in
			date = covid_data[i][3].split('-')
			day_of_year = doy( int(date[0]), int(date[1]), int(date[2]) )
	
			if int(date[0]) == 2019:
				# If DOY is already in arrays to be plotted, add the data to that existing day
				if day_of_year in x_axis_2019:
					index = x_axis_2019.index(day_of_year)
					y_axis_2019[ index ] += covid_data[i][ header.index(data_category) ]
				# If DOY is NOT already in arrays to be plotted, add it 
				else:
					x_axis_2019.append( day_of_year )
					y_axis_2019.append( covid_data[i][ header.index(data_category) ] )

			if int(date[0]) == 2020:
				# If DOY is already in arrays to be plotted, add the data to that existing day
				if day_of_year in x_axis_2020:
					index = x_axis_2020.index(day_of_year)
					y_axis_2020[ index ] += covid_data[i][ header.index(data_category) ]
				# If DOY is NOT already in arrays to be plotted, add it 
				else:
					x_axis_2020.append( day_of_year )
					y_axis_2020.append( covid_data[i][ header.index(data_category) ] )

			if int(date[0]) == 2021:
				# If DOY is already in arrays to be plotted, add the data to that existing day
				if day_of_year in x_axis_2021:
					index = x_axis_2021.index(day_of_year)
					y_axis_2021[ index ] += covid_data[i][ header.index(data_category) ]
				# If DOY is NOT already in arrays to be plotted, add it 
				else:
					x_axis_2021.append( day_of_year )
					y_axis_2021.append( covid_data[i][ header.index(data_category) ] )

	# Convert arrays to Numpy arrays
	x_axis_2019 = np.asarray(x_axis_2019)
	x_axis_2020 = np.asarray(x_axis_2020)
	x_axis_2021 = np.asarray(x_axis_2021)
	y_axis_2019 = np.asarray(y_axis_2019)
	y_axis_2020 = np.asarray(y_axis_2020)
	y_axis_2021 = np.asarray(y_axis_2021)
	
	# Sort and generate array of index values that are now in chronological order
	permutation_2019 = x_axis_2019.argsort()
	permutation_2020 = x_axis_2020.argsort()
	permutation_2021 = x_axis_2021.argsort()
	
	# Reorder the combined arrays
	x_axis_2019 = x_axis_2019[permutation_2019]
	x_axis_2020 = x_axis_2020[permutation_2020]
	x_axis_2021 = x_axis_2021[permutation_2021]
	y_axis_2019 = y_axis_2019[permutation_2019]
	y_axis_2020 = y_axis_2020[permutation_2020]
	y_axis_2021 = y_axis_2021[permutation_2021]

	for i in range( len( y_axis_2019 ) ):
		y_axis.append( y_axis_2019[i] )
	for i in range( len( y_axis_2020 ) ):
		y_axis.append( y_axis_2020[i] )
	for i in range( len( y_axis_2021 ) ):
		y_axis.append( y_axis_2021[i] )

	# Convert MET to UTC for plot x-axis
	for day_of_year in x_axis_2019:
		YYYY, MM, DD = ymd( 2019, day_of_year )
		currentDate = datetime( YYYY, MM, DD )
		x_axis.append( currentDate )
	for day_of_year in x_axis_2020:
		YYYY, MM, DD = ymd( 2020, day_of_year )
		currentDate = datetime( YYYY, MM, DD )
		x_axis.append( currentDate )
	for day_of_year in x_axis_2021:
		YYYY, MM, DD = ymd( 2021, day_of_year )
		currentDate = datetime( YYYY, MM, DD )
		x_axis.append( currentDate )

	# Arrays for X day averaged cases
	x_axis_averaged = x_axis[(x_average):]
	y_axis_averaged = []
	
	# Fill x day averaged arrays
	for i in range( x_average, len(x_axis) ):
		y_axis_averaged_value = 0
		for j in range(x_average):
			y_axis_averaged_value += y_axis[i - j]
		y_axis_averaged_value /= x_average
		y_axis_averaged.append(y_axis_averaged_value)

	return( x_axis_averaged, y_axis_averaged )

# Array of matplotlib colors for plotting
matplotlib_colors = [ 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan' ]

# Update user to status of program
print('loading data...\n')

# Import data
data = np.loadtxt('owid-covid-data.csv', dtype='str', delimiter=',')
#NOTE: Data is in a pseudo-array and needs to be put into a proper array to be played with

# Generate header array
header_temp = data[0][:]
header = []
for i in range( len( header_temp ) ):
	header.append( header_temp[i] )

# Generate data array
covid_data = []
for i in range( 1, len( data ) ): # down
	row = []
	for j in range( len( header ) ): # across
		# Convert strings to floats for the values that are numbers
		if j >= 4:
			try:
				row.append( float( data[i][j] ) )
			except ValueError: 
				# When there is no value input 0.0
				row.append( float(0.0) )
		else:
			row.append( data[i][j] )
	covid_data.append( row )

# Option for user to continut plotting data
plot_more_data = 'yes'
while plot_more_data != 'no':

	x_axis_array = []
	y_axis_array = []
	string_array = []
	labels_array = []
	category_array = []
	specific_category_array = []

	# Option for user to add data to existing plot
	add_to_plot = 'yes'
	while add_to_plot != 'no':
	
		x_axis_array_temp = []
		y_axis_array_temp = []
		
		search_by_list = [ header[1], header[2] ]
		search_by_list_printed = [ 'continent', 'country / location', 'world' ]

		# Outut "sort by" options to terminal
		print( '\nsort by:' )
		for i in range( len( search_by_list_printed ) ):
			print( str(i) + ': ' + str(search_by_list_printed[i]) )
		print('')
		
		# Save user selestion
		search_by_selection = raw_input()

		# For everything except 'World'
		if search_by_selection != '2':

			# Update category selestion
			category = search_by_list[ int(search_by_selection) ]
			category_array.append( str(category) )

			category_list = []
			
			# Generate category list
			for i in range( len(covid_data) ):
				content = covid_data[i][ header.index(category) ]
				if content != '' and content not in category_list:
					category_list.append( covid_data[i][ header.index(category) ] )
			category_list.sort()

			# Outut "selection" options to terminal
			print( '\nselect ' + category + ':' )
			for i in range( len( category_list ) ):
				print( str(i) + ': ' + str(category_list[i]) )
			print('')
			
			# Save user selestion
			specific_category_selection = raw_input()
			specific_category = category_list[ int(specific_category_selection) ]
			specific_category_array.append( str(specific_category) )

		# For 'World'
		if search_by_selection == '2':
			search_by_selection = '1'

			# Update category selestion
			category = search_by_list[ int(search_by_selection) ]
			category_array.append( str(category) )

			category_list = []
			
			# Generate category list
			for i in range( len(covid_data) ):
				content = covid_data[i][ header.index(category) ]
				if content != '' and content not in category_list:
					category_list.append( covid_data[i][ header.index(category) ] )
			category_list.sort()

			# Save user selestion
			specific_category_selection = category_list.index('World')
			specific_category = category_list[ int(specific_category_selection) ]
			specific_category_array.append( str(specific_category) )

		data_list = []
		
		# Organize selection options
		for i in range( 4, len( header ) ):
			data_list.append( header[i] )
		data_list.sort()

		# Outut "selection" options to terminal
		print( '\nselect data:' )
		for i in range( len( data_list ) ):
			print( str(i) + ': ' + str(data_list[i]) )
		print('')

		# Save user selestion
		data_selection = raw_input()
		data_category = data_list[ int(data_selection) ]

		# Prompt user to average data over X number of days
		x_averaged_selection = raw_input( '\naverage the data every _ day(s):\n' )
		x_average = int( x_averaged_selection )

		# Add information to plot queue to be plotted when user is ready
		x_axis_array_temp, y_axis_array_temp = plot_queue( covid_data, header, category, specific_category, data_category, x_average )
		x_axis_array.append( x_axis_array_temp )
		y_axis_array.append( y_axis_array_temp )
		string_array.append( x_average )
		labels_array.append( data_category )
	
		# Ask user if they want to over-plot more data
		yes_no = raw_input( '\nwould you like to add more data to this plot?\ny: yes\nn: no\n' )
		if yes_no == 'y' or yes_no == 'yes':
			add_to_plot = 'yes'
		if yes_no == 'n' or yes_no == 'no':
			add_to_plot = 'no'

	# Plot the data with legend ad title	
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %d, %Y'))
	for i in range( len( x_axis_array ) ):
		plt.plot( x_axis_array[i], y_axis_array[i], label=str(string_array[i])+' day avg. '+labels_array[i]+ ' ('+category_array[i] + ': ' + specific_category_array[i]+')'+'  |  '+x_axis_array[i][-1].strftime('%Y-%m-%d')+': '+str("{:.0f}".format(y_axis_array[i][-1])), color=matplotlib_colors[i] )
		plt.scatter( x_axis_array[i][-1], y_axis_array[i][-1], color=matplotlib_colors[i], s = 5 )
	plt.legend(bbox_to_anchor=(0.00, 1.01), loc='lower left', borderaxespad=0.)
	plt.xlabel( 'Date' )
	plt.ylabel( 'Number of People' )
	plt.gcf().autofmt_xdate()
	print( '\nplease exit out of plotting window before continuing\n' )
	plt.show()

	# Ask user if they want to save the plot they generated
	print_plot = raw_input( '\nwould you like to save this plot?\ny: yes\nn: no\n' )

	if print_plot == 'y':
		# Ask user what name they want to save the file as
		plot_name = raw_input( '\nwhat would you like to same this plot? [________.jpeg]\n' )
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %d, %Y'))
		for i in range( len( x_axis_array ) ):
			plt.plot( x_axis_array[i], y_axis_array[i], label=str(string_array[i])+' day avg. '+labels_array[i]+ ' ('+category_array[i] + ': ' + specific_category_array[i]+')'+'  |  '+x_axis_array[i][-1].strftime('%Y-%m-%d')+': '+str("{:.0f}".format(y_axis_array[i][-1])), color=matplotlib_colors[i] )
			plt.scatter( x_axis_array[i][-1], y_axis_array[i][-1], color=matplotlib_colors[i], s = 5 )
		plt.legend(bbox_to_anchor=(0.00, 1.01), loc='lower left', borderaxespad=0.)
		plt.xlabel( 'Date' )
		plt.ylabel( 'Number of People' )
		plt.gcf().autofmt_xdate()
		plt.savefig(plot_name+'.jpeg')

	# Ask user if they want to plot more data
	more_data_yes_no = raw_input( '\nwould you like to look at more data?\ny: yes\nn: no\n' )
	if more_data_yes_no == 'y' or more_data_yes_no == 'yes':
		plot_more_data = 'yes'
	if more_data_yes_no == 'n' or more_data_yes_no == 'no':
		plot_more_data = 'no'
	
# End of program
print( '\n-- END OF PROGRAM --\n' )

