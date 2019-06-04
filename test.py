#!/usr/bin/env python3

# Tweet timing tester for mensatron. Simulates years of activity.

from random import (random, randrange, gauss)

def test_timing():
	days_to_simulate = 100000
	hour_chance = 0.02
	mu = 15
	sigma = 10
	stat_list = []

	for i in range(0, days_to_simulate):
		tweets = 0
		times = []
		for j in range(0, 24):
			if random() < hour_chance:
				k_init = randrange(60)
				k = k_init
				while k < 60 and k - k_init < 30:
					tweets += 1
					times.append("{}:{}".format(j, k))
					k += max(int(gauss(mu, sigma)), 0)
		stat_list.append([tweets, times])

	histogram = [i[0] for i in stat_list]
	mean = float(sum(histogram)) / days_to_simulate
	_min = min(histogram)
	_max = max(histogram)

	print("Tested {} days (~{} years)".format(days_to_simulate,
		int(days_to_simulate / 365.2425)))
	print("Min:  {}".format(_min))
	print("Mean: {:.2f}".format(mean))
	print("Max:  {}".format(_max))
	print()

	for i in range(0, _max + 1):
		num = len([j for j in histogram if j == i])
		frac = num/days_to_simulate
		print("{:2d}: {:6d}, {:6.2f}/yr, 1/{:.1f}".format(i, num,
			frac*365.2425, (1/frac if frac != 0 else float('NaN'))))

	all_times = [i[1] for i in stat_list if i[0] != 0]
	for i in all_times[1:12]:
		print(str(i))

def test_selection():
	tweets_to_simulate = 100000
	stat_list = []
	tweet_list = ( # (<cumulative weight>, <tweet text>)
		(6, "Ciao, dimmi."),
		(14, "Dimmi."),
		(16, "Buon appetito."),
	)
	for i in range(0, tweets_to_simulate):
		index = randrange(tweet_list[-1][0])
		for i in tweet_list:
			if index < i[0]:
				stat_list.append(i[1])
				break

	print("Tested {} tweets".format(tweets_to_simulate))
	for i in [j[1] for j in tweet_list]:
		n = len([j for j in stat_list if j == i])
		print("{:6d} ({:2.0f}%): {}".format(n, n/tweets_to_simulate*100, i))
	print(stat_list[1:16])

# test_timing()
# test_selection()
