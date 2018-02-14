from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import make_html

#크롬 드라이버의 경로를 지정해준다.
C_D_PATH = "c:\chrom_driver\chromedriver"
CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

#제목을 걸러낼 필터를 만든다.
OK_FILTER = ['인턴', '디딤돌','ICT','인공지능', '창업', '특허', '마케팅', '산업인턴','기술']
NOT_OK_FILTER = ['장비','온실가스','청소년','입주','생명','현장','일본','의료','해양','자동차','관광','융복합','생태계','장애인','크라우드펀딩','항만','농산','부품','연구인력','철도','수산','기상','시제품','인체','시큐리티','환경산업','선박','건설','협력', '산학연협력', '강소기업','바이오','신재생','교육생','여성벤처','여성창업','농림','식품','재도전','환경기술']


def check_not_ok(name) : #제외 단어 필터링
    for not_ok in NOT_OK_FILTER:
        if name.find(not_ok) >= 0:
            return -1
    return 0

def crm_cfg() : #크롬의 옵션을 정해준다.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.binary_location = CHROME_PATH

def check_date(due_str) : #기한의유효성을 확인.
    due = datetime.datetime.strptime(due_str, '%Y-%m-%d')
    due_date = due.strftime('%Y-%m-%d')
    red_date = (now + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    yellow_date = (now + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    if now_date > due_date:
        return -1
    if due_date <= red_date :
        return make_html.RED_FC
    if due_date <= yellow_date :
        return make_html.YELLOW_FC

    return 0

#오늘의 날짜를 저장한다 기한과 비교할것이다.
now = datetime.datetime.now()
now_date = now.strftime('%Y-%m-%d')

chrome_options = webdriver.ChromeOptions()
crm_cfg()
# selenium의 webdriver로 옵션을 추가하여크롬 브라우저를 실행한다.
driver = webdriver.Chrome(executable_path=C_D_PATH, chrome_options=chrome_options)

def bizinfo(html) :
    #글의 기본 URL이다.
    BASE_URL = "http://www.bizinfo.go.kr/see/seea/selectSEEA140Detail.do?pblancId=%s&menuId=80001001001"


    #Page를 변경할 변수를 선언한다.
    page=1
    #while을 종료할수있는 플래그를 만든다.
    end_flag = False

    #몇개를 발견했는지 세보자
    cnt=1

    html = make_html.default_html(html)

    while 1 :
        if end_flag:
            break
        #순차적으로 다음페이지에 접속하기 위해 URL을 만들어준다.
        INPUT_URL = "http:/www.bizinfo.go.kr/see/seea/selectSEEA100.do?pageIndex=%d" % page
        #Page 변경후 i값을 1 증가시켜 다음 페이지를 열 준비를 한다.
        page = page+1

        #홈페이지에 접속한다.
        driver.get(INPUT_URL)
        #페이지의 element 모두가져오기
        html_parse = driver.page_source
        soup = BeautifulSoup(html_parse, 'html.parser')
        #사업명이 들어있는 필드에 접근해서 모든 사업명을 total_title이라는 변수에 넣는답
        total_title = soup.select("#content > div.boardBusiness > div.bbsTable > table > tbody > tr > td.txtAgL > a")
        #table에서 값을 따로 가져오기 위해 Table에서 가장 가까운 div를 잡는다.
        table_div = soup.find(class_="bbsStyle1")
        #table을 포커싱 하기위해서 div에서 모든 tbody를 찾는다.(하나밖에없긴하다)
        tables = table_div.find_all('tbody')
        #첫번째 table을 기준으로 잡는다.
        table = tables[0]
        #기준이 되는 테이블에서 모든 tr을 찾는다.
        trs = table.find_all("tr")
        #tr을 변경할 변수 j선언
        tr_cnt = 0
        for title in total_title:
            if end_flag :
                break
            #사업명을 가져옴
            name = title.text.lstrip().rstrip()
            #제외키워드
            result = check_not_ok(name)
            if result <0 :
                continue

            #필요한 단어들이 있는지 필터링
            for ok in OK_FILTER:
                if name.find(ok) >= 0 :
                    fc_flag = make_html.DEFAULT_FC
                    #j번째 tr에서 모든 td를 찾는다.
                    tds = trs[tr_cnt].find_all("td")
                    tr_cnt = tr_cnt + 1
                    #다섯번째 td에서 등록일을 가져온다
                    regist_day = tds[4].string.lstrip().rstrip()
                    if regist_day[0:4] == '2017' : #작년 년도수를
                        end_flag=True
                        break

                    # 세번째 td에서 기한을 가져옴
                    due_ori = tds[2].string.lstrip().rstrip()
                    # 기한이 지났는지 체크
                    if len(due_ori) == 23:
                        due_str = due_ori[13:]
                        fc_flag = check_date(due_str)
                        if fc_flag < 0 :
                            break

                    #첫번째 td에서 글번호
                    num = tds[0].string.lstrip().rstrip()

                    #네번째 td에서 기관명을 가져옴
                    org = tds[3].string.lstrip().rstrip()

                    #글의 PBLN값을 가져옴 (PBLN값은 글에 들어갈 주소에 필요한 값.)
                    pbln = title.get('onclick')[17:37]

                    url = BASE_URL % pbln
                    table_src = make_html.table_src
                    table_src.set_data(table_src,cnt,url,name,due_ori,regist_day)
                    html = make_html.write_table(html, fc_flag, table_src)

                    print("%d. %s/%s/ (%s)" % (cnt,name,regist_day,url)) #debug
                    cnt = cnt+1
                    break

    driver.close()
    html = make_html.html_tail(html)
    return html

def kstratup(html) :
    #글의 기본 URL이다.
    BASE_URL = "k-startup.go.kr/common/announcement/announcementDetail.do?searchDtlAncmSn=0&searchPrefixCode=BOARD_701_001&searchBuclCd=&searchAncmId=&searchPostSn=%s&bid=701&mid=30004&searchBusinessSn=0"

    #Page를 변경할 변수를 선언한다.
    page=1
    #while을 종료할수있는 플래그를 만든다.
    end_flag = False

    #몇개를 발견했는지 세보자
    cnt=1

    html = make_html.input_script(html)
    html = make_html.default_html(html)
    html = make_html.input_form(html)
    #페이지에 접속하기 위해 URL을 만들어준다.
    INPUT_URL = "http://k-startup.go.kr/common/announcement/announcementList.do"

    #홈페이지에 접속한다.
    driver.get(INPUT_URL)
    #페이지의 element 모두가져오기
    html_parse = driver.page_source
    soup = BeautifulSoup(html_parse, 'html.parser')
    #사업명이 들어있는 필드에 접근해서 모든 사업명을 total_title이라는 변수에 넣는답
    total_title = soup.select("#content_w1100 > div > ul > li > h4 > a")
    #table에서 값을 따로 가져오기 위해 Table에서 가장 가까운 div를 잡는다.
    total_info = soup.find_all(class_="list_info")

    #tr을 변경할 변수 j선언
    li_cnt = 0
    for title in total_title :
        name = title.text.lstrip().rstrip()
        #제외키워드
        result = check_not_ok(name)
        if result <0 :
            continue

        #필요한 단어들이 있는지 필터링
        for ok in OK_FILTER:
            if name.find(ok) >= 0:

                #j번째 tr에서 모든 td를 찾는다.
                lis = total_info[li_cnt].find_all("li")
                li_cnt = li_cnt + 1

                due_ori = lis[2].string.lstrip().rstrip()[6:16]
                if len(lis) >= 3 :
                    # 기한이 지났는지 체크
                    fc_flag = make_html.DEFAULT_FC
                    fc_flag = check_date(due_ori)
                    if fc_flag < 0 :
                        break

                #네번째 td에서 기관명을 가져옴
                org = lis[2].string.lstrip().rstrip()

                #글의 HREF값을 가져옴
                href = title.get('href')

                if href.find('itemSelect') >= 0 :
                    url = BASE_URL % href[40:44]

                if href.find('biNetSelect') >= 0 :
                    url = href

                regist_day = ""
                table_src = make_html.table_src
                table_src.set_data(table_src, cnt, url, name, due_ori, regist_day)
                html = make_html.write_table(html,fc_flag,table_src)
                print("%d. %s/%s/ (%s)" % (cnt,name,due_ori,url)) #debug
                cnt = cnt + 1
                break

    driver.close()
    html = make_html.html_tail(html)
    return html


html = ""
html = make_html.input_css(html)
html = bizinfo(html)
html = kstratup(html)

#파일저장
make_html.save_html(html,now)