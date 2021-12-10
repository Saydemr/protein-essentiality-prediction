#!/bin/bash

Models="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"


for epochs in 10 20 30
do
    for validate_iter in 10 20
    do
        for identity_dim in 64 128 32 0
        do
            for model in $Models
            do
                my_dir="king_esad/e${epochs}_iter${validate_iter}_id${identity_dim}"
                mkdir -p ${my_dir}
                python -m graphsage.unsupervised_train --train_prefix ./example_data/eppugnn --model ${model} --epochs ${epochs} --identity_dim ${identity_dim} --validate_iter ${validate_iter} --base_log_dir ${my_dir} --max_total_steps 600 --gpu 0
            done
        done
    done
done


SupModels="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq"

for epochs in 10 20 30
do
    for validate_iter in 10 20
    do
        for identity_dim in 64 128 32 0
        do
            for model in $SupModels
            do
                my_dir="king_esad_supervised/e${epochs}_iter${validate_iter}_id${identity_dim}"
                mkdir -p ${my_dir}
                python -m graphsage.supervised_train --train_prefix ./example_data/eppugnn --model ${model} --epochs ${epochs} --identity_dim ${identity_dim} --validate_iter ${validate_iter} --base_log_dir ${my_dir} --max_total_steps 600 --gpu 0
            done
        done
    done
done
