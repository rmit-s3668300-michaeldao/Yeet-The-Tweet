import argparse
import csv
import sys
import time
import os
import twitter
from dateutil.parser import parse

# this is where the deleting happens
def delete(api, date, r):
	# counter
	count = 0

	# open up your twitter archive
	with open("tweets.csv") as file:
	
	# get tweet id and date of each tweet
	for row in csv.DictReader(file):
		tweet_id = int(row["tweet_id"])
		tweet_date = parse(row["timestamp"], ignoretz=True).date()
	# 
	if date != "" and tweet_date >= parse(date).date():
		continue
	
	# delete the tweet
	try:
		print "Deleting tweet no. {0} ({1})".format(tweet_id, tweet_date)

		# call api
		api.DestroyStatus(tweet_id)

		# increment and delay program
		count += 1
		time.sleep(0.5)

	# catch error
	except twitter.TwitterError, err:
		print "Exception: %s\n" % err.message
	
	print "Number of deleted tweets: %s\n" % count

# main method
def main():
	parser = argparse.ArgumentParser(description="Delete old tweets")
	parser.add_argument("-d", dest="date", required=True, help="Delete tweets until this date")
	parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"], help="Restrict to either replies or retweets")

	args = parser.parse_args()

	api = twitter.Api(
		consumer_key="",
		consumer_secret="",
                access_token_key="",
                access_token_secret="")

	delete(api, args.date, args.restrict)

if __name__ == "__main__":
	main()
