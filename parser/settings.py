# -*- coding: utf-8 -*-
# Начальные параметры для парсинга статьи


""" Параметр maxlength определяет длинну строки. Каждый n-ый сивол будет осуществляться пересно по словам. """

maxlength=80


""" Параметр accuracy определяет точность попадания в тело статьи.

	0 - будет взят блог, в котором лежит тег оглавления <h1>.
	1 - будет взят блог, в котором лежит тег оглавления <h1> и рядом имеются теги параграфов <p>.
	2 - будет взят блог, в котором лежат одновременно тег оглавления <h1>, теги параграфов <p> и тег картинки <img>.

"""
accuracy=1 