import jieba
import asyncio
from urllib import parse
from scrapy.http import Request
from SlaveCar.items import SlavecarItem
from SlaveCar.Common.StandardDict import  *
from SlaveCar.Common.CommonMethod import  *

# 获得汽车车型
def _getCatType(url):
    urla = url.split("&")
    res = parse.parse_qs(urla[1])
    CType = res.get('ctype')[0];
    if CType == 'b':
        return '宝来';
    elif CType == 't':
        return '骐达';
    elif CType == 'g':
        return '高尔夫';
    elif CType == 'k':
        return '卡罗拉';

# aicar
def aika(response):
    try:
        Ctype = _getCatType(response.url);
        comments = response.xpath('//body/div[@class="home_list clearfix"]')
        for comment in comments:
            car_type = comment.xpath('.//div[@class="tie_rh tie_list1"]/div[@class="tit_list_z clearfix"]'
                                     '/div[@class="tit_list tit_list_t"]/div[@class="list_infor"]/dl/dd/span/a/text()').extract_first()
            post_time = comment.xpath('.//div[@class="tie_rh tie_list1"]/div[@class="publish"]/child::node()[1]').extract()[0]
            youdian = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_22"]/dd/text()').extract_first()
            quedian = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_23"]/dd/text()').extract_first()
            waiguan = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_1"]/dd/text()').extract_first()
            neishi = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_1"]/dd/text()').extract_first()
            kongjian = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_3"]/dd/text()').extract_first()
            shushi = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_4"]/dd/text()').extract_first()
            youhao = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_5"]/dd/text()').extract_first()
            dongli = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_6"]/dd/text()').extract_first()
            caokong = comment.xpath(
                './/div[@class="tie_rh tie_list1"]/div[@class="tit_list"]/div[@class="experience exper_intro"]'
                '/div[@class="review_post"]/dl[@class="dw_6"]/dd/text()').extract_first()
            item = SlavecarItem()
            _SetItemValuesNull(item);
            item['Url'] = response.url
            item['Post_Time'] = post_time.strip()
            item['Car_Type'] = Ctype;
            item['Car_Type_Title'] = car_type
            item['youdian'] = youdian
            item['quedian'] = quedian
            item['waiguan'] = waiguan
            item['SenW'] = SnowNLP(waiguan).sentiments
            item['neishi'] = neishi
            item['SenN'] = SnowNLP(neishi).sentiments
            item['kongjian'] = kongjian
            item['SenK'] = SnowNLP(kongjian).sentiments
            item['dongli'] = dongli
            item['SenD'] = SnowNLP(dongli).sentiments
            item['chaokong'] = caokong
            item['SenC'] = SnowNLP(chaokong).sentiments
            item['youhao'] = youhao
            item['SenY'] = SnowNLP(youhao).sentiments
            item['shushi'] = shushi
            item['SenS'] = SnowNLP(shushi).sentiments
            yield item
    except Exception as e:
        print(e);

# 盖世
def gaisi(response):
    try:
        Ctype = _getCatType(response.url);
        car_title = response.xpath('//div[@class="detailed"]/h1/text()').extract_first()
        post_time = response.xpath('//span[@class="timeSource"]/text()').extract_first()
        comments = response.xpath('//div[@id="ArticleContent"]/p/text()').extract()
        item = SlavecarItem()
        _SetItemValuesNull(item);
        item['Url'] = response.url
        item['Post_Time'] = post_time
        item['Car_Type'] = Ctype
        item['Car_Type_Title'] = car_title
        _SetItemsValue(item, comments);
        yield item
    except Exception as e:
        raise e;

