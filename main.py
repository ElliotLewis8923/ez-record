import os, time
import subprocess
from recorder import Recorder

dir = os.getenv('EZ_REC_PATH')
if not dir:
    dir = os.path.dirname(os.path.realpath(__file__)) + '/'

PIPE_PATH = '/tmp/recpipe'
FILE_NAME = dir + time.strftime("%Y-%m-%d_%H-%M-%S") + '.wav'
# timeout in seconds
TIMEOUT = 60
# number of input channels
CHANNELS = 2

def run():
    if os.path.exists(PIPE_PATH):
        subprocess.call(['echo "stop" > ' + PIPE_PATH], shell=True)
        return

    os.mkfifo(PIPE_PATH)
    pipe_fd = lambda: os.fdopen(os.open(PIPE_PATH, os.O_RDONLY | os.O_NONBLOCK))

    rec = Recorder(channels=CHANNELS)
    write_stream = lambda: rec.open(FILE_NAME, 'wb')

    with write_stream() as record, pipe_fd() as pipe:
        record.start_recording()
        print('start capture...')
        start = time.time()
        while True:
            try:
                elapsed = time.time() - start
                if elapsed > TIMEOUT:
                    print('timed out')
                    break
                pipe.read()
            except IOError: 
                break
        os.remove(PIPE_PATH)
        record.stop_recording()
        print('audio captured!')

if __name__ == '__main__':
    run()

