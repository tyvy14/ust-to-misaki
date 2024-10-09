import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import os


# Função para ler e converter o arquivo UST para Misaki
def read_ust_file(ust_file):
    ust_data = []
    current_note = {}

    try:
        with open(ust_file, 'r', encoding='shift_jis') as file:
            for line in file:
                line = line.strip()
                if line.startswith("[#") and line != "[#END]":
                    if current_note:  # Salva a nota anterior
                        ust_data.append(current_note)
                    current_note = {}
                elif "=" in line:
                    key, value = line.split("=", 1)
                    current_note[key.strip()] = value.strip()

        if current_note:  # Salva a última nota
            ust_data.append(current_note)

    except UnicodeDecodeError:
        messagebox.showerror("Erro",
                             "Erro ao decodificar o arquivo. Certifique-se de que o arquivo UST está em Shift_JIS ou UTF-8.")
        return []

    return ust_data


# Função para converter dados UST para o formato Misaki
def convert_to_misaki(ust_data, output_file, tempo):
    # Criação manual do conteúdo XML usando strings
    plist_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    plist_content += '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
    plist_content += '<plist version="1.0">\n'
    plist_content += '  <dict>\n'
    plist_content += '    <key>header</key>\n'
    plist_content += '    <dict>\n'
    plist_content += '      <key>length</key>\n'
    plist_content += f'      <string>{max(len(ust_data), 10)}</string>\n'  # No mínimo 10
    plist_content += '      <key>tempo</key>\n'
    plist_content += f'      <string>{tempo}</string>\n'  # Usa o valor de tempo fornecido
    plist_content += '    </dict>\n'
    plist_content += '    <key>notes</key>\n'
    plist_content += '    <array>\n'

    # Conversão de ticks (UST) para tempo em segundos
    ticks_per_beat = 480  # UST usa 480 ticks por batida
    seconds_per_tick = 60 / (tempo * ticks_per_beat)

    # Acumular tempo de início para cada nota
    time_accumulator = 0.0

    for note in ust_data:
        if 'Lyric' not in note or 'Length' not in note:
            continue

        lyric = note.get('Lyric', '-')
        note_length_in_ticks = int(note.get('Length', '0'))
        note_length_in_seconds = note_length_in_ticks * seconds_per_tick

        if lyric == 'R':  # Se for pausa, apenas acumula o tempo
            time_accumulator += note_length_in_seconds
            continue

        note_num = int(note.get('NoteNum', '60'))
        if note_num > 83:  # Limita as notas a B5 (83)
            note_num = 83

        # Adiciona a nota ao conteúdo
        plist_content += '      <dict>\n'
        plist_content += f'        <key>starts_at</key>\n'
        plist_content += f'        <string>{time_accumulator:.6f}</string>\n'
        plist_content += f'        <key>ends_at</key>\n'
        plist_content += f'        <string>{(time_accumulator + note_length_in_seconds):.6f}</string>\n'
        plist_content += f'        <key>key</key>\n'
        plist_content += f'        <string>{note_num}</string>\n'
        plist_content += f'        <key>spell</key>\n'
        plist_content += f'        <string>{lyric}</string>\n'
        plist_content += f'        <key>velocity</key>\n'
        plist_content += f'        <string>0.800000</string>\n'
        plist_content += '      </dict>\n'

        # Atualiza o acumulador de tempo
        time_accumulator += note_length_in_seconds

    plist_content += '    </array>\n'
    plist_content += '  </dict>\n'
    plist_content += '</plist>\n'

    # Escreve o conteúdo gerado no arquivo de saída
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plist_content)


# Função para carregar e converter o arquivo UST
def load_ust_and_convert():
    ust_file = filedialog.askopenfilename(
        title="Selecione o arquivo UST",
        filetypes=[("UST files", "*.ust")]
    )
    if not ust_file:
        return

    try:
        ust_data = read_ust_file(ust_file)

        if not ust_data:  # Se houver erro ou dados vazios
            return

        # Gerar o arquivo Misaki
        output_file = filedialog.asksaveasfilename(
            title="Salvar arquivo Misaki",
            defaultextension=".misaki",
            filetypes=[("Misaki files", "*.misaki")]
        )
        if not output_file:
            return

        tempo = 120  # Usando tempo fixo como 120 BPM
        convert_to_misaki(ust_data, output_file, tempo)
        messagebox.showinfo("Sucesso", f"Arquivo Misaki salvo em: {output_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Conversor UST para Misaki")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# Botão para carregar o arquivo UST e converter
convert_button = tk.Button(frame, text="Converter UST para Misaki", command=load_ust_and_convert)
convert_button.grid(row=0, column=0, pady=10)

root.mainloop()
