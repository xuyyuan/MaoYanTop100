spider和spider都可以运行
两者对image元素的提取有问题，具体看正则表达式部分：
    +r'.*?src.*?">.*?src="(.*?)"'
    +r'.*?poster-default.*?">.*?src="(.*?)"'