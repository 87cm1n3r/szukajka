from pathlib import Path
import numpy as np

cwd = Path(__file__).parents[0]
with open(str(cwd) + '/src.txt', encoding='UTF-8') as f:
    source_text = f.read()

wordlist=np.load("rank_lista.npy")




def szukaj_frazy(text, word, l=0): #(porcja tekstu, fraza do szukania)
    id_arr = []
    try:
        for litera in word:
            i=text[l:].index(litera)
            id_arr.append(l+i)
            l+=i+1
    except:
        return False
    return id_arr


def dopasowywanie_frazy(user_input, wordlist=wordlist, text=source_text, N=1, l=0): #(to wpisuje user, wordlista, porcja tekstu, ile wynikow syswietlic)
    wyniki=[]
    if user_input:
        wordlist = [x for x in wordlist if x.startswith(user_input.lower())] #tutaj jeśli ma zaczynać sie na user_input
#        wordlist = list(filter(lambda x: user_input in x, wordlist)) #tutaj jeśli ma zawierać user_input
        if not wordlist: #co jesli nie znalazlo wpisanej frazy w na wordliscie
            wynik = szukaj_frazy(text, user_input, l)
            if wynik:
                return([[user_input, int(wynik[-1]/len(wynik)), wynik]])
            else:
                return False

    for word in wordlist:
        wynik = szukaj_frazy(text, word, l)
        if wynik:
            wyniki.append([word, int((wynik[-1]-l)/len(wynik)), wynik]) #[słowo; stosunek zajmowanego miejsca do dlugosci frazy (the less the better); array indeksow]

    wyniki = sorted(wyniki, key=lambda x:x[1])
    return(wyniki[:N]) 


def wybierz_fraze(l): #(kursor)
    fraza = input("Podej fraze:\n")
    wyniki = dopasowywanie_frazy(fraza, wordlist, source_text[l:l+batch_size], 10)
    if not wyniki:
        print("Nie znaleziono takiej frazy, jeszcze raz wpisz")
        return False
    for e, entry in enumerate(wyniki):
        print(e+1, entry)
    kture = input("Kture wybrac(1-10), 0-repeat:\n")
    if int(kture)==0:
        return False
    else:
        return wyniki[int(kture)-1]



l=0 #kursor
batch_size=200 #tyle znakow w przod patrzy
podsumowanie = []
wygenerowane_frazy = ""

'''
while (l+batch_size<len(source_text)): #taka sobie pętelka
    zwrot = wybierz_fraze(l)
    if not zwrot:   #co jesli nie ma takiego slowa
        continue
    for item in zwrot[2]:
        podsumowanie.append(item+l)
    wygenerowane_frazy+=zwrot[0]+" "
    l+=zwrot[2][-1]+1 #przeswa kursor
    print("\nWygenerowano jak narazie:") #przeswa kursor
    print("\n", podsumowanie, "\n", wygenerowane_frazy)

'''