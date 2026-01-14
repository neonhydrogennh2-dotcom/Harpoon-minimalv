import kivy
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen 
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image 
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
LabelBase.register(name="PirataOne", fn_regular="fonts/PirataOne-Regular.ttf")
from plyer import notification
import re 
import yt_dlp 
from yt_dlp import YoutubeDL
import os 
import threading

# Main Colors
PIRATE_BLACK = (0.08, 0.12, 0.18, 1)      # Deep ocean night
PIRATE_NAVY = (0.15, 0.25, 0.4, 1)         # Ship deck at night  
PIRATE_GOLD = (0.95, 0.75, 0.2, 1)         # Treasure gold
PIRATE_RUST = (0.7, 0.25, 0.15, 1)         # Cannon rust
PIRATE_SEAFOAM = (0.2, 0.65, 0.55, 1)      # Ocean waves
PIRATE_PARCHMENT = (0.95, 0.85, 0.65, 0.9) # Old treasure map

# Accents
PIRATE_WHITE = (0.95, 0.95, 0.98, 1)       # Off-white sails
PIRATE_SILVER = (0.75, 0.8, 0.85, 1)       # Cutlass steel

# This is a Minimal Version of a larger Project which is why there is a few lines of incomplete code and code in "#". 


class DevNull:
    def write(self, msg): 
        pass
    def flush(self): 
        pass
    def isatty(self): 
        return False

class roundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_color = (0,0,0,0)

        with self.canvas.before:
            self.bg_color = Color(0.15, 0.25, 0.4, 1) 
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
            self.bg_rect.pos = self.pos 
            self.bg_rect.size = self.size 

class SpinnerOption(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.15, 0.25, 0.4, 1)
        self.color = (1, 0.9, 0.3, 1)
        self.font_size = '16sp'
        self.font_name= "PirataOne"
        self.size_hint_y = None
        self.height = 50

        #github.com/neonhydrogennh2-dotcom
        

