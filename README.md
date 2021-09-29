# crawl-chiasenhac
Crawl top-20 songs from website chiasenhac.vn with specify topic name (example: us-uk, nhạc nhật, nhạc hoa, ...)
# Installation
Dependencies
```
pip install -r requirements.txt
```
Splash server
```
docker pull scrapinghub/splash
```
# Usage
Start docker
```
docker run -it -p 8050 --rm scrapinghub/splash
```
Move to project folder (where scrapy.cfg stand)
```
scrapy crawl songs -a name='topic_name'
```
