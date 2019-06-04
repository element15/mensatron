#!/usr/bin/env python3

# The one and only @mensatron. This script is intended to be invoked as a `cron`
# job once an hour, more or less on the hour.
# Written by Christian Moomaw
# Last revised 2019-06-01

DEBUG = False

import logging
from logging import (info, debug)

from datetime import datetime
from random import (random, randrange, gauss)
from time import sleep

logging.basicConfig(
	filename=('mensatron_debug.log' if DEBUG else 'mensatron.log'),
	level=(logging.DEBUG if DEBUG else logging.INFO),
	format='%(asctime)s [%(levelname)s/%(process)s]: %(message)s',
	datefmt='%Y-%m-%dT%H:%M:%S%Z')

def get_api():
	# Only setup for twitter if necessary
	info('Initialising Twitter API...')
	from secrets import (C_KEY, C_SECRET, A_TOKEN, A_TOKEN_SECRET)
	import tweepy

	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)
	info('API initialised')
	return api

def tweet(api):
	tweet_list = ( # (<cumulative weight>, <tweet text>)
		(6, "Ciao, dimmi."),
		(14, "Dimmi."),
		(16, "Buon appetito."),
		(24, "Poi?"),
	)
	index = randrange(tweet_list[-1][0])
	debug('Tweet selection index: {}'.format(index))
	for i in tweet_list:
		if index < i[0]:
			api.update_status(i[1])
			info('Tweeted "{}"'.format(i[1]))
			return

def tweet_burst():
	info('Beginning tweet burst...')

	# Units for the following parameters are in minutes
	tweet_spacing_mu = 15
	tweet_spacing_sigma = 10
	max_burst_length = 30

	api = get_api()
	init_hour = datetime.now().hour
	debug('Init hour set: {}'.format(init_hour))
	target_minute_init = randrange(datetime.now().minute, 60)
	debug('Initial target minute: {}'.format(target_minute_init))
	target_minute = target_minute_init
	while (datetime.now().hour == init_hour and target_minute < 60
		and (target_minute - target_minute_init) < max_burst_length):
		debug('Entered burst loop')

		sleep_minutes = target_minute - datetime.now().minute
		info('Sleeping for {} minutes...'.format(minutes))
		sleep(minutes * 60)
		info('Resuming from sleep...')

		tweet(api)
		target_minute += max(int(gauss(
			tweet_spacing_mu, tweet_spacing_sigma)), 0)
		debug('New target minute: {}'.format(target_minute))
	info('Tweet burst finished')

hourly_chance = 0.02
info('New mensatron invoked')
if random() < hourly_chance:
	tweet_burst()
else:
	info('No tweet burst triggered')
