FROM python:3.9-slim

WORKDIR /app

# install chromium and driver
RUN apt-get update && apt-get install -y \
    vim \
    tzdata \
    cron

# update timezone
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

COPY . /app
COPY scripts/keyword_crontab /etc/cron.d/crontab

RUN pip3 install --no-cache-dir -r /app/services/keyword_service/requirements.txt

RUN chmod 0644 /etc/cron.d/crontab

#CMD ["tail", "-f", "/dev/null"]
CMD ["/usr/sbin/cron", "-f"]
