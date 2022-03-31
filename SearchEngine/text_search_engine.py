"""
File Created: 19th October 2021
Author: Venkata Ravi K A
Reference: http://www.cs.virginia.edu/~evans/cs101/
           
           
My Notes:
    For search engine we should have data. Data is created by crawling web.
    
    Step1: Data creation: (done by WebCrawler)
            Web crawler should work to find all the links that can be found from a seed
            page. We need to start by finding all the links on the seed page, we store
            them in a list so we can use them to keep going. 
            We will go through all the links in that list to continue our crawl, and 
            keep going as long as there are more pages to crawl.
            
            The web crawler is meant to be able to find links on a seed page, make them
            into a list and then follow those links to new pages where there
            may be more links, which we want your web crawler to follow.
            
    Step2: Create a index for fast searching. This is done using dictionary (hash function).
           Index is maintained as hash table, which can respond to a query in a time
           that does not increase even if the size of index increases.
    
    

"""

from dummy_web_cache import cache

def get_test_page1(url):
    if url in cache:
        return cache[url]
    return ""


from typing import Tuple


class WebCrawler:  
    ''' 
    Class WebCrawler provides functionality in creating data for search
    engine by crawling pages from seed page provided.
    '''
    def __init__(self, seed_page : str) -> None:
        ''' 
        Constructor for webcrawler class
        
            Parameters
            ----------
            seed_page : str
                starting page from where we parse links and create data for search engine.

            Returns
            -------
            None
        '''
        # configurable parameters
        # damping factor to consider random surfer typing a link on IE or chrome instead
        #  of following hyper linkss. 80% of time surfer clicks links and 20% time types link on broswer.
        self.damping_factor = 0.8
        self.number_of_iterations = 10
        
        # member variables.
        self.seed_page    = seed_page
        self.crawled_lst  = []
        self.to_crawl_lst = [seed_page]
        # index is maintained as hash table, which can respond to a query in a time
        # that does not increase even if the index increases.
        self.index        = {}
        # graph is to maintain out links for each url.
        self.graph        = {}
        # rank dictionary
        self.page_ranks   = {}
        
        # create content index, graph and rank dictionary
        self._crawl_web()
        self._compute_vrk_rank()
        return
     
    def _get_next_target(self, page : str) -> Tuple[str, int]:
        '''
            Private function for internal purpose. This function returns the
            first observed target link from page provided in argument. Function
            is used during web crawling while parsing html web page for links.
        Parameters
        ----------
            page : str
                content page to search for first target link (i.e., hyper link)

        Returns
        -------
            tuple (str, int)
                tuple of url of first target link if found else None and
                position of link in page provided if found else -1..

        '''
         
        start_link_pos = page.find('<a href=')
        if start_link_pos == -1:
            return (None, 0)
         
        start_quote_pos = page.find('"', start_link_pos)
        end_quote_pos = page.find('"', start_quote_pos+1)
        url =  page[start_quote_pos+1:end_quote_pos]
        return (url, end_quote_pos)
     
    def _get_all_links(self, page : str) ->list:
        '''
            Private function for internal purpose. This function gets all hyper 
            links from provided htmlpage and add links to to_crawl list if link is
            not crawled.            

        Parameters
        ----------
            page : str
                content page to search for first target link (i.e., hyper link).

        Returns
        -------
            list of hyper links contained in page.

        '''
        content_page_from_end_pos = page
        
        links = []
        while True:
            url, end_pos = self._get_next_target(content_page_from_end_pos)
            if url:
                links.append(url)
                content_page_from_end_pos = content_page_from_end_pos[end_pos:]
            else:
                break
        
        return links
    
    
     
    def _update_to_crawl_lst(self, links : list):
        '''
            Private function for internal purpose. This function updates to_crawl
            list from provided links list.
            
        Parameters
        ----------
            links : list
                scan links list if links to be scanned, if not scanned link is 
                added to self.to_crawl list.

        Returns
        -------
            None.

        '''
        if links :
            for item in links:
                if item not in self.to_crawl_lst:
                    self.to_crawl_lst.append(item)
        return
    
    def _add_to_index(self, keyword : str, url : str):
        '''
            This is a private function used as helper for creating index of search engine.
            Index is maintained as hash table using dictionary.
                { key1: <list of urls>, key2: <list of urls>, ...}
            example: {'<html>': ['http://www.udacity.com/cs101x/index.html',
                                 'http://www.udacity.com/cs101x/flying.html',
                                 'http://www.udacity.com/cs101x/walking.html',
                                 'http://www.udacity.com/cs101x/crawling.html'],
                      '<body>': ['http://www.udacity.com/cs101x/index.html',
                                 'http://www.udacity.com/cs101x/walking.html',
                                 'http://www.udacity.com/cs101x/crawling.html'],
                      'This': ['http://www.udacity.com/cs101x/index.html']
                    }
        Parameters
        ----------
            keyword : str
                keyword. If keyword already exists in index table, url is added to list
                         corresponding to that keyword. 
                         else if keyword does not exits new entry for keyword is created 
                         in index table and url is added to list for this new entry.
            url : str
                url link for corresponding keyword to be added to index.

        Returns
        -------
            None.

        '''
        if keyword in self.index:
            self.index[keyword].append(url)
        else:
            self.index[keyword] = [url]
        return
        
    def _add_page_to_index(self, url : str, content : str):
        '''
            This is a private function used as helper for creating index of search engine.
            This function reads the contents of the page and creates index using helper
            function _add_to_index. 
            The order in which the pages appear in the list of URL’s for corresponding keyword
            is the order the pages were crawled
        Parameters
        ----------
            url : str
                url link for corresponding content passed as argument.
            content : str
                content of corresponding url link passed as argument.

        Returns
        -------
            None.

        '''
        words = content.split()
        for word in words:
            self._add_to_index(word, url)
        return
     
    def _crawl_web(self)->list:
        '''
        Function crawls or spidering a web from seed provided in constructor.
        Seed link is added to self.to_crawl_list in constructor.
        Performs following actionss:
                1. Creates hash table with keyword as index and item as list of url's 
                   present for that keyword.
                2. Creates Graph i.e., consits of number of outlinks for this page.
                   This created graph is used in ranking algorithm. 
        

        Returns
        -------
        list of crawled url's'

        '''
        
        while self.to_crawl_lst:
            page = self.to_crawl_lst.pop()
            
            if page not in self.crawled_lst:
                # IMPORTANT: change her to use right get function for url page.
                content = get_test_page1(page)       
                self._add_page_to_index(page, content)
                out_links = self._get_all_links(content)
                self._update_to_crawl_lst(out_links)
                # create graph. Used for calculating rank while displaying result.
                self.graph[page] = out_links
                self.crawled_lst.append(page)
                if(len(self.crawled_lst) > 100):
                    break
             
        return self.crawled_lst
    
    def _compute_vrk_rank(self) -> dict:
        '''
        The problem of deciding how to rank the pages leads to the question
        of how to decide popularity
        
        Compute page ranks for pages present in graph (self.graph) created
        while web crawling.
        
        Reference: youtube channel link:
                https://www.youtube.com/watch?v=9nkR2LLPiYo&list=PLAwxTw4SYaPmjFQ2w9j05WDX8Jtg5RXWW
                videos: from 418 onwards.

        Returns
        -------
        dictionary page rank for each webpage present in graph.
        {
            'http://udacity.com/cs101x/urank/index.html': 0.033333333333333326, 
            'http://udacity.com/cs101x/urank/zinc.html': 0.038666666666666655,
            'http://udacity.com/cs101x/urank/nickel.html': 0.09743999999999997,
            'http://udacity.com/cs101x/urank/kathleen.html': 0.11661866666666663,
            'http://udacity.com/cs101x/urank/arsenic.html': 0.05413333333333332,
            'http://udacity.com/cs101x/urank/hummus.html': 0.038666666666666655
        }

        '''
        npages = len(self.graph)
        # base case. Initialize page rank for each webpage i.e., probability of 
        # reaching that page by random surfer.
        for page in self.graph:
            self.page_ranks[page] = 1.0 / npages
        
        # recursive case
        for i in range(0, self.number_of_iterations):
            # ranks at time stamp t. ranks dictionary contains rank at time stamp (t-1)
            newranks = {} 
            # graph structure looks like below
            # {
            #   'url1': ['outgoing link 1, outgoing link 2, ...],
            #   'url2': ['outgoing link 1, outgoing link 2, ...],
            #   ...
            # }
            for page in self.graph:
                newrank = (1 - self.damping_factor) / npages
                # compue reachable probability through clicking.
                for node in self.graph:
                    # check if page is pointed by node, i.e., inlinks
                    if page in self.graph[node]:
                        newrank = newrank + self.damping_factor * (self.page_ranks[node]/(len(self.graph[node])))
                # assign new rank for current page for time t
                newranks[page] = newrank
            self.page_ranks = newranks
        return self.page_ranks
    
   # Following are PUBLIC functions.
    
    def get_created_search_index(self) ->list:
        '''
              Returns created index for search engine. This function should be
              called after calling crawl_web

        Returns
        -------
        list of indexes in format
            keyword : str
                keyword.
            url : str
                url link for corresponding keyword to be added to index.

        '''
        return self.index
    
    def get_url_ranks(self)->dict:
        '''
        Used by search engine to get url ranks.

        Returns
        -------
        dict
            returns page ranks for urls crawled by crawler.

        '''
        return self.page_ranks
    
    def get_content_index(self)->dict:
        '''
        Used by search engine to get content index.

        Returns
        -------
        dict
            returns content index of cralwer.

        '''
        return self.index
    
    
