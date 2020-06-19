from pathlib import path

bind = 'unix:/tmp/nginx.socket'
Path('/tmp/app-initialized').touch()
