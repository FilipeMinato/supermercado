"""
Simulador de Caixa de Mercado com Interface Tkinter
---------------------------------------------------
O sistema permite adicionar produtos ao carrinho clicando em botões.
Ao finalizar a compra, o cliente pode:

- Adicionar recarga de celular
- Optar por entrega em casa (+R$15)
- Adquirir vale-gás (+R$50)
- Informar CPF na nota
- Obter desconto se for cliente cadastrado
- Escolher pagamento por PIX (5% de desconto) ou cartão (1 a 3x)

Descontos acumulativos: cadastro + PIX = 10% de desconto.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog

class CaixaMercado:
    def __init__(self, root):
        self.root = root
        self.root.title("Caixa de Mercado")

        # Variáveis principais
        self.total = 0.0
        self.carrinho = []
        self.cliente_cadastrado = False
        self.cpf = ""
        self.entrega = False
        self.vale_gas = False
        self.pagamento = ""
        self.parcelas = 1
        self.total_label = None  # Label para exibir o total

        # Dicionário com produtos disponíveis
        self.produtos = {
            "Arroz 5kg": 20.00,
            "Feijão 1kg": 7.50,
            "Óleo de soja 900ml": 6.00,
            "Macarrão 500g": 4.50,
            "Leite 1L": 3.20,
        }

        self.criar_interface()

    # Cria todos os elementos da interface
    def criar_interface(self):
        tk.Label(self.root, text="Clique nos produtos para adicionar:").pack(pady=5)

        # Botões para cada produto
        for nome, preco in self.produtos.items():
            tk.Button(
                self.root, text=f"{nome} - R$ {preco:.2f}", width=30,
                command=lambda n=nome, p=preco: self.adicionar_item(n, p)
            ).pack(pady=2)

        # Total em destaque
        self.total_label = tk.Label(self.root, text="TOTAL: R$ 0.00", font=("Arial", 20, "bold"), fg="blue")
        self.total_label.pack(pady=10)

        # Carrinho de compras (campo de texto)
        self.txt_carrinho = tk.Text(self.root, height=15, width=50)
        self.txt_carrinho.pack(pady=10)

        # Botão para finalizar compra
        tk.Button(self.root, text="Finalizar Compra", bg="green", fg="white", width=30,
                  command=self.finalizar_compra).pack(pady=10)

    # Adiciona item ao carrinho
    def adicionar_item(self, nome, preco):
        self.carrinho.append((nome, preco))
        self.total += preco
        self.atualizar_carrinho()

    # Atualiza o conteúdo do carrinho na interface
    def atualizar_carrinho(self):
        self.txt_carrinho.delete("1.0", tk.END)
        for item in self.carrinho:
            self.txt_carrinho.insert(tk.END, f"{item[0]} - R$ {item[1]:.2f}\n")
        self.txt_carrinho.insert(tk.END, f"\nTOTAL: R$ {self.total:.2f}")
        if self.total_label:
            self.total_label.config(text=f"TOTAL: R$ {self.total:.2f}")

    # Etapas ao finalizar a compra
    def finalizar_compra(self):
        self.recarga_popup()  # Oferece recarga de celular

        # Outras opções e perguntas
        self.vale_gas = messagebox.askyesno("Vale Gás", "Deseja adicionar Vale Gás por R$50?")
        self.entrega = messagebox.askyesno("Entrega", "Deseja entrega em casa por R$15?")
        self.cliente_cadastrado = messagebox.askyesno("Cadastro", "Cliente possui cadastro? (5% de desconto)")
        self.cpf = simpledialog.askstring("CPF na Nota", "Digite o CPF (ou deixe em branco):")
        self.pagamento_popup()  # Pergunta forma de pagamento e parcelas

        # Adiciona serviços ao carrinho
        if self.vale_gas:
            self.carrinho.append(("Vale Gás", 50.00))
            self.total += 50.00
        if self.entrega:
            self.carrinho.append(("Entrega em casa", 15.00))
            self.total += 15.00

        # Calcula descontos
        desconto_total = 0.0
        if self.cliente_cadastrado:
            desconto_total += 0.05
        if self.pagamento == "PIX":
            desconto_total += 0.05

        valor_desconto = self.total * desconto_total
        total_final = self.total - valor_desconto

        # Monta o resumo da compra
        msg = f"Subtotal: R$ {self.total:.2f}\n"
        if desconto_total > 0:
            msg += f"Desconto ({int(desconto_total*100)}%): -R$ {valor_desconto:.2f}\n"

        if self.pagamento == "CARTÃO":
            valor_parcela = total_final / self.parcelas
            msg += f"Pagamento em {self.parcelas}x de R$ {valor_parcela:.2f} sem juros\n"
        else:
            msg += "Pagamento via PIX\n"

        msg += f"Total a pagar: R$ {total_final:.2f}\n"
        if self.cpf:
            msg += f"CPF na nota: {self.cpf}"

        # Exibe mensagem final e encerra
        messagebox.showinfo("Compra Finalizada", msg)
        self.root.destroy()

    # Pergunta se deseja fazer recarga de celular
    def recarga_popup(self):
        op = simpledialog.askinteger("Recarga", "Deseja recarga de celular?\n1 - R$15\n2 - R$25\n3 - R$35\n4 - R$50\n0 - Não")
        valores = {1: 15, 2: 25, 3: 35, 4: 50}
        if op in valores:
            valor = valores[op]
            self.carrinho.append(("Recarga Celular", valor))
            self.total += valor
            self.atualizar_carrinho()

    # Janela que pergunta forma de pagamento e, se cartão, número de parcelas
    def pagamento_popup(self):
        while True:
            try:
                op = int(simpledialog.askstring("Pagamento", "Forma de pagamento:\n1 - PIX (5% de desconto)\n2 - Cartão de crédito (1 a 3x)"))
                if op == 1:
                    self.pagamento = "PIX"
                    break
                elif op == 2:
                    self.pagamento = "CARTÃO"
                    while True:
                        try:
                            parcelas = int(simpledialog.askstring("Parcelas", "Número de parcelas (1 a 3):"))
                            if parcelas in [1, 2, 3]:
                                self.parcelas = parcelas
                                break
                            else:
                                raise ValueError
                        except:
                            messagebox.showerror("Erro", "Número de parcelas inválido.")
                    break
                else:
                    raise ValueError
            except:
                messagebox.showerror("Erro", "Digite 1 para PIX ou 2 para Cartão.")

# Execução principal do programa
if __name__ == "__main__":
    root = tk.Tk()
    app = CaixaMercado(root)
    root.mainloop()
