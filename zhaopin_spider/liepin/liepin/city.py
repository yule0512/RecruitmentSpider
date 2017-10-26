from lxml import etree

def city():
    with open('city.html') as f:
        html = etree.HTML(f.read())
        citylist = html.xpath('//a/@data-code')
        return citylist