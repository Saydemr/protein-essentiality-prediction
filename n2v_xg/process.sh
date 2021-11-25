#!/bin/bash

for dim in 32 
do
    for epochs in 10
    do
        for length in 120
        do
            for walk in 5 10 20
            do
                ./node2vec -i:graph/ppi_graph.txt -o:emb/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}.emb -d:${dim} -e:${epochs} -l:${length} -r:${walk}
            done
        done
    done
done

for dim in 32 64 128 256 
do
    for epochs in 1 3 5 10
    do
        for length in 40 80 120
        do
            for walk in 5 10 20
            do
                $filename = "emb/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}.emb"
                python emb_essentiality.py $filename
            done
        done
    done
done

for dim in 32 64 128 256 
do
    for epochs in 1 3 5 10
    do
        for length in 40 80 120
        do
            for walk in 5 10 20
            do
                $emb_filename = "csv/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}.emb.csv"
                $es_filename  = "csv/ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}.emb_out.csv"
                python booster.py $emb_filename $es_filename
            done
        done
    done
done