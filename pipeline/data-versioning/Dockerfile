FROM dockershelf/python:3.6

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

RUN pip install argparse==1.4.0 && \
    pip install awscli==1.16.197

RUN pip install pandas==0.25.0 && \
    pip install scikit-learn==0.21.2

COPY . /app

ENTRYPOINT [ "python", "/app/data_versioning.py" ]
