FROM ubuntu:20.04
ENV ROOT_DIR /usr/local

USER root

RUN apt-get update && apt-get install -y \
	libgeos-dev \
	git \
	vim \ 
	python3-pip 

RUN apt-get install -y curl 
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash
RUN apt-get install nodejs


RUN useradd -ms /bin/bash developer
USER developer
WORKDIR /home/developer

RUN pip install --user \
	pyyaml \
	bac0 \ 
	brickschema 

#RUN python3 -m pip install --user buildingspy@git+https://github.com/lbl-srg/buildingspy.git@v2.1.0

RUN mkdir git && cd git && \
    mkdir buildings && cd buildings && git clone https://github.com/lbl-srg/modelica-buildings.git && cd modelica-buildings && cd ../.. && \
    mkdir boptest && cd boptest && git clone https://github.com/ibpsa/project1-boptest.git && cd project1-boptest && git checkout 3a27ad8e50954465597c683182ae0959d844af37 && cd ../.. && \
    mkdir m2j && cd m2j && git clone https://github.com/lbl-srg/modelica-json.git && cd modelica-json && git checkout dc7692fc360a15f54428e6ae10526f5229439751 && npm install && cd ../..
    #mkdir ideas && cd ideas && git clone https://github.com/open-ideas/IDEAS && cd ..
    #mkdir pyfunnel && cd pyfunnel && git clone https://github.com/lbl-srg/funnel.git

#RUN rm -rf $WORKDIR/git/buildings/modelica-buildings/Buildings/Examples/VAVReheat && cp -R /mnt/shared/simulated-digital-twin/test/Buildings/Examples/* $WORKDIR/git/buildings/modelica-buildings/Buildings/Examples/

WORKDIR $ROOT_DIR

#ENV JMODELICA_HOME $ROOT_DIR/JModelica
#ENV IPOPT_HOME $ROOT_DIR/Ipopt-3.12.4
#ENV SUNDIALS_HOME $JMODELICA_HOME/ThirdParty/Sundials
#ENV SEPARATE_PROCESS_JVM /usr/lib/jvm/java-8-openjdk-amd64/
#ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
#ENV PYTHONPATH $PYTHONPATH:$HOME/git/mpcpy/MPCPy:$JMODELICA_HOME/Python:$JMODELICA_HOME/Python/pymodelica:$HOME/git/pyfunnel/funnel/bin
ENV MODELICAPATH $MODELICAPATH:$HOME/git/buildings/modelica-buildings
ENV MODELICAJSONPATH $HOME/git/m2j/modelica-json

