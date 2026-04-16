import tkinter as tk
from tkinter import ttk


class AplicacionCotizacion:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Cotización")
        self.raiz.configure(bg="#e6e6e6")

        self.columnas = ["Cantidad", "Descripción", "Valor Unitario", "Total"]
        self.filas = []

        self.var_neto = tk.StringVar(value="$0")
        self.var_iva = tk.StringVar(value="$0")
        self.var_total = tk.StringVar(value="$0")

        self.var_nombre_ejecutivo = tk.StringVar(value="Emma Oliveros")
        self.var_cargo_ejecutivo = tk.StringVar(value="Ejecutiva de Ventas")

        self._construir_interfaz()
        self.agregar_fila()

    def _construir_interfaz(self):
        marco_principal = tk.Frame(self.raiz, bg="#e6e6e6", padx=18, pady=18)
        marco_principal.pack(fill="both", expand=True)

        tk.Label(
            marco_principal,
            text="■ GERMANIA ■",
            font=("Arial", 22, "bold"),
            fg="#d11d1d",
            bg="#e6e6e6",
        ).pack(pady=(0, 12))

        tk.Label(
            marco_principal,
            text="EQUIPOS CONTRA INCENDIO GREIG HERMANOS LTDA",
            font=("Arial", 11, "bold"),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            marco_principal,
            text="Empresa certificada según Decreto 44",
            font=("Arial", 10),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            marco_principal,
            text="Fono: 22 357 8163 – 6212403 | Cel: +56 9 9873 0662",
            font=("Arial", 10),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            marco_principal,
            text="Señores: Comunidad Rivas Vicuña 1214, Quinta Normal",
            font=("Arial", 10),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            marco_principal,
            text="Atención: Sr. Roberto Armijo",
            font=("Arial", 10),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x", pady=(0, 12))

        tk.Label(
            marco_principal,
            text=(
                "Estimados señores, junto con saludar, tenemos el agrado de presentar "
                "la siguiente cotización de equipos y servicios contra incendio:"
            ),
            wraplength=820,
            justify="left",
            font=("Arial", 10),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        self.marco_tabla = tk.Frame(marco_principal, bg="#2b2b2b", bd=1)
        self.marco_tabla.pack(fill="x")

        marco_botones_tabla = tk.Frame(marco_principal, bg="#e6e6e6")
        marco_botones_tabla.pack(fill="x", pady=(8, 10))

        ttk.Button(marco_botones_tabla, text="Agregar fila", command=self.agregar_fila).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(
            marco_botones_tabla, text="Eliminar fila", command=self.eliminar_fila
        ).pack(side="left", padx=(0, 14))

        ttk.Button(
            marco_botones_tabla,
            text="Agregar columna",
            command=self.agregar_columna,
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            marco_botones_tabla,
            text="Eliminar columna",
            command=self.eliminar_columna,
        ).pack(side="left")

        marco_totales = tk.Frame(marco_principal, bg="#e6e6e6")
        marco_totales.pack(fill="x", pady=(6, 10))

        self._crear_linea_total(marco_totales, "Neto:", self.var_neto)
        self._crear_linea_total(marco_totales, "IVA:", self.var_iva)
        self._crear_linea_total(marco_totales, "Total:", self.var_total)

        tk.Label(
            marco_principal,
            text="Plazo de entrega: Inmediata",
            font=("Arial", 10, "bold"),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            marco_principal,
            text="Forma de pago: A convenir",
            font=("Arial", 10, "bold"),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x", pady=(0, 14))

        tk.Label(
            marco_principal,
            text="Atentamente,",
            font=("Arial", 10),
            bg="#e6e6e6",
            anchor="w",
        ).pack(fill="x")

        tk.Entry(
            marco_principal,
            textvariable=self.var_nombre_ejecutivo,
            font=("Arial", 12, "bold"),
            relief="flat",
            bg="#e6e6e6",
            justify="left",
        ).pack(fill="x", pady=(8, 2))

        tk.Entry(
            marco_principal,
            textvariable=self.var_cargo_ejecutivo,
            font=("Arial", 11),
            relief="flat",
            bg="#e6e6e6",
            justify="left",
        ).pack(fill="x")

    def _crear_linea_total(self, padre: tk.Frame, etiqueta: str, variable: tk.StringVar):
        fila = tk.Frame(padre, bg="#e6e6e6")
        fila.pack(anchor="w")
        tk.Label(fila, text=etiqueta, font=("Arial", 11, "bold"), bg="#e6e6e6").pack(
            side="left"
        )
        tk.Label(fila, textvariable=variable, font=("Arial", 11), bg="#e6e6e6").pack(
            side="left"
        )

    def agregar_fila(self):
        nuevas_celdas = []
        for indice_columna, _ in enumerate(self.columnas):
            entrada = tk.Entry(self.marco_tabla, font=("Arial", 10), relief="solid", bd=1)
            if indice_columna == 0:
                entrada.insert(0, "1")
            elif indice_columna in (2, 3):
                entrada.insert(0, "0")
            entrada.bind("<KeyRelease>", self._actualizar_calculos_automaticos)
            nuevas_celdas.append(entrada)

        self.filas.append(nuevas_celdas)
        self._renderizar_tabla()
        self._actualizar_calculos_automaticos()

    def eliminar_fila(self):
        if not self.filas:
            return
        fila = self.filas.pop()
        for celda in fila:
            celda.destroy()
        self._renderizar_tabla()
        self._actualizar_calculos_automaticos()

    def agregar_columna(self):
        nombre = f"Columna {len(self.columnas) - 3}" if len(self.columnas) > 3 else "Columna 1"
        self.columnas.insert(-1, nombre)

        for fila in self.filas:
            entrada = tk.Entry(self.marco_tabla, font=("Arial", 10), relief="solid", bd=1)
            entrada.bind("<KeyRelease>", self._actualizar_calculos_automaticos)
            fila.insert(-1, entrada)

        self._renderizar_tabla()

    def eliminar_columna(self):
        # Se mantiene un mínimo de las cuatro columnas base para respetar el formato.
        if len(self.columnas) <= 4:
            return

        indice = len(self.columnas) - 2
        self.columnas.pop(indice)

        for fila in self.filas:
            celda = fila.pop(indice)
            celda.destroy()

        self._renderizar_tabla()
        self._actualizar_calculos_automaticos()

    def _renderizar_tabla(self):
        for widget in self.marco_tabla.grid_slaves():
            widget.grid_forget()

        for indice_columna, titulo in enumerate(self.columnas):
            encabezado = tk.Entry(
                self.marco_tabla,
                font=("Arial", 10, "bold"),
                relief="solid",
                bd=1,
                bg="#e31d1d",
                fg="white",
                justify="left",
            )
            encabezado.insert(0, titulo)
            encabezado.bind(
                "<FocusOut>",
                lambda evento, i=indice_columna: self._actualizar_nombre_columna(i, evento),
            )
            encabezado.grid(row=0, column=indice_columna, sticky="nsew")

        for indice_fila, fila in enumerate(self.filas, start=1):
            for indice_columna, celda in enumerate(fila):
                if indice_columna == len(self.columnas) - 1:
                    celda.configure(state="readonly")
                else:
                    celda.configure(state="normal")
                celda.grid(row=indice_fila, column=indice_columna, sticky="nsew")

        for indice_columna in range(len(self.columnas)):
            self.marco_tabla.grid_columnconfigure(indice_columna, weight=1)

    def _actualizar_nombre_columna(self, indice_columna: int, evento):
        self.columnas[indice_columna] = evento.widget.get().strip() or self.columnas[indice_columna]

    def _actualizar_calculos_automaticos(self, *_):
        total_neto = 0

        for fila in self.filas:
            if len(fila) < 4:
                continue

            cantidad = self._texto_a_numero(fila[0].get())
            valor_unitario = self._texto_a_numero(fila[2].get())
            total_fila = int(cantidad * valor_unitario)

            total_neto += total_fila
            fila[-1].configure(state="normal")
            fila[-1].delete(0, tk.END)
            fila[-1].insert(0, self._formatear_moneda(total_fila))
            fila[-1].configure(state="readonly")

        iva = int(total_neto * 0.19)
        total = total_neto + iva

        self.var_neto.set(self._formatear_moneda(total_neto))
        self.var_iva.set(self._formatear_moneda(iva))
        self.var_total.set(self._formatear_moneda(total))

    def _texto_a_numero(self, texto: str) -> float:
        texto_limpio = texto.replace("$", "").replace(".", "").replace(",", ".").strip()
        if not texto_limpio:
            return 0
        try:
            return float(texto_limpio)
        except ValueError:
            return 0

    def _formatear_moneda(self, valor: int) -> str:
        return f"${valor:,.0f}".replace(",", ".")


def main():
    raiz = tk.Tk()
    AplicacionCotizacion(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()