class Home(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        main_layout = BoxLayout(orientation='vertical')
        with main_layout.canvas.before:
            Color(0.08, 0.12, 0.18, 1)  # Dark blue background
            self.main_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_main_rect, pos=self._update_main_rect)

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        layout = BoxLayout(orientation = "vertical", spacing=20, padding = [35], size_hint_y=None)
        
        layout.bind(minimum_height=layout.setter('height'))

        #Header 
        head_box = BoxLayout(orientation= "vertical", size_hint_y=None, height=140)
        image = Image(source="Harpoon.png", 
                      size_hint=(None,None), 
                      size_hint_y=None, 
                      size=(100,100),
                      pos_hint={'center_x': 0.5}
                      )
        title = Label(text="Harpoon", 
                      font_size='40sp',
                      size_hint_y=None,
                      height=30,
                      font_name="PirataOne",
                      color=(0.95, 0.75, 0.2, 1) #Title Color 
                      )
        
        #Text box section

        url_card = BoxLayout(orientation="vertical", size_hint_y=None, height=95, spacing=10)

        url_label = Label(text="Video URL",
        font_size='16sp',
        font_name="PirataOne",
        size_hint_y=None,
        height=22,
        halign="left"             
                          )
        url_label.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))
        
        self.url_input = TextInput(
            multiline=False,
            height=58,
            size_hint_y=None,
            font_size='17sp',
            font_name="PirataOne",
            foreground_color=(0.95, 0.95, 0.98, 1),
            background_color=(0.15, 0.25, 0.4, 1),
            cursor_color=(0.95, 0.75, 0.2, 1),
            hint_text='https://youtube.com/watch?v=...',
            hint_text_color=(0.75, 0.8, 0.85, 1),
            padding=[16, 16, 16, 16]
            )
        
        qb = BoxLayout(orientation="vertical", size_hint_y=None, height=95, spacing=10)

        qualitylabel = Label(
            text="Choose Video Quality",
            font_size="16sp",
            font_name="PirataOne",
            size_hint_y=None,
            height=22,
            halign="left",
            color=(0.95, 0.95, 0.98, 1)
        )
        qualitylabel.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))

        self.quality_spinner = Spinner(
            text='Best(Recommended)',
            values=('Best (Recommended)', '1080p', '720p', '480p', '360p', 'Audio Only'),
            size_hint_y=None,
            font_name="PirataOne",
            height=58,
            font_size='17sp',
            color=(0.95, 0.95, 0.98, 1),
            background_normal='',
            background_color=(0.15, 0.25, 0.4, 1),
            option_cls=SpinnerOption
        )
        
        #Status 
        status_card = BoxLayout(orientation="vertical", size_hint_y=None, height=95, spacing=10)

        status_label = Label(
            text="Status",
            font_size='16sp',
            font_name="PirataOne",
            color=(0.95, 0.95, 0.98, 1),
            size_hint_y=None,
            height=22,
            halign='left'
        )
        status_label.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))

        status_box = BoxLayout(size_hint_y=None, height=50)
        with status_box.canvas.before:
            Color(0.15, 0.25, 0.4, 1)
            self.status_bg = RoundedRectangle(pos=status_box.pos, size=status_box.size, radius=[10])
            status_box.bind(pos=self._update_status_bg, size=self._update_status_bg)

        self.status_text = Label(
            text="Ready to download",
            font_size='15sp',
            font_name="PirataOne",
            color=(0.2, 0.65, 0.55, 1),
            halign='left',
            valign='middle',
            padding=(20, 15)
        )
        self.status_text.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))

        status_box.add_widget(self.status_text)
        status_card.add_widget(status_label)
        status_card.add_widget(status_box)


        # Progress bar 
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=20
        )
        
        #Download Button 

        self.download_btn = roundedButton(
            text="[b]DOWNLOAD[/b]",
            markup = True, 
            size_hint_y=None, 
            height=62,
            font_size='21sp',
            font_name="PirataOne",
            color=(0.95, 0.75, 0.2, 1),
            background_color=(0.2, 0.45, 0.75, 1)

        )
        self.download_btn.bind(on_press=self.on_download)

        nav_bar = BoxLayout(orientation="horizontal", size_hint_y=None, spacing=10, height=50)

        self.infopage_btn = roundedButton(
        text="[b]INFO[/b]",
        markup=True,
        font_size='20sp',
        font_name="PirataOne",
        size_hint_y=None, height=50,
        color=(0.95, 0.75, 0.2, 1),
        background_color=(0.95, 0.85, 0.65, 0.9)
        )
        #self.infopage_btn.bind(on_press=lambda x: self.go_info('info','left'))


        self.mediaplayer_btn = roundedButton(
            text="[b]Media[/b]",
            markup=True, 
            font_size='20sp',
        font_name="PirataOne",
        size_hint_y=None, height=50,
        color=(0.95, 0.75, 0.2, 1),
        background_color=(0.95, 0.85, 0.65, 0.9)
        )
        #self.mediaplayer_btn.bind(on_press=lambda x: self.go_media('media','left'))

        #Info Box 
        info_box = BoxLayout(orientation='vertical', size_hint_y=None, height=75, padding=[12, 12])
        with info_box.canvas.before:
            Color(0.95, 0.85, 0.65, 0.9)
            self.info_bg = RoundedRectangle(pos=info_box.pos, size=info_box.size, radius=[10])
        info_box.bind(pos=self._update_info_bg, size=self._update_info_bg)
        
        info_text = Label(
            text="[b]Note:[/b] Downloads are saved to your Downloads folder \nDifferent qualities saved as separate files \nNotifications will keep you updated",
            font_size='13sp',
            font_name="PirataOne",
            markup=True,
            color=(0.08, 0.12, 0.18, 1),
            halign='left',
            valign='middle'
        )
        info_text.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))
        
        info_box.add_widget(info_text)
        
        

        url_card.add_widget(url_label)
        url_card.add_widget(self.url_input)
        head_box.add_widget(image)
        head_box.add_widget(title)
        qb.add_widget(qualitylabel)
        qb.add_widget(self.quality_spinner)
        nav_bar.add_widget(self.infopage_btn)
        nav_bar.add_widget(self.mediaplayer_btn)
        layout.add_widget(head_box)
        layout.add_widget(url_card)
        layout.add_widget(qb)
        layout.add_widget(status_card)
        layout.add_widget(self.progress_bar)
        layout.add_widget(self.download_btn)
        #layout.add_widget(nav_bar)
        layout.add_widget(info_box)
        scroll.add_widget(layout)
        self.add_widget(scroll)

