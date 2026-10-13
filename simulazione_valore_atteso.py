"""
Simulazione del valore atteso nel breve, medio e lungo periodo.

Il programma genera cinque grafici:

1. risultato cumulato reale ed EV cumulato dopo 100 prove;
2. risultato cumulato reale ed EV cumulato dopo 1.000 prove;
3. risultato cumulato reale ed EV cumulato dopo 10.000 prove;
4. media empirica M_n e valore atteso teorico mu;
5. soluzione continua m(t) del modello differenziale.

Modello casuale:

    X_k = -4 con probabilità 0,4
    X_k =  6 con probabilità 0,6

Valore atteso:

    mu = (-4)*0,4 + 6*0,6 = 2

Modello continuo:

    m'(t) = lambda * (mu - m(t))

con soluzione:

    m(t) = mu + (m0 - mu) * exp(-lambda * t)
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# -------------------------------------------------------------------
# 1. PARAMETRI DEL MODELLO CASUALE
# -------------------------------------------------------------------

SEME = 198
# Seme del generatore pseudocasuale.
# Permette di ottenere sempre la stessa sequenza e gli stessi grafici.

VALORI = np.array([-4.0, 6.0])
# Possibili risultati della singola prova X_k.

PROBABILITA = np.array([0.4, 0.6])
# Probabilità associate rispettivamente ai valori -4 e +6.

NUMERO_PROVE_MASSIMO = 10_000
# Numero massimo di prove generate.

INTERVALLI = {
    "breve": 100,
    "medio": 1_000,
    "lungo": 10_000,
}
# Intervalli usati per i primi tre grafici.


# -------------------------------------------------------------------
# 2. PARAMETRI DEL MODELLO CONTINUO
# -------------------------------------------------------------------

M0 = -4.0
# Condizione iniziale della soluzione continua: m(0) = -4.

LAMBDA = 0.5
# Velocità di avvicinamento della soluzione continua al valore atteso.

TEMPO_FINALE = 15.0
# Estremo finale dell'intervallo temporale rappresentato.

NUMERO_PUNTI_TEMPORALI = 500
# Numero di punti usati per disegnare la curva continua.


# -------------------------------------------------------------------
# 3. CARTELLA DI OUTPUT
# -------------------------------------------------------------------

CARTELLA_SCRIPT = Path(__file__).resolve().parent

CARTELLA_OUTPUT = (
    CARTELLA_SCRIPT / "output_simulazione_valore_atteso"
)
# Cartella nella quale vengono salvati tutti i grafici.

CARTELLA_OUTPUT.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# 4. FUNZIONI DI SUPPORTO
# -------------------------------------------------------------------

def salva_grafico(nome_file: str) -> None:
    """Salva il grafico corrente in formato PNG e chiude la figura."""
    percorso = CARTELLA_OUTPUT / nome_file
    plt.tight_layout()
    plt.savefig(percorso, dpi=300, bbox_inches="tight")
    plt.close()


def grafico_cumulativo(
    prove: np.ndarray,
    risultato_cumulato: np.ndarray,
    ev_cumulato: np.ndarray,
    numero_prove: int,
    titolo: str,
    nome_file: str,
) -> None:
    """
    Disegna il confronto tra:

        W_n = somma dei risultati reali
        E_n = n * mu

    per il numero di prove indicato.
    """
    plt.figure(figsize=(11, 6))

    plt.plot(
        prove[:numero_prove],
        risultato_cumulato[:numero_prove],
        color="green",
        linewidth=1.8,
        label="Risultato cumulato reale $W_n$",
    )

    plt.plot(
        prove[:numero_prove],
        ev_cumulato[:numero_prove],
        color="gold",
        linewidth=2.2,
        label="EV cumulato $E_n = n\\mu$",
    )

    plt.axhline(
        y=0,
        color="black",
        linewidth=0.8,
    )

    plt.xlabel("Numero di prove $n$")
    plt.ylabel("Risultato cumulato")
    plt.title(titolo)
    plt.legend()
    plt.grid(True, alpha=0.3)

    salva_grafico(nome_file)


# -------------------------------------------------------------------
# 5. CALCOLO DEL VALORE ATTESO
# -------------------------------------------------------------------

mu = float(np.sum(VALORI * PROBABILITA))
# Calcolo automatico:
# mu = (-4)*0,4 + 6*0,6 = 2.


# -------------------------------------------------------------------
# 6. GENERAZIONE DELLA SUCCESSIONE CASUALE
# -------------------------------------------------------------------

rng = np.random.default_rng(SEME)
# Creazione del generatore pseudocasuale.

risultati = rng.choice(
    VALORI,
    size=NUMERO_PROVE_MASSIMO,
    p=PROBABILITA,
)
# Generazione della successione X_1, X_2, ..., X_10000.

prove = np.arange(1, NUMERO_PROVE_MASSIMO + 1)
# Numeri progressivi delle prove: 1, 2, ..., 10000.


# -------------------------------------------------------------------
# 7. CALCOLO DELLE GRANDEZZE DISCRETE
# -------------------------------------------------------------------

risultato_cumulato = np.cumsum(risultati)
# W_n = X_1 + X_2 + ... + X_n.

ev_cumulato = prove * mu
# E_n = n * mu.

media_empirica = risultato_cumulato / prove
# M_n = W_n / n.


# -------------------------------------------------------------------
# 8. PRIMO GRAFICO: BREVE PERIODO
# -------------------------------------------------------------------

grafico_cumulativo(
    prove=prove,
    risultato_cumulato=risultato_cumulato,
    ev_cumulato=ev_cumulato,
    numero_prove=INTERVALLI["breve"],
    titolo="Breve periodo: risultato reale ed EV cumulato",
    nome_file="01_breve_periodo.png",
)


# -------------------------------------------------------------------
# 9. SECONDO GRAFICO: MEDIO PERIODO
# -------------------------------------------------------------------

grafico_cumulativo(
    prove=prove,
    risultato_cumulato=risultato_cumulato,
    ev_cumulato=ev_cumulato,
    numero_prove=INTERVALLI["medio"],
    titolo="Medio periodo: risultato reale ed EV cumulato",
    nome_file="02_medio_periodo.png",
)


# -------------------------------------------------------------------
# 10. TERZO GRAFICO: LUNGO PERIODO
# -------------------------------------------------------------------

grafico_cumulativo(
    prove=prove,
    risultato_cumulato=risultato_cumulato,
    ev_cumulato=ev_cumulato,
    numero_prove=INTERVALLI["lungo"],
    titolo="Lungo periodo: risultato reale ed EV cumulato",
    nome_file="03_lungo_periodo.png",
)


# -------------------------------------------------------------------
# 11. QUARTO GRAFICO: MEDIA EMPIRICA
# -------------------------------------------------------------------

plt.figure(figsize=(11, 6))

plt.plot(
    prove,
    media_empirica,
    linewidth=1.4,
    label="Media empirica $M_n = W_n/n$",
)

plt.axhline(
    y=mu,
    linestyle="--",
    linewidth=2,
    label="Valore atteso teorico $\\mu = 2$",
)

indici_controllo = [100, 1_000, 10_000]

for n in indici_controllo:
    valore_medio = media_empirica[n - 1]

    plt.scatter(
        n,
        valore_medio,
        s=45,
        zorder=3,
    )

    plt.annotate(
        f"$M_{{{n}}}={valore_medio:.3f}$",
        xy=(n, valore_medio),
        xytext=(8, 10),
        textcoords="offset points",
        fontsize=9,
    )

plt.xlabel("Numero di prove $n$")
plt.ylabel("Media empirica $M_n$")
plt.title("Convergenza della media empirica verso il valore atteso")
plt.legend()
plt.grid(True, alpha=0.3)

salva_grafico("04_media_empirica.png")


# -------------------------------------------------------------------
# 12. QUINTO GRAFICO: SOLUZIONE CONTINUA
# -------------------------------------------------------------------

t = np.linspace(
    0.0,
    TEMPO_FINALE,
    NUMERO_PUNTI_TEMPORALI,
)
# Creazione di 500 istanti compresi tra 0 e 15.

m_t = mu + (M0 - mu) * np.exp(-LAMBDA * t)
# Applicazione della soluzione:
# m(t) = mu + (m0 - mu) * e^(-lambda t).

plt.figure(figsize=(11, 6))

plt.plot(
    t,
    m_t,
    linewidth=2,
    label="Soluzione continua $m(t)$",
)

plt.axhline(
    y=mu,
    linestyle="--",
    linewidth=2,
    label="Equilibrio $\\mu = 2$",
)

plt.scatter(
    [0],
    [M0],
    s=50,
    zorder=3,
    label="Condizione iniziale $m(0)=-4$",
)

plt.xlabel("Tempo continuo $t$")
plt.ylabel("Valore di $m(t)$")
plt.title("Soluzione continua e convergenza verso il valore atteso")
plt.legend()
plt.grid(True, alpha=0.3)

salva_grafico("05_soluzione_continua.png")


# -------------------------------------------------------------------
# 13. STAMPA DEI RISULTATI PRINCIPALI
# -------------------------------------------------------------------

print("SIMULAZIONE COMPLETATA")
print("-" * 65)
print(f"Valore atteso teorico mu: {mu:.4f}")
print()

for nome_periodo, n in INTERVALLI.items():
    w_n = risultato_cumulato[n - 1]
    e_n = ev_cumulato[n - 1]
    m_n = media_empirica[n - 1]

    print(
        f"{nome_periodo.capitalize():>6} periodo | "
        f"n = {n:>5} | "
        f"W_n = {w_n:>8.2f} | "
        f"E_n = {e_n:>8.2f} | "
        f"M_n = {m_n:.4f}"
    )

print()
print("Valori della soluzione continua:")

for tempo in [0, 1, 2, 5, 10, 15]:
    valore = mu + (M0 - mu) * np.exp(-LAMBDA * tempo)
    print(f"t = {tempo:>2} | m(t) = {valore:.6f}")

print()
print(f"Grafici salvati in: {CARTELLA_OUTPUT}")
