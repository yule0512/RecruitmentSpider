from lxml import etree

def industries():
    indusIdList = []
    with open('industries.html') as f:
        html = etree.HTML(f.read())
        datalist = html.xpath('//a/@href')
        for data in datalist:
            datas = data.split('&')
            for d in datas:
              if 'industries' in d:
                  indusIdList.append(d.split('=')[1])
        return indusIdList