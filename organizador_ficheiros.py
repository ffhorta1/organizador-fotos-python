import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from PIL.ExifTags import TAGS

# Mapeamento padrão dos meses em português
MESES_PT = {
    1: "01-Janeiro", 2: "02-Fevereiro", 3: "03-Março", 4: "04-Abril",
    5: "05-Maio", 6: "06-Junho", 7: "07-Julho", 8: "08-Agosto",
    9: "09-Setembro", 10: "10-Outubro", 11: "11-Novembro", 12: "12-Dezembro"
}

def get_exif_date(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'DateTimeOriginal':
                return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None

def get_file_date(file_path, use_mtime=False, use_exif=False):
    if use_exif:
        exif_date = get_exif_date(file_path)
        if exif_date:
            return exif_date
    timestamp = os.path.getmtime(file_path) if use_mtime else os.path.getctime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)

def organize_files_pt(directory, by_month=False, use_mtime=False, move_files=True, use_exif=False, month_names=None):
    if not os.path.isdir(directory):
        raise ValueError("O caminho fornecido não é um diretório válido.")

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_date = get_file_date(item_path, use_mtime, use_exif)
            if not file_date:
                continue  # Ignora arquivos sem data válida
            year = str(file_date.year)
            if by_month:
                if month_names and file_date.month in month_names:
                    month_name = month_names[file_date.month]
                else:
                    month_name = MESES_PT[file_date.month]
                target_dir = os.path.join(directory, year, month_name)
            else:
                target_dir = os.path.join(directory, year)

            os.makedirs(target_dir, exist_ok=True)

            dest_path = os.path.join(target_dir, item)
            if move_files:
                shutil.move(item_path, dest_path)
            else:
                shutil.copy2(item_path, dest_path)

    return True

def launch_gui():
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)

    def run_organizer():
        folder = folder_var.get()
        by_month = (folder_format_var.get() == "Ano/Mês")

        use_exif = (date_option_var.get() == "EXIF")
        use_mtime = (date_option_var.get() == "Modificação")
        # Se não for EXIF nem modificação, é criação (default do get_file_date)

        move_files = (action_var.get() == "Mover")

        custom_months = {i + 1: month_entries[i].get() or MESES_PT[i + 1] for i in range(12)}

        try:
            organize_files_pt(folder, by_month, use_mtime, move_files, use_exif, custom_months)
            messagebox.showinfo("Sucesso", "Arquivos organizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    root = tk.Tk()
    root.title("Organizador de Arquivos por Data")
    root.geometry("600x750")
    root.resizable(False, False)

    folder_var = tk.StringVar()
    folder_format_var = tk.StringVar(value="Ano/Mês")
    date_option_var = tk.StringVar(value="EXIF")
    action_var = tk.StringVar(value="Copiar")

    ttk.Label(root, text="Selecione a pasta de arquivos:").pack(pady=10)

    folder_frame = ttk.Frame(root)
    folder_frame.pack(padx=10)
    ttk.Entry(folder_frame, textvariable=folder_var, width=50).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(folder_frame, text="Procurar", command=browse_folder).pack(side=tk.LEFT)

    # Segmento 1 - Formato dos folders
    format_frame = ttk.LabelFrame(root, text="Formato dos folders")
    format_frame.pack(pady=10, fill='x', padx=20)

    tk.Radiobutton(format_frame, text="Ano/Mês", variable=folder_format_var, value="Ano/Mês").pack(anchor='w')
    tk.Radiobutton(format_frame, text="Ano", variable=folder_format_var, value="Ano").pack(anchor='w')

    # Segmento 2 - Data a utilizar
    date_frame = ttk.LabelFrame(root, text="Data a utilizar")
    date_frame.pack(pady=10, fill='x', padx=20)

    tk.Radiobutton(date_frame, text="EXIF - para fotos", variable=date_option_var, value="EXIF").pack(anchor='w')
    tk.Radiobutton(date_frame, text="Última modificação", variable=date_option_var, value="Modificação").pack(anchor='w')
    tk.Radiobutton(date_frame, text="Data de criação", variable=date_option_var, value="Criação").pack(anchor='w')

    # Segmento 3 - Ação
    action_frame = ttk.LabelFrame(root, text="Ação")
    action_frame.pack(pady=10, fill='x', padx=20)

    tk.Radiobutton(action_frame, text="Copiar", variable=action_var, value="Copiar").pack(anchor='w')
    tk.Radiobutton(action_frame, text="Mover", variable=action_var, value="Mover").pack(anchor='w')

    # Entradas para nomes personalizados dos meses
    ttk.Label(root, text="Nomes personalizados dos meses:").pack(pady=(20, 5))
    month_entries = []
    months_frame = ttk.Frame(root)
    months_frame.pack()

    for i in range(12):
        row = i // 3
        col = i % 3
        frame = ttk.Frame(months_frame)
        frame.grid(row=row, column=col, padx=10, pady=5)
        ttk.Label(frame, text=f"Mês {i+1:02d}:").pack()
        entry = ttk.Entry(frame, width=20)
        entry.insert(0, MESES_PT[i+1])
        entry.pack()
        month_entries.append(entry)

    ttk.Button(root, text="Organizar", command=run_organizer).pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    launch_gui()
