import requests
import requests as rq
import os
import sys

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def loading_files() -> None:

    url = "https://185.106.92.10/game/sight1"
    file = open("hash.txt", "r")
    data = [x.replace("\n", '') for x in file.readlines() if x != '' or x != '\n']
    file.close()

    data = ("other".join(data)).replace("[", "").replace("]", "").split(",other")

    data = [x[x.index("/")+1:x.index(",")-1] for x in data]

    count_data = len(data)
    counter = 0
    for item in data:
        abs_url = url + item
        way = ("../InstallerME2/files/" + item[item.rindex('/')+1:])

        try:
            r = requests.get(abs_url, verify=False, timeout=None, cert=False)
            with open(way, "wb") as f:
                f.write(r.content)

            #print("Downloading " + item[item.rindex('/')+1:] + " is done")

            counter += 1

            progress = counter / count_data * 100

            sys.stdout.write("\r" + f"{progress:5.2f}%" + " " + f"{counter}" + "/" + f"{count_data}" +
                             " " + "Downloading " + item[item.rindex('/')+1:] + " is done")
            sys.stdout.flush()

        except rq.exceptions.ConnectionError:
            continue

    print(counter)


if __name__ == "__main__":
    loading_files()
