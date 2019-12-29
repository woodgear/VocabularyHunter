FROM vh-server-base:0.1


WORKDIR /vh
COPY ./ /vh
RUN pip3 install nltk
RUN pip3 install -r ./requirements.txt
RUN cp -r /vh/lib/nltk_data /usr/share/nltk_data
ENTRYPOINT /vh/start.sh
