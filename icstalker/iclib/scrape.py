#!usr/bin/python

from BeautifulSoup import BeautifulSoup as bs

def schedule(text):
	soup = bs(text)
	l = soup.body.table.findAll('td', attrs={'class':'scheduleBody'})
	final = []
	for row in l:
		if 'portal' in str(row):
			if row:
				sp = bs(str(row))
				url = sp.a['href']
				name = sp.a.b.contents[0]
				final.append({'url':url,'name':name})
	return final


def classes(text):
	soup = bs(text)
	search = soup.body.findAll('td',attrs={'align':'right'})
	for row in search:
		if row.br:
			set = str(row)
	soup = bs(set)
	grade = soup.td.contents[0]
	return grade









if __name__ == "__main__":
	f=open('../schedule.html','r')
	t=f.read()
	f.close()
	print schedule(t)
