#!/bin/bash
# Sync pipeline_issue_250 to Raspberry Pi (excludes __pycache__, .pyc, .hef)

PI="root@10.21.220.158"
SRC="$(dirname "$0")/"
DST="/home/pipeline_issue_250/"

rsync -avz \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.hef' \
  --exclude='sync_to_pi.sh' \
  "$SRC" "$PI:$DST"
