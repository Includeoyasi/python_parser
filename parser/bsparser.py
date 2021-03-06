# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from settings import *


def advtFilter(tree):

	""" Фильтрует статью от возможной рекламы других похожих статей.

		В качестве параметра принимает дерево тегов и ищет внутри упомянание или намёк на другую статью,
		в случае нахождения удаляет. 

	"""

	advts = tree.find_all(["article","aside"])
	for advt in advts:
		advt.clear()
	return True

def parseArticle(tree):

	""" Парсит и формирует текст статьи.
	
		В качестве параметра принимает дерево тегов. После формирования текста вызывает функцию форматирования
		и возвращает уже готовую для чтения статью.

	"""

	article = ''
	if advtFilter(tree)==False:
		return 'only advertisement'
	paragraphs = tree.find_all(["p","h1","h2"])
	for p in paragraphs:
		if p.find_all('a'):
			href ='['+p.a['href']+'] '+p.a.text
			p.a.clear()
			p.a.append(href)
		if p.text!='':
			if p.text[0].islower():
				article+=' '+p.text
			else:
				article+='\n\n'+'    '+p.text
	result = formatArticle(article)
	return result

def formatArticle(article):

	""" Форматирует статью для более удобного чтения.

		В качестве параметра принимает текст статьи и с учётом заданного переноса строк форматирует её.
		Возвращает отформатированную статью.

		Для реализации переноса строк использует функцию splitString.
		Так же игнорирует возможный скрытый текст с рекламой подписки на портал.

	"""

	result = ''
	for string in article.split('\n\n'):
		subscription = ' Подпишитесь на '.decode('utf8')
		if subscription not in string and string!='':
			if len(string)<maxlength:
				result+=string+'\n\n'
			else:
				result+=splitString(string)+'\n\n'
	return result

def splitString(string):

	""" Нарезает строки.

		В качестве параметра принимает текст строки, которая подлежит нарезке.
		Разбирает строку и собирает её заного, вставляя в необходимые места символ переноса.
		Возвращает нарезанную строку.

	"""

	result = ''
	i = 0
	chackpoint = 0
	savedstring = ''
	for char in string:
		if i<=maxlength:
			i+=1
			if char == ' ':
				chackpoint = i
			savedstring += char
		else:
			savedstring += char
			result+=savedstring[0:chackpoint]+'\n'
			savedstring=savedstring.replace(savedstring[0:chackpoint],'')
			i=i-chackpoint+1
	result+=savedstring

	return result

def testArticle(tree):

	""" Проверяет точность попадания в тело статьи.

		В качестве параметра принимает дерево тегов, внутри которого ищет html элементы,
		которые наиболее свойственны онлайн пабликациям.
		Возвращает дерево тегов.

		В случае несовпадения перепрыгивает на один элемент выше и вызывает себя рекурсивно.
		Для работы необходимо задать параметр accuracy, определяющий критерии отбора.

	"""

	if tree.find_all('p'):
		if tree.find_all('img'):
			return tree
		else:
			if accuracy<2:
				print('!!!WARNING!!! This article has no picture')
				return tree
			else:
				return testArticle(tree.parent)
	else:
		return testArticle(tree.parent)

def writeArticle(article, url):

	"""	Создаёт файл c уникальным именем и записывает в него готовую статью. """

	fileName = url.split(':/')[1]
	fileName = fileName.replace('/','-')
	file = open('articles\{0}.txt'.format(fileName), 'w')
	for string in article:
		file.write(string.encode('utf-8'))
	file.close()
	return 0

def main():

	""" Основная функция программы.

		Отправляет запрос на заданный адрес,
		после чего формирует дерево элементов с помощью библиотеки BeautifulSoup
		и ищет предпологаемое оглавление статьи внутри дерева,
		после чего запускает цепочку функция для формирования результата парсинга.

	"""
	try:
		url = raw_input('Please enter URL: ')
	except(EOFError):
		print('You got EOFError')
	contentPage = requests.get(url).text
	soup = BeautifulSoup(contentPage, 'html.parser')
	body = soup.find('h1')
	if body:
		if accuracy<1:
			result = parseArticle(body.parent)
		else:
			result = parseArticle(testArticle(body.parent))
	else:
		print('h1 is not found')
		return 0

	return writeArticle(result, url)

if __name__ == '__main__':
	main()