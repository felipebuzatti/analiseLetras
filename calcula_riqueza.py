#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import sys;
import numpy as np;
from matplotlib import pyplot as plt
import matplotlib
from nltk import word_tokenize;
from dircache import listdir


if __name__ == "__main__":
	
	nomes_dirs_anos = sys.argv[1:];
	if len(nomes_dirs_anos) == 0:
		print "\nSintaxe: <nome_script> <diretorio_letras...>\n";
		sys.exit(1);

	matriz_res = [];

	for nome_dir_ano in nomes_dirs_anos:
		print "Processando diretório {0}".format(nome_dir_ano);

		valores = []

		for nome_arq_texto in listdir(nome_dir_ano):
			caminho_arq_texto = nome_dir_ano + nome_arq_texto
			with open(caminho_arq_texto, "rb") as arq_texto:
				raw = arq_texto.read();
				tokens = [t for t in word_tokenize(raw) if t not in [",", ".", "!", "?", "?!", ";", "...", "(", ")", "/"]];

				def media_repeticoes(palavras):
					return len(palavras) / float(len(set(palavras)));

				valores.append(media_repeticoes(tokens));

		print "{0}: {1:.2f}±{2:.2f} ({3:.2f})".format(nome_dir_ano, np.mean(valores), np.std(valores), np.median(valores));
		matriz_res.append(list(valores));

	plt.boxplot(matriz_res, showmeans=True);
	plt.xticks(np.arange(len(matriz_res))+1.0, [n.strip()[:-1] for n in nomes_dirs_anos], rotation='vertical')

	# plt.errorbar(range(len(matriz_res)), [np.mean(v) for v in matriz_res], yerr=[np.std(v) for v in matriz_res])

	mediana_medianas = np.median(sum(matriz_res, []));
	media_medias = np.mean(sum(matriz_res, []));

	# plt.bar(range(len(matriz_res)), [np.mean(v) for v in matriz_res])
	# plt.xticks(np.arange(len(matriz_res))+0.5, [n.strip()[:-1] for n in nomes_dirs_anos], rotation='vertical')
	# plt.plot([0, len(matriz_res)+1], [media_medias]*2, color='b')
	

	plt.plot([-1, len(matriz_res)+1], [media_medias]*2, 'r--')
	# plt.grid(b=True, which='major', color='r', axis='y', linestyle='--')
	
	plt.tight_layout();
	plt.show();