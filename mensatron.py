#!/usr/bin/env python3

# The one and only @mensatron. This script is intended to be invoked as a `cron`
# job once an hour, more or less on the hour.
# Written by Christian Moomaw
# Last revised 2019-06-01

from datetime import datetime
from random import (random, randrange, gauss)
from time import sleep

def get_api():
	# Only setup for twitter if necessary
	from secrets import (C_KEY, C_SECRET, A_TOKEN, A_TOKEN_SECRET)
	import tweepy

	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)
	return api

def tweet(api):
	tweet_list = ( # (<cumulative weight>, <tweet text>)
		(6, "Ciao, dimmi."),
		(14, "Dimmi."),
		(16, "Buon appetito."),
		(24, "Poi?"),
	)
	index = randrange(tweet_list[-1][0])
	for i in tweet_list:
		if index < i[0]:
			api.update_status(i[1])
			return

def tweet_burst():
	# Units for the following parameters are in minutes
	tweet_spacing_mu = 15
	tweet_spacing_sigma = 10
	max_burst_length = 30

	api = get_api()
	init_hour = datetime.now().hour
	target_minute_init = randrange(datetime.now().minute, 60)
	target_minute = target_minute_init
	while (datetime.now().hour == init_hour and target_minute < 60
		and (target_minute - target_minute_init) < max_burst_length):
		sleep((target_minute - datetime.now().minute) * 60)
		tweet(api)
		target_minute += max(int(gauss(
			tweet_spacing_mu, tweet_spacing_sigma)), 0)

hourly_chance = 0.02
if random() < hourly_chance:
	tweet_burst()
