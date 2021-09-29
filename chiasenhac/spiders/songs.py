from os import error
import logging
import scrapy
from scrapy_splash import SplashRequest
from chiasenhac.items import ChiasenhacItem



class SongsSpider(scrapy.Spider):
    name = 'songs'
    allowed_domains = ['chiasenhac.vn']
    
    script_login = '''
    function main(splash, args)
        splash.private_mode_enable = false 
        --splash:init_cookies(splash.args.cookies)
        
        assert(splash:go(args.url))
        assert(splash:wait(0.5))

        login_btn = splash:select('#header > div > div > div > ul > li:nth-child(1) > a')
        login_btn.click()
        assert(splash:wait(1))
        
        email_input = splash:select('#form-login > div:nth-child(1) > div > input.email')
        email_input:focus()
        email_input:send_text('hoangnd997')
        assert(splash:wait(0.5))

        password_input = splash:select('#form-login > div:nth-child(1) > div > input.password')
        password_input:focus()
        password_input:send_text('hoangndnd1805111')
        assert(splash:wait(0.5))

        login1_btn = splash:select('#form-login > div:nth-child(1) > div > div > button')
        login1_btn.click()
        assert(splash:wait(2))

        splash:set_viewport_full()
        return {
            html = splash:html(),
            cookies = splash:get_cookies()
        }
    end 
    '''
    script_render = '''
    function main(splash, args)
        splash.private_mode_enable = false 

        splash:init_cookies(splash.args.cookies)

        assert(splash:go(args.url))
        assert(splash:wait(5))

        splash:set_viewport_full()
        return splash:html()
    end
    '''

    def start_requests(self):
        yield SplashRequest(
            url= 'https://chiasenhac.vn/nhac-hot.html',
            endpoint='execute',
            args={
                'lua_source': self.script_login
            },
            callback=self.parse
        )

    def parse(self, response):
        ## Check if this web-site is logged in
        # if response.xpath('//a[contains(@href, "https://chiasenhac.vn/logout?back")]'):
        #     logging.warning('logged in')
        # else:
        #     logging.warning('failed')
        # print(response.data['cookies'])

        # Get cookies from response to keep login
        cookies = response.data['cookies']

        # Create a list of availble music list
        music_lists = {}
        for list in response.xpath('//ul[@id="myTab"]/li/a'):
            name = list.xpath('.//text()').get()
            id = list.xpath('.//@aria-controls').get()
            music_lists[name.lower()] = id

        # Find if target list is availble
        target_list_name = self.list_name.lower()
        target_list_id = music_lists.get(target_list_name)
        if not(target_list_id):
            logging.warning('Your list_name is not availble!!!')
            return None

        # Crape each song in music list
        songs = response.xpath(f"//*[@id='{target_list_id}-music']/ul/li/div[3]/div/h5/a/@href").getall()
        for song in songs:
            url = response.urljoin(song)
            yield SplashRequest(url = url, 
                                callback=self.song_parse, 
                                endpoint='execute',args={
                                    'lua_source': self.script_render
                                }, 
                                meta={
                                    'cookies': cookies,
                                    'list_name': target_list_name
                                })

    def song_parse(self, response):       
        song_name = response.xpath("//h2[@class = 'card-title']/text()").get()
        singer = response.xpath("//div[@class = 'card card-details']/div[2]/ul/li[1]/a/text()").get()
        urls = response.xpath("//a[@class = 'download_item']")

        try:
            url = urls[-2]
        except IndexError:
            logging.warning('out of range')
            url = urls[-1]
        except TypeError:
            logging.warning('Type error')
            url = urls
        song_quality = url.xpath(".//span/text()").getall()
        song_url = url.xpath(".//@href").getall()
        
        file_name = f"{song_name}-{singer}-{song_quality}"
        file_name = file_name.strip()
        # loader = ItemLoader(ChiasenhacItem)
        # loader.add_value('file_name', file_name)
        # loader.add_value('file_urls', song_url)
        # yield loader.load_item()

        yield {
            'folder_name': response.meta['list_name'],
            'file_name': file_name,
            'file_urls': song_url
        }
