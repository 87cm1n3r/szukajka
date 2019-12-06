from pathlib import Path
import numpy as np

cwd = Path(__file__).parents[0]
with open(str(cwd) + '/src.txt', encoding='UTF-8') as f:
    source_text = f.read()

wordlist=np.load("rank_lista.npy")

#podsumowanie = []


def szukaj_slowa(text, word): #(porcja tekstu, fraza do szukania)
    l=0
    id_arr = []
    try:
        for litera in word:
            i=text[l:].index(litera)
            id_arr.append(l+i)
            l+=i+1
    except:
        return False
    return id_arr


def dopasowywanie_slowa(user_input, wordlist, text, N): #(to wpisuje user, wordlista, porcja tekstu, ile wynikow syswietlic)
    wyniki=[]
    if user_input:
        wordlist = [x for x in wordlist if x.startswith(user_input.lower())] #tutaj jeśli ma zaczynać sie na user_input
#        wordlist = list(filter(lambda x: user_input in x, wordlist)) #tutaj jeśli ma zawierać user_input
        if not wordlist: #co jesli nie znalazlo wpisanej frazy w na wordliscie
            wynik = szukaj_slowa(text, user_input) 
            return([[user_input, int(wynik[-1]/len(wynik)), wynik]])

    for word in wordlist:
        wynik = szukaj_slowa(text, word)
        if wynik:
            wyniki.append([word, int(wynik[-1]/len(wynik)), wynik]) #[słowo; stosunek zajmowanego miejsca do dlugosci slowa (the less the better); array indeksow]

    wyniki = sorted(wyniki, key=lambda x:x[1])
    return(wyniki[:N]) 

l=0 #kursor
batch_size=100 #tyle znakow w przod patrzy

# print(dopasowywanie_slowa("", wordlist, source_text[l:l+batch_size], 10))

'''
for word in wordlist:
    wynik = szukaj_slowa(source_text[l:l+batch_size], word)
    for ix in wynik:
        podsumowanie.append(ix+l)
    l+=wynik[-1]

print(podsumowanie)
'''