import urllib,urllib2,re,os
import xbmcplugin,xbmcgui
import ustream
from BeautifulSoup import BeautifulSoup

class Set:
	"""
	Displays the output to XBMC
	"""

	# Current instance of the plugin
	plugin_id = 0

	# Set the default plugin name
	_plugin_name = ''

	# Set the default page number
	page_no = 1

	# Set the params field to a list
	params = []
	
	# values default to none
	url=None
	name=None
	mode=None

	def __init__(self, plugin_id, in_params):
		"""
		constructor

		@param int plugin_id - id of current plugin instance
		@param string plugin_name - name of plugin
		"""

		self.this_plugin = plugin_id

		self.params = in_params

		try:
			self.url=urllib.unquote_plus(self.params["url"])
		except:
			pass
		try:
			self.name=urllib.unquote_plus(self.params["name"])
		except:
			pass
		try:
			self.iconimage=urllib.unquote_plus(self.params["iconimage"])
		except:
			pass
		try:
			self.mode=int(self.params["mode"])
		except:
			pass
		# Check to see if the page version is set
		try:
			self.page_no=int(self.params["page_no"])
		except:
			pass
		
		# If mode isn't set, then display the category choices
		if self.mode==None or self.url==None or len(self.url)<1:
			print ""
			self.show_categories()

		# If the mode is set to one, then get the live video 
		elif self.mode==1:
			print ""+self.url
			self.show_categories()	

		# If the mode is set to 2, then get the default video list
		elif self.mode==2:
			print ""+self.url
			video_list = {}
			video_list = ustream.pull_video_list('http://www.ustream.tv/joerogan/videos', self.page_no)
			self.show_video_list(video_list)
			
		# If the mode is set to 3, then get the MP4 file
		elif self.mode==3:
			print ""+self.url
			video_to_play = ustream.pull_video_url(self.url)
			self.play_vid(video_to_play)

		# If the mode is set to 4, then get the Live Stream
		elif self.mode==4:
			print ""+self.url
			live_video_to_play = ustream.pull_live_stream(self.url)

			# If the Live Video URL can't be found, we're not broadcasting
			if live_video_to_play == False:
				# Echo something to the screen saying Not Broadcasting
				print "Video didn't work"
			else:
				self.play_vid(live_video_to_play)
	
	def _add_directory(self, name, url, mode, icon):
		"""
		Displays list of videos as a directory listing

		@param list listing
		@return void
		"""

		final_url = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)

		if name == 'Next Page':
			self.page_no += 1
			final_url += "&page_no=" + str(self.page_no)

		list_item = xbmcgui.ListItem(name)
		
		ok=xbmcplugin.addDirectoryItem(this_plugin, final_url, list_item, isFolder=True)
		
		return ok
		
	def _add_live_link(self, name, url, mode, icon):
		"""
		Displays list of videos as a directory listing

		@param list listing
		@return void
		"""

		final_url = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)

		list_item = xbmcgui.ListItem(name)
		list_item.setProperty('IsPlayable', 'true')
		
		return xbmcplugin.addDirectoryItem(self.this_plugin, final_url, list_item)


	def show_categories(self):
		"""
		Displays the list of categories you first see when you use the plugin
		"""

		 # Mode 4 = Live Video
		self._add_live_link('Live','http://cdngw.ustream.tv/Viewer/getStream/1/2399940.amf',4,'http://static-cdn1.ustream.tv/i/channel/picture/2/3/9/9/2399940/2399940_joerogan171008_450x366,90x90,r:1.jpg')

		 # Mode 2 = Video Links
		self._add_directory('Recorded Videos','http://www.ustream.tv/joerogan/videos',2,'http://static-cdn1.ustream.tv/i/channel/picture/2/3/9/9/2399940/2399940_joerogan171008_450x366,90x90,r:1.jpg')

		# We're done with the directory listing
		xbmcplugin.endOfDirectory(self.this_plugin)

	def show_video_list(self, match):
		"""
		Shows a list of videos
		@param dict match - a key -> value pair of lists
		@return void
		"""
		# send each item to XBMC, mode 3 opens video
		for index in range (len(match['name'])):
			self._add_live_link(match['name'][index], 
						  match['vid_url'][index],
						  3,
						  match['thumbnail'])
		
		# Lastly add a link to the Next Video
		self._add_directory('Next Page', 'http://www.ustream.tv/joerogan/videos', 2, 'http://static-cdn1.ustream.tv/i/channel/picture/2/3/9/9/2399940/2399940_joerogan171008_450x366,90x90,r:1.jpg')

		# We're done with the directory listing
		xbmcplugin.endOfDirectory(self.this_plugin)


	def play_vid(self, video_to_play):
		"""
		Plays a video from URL
		@ param string video_to_play - a URL of a video file
		"""
		item = xbmcgui.ListItem(path=video_to_play)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
	
	### END SET CLASS

def get_params():
		"""
		Get the params from main URL (taken from the original XBMC scripting guide.
		"""
		param=[]
		# Get the second argument
		paramstring=sys.argv[2]
		# If the length of the parameters is more than 2
		if len(paramstring)>=2:
				# Set the parameter string to above 2
				params=sys.argv[2]
				# Remove the question mark
				cleanedparams=params.replace('?','')
				# If the parameter before last is a slash
				if (params[len(params)-1]=='/'):
						# Erm...
						params=params[0:len(params)-2]
				# Create a list of parameters
				pairsofparams=cleanedparams.split('&')
				# Create a key -> value hash
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')

						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]

		return param

# id of this plugin's instance
this_plugin = int(sys.argv[1])

# Main program
Set(this_plugin, get_params())
		
