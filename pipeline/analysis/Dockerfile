FROM dockershelf/python:3.6

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

RUN apt-get update -y && \
    apt-get install libgomp1 -y

RUN pip install argparse==1.4.0 && \
    pip install awscli==1.16.197 && \
    pip install pandas==0.25.0 && \
    pip install scikit-learn==0.21.2 && \
    pip install xgboost==0.90 && \
    pip install plotly==4.0.0

COPY . /app

ENTRYPOINT [ "python3.6", "/app/analysis.py" ]
