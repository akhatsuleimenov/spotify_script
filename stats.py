'''
┌───────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────┐
│                                               │                                                                 │
│                   stats.py                    │   ▄████████    ▄█   ▄█▄    ▄█    █▄       ▄████████     ███     │
│                                               │  ███    ███   ███ ▄███▀   ███    ███     ███    ███ ▀█████████▄ │
│ By: Akhat <as13966@nyu.edu>                   │  ███    ███   ███▐██▀     ███    ███     ███    ███    ▀███▀▀██ │
│                                               │  ███    ███  ▄█████▀     ▄███▄▄▄▄███▄▄   ███    ███     ███   ▀ │
│ Created: 2022-04-06 12:21:03 by Akhat         │▀███████████ ▀▀█████▄    ▀▀███▀▀▀▀███▀  ▀███████████     ███     │
│ Updated: 2022-04-06 22:57:39 by Akhat         │  ███    ███   ███▐██▄     ███    ███     ███    ███     ███     │
│                                               │  ███    ███   ███ ▀███▄   ███    ███     ███    ███     ███     │
│ Copyright (c) 2022 github.com/akhatsuleimenov │  ███    █▀    ███   ▀█▀   ███    █▀      ███    █▀     ▄████▀   │
│            All rights reserved.               │               ▀                                                 │
└───────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
'''

import json
import csv

# save the JSON into dictionary
def extract_data(file_names):
	'''
	{	
		'endTime': '2021-03-26 12:22', 
		'artistName': 'dudeontheguitar', 
		'trackName': 'Boiy Bolgan', 
		'msPlayed': 115846
	}
	'''

	list_data = []
	for file in file_names:
		with open(file) as json_file:
			list_data.append(json.load(json_file))
	return list_data

# get the most played item + time
def get_most_played_item(list_data, item):
	dic = {}
	dic_time = {}
	for data in list_data:
		for instance in data:
			name = instance[item]
			ms_played = instance['msPlayed']
			if name not in dic:
				dic[name] = 1
				dic_time[name] = ms_played
			else:
				dic[name] += 1
				dic_time[name] += ms_played
	dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) # sort in reverse order
	dic_time = dict(sorted(dic_time.items(), key=lambda item: item[1], reverse=True)) # sort in reverse order
	return (dic, dic_time)

# get the part of the day when tracks where played + time
def get_most_played_part_of_the_day(list_data, item):
	'''
		Morning: 5 am - 12 pm ---> 300 <= x < 720
		Afternoon: 12 pm - 5 pm ---> 720 <= x < 1020
		Evening: 5 pm - 9 pm ---> 1020 <= x < 1260
		Night: 9 pm - 5 am ---> x < 300 && x >= 1260
	'''

	dic = {'Morning' : 0, 'Afternoon' : 0, 'Evening' : 0, 'Night' : 0}
	dic_time = {'Morning' : 0, 'Afternoon' : 0, 'Evening' : 0, 'Night' : 0}
	for data in list_data:
		for instance in data:
			time = instance[item][11:]
			int_time = int(time[0:2]) * 60 + int(time[3:])
			ms_played = instance['msPlayed']
			if int_time >= 300 and int_time < 720:
				part_of_the_day = 'Morning'
			elif int_time >= 720 and int_time < 1020:
				part_of_the_day = 'Afternoon'
			elif int_time >= 1020 and int_time < 1260:
				part_of_the_day = 'Evening'
			else:
				part_of_the_day = 'Night'
			dic[part_of_the_day] += 1 
			dic_time[part_of_the_day] += ms_played
	dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) # sort in reverse order
	dic_time = dict(sorted(dic_time.items(), key=lambda item: item[1], reverse=True)) # sort in reverse order
	return (dic, dic_time)

def get_most_played_day_or_month(list_data, day):
	dic = {}
	dic_time = {}
	for data in list_data:
		for instance in data:
			time = instance['endTime'][:10]
			if day:
				int_time = int(time[8:])
			else:
				int_time = int(time[5:7])
			ms_played = instance['msPlayed']
			if int_time not in dic:
				dic[int_time] = 1
				dic_time[int_time] = ms_played
			else:
				dic[int_time] += 1
				dic_time[int_time] += ms_played
	dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True)) # sort in reverse order
	dic_time = dict(sorted(dic_time.items(), key=lambda item: item[1], reverse=True)) # sort in reverse order
	return (dic, dic_time)

def save_to_csv(names, list_dictionaries):
	for name, d in zip(names, list_dictionaries):
		w = csv.writer(open("csv_files/" + name, "w"))
		for key, val in d.items():
			w.writerow([key, val])

def create_dicitonaries(list_data):
	most_played_artists, most_played_artists_time = get_most_played_item(list_data, 'artistName')
	most_played_track, most_played_track_time = get_most_played_item(list_data, 'trackName')
	most_played_part_of_the_day, most_played_part_of_the_day_time = get_most_played_part_of_the_day(list_data, 'endTime')
	most_played_day, most_played_day_time = get_most_played_day_or_month(list_data, True)
	most_played_month, most_played_month_time = get_most_played_day_or_month(list_data, False)

	names = ["most_played_artists.csv", "most_played_artists_time.csv", "most_played_track.csv", "most_played_track_time.csv", 
			 "most_played_part_of_the_day.csv", "most_played_part_of_the_day_time.csv", "most_played_day.csv", "most_played_day_time.csv",
			 "most_played_month.csv", "most_played_month_time.csv"]
	list_dictionaries = [most_played_artists, most_played_artists_time, most_played_track, most_played_track_time, 
						 most_played_part_of_the_day, most_played_part_of_the_day_time, most_played_day, most_played_day_time,
						 most_played_month, most_played_month_time]

	return (names, list_dictionaries)

def main():
	file_names = ["StreamingHistory0.json", "StreamingHistory1.json", "StreamingHistory2.json"]

	list_data = extract_data(file_names)
	names, list_dictionaries = create_dicitonaries(list_data)
	save_to_csv(names, list_dictionaries)

if __name__ == '__main__':
	main()