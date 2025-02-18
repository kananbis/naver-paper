import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=coupon"
page_url = "https://www.ppomppu.co.kr/zboard/zboard.php?"

def find_naver_campaign_links(visited_urls_file='visited_urls_ppomppu.txt'):
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    list_subject_links = soup.find_all('td', class_='list_vspace')

    naver_links = []
    for span in list_subject_links:
        a_tag = span.find('a', href=True)

        if a_tag and '네이버' in a_tag.text:
            naver_links.append(a_tag['href'])

    # Initialize a list to store campaign links
    campaign_links = []

    # Check each naver_links
    for link in naver_links:
        full_link = urljoin(page_url, link)
        print("naver_links - " + full_link)
        if link in visited_urls:
            continue  # Skip already visited links

        res = requests.get(full_link)
        inner_soup = BeautifulSoup(res.text, 'html.parser')

        campaign_a_tags = inner_soup.find_all('a', href=True)

        for a_tag in campaign_a_tags:
            campaign_link = a_tag.get_text().strip()

            if ('campaign2-api.naver.com' in campaign_link or 'ofw.adison.co' in campaign_link) and campaign_link not in campaign_links:
                campaign_links.append(campaign_link)

        # Add the visited link to the set
        visited_urls.add(link)

    # Save the updated visited URLs to the file
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')

    return campaign_links