import json
import time
import random

import fb
import requests


class Spammer:
    """
    Spams facebook

    Arguments
    ---------
    :api_key: key to login to facebook with

    :comment_conf: dict of facebook id's to pull posts and send message
            in format: 'fb_id':"comment"

    :share_conf: list of pages to grab posts from and share to your wall
    """

    def __init__(self, own_id: str, api_key: str, comment_conf: dict, share_ids: dict):
        self._own_id = own_id
        self._api_key = api_key
        self._graph = fb.graph.api(api_key)
        self._comment_conf = comment_conf
        self._share_ids = {i:"" for i in share_ids}
        self._request = "https://graph.facebook.com/v2.3/{0._own_id}/home?fields=from&format=json&access_token={0._api_key}".format(
            self)
        self._current_request = self._request
        for i in self._share_ids:
            self._share_ids[i] = "https://graph.facebook.com/v2.3/{0}/posts?format=json&access_token={1._api_key}".format(i, self)

    def do_comments(self, limit=250):
        request = requests.get(
            "{0._current_request}&limit={1}".format(self, limit))
        if not request.status_code == 200:
            raise Exception("Requests didn't get 200 response")
        data = request.json()
        self._current_request = data["paging"]["next"]
        # set next request
        for i in data["data"]:
            user_id = i["from"]["id"]
            if user_id in self._comment_conf:
                print("Commenting on message from: {}, with: {}".format(
                    i["from"]["name"], self._comment_conf[user_id]))
                self._graph.publish(cat="comments", id=i[
                                    "id"], message=self._comment_conf[user_id])

    def do_shares(self):
        for i in self._share_ids:
            link = self._share_ids[i]
            request = requests.get(link)
            print(link)
            if not request.status_code == 200:
                raise Exception("Requests didn't get 200 response, instead got: {}".format(request.status_code))
            data = request.json()
            self._share_ids[i] = data["paging"]["next"]

            for p in data["data"]:
                post = p.get("link")
                if post:
                    self._graph.publish(cat="feed", id=self._own_id, message="wewlad", link=post, caption="memes",
                                        description="ayy lmao")
                    print("Sharing post: {}".format(post))
                    time.sleep(random.randint(3, 9))
            time.sleep(random.randint(4, 7))

if __name__ == "__main__":

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    mySpammer = Spammer(config["self_id"], config["api_key"], config[
                        "comment_conf"], config["share_ids"])

    mySpammer.do_comments()
    mySpammer.do_shares()
