# _*_coding:utf-8_*_
# version : 3.5

# P 72

import urllib.request
import json
import datetime
import BaseCollector
from collections import OrderedDict

facebook_app_id = '238829726646010'
facebook_app_secret = 'c79a4b220896c1d784cecdd92cd8f229'


class FaceBookCollector(BaseCollector.BaseCollector):




    def __init__(self):
        pass

    def get_request_url(self, url):
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                print("[%s] Url Request Success" % datetime.datetime.now())
                return response.read().decode('utf-8')

        except Exception as e:
            print(e)
            print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
            return None


    def getFacebookNumbericID(self, page_id, access_token):
        base = "https://graph.facebook.com/v2.8"
        node = "/" + page_id
        parameters = "/?access_token=%s" % access_token
        url = base + node + parameters

        ret_data = self.get_request_url(url)

        if ret_data is None:
            return None
        else:
            jsonData = json.loads(ret_data)
            return jsonData['id']

    def getFacebookPost(self, page_id, access_token, from_date, to_date, num_statuses):
        base = "https://graph.facebook.com/v2.8"
        node = "/%s/posts" % page_id
        fields = "/?fields=id,message,link,name,type,shared,reactions," + \
            "created_time,comments.limit(0).summary(true)" + \
            ".limit(0).summary(true)"
        duration = "&since=%s&access_token=%s" % (from_date, to_date)
        parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
        url = base + node + fields + duration + parameters

        retData = self.get_request_url(url)

        if retData == None:
            return None
        else:
            return json.loads(retData)

    def getPostItem(self, post, key):
        try:
            if key in post.keys():
                return post[key]
            else:
                return ''
        except:
            return ''

    def getPostTotalCount(self, post,key):
        try:
            if key in post.keys():
                return post[key]['summary']['total_count']
            else:
                return 0
        except:
            return 0

    def getPostData(self, post, access_token, jsonResult):
        post_id = self.getPostItem(post,'id')
        post_message = self.getPostItem(post, 'message')
        post_name = self.getPostItem(post, 'name')
        post_link = self.getPostItem(post, 'link')
        post_type = self.getPostItem(post, 'type')

        post_num_reactions = self.getPostTotalCount(post, 'reactions')
        post_num_comment = self.getPostTotalCount(post, 'created_time')
        post_num_shares = 0 if 'shares' not in post.keys() else post['shares']['count']

        post_created_time = self.getPostItem(post, 'created_time')

        post_created_time = datetime.datetime.strptime(post_created_time, '%Y-%m-%dT%H:%M:%S+0000')
        post_created_time += datetime.timedelta(hours =+ 9)
        post_created_time = post_created_time.strftime('%Y-%m-%d %H:%M:%S')

        reaction = self.getFacebookReaction(post_id, access_token) if post_created_time > '2016-02-24 00:00:00' else{}
        post_num_likes = self.getPostTotalCount(reaction, 'like')
        post_num_likes = post_num_reactions if post_created_time < '2016-02-24 00:00:00' else post_num_likes


        post_num_loves = self.getPostTotalCount(reaction, 'love')
        post_num_wows = self.getPostTotalCount(reaction,'wow')
        post_num_hahas = self.getPostTotalCount(reaction,'haha')
        post_num_sads = self.getPostTotalCount(reaction, 'sad')
        post_num_angrys = self.getPostTotalCount(reaction,'angry')

        jsonResult.append({'post_id':post_id, 'message':post_message,
                           'name': post_name, 'link':post_link,
                           'created_time': post_num_comment, 'num_shares':post_num_shares,
                           'num_likes': post_num_likes, 'num_loves':post_num_loves,
                           'num_wows': post_num_wows, 'num_hahas':post_num_hahas,
                           'num_sads': post_num_sads, 'num_angrys':post_num_angrys})


    def getFacebookReaction(self, post_id, access_token):
        base = "https://graph.facebook.com/v2.8"
        node = "/%s" % post_id
        reactions = '/?fields='\
                    'reactions.type(LIKE).limit(0).summary(total_count).as(like)'\
                    ',reactions.type(LOVE).limit(0).summary(total_count).as(love)'\
                    ',reactions.type(WOW).limit(0).summary(total_count).as(wow)' \
                    ',reactions.type(HAHA).limit(0).summary(total_count).as(haha)' \
                    ',reactions.type(SAD).limit(0).summary(total_count).as(sad)' \
                    ',reactions.type(ANGRY).limit(0).summary(total_count).as(angry)'
        parameters = '&access_token=%s' % access_token
        url = base + node + reactions + parameters

        ret_data = self.get_request_url(url)

        if ret_data is None:
            return None
        else:
            return json.loads(ret_data)


def main():
    facebook_coll = FaceBookCollector()

    page_name = 'jtbcnews'
    access_token = facebook_app_id + "|" + facebook_app_secret

    from_date = '2017-09-21'
    to_date = '2017-09-21'

    num_statuses = 10
    go_next = True
    json_result = []

    page_id = facebook_coll.getFacebookNumbericID(page_name, access_token)

    if page_id is None:
        print('[%s] %s is Invaild Page Name' % (datetime.datetime.now(), page_name))
        exit()

    print('[%s] %s page id is %s' % (datetime.datetime.now(), page_name, page_id))

    json_post = facebook_coll.getFacebookPost(page_id, access_token, from_date, to_date, num_statuses)

    i = 0

    if json_post is None:
        print("No DATA")
        exit()

    while go_next:
        print(json_post)

        for post in json_post['data']:
            i += 1
            #print(post)
            facebook_coll.getPostData(post, access_token, json_result)

        if 'paging' in json_post.keys():
            if ('next' in json_post['paging']):
                l = json_post['paging']['next']
                json_post = json.loads(facebook_coll.get_request_url(l))
            else:
                go_next = False
        else:
            go_next = False

    with open('%s_facebook_%s_%s.json' % (page_name, from_date, to_date), 'w', encoding='utf8') as outfile:
        str_ = json.dumps(json_result,
                          indent=4, sort_keys=True,
                          ensure_ascii=False)

        outfile.write(str_)

    print('%s_facebook_%s_%s.json SAVED' % (page_name, from_date, to_date))

if __name__ == '__main__':
    main()
