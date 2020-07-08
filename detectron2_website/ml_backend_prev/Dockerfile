FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04 
# TODO: do we really need cuda?

# install stuff
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

# install using script
COPY setup.sh /home/appuser
COPY requirements.txt /home/appuser
RUN pip3 install cython==0.29.15 &&\
pip3 install -r requirements.txt &&\
pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI' &&\
pip3 install 'git+https://github.com/facebookresearch/detectron2.git'


# install detectron2
# RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
# ENV FORCE_CUDA="1"
# # This will build detectron2 for all common cuda architectures and take a lot more time,
# # because inside `docker build`, there is no way to tell which architecture will be used.
# ENV TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"

# Set a fixed model cache directory.
# ENV FVCORE_CACHE="/tmp"
# WORKDIR /home/appuser/detectron2_repo
ENV PILLOW_VERSION=7.0.0

# add dir
COPY . /home/appuser

# Make port 8080 available to the world outside the container
# ENV PORT 8080
ENV PORT 5000
# EXPOSE 8080
EXPOSE 5000

# environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=api
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5000
ENV SECRET_KEY=cherry

# Define environment variable
# ENV NAME World
# ENV GOOGLE_APPLICATION_CREDENTIALS /home/appuser/detectron2_repo/key.json
# CMD ["python3", "api/ml/ml.py"] 

RUN pip install python-dotenv
CMD ["flask", "run"]


