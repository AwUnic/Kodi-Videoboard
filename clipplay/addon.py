import sys,os
import xbmc as x
from xbmc import Player
from xbmc import sleep
import xbmcgui as xgui

class clipPlayer(Player):

    def __init__(self):
        Player.__init__(self)
        self.state = None
    #resume previous playback after clip
    #TODO add restoring playlist
    def onPlayBackEnded(self):
        if self.state is not None:
            x.log('# clip ended: resuming ' +self.state[0]+' at '+ str(self.state[1]))
            litem = xgui.ListItem(self.state[0])
            litem.setProperty('Startoffset',str(self.state[1]))
            Player().play(self.state[0],litem)
        else:
            x.log('# nothing to resume')

    #save previous playback state
    #TODO add saving of playlists
    def saveState(self):
        if Player().isPlaying():
            cur_time = Player().getTime()
            cur_file = Player().getPlayingFile()
            self.state = (cur_file,cur_time)
            x.log('# '+str(self.state))
            return (cur_file,cur_time)
        x.log('# no state to save')
    #initiate playback of chosen clip
    #does not check if file exists
    def playClip(self,clip_path):
        x.log('# playing clip ' + clip_path)
        self.play(clip_path)
# path to clip and its length as arguments. If none are specified it's time
# for JOHN CEEEEEEENA
def main(clip_path, clip_length):
    player = clipPlayer()
    player.saveState()
    player.playClip(clip_path)
    x.sleep(int(clip_length)+250)

if __name__=='__main__':
    x.log('# '+str(sys.argv)+str(len(sys.argv)))
    if(len(sys.argv) == 3):
        x.log('# starting meme')
        main(sys.argv[1],sys.argv[2])
    else:
        x.log('# using default')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        main(dir_path+'/resources/cena.mkv',6400)
