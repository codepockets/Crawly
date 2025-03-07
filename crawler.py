#Web Crawler

#small revision on kachilous code (for fun!)




import urllib2
import re
from BeautifulSoup import BeautifulSoup
from collections import deque

depth, i = 0


#this function will check to see if a link is valid
def validate(n):
	try:
		currenturl = urllib2.urlopen(n) 
		return 1
	except urllib2.URLError:
		return 0
		
def visited_test(n):
	for x in visited:
		if n == x:
			break
			return 0
	return 1
	
def unvisited_test(n):
	for y in unvisited:
		if n == y:
			break
			return 0
	return 1

url_seed = raw_input("Please enter a url seed: ");
string = raw_input("Please enter search string: ");
max_depth = int(raw_input("Please enter the max depth to crawl to: ")); #raw_input returns a string, but you need an int.
	
#create visited and unvisited lists as well as a temp list to hold unvisited links during iteration
unvisited = deque([])
visited = deque([])
temp = []

#append the url seed to the unvisited list
unvisited.append(url_seed)

currenturl = unvisited.popleft()

while(unvisited != [] or depth <= max_depth):
	try:
		#open the url for parsing
		url = urllib2.urlopen(currenturl) 
		
		#create BeautifulSoup object
		soup = BeautifulSoup(url) 
		
		#this will see if string is on current html page
		#regexp is looking for an occurrence of string not the exact match to the NavigableString string
		find_string = soup.body.find(text=re.compile(string))
		#find_string = soup.body.findAll(text=re.compile(string), limit=1) 
		
		#if the keyword is found, print that the string is not on the currenturl
		if find_string == []: 
	            print string, "was not found on the page: ", currenturl 
		#otherwise, print that the keyword was not foudn on the currenturl
		else: 
    		    print string, "was found on the page: ", currenturl
		
		#Find all links in anchor tags and extract only the links
		links =  soup.findAll('a', href = re.compile("http://")) 
		
		print len(links)
						
		#this should only happen once, since unvisited list won't be populated with links in the first iteration
		if(unvisited == deque([]) and visited == deque([])):
		    for link in links:
			if validate(link['href']) == 1:
		  	    unvisited.append(link['href'])
					
		#Loop through all links and check to see if link is valid and not in visited or unvisited list -> if so then add link to a temporary list [threshold is 50]
		else:
		    for link in links:
			if validate(link['href']) == 1 and visited_test(link['href']) == 1 and unvisited_test(link['href']) == 1 and len(temp) < 10:
			    temp.append(link['href'])
					
			
		
		
		
			#extend unvisited list with all of the links accumulated in current iteration
		            unvisited.extend(temp)
			
			#free memory in temp list
			    del temp[:]
			
			#each time temp list is filled with 10 new links, a new depth has been reached
		            depth += 1
		            print "current depth is ", depth
			
		#move current url to visited list
		            visited.append(currenturl)
		
		            currenturl = unvisited.popleft()
		            print currenturl

	except ValueError, urllib2.URLError:
		if unvisited != deque([]):
		    currenturl = unvisited.popleft()
		else:
		    print "Oops! ", currenturl, "is not a valid url and there are no more links to parse."
		    break