# FROM nvidia/cuda:10.2-cudnn7-devel
FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo curl && \
  rm -rf /var/lib/apt/lists/*

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py

# install dependencies
RUN pip install -U tensorboard cython
RUN pip install -U --user 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN pip install -U --user 'git+https://github.com/facebookresearch/fvcore'

# install detectron2
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
ENV FORCE_CUDA="1"
# This will build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ENV TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"

# add dir
COPY requirements.txt /home/appuser/detectron2_repo
COPY coco.txt /home/appuser/detectron2_repo

# install
RUN pip install --user -r /home/appuser/detectron2_repo/requirements.txt
RUN pip install --user -r /home/appuser/detectron2_repo/coco.txt
RUN pip install --user -e detectron2_repo

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"
WORKDIR /home/appuser/detectron2_repo
ENV PILLOW_VERSION=7.0.0

# add dir
COPY . /home/appuser/detectron2_repo

# Make port 8080 available to the world outside the container
ENV PORT 8080
EXPOSE 8080

# Define environment variable
# ENV NAME World
# ENV GOOGLE_APPLICATION_CREDENTIALS /home/appuser/detectron2_repo/key.json

# CMD python app.py
CMD ["python3", "app.py"] 

