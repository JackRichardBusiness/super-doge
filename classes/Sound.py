from pygame import mixer


class Sound:
    def __init__(self):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)

        self.allowSFX = True

        self.soundtrack = mixer.Sound("./sfx/main_theme.ogg")
        self.castle = mixer.Sound("./sfx/castletheme.ogg")
        self.desert = mixer.Sound("./sfx/deserttheme.ogg")
        self.haunted = mixer.Sound("./sfx/hauntedtheme.ogg")
        self.snow = mixer.Sound("./sfx/snowtheme.ogg")
        self.underground = mixer.Sound("./sfx/undergroundtheme.ogg")
        self.underwater = mixer.Sound("./sfx/underwatertheme.ogg")
        
        self.coin = mixer.Sound("./sfx/coin.ogg")
        self.bump = mixer.Sound("./sfx/bump.ogg")
        self.stomp = mixer.Sound("./sfx/stomp.ogg")
        self.jump = mixer.Sound("./sfx/small_jump.ogg")
        self.death = mixer.Sound("./sfx/death.wav")
        self.clear = mixer.Sound("./sfx/clear.ogg")
        self.pipe = mixer.Sound("./sfx/pipe.ogg")

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music):
        self.music_channel.play(music)
