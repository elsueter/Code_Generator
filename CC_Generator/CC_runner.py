import csv
import argparse
import os
parser = argparse.ArgumentParser()

csv_args = []

with open('config.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        exit


# Location,Language,No_Files,Fn_Complexity,No_Structs,Structs,Execution_Path,CC
parser.add_argument("-cc", "--cyclomatic-complexity", help="Cyclomatic Complexity")
parser.add_argument("-o", "--output", help="Output File")
parser.add_argument("-l", "--language", help="Output Language")
parser.add_argument("-f", "--no-files", help="Number of Files")
parser.add_argument("-c", "--complexity", help="Function Complexity")



args = parser.parse_args()
































string1 = '''int func_1_01(int a, int b){ // CC = 2
    if(a && b){
        return 1;
    }
    if(a || b){
        return 1;
    }
    return 0;
}
int func_2_01(int a, int b){ // CC = 2
    if(a){
        if(b){
            return 1;
        }
    }
    return 0;
}
void func_3_01(){

}'''

string2 = '''int func_1_01(int a){ // CC = 1
    return 0;
}
int func_2_01(int a){ // CC = 1
    return 0;
}
void func_3_01(){

}'''

os.system('rm -r src')
os.system('mkdir src')

for i in range(0, int(args.no_files)):
    os.mkdir(f"src/{i}")
    text_file = open(f"src/{i}/main.cpp", "x")

    if(int(args.cyclomatic_complexity) == 2):
        text_file.write(string1)
    else:
        text_file.write(string2)
    text_file.close()