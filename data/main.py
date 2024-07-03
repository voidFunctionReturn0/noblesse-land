import pdfplumber
import datetime
import time
import random
import os
from models.building import Building
from models.owner import Owner
from models.owner_building import OwnerBuilding
from models.coordinates import Coordinates
from functools import reduce
from dataclasses import replace
import requests
from repo import Repo
from bs4 import BeautifulSoup as bs


NAMU_WIKI_DOMAIN = 'https://namu.wiki'
DEFAULT_PROFILE_IMAGE_PATH = f'res/account_circle.png'


def remove_newline(string):
    return string.replace('\n', '')


def add_building(building, buildings, owner, owners_buildings):
    buildings.append(building)
    owners_buildings.append(OwnerBuilding(owner=owner, building=building, created_at=CREATED_AT))
    return [buildings, owners_buildings]


def page_processor(acc, page):
    if page.extract_table() is None:
        return acc
    else:
        return reduce(row_processor, page.extract_table(), acc)


def number_string_to_int(string):
    return int(string.replace(',', ''))


def correct_last_building(buildings, TYPE, DETAILS, NOTE):
    building = buildings[-1]
    if TYPE != '':
        building.type += TYPE
    if DETAILS != '':
        building.details += DETAILS
    if NOTE != '':
        building.note += NOTE
    return buildings


def get_coordinates_query(details):
    space건물idx = details.find(" 건물")
    space대지idx = details.find(" 대지")
    건물idx = details.find("건물")
    대지idx = details.find("대지")
    제곱미터idx = details.find("㎡")

    idxs = [space건물idx, space대지idx, 건물idx, 대지idx, 제곱미터idx]
    idxs = [idx for idx in idxs if idx != -1]
    idxs.sort()

    if not idxs:
        raise Exception("건물, 대지 없음")
    else:
        last_pointer = idxs[0]

    return details[:last_pointer]    


def fetch_coordinates(details, buildings):
    query = get_coordinates_query(details)
    old_building_result = [building for building in buildings if get_coordinates_query(building.details) == query]
    if old_building_result:
        old_building_result[0].coordinates
    else:
        # TODO: headers 정보를 숨기기
        headers={
            'X-Naver-Client-Id': 'lkSa69oJrH5iDsz0gaWS',
            'X-Naver-Client-Secret': 'og0iVFM6hr'
        }
        response = requests.get(f"https://openapi.naver.com/v1/search/local.json?query={query}", headers=headers).json()

        if "items" in response:
            response = response["items"]
            if response:
                x = response[0]["mapx"]
                y = response[0]["mapy"]
                return Coordinates(x, y)
            else:
                return None
        elif response['errorMessage'] == 'Rate limit exceeded. (속도 제한을 초과했습니다.)':
            print("## 1 second time sleep due to 네이버 API 호출 속도 제한")
            time.sleep(1)
            return fetch_coordinates(details, buildings)
        else:
            print(f'response: {response}')
            raise Exception('네이버 API 에러')
        

def update_building(relation, type, details, price, note, owners, buildings, owners_buildings):
    owner = owners[-1]
    if (price == ''):
        buildings = correct_last_building(buildings, type, details, note)
    else:
        coordinates = fetch_coordinates(details, buildings)
        price = number_string_to_int(price) * 1000
        new_building = Building(type=type, details=details, price=price, note=note, coordinates=coordinates)
        if note == '〃':
            note = buildings[-1].note

        if (price == 0):
            pass
        elif (type == '임야') or (type == '묘지'):
            pass
        elif (owner.relation is None):
            owner.relation = relation
            buildings, owners_buildings = add_building(new_building, buildings, owner, owners_buildings)

        elif (owner.relation == relation):
            buildings, owners_buildings = add_building(new_building, buildings, owner, owners_buildings)
        else:
            owner = replace(owner, relation=relation)
            owners.append(owner)
            buildings, owners_buildings = add_building(new_building, buildings, owner, owners_buildings)

    return [buildings, owners_buildings]


def fetch(URL):
    print(f'## fetch: {URL}')
    time.sleep(random.uniform(2,4))
    return requests.get(URL)


def download(SRC_URL, FILE_PATH):
    FILE_PATH = FILE_PATH.replace(' ', '')
    print(f' FILE_PATH: {FILE_PATH}')

    if not os.path.isfile(FILE_PATH):
        os.system(f'curl --output {FILE_PATH} {SRC_URL}')
        time.sleep(random.uniform(2,4))   