# 搜狐
def souhu(response):
    try:
        Ctype = _getCatType(response.url);
        comments = response.xpath('//div[@class="koubeico"]/div[@class="koubei-tabcon  cur"]/ul/li') + response.xpath(
            '//div[@class="koubeico"]/div[@class="koubei-tabcon "]/ul/li')
        # comments = response.xpath('//div[@class="koubeico"]/div[@class="koubei-tabcon "]/ul/li')
        for comment in comments:
            car_type = comment.xpath('.//div[@class="comm-content"]/div[@class="serise-content"]/a/text()').extract()
            comment_details = comment.xpath('.//div[@class="comm-content"]/p[@class="short-comm"]/text()').extract()
            post_time = comment.xpath('.//div[@class="comm-content"]/div[@class="comm-extra"]/span/text()').extract()
            item = SlavecarItem()
            _SetItemValuesNull(item);
            item['Url'] = response.url
            item['Post_Time'] = post_time
            item["Car_Type"] = Ctype
            item['Car_Type_Title'] = car_type
            _SetItemsValue(item, comments);
            yield item
    except Exception as e:
        raise e;

# 太平洋
def tai(response):
    try:
        Ctype = _getCatType(response.url);
        comments = response.xpath('//div[@class="scollbody"]/div/table')
        for comment in comments:
            youdian = comment.xpath('.//tr/td[2]/div/div[2]/div[1]/span/text()').extract_first()
            quedian = comment.xpath('.//tr/td[2]/div/div[2]/div[2]/span/text()').extract_first()
            waiguan = comment.xpath('.//tr/td[2]/div/div[2]/div[3]/span/text()').extract_first()
            neishi = comment.xpath('.//tr/td[2]/div/div[2]/div[4]/span/text()').extract_first()
            kongjian = comment.xpath('.//tr/td[2]/div/div[2]/div[5]/span/text()').extract_first()
            peizhi = comment.xpath('.//tr/td[2]/div/div[2]/div[6]/span/text()').extract_first()
            dongli = comment.xpath('.//tr/td[2]/div/div[2]/div[7]/span/text()').extract_first()
            chaokong = comment.xpath('.//tr/td[2]/div/div[2]/div[8]/span/text()').extract_first()
            youhao = comment.xpath('.//tr/td[2]/div/div[2]/div[9]/span/text()').extract_first()
            shushi = comment.xpath('.//tr/td[2]/div/div[2]/div[10]/span/text()').extract_first()
            car_type = comment.xpath('.//tr/td/div/div/div[2]/a/text()').extract_first()
            post_time = comment.xpath('.//tr/td/div/div/div/span/a/text()').extract_first()
            commentSum = comment.xpath('.//tr/td[2]/div/div[1]/a/text()').extract();
            item = SlavecarItem()
            item['Url'] = response.url
            item["Car_Type"] = Ctype
            item['Post_Time'] = post_time
            item['Car_Type_Title'] = car_type
            item['youdian'] = youdian
            item['quedian'] = quedian
            item['waiguan'] = waiguan
            item['SenW'] = SnowNLP(waiguan).sentiments
            item['neishi'] = neishi
            item['SenN'] = SnowNLP(neishi).sentiments
            item['kongjian'] = kongjian
            item['SenK'] = SnowNLP(kongjian).sentiments
            item['peizhi'] = peizhi
            item['SenP'] = SnowNLP(peizhi).sentiments
            item['dongli'] = dongli
            item['SenD'] = SnowNLP(dongli).sentiments
            item['chaokong'] = chaokong
            item['SenC'] = SnowNLP(chaokong).sentiments
            item['youhao'] = youhao
            item['SenY'] = SnowNLP(youhao).sentiments
            item['shushi'] = shushi
            item['SenS'] = SnowNLP(shushi).sentiments
            if commentSum == []:
                item['comments'] = None
            else:
                item['comments'] = commentSum
            yield item
    except Exception as e:
        raise e;

