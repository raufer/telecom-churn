FROM dockershelf/python:3.6

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

RUN apt-get update -y && \
    apt-get install libgomp1 -y

RUN apt-get install build-essential autoconf libtool pkg-config python-opengl python-pil python-pyrex python-pyside.qtopengl qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev && \
    apt-get install gcc -y && \
    apt-get install nodejs -y && \
    apt-get install npm -y

RUN pip install argparse==1.4.0 && \
    pip install awscli==1.16.197 && \
    pip install pandas==0.25.0 && \
    pip install scikit-learn==0.21.2 && \
    pip install xgboost==0.90 && \
    pip install plotly==4.0.0

COPY . /app

ENTRYPOINT [ "python3.6", "/app/evaluate.py" ]
