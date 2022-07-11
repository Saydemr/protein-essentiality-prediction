organism="$1"
for option in 0 1 2 3 4
do
    echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Inout_Hyperparam,Accuracy,std,F1_Score,std,Roc_Auc,std,Precision,std,Recall,std" > log/${organism}_results_${option}.csv
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
                                FILE="${PWD}/emb/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}_q${inout}.emb"
                                if [ -f $FILE ]; then
                                    echo "$FILE exists"

                                    if [ $option != 0 ]; then 
                                        python3 reorder.py $FILE $organism
                                    fi
                                    python3 embedding.py ${FILE} ${option} ${organism}
                                    log_file="log/${organism}_results_${option}.csv"
                                    echo -n "${dim},${epochs},${length},${walk},${cont},${retpar},${inout}," >> $log_file
                                    
                                    emb_filename="csv_${option}/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}_q${inout}.emb.csv"
                                    es_filename="csv_${option}/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}_q${inout}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                                fi
                            done
                        done
                    done
                done
            done
        done
    done
done
