from scrapy.item import Item, Field

class filmexclueItem(Item):

    url = Field()
    title = Field()
    link = Field()
    desc = Field()
    imgurl = Field()

    pass
