import tkinter as tk
from tkinter import ttk

class EstatisticaCoresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Estatística de Preferência de Cores")
        self.root.geometry("650x650")
        
        # Configuração da interface principal
        self.root.config(bg="#E6E6FA")
        self.frame_inputs = tk.Frame(self.root, bg="#FFF8DC", bd=2, relief="solid")
        self.frame_inputs.pack(pady=20, padx=20, fill="x")

        # Lista de cores e os respectivos códigos para as barras
        self.cores = [
            ("Azul", "#1E90FF"), ("Verde", "#32CD32"), ("Vermelho", "#FF4500"), 
            ("Rosa", "#FF69B4"), ("Laranja", "#FFA500"), ("Amarelo", "#FFD700"), 
            ("Roxo", "#8A2BE2"), ("Preto", "#000000"), ("Cinza", "#A9A9A9"), 
            ("Branco", "#FFFFFF"), ("Ciano", "#00FFFF")
        ]

        self.inputs = {}
        for cor, _ in self.cores:
            row = tk.Frame(self.frame_inputs, bg="#FFF8DC")
            row.pack(fill="x", pady=2)
            label = tk.Label(row, text=f"{cor}:", width=10, anchor="w", bg="#FFF8DC", font=("Arial", 10, "bold"))
            label.pack(side="left")
            entry = tk.Entry(row, width=10)
            entry.pack(side="left")
            self.inputs[cor] = entry

        # Botão para calcular
        self.btn_calcular = tk.Button(self.root, text="Calcular", command=self.calcular_estatisticas, bg="#4682B4", fg="white", font=("Arial", 12, "bold"))
        self.btn_calcular.pack(pady=10)

        # Exibição dos resultados
        self.label_total = tk.Label(self.root, text="", bg="#E6E6FA", font=("Arial", 12, "bold"))
        self.label_total.pack(pady=10)

        # Configuração do Canvas para os resultados com Scrollbar
        self.canvas = tk.Canvas(self.root, bg="#E6E6FA", highlightthickness=0)
        self.frame_resultados = tk.Frame(self.canvas, bg="#E6E6FA")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)
        
        # Adiciona o frame de resultados ao Canvas
        self.canvas.create_window((0, 0), window=self.frame_resultados, anchor="nw")
        self.frame_resultados.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        # Atualiza a região de visualização do Canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def calcular_estatisticas(self):
        # Coleta e validação dos dados
        total_pessoas = 0
        contagem_cores = {}
        
        for cor, entry in self.inputs.items():
            try:
                quantidade = int(entry.get())
                if quantidade < 0:
                    quantidade = 0
                contagem_cores[cor] = quantidade
                total_pessoas += quantidade
            except ValueError:
                contagem_cores[cor] = 0

        # Exibe o total de pessoas
        self.label_total.config(text=f"Total de pessoas pesquisadas: {total_pessoas}")
        
        # Limpa os resultados anteriores
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        
        # Exibe as porcentagens em formato de barra com cores
        for (cor, hex_cor), quantidade in zip(self.cores, contagem_cores.values()):
            porcentagem = (quantidade / total_pessoas * 100) if total_pessoas > 0 else 0

            # Linha da cor
            row = tk.Frame(self.frame_resultados, bg="#E6E6FA")
            row.pack(fill="x", pady=2)

            # Nome da cor
            label_cor = tk.Label(row, text=cor, width=10, anchor="w", bg="#E6E6FA", font=("Arial", 10, "bold"))
            label_cor.pack(side="left")

            # Barra de porcentagem
            barra = ttk.Progressbar(row, length=300, maximum=100, style=f"{cor}.Horizontal.TProgressbar")
            barra['value'] = porcentagem
            barra.pack(side="left", padx=5, pady=2)

            # Porcentagem ao lado da barra
            label_porcentagem = tk.Label(row, text=f"{porcentagem:.2f}%", width=6, anchor="w", bg="#E6E6FA", font=("Arial", 10, "bold"))
            label_porcentagem.pack(side="left")

            # Estilo da barra
            style = ttk.Style()
            style.configure(f"{cor}.Horizontal.TProgressbar", troughcolor="#DCDCDC", background=hex_cor, thickness=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = EstatisticaCoresApp(root)
    root.mainloop()
