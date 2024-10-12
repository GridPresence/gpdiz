#
# Copyright Endava Games. All Rights Reserved
#
FROM ubuntu:24.04 AS igorsden
# Non-interactive apt tools behaviour
ENV DEBIAN_FRONTEND=noninteractive

ENV SERVICE_NAME="igorsden"
ENV NEWHOME=/home/$SERVICE_NAME
ENV IGORUID=12345
ENV GID=23456

# Current HCL application versions
ENV TFV=1.9.5
ENV PKRV=1.11.2
# Current terraform-docs application version
ENV TDV=v0.18.0
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

# Need this in case we're building an image on Apple Silicon
ARG AWSCLI_ARCH
# Also need this variation in case we're building an image on Apple Silicon
ARG TFDOCS_ARCH
# Install V.2 of AWS CLI
# While the Ubuntu distro package is still at V.1.x
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWSCLI_ARCH}.zip" -o "awscliv2.zip"; \
    unzip -qq awscliv2.zip; \
    ./aws/install

# Download terraform for linux
RUN wget https://releases.hashicorp.com/terraform/${TFV}/terraform_${TFV}_linux_${TFDOCS_ARCH}.zip ; \
    unzip -o terraform_${TFV}_linux_${TFDOCS_ARCH}.zip ; \
    install terraform /usr/local/bin/terraform
# Download packer for linux
RUN wget https://releases.hashicorp.com/packer/${PKRV}/packer_${PKRV}_linux_${TFDOCS_ARCH}.zip ; \
    unzip -o packer_${PKRV}_linux_${TFDOCS_ARCH}.zip ; \
    install packer /usr/local/bin/packer

# Download and execute the OpenTofu installer script:
RUN wget --secure-protocol=TLSv1_2 --https-only https://get.opentofu.org/install-opentofu.sh -O install-opentofu.sh ; \
    chmod +x install-opentofu.sh ; \
    ./install-opentofu.sh --install-method deb ; \
    rm install-opentofu.sh

# For generating Markdown documentation in Terraform HCL source code
RUN curl -sSLo ./terraform-docs.tar.gz https://terraform-docs.io/dl/${TDV}/terraform-docs-${TDV}-linux-${TFDOCS_ARCH}.tar.gz ; \
    tar -xzf terraform-docs.tar.gz ; \
    install terraform-docs /usr/local/bin/terraform-docs

# Install Go
RUN wget -c https://go.dev/dl/go${GOVER}.linux-${TFDOCS_ARCH}.tar.gz ; \
    tar -C /usr/local -xvzf go${GOVER}.linux-${TFDOCS_ARCH}.tar.gz


# Install local executables for this image
COPY igor_env.sh /tmp/igor_env.sh
RUN install /tmp/igor_env.sh /usr/local/bin/igor_env.sh

COPY igor_execute /tmp/igor_execute
RUN install /tmp/igor_execute /usr/local/bin/igor_execute

COPY igor_python /tmp/igor_python
RUN install /tmp/igor_python /usr/local/bin/igor_python

COPY igor_pkg /tmp/igor_pkg
RUN install /tmp/igor_pkg /usr/local/bin/igor_pkg

COPY igor_build_layer /tmp/igor_build_layer
RUN install /tmp/igor_build_layer /usr/local/bin/igor_build_layer

COPY igor_sphinx /tmp/igor_sphinx
RUN install /tmp/igor_sphinx /usr/local/bin/igor_sphinx

COPY igor_go /tmp/igor_go
RUN install /tmp/igor_go /usr/local/bin/igor_go

COPY igor_hcl /tmp/igor_hcl
RUN install /tmp/igor_hcl /usr/local/bin/igor_hcl

COPY igor_iac /tmp/igor_iac
RUN install /tmp/igor_iac /usr/local/bin/igor_iac

COPY igor_packer /tmp/igor_packer
RUN install /tmp/igor_packer /usr/local/bin/igor_packer

COPY igor_pulumi /tmp/igor_pulumi
RUN install /tmp/igor_pulumi /usr/local/bin/igor_pulumi

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

CMD ["bash", "igor_execute"]
