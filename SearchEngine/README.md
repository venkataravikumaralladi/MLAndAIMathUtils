# Search Engine
Computer science is about how to design solution for problems. Here we will look at idea on how search engine works.Build a search engine by breaking into small problems. Small problems like <br>
      i.	Find data. This is done by crawling web pages. <br>
      ii.	Build an index. This helps to respond quickly to search queries. <br>
      iii.	Rank pages. This helps to get best results for given query. <br>
 
Text search engine allow people to search a large set of documents for a list of words, and which rank results according to how relevant the documents are to those words. We will look in to idea of "Page Rank" algorithm used by Google which is a revolutionary algorithm in search engine category.

Before Google page rank algorithm:  Before google old search engines did not work well because websites are not polite, they tried to manipulate content to gain rank. For example website mentioned 'resaturant' 32 times in text so they go to top of rank if searched by restaturant keyword thn website which mentioned 'restaurant' 2 times. To avoid this google came up with algorithm which gives rank based on external links rather than content of webpage. <br>

High level over view of search engine design.

![image](https://user-images.githubusercontent.com/10434795/142728176-e4ec2251-4407-4b53-bb57-6ac05c78f473.png)


### Webcrawler (class WebCrawler in text_search_engine.py)

For our web crawler, the important thing is to find the links to other web pages in the page. We will start with 'seed' passed as argument by user to start with. We can find those  links by looking for the anchor tags that match this structure: ` <a href="<url>">`. To build our crawler, for each web page we want to find all the link target URLs on the page. We want to keep track of them and follow them to find more content on the web.

### Index building (text_search_engine.py)

We will build content index by parsing web page content and maintain a dictionary with key word as content and value has list of url's that particular content is present. Index is maintained as hash table for fast retrival and storing.

### Page Ranking algorithm (text_search_engine.py)
Google page rank algorithm is based on random surfer model. Random surfer who starts at a random page and then follows the links at random. The popularity of page is the probability that the random surfer reaches a particular page. Page rank algorithm has to handle following while calculating page rank for a url page. <br>
       1. Number of outlinks for given page. <br>
       2. Number of inlinks for a given page. <br>
       3. Quality of inlinks for a page (i.e, ieee website pointing to your article has most weightage) <br>
       4. New webpage has no links <br>
       5. We want our algorithm to handle typing of webaddress rather then following links. (damping factor) <br>
       6. We want to keep ranks in reasonable range for example in `[0,1)` so we start with rank of 1/N for each url page where N is number of pages in our corpus. <br>
       
 #### Refernces
 Reference: Udacity cs101: Introduction to Computer Science
 
