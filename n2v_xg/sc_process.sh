organism="$1"

echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/${organism}_last1.csv
echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/${organism}_last2.csv
echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/${organism}_last3.csv
echo "Dimension,Epochs,Length_of_Walk,Num_Walks,Context_Size,Return_Hyperparam,Accuracy,Balanced_Accuracy,F1_Score,Matthews_Corrcoef,Roc_Auc,Precision,Recall" > log/${organism}_last4.csv

for dim in 32 64
do
    for epochs in 1 3
    do
        for length in 80 120
        do
            for walk in 10 20
            do
                for cont in 10 20
                do
                    for retpar in 0.5 1 2
                    do
                        FILE="${PWD}/emb/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb"
                        if [ -f $FILE ]; then
                            echo "$FILE exists"
                            python3 subcellular_localization.py $FILE $organism
                            python3 gene_expression.py $FILE $organism &
                            wait
                            for option in 1 2 3 4
                            do
                                python3 embedding.py $FILE $option $organism
                                log_file="log/${organism}_last${option}.csv"
                                echo -n "${dim},${epochs},${length},${walk},${cont},${retpar}," >> $log_file
                                if [[ $option -eq 1 ]]
                                then
                                    emb_filename="csv_imp/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file                                
                                elif [[ $option -eq 2 ]]
                                then
                                    emb_filename="csv_imp_sl/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp_sl/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                                elif [[ $option -eq 3 ]]
                                then
                                    emb_filename="csv_imp_ge/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp_ge/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                                else
                                    emb_filename="csv_imp_sl_ge/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb.csv"
                                    es_filename="csv_imp_sl_ge/${organism}_ppi_emb_d${dim}_e${epochs}_l${length}_w${walk}_k${cont}_p${retpar}.emb_out.csv"
                                    python3 boost.py $emb_filename $es_filename $option >> $log_file
                               fi
                           done
                        fi
                    done
                done
            done
        done
    done
done
