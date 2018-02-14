#font color Define
RED_FC = 1
YELLOW_FC = 2
DEFAULT_FC = 0
FC_FLAG = 0

class table_src:
    def set_data(self,cnt,url,name,due,regist_day):
        self.cnt = cnt
        self.url = url
        self.name = name
        self.due = due
        self.regist_day = regist_day
def input_css(html) :
    html = html + "<style type='text/css'>\n@import url('style.css');\n</style>\n"
    return html

def default_html(html) :
    html = html + "<table class='type09'>\n    <thead>\n    <tr>\n        <th scope='cols'>번호</th>\n        <th scope='cols'>지원 사업명</th>\n        <th scope='cols'>신청기간</th>\n        <th scope='cols'>등록일</th>\n    </tr>\n    </thead>\n    <tbody>\n"
    return html

def write_table(html, flag, table_src) :
    due_color = ""
    if flag :
        if flag == RED_FC :
            due_color = "class='red'"
        if flag == YELLOW_FC :
            due_color = "class='yellow'"

    html = html + "    <tr>\n        <th scope='row'>%s</th>\n        <td><a href=\"%s\">%s</a></td>\n        <td  %s>%s</td>\n        <td>%s</td>\n    </tr>\n" % (table_src.cnt,table_src.url,table_src.name,due_color,table_src.due,table_src.regist_day)
    return html

def html_tail(html) :
    html = html + "    </tbody>\n</table>\n"
    return html

def save_html(html, now) :
    f_name = ("result_%s" % now)[:23].replace(":","",2)+".html"
    f = open(f_name,"w")
    f.write(html)
    f.close()

def input_script(html) :
    html = html + "<script>\n var biNetSelect = function(postSeq, paramValue){ \n		var paramArray = paramValue.split(':');\n		var boardID = paramArray[0];\n		var frefaceCode =paramArray[1];\n		var viewFlag = paramArray[2];\n		var registDate = paramArray[3];\n		\n		document.listForm.action = 'http://www.bi.go.kr/board/editView.do';\n		document.listForm.elements['boardVO.boardID'].value = boardID;\n		document.listForm.elements['boardVO.postSeq'].value = postSeq;\n		document.listForm.elements['boardVO.registDate'].value = registDate;\n		document.listForm.elements['boardVO.viewFlag'].value = viewFlag;\n		document.listForm.elements['boardVO.frefaceCode'].value =frefaceCode;\n		\n		document.listForm.submit();		\n	};\n</script>\n"
    return html

def input_form(html) :
    html = html + '<form name="listForm" method="post" action="http://www.bi.go.kr/board/editView.do">\n<input id="currentPage" name="currentPage" type="hidden" value="0"/>\n<input id="boardVO.boardID" name="boardVO.boardID" type="hidden" value="RECRUIT"/>\n<input id="boardVO.boardName" name="boardVO.boardName" type="hidden" value="주요모집공고"/>\n<input id="boardVO.postSeq" name="boardVO.postSeq" type="hidden" value="999939860"/>\n<input id="boardVO.viewFlag" name="boardVO.viewFlag" type="hidden" value="view"/>\n<input id="boardVO.registDate" name="boardVO.registDate" type="hidden" value="20180209033259"/>\n<input id="boardVO.frefaceCode" name="boardVO.frefaceCode" value="ENTERPRISERECRUIT" type="hidden" />\n</form>\n'
    return html

