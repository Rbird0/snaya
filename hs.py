dico = {1: 3333, 2: 1155, 3: 1115, 4: 1111, 5: 1110, 6: 1100, 7: 1000, 8: 900, 9: 800, 10: 700}
newScore = 400

oldDico = {0 : 0}

for j in range(1, 11) :
	oldDico[j] = dico[j]

for j in range(1,11) :
	if newScore > dico[j] :
		dico[j+1] = oldDico[j]
	if newScore > oldDico[j] and (newScore <= oldDico[j-1] or oldDico[j-1] is oldDico[0]) :
		dico[j] = newScore

dico[11] = 0
del dico[11]

print(dico)