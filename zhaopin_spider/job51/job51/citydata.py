from lxml import etree
def citydata():
    with open('city.html','r') as f:
        html = etree.HTML(f.read())
        data = html.xpath('//em[@data-value]/@data-value')
        return data