# 网易汽车
def wangyi(response):  # 详情页面信息获取
    Ctype = _getCatType(response.url);
    title_A = response.xpath('//div[@id="epContentLeft"]/h1/text()').extract_first()
    title_B = response.xpath('//h1[@id="h1title"]/text()').extract_first()
    post_timeA = response.xpath('//div[@id="epContentLeft"]/div[@class="post_time_source"]/text()').extract_first()
    post_timeB = response.xpath('//div[@class="endContent"]/span[@class="info"]/text()').extract_first()
    post_timeC = response.xpath('//div[@class="endContent"]/span[@class="info"]/span/text()').extract_first()
    post_timeD = response.xpath('//div[@class="ep-info cDGray"]/div[@class="left"]/text()').extract_first()
    commentsA = response.xpath('//div[@id="epContentLeft"]/div[@class="post_body"]/div[@id="endText"]/p/text()').extract()
    commentsB = response.xpath('//div[@class="endContent"]/p/text()').extract()
    commentsC = response.xpath('//div[@id="epContentLeft"]/p/text()').extract()
    commentSum = [];
    print(commentsB);
    item = SlavecarItem()
    _SetItemValuesNull(item);
    item['Url'] = response.url
    item["Car_Type"] = Ctype
    if post_timeA == None:
        if post_timeC == None:
            if post_timeB == None:
                item['Post_Time'] = post_timeD
            else:
                item['Post_Time'] = post_timeB
        else:
            item['Post_Time'] = post_timeC

        item['Car_Type_Title'] = title_B
    else:
        item['Post_Time'] = post_timeA
        item['Car_Type_Title'] = title_A

    if commentsA == []:
        if commentsB == []:
            commentSum = commentsC
        else:
            commentSum = commentsB
    else:
        commentSum = commentsA
    _SetItemsValue(item, commentSum);
    yield item

# 新浪汽车
def sina(response):
    try:
        Ctype = _getCatType(response.url);
        car_title = response.xpath('//div[@class="comment"]/div[@class="wpkwp_ck"]/dl/dd/p/a/text()').extract_first()
        post_time = response.xpath(
            '//div[@class="comment"]/div[@class="wpkwp_ck"]/dl/dd/p[@class="ms"]/span/text()').extract_first()
        comments_youdian = response.xpath(
            '//div[@class="comment"]/div[@class="wpkwp_ck"]/dl/dd/p[@class="yo"]/text()').extract_first()
        comments_quedian = response.xpath(
            '//div[@class="comment"]/div[@class="wpkwp_ck"]/dl/dd/p[@class="qu"]/text()').extract_first()
        comments = response.xpath(
            '//div[@class="comment"]/div[@class="wpkwp_ck"]/dl/dd/p[@class="zs"]/text()').extract();
        item = SlavecarItem()
        _SetItemValuesNull(item);
        item['Url'] = response.url;
        item['Post_Time'] = post_time;
        item['Car_Type'] = Ctype
        item['Car_Type_Title'] = car_title;
        item['youdian'] = comments_youdian;
        item['quedian'] = comments_quedian;
        _SetItemsValue(item, comments);
        yield item
    except Exception as e:
        raise e;

