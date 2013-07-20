import urllib2
import json

from BeautifulSoup import BeautifulSoup


def get(url):
    """ Return the contents of the page as a string """
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    output = response.read()
    response.close()

    return output.decode('ascii', 'ignore')
    

def get_podcasts(html):
    """ Return a list of tuples like (name, url, thumbnail)"""
    output = []

    soup = BeautifulSoup(html)
    podcasts = soup.findAll('div', 'episode')
    for podcast in podcasts:
        thumb_section = podcast.find('div', 'podcast-thumb')
        name = thumb_section.find('a', 'autoplay')['data-title']
        slug = thumb_section.find('a', 'autoplay')['data-slug']
        thumb = thumb_section.find('img')['src']
        output.append(
            (name, slug, thumb))

    return output

def get_video_id(content):
    """ Return a dictionary containing video information """
    data = json.loads(content)
    if 'response' in data:
        html = data['response']['html']
        soup = BeautifulSoup(html)
        link = soup.find('a', 'podcast-video-container')
        return {
            'provider': link['data-video-provider'],
            'id': link['data-video-id']}

if __name__ == '__main__':
    html = get("http://podcasts.joerogan.net/podcasts/page/2?load")
    print get_podcasts(html)
    content = get("http://podcasts.joerogan.net/wp-admin/admin-ajax.php?action=loadPermalink&slug=marc-maron")
    print get_video_id(content)
