#!/bin/bash
# one test cell: pick table -> rule (first) -> announce -> run -> result -> beliefs
set -e
cd /home/user/eda-routine/runs/2026-10-05_crypto-101alphas
PY=../../.venv/bin/python
NN=$1; H=$2; SL=$3
$PY code/pick.py > code/pick_$(printf %02d $NN).md
$PY code/write_rule.py $NN $H $SL
sleep 1
$PY code/cell_test.py $NN $H $SL
$PY code/update_beliefs.py $NN
