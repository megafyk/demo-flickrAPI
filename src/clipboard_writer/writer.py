import clipboard
import time


class ClipboardWriter(object):
    # Clipboard's timer countdown
    CLIP_TIMER = 0.2

    def __init__(self, filepath):
        self._filepath = filepath
        self._temp_clip = ""
        # Clear clipboard
        clipboard.copy("")

    def run(self):
        """Run clipboard writer.
        Read and write url from clipboard every CLIP_TIMER tick.
        
        """
        try:
            while True:
                if self.is_has_new_clipboard(self._temp_clip):
                    url = self.read_clipboard()
                    print("Has new url: %s", url)
                    self.write_to_file(url)
                print("Waiting...")
                time.sleep(self.CLIP_TIMER)
        except KeyboardInterrupt:
            pass

    @staticmethod
    def is_has_new_clipboard(temp_clip):
        """Detech new url from clipboard.
        
        Parameters
        ----------
        temp_clip : str
            Url from clipboard.

        """
        return temp_clip != clipboard.paste()

    def read_clipboard(self):
        """Set new clipboard to temp
        
        Returns
        -------
        _temp_clip : str
            Temporary clipboard

        """
        self._temp_clip = clipboard.paste()
        return self._temp_clip

    def write_to_file(self, url):
        """Write url to file  
        
        Parameters
        ----------
        url : str
            Url

        """
        try:
            with open(self._filepath, 'a') as f:
                f.write(url + '\n')
                f.close()
        except Exception as ex:
            print(ex)
