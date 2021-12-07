#!/bin/bash

Models="gcn graphsage_maxpool graphsage_mean graphsage_meanpool graphsage_seq n2v"


for epochs in 10 20 30
do
    for validate_iter in 10 20
    do
        for identity_dim in 0 32 64 128
        do            
            for model in $Models
            do
                mkdir -p "king_esad/$model/$epochs/$validate_iter/$identity_dim"
                python -m graphsage.unsupervised_train --train_prefix ./example_data/eppugnn --model ${model} --train_prefix ${train_prefix} --epochs ${epochs} --identity_dim ${identity_dim} --validate_iter ${validate_iter} --max_total_steps 600 --base_log_dir "./king_esad/$model/$epochs/$validate_iter/$identity_dim" --gpu 0
            done
        done
    done
done

for epochs in 10 20 30
do
    for validate_iter in 10 20
    do
        for identity_dim in 0 32 64 128
        do            
            for model in $Models
            do
                mkdir -p "king_esad_supervised/$model/$epochs/$validate_iter/$identity_dim"
                python -m graphsage.supervised_train --train_prefix ./example_data/eppugnn --model ${model} --train_prefix ${train_prefix} --epochs ${epochs} --identity_dim ${identity_dim} --validate_iter ${validate_iter} --sigmoid --max_total_steps 600 --base_log_dir "./king_esad/$model/$epochs/$validate_iter/$identity_dim" --gpu 0
            done
        done
    done
done