class MySeachEngine:
    
    def __init__(self, seed:str):
        # prepare index and ranking for searching
        webcrawler = WebCrawler(seed)
        self.index = webcrawler.get_content_index()
        self.ranks = webcrawler.get_url_ranks()
        return
    
    def lucky_search(self, keyword : str) ->str:
        '''
        Lucky search returns website with best rank value for given keyword

        Parameters
        ----------
        keyword : str
            keyword to be searched.

        Returns
        -------
        str
            best rank website for given keyword.

        '''
        result_pages  = self.lookup(keyword)
        if not result_pages:
            return None
        best_page = result_pages[0]
        for page in result_pages:
            if self.ranks[page] > self.ranks[best_page]:
                best_page = page
        return best_page
        
    def ordered_search(self, keyword:str)->list:
        # TODO: return multiple url's in the order of rank
        return
    
    
    def lookup(self, keyword : str) -> list:
        '''
        Returns the links for keyword   

        Parameters
        ----------
        keyword : str
            keyword to search for.

        Returns
        -------
        list of websites of keyword.

        '''
        if keyword in self.index:
            return self.index[keyword]
        else:
            return None
        
        
     
            

if __name__ == '__main__':
    search_engine = MySeachEngine("http://udacity.com/cs101x/urank/index.html")
    print('[TEST CASE1] best rank url for keyword Hummus',
                     search_engine.lucky_search('Hummus'))
    print('[TEST CASE1] best rank url for keyword the',
                     search_engine.lucky_search('the'))
    print('[TEST CASE1] best rank url for keyword babaganoush',
                     search_engine.lucky_search('babaganoush'))
    
    print(search_engine.ordered_search('Hummus'))
    
     
