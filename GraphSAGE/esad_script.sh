#!/bin/bash

Models="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"

for model in $Models
do
    echo "Unsupervised | Model : ${model}"
    python -m graphsage.unsupervised_train --train_prefix ./example_data/sc_eppugnn --model ${model} --validate_iter 100 --gpu 0
done

SupModels="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq"

for model in $SupModels
do
    echo "Supervised | Model : ${model}"
    python -m graphsage.supervised_train --train_prefix ./example_data/sc_eppugnn --model ${model} --gpu 0
done
