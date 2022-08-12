import scrapy
from scrapy.selector import Selector


class Example1Spider(scrapy.Spider):
    name = 'example1'
    allowed_domains = ['m.xbiquge.so']
    start_urls = ['https://m.xbiquge.so/chapters_4772/1']

    def parse(self, response, page = 1):
        urlSplitList = response.url.split('/')
        print(urlSplitList)
        urlSplitList[4] = 2
        aaa = urlSplitList.join('//')
        print(aaa)
        # print(response.url.split('/'))
        print("-------------------------")
        responseBody = response.body.decode(response.encoding)
        print(responseBody)
        print("-------------------------")
        nextChapterPageHtml = Selector(text=responseBody).css(".page-book").get()
        if (self._checkExistNextPage(nextChapterPageHtml)):
            page = page +1
            nextChapterUrl = response.url + str(page)
            yield scrapy.Request(url=nextChapterUrl, callback=self.parse, cb_kwargs=dict(page=page))

        # print("章节尾部text信息:")
        # print(nextChapterPageHtml)
        pass

    def _checkExistNextPage(self, string):
        isExistNextPage = string.find("下一页")
        return isExistNextPage != -1

