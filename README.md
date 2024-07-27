# 나라님 부동산

### 문제 인식
1. <a href="https://www.peti.go.kr/prptOptp.do">우리나라는 고위공직자 재산을 정기적으로 공개하고 있음</a>
2. 고유공직자는 미공개 정보를 이용할 가능성이 있으므로, 고위공직자 부동산 소유액이 많은 곳은 향후 가치가 상승할 가능성이 높을 것 같음
3. 재산 공개 데이터는 PDF 형식이라, 고위공직자가 어느 동네, 어느 아파트에 부동산 소유액이 많은지 알기 어려움


### 해결 방법
고위공직자 부동산 정보를 (읍/면/동 or 아파트) 단위로 묶어서
소유 자산액이 많은 순으로 랭킹을 볼 수 있도록 함


### 주요 타겟
부동산 투자에 관심이 있는 사람


### 할 일
<b>Python 앱(data 폴더)</b><br/>
<del><label for="download_pdf">PDF 다운로드(일단 수동으로 하고, 추후 자동화)</label></del><br/>
<del><label for="parse_pdf">PDF 파싱</label></del><br/>
<del><label for="naver_location_search_api">아파트별 위도, 경도 정보 불러오기(네이버 지역 검색 API 사용)</label></del><br/>
<del><label for="get_profile_image">공직자별 프로필 사진 저장하기(나무위키 스크래핑)</label></del><br/>
<label for="insert_data">공직자, 재산 데이터를 DB에 저장하기</label><br/>

<b>Phoenix 앱(service 폴더)</b><br/>
<label for="show_properties_map">재산 정보를 지도로 표시하기</label><br/>
<label for="show_properties_rank">(동네 or 아파트) 랭킹 표시하기</label><br/>
<label for="search_location">지역 검색 기능 추가</label><br/>
<label for="search_name">공직자 이름 검색 기능 추가</label><br/>


### 예시 이미지
<img width="300" src="https://github.com/user-attachments/assets/80a950b2-7918-4f7b-8c36-265b41de9d71" />
<img width="300" src="https://github.com/user-attachments/assets/a369e7cd-9dfb-417f-8d3a-54dc4b7d4311" />
<img width="300" src="https://github.com/user-attachments/assets/52f31428-8139-428a-a0db-cda508f89332" />
