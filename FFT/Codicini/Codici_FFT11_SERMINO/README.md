# Informazioni cruciali se si vuole usare questi file

Per essere ordinato (autism dell'altro Fra; io però ho l'autismo di distribuire su più file, lui nello stesso file: questo perché, essendo un CHAD average C enjoyer, mi piace overcomplicare i programmi spezzandoli), ho separato il processo di fitting in un file chiamato *fit.py* e il processo della RFFT in un file chiamato *plot.py*. 
- Il programma *fit.py* è fatto in maniera tale che, se runnato, restituisce $\omega$ del segnale sinusoidale nel file passato. Ciò è possibile cambiando manualmente il nome del file all'interno del file fit.py: **NON CAMBIARE ALTRO**.
- Il programma *plot.py* richiama la funzione *fitting* presente all'interno di fit.py, a cui passa per singolo file il valore $p_0$ necessario per far convergere il fit.

P.S: quanto cazzo è bello definire 70 struct differenti in 70 file header diversi. C peak language