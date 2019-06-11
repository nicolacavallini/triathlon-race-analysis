import tabula

from os import path
from glob import glob

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

def get_file():

    f_list = find_ext(".","pdf")
    message = "Choose input file:\n"
    index = 0
    for f in f_list:
        message+=" "+str(index)+") for {}".format(f)+"\n"
        index+=1

    while True:
        try:
            quiz_number = int(input(message))
        except ValueError:
            print "Not a number, please try again\n"
        else:
            if 0 > quiz_number or quiz_number >= len(f_list):
                print "Invalid value, please try again\n"
            else:
                return f_list[quiz_number][:-4]#without extension


if __name__ == "__main__":

    filename = get_file()


    # filename = input("file to be extracted, without extension:")
    #
    print("Converting to CSV: "+ filename)
    #
    # convert PDF into CSV
    tabula.convert_into(filename+".pdf",
                        filename+".tmp.csv",
                        output_format="csv",
                        pages='all')

    print("Cleaning CSV")

    in_file  = open(filename+".tmp.csv", "r")
    out_file  = open(filename+".csv", "w")
    num = 0
    for line in in_file:

        is_header_line = line[:4] == "Pos."
        is_bad_line = line[:2] == '""'
        is_good_line = line[:2] != '""'
        not_header_line = line[:4] != "Pos."

        if (is_header_line and num==0):
            out_file.write(line)
        elif( is_good_line and not_header_line):
            out_file.write(line)
        if (is_header_line):
            num+=1
