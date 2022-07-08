#!/bin/bash
organism="$1"

for dim in 32 64 128
do
    for epochs in 1 3
    do
        for length in 40 80
        do
            for walk in 15 20
            do
                for cont in 10 15
                do
                    for retpar in 0.5 1 1.5
                    do
                        for inout in 0.5 1 1.5
                        do
                            ./node2vec -i:../data/${organism}_ppi_graph.txt -o:emb/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}_q${inout}.emb -d:${dim} -e:${epochs} -l:${length} -r:${walk} -k:${cont} -p:${retpar} -q:${inout}
                        done
                    done
                done
            done
        done
    done
done
