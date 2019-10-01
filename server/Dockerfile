FROM python:3.6-slim
WORKDIR /vh

RUN rm /etc/apt/sources.list && echo "deb http://mirrors.aliyun.com/debian buster main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian buster-proposed-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian-security/ buster/updates main non-free contrib" >> /etc/apt/sources.list 

RUN apt update && apt install gcc -y
RUN mkdir ~/.pip &&  echo "[global]\nindex-url = https://mirrors.aliyun.com/pypi/simple" > ~/.pip/pip.conf

RUN cat ~/.pip/pip.conf

RUN pip3 install nltk
RUN python3 -c "import nltk; nltk.download('punkt')"
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
    && sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
    && apt-get update 
RUN apt install gcc -y
COPY ./ /vh

RUN pip3 install -r ./requirements.txt

ENTRYPOINT /vh/start.sh 

