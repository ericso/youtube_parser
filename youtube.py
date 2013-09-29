#!/usr/bin/python

import requests # http://docs.python-requests.org/en/latest/
import json
# from urllib.parse import urlencode # Python 3
from urllib import urlencode # Python 2
from urlparse import urlparse

# Youtube Video Object
class YoutubeVideo:
	raw_json = None
	name = ''
	url = ''
	category = ''
	thumbnail = ''

	def __init__(self, raw_json, name, url, category, thumbnail):
		self.raw_json = raw_json
		self.name = name
		self.url = url
		self.category = category
		self.thumbnail = thumbnail


class YoutubeParser:
	"""
	Class for querying Youtube
	"""

	def __init__(self, params, api_endpoint='http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed'):
		self.params = params
		self.api_endpoint = api_endpoint

	def query_youtube(self, params=None):
		"""
		Queries Youtube
		@param params dictionary of api parameters
		@returns query response
		"""
		if params is not None:
			self.params = params

		return requests.get(self.api_endpoint, params=urlencode(self.params))
			
	def query_single_url(self, url):
		"""
		Gets information on a single Youtube video
		@param url The url of the Youtube video
		@returns query response
		"""
		# Parse out the video id from the url
		url_comps = urlparse(url)
		url = url_comps.query.split('=')[1]

		single_video_endpoint = 'https://gdata.youtube.com/feeds/api/videos/' + url
		single_video_params = {
			'v': 2,
			'alt': 'json'
		}

		return requests.get(single_video_endpoint, params=urlencode(single_video_params))


if __name__ == "__main__":

	api_endpoint = 'http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed'
	params = {
		'max-results': 10,
		'time': 'this_week',
		'alt': 'json',
		'orderby': 'viewCount'
	}
	
	# Create the Youtube Parser
	youtube_parser = YoutubeParser(params, api_endpoint)
	# Query Youtube
	resp = youtube_parser.query_youtube()

	# Store the json response
	resp_json = resp.json() # Will get decoding error if running on Windows cmd

	# Parse each video out into an array
	videos = [video for video in resp_json['feed']['entry']]
	print('Number of videos: %d' % len(videos))
	# print(videos)

	youtube_videos = []

	# Create YoutubeVideo objects
	for video in videos:
		print('Creating a YoutubeVideo object')
		youtube_videos.append(YoutubeVideo(video, video['title']['$t'], video['link'][0]['href'], video['category'][1]['label'], video['media$group']['media$thumbnail'][0]['url']))

	# Youtube analytics
	# Never got to this

	# Show that they actually exist and have data
	for video in youtube_videos:
		print('-----------------------')
		print('Name: %s' % video.name)
		print('URL: %s' % video.url)
		print('Category: %s' % video.category)
		print('Thumbnail: %s' % video.thumbnail)

	# Query for a single video, Conan skit
	test_url = 'http://www.youtube.com/watch?v=enKCgVSBSPs'
	single_video_resp = youtube_parser.query_single_url(test_url).json()
	single_video_json = single_video_resp['entry']
	single_video = YoutubeVideo(single_video_json, single_video_json['title']['$t'], single_video_json['link'][0]['href'], single_video_json['category'][1]['label'], single_video_json['media$group']['media$thumbnail'][0]['url'])
	
	print('-----------------------')
	print('SINGLE Video')
	print('Name: %s' % single_video.name)
	print('URL: %s' % single_video.url)
	print('Category: %s' % single_video.category)
	print('Thumbnail: %s' % single_video.thumbnail)