def has_profile_image(div_tag):
    if div_tag.has_attr('style'):
        style = div_tag['style'].replace(' ', '')
        return (style == 'width:420px;') or (style == 'width:400px;')
    else:
        return False


def get_image_from_detail_page(DETAIL_URL, FILE_NAME):
    print(f'## url: {DETAIL_URL}')
    print(f'## file_name: {FILE_NAME}')

    RESPONSE = fetch(DETAIL_URL)
    if RESPONSE.status_code != 200:
        print('## ERROR')
        print(f'## response: {RESPONSE}')
        raise Exception('상세페이지 불러오기 실패')

    DIVS = bs(RESPONSE.text, 'html.parser').find_all('div')
    DIVS = list(filter(has_profile_image, DIVS))

    if len(DIVS) == 0:
        return DEFAULT_PROFILE_IMAGE_PATH

    IMAGES = DIVS[0].find_all('img')

    if len(IMAGES) == 0:
        return DEFAULT_PROFILE_IMAGE_PATH

    PROFILE_IMAGE = IMAGES[0]
    SRC = PROFILE_IMAGE.get('src')
    SRC_URL = 'https:' + SRC
    FILE_EXTENSION = SRC.split('.')[-1]
    FILE_PATH = f'res/{FILE_NAME}.{FILE_EXTENSION}'
    download(SRC_URL, FILE_PATH)
    return FILE_PATH


def create_image_path(NAME, ORGANIZATION, POSITION):
    image_path = DEFAULT_PROFILE_IMAGE_PATH
    QUERY = ' '.join([NAME, ORGANIZATION, POSITION])
    SEARCH_PATH = '/Search?q='
    SEARCH_URL = NAMU_WIKI_DOMAIN + SEARCH_PATH + QUERY
    RESPONSE = fetch(SEARCH_URL)

    if RESPONSE.status_code == 200:
        SECTION_ITEMS = bs(RESPONSE.text, 'html.parser').select('section')[0].children
        RESULTS = [ITEM for ITEM in SECTION_ITEMS if ITEM.name == 'div']
        MATCHING_RESULTS = []
        for RESULT in RESULTS:
            A_TAG = RESULT.find('a')
            if A_TAG:
                TITLE = A_TAG.text.strip()
                TEXT = RESULT.text
                ORGANIZATION_PARTS = ORGANIZATION.split(' ')
                POSITION_PARTS = POSITION.split(' ')
                if (NAME in TITLE) and all([PART in TEXT for PART in ORGANIZATION_PARTS]) and all([PART in TEXT for PART in POSITION_PARTS]):
                    MATCHING_RESULTS.append(RESULT)
        
        if len(MATCHING_RESULTS) > 0:
            MATCHING_RESULTS.sort(key=lambda RESULT: len(RESULT.find('a').text.strip()))
            RESULT = MATCHING_RESULTS[0]
            HREF = RESULT.find('a').get('href')
            FILE_PATH = get_image_from_detail_page(NAMU_WIKI_DOMAIN + HREF, f'{ORGANIZATION}_{POSITION}_{NAME}')
            if FILE_PATH:
                image_path = FILE_PATH
        
    else:
        print('## ERROR')
        print(f'## response: {RESPONSE}')
        raise Exception('크롤링 실패')
    
    return image_path


