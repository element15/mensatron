#!/usr/bin/env python3

# The one and only @mensatron. This script is intended to be invoked as a `cron`
# job once an hour, more or less on the hour.
# Written by Christian Moomaw
# Last revised 2019-06-01

DEBUG = False
DRY_RUN = False # Post to stdout instead of Twitter

if DEBUG:
	from sys import exit

import logging
from logging import (critical, error, warning, info, debug)

import re
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
	import twitter
	api = twitter.Api(consumer_key=C_KEY, consumer_secret=C_SECRET,
		access_token_key=A_TOKEN, access_token_secret=A_TOKEN_SECRET)
	info('API initialised')
	return api


def load_sequence_id(api=None):
	# Extract the most recent sequence ID and increment by one
	if not api:
		return 0

	latest_tweet_text = api.GetUserTimeline(screen_name='mensatron',
		count=1, include_rts=False, exclude_replies=True,
		trim_user=True)[0].text
	p = re.compile(r'(\d)+: .*')
	m = p.match(latest_tweet_text)
	if m:
		sequence_id = int(m.group(1))
		info('Got sequence ID: {}'.format(sequence_id))
	else:
		critical('Failed to load sequence ID, exiting...')
		exit(1)
	return sequence_id + 1


def tweet(sequence_id, api=None):
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
			tweet_text = '{}: {}'.format(sequence_id, i[1])
			sequence_id += 1
			if api:
				api.PostUpdate(tweet_text)
				info('Tweeted "{}"'.format(tweet_text))
			else: # DRY_RUN
				print(tweet_text)
				info('Simulated tweet: "{}"'.format(tweet_text))
			return sequence_id


def tweet_burst():
	info('Beginning tweet burst...')

	# Units for the following parameters are in minutes
	tweet_spacing_mu = 15
	tweet_spacing_sigma = 10
	max_burst_length = 30

	if not DRY_RUN:
		api = get_api()
	else:
		api = None

	sequence_id = load_sequence_id(api)

	init_hour = datetime.now().hour
	debug('Init hour set: {}'.format(init_hour))
	target_minute_init = randrange(datetime.now().minute, 60)
	debug('Initial target minute: {}'.format(target_minute_init))
	target_minute = target_minute_init

	while (datetime.now().hour == init_hour and target_minute < 60
		and (target_minute - target_minute_init) < max_burst_length):
		debug('Entered burst loop')

		sleep_minutes = target_minute - datetime.now().minute
		if not DRY_RUN:
			info('Sleeping for {} minutes...'.format(sleep_minutes))
			sleep(sleep_minutes * 60)
			info('Resuming from sleep...')
		else:
			info('Skipping {}-minute sleep...'.format(sleep_minutes))

		sequence_id = tweet(sequence_id, api)

		target_minute += max(int(gauss(
			tweet_spacing_mu, tweet_spacing_sigma)), 1)
		debug('New target minute: {}'.format(target_minute))

	info('Tweet burst finished')


def main():
	hourly_chance = 0.02
	info('New mensatron invoked')
	if DRY_RUN:
		info('Running in dry run mode')

	if random() < hourly_chance:
		tweet_burst()
		if DEBUG: # Nonzero exit codes used for testing with shell scripts
			exit(40)
	else:
		info('No tweet burst triggered')
		if DEBUG: # Nonzero exit codes used for testing with shell scripts
			exit(41)

main()
