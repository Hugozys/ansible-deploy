FROM hugozzys/ansible-deploy:latest

ADD main.sh .
COPY export.py /usr/bin/exp
RUN chmod 777 /usr/bin/exp
RUN chmod 777 ./main.sh

ENTRYPOINT ["/main.sh"]