# RecruitmentSpider
	scrapy框架爬取智联，拉钩，51job，猎聘中的招聘信息
  	每个网站是有一个单独的爬虫
	
	parse（） 生成第一个请求，为了启动分布式爬虫，先在redis中放一个url触发

	parse起始url请求
	然后写 网站首页的解析
	。。。
	
	
	分别做了分布式配置，将缓存数据临时存储到redis，然后存储到mysql 或则别的数据库
	
	
