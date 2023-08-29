````python
try:
    import logging
    import sys
    import os
    path = r"assets"
    try:
       wd = sys._MEIPASS
    except Exception as es:
        print(es)
        wd = os.getcwd()
    file_path = os.path.join(wd, path)
    with open(file_path+"/test.ico") as icon:
        print("Icon succesfully opend")
    with open(file_path+"/test.txt") as txt:
        print("Text succesfully opend")
    input()
except Exception as e:
    print("FUCKED UP", e)
    input()
````
