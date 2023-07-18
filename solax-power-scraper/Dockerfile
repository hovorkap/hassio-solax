ARG BUILD_FROM
FROM $BUILD_FROM

ARG serial

# Install requirements for add-on
RUN apk add --no-cache \
    python3 py3-pip eudev git
RUN pip3 install toml pymodbus==2.5.3 Twisted influxdb-client

WORKDIR /solax
RUN git clone https://github.com/hovorkap/PowerScraper.git .

# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
# WORKDIR /data

copy config-solax.toml config.toml

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

