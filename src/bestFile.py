import ijson
import json
import os
import surprise


if __name__ == '__main__':
    file_path = os.path.expanduser(r"C:\Users\kimme\Git\web-int\src\one_week\20170101")
    maks=10
    counter = 0
    data=[]
    with open(file_path) as infile:
        for line in infile:
            counter+=1
            temp = json.loads(line.strip())
            print(temp)
            if counter == maks:
                break

"""
            for key in temp:
                if(key == "profile"):
                    print(temp[key])
                    print(temp)
                    break
"""

    #print(data)