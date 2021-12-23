#!/bin/bash

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
                        ./node2vec -i:graph/sc_ppi_graph.txt -o:emb/sc_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb -d:${dim} -e:${epochs} -l:${length} -r:${walk} -k:{cont} -p:{retpar}
                    done
                done
            done
        done
    done
done
