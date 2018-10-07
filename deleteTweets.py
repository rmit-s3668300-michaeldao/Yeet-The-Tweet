import argparse
import csv
import sys
import time
import os
import twitter
from dateutil.parser import parse

# i need to see how many we will remove
def howManyTweets(date):
	rows = 0
	with open("tweets.csv") as file:	
		# get tweet id and date of each tweet
		for row in csv.DictReader(file):
			tweet_id = int(row["tweet_id"])
			tweet_date = parse(row["timestamp"], ignoretz=True).date()

			# make sure only the tweets before the defined date is checked
			if date != "" and tweet_date >= parse(date).date():
				continue
				
			rows += 1
	print ("I have found {} tweets in the csv file provided\n".format(rows))
	input("Press Enter to continue...\n")
	
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
	
			# make sure only the tweets before the defined date is deleted
			if date != "" and tweet_date >= parse(date).date():
				continue
			
			# delete the tweet	
			try:
				print ("Deleting tweet #{0} ({1})".format(tweet_id, tweet_date))
		
				# pass tweet id to twitter to be deleted
				api.DestroyStatus(tweet_id)
				count += 1
				time.sleep(0.5)

			# catch error
			except (twitter.TwitterError, err):
				print ("Exception: %s\n" % err.message)
	
	print ("Number of deleted tweets: %s\n" % count)

def error(msg, exit_code=1):
	sys.stderr.write("Error: %s\n" % msg)
	exit(exit_code)	
	
# main method
def main():	
	# setup arguments
	parser = argparse.ArgumentParser(description="Delete old tweets")
	parser.add_argument("-d", dest="date", required=True, help="Delete tweets until this date")
	parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"], help="Restrict to either replies or retweets")
	args = parser.parse_args()

	# define twitter api keys
	api = twitter.Api(
		# Consumer Api Keys (insert your own!)
		consumer_key="",
		consumer_secret="",
		# Consumer Api Keys (insert your own!)
		access_token_key="",
        access_token_secret="")

	# count how many we will delete
	howManyTweets(args.date)
	
	# pass keys into delete method to begin process
	delete(api, args.date, args.restrict)

if __name__ == "__main__":
	main()