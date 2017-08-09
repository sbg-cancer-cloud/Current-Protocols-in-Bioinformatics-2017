# Define base image
FROM ubuntu:14.04


# Install required packages
RUN apt-get update && apt-get install -y \
        wget \
	build-essential \
	zlib1g-dev \
	python \
	r-base \
	perl \
	libcam-pdf-perl


#Install bedtools
WORKDIR /opt
RUN wget https://github.com/arq5x/bedtools2/releases/download/v2.25.0/bedtools-2.25.0.tar.gz
RUN tar zxvf bedtools-2.25.0.tar.gz
RUN rm -rf bedtools-2.25.0.tar.gz
WORKDIR /opt/bedtools2
RUN make

#Install tabix
WORKDIR /opt
RUN wget http://downloads.sourceforge.net/project/samtools/tabix/tabix-0.2.6.tar.bz2
RUN tar jxvf tabix-0.2.6.tar.bz2
WORKDIR /opt/tabix-0.2.6
RUN make

#Install TFPM
WORKDIR /opt
RUN wget http://bioinfo.lifl.fr/tfm-pvalue/TFM-Pvalue.tar.gz
RUN tar zxvf TFM-Pvalue.tar.gz
WORKDIR /opt/TFM-Pvalue
RUN  sed '15 a\
\#include <getopt.h>' TFMpvalue.cpp > temp.cpp
RUN mv temp.cpp TFMpvalue.cpp
RUN make

#Install bigWigAverageOverBed
WORKDIR /opt
RUN wget http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bigWigAverageOverBed
RUN chmod +x bigWigAverageOverBed

#Install Parallel::ForkManager
RUN cpan Parallel::ForkManager

#Install FunSeq2
WORKDIR /opt
RUN wget http://funseq2.gersteinlab.org/static/download/funseq2.1.2.tar.bz2
RUN tar jxvf funseq2.1.2.tar.bz2


# Add to path
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt:/opt/bedtools-2.17.0/bin/:/opt/TFM-Pvalue:/opt/tabix-0.2.6:/opt/funseq2-1.2/
WORKDIR /opt/funseq2-1.2

COPY Dockerfile /opt/ 
MAINTAINER Anurag Sethi, Seven Bridges, <anurag.sethi@sbgenomics.com>

