# Scrapy settings for filmexclue project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'filmexclue'

SPIDER_MODULES = ['filmexclue.spiders']
NEWSPIDER_MODULE = 'filmexclue.spiders'

ITEM_PIPELINES = {
    'filmexclue.pipelines.JsonWriterPipeline': 800,
    'filmexclue.pipelines.FilmexcluePipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'filmexclue (+http://www.yourdomain.com)'
