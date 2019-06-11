import tabula

if __name__ == "__main__":

    filename = input("file to be extracted, without extension:")

    print(text)

    # convert PDF into CSV
    tabula.convert_into(filename+".pdf",
                        filename+".tmp.csv",
                        output_format="csv",
                        pages='all')

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
