from libqtile import widget
from libqtile import hook

class CurrentLayout(widget.CurrentLayout):
    def __init__(self, **config):
        super().__init__(**config)
        self._count = 0

    def change(self):
        if self._layout.name == "max":
            if self._count == 0:
                self.text = "[M]"
            else:
                self.text = "[{}]".format(self._count)
        else:
            self.text = "[]="
        self.bar.draw()

    def _wincount(self, *args):
        try:
            self._count = len(self.bar.screen.group.windows)
        except AttributeError:
            self._count = 0
        self.change()

    def _win_killed(self, window):
        try:
            self._count = len(self.bar.screen.group.windows)
        except AttributeError:
            self._count = 0
        self.change()
    
    def hook_response(self, layout, group):
        self._layout = layout
        if group.screen is not None and group.screen == self.bar.screen:
            self.change()

    def setup_hooks(self):
        hook.subscribe.layout_change(self.hook_response)
        hook.subscribe.client_killed(self._win_killed)
        hook.subscribe.client_managed(self._wincount)
        hook.subscribe.current_screen_change(self._wincount)
        hook.subscribe.setgroup(self._wincount)


class Volume(widget.Volume):

    def __init__(self, **config):
        super().__init__(**config)

    def _update_drawer(self):
        if self.theme_path:
            self.drawer.clear(self.background or self.bar.background)
            if self.volume <= 0:
                img_name = "audio-volume-muted"
            elif self.volume <= 30:
                img_name = "audio-volume-low"
            elif self.volume < 80:
                img_name = "audio-volume-medium"
            else:  # self.volume >= 80:
                img_name = "audio-volume-high"

            self.drawer.ctx.set_source(self.surfaces[img_name])
            self.drawer.ctx.paint()
        elif self.emoji:
            if len(self.emoji_list) < 4:
                self.emoji_list = ["\U0001f507", "\U0001f508", "\U0001f509", "\U0001f50a"]
                logger.warning(
                    "Emoji list given has less than 4 items. Falling back to default emojis."
                )

            if self.volume == -1:
                self.text = "<span font_size='18pt' letter_spacing='15000'>󰖁</span><span rise='2700'>muted</span>"
            else: 
                if self.volume <= 10:
                    icon = self.emoji_list[0]
                elif self.volume <= 30:
                    icon = self.emoji_list[1]
                elif self.volume < 50:
                    icon = self.emoji_list[2]
                elif self.volume >= 50:
                    icon = self.emoji_list[3]
                self.text = "<span font_size='18pt' letter_spacing='15000'>{}</span><span rise='2700'>{}%</span>".format(icon, self.volume)
        else:
            if self.volume == -1:
                self.text = "muted"
            else:
                self.text = "{}%".format(self.volume)
