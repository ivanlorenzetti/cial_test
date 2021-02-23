import re
url = 'https://www.phosagro.com/contacts/'

import requests

r = requests.get(url)

def phone_light_cleaning(phone):
	filtered_str = ''
	allowed_chars = ['0','1','2','3','4','5','6','7','8','9','(',')','+']
	for char in phone:
		if char in allowed_chars:
			filtered_str += char
		else:
			filtered_str += ''

	return filtered_str


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
phone_list = re.findall(phone_regex, r.text)


phone_list_cleaned = []
for phone in phone_list:
	phone_list_cleaned.append(phone_light_cleaning(phone))


phone_contact_list = []
for phone in phone_list_cleaned:
    if phone not in phone_contact_list:
        phone_contact_list.append(phone)



print((phone_contact_list))