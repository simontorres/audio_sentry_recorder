import os.path
import datetime
import customtkinter as ctk
import tkinter as tk

from customtkinter import filedialog


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.save_to_folder = tk.StringVar(self, os.path.expanduser('~'))
        self.threshold = tk.IntVar(self, 100)
        self.threshold_step = 10

        self.title("Audio Sentry Recorder")
        self.geometry("800x800")
        self.grid_columnconfigure(0, weight=1)

        self.btn_toggle_recording = ctk.CTkButton(
            master=self,
            text="Start Monitoring",
            text_color='red',
            fg_color='transparent',
            border_width=1,
            border_color='red',
            hover_color='black',
            command=self._toggle_recording)
        self.btn_toggle_recording.cget('font').configure(size=16)
        self.btn_toggle_recording.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.pgb_sound_level = ctk.CTkProgressBar(master=self)
        self.pgb_sound_level.grid(row=1, column=0, padx=20, pady=0, sticky='ew')

        self.frm_settings = ctk.CTkFrame(master=self)

        row_save_to_folder = 0
        row_threshold = 1
        self.lbl_save_to_folder = ctk.CTkLabel(master=self.frm_settings, text='Save to Folder')
        self.lbl_save_to_folder.grid(row=row_save_to_folder, column=0, padx=10, pady=10, sticky='e')
        self.ent_save_to_folder = ctk.CTkEntry(
            master=self.frm_settings,
            textvariable=self.save_to_folder,
            width=500)
        self.ent_save_to_folder.grid(row=row_save_to_folder, column=1)
        self.btn_browse_filesystem = ctk.CTkButton(
            master=self.frm_settings,
            text='Browse',
            command=self._select_folder)
        self.btn_browse_filesystem.grid(row=row_save_to_folder, column=2, padx=10, pady=10, sticky='ne')

        self.lbl_threshold = ctk.CTkLabel(master=self.frm_settings, text="Threshold")
        self.lbl_threshold.grid(row=row_threshold, column=0, padx=10, pady=10, sticky='e')

        self.frm_threshold = ctk.CTkFrame(master=self.frm_settings)

        self.btn_threshold_less = ctk.CTkButton(
            master=self.frm_threshold,
            text='-',
            width=30,
            command=self._threshold_less)
        self.btn_threshold_less.grid(row=0, column=0, padx=1, sticky='w')

        self.ent_threshold = ctk.CTkEntry(master=self.frm_threshold, textvariable=self.threshold, width=60)
        self.ent_threshold.grid(row=0, column=1, padx=1, sticky='w')

        self.btn_threshold_more = ctk.CTkButton(
            master=self.frm_threshold,
            text='+',
            width=30,
            command=self._threshold_more)
        self.btn_threshold_more.grid(row=0, column=2, padx=1)

        self.frm_threshold.grid(row=row_threshold, column=1, sticky='w')

        self.frm_settings.grid(row=2, column=0, padx=20, pady=20, sticky='we')

        self.txt_logs = ctk.CTkTextbox(master=self, height=500, text_color='green2', state='disabled')
        self.txt_logs.grid(row=3, column=0, padx=20, sticky='wens')

        # self.frm_logs.grid(row=3, column=0, padx=20, pady=20, sticky='we')
        self._log("Press start monitoring to start")



    def _toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self._log("Monitoring Started")
            self.btn_toggle_recording.configure(
                text="Stop Monitoring",
                text_color='white',
                fg_color='red',
                border_width=1,
                border_color='red',
                hover_color='red2')
            self.ent_save_to_folder.configure(state='disabled')
            self.btn_browse_filesystem.configure(state='disabled')
        else:
            self._log("Monitoring Stopped")
            self.btn_toggle_recording.configure(
                text="Start Monitoring",
                text_color='red',
                fg_color='transparent',
                border_width=1,
                border_color='red',
                hover_color='black')
            self.ent_save_to_folder.configure(state='normal')
            self.btn_browse_filesystem.configure(state='normal')

    def _select_folder(self):
        save_to_folder = filedialog.askdirectory(initialdir=self.save_to_folder.get())
        self.save_to_folder.set(save_to_folder)

    def _threshold_less(self):
        self.threshold.set(self.threshold.get() - self.threshold_step)

    def _threshold_more(self):
        self.threshold.set(self.threshold.get() + self.threshold_step)

    def _log(self, text):
        now = datetime.datetime.now()
        if len(self.txt_logs.get('1.0', tk.END)) >= 2:
            formatted_text = f"\n{now: %x - %X}: {text}"
        else:
            formatted_text = f"{now: %x - %X}: {text}"
        self.txt_logs.configure(state='normal')
        self.txt_logs.insert(tk.END, formatted_text)
        self.txt_logs.yview(tk.END)
        self.txt_logs.configure(state='disabled')


if __name__ == '__main__':
    app = App()
    app.mainloop()

