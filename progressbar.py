import progressbar
from time import sleep
bar = progressbar.progressbar(maxval=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
for i in xrange(20):
    bar.update(i+1)
    sleep(0.1)
bar.finish()
