FROM waleedka/modern-deep-learning:latest

# install stuff
RUN apt update && apt install -y python3-dev git

RUN git clone https://github.com/matterport/Mask_RCNN repo
RUN cd repo && pip3 install --upgrade pip && pip install -r requirements.txt && \
pip3 install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

COPY test.py /root/repo/

RUN git clone https://github.com/cocodataset/cocoapi.git coco
RUN cd coco/PythonAPI && python3 setup.py install

ENV DISPLAY :0
# RUN python3 repo/test.py

# add dir
COPY requirements.txt /root

# install
RUN pip install -r requirements.txt
ENV PILLOW_VERSION=6.2.0
ENV PORT 8080

COPY . /root
EXPOSE 8080
EXPOSE 80
ENV NAME World

CMD ["python3", "app.py"]

