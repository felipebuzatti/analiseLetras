#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import sys;
import requests;
import io
import json
import os
import urllib2
from PIL import Image

api_vag = "http://api.vagalume.com.br/search.php"

if __name__ == "__main__":

	nomes_arqs_anos = sys.argv[1:];
	if len(nomes_arqs_anos) == 0:
		print "\nSintaxe: <nome_script> <arq_lista_musicas...>\n";
		sys.exit(1);

	for nome_arq_ano in nomes_arqs_anos:
		lista_letras = [];

		with open(nome_arq_ano) as arq_ano:
			print "Processando arquivo {0}".format(nome_arq_ano);
			serial = None;
			udig = None;
			for linha_musica in arq_ano:
				musica, artista = linha_musica.strip().split("-");
				# print "Buscando letra para música {0} de {1}".format(musica, artista);
				parametros = {'mus':musica, 'art':artista};

				if udig != None:
					parametros['udig'] = udig;
					parametros['serial'] = serial;
					udig = None;
					serial = None;

				ret_letra = requests.get(api_vag, params=parametros);
				ret_json = ret_letra.json();

				if 'captcha' in ret_json:
					end_img = ret_json['captcha_img'];
					fd = urllib2.urlopen(end_img)
					image_file = io.BytesIO(fd.read())
					img = Image.open(image_file);
					img.show();
					udig = raw_input("Digite o captcha na imagem mostrada (4 dígitos)");
					serial = ret_json['serial'];

				try:
					lista_letras.append((linha_musica.strip(), ret_json['mus'][0]['text']));
					# print "Letra buscada com sucesso para arquivo {0}".format(linha_musica);
				except KeyError:
					if ret_json['type'] == u'song_notfound' or ret_json['type'] == u'notfound':
						print "Não foi encontrada letra para {0}".format(linha_musica);
					else:
						import pdb; pdb.set_trace();

			print "arquivo de ano {0} processado com sucesso".format(nome_arq_ano);

		os.remove(nome_arq_ano);

		novo_diretorio = nome_arq_ano + "/";
		os.makedirs(novo_diretorio);

		for nome_arq, letra in lista_letras:
			caminho_arq = novo_diretorio + nome_arq;
			with open(caminho_arq, "w") as arq_letra:
				arq_letra.write(letra.encode('utf8'));

