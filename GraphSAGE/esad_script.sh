#!/bin/bash

SupModels="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq"


for identity_dim in 64 0
do
    for lr in 0.01 0.005 0.001 0.05
    do
        for model in $SupModels
        do
            echo "Identity Dim : ${identity_dim} | Learning Rate : ${lr} | Model : ${model}"
            my_dir="king_esad-supervised/id${identity_dim}_lr${lr}"
            mkdir -p ${my_dir}
            python -m graphsage.supervised_train --train_prefix ./example_data/sc_eppugnn --model ${model} --identity_dim ${identity_dim} --learning_rate ${lr} --validate_iter 10 --base_log_dir ${my_dir}  --gpu 0
        done
    done
done

Models="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"

for identity_dim in 64 0
do
    for lr in 0.01 0.005 0.001 0.05
    do
        for model in $Models
        do
            echo "Identity Dim : ${identity_dim} | Learning Rate : ${lr} | Model : ${model}"
            my_dir="king_esad/id${identity_dim}_lr${lr}"
            mkdir -p ${my_dir}
            python -m graphsage.unsupervised_train --train_prefix ./example_data/sc_eppugnn --model ${model} --identity_dim ${identity_dim} --learning_rate ${lr} --validate_iter 10 --base_log_dir ${my_dir}  --gpu 0
        done
    done
done
