from tkinter import messagebox

import os
import requests

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def converter(file_path: str) -> list:
    try:
        with open(file_path, "r") as f:
            return eval(f.read())
    except FileNotFoundError:
        messagebox.showwarning("Ошибка", "Файл hash.txt не найден")
        return []


class InstallerME2:
    def __init__(self):
        self.url = "https://185.106.92.10/game/sight1"
        self.data = converter("hash.txt")
        self.not_installed = []
        self.installed = []
        self.current_folder_for_install = "C:/Users/admin/Other/TestingInstallerME2"    # filedialog потом добавить
        self.progress_bar = 0.0
        self.dirs_for_installed_files = self.get_dirs_for_install()
        self.dirs_to_install = False

    def set_current_folder_for_install(self):
        self.current_folder_for_install = ""    # Вставить сюда работу filedialog

    def exist_current_folder_for_install(self):
        return os.path.exists(self.current_folder_for_install)

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
        names_files = [item["name"].replace("../", "") for item in self.data]
        return names_files

    def update_progress_bar(self):
        self.progress_bar = self.installed.__len__() / self.data.__len__() * 100

    @staticmethod
    def get_response(url):
        return requests.get(url, verify=False, timeout=None, cert=False)

    def loading_files(self):
        dirs = self.dirs_for_installed_files

        for name in self.get_names_files():
            abs_url = self.url + name
            way = (self.current_folder_for_install + name.replace("/Contents", ""))

            print(abs_url)
            print(way)

            # try:
            #     r = self.get_response(abs_url)
            #
            #     with open(way, "wb") as f:
            #         f.write(r.content)
            #
            #     self.installed.append(name)
            #     self.update_progress_bar()
            #
            # except requests.exceptions.ConnectionError:
            #     self.not_installed.append(name)

    def try_to_install_not_installed(self):
        for name in self.not_installed:
            abs_url = self.url + name
            way = (self.current_folder_for_install + name.replace("/Contents", ""))

            try:
                r = self.get_response(abs_url)

                with open(way, "wb") as f:
                    f.write(r.content)

                self.installed.append(name)
                self.update_progress_bar()

            except requests.exceptions.ConnectionError:
                continue

        self.not_installed = [name for name in self.installed if not self.not_installed.__contains__(name)]


install = InstallerME2()
print(install.loading_files())