# 易车网
def yiche(response):
    try:
        Ctype = _getCatType(response.url);
        car_type = response.xpath('//div[@class="con-l"]/h6/text()').extract_first()
        post_time = response.xpath('//div[@class="comment-summary"]//span/text()').extract_first()
        HeadList = response.xpath('//div[@class="details-cont"]/div[@class="item-box div_ImgLoadArea"]/div[@class="head"]/text()').extract()
        commentList = response.xpath('//div[@class="details-cont"]/div[@class="item-box div_ImgLoadArea"]/p/text()').extract()
        commentsSum = response.xpath( '//div[@class="details-cont"]/div[@class="item-box div_ImgLoadArea"]/text()').extract()
        item = SlavecarItem()
        _SetItemValuesNull(item);
        FHList = [];
        item['Url'] = response.url
        item['Post_Time'] = post_time
        item['Car_Type'] = Ctype
        item['Car_Type_Title'] = car_type
        if len(HeadList) == 2:
            _SetItemsValue(item, commentsSum);
        else:
            for t in HeadList:
                t = ''.join(t.split())
                if t != '综合：' and t != '':
                    FHList.append(t);
            print(FHList);
            for (h, c) in zip(FHList, commentList):
                h = ''.join(h.split())
                c = ''.join(c.split())
                if h == '满意：':
                    item["youdian"] = c;
                elif h == '不满意：':
                    item["quedian"] = c;
                elif h == '外观：':
                    item["waiguan"] = c;
                    item['SenW'] = SnowNLP(c).sentiments
                elif h == '内饰：':
                    item["neishi"] = c;
                    item['SenN'] = SnowNLP(c).sentiments
                elif h == '空间：':
                    item["kongjian"] = c;
                    item['SenK'] = SnowNLP(c).sentiments
                elif h == '配置：':
                    item["peizhi"] = c;
                    item['SenP'] = SnowNLP(c).sentiments
                elif h == '动力：':
                    item["dongli"] = c;
                    item['SenD'] = SnowNLP(c).sentiments
                elif h == '操控：':
                    item["chaokong"] = c;
                    item['SenC'] = SnowNLP(c).sentiments
                elif h == '油耗：':
                    item["youhao"] = c;
                    item['SenY'] = SnowNLP(c).sentiments
                elif h == '舒适度：':
                    item["shushi"] = c;
                    item['SenS'] = SnowNLP(S).sentiments
            item['comments'] = ''.join(commentsSum).strip();
        yield item
    except Exception as e:
        raise e;

# 将解析方法放入字典中
switch={'aika':aika
       ,'gaisi': gaisi
       ,'souhu': souhu
       ,'tai': tai
       ,'wangyi': wangyi
       ,'sina': sina
       ,'yiche': yiche
        };

# 根据传入参数调用解析方法
def CommonFun(response,UrlType):
    try:
        method = switch.get(UrlType)
        if method:
            yield from method(response)
    except Exception as e:
        print(e);

# 设置冗余字段值为NUll
def _SetItemValuesNull(item):
    item['Car_Type'] = None;
    item['youdian'] = None
    item['quedian'] = None
    item['waiguan'] = None
    item['neishi'] = None
    item['kongjian'] = None
    item['peizhi'] = None
    item['dongli'] = None
    item['chaokong'] = None
    item['youhao'] = None
    item['shushi'] = None
    item['comments'] = None
    item['SenW'] = None
    item['SenN'] = None
    item['SenK'] = None
    item['SenP'] = None
    item['SenD'] = None
    item['SenC'] = None
    item['SenY'] = None
    item['SenS'] = None

# 对总评进行分类
def _SetItemsValue(item,Commons):
    commonStr = ''.join(Commons).strip();
    ComentList = divideWords(commonStr);
    for coms in ComentList:
        for u in waiguan:
            if u in coms:
                item["waiguan"] = coms;
                item['SenW'] = SnowNLP(coms).sentiments
        for u in neishi:
            if u in coms:
                item["neishi"] = coms;
                item['SenN'] = SnowNLP(coms).sentiments

        for u in kongjian:
            if u in coms:
                item["kongjian"] = coms;
                item['SenK'] = SnowNLP(coms).sentiments

        for u in peizhi:
            if u in coms:
                item["peizhi"] = coms;
                item['SenP'] = SnowNLP(coms).sentiments
        for u in dongli:
            if u in coms:
                item["dongli"] = coms;
                item['SenD'] = SnowNLP(coms).sentiments
        for u in chaokong:
            if u in coms:
                item["chaokong"] = coms;
                item['SenC'] = SnowNLP(coms).sentiments
        for u in youhao:
            if u in coms:
                item["youhao"] = coms;
                item['SenY'] = SnowNLP(coms).sentiments
        for u in shushi:
            if u in coms:
                item["shushi"] = coms;
                item['SenS'] = SnowNLP(coms).sentiments
        item['comments'] = commonStr;