def row_processor(acc, row):
    owners, buildings, owners_buildings, is_creating_building = acc
    if row[0] is not None:
        row[0] = row[0].replace('\n', '')
    match row:
        case ['소속', organization, None, '직위', position, None, '성명', name] | ['소속', organization, None, '직위', position, '성명', name] | ['소 속', organization, None, '직 위', position, None, None, None, '성 명', None, None, name] | ['소 속', organization, None, '직 위', position, None, '성 명', None, name] | [None, '소 속', organization, None, '직 위', position, None, None, None, '성 명', None, None, name] | ['소 속', organization, None, '직 위', position, None, None, '성 명', None, None, name] | ['소 속', organization, None, '직 위', position, None, None, None, '성 명', None, None, name, None, None] | ['소 속', organization, None, '직 위', position, None, None, None, '성 명', None, name]:
            is_creating_building = False
            organization, position, name = list(map(remove_newline, [organization, position, name]))
            name = name.replace(' ', '')
            owners.append(Owner(name=name, organization=organization, position=position, image_path=create_image_path(name, organization, position)))

        case ['▶ 건물(소계)', *last] | ['▶건물(소계)', *last] | [_, '▶건물(소계)', *last]:
            is_creating_building = True

        case ['▶ 부동산에 관한 규정이 준용되는 권리와 자동차·건설기계·선박 및 항공기(소계)', *last] | ['▶ 예금(소계)', *last] | ['▶ 현금(소계)', *last] | ['▶부동산에 관한 규정이 준용되는 권리와 자동차·건설기계·선박 및 항공기(소계)', *last] | ['▶예금(소계)', *last] | ['▶현금(소계)', *last] | [None, '▶부동산에 관한 규정이 준용되는 권리와 자동차·건설기계·선박 및 항공기(소계)', *last] | ['▶자동차(소계)', None, None, None, None, *last]:
            is_creating_building = False

        case ['', None, *last]:
            pass

        # 5 params
        case [relation, type, details, price, note] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            if '(' in price:
                price, _실거래가격 = price.split('(')
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 7 params
        case [relation, type, details, None, price, None, note] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            if '(' in price:
                price, _실거래가격 = price.split('(')
            buildings, owners_buildings = update_building(relation, type, details, price, owners, buildings, owners_buildings)

        # 8 params
        case [relation, type, details, _종전가액, _증가액, _감소액, price, note] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 9 params
        case [relation, type, details, None, None, price, None, note, None] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 9 params
        case [_, relation, type, details, _종전가액, _증가액, _감소액, price, note] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 11 params
        case [relation, type, details, None, None, _종전가액, _증가액, _감소액, None, price, note] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 11 params
        case [relation, type, details, None, None, _종전가액, _증가액, _감소액, price, note, _] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 12 params
        case [relation, type, details, None, None, _종전가액, _증가액, _감소액, None, price, note, None] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 13 params
        case [None, relation, type, details, None, None, _종전가액, _증가액, _감소액, None, price, note, None] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)

        # 14 params
        case [relation, type, details, None, None, _종전가액, _증가액, _감소액, None, price, note, None, None, None] if (is_creating_building == True):
            relation, type, details, price, note = list(map(remove_newline, [relation, type, details, price, note]))
            buildings, owners_buildings = update_building(relation, type, details, price, note, owners, buildings, owners_buildings)
        
        case [None, *last]:
            pass

    return [owners, buildings, owners_buildings, is_creating_building]


ORIGINS_PATH = "./origins"

start = time.time()


total_building_len = 0
total_owner_len = 0
for DIR_NAME in os.listdir(ORIGINS_PATH):
    YEAR, MONTH, DAY = list(map(int, DIR_NAME.split("_")))
    CREATED_AT = datetime.datetime(YEAR, MONTH, DAY)
    
    for PDF_NAME in os.listdir(f'{ORIGINS_PATH}/{DIR_NAME}'):
        PDF_PATH = f'{ORIGINS_PATH}/{DIR_NAME}/{PDF_NAME}'
        print(f'## {PDF_PATH}')

        PDF = pdfplumber.open(PDF_PATH)
        owners, buildings, owners_buildings, _is_creating_building = reduce(page_processor, PDF.pages, [[], [], [], False])

        total_building_len += len(buildings)
        total_owner_len += len(owners)
        print(f'## owners len: {len(owners)}')
        print(f'## building len: {len(buildings)}')
        print(f'## owners_buildings len: {len(owners_buildings)}')
        print(f'## total_building_len: {total_building_len}')
        print(f'## total_owner_len: {total_owner_len}')
        print('')


# PDF_PATH = "./origins/2024_03_28/경기도_240328.pdf"
# pdf = pdfplumber.open(PDF_PATH)
# CREATED_AT = datetime.datetime(2024, 3, 28)
# pages = pdf.pages
# owners, buildings, owners_buildings, _is_creating_building = reduce(page_processor, pages, [[], [], [], False])
# print(f'## owners len: {len(owners)}')
# print(f'## building len: {len(buildings)}')
# print(f'## owners_buildings len: {len(owners_buildings)}')
# for ob in owners_buildings:
#     print(ob)


## DB INSERT
# repo = Repo()
# for building in buildings:
#     repo.insert_building(building)

# for owner in owners:
#     repo.insert_owner(owner)

# for owner_building in owners_buildings:
#     repo.insert_owner_building(owner_building)


print(f"time : {time.time() - start} sec")