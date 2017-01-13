  
# -- Imports ------------------------------------------------
import datetime,socket,subprocess,os
import xbmc,xbmcplugin,xbmcgui,xbmcaddon

# -- Constants ----------------------------------------------
ADDON_ID = 'service.homelynk'


# -- Settings -----------------------------------------------
settings = xbmcaddon.Addon(id=ADDON_ID)

# -- I18n ---------------------------------------------------
language = xbmcaddon.Addon(id=ADDON_ID).getLocalizedString

# -- Functions ----------------------------------------------

# -- Classes ------------------------------------------------
class homelynkHandler(xbmc.Player):

	def __init__ (self):
		xbmc.Player.__init__(self)
		self.isplayingvideo = False;
		self.dbg = self.getCommand('debug')


	def getCommand(self,command):
		return settings.getSetting(command)

	def SendHL(self,command=''):
		if type(command) is str and len(command) > 0:
			xbmc.log ('Sending command to HomeLYnk: '+command)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((settings.getSetting('hostname'), int(settings.getSetting('port'))))
			s.send('{0}\n'.format('<GROUPADR>'+ format(self.getCommand('groupadr')+'</GROUPADR>'+'<VALUE>'+format(command)+'</VALUE>')))
			s.close()

	def switch_log(message):
		if dbg =="true":
			xbmc.log(message) 

	def Run(self):
		while(not xbmc.abortRequested):
			if xbmc.Player().isPlaying():
				if xbmc.Player().isPlayingVideo():
					self.isplayingvideo = True
				else:
					self.isplayingvideo = False
			xbmc.sleep(1000)

	def StartUp(self):
		xbmc.log('Starting up HomeLYnk...')
		self.SendHL(self.getCommand('onstartup'))

	def ShutDown(self):
		self.SendHL(self.getCommand('onshutdown'))
		xbmc.log('HomeLYnk shut down')

	def onPlayBackStarted(self):
		if xbmc.Player().isPlayingAudio():
			self.SendHL(self.getCommand('onaudioplay'))
		else:
			self.isplayingvideo = True;
			self.SendHL(self.getCommand('onvideoplay'))

	def onPlayBackEnded(self):
		if self.isplayingvideo:
			self.SendHL(self.getCommand('onvideostop'))
		else:
			self.SendHL(self.getCommand('onaudiostop'))

	def onPlayBackStopped(self):
		if self.isplayingvideo:
			self.SendHL(self.getCommand('onvideostop'))
		else:
			self.SendHL(self.getCommand('onaudiostop'))

	def onPlayBackPaused(self):
		if xbmc.Player().isPlayingAudio():
			self.SendHL(self.getCommand('onaudiopause'))
		else:
			self.SendHL(self.getCommand('onvideopause'))

	def onPlayBackResumed(self):
		if xbmc.Player().isPlayingAudio():
			self.SendHL(self.getCommand('onaudioplay'))
		else:
			self.isplayingvideo = True;
			self.SendHL(self.getCommand('onvideoplay'))

# -- Main Code ----------------------------------------------
handler=homelynkHandler()
handler.StartUp()
handler.Run()
handler.ShutDown()