# import os
# import datetime
# import tkinter as tk
# from tkinter import ttk, filedialog
# from tkinter.scrolledtext import ScrolledText
#
# from os import PathLike
#
#
# class App(tk.Tk):
#
#     def __init__(self, save_to_folder=None, threshold: int = 100):
#         super().__init__()
#
#         style = ttk.Style(self)
#         style.map("C.TButton",
#                   foreground=[('pressed', 'red'), ('active', 'blue')],
#                   background=[('pressed', '!disabled', 'black'), ('active', 'white')]
#                   )
#
#         style.configure('TLabel', background='gray22', foreground='green2')
#         style.configure('TEntry', background='gray22', foreground='green2')
#         style.configure('TFrame', background='gray22', foreground='green2')
#         style.configure('TButton', background='gray22', foreground='green2')
#         style.configure('TScrolledText', background='gray22', foreground='green2')
#
#         self.threshold = tk.IntVar(self, threshold)
#
#         if save_to_folder is None:
#             self.save_to_folder = os.path.expanduser('~')
#         else:
#             self.save_to_folder = save_to_folder
#
#         self.title("Audio Sentry Recorder")
#         self.configure(bg='gray22')
#         # self.minsize(800, 500)
#         # self.maxsize(800, 500)
#         self.resizable(width=False, height=False)
#
#         frm_control = tk.Frame(master=self, height=100)
#         frm_control.configure(bg='gray22')
#
#         btn_toggle_recording = ttk.Button(
#             master=frm_control,
#             text="Start Recording",
#             style="C.TButton",
#             command=self.__print_long_message)
#         btn_toggle_recording.grid(row=0, column=0, padx=10, pady=5)
#         frm_control.grid(row=0, column=0, padx=10, pady=10)
#
#         frm_settings = tk.Frame(master=self, height=100)
#         frm_settings.configure(bg='gray22')
#         lbl_threshold = ttk.Label(master=frm_settings, text="Threshold")
#         # lbl_threshold.configure(bg='gray22', fg='green2')
#         lbl_threshold.grid(row=0, column=0, sticky="w")
#         self.spn_threshold = tk.Spinbox(
#             master=frm_settings,
#             from_=0,
#             to=1000,
#             textvariable=self.threshold,
#             width=10)
#         self.spn_threshold.grid(row=0, column=1, padx=5, sticky="w")
#         self.spn_threshold.configure(bg='gray10', fg='green2')
#         self.threshold.trace_add("write", self.__log_threshold_change)
#
#         self.ent_save_to_folder = ttk.Entry(master=frm_settings, width=70)
#         self.ent_save_to_folder.insert(tk.END, self.save_to_folder)
#         lbl_save_to_folder = ttk.Label(master=frm_settings, text="Save to Folder")
#         # lbl_save_to_folder.configure(bg='gray22', fg='green2')
#         btn_select_save_to_folder = ttk.Button(
#             master=frm_settings,
#             text="Browse",
#             command=self.select_folder)
#
#         lbl_save_to_folder.grid(row=1, column=0, sticky="w")
#
#         self.ent_save_to_folder.grid(row=1, column=1, padx=5, sticky="w")
#         # self.ent_save_to_folder.configure(bg='gray10', fg='green2')
#
#         frm_settings.grid(row=1, column=0, padx=10)
#         btn_select_save_to_folder.grid(row=1, column=2, padx=10, pady=10)
#         # btn_select_save_to_folder.configure(bg='black', fg='green2')
#
#         frm_logs = tk.Frame(master=self, relief=tk.SUNKEN, height=250)
#
#         self.txt_logs = ScrolledText(master=frm_logs, width=100, padx=10, pady=10)
#         self.txt_logs.place(x=0, y=0, relwidth=1, relheight=1)
#
#         self.txt_logs.grid(row=0, column=0)
#         # self.txt_logs.configure(bg='black', fg='green2')
#
#         frm_logs.grid(row=2, column=0, padx=5, sticky='we')
#         # frm_logs.configure(background='red')
#         print(style.theme_names())
#
#     def __call__(self, *args, **kwargs):
#         self.mainloop()
#
#     def __log_threshold_change(self, *args):
#         self._log(f"Threshold set to: {self.threshold.get()}")
#
#     def __print_long_message(self, *args):
#         self._log(f"This is a long text for testing scroll")
#
#     def select_folder(self, save_to_folder=None):
#         if save_to_folder is PathLike:
#             self.save_to_folder = save_to_folder
#         else:
#             self.save_to_folder = filedialog.askdirectory(initialdir=self.save_to_folder)
#
#         self.ent_save_to_folder.delete(0, tk.END)
#         self.ent_save_to_folder.insert(0, self.save_to_folder)
#         self._log(f"New folder set to: {self.save_to_folder}")
#
#     def _log(self, text):
#         now = datetime.datetime.now()
#         self.txt_logs.insert(tk.END, f"\n{now.strftime('%X')}: {text}")
#         self.txt_logs.yview(tk.END)
#
#
# if __name__ == '__main__':
#     app = App()
#     app()
