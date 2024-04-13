from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from installer import *


class GUI(Tk):
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("600x500")
        self.tk.title("Установщик")

        self.panelFrame = Frame(self.tk, height=60, bg='gray')
        self.panelFrameUnderPanelFrame = Frame(self.tk, height=50, bg='gray')
        self.panelFrameBottom = Frame(self.tk, height=60, bg='gray')
        self.textFrame = Frame(self.tk, height=340, width=600)

        self.panelFrame.pack(side='top', fill=X)
        self.panelFrameUnderPanelFrame.pack(side='top', fill=X)
        self.panelFrameBottom.pack(side='bottom', fill=X)
        self.textFrame.pack(side='bottom', fill='both', expand=1)

        self.textbox = Text(self.textFrame, font='Arial 10', wrap='word')
        self.scrollbar = Scrollbar(self.textFrame)

        self.scrollbar['command'] = self.textbox.yview
        self.textbox['yscrollcommand'] = self.scrollbar.set

        self.textbox.pack(side='left', fill='both', expand=1)
        self.scrollbar.pack(side='right', fill='y')

        self.entry = ttk.Entry(self.panelFrame, width=200)
        self.entry.place(x=25, y=10, width=400, height=30)
        self.entry.bind('<Return>', self.exist_cmd)

        self.progress_bar = ttk.Progressbar(self.panelFrameUnderPanelFrame, orient='horizontal', mode='determinate')
        self.progress_bar.place(x=25, y=10, width=500, height=30)

        self.value_progress = ttk.Label(self.panelFrameUnderPanelFrame, font='Arial 10', foreground="black", text="0.0%")
        self.value_progress.place(x=530, y=10, width=50, height=30)

        self.loadBtn = ttk.Button(self.panelFrame, text='Выбрать папку')
        self.nextBtn = ttk.Button(self.panelFrameBottom, text='Установка')
        self.quitBtn = ttk.Button(self.panelFrameBottom, text='Отмена')

        self.loadBtn.bind("<Button-1>", self.load_folder)
        self.nextBtn.bind("<Button-1>", self.install_cmd)
        self.quitBtn.bind("<Button-1>", self.quit_app)

        self.loadBtn.place(x=460, y=10, width=100, height=30)
        self.nextBtn.place(x=425, y=10, width=70, height=30)
        self.quitBtn.place(x=500, y=10, width=60, height=30)

        self.tk.after(1000, self.task)

    def task(self):
        if not installer_me2.installed:
            installer_me2.loading_files(self.textbox, (self.progress_bar, self.value_progress))
            self.tk.after(500, self.task)
        else:
            self.tk.after(1000, self.task)

    def quit_app(self, ev):
        self.tk.destroy()

    def load_folder(self, ev):
        fn = filedialog.askdirectory()
        if fn == '':
            return
        self.entry.delete('0', 'end')
        self.entry.insert('0', os.path.abspath(fn))
        installer_me2.set_current_folder_for_install(self.entry.get())

    def install_cmd(self, ev):
        if self.exist_cmd(ev):
            installer_me2.make_dirs()
            installer_me2.installed = False
            print(installer_me2.installed)

    def exist_cmd(self, ev):
        if installer_me2.data is None:
            messagebox.showerror("ФАТАЛЬНАЯ ОШИБКА", "Отсутствует файл data.txt")
            self.quit_app(ev)
        else:
            if installer_me2.set_current_folder_for_install(self.entry.get()):
                messagebox.showinfo("Информация", "Всё отлично, установка началась")
                return True
            else:
                messagebox.showerror("Ошибка", "Такой папки не существует")
                return False


root = GUI()
root.mainloop()
