import csv

overall_filename = 'cities_short.csv'
header1 = ['date','rent_1_median','rent_1_count','rent_2_median','rent_2_count','rent_3_median','rent_3_count','rent_4_median','rent_4_count','rent_5_median','rent_5_count','rent_6_median','rent_6_count']
header2 = ['home_1_median','home_1_count','home_1_median_hoa','hoa_1_bd_median','home_1_count_hoa','home_1_both_median','home_1_count+home_1_count_hoa','home_2_median','home_2_count','home_2_median_hoa','hoa_2_bd_median','home_2_count_hoa','home_2_both_median','home_2_count+home_2_count_hoa','home_3_median','home_3_count','home_3_median_hoa','hoa_3_bd_median','home_3_count_hoa','home_3_both_median','home_3_count+home_3_count_hoa','home_4_median','home_4_count','home_4_median_hoa']
header3 = ['hoa_4_bd_median','home_4_count_hoa','home_4_both_median','home_4_count+home_4_count_hoa','home_5_median','home_5_count','home_5_median_hoa','hoa_5_bd_median','home_5_count_hoa','home_5_both_median','home_5_count+home_5_count_hoa','home_6_median','home_6_count','home_6_median_hoa','hoa_6_bd_median','home_6_count_hoa','home_6_both_median','home_6_count+home_6_count_hoa']
header6 = ['home_1_median_condo','home_1_count_condo','home_1_median_hoa_condo','hoa_1_bd_median_condo','home_1_count_hoa_condo','home_1_both_median_condo','home_1_count_condo+home_1_count_hoa_condo','home_2_median_condo','home_2_count_condo','home_2_median_hoa_condo','hoa_2_bd_median_condo','home_2_count_hoa_condo','home_2_both_median_condo','home_2_count_condo+home_2_count_hoa_condo','home_3_median_condo','home_3_count_condo','home_3_median_hoa_condo','hoa_3_bd_median_condo','home_3_count_hoa_condo','home_3_both_median_condo','home_3_count_condo+home_3_count_hoa_condo','home_4_median_condo','home_4_count_condo','home_4_median_hoa_condo']
header7 = ['hoa_4_bd_median_condo','home_4_count_hoa_condo','home_4_both_median_condo','home_4_count_condo+home_4_count_hoa_condo','home_5_median_condo','home_5_count_condo','home_5_median_hoa_condo','hoa_5_bd_median_condo','home_5_count_hoa_condo','home_5_both_median_condo','home_5_count_condo+home_5_count_hoa_condo','home_6_median_condo','home_6_count_condo','home_6_median_hoa_condo','hoa_6_bd_median_condo','home_6_count_hoa_condo','home_6_both_median_condo','home_6_count_condo+home_6_count_hoa_condo']
header8 = ['home_1_median_house','home_1_count_house','home_1_median_hoa_house','hoa_1_bd_median_house','home_1_count_hoa_house','home_1_both_median_house','home_1_count_house+home_1_count_hoa_house','home_2_median_house','home_2_count_house','home_2_median_hoa_house','hoa_2_bd_median_house','home_2_count_hoa_house','home_2_both_median_house','home_2_count_house+home_2_count_hoa_house','home_3_median_house','home_3_count_house','home_3_median_hoa_house','hoa_3_bd_median_house','home_3_count_hoa_house','home_3_both_median_house','home_3_count_house+home_3_count_hoa_house','home_4_median_house','home_4_count_house','home_4_median_hoa_house']
header9 = ['hoa_4_bd_median_house','home_4_count_hoa_house','home_4_both_median_house','home_4_count_house+home_4_count_hoa_house','home_5_median_house','home_5_count_house','home_5_median_hoa_house','hoa_5_bd_median_house','home_5_count_hoa_house','home_5_both_median_house','home_5_count_house+home_5_count_hoa_house','home_6_median_house','home_6_count_house','home_6_median_hoa_house','hoa_6_bd_median_house','home_6_count_hoa_house','home_6_both_median_house','home_6_count_house+home_6_count_hoa_house']
header10 = ['home_1_median_th','home_1_count_th','home_1_median_hoa_th','hoa_1_bd_median_th','home_1_count_hoa_th','home_1_both_median_th','home_1_count_th+home_1_count_hoa_th','home_2_median_th','home_2_count_th','home_2_median_hoa_th','hoa_2_bd_median_th','home_2_count_hoa_th','home_2_both_median_th','home_2_count_th+home_2_count_hoa_th','home_3_median_th','home_3_count_th','home_3_median_hoa_th','hoa_3_bd_median_th','home_3_count_hoa_th','home_3_both_median_th','home_3_count_th+home_3_count_hoa_th','home_4_median_th','home_4_count_th','home_4_median_hoa_th']
header11 = ['hoa_4_bd_median_th','home_4_count_hoa_th','home_4_both_median_th','home_4_count_th+home_4_count_hoa_th','home_5_median_th','home_5_count_th','home_5_median_hoa_th','hoa_5_bd_median_th','home_5_count_hoa_th','home_5_both_median_th','home_5_count_th+home_5_count_hoa_th','home_6_median_th','home_6_count_th','home_6_median_hoa_th','hoa_6_bd_median_th','home_6_count_hoa_th','home_6_both_median_th','home_6_count_th+home_6_count_hoa_th']

header100 = header1 + header2 + header3 + header6 + header7 + header8 + header9 + header10 + header11
print header100
csv_list = []
column = line = 0

while True:
    line += 1
    csv_file = open(overall_filename,'rb')
    csv_reader = csv.reader(csv_file, delimiter = ',')
    cities_states = []
    for row in csv_reader:
        cities_states.append(row)
    craigs_url = cities_states[line][column]
    neigh = cities_states[line][column+1]
    city = cities_states[line][column+2]
    state = cities_states[line][column+3]
    today_file = cities_states[line][column+4]

    if neigh != '':
        folder_and_file = craigs_url + str("/") + neigh + ".csv"
    else:
        folder_and_file = craigs_url + str("/") + city + ".csv"
    print folder_and_file

    with open(folder_and_file,"a") as f:
         writer = csv.writer(f, lineterminator='\n')
         writer.writerow(header100)
         f.close()
