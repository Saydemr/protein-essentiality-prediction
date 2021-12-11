#!/bin/bash

SupModels="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq"

for epochs in 10 20 30
do
    for batch_size in 16 32 64 128
    do
        for identity_dim in 64 128 32 0
        do
            for lr in 0.01 0.005 0.001 0.05
            do
                for model in $SupModels
                do
                    my_dir="king_esad-supervised/e${epochs}_b${batch_size}_id${identity_dim}_lr{lr}"
                    mkdir -p ${my_dir}
                    python -m graphsage.supervised_train --train_prefix ./example_data/eppugnn --model ${model} --epochs ${epochs} --identity_dim ${identity_dim} --learning_rate ${lr} --base_log_dir ${my_dir} --max_total_steps 10100 --gpu 0
                done
            done
        done
    done
done

Models="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"

for epochs in 10 20 30
do
    for batch_size in 16 32 64 128
    do
        for identity_dim in 64 128 32 0
        do
            for lr in 0.01 0.005 0.001 0.05
            do
                for model in $Models
                do
                    my_dir="king_esad/e${epochs}_b${batch_size}_id${identity_dim}_lr{lr}"
                    mkdir -p ${my_dir}
                    python -m graphsage.unsupervised_train --train_prefix ./example_data/eppugnn --model ${model} --epochs ${epochs} --identity_dim ${identity_dim} --learning_rate ${lr} --base_log_dir ${my_dir} --max_total_steps 10100 --gpu 0
                done
            done
        done
    done
done
