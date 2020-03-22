import imagesearch

execfile('loaddata.py')

src = imagesearch.Searcher('test.db',voc)
print 'try a query...'
print src.query(imlist[0])[:10]
