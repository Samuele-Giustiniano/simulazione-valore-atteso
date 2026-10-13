# Simulazione del valore atteso nel breve, medio e lungo periodo

Programma in Python sviluppato per la prova finale di Analisi Matematica II
(*Equazioni differenziali e modelli dinamici: analisi del valore atteso nel lungo periodo*),
Corso di Laurea in Ingegneria Informatica.

Mostra come, ripetendo molte volte una prova casuale, la media dei risultati si avvicina al valore atteso teorico.

## Il modello

Ogni prova ha due esiti possibili:

- -4 con probabilità 0,4
- +6 con probabilità 0,6

Il valore atteso è μ = (-4)·0,4 + 6·0,6 = 2.

Accanto alla simulazione casuale c'è un modello continuo, descritto dall'equazione differenziale

```
m'(t) = λ · (μ − m(t))     con soluzione     m(t) = μ + (m0 − μ) · e^(−λt)
```

che descrive l'avvicinamento di una media al valore atteso.

## Cosa produce

Il programma genera cinque grafici (cartella `output_simulazione_valore_atteso`):

1. risultato cumulato reale e valore atteso cumulato dopo 100 prove;
2. lo stesso dopo 1.000 prove;
3. lo stesso dopo 10.000 prove;
4. media empirica e valore atteso teorico;
5. soluzione continua m(t) del modello differenziale.

Con il seme usato (198) i risultati sono sempre riproducibili: la media empirica è 1,5 dopo 100 prove, 2,16 dopo 1.000 e 1,999 dopo 10.000.

## Come eseguirlo

Serve Python 3.9 o successivo.

```bash
pip install -r requirements.txt
python simulazione_valore_atteso.py
```

Librerie usate: NumPy (calcolo e generazione casuale) e Matplotlib (grafici).
