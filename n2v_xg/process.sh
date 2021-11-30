#!/bin/bash

# echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef" >> log/logs.csv

# for dim in 32 64 128 256 
# do
#     for epochs in 1 3 5 10
#     do
#         for length in 40 80 120
#         do
#             for walk in 5 10 20
#             do
#                 echo -n "${dim},${epochs},${length},${walk}," >> log/logs.csv
#                 emb_filename="csv/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}.emb.csv"
#                 es_filename="csv/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}.emb_out.csv"
#                 python boost.py $emb_filename $es_filename >> log/logs.csv
#             done
#         done
#     done
#done



echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef" >> log/logs2.csv

for dim in 32 64
do
    for epochs in 5 10
    do
        for length in 80 120
        do
            for walk in 10 20
            do
                for cont in 5 10 20
                do
                    for retpar in 0.5 1 1.5
                    do
                        echo -n "${dim},${epochs},${length},${walk},${cont},${retpar}," >> log/logs2.csv
                        emb_filename="csv/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                        es_filename="csv/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                        python boost.py $emb_filename $es_filename >> log/logs2.csv
                    done
                done
            done
        done
    done
done