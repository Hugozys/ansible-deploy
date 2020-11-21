FROM hugozzys/ansible-deploy:latest

COPY run.py /usr/bin/run_play
RUN chmod 777 /usr/bin/run_play

ENTRYPOINT ["run_play"]