#def
    def _update_main_rect(self, instance, value):
        self.main_rect.pos = instance.pos
        self.main_rect.size = instance.size

    def _update_status_bg(self, instance, value):
        self.status_bg.pos = instance.pos
        self.status_bg.size = instance.size

    def send_notification(self, title, message):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Harpoon',
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def go_info(self, name, direction):
        direction = self.manager.transition.direction = "left"
        name = self.manager.current = "info"

    def go_media(self, name, direction):
        direction = self.manager.transition.direction = "left"
        name = self.manager.current = "media"

    def _update_info_bg(self, instance, value):
        self.info_bg.pos = instance.pos
        self.info_bg.size = instance.size

    def update_status(self, msg, color=(0.3, 1, 0.5, 1)):
        """Update status with color"""
        def update(dt):
            self.status_text.text = msg
            self.status_text.color = color
        Clock.schedule_once(update)

    def update_progress(self, value):
        """Update progress bar"""
        Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', value))
    
    def get_download_path(self):
        """Get appropriate download path for platform"""
        app_name = "Harpoon"
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                base_path = os.path.join(primary_external_storage_path(), 'Download', app_name) 
                
            except ImportError:
                base_path = os.path.join('/storage/emulated/0/Download', app_name)
        else:
            base_path = os.path.join(os.path.expanduser("~"), "Downloads", app_name)

        os.makedirs(base_path, exist_ok=True)
        return base_path
    
        
    def validate_input(self):
        
        url = self.url_input.text.strip()
        
        if not url:
            self.update_status(" Please enter a URL", (0.7, 0.25, 0.15, 1))
            return False
        
        if not ("youtube.com" in url or "youtu.be" in url):
            self.update_status(" Invalid YouTube URL", (0.7, 0.25, 0.15, 1))
            return False
        
        return True


    def on_download(self, instance):
        if not self.validate_input():
            return
        
        instance.disabled = True
        self.current_btn = instance
        
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()


    def download_video(self):
        """Download video in background thread"""
        import sys
        
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = DevNull()
        sys.stderr = DevNull()

        sent_milestones = set()
        
        try:
            url = self.url_input.text.strip()
            quality = self.quality_spinner.text

            self.send_notification(
                "Harpoon - Download Started",
                f"Quality: {quality}"
            )
            
            self.update_status("Starting download...", (0.2, 0.65, 0.55, 1))
            self.update_progress(5)
            
            download_path = self.get_download_path()
            
            # Ensure directory exists
            if not os.path.exists(download_path):
                os.makedirs(download_path, exist_ok=True)
            
            if quality == 'Best (Recommended)':
                format_str = "best[ext=mp4]/best"
            elif quality == "1080p":
                format_str = "best[height<=1080][ext=mp4]/best[height<=1080]/best"
            elif quality == '720p':
                format_str = "best[height<=720][ext=mp4]/best[height<=720]/best"
            elif quality == '480p':
                format_str = "best[height<=480][ext=mp4]/best[height<=480]/best"
            elif quality == '360p':
                format_str = "best[height<=360][ext=mp4]/best[height<=360]/best"
            elif quality == 'Audio Only':
                format_str = "bestaudio[ext=m4a]/bestaudio/best"
            else:
                format_str = "best[ext=mp4]/best"
            
            def progress_hook(d):
                nonlocal sent_milestones

                try:
                    if d['status'] == 'downloading':
                        percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
                        speed = d.get('_speed_str', 'N/A')
                        clean_percent = ansi_escape.sub('', percent_str).strip()
                        clean_speed = ansi_escape.sub('', speed).strip()
                        
                        try:
                            progress_val = float(clean_percent)
                            self.update_progress(progress_val)

                            milestone = int(progress_val // 25) * 25
                            if milestone in [50] and milestone not in sent_milestones:
                                sent_milestones.add(milestone)
                                self.send_notification(
                                    f"Download {milestone}% Complete",
                                    f"Speed: {clean_speed}"
                                )
                        except:
                            pass
                        
                        self.update_status(f"Downloading: {clean_percent}% • {clean_speed}", (0.2, 0.65, 0.55, 1))
                    
                    elif d['status'] == 'finished':
                        self.update_progress(100)
                        self.update_status("✓ Download complete!", (0.2, 0.65, 0.55, 1))
                except:
                    pass
            
            
            ydl_opts = {
                "format": format_str,
                "outtmpl": os.path.join(download_path, "%(title)s [{quality_tag}].%(ext)s"),
                "nooverwrites": True,  
                "continuedl": True,  
                "quiet": True,
                "no_warnings": True,
                "progress_hooks": [progress_hook],
                "writethumbnail": True,        # Download thumbnail.jpg/png
                "prefer_free_formats": True,
                "retries": 10,
                "fragment_retries": 10,
                "skip_unavailable_fragments": True,
                "http_chunk_size": 10485760,
                "no_check_certificate": True,
                "socket_timeout": 30,             # Faster timeout
                "extractor_retries": 5,  
                "http_headers": {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',}       
            }
            
            # Download
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')[:35]

                self.send_notification(
                    "Download Complete!",
                    f"'{title[:30]}...' saved"
                )

                self.update_status(f"Saved: {title}...", (0.95, 0.75, 0.2, 1))
                self.update_progress(100)
        
        except yt_dlp.utils.DownloadError as e:
            sys.stdout = original_stdout
            error_msg = str(e).lower()
            
            if "429" in error_msg or "too many requests" in error_msg:
                self.send_notification("Download Failed", "Rate limited by YouTube")
                self.update_status("Rate limited. Wait and retry.", (0.7, 0.25, 0.15, 1))
            elif "not available" in error_msg or "unavailable" in error_msg:
                self.send_notification("Download Failed", "Video not available")
                self.update_status("Video unavailable or private", (0.7, 0.25, 0.15, 1))
            else:
                self.send_notification("Download Failed", "An error occurred")
                self.update_status("Download failed", (0.7, 0.25, 0.15, 1))
            
            self.update_progress(0)
            print(f"Download Error: {e}")
        
        except Exception as e:
            sys.stdout = original_stdout
            self.send_notification("Error", "Something went wrong")
            self.update_status("An error occurred", (0.7, 0.25, 0.15, 1))
            self.update_progress(0)
            print(f"Error: {e}")
        
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            Clock.schedule_once(lambda dt: self.enable_button(), 2)

    def enable_button(self):
        """Re-enable download button"""
        if hasattr(self, 'current_btn'):
            self.current_btn.disabled = False

class Harpoon(App):
    def build(self):
        self.title = "Harpoon"

        if platform == 'android':
            Window.softinput_mode = 'below_target'
        else:
            Window.size = (420, 700)

        sm = ScreenManager()
        sm.add_widget(Home(name ="home"))
        #sm.add_widget(Info(name="info"))
        #sm.add_widget(MediaPlayer(name="media"))
        return sm 


if __name__ == "__main__":
    Harpoon().run()