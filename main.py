import os, time
from recorder import Recorder

PIPE_PATH = '/tmp/recpipe'
FILE_NAME = time.strftime("%Y-%m-%d_%H-%M-%S") + '.wav'
# timeout in seconds
TIMEOUT = 5

if not os.path.exists(PIPE_PATH):
    os.mkfifo(PIPE_PATH)
pipe_fd = lambda: os.fdopen(os.open(PIPE_PATH, os.O_RDONLY | os.O_NONBLOCK))

rec = Recorder(channels=2)
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
    record.stop_recording()
    print('audio captured!')

