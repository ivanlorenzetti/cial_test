import os
import re
import scrapy
from urllib.parse import urlparse
from cial_test.items import CialTestItem


class CialTestSpider(scrapy.Spider):
	name = 'cialtest'

	def __init__(self, start_urls=[], **kwargs):
		self.start_urls = start_urls
		super().__init__(**kwargs)

	
	def clean_url(self, url):
		url = url.replace("['", "")
		url = url.replace("']", "")
		url = url.lower()
		return url
	
	def phone_cleaning(self, phone):
		filtered_str = ''
		allowed_chars = ['0','1','2','3','4','5','6','7','8','9','(',')','+']
		for char in phone:
			if char in allowed_chars:
				filtered_str += char
			else:
				filtered_str += ''

		return filtered_str
	

	def parse_phone(self, response):

		html_text = str(response.text)
		
		phone_regex = re.compile(r"(^\d{3}[-\.\s]\d{3}[-\.\s]\d{4}" + 
                r"|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}" + 
                r"|^\d{3}[-\.\s]\d{4}[-\.\s]\d{4,5}" + 
                r"|^\d{3}[-\.\s]\d{4,7}" + 
                r"|\d{2}[-\.\s]\d{5}[-\.\s]\d{4}" +
                r"|\(\d{2}\)\d{5}[-\.\s]\d{4}" +
                r"|\+\d{1,3}[-\.\s]\(\d{3}\)[-\.\s]\d{3}[-\.\s]\d{2,3}[-\.\s]\d{2,3}" +
                r"|\+\d{2,3}[-\.\s]\(?\d{2,3}\)?[-\.\s]\d{4,5}[-\.\s]\d{4}" + 
                r"|\+\d{1,2}[-\.\s]\(?\d{2,3}\)[-\.\s]\d{3}[-\.\s]\d{4}" +
                r"|^\d{1}[-\.\s]\d{4}[-\.\s]\d{4}" + 
                r"|\+\d{1,2}[-\.\s]\d{1}[-\.\s]\d{4}[-\.\s]\d{4}" +
                r"|\d{4}[ ]\d{6}|^\d{4}[-\.\s]\d{3}[-\.\s]\d{3}" +
                r"|\(\d{2,3}\)[-\.\s]\d{4,5}[-\.\s]\d{4,5}" +
                r"|^\+\d{2,3}[-\.\s]\d{2,3}[-\.\s]\d{2,3}[-\.\s]\d{2,5}" +
                r"|\(\d{3}\)[-\.\s][-\.\s\/]?[-\.\s]\d{3}[-\.\s]\d{5}" +
                r"|\d{2,3}[-\.\s]\d{4}[-\.\s]\d{4}" +
                r"|\d{4}[-\.\s]\d{3}[-\.\s]\d{3}" +
                r"|\+\d{1,3}[-\.\s]\d{3}[-\.\s]\d{3}[-\.\s]\d{4}" +
                r"|\+\d{2,3}[-\.\s]\(\d{2,3}\)[-\.\s]\d{3,4}[-\.\s]\d{3,4}" +
                r"|\d{2,3}[-\.\s][\/][-\.\s]\d{3,4}[-\.\s]\d{5})")
		
		phone_list = re.findall(phone_regex, html_text)
		
		
		phone_list_cleaned = []
		for phone in phone_list:
			phone_list_cleaned.append(self.phone_cleaning(phone))


		phone_contact_list = []
		for phone in phone_list_cleaned:
			if phone not in phone_contact_list:
				phone_contact_list.append(phone)

		return phone_contact_list
		
	def parse_logo(self, response):

		ext_list = [".png", ".gif", ".jpg", ".tif", ".tiff", ".bmp", ".svg"]

		str_url = str(response.url).lower()
		o = urlparse(str_url)
		homepage = o.scheme + '://' + o.netloc
		logo = []


		CHECK = False
		for tag_a in response.xpath('//a'):
			for tag_img in tag_a.xpath('.//img'):
				img_url = str(tag_img.xpath('@src').extract())
				img_url = self.clean_url(img_url)
				ind = img_url.find('logo')
				if ind > 0:
					CHECK = True
					if img_url.find("https") < 0 or img_url.find("http")< 0 or img_url.find("www") < 0:
						img_url = homepage + img_url
					logo.append(img_url)


		if not CHECK:
			for tag_div in response.xpath('//div'):
				for tag_img in tag_div.xpath('.//img'):
					img_url = str(tag_img.xpath('@src').extract())
					img_url = self.clean_url(img_url)
					ind = img_url.find('logo')
					if ind > 0:
						CHECK = True
						if img_url.find("https") < 0 or img_url.find("http")< 0 or  img_url.find("www") < 0:
							img_url = homepage + img_url
						logo.append(img_url)


		if not CHECK:
			for tag_a in response.xpath('//a'):
				a_href = str(tag_a.xpath('@href').extract())
				a_href = self.clean_url(a_href)
				if a_href[:6] == str("index.") or a_href == homepage:
					for tag_img in tag_a.xpath('.//img'):
						img_url = str(tag_img.xpath('@src').extract())
						img_url = self.clean_url(img_url)
						img_name, img_ext = os.path.splitext(img_url)

						tag_class = str(tag_img.xpath('@class').extract()).lower().strip()
						title = str(tag_img.xpath('@title').extract()).lower().strip()
						alt = str(tag_img.xpath('@alt').extract()).lower().strip()

						if img_ext in ext_list or tag_class.find("logo") > 0 or title.find("logo") > 0 or alt.find("logo") > 0:
							CHECK = True
							if img_url.find("https") < 0 or img_url.find("http") < 0 or img_url.find("www") < 0:
								img_url = homepage + img_url
							logo.append(img_url)
		return logo

	def parse(self, response):

		website =  response.url

		logo = ','.join(self.parse_logo(response))

		phone = self.parse_phone(response)
		cial_test = CialTestItem()


		cial_test['phone'] = []
		if phone:
			cial_test['phone'] = phone

		cial_test['logo'] = []
		if logo:
			cial_test['logo'] = logo

		cial_test['website'] = website
		cial_test['logo'] = logo
		cial_test['phone'] = phone
		#print(cial_test)
		yield cial_test

    