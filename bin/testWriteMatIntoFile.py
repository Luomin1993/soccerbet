import csv


mat = [[0.0, 0.0, 1.0], [0.5, 0.0, 0.5], [1.22, 6.63, 13.81], ['55.1', '19.8', '25.1'], ['100', '57', '45'], [3.4, 0, 1.5], [2.0, 0, 0.2], [3.4400000000000004, 0, 0.25], [4.0, 0, 0.16000000000000003]];

csvfile = file('Mat.csv', 'a+')

writer = csv.writer(csvfile)
m = len(mat)
writer.writerow(' ')
for i in range(m):
    writer.writerow(mat[i])
csvfile.close()
