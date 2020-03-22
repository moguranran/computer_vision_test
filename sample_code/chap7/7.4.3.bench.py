import imagesearch

execfile('loaddata.py')

src = imagesearch.Searcher('test.db',voc)

#print imagesearch.compute_ukbench_score(src,imlist)

print imagesearch.compute_ukbench_score(src,imlist[:100])

