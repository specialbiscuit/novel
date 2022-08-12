import scrapy
from scrapy.selector import Selector

class BookSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['m.xbiquge.so']
    start_urls = ['https://m.xbiquge.so/list/1_1.html']

    def parse(self, response):
        response_body = response.body.decode(response.encoding)
        print("书本列表")
        table_html_list = Selector(text=response_body).xpath("//table[1]").getall()
        if table_html_list:
            for table in table_html_list:
                print("---------------------start---------------------")
                _, _, _, bookId = self.parseBook(table)
                book_chapter_url = "https://m.xbiquge.so/chapters_" + bookId + "/"
                print("书本章节列表跳转地址:" + book_chapter_url)
                print("---------------------end---------------------")
                yield scrapy.Request(url=book_chapter_url, callback=self.parseChapter)

                # TODO 书本列表分页

        else:
            print("列表为空")

        pass

    def parseBook(self, table):
        bookThumb = Selector(text=table).xpath("//img/@src").get()
        print("缩略图:" + bookThumb)
        title = Selector(text=table).css("a:nth-child(1)::text").get()
        print("标题:" + title)
        author = Selector(text=table).css(".mr15::text").get()
        print("作者:" + author[3:])
        bookJumpUrl = Selector(text=table).css("a:nth-child(1)").xpath("@href").get()
        bookId = bookJumpUrl[26:len(bookJumpUrl)-1]
        print("书本ID:" + bookId)
        return bookThumb, title, author, bookId

    def parseChapter(self, response):
        responseBody = response.body.decode(response.encoding)
        # TODO get -> getall
        chapterHtmlList = Selector(text=responseBody).css('li:not(.title)').getall()
        print(chapterHtmlList)
        for chapterHtml in chapterHtmlList:
            print(chapterHtml)
            chapterTitle = Selector(text=chapterHtml).css('a::text').get()
            print("章节标题:" + chapterTitle)
            contentUrl = Selector(text=chapterHtml).css('a').xpath("@href").get()
            print("内容地址:" + contentUrl)
            yield scrapy.Request(url=contentUrl, callback=self.parseChapterContent)

            # TODO 章节分页

    def parseChapterContent(self, response, page = 1, chapterContent = ''):
        responseBody = response.body.decode(response.encoding)
        nextTitle = Selector(text=responseBody).css('#pb_next::text').get()
        content = Selector(text=responseBody, type='html').css('#nr1').get()
        chapterContent = chapterContent + content
        if nextTitle == '下一页':
            page = page + 1
            contentUrlSuffix = "_" + str(page) + ".html"
            contentUrlPrefix = response.url[:len(response.url) - 5]  # 内容地址前半部分
            completeContentUrl = contentUrlPrefix + contentUrlSuffix
            # print("nextPage:" + completeContentUrl)
            yield scrapy.Request(url=completeContentUrl, callback=self.parseChapterContent, cb_kwargs=dict(page = page, chapterContent = chapterContent))

        print("该章节最终内容:" + chapterContent)




