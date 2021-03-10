# Use working python3 opencv docker
FROM jjanzic/docker-python3-opencv

# Copy files and install dependencies
COPY requirements.txt /
COPY play_ur.py /
COPY play_manual.py /
COPY detect_board.py /
COPY ConnectFour /ConnectFour
RUN pip install -r requirements.txt

# The following command will execute "python ./play_ur.py".
CMD [ "python", "-u", "./play_ur.py" ]