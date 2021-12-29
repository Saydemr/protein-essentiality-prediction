import os

models = ['gcn', 'graphsage_maxpool', 'graphsage_mean', 'graphsage_meanpool', 'graphsage_seq']

with open('./log/logs_last_sup.csv', 'w+') as log_csv:
    log_csv.write('Model,Class,F1_Micro,F1_Macro,Loss,TestorVal\n')
    for model in models:
        for i in range(1,8):
            val_txt  = './runs/' + str(i) + '/sup-example_data/' + model + '_small_0.0100/val_stats.txt'
            test_txt = './runs/' + str(i) + '/sup-example_data/' + model + '_small_0.0100/test_stats.txt'

            if os.path.isfile(val_txt) and os.path.isfile(test_txt):
                with open(val_txt, 'r') as val_txt:
                    with open(test_txt, 'r') as test_txt:
                        val_line = val_txt.readline().strip().replace('=', ' ').split()
                        test_line = test_txt.readline().strip().replace('=', ' ').split()
                        log_csv.write(str(i) + ',' + model + ',' + test_line[1] + ',' + test_line[3] + ',' + test_line[5] + ',Test\n')
                        log_csv.write(str(i) + ',' + model + ',' + val_line[1] + ',' + val_line[3] + ',' + val_line[5] + ',Val\n')