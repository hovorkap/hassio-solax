ARG BUILD_FROM
FROM $BUILD_FROM

ARG serial

# Install requirements for add-on
RUN apk add --no-cache \
    python3 py3-pip eudev git
RUN pip3 install --quiet toml pymodbus==2.5.3 Twisted influxdb-client paho-mqtt pyyaml

WORKDIR /solax
COPY src/ /solax/

copy config-solax.toml config.toml

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

