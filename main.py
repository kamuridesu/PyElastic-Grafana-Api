from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError
from elasticsearch.helpers import bulk
from datetime import datetime
import time
from datetime import datetime


class GitlabAnalElastic:
    def __init__(self, host: str):
        self.elclient = Elasticsearch(host)
        self.init()

    def init(self):
        while True:
            if self.elclient.ping():
                break
            else:
                print("Waiting for Elasticsearch to start...")
                time.sleep(5)
        print("Elasticsearch is up!")

    def put_content(self, index: str, id: str, content: dict):
        resp = self.elclient.index(index=index, id=id, body=content)
        return (resp['result'] == "created")

    def add_content(self, index: str, content: dict):
        if not "timestamp" in content:
            content["timestamp"] = datetime.now()
        # get last id
        id = 1
        try:
            resp = self.elclient.search(index=index, body={
                "query": {
                    "match_all": {}
                }
            })
            id = int(resp['hits']['hits'][-1]["_id"]) + 1
        except (NotFoundError, IndexError):
            pass
        resp = self.elclient.index(index=index, id=id, body=content)

    def put_content_bulk(self, index: str, content: list):
        resp = bulk(self.elclient, content)
        return (resp['errors'] == False)

    def get_content(self, index: str, id: str):
        resp = self.elclient.get(index=index, id=id)
        return resp['_source']

    def get_content_all(self, index: str):
        resp = self.elclient.search(index=index)
        return resp['hits']['hits']

    def get_content_all_ids(self, index: str):
        resp = self.elclient.search(index=index)
        return [hit['_id'] for hit in resp['hits']['hits']]

    def get_content_all_ids_by_author(self, index: str, author: str):
        resp = self.elclient.search(index=index, body={
            "query": {
                "match": {
                    "author": author
                }
            }
        })
        return [hit['_id'] for hit in resp['hits']['hits']]

    def get_content_all_by_author(self, index: str, author: str):
        resp = self.elclient.search(index=index, body={
            "query": {
                "match": {
                    "author": author
                }
            }
        })
        return resp['hits']['hits']

    def get_content_by_index(self, index: str):
        resp = self.elclient.search(index=index)
        return resp['hits']['hits']

    def delete_content(self, index: str, id: str):
        try:
            resp = self.elclient.delete(index=index, id=id)
            return (resp['result'] == "deleted")
        except NotFoundError:
            return {"error": "Not found"}
