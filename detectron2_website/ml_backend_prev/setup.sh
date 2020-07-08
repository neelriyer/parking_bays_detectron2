pip3 install --user cython==0.29.15 &&\
pip3 install --user  -r requirements.txt &&\
pip3 install --user 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI' &&\
pip3 install --user 'git+https://github.com/facebookresearch/detectron2.git'