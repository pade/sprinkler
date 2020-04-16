#!/bin/sh

WORK_DIR=$HOME/sprinkler
BRANCH=deploy

if [ ! -d $WORK_DIR ] ; then
    git clone https://github.com/pade/sprinkler.git $WORK_DIR
else
    git -C $WORK_DIR pull
fi
git -C $WORK_DIR checkout $BRANCH

cd $WORK_DIR && pipenv install
sudo cp $WORK_DIR/scripts/sprinkler.service /etc/systemd/system
sudo systemctl stop sprinkler.service
sudo systemctl enable sprinkler.service
sudo systemctl start sprinkler.service
sudo systemctl daemon-reload



