import re
import urllib2
import time

consoles = ['ps3', 'xbox360', 'ds', '3ds', 'psp', 'pc', 'ios', 'vita']

f = open("averages.txt", "w")
f.write("Data scraped on {0}\n\n\n".format(time.asctime()))

for console in sorted(consoles):
    metascores = []
    userscores = []
    progress = 0
    
    print "\nCurrent console: {0}\n".format(console)
    
    # Find number of pages using first page
    source = urllib2.urlopen("http://www.metacritic.com/browse/games/score/metascore/all/{0}?sort=desc&tag=supplementary-nav%3Bitem%3B6&page=0".format(console)).read()
    pages = [int(page) for page in re.findall(r'supplementary-nav%3Bitem%3B6&page=(\d+)', source)]
    
    # Determine last page
    if pages: number_of_pages = max(pages)
    else: number_of_pages = 0
    
    # Loop through available pages
    for page in range(0, number_of_pages+1):
        # Get page source
        if page:
            source = urllib2.urlopen("http://www.metacritic.com/browse/games/score/metascore/all/{0}?sort=desc&tag=supplementary-nav%3Bitem%3B6&page={1}".format(console, page)).read()
        else:
            pass
        
        # Get metascores and userscores, convert to ints/floats, then add to original list
        metascores += [int(score) for score in re.findall(r'<span class="data metascore \w+">(\d\d)</span>', source)]
        userscores += [float(score) for score in re.findall(r'<span class="data textscore \w+">(\d\.\d)</span>', source)]
        
        # Show progress
        progress += 1
        print "   * {0} page(s) done, {1} page(s) to go".format(progress, number_of_pages-progress+1)
    
    # Print averages for console and writes them to a file
    averages = (sum(metascores)/len(metascores), sum(userscores)/len(userscores))
    print "\n   Average metascore and userscore for {0}: {1} and {2}".format(console, averages[0], averages[1])
    
    f.write("Console: " + console + '\n\n')
    f.write("   Average metascore: {0}\n".format(averages[0]))
    f.write("   Average userscore: {0}\n\n".format(averages[1]))
    f.write("-------------------------------------------------------\n\n")
    
f.close()