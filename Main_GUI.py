from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar
from tkinter.font import Font
import PIL
import csv
import math
import xlrd
import xlrd
from collections import OrderedDict

from PIL import Image, ImageTk
from zillow_scraper import *
HEADING = []

class MainGUI:
    def __init__(self, master, result_row):
        self.master = master
        self.result_row = result_row
        master.resizable(0, 0)
        self.center(win_w=1020, win_h=1000)
        master.title("ZILLOW SCRAPPER TOOL v7.0")

        # create a menu
        menu = Menu(master)
        master.config(menu=menu)

        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.callback_about)

        title_comment_frame = Frame(master)
        title_comment_frame.place(x=200, y=20)
        title_txt = 'ZILLOW SCRAPPER TOOL'
        title_lbl = Label(title_comment_frame, text=title_txt, font=('Comic Sans MS bold', 15), fg='#60A644', width=50)
        title_lbl.pack(side=TOP, anchor=CENTER, padx=10, pady=10)

        file_comment_frame = Frame(master)
        file_comment_frame.place(x=10, y=80)
        file_comment = 'To use the tool browse for the import file (csv or excel)'
        comment_lbl = Label(file_comment_frame, text=file_comment, font=('Calibri bold', 12), fg='#60A644')
        comment_lbl.pack(side=TOP, anchor=W, padx=10, pady=10)

        image = Image.open('resources/logo.png').convert("RGBA")
        image = image.resize((130, 80), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = Label(master, image=photo)
        label.image = photo  # keep a reference!
        # label.place(x=15, y=320)
        label.place(x=795, y=10)

        file_path_frame = Frame(master)
        file_path_frame.place(x=10, y=200)

        file_path_frame = Frame(master)
        file_path_frame.place(x=10, y=110)

        file_path_txt = 'File path:'
        file_path_lbl = Label(file_path_frame, text=file_path_txt, font=('Calibri', 12), fg='black')
        file_path_lbl.config(height=2)
        file_path_lbl.pack(side=LEFT, anchor=CENTER, padx=10, pady=50)

        self.path = StringVar()
        self.path.trace("w", lambda name, index, mode, sv=self.path: self.get_filename(sv))
        file_path_entry = Entry(file_path_frame, textvariable=self.path, relief=FLAT, highlightbackground='black',
                                highlightthickness=1)
        file_path_entry.focus_set()
        file_path_entry.config(width=110)
        file_path_entry.pack(side=LEFT, anchor=CENTER, padx=10, pady=50)

        browse_btn = Button(file_path_frame, text='BROWSE', font=('Calibri bold', 12), bg='#60A644', fg='white',
                            command=self.browse_click)
        browse_btn.config(width=14, height=1)
        browse_btn.pack(side=LEFT, anchor=CENTER, padx=20, pady=50)

        # browse_btn.bind("<Button-1>", self.browse_click)

        ############################################################################################################
        property_columns_frame = Frame(master)
        property_columns_frame.place(x=70, y=220)

        Label(property_columns_frame, text="Property Address: ", font=('Calibri', 12), anchor=E).grid(
            row=0,
            column=1,
            columnspan=4,
            sticky=W + E + N + S,
            padx=5,
            pady=5)
        Label(property_columns_frame, text="Property City: ", font=('Calibri', 12), anchor=E).grid(
            row=1,
            column=1,
            columnspan=4,
            sticky=W + E + N + S,
            padx=5,
            pady=5)
        Label(property_columns_frame, text="Property State: ", font=('Calibri', 12), anchor=E).grid(
            row=2,
            column=1,
            columnspan=4,
            sticky=W + E + N + S,
            padx=5,
            pady=5)
        Label(property_columns_frame, text="Property Zip: ", font=('Calibri', 12), anchor=E).grid(
            row=3,
            column=1,
            columnspan=4,
            sticky=W + E + N + S,
            padx=5, pady=5)

        self.Property_Address_Column = StringVar()
        self.Property_City_Column = StringVar()
        self.Property_State_Column = StringVar()
        self.Property_Zip_Column = StringVar()
        Property_Address_Column_entry = Entry(property_columns_frame, textvariable=self.Property_Address_Column,
                                              relief=FLAT,
                                              highlightbackground='black',
                                              highlightthickness=1)
        Property_Address_Column_entry.focus_set()
        Property_Address_Column_entry.config(width=80)
        Property_Address_Column_entry.grid(row=0, column=6, columnspan=12, sticky=W + E + N + S, padx=5, pady=5)

        Property_City_Column_entry = Entry(property_columns_frame, textvariable=self.Property_City_Column,
                                           relief=FLAT,
                                           highlightbackground='black',
                                           highlightthickness=1)
        Property_City_Column_entry.focus_set()
        Property_City_Column_entry.config(width=80)
        Property_City_Column_entry.grid(row=1, column=6, columnspan=12, sticky=W + E + N + S, padx=5, pady=5)

        Property_State_Column_entry = Entry(property_columns_frame, textvariable=self.Property_State_Column,
                                            relief=FLAT,
                                            highlightbackground='black',
                                            highlightthickness=1)
        Property_State_Column_entry.focus_set()
        Property_State_Column_entry.config(width=80)
        Property_State_Column_entry.grid(row=2, column=6, columnspan=12, sticky=W + E + N + S, padx=5, pady=5)

        Property_Zip_Column_entry = Entry(property_columns_frame, textvariable=self.Property_Zip_Column, relief=FLAT,
                                          highlightbackground='black',
                                          highlightthickness=1)
        Property_Zip_Column_entry.focus_set()
        Property_Zip_Column_entry.config(width=80)
        Property_Zip_Column_entry.grid(row=3, column=6, columnspan=12, sticky=W + E + N + S, padx=5, pady=5)

        self.Property_Address_Column.set('D')
        self.Property_City_Column.set('E')
        self.Property_State_Column.set('F')
        self.Property_Zip_Column.set('G')

        ###########################################################################################################
        # Select proxy or captcha

        proxy_captcha_select_frame = LabelFrame(master, text="Proxy or Captcha")
        proxy_captcha_select_frame.config(font=('Calibri bold', 13), fg='#60A644')
        proxy_captcha_select_frame.place(x=150, y=400)

        self.proxy_or_captcha_v = IntVar()
        self.proxy_rb = Radiobutton(proxy_captcha_select_frame, text="Proxy", variable=self.proxy_or_captcha_v, value=1,
                                    command=lambda: self.select_proxy_captcha(self.proxy_rb))
        self.proxy_rb.pack(anchor=W)
        self.proxy_rb.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
        # self.proxy_rb.config(width=20, height=1)

        self.captcha_rb = Radiobutton(proxy_captcha_select_frame, text="Deathbycaptcha", variable=self.proxy_or_captcha_v, value=2,
                                      command=lambda: self.select_proxy_captcha(self.captcha_rb))
        self.captcha_rb.pack(anchor=W)
        self.captcha_rb.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
        # self.captcha_rb.config(width=20, height=1)

        self.proxy_rb.config(fg='#8ab1f2')
        self.captcha_rb.config(fg='#8ab1f2')

        self.proxy_or_captcha_v.set(1)

        ############################################################################################################

        self.status_txt = StringVar()
        status_lbl = Label(master, textvariable=self.status_txt, font=('Calibri bold', 15), fg='#60A644')
        status_lbl.config(width=40, height=1)
        status_lbl.place(x=300, y=480)

        self.status_txt.set("There are no Zillow lines.")

        import_bnt = Button(master, text='IMPORT', font=('Calibri bold', 12), bg='#0F75BD', fg='white',
                            command=self.import_click)
        import_bnt.config(width=18, height=1)
        import_bnt.place(x=520, y=530)

        # import_bnt.bind("<Button-1>", self.import_click)

        assessor_bnt = Button(master, text='GET ZILLOW DATA', font=('Calibri bold', 12), bg='#60A644', fg='white',
                              command=self.assessor_click)
        assessor_bnt.config(width=18, height=1)
        assessor_bnt.place(x=330, y=530)

        # assessor_bnt.bind("<Button-1>", self.assessor_click)

        progress_frame = Frame(master)
        progress_frame.place(x=60, y=580)

        self.prog_ratio_txt = StringVar()
        prog_ratio_lbl = Label(progress_frame, textvariable=self.prog_ratio_txt, font=('Calibri bold', 12),
                               fg='#60A644')

        prog_ratio_lbl.pack(side=TOP, anchor=CENTER, padx=0)
        prog_ratio_lbl.config(width=20)

        self.progress = Progressbar(progress_frame, orient=HORIZONTAL, length=850, mode='determinate')
        self.progress.pack(side=LEFT, anchor=CENTER, padx=20)

        self.prog_percent_txt = StringVar()
        prog_percent_lbl = Label(progress_frame, textvariable=self.prog_percent_txt, font=('Calibri bold', 12),
                                 fg='#60A644')
        prog_percent_lbl.pack(side=RIGHT, anchor=CENTER, padx=0)

        table_frame = Frame(master)
        table_frame.place(x=18, y=670)
        yscrollbar = Scrollbar(table_frame, orient=VERTICAL)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(table_frame, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        self.listbox = Listbox(table_frame, width=160, height=14)
        self.listbox.pack()

        # attach listbox to scrollbar
        self.listbox.config(yscrollcommand=yscrollbar.set)
        self.listbox.config(xscrollcommand=xscrollbar.set)
        yscrollbar.config(command=self.listbox.yview)
        xscrollbar.config(command=self.listbox.xview)

        self.listbox_rows_cnt = 0

        self.zillow_lines = []
        self.running = 0

    def browse_click(self):
        # def browse_click(self, event):
        default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
        fname = askopenfilename(filetypes=(("Input files", "*.csv;*.xlsx;*.xls"),
                                           ("CSV files", "*.csv"),
                                           ("Excel files", "*.xls;*.xlsx"),
                                           ("All files", "*.*")),
                                initialdir=default_path)
        if fname:
            self.path.set(fname)

    def import_click(self):
        fname = self.path.get()
        if fname:
            if fname.endswith('xlsx'):
                input_xls = xlrd.open_workbook(fname)
                sheet = input_xls.sheet_by_index(0)
                headers = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

                for row_index in range(0, sheet.nrows):
                    row = [sheet.cell(row_index, col_index).value if isinstance(
                        sheet.cell(row_index, col_index).value, str) else str(
                        int(sheet.cell(row_index, col_index).value)) for col_index in range(sheet.ncols)]

                    if all(elm == '' for elm in row):
                        continue
                    self.zillow_lines.append(row)

            elif fname.endswith('csv'):
                csv_reader = csv.reader(open(fname, 'r', encoding='utf-8'))
                for row_index, row in enumerate(csv_reader):
                    if all(elm == '' for elm in row):
                        continue
                    self.zillow_lines.append(row)

            global TOTAL_CNT
            TOTAL_CNT = len(self.zillow_lines) - 1

            self.status_txt.set(
                'There are {} Zillow lines imported'.format(TOTAL_CNT)
            )

        else:
            messagebox.showwarning("Warning", "Please input file name.")

    def assessor_click(self):
        # def assessor_click(self, event):
        if self.zillow_lines:
            self.running = 1
        else:
            messagebox.showwarning("Warning", "There are no Zillow lines. Please input file name.")

    def get_filename(self, sv):
        print(sv.get())

    def center(self, win_w=1200, win_h=800):
        rootsize = (win_w, win_h)
        w = self.master.winfo_screenwidth()
        h = self.master.winfo_screenheight()
        x = w / 2 - rootsize[0] / 2
        y = h / 2 - rootsize[1] / 2
        self.master.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))

    def update_prog_bar(self):
        global TOTAL_CNT

        while self.result_row.qsize():
            try:
                result_row = self.result_row.get(0)
                total_completed = result_row[0]
                self.prog_ratio_txt.set("{}/{}".format(total_completed, TOTAL_CNT))
                self.prog_percent_txt.set('{}%'.format(math.floor(total_completed / TOTAL_CNT * 100)))
                self.progress['value'] = math.floor(total_completed / TOTAL_CNT * 100)

                result = result_row
                self.listbox.insert(END, str(result))
                self.listbox_rows_cnt += 1
                if self.listbox_rows_cnt > 10000:
                    self.listbox.delete(0, 0)
                self.listbox.yview(END)
                if total_completed == TOTAL_CNT:
                    messagebox.showinfo('Success', "Zillow details have been extracted!")
            except:
                pass

    def callback_about(self):
        about_txt = "Joseph Nguyen\n(301)717-7631\njoseph@urbanxdevelopment.com"
        messagebox.showinfo('About', about_txt)

    def select_proxy_captcha(self, widget):
        if self.proxy_or_captcha_v.get() == 1:
            self.proxy_rb.config(fg='blue')
            self.captcha_rb.config(fg='#8ab1f2')
        elif self.proxy_or_captcha_v.get() == 2:
            self.captcha_rb.config(fg='blue')
            self.proxy_rb.config(fg='#8ab1f2')

    def update_proxy_or_captcha(self):
        if self.proxy_or_captcha_v.get() == 1:
            self.proxy_rb.config(fg='blue')
            self.captcha_rb.config(fg='#8ab1f2')
        elif self.proxy_or_captcha_v.get() == 2:
            self.captcha_rb.config(fg='blue')
            self.proxy_rb.config(fg='#8ab1f2')