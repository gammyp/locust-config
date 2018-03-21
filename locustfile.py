from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup

def fetch_static_assets(session, response):
        resource_urls = set()
        soup = BeautifulSoup(response.text, "html.parser")
        for res in soup.find_all(src=True):
            url = res['src']
            if is_static_file(url):
                resource_urls.add(url)
            else:
                print("Skipping: ") + url
        for url in set(resource_urls):
                session.client.get(url, name="Static File")
                print ("Regular: ") + url

class LoadTask(TaskSet):
    @task
    def index(self):
        response = self.client.get("/")
        fetch_static_assets(self, response)
    
    def is_static_file(f):
        if "/static/" in f:
            return True
        else:
            return False
        
class MyLocust(HttpLocust):
    task_set = LoadTask
    min_wait = 5000
    max_wait = 15000
	
