import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

from src.service.calc import (
    pr_wo_rep, pr_w_rep,
    pl_wo_rep, pl_w_rep,
    cm_wo_rep, cm_w_rep,
    all_marked, r_marked
)

import io
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

import sys

if sys.platform == "win32":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

DEFAULT_FONT = 'Segoe UI'
TITLE_FONT_SIZE = 20
LABEL_FONT_SIZE = 16
ENTRY_FONT_SIZE = 16
BUTTON_FONT_SIZE = 16
RESULT_FONT_SIZE = 16

subscript_digits = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅',
    '6': '₆', '7': '₇', '8': '₈', '9': '₉', 'k': 'ₖ'
}

def make_subscript(text):
    return ''.join(subscript_digits.get(c, c) for c in text)

def render_latex(formula: str, font_size=20, dpi=200):
    fig = plt.figure(figsize=(4, 1.2))
    fig.text(0, 0, f"${formula}$", fontsize=font_size)
    buffer = io.BytesIO()
    plt.axis('off')
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=dpi, transparent=True)
    plt.close(fig)
    buffer.seek(0)
    image = Image.open(buffer)
    return ImageTk.PhotoImage(image)

class CombinatorialCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title('Комбинаторный Калькулятор')
        if sys.platform == 'win32':
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        base_w, base_h = 1920, 1080
        scale = max(min(sw/base_w, sh/base_h) * 1.2, 1.0)
        self.root.tk.call('tk', 'scaling', scale)
        for fname in ('TkDefaultFont','TkMenuFont','TkTextFont','TkHeadingFont'):
            try:
                f = tkfont.nametofont(fname)
                f.configure(size=int(f.cget('size')*scale))
            except tk.TclError:
                pass
        style = ttk.Style()
        style.configure('TLabel', font=(DEFAULT_FONT, LABEL_FONT_SIZE))
        style.configure('TButton', font=(DEFAULT_FONT, BUTTON_FONT_SIZE))
        style.configure('TEntry', font=(DEFAULT_FONT, ENTRY_FONT_SIZE))
        style.configure('Big.TButton', font=(DEFAULT_FONT, BUTTON_FONT_SIZE, 'bold'))
        style.configure('Title.TLabelframe.Label', font=(DEFAULT_FONT, TITLE_FONT_SIZE))
        style.configure('Result.TLabel', font=(DEFAULT_FONT, RESULT_FONT_SIZE, 'bold'))
        self.root.geometry('1200x900')
        self.root.minsize(800,600)
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.main_frame=ttk.Frame(self.root,padding=20)
        self.main_frame.grid(row=0,column=0,sticky='nsew')
        self.main_frame.grid_rowconfigure(0,weight=1)
        self.main_frame.grid_columnconfigure(0,weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.notebook=ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
        self.create_permutation_tab()
        self.create_placement_tab()
        self.create_combination_tab()
        self.create_probability_tab()
        self.status_var=tk.StringVar()
        self.status_bar=ttk.Label(self.main_frame,textvariable=self.status_var,
            relief='sunken',padding=(10,5),font=(DEFAULT_FONT,LABEL_FONT_SIZE))
        self.status_bar.grid(row=1,column=0,sticky='ew',pady=(10,0))

    def create_tab_frame(self,parent):
        cont=ttk.Frame(parent)
        cont.pack(fill='both',expand=True)
        canvas=tk.Canvas(cont,highlightthickness=0)
        vs=ttk.Scrollbar(cont,orient='vertical',command=canvas.yview)
        canvas.configure(yscrollcommand=vs.set)
        canvas.pack(side='left',fill='both',expand=True)
        vs.pack(side='right',fill='y')
        frm=ttk.Frame(canvas)
        canvas.create_window((0,0),window=frm,anchor='nw')
        frm.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        frm.bind('<Enter>',lambda e:canvas.bind_all('<MouseWheel>',
            lambda ev:canvas.yview_scroll(int(-1*(ev.delta/120)),'units')))
        frm.bind('<Leave>',lambda e:canvas.unbind_all('<MouseWheel>'))
        return cont,frm

    def create_input_section(self,parent,title,inputs,cmd):
        f=ttk.LabelFrame(parent,text=title,padding=15,style='Title.TLabelframe')
        f.pack(fill='x',padx=10,pady=10)
        for i,(lt,vs) in enumerate(inputs):
            ttk.Label(f,text=lt).grid(row=i,column=0,sticky='e',padx=10,pady=10)
            e=ttk.Entry(f,font=(DEFAULT_FONT,ENTRY_FONT_SIZE),width=25)
            e.grid(row=i,column=1,sticky='ew',padx=10,pady=10)
            vs.append(e)
        f.grid_columnconfigure(1,weight=1)
        b=ttk.Button(f,text='Вычислить',command=cmd,style='Big.TButton')
        b.grid(row=0,column=2,rowspan=len(inputs),padx=15,pady=15,sticky='nsew')
        rl=ttk.Label(f,text='Результат: ',style='Result.TLabel')
        rl.grid(row=len(inputs),column=0,columnspan=3,sticky='w',pady=(15,5))
        return rl

    def create_permutation_tab(self):
        c,t=self.create_tab_frame(self.notebook);self.notebook.add(c,text='Перестановки')
        self.pr_wo_rep_n=[];self.pr_w_rep_n=[];self.pr_w_rep_ks=[]
        self.pr_wo_rep_result=self.create_input_section(t,'Без повторений',[("n:",self.pr_wo_rep_n)],self.calculate_pr_wo_rep)
        img=render_latex(r'P_n = n!');l=ttk.Label(t,image=img);l.image=img;l.pack(pady=(0,15))
        fw=ttk.LabelFrame(t,text='С повторениями',padding=15,style='Title.TLabelframe');fw.pack(fill='x',padx=10,pady=10)
        ttk.Label(fw,text='n:').grid(row=0,column=0,sticky='e',padx=10,pady=10)
        e1=ttk.Entry(fw,font=(DEFAULT_FONT,ENTRY_FONT_SIZE),width=25);e1.grid(row=0,column=1,sticky='ew',padx=10,pady=10);self.pr_w_rep_n.append(e1)
        ttk.Label(fw,text=f"{make_subscript('n1')}, {make_subscript('n2')}, ..., {make_subscript('nk')}").grid(row=1,column=0,sticky='e',padx=10,pady=10)
        e2=ttk.Entry(fw,font=(DEFAULT_FONT,ENTRY_FONT_SIZE),width=25);e2.grid(row=1,column=1,sticky='ew',padx=10,pady=10);self.pr_w_rep_ks.append(e2)
        fw.grid_columnconfigure(1,weight=1)
        ttk.Button(fw,text='Вычислить',command=self.calculate_pr_w_rep,style='Big.TButton').grid(row=0,column=2,rowspan=2,padx=15,pady=15,sticky='nsew')
        self.pr_w_rep_result=ttk.Label(fw,text='Результат: ',style='Result.TLabel');self.pr_w_rep_result.grid(row=2,column=0,columnspan=3,sticky='w',pady=(15,5))
        img2=render_latex(r'P = \frac{n!}{n_1!\,n_2!\,\dots\,n_k!}');l2=ttk.Label(t,image=img2);l2.image=img2;l2.pack(pady=(0,15))

    def create_placement_tab(self):
        c,t=self.create_tab_frame(self.notebook);self.notebook.add(c,text='Размещения')
        self.pl_wo_rep_k=[];self.pl_wo_rep_n=[];self.pl_w_rep_k=[];self.pl_w_rep_n=[]
        self.pl_wo_rep_result=self.create_input_section(t,'Без повторений',[("k:",self.pl_wo_rep_k),("n:",self.pl_wo_rep_n)],self.calculate_pl_wo_rep)
        img=render_latex(r'A_k^n = \frac{n!}{(n-k)!}');l=ttk.Label(t,image=img);l.image=img;l.pack(pady=(0,15))
        self.pl_w_rep_result=self.create_input_section(t,'С повторениями',[("k:",self.pl_w_rep_k),("n:",self.pl_w_rep_n)],self.calculate_pl_w_rep)
        img2=render_latex(r'A_k^n = n^k');l2=ttk.Label(t,image=img2);l2.image=img2;l2.pack(pady=(0,15))

    def create_combination_tab(self):
        c,t=self.create_tab_frame(self.notebook);self.notebook.add(c,text='Сочетания')
        self.cm_wo_rep_k=[];self.cm_wo_rep_n=[];self.cm_w_rep_k=[];self.cm_w_rep_n=[]
        self.cm_wo_rep_result=self.create_input_section(t,'Без повторений',[("k:",self.cm_wo_rep_k),("n:",self.cm_wo_rep_n)],self.calculate_cm_wo_rep)
        img=render_latex(r'C_k^n = \frac{n!}{k!(n-k)!}');l=ttk.Label(t,image=img);l.image=img;l.pack(pady=(0,15))
        self.cm_w_rep_result=self.create_input_section(t,'С повторениями',[("k:",self.cm_w_rep_k),("n:",self.cm_w_rep_n)],self.calculate_cm_w_rep)
        img2=render_latex(r'C_k^n = C_k^{n+k-1}');l2=ttk.Label(t,image=img2);l2.image=img2;l2.pack(pady=(0,15))

    def create_probability_tab(self):
        c,t=self.create_tab_frame(self.notebook);self.notebook.add(c,text='Вероятность')
        self.all_marked_k=[];self.all_marked_m=[];self.all_marked_n=[];self.r_marked_r=[];self.r_marked_k=[];self.r_marked_m=[];self.r_marked_n=[]
        self.all_marked_result=self.create_input_section(t,'Урновая модель, где все меченные',[("k:",self.all_marked_k),("m:",self.all_marked_m),("n:",self.all_marked_n)],self.calculate_all_marked)
        img=render_latex(r'P = \frac{C_k^m}{C_k^n}');l=ttk.Label(t,image=img);l.image=img;l.pack(pady=(0,15))
        self.r_marked_result=self.create_input_section(t,'Урновая модель, где R меченных',[("r:",self.r_marked_r),("k:",self.r_marked_k),("m:",self.r_marked_m),("n:",self.r_marked_n)],self.calculate_r_marked)
        img2=render_latex(r'P = \frac{C_r^m \cdot C_{k-r}^{n-m}}{C_k^n}');l2=ttk.Label(t,image=img2);l2.image=img2;l2.pack(pady=(0,15))

    def calculate_pr_wo_rep(self):
        try:
            n = int(self.pr_wo_rep_n[0].get())
            result = pr_wo_rep(n)
            self.pr_wo_rep_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_pr_w_rep(self):
        try:
            n = int(self.pr_w_rep_n[0].get())
            ks_str = self.pr_w_rep_ks[0].get()
            ks = [int(k.strip()) for k in ks_str.split(',') if k.strip()]
            result = pr_w_rep(n, *ks)
            self.pr_w_rep_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_pl_wo_rep(self):
        try:
            k = int(self.pl_wo_rep_k[0].get())
            n = int(self.pl_wo_rep_n[0].get())
            result = pl_wo_rep(k, n)
            self.pl_wo_rep_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_pl_w_rep(self):
        try:
            k = int(self.pl_w_rep_k[0].get())
            n = int(self.pl_w_rep_n[0].get())
            result = pl_w_rep(k, n)
            self.pl_w_rep_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_cm_wo_rep(self):
        try:
            k = int(self.cm_wo_rep_k[0].get())
            n = int(self.cm_wo_rep_n[0].get())
            result = cm_wo_rep(k, n)
            self.cm_wo_rep_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_cm_w_rep(self):
        try:
            k = int(self.cm_w_rep_k[0].get())
            n = int(self.cm_w_rep_n[0].get())
            result = cm_w_rep(k, n)
            self.cm_w_rep_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_all_marked(self):
        try:
            k = int(self.all_marked_k[0].get())
            m = int(self.all_marked_m[0].get())
            n = int(self.all_marked_n[0].get())
            result = all_marked(k, m, n)
            self.all_marked_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))

    def calculate_r_marked(self):
        try:
            r = int(self.r_marked_r[0].get())
            k = int(self.r_marked_k[0].get())
            m = int(self.r_marked_m[0].get())
            n = int(self.r_marked_n[0].get())
            result = r_marked(r, k, m, n)
            self.r_marked_result.config(text=f"Результат: {result}")
            self.status_var.set("")
        except ValueError as e:
            self.status_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))