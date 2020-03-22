import imagesearch

execfile('loaddata.py')

src = imagesearch.Searcher('test.db',voc)

nbr_results = 6
res = [w[1] for w in src.query(imlist[0])[:nbr_results]]
imagesearch.plot_results(src,res)
