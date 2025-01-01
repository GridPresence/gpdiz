#
# Copyright Grid Presence. All Rights Reserved
#
FROM ubuntu:24.04 AS dzbld
ENV DEBIAN_FRONTEND=noninteractive

ENV SERVICE_NAME="dzbld"
ENV NEWHOME=/home/$SERVICE_NAME
ENV IGORUID=4321
ENV GID=1234

# Current Go language version
ENV GOVER=1.22.5

# Repairing the Ubuntu default shell as bash
RUN rm /bin/sh ; \
    ln -s /bin/bash /bin/sh

# Basic package set
RUN apt-get -y update; apt-get -y upgrade
COPY packages.txt /tmp/packages.txt
RUN xargs apt-get -y install < /tmp/packages.txt

# Add some python dependencies
RUN python3 -m pip install --upgrade pip --break-system-packages --ignore-installed
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade -r /tmp/requirements.txt --break-system-packages

# ARG TARG_ARCH
# Install Go
#RUN wget -c https://go.dev/dl/go${GOVER}.linux-${TARG_ARCH}.tar.gz ; \
#    tar -C /usr/local -xvzf go${GOVER}.linux-${TARG_ARCH}.tar.gz


# Install local executables for this image
COPY bldr_* /usr/local/bin/
RUN chmod 755 /usr/local/bin/bldr_*

RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/bin/bash" \
    --home "$NEWHOME" \
    --uid "$IGORUID" \
    "$SERVICE_NAME"
# Move down onto project root directory
WORKDIR $NEWHOME
COPY dot.pylintrc .pylintrc
# Create host FS mount point
RUN mkdir -p $NEWHOME/work
RUN chown -R $SERVICE_NAME:$SERVICE_NAME $NEWHOME
WORKDIR $NEWHOME/work
# Don't want to run as root
USER $SERVICE_NAME

CMD ["bash", "./execute"]
