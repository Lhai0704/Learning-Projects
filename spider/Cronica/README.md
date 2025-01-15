
Cronica.py: 给定关键词和页数，输出csv文件，第一列为title，第二列为url
使用的是网站自带的搜索功能，所以得到的结果中有很多是标题里面没有关键词，只是正文里面有关键词，这些数据需要用只要标题+去重.py筛选掉
然后用spiderBasedUrl.py获取正文和日期数据。
最后用getCategory.py从url中获取分类信息。