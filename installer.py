import os
import requests
import base64
import time

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class InstallerME2:
    def __init__(self):
        self.url = "https://149.202.225.182/game/sight1/Contents"
        self.data = self.converter(os.getcwd() + "/data.txt")
        self.not_installed = []
        self.installed_files = []
        self.index_installed_file = 0
        self.current_folder_for_install = "C:/Users/admin/Other/TestingInstallerME2"
        self.progress_bar = 0.0
        self.dirs_for_installed_files = self.get_dirs_for_install() if self.data is not None else []
        self.dirs_to_install = False
        self.installed = True if self.index_installed_file < len(self.dirs_for_installed_files) else False

    @staticmethod
    def converter(file_path: str) -> list or None:
        try:
            with open(file_path, "r") as f:
                data = f.readlines()
                data = " ".join(data)
                data = base64.b64decode(data.encode('ascii')).decode('ascii')
                return eval(data)
        except FileNotFoundError:
            return None

    def set_current_folder_for_install(self, path_folder: str):
        if os.path.exists(path_folder):
            self.current_folder_for_install = path_folder.replace('\\', '/')
            return True
        else:
            return False

    def get_dirs_for_install(self):
        directories = []
        for item in [name.replace("//", "") for name in self.get_names_files()]:
            directories.append(item[item.index('/'): item.rindex('/')])
        return list(set(directories))

    def make_dirs(self):
        for folder in self.dirs_for_installed_files:
            if not os.path.exists(self.current_folder_for_install + folder):
                if folder.count('/') == 1:
                    os.mkdir(self.current_folder_for_install + folder)
                else:
                    if not os.path.exists(self.current_folder_for_install + folder[:folder.rindex('/')]):
                        os.mkdir(self.current_folder_for_install + folder[:folder.rindex('/')])
                    os.mkdir(self.current_folder_for_install + folder)
            else:
                continue

    def get_names_files(self) -> list:
        names_files = [item["name"].replace("..//Contents", "") for item in self.data]
        return names_files

    def update_progress_bar(self, progress_bar: tuple):
        self.progress_bar = self.installed_files.__len__() / self.data.__len__() * 100
        progress_bar[0]['value'] = self.progress_bar
        progress_bar[1].config(text=(round(self.progress_bar, 2).__str__() + "%"))

    @staticmethod
    def get_response(url):
        return requests.get(url, verify=False, timeout=None, cert=False)

    def loading_files(self, frame, progress_bar: tuple):
        name = self.get_names_files()[self.index_installed_file]

        abs_url = self.url + name
        way = (self.current_folder_for_install + name.replace("/Contents", ""))

        try:
            r = self.get_response(abs_url)

            with open(way, "wb") as f:
                f.write(r.content)

            self.installed_files.append(name)
            time.sleep(0.01)
            self.update_progress_bar(progress_bar)

            frame.insert("1.0", f"Installing '{name}' is done\n")

        except requests.exceptions.ConnectionError:
            self.not_installed.append(name)

        self.index_installed_file += 1

    def try_to_install_not_installed(self):
        for name in self.not_installed:
            abs_url = self.url + name
            way = (self.current_folder_for_install + name.replace("/Contents", ""))

            try:
                r = self.get_response(abs_url)

                with open(way, "wb") as f:
                    f.write(r.content)

                self.installed_files.append(name)
                self.update_progress_bar()

            except requests.exceptions.ConnectionError:
                continue

        self.not_installed = [name for name in self.installed_files if not self.not_installed.__contains__(name)]


installer_me2 = InstallerME2()
