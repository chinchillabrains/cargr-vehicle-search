from bs4 import BeautifulSoup
import requests
import re

def get_moto_listings(request_url):
	url 		= requests.get( request_url )

	soup 		= BeautifulSoup( url.text, "html.parser" )
	vehicles	= soup.find_all( "div", {"class": "p-2"} )
	vehicles_found = []
	for vehicle in vehicles :
		title 		= vehicle.find("h2")["title"]
		price 		= int(vehicle.find("span", {"class": "price-no-decimals"}).string.strip().replace('.', ''))
		vehicle_attributes 		= vehicle.find_all( "div", {"class": "text-muted"} )
		details = vehicle_attributes[0].string
		area = vehicle_attributes[1].find("span").string
		mileage_match = re.search( r"[\d\.]+ χλμ", details)
		mileage = mileage_match.group().replace(' χλμ', '') if mileage_match else ''
		mileage = int(mileage.replace('.', ''))
		vehicles_found.append( {
			"title": title.strip(),
			"price": price,
			"details": details.strip(),
			"area": area.strip(),
			"mileage": mileage,
		})

	return vehicles_found

if __name__ == '__main__':
	# xt_request_url = "https://www.car.gr/classifieds/bikes/?fs=1&condition=used&offer_type=sale&onlyprice=1&price=%3E50&make=270&model=2914&model=6288&model=2915&model=2916&engine_size-from=%3E125&engine_size-to=%3C125&significant_damage=f&sort=cr"
	dero_request_url = "https://www.car.gr/used-bikes/honda.html?condition=used&engine_size-from=125&engine_size-to=125&make=32493&model=15800&model=17763&model=17765&offer_type=sale&onlyprice=1&pg=1&price=%3E50&significant_damage=f&sort=cr"
	for moto in get_moto_listings(dero_request_url):
		print("{price}€ {mileage}χλμ {title} {area} {details}".format(**moto))

