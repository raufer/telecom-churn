FROM python:3.7-slim

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

RUN pip install keras==2.2.4 && \
    pip install seldon-core==0.3.1 && \
    pip install awscli==1.16.197

RUN pip install argparse==1.4.0 && \
    pip install awscli==1.16.197

RUN pip install pandas==0.25.0 && \
    pip install scikit-learn==0.21.2 && \
    pip install xgboost==0.90

RUN apt-get update -y && \
    apt-get install libgomp1 -y

COPY . /
WORKDIR /

EXPOSE 9000

# Define environment variable
ENV MODEL_NAME ChurnModel
ENV API_TYPE REST
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE
