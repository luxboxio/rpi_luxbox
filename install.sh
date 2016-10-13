#!/bin/bash

mkdir /opt/luxbox
cp luxbox_sender.py /opt/luxbox/luxbox_sender.py
cp luxbox_receiver.py /opt/luxbox/luxbox_receiver.py
chmod +x /opt/luxbox/luxbox_sender.py
chmod +x /opt/luxbox/luxbox_receiver.py


mkdir /etc/luxbox

cp luxbox_sender.service //lib/systemd/system/luxbox_sender.service
cp luxbox_receiver.service //lib/systemd/system/luxbox_receiver.service
systemctl daemon-reload
