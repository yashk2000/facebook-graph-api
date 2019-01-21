import json
import datetime
import csv
import time
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

app_id = ""
app_secret = ""  # DO NOT SHARE WITH ANYONE!
page_id = "431851910256044"

# input date formatted as YYYY-MM-DD
since_date = "2018-01-01"
until_date = "2018-12-31"

access_token = app_id + "|" + app_secret

def request_until_succeed(url):
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()


# Needed to write tricky unicode correctly to csv
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')


def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=posts.limit(10){message}"

    return base_url + fields

def processFacebookPageFeedStatus(status):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_type = status['type']

    status_message = '' if 'message' not in status else \
        unicode_decode(status['message'])
    link_name = '' if 'name' not in status else \
        unicode_decode(status['name'])
    status_link = '' if 'link' not in status else \
        unicode_decode(status['link'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(
        status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
        datetime.timedelta(hours=-5)  # EST
    status_published = status_published.strftime(
        '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

    # Nested items require chaining dictionary keys.


    return (status_id, status_message, link_name, status_type, status_link,
            status_published)

def scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date):
    with open('{}_facebook_statuses.csv'.format(page_id), 'w') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "link_name", "status_type",
                    "status_link", "status_published"])

        has_next_page = True
        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        after = ''# "amfoss.in?fields=posts.limit(10){message}"
        base = "https://graph.facebook.com/v3.2"
        node = "/{}?fields=posts".format(page_id)
        parameters = "/?limit={}&access_token={}".format(100, access_token)
        since = "&since={}".format(since_date) if since_date \
            is not '' else ''
        until = "&until={}".format(until_date) if until_date \
            is not '' else ''

        print("Scraping {} Facebook Page: {}\n".format(page_id, scrape_starttime))

        while has_next_page:
            after = '' if after is '' else "&after={}".format(after)
            base_url = base + node + parameters + after + since + until

            url = getFacebookPageFeedUrl(base_url)
            statuses = json.loads(request_until_succeed(url))

            for status in statuses["posts"]["data"]:
                print(status,"\n")
                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Statuses Processed: {}".format
                          (num_processed, datetime.datetime.now()))

            # if there is no next page, we're done.
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
            else:
                has_next_page = False

        print("\nDone!\n{} Statuses Processed in {}".format(
              num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date)
