#!/bin/bash

START_IMAGE="nvcr.io/nvidia/pytorch:22.11-py3"
BUILD_NAME="localdev/nxq/maskdet:22.11-py3"
USERNAME="dev_nxq"
ROOT_DIR="/home/$USERNAME"
#ROOT_DIR="/root"

if [ $1 ]
then
    DOCKER_NAME=$1
    START_CMD="/bin/bash"
else
    DOCKER_NAME="python_dev"
    START_CMD="/bin/bash"
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pushd $SCRIPT_DIR
docker build -f Dockerfile -t $BUILD_NAME \
            --build-arg=BASE_IMAGE=$START_IMAGE \
            --build-arg=USER_NAME=$USERNAME \
            .
popd

if [ -z "$DISPLAY" ]; then
    printf "\tDISPLAY does not exist\n"
    DISPLAYID=$(netstat -x | grep @/tmp/.X11-unix/X | head -n 1 | awk '{ print $8 }' | cut -d'X' -f 3)
    echo "FOUND DISPLAY WITH NUMBER=$DISPLAYID"
    #echo "SET DISPLAY WITH ID = $DISPLAYID"
    export DISPLAY=:$DISPLAYID.0
    echo "SET DISPLAY=$DISPLAY"
    echo "You need to source this file to make DISPLAY=$DISPLAY in current bash shell"
    echo "if you are using remote desktop, you should add non-netwok local connection to xhost"
    echo "Example: xhost +local:"
fi

printf "Run detach docker image with following parameter\n"
printf "\tDOCKER_NAME: $DOCKER_NAME\n"
printf "\tENTRY: $START_CMD\n"
printf "\tBASE_IMAGE: $BUILD_NAME\n"
printf "\tROOT_DIR: $ROOT_DIR\n"
printf "\tDISPLAY = $DISPLAY \n"
# make local directory
# shellcheck disable=SC1101
printf "\tstart new $DOCKER_NAME container\n"

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

mkdir -p ./.cache/$DOCKER_NAME

HOMEDIR=$(realpath ./.cache/$DOCKER_NAME)

touch $HOMEDIR/.bash_history
mkdir -p ${HOMEDIR}/shared
mkdir -p ${HOMEDIR}/.cache
mkdir -p ${HOMEDIR}/.keras
mkdir -p ${HOMEDIR}/.vscode-server
mkdir -p ${HOMEDIR}/.local
mkdir -p ${HOMEDIR}/.ipython


docker run --privileged --rm -itd --init \
           --gpus all \
           --cap-add=SYS_PTRACE \
           --security-opt seccomp=unconfined \
           --volume=$XSOCK:$XSOCK:rw \
           --volume=$XAUTH:$XAUTH:rw \
           --volume=/dev:/dev:rw \
           -v $HOMEDIR/.keras:$ROOT_DIR/.keras \
           -v $HOMEDIR/.cache:$ROOT_DIR/.cache \
           --volume=$HOMEDIR/.bash_history:$ROOT_DIR/.bash_history:rw \
           --volume=$HOMEDIR/.vscode-server:$ROOT_DIR/.vscode-server:rw \
           --volume=$HOMEDIR/.local:$ROOT_DIR/.local:rw \
           -v ${HOMEDIR}/.ipython:$ROOT_DIR/.ipython:rw \
           -v /media/:/media/   \
           -v $HOMEDIR/shared:/shared/ \
           -v $PWD:$PWD \
           -w $PWD \
           --shm-size=2gb \
           --env="XAUTHORITY=${XAUTH}" \
           --env="DISPLAY=${DISPLAY}" \
           --env=TERM=xterm-256color \
           --env=QT_X11_NO_MITSHM=1 \
           --net=host \
           --ipc=host \
           --name=$DOCKER_NAME \
           --user $(id -u):$(id -g)  \
           $BUILD_NAME $START_CMD

sleep 1
docker ps --size | grep $DOCKER_NAME
