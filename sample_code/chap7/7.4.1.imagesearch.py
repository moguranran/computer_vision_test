import sift
import imagesearch

execfile('loaddata.py')

src = imagesearch.Searcher('test.db',voc)
locs,descr = sift.read_features_from_file(featlist[0])
iw = voc.project(descr)

print 'ask using a histogram...'
print src.candidates_from_histogram(iw)[:10]

