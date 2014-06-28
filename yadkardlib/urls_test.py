#!/data/project/yadkard/venv/bin/python
# -*- coding: utf-8 -*-

"""Test urls.py module."""


import unittest

import urls


class BostonTest(unittest.TestCase):

    def test_bg1(self):
        """boston.com"""
        i = 'http://www.boston.com/health/2014/06/02/companies-offer-health-plans-new-hampshire/GmmhqI6s4GmTlMWN3HBLnM/story.html'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Ramer|first=Holly|title=5 companies to offer health plans in New Hampshire|website=Boston.com|date=2014-06-02|year=2014|url=http://www.boston.com/health/2014/06/02/companies-offer-health-plans-new-hampshire/GmmhqI6s4GmTlMWN3HBLnM/story.html|ref=harv|accessdate='
        self.assertIn(e, o.cite)

    def test_bg2(self):
        """bostonglobe.com"""
        i = 'http://www.bostonglobe.com/metro/2014/06/03/walsh-meets-with-college-leaders-off-campus-housing/lsxtLSGJMD86Gbkjay3D6J/story.html'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Saltzman|first=Jonathan|last2=Farragher|first2=Thomas|title=Walsh meets with college leaders on off-campus housing|website=BostonGlobe.com|date=2014-06-03|year=2014|url=https://www.bostonglobe.com/metro/2014/06/03/walsh-meets-with-college-leaders-off-campus-housing/lsxtLSGJMD86Gbkjay3D6J/story.html|ref=harv|accessdate='
        self.assertIn(e, o.cite)
        

class WashingtonpostTest(unittest.TestCase):

    def test_wp1(self):
        """`1 author, 2005, the pubdate is different from last edit date"""
        i = 'http://www.washingtonpost.com/wp-dyn/content/article/2005/09/02/AR2005090200822.html'
        o = urls.Citation(i)
        e1 = u'{{sfn|Sachs|2005}}'
        e2 = u'* {{cite web|last=Sachs|first=Andrea|title=March of the Migration|website=Washington Post|date=2005-09-04|year=2005|url=http://www.washingtonpost.com/wp-dyn/content/article/2005/09/02/AR2005090200822.html|ref=harv|accessdate='
        self.assertIn(e1, o.ref)
        self.assertIn(e2, o.cite)


class HuffingtonpostTest(unittest.TestCase):

    def test_hp1(self):
        """`1 author, 2013"""
        i = 'http://www.huffingtonpost.ca/annelise-sorg/blackfish-killer-whale-seaworld_b_3686306.html'
        o = urls.Citation(i)
        e1 = u'{{sfn|Sorg|2013}}'
        e2 = u'* {{cite web|last=Sorg|first=Annelise|title=When Killer Whales Kill: Why the movie "Blackfish" Should Sink Captive Whale Programs|website=The Huffington Post|date=2013-08-01|year=2013|url=http://www.huffingtonpost.ca/annelise-sorg/blackfish-killer-whale-seaworld_b_3686306.html|ref=harv|accessdate='
        self.assertIn(e1, o.ref)
        self.assertIn(e2, o.cite)


class DilyTelegraphTest(unittest.TestCase):

    def test_dt1(self):
        """`1 author, 2005"""
        i = 'http://www.telegraph.co.uk/health/3334755/We-could-see-the-whales-eyes-mouth...-the-barnacles-on-its-back.html'
        o = urls.Citation(i)
        e1 = u'{{sfn|Fogle|2005}}'
        e2 = u"* {{cite web|last=Fogle|first=Ben|title=We could see the whale's eyes, mouth... the barnacles on its back|website=Telegraph.co.uk|date=2005-12-22|year=2005|url=http://www.telegraph.co.uk/health/3334755/We-could-see-the-whales-eyes-mouth...-the-barnacles-on-its-back.html|ref=harv|accessdate="
        self.assertIn(e1, o.ref)
        self.assertIn(e2, o.cite)


class DilyMirrorTest(unittest.TestCase):

    def test_dmr1(self):
        """no authors"""
        i = 'http://www.mirror.co.uk/news/uk-news/whale-doomed-to-die-557471'
        o = urls.Citation(i)
        e1 = u'{{sfn|Mirror.co.uk|2005}}'
        e2 = u'* {{cite web|last=Mirror.co.uk|first=|title=WHALE DOOMED TO DIE|website=mirror|date=2005-09-15|year=2005|url=http://www.mirror.co.uk/news/uk-news/whale-doomed-to-die-557471|ref=harv|accessdate='
        self.assertIn(e1, o.ref)
        self.assertIn(e2, o.cite)


class DilyMailTest(unittest.TestCase):

    def test_dm1(self):
        """4 authors"""
        i = 'http://www.dailymail.co.uk/news/article-2633025/London-cleric-convicted-NYC-terrorism-trial.html'
        o = urls.Citation(i)
        e1 = u'{{sfn|Malm|Witheridge|Drury|Bates|2014}}'
        e2 = u'* {{cite web|last=Malm|first=Sara|last2=Witheridge|first2=Annette|last3=Drury|first3=Ian|last4=Bates|first4=Daniel|title=Hate preacher Abu Hamza GUILTY of setting up US terror training camps|website=Mail Online|date=2014-05-20|year=2014|url=http://www.dailymail.co.uk/news/article-2633025/London-cleric-convicted-NYC-terrorism-trial.html|ref=harv|accessdate='
        self.assertIn(e1, o.ref)
        self.assertIn(e2, o.cite)
        

class BbcTest(unittest.TestCase):

    def test_bbc1(self):
        """no authors"""
        i = 'https://www.bbc.com/news/world-asia-27653361'
        o = urls.Citation(i)
        e = u"* {{cite web|title=US 'received Qatar assurances' on Afghan prisoner deal|website=BBC News|date=2014-06-01|year=2014|url=http://www.bbc.com/news/world-asia-27653361|ref={{sfnref|BBC News|2014}}|accessdate="
        self.assertIn(e, o.cite)

    def test_bbc2(self):
        """1 author"""
        i = 'https://www.bbc.com/news/science-environment-23814524'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Gage|first=Suzi|title=Sea otter return boosts ailing seagrass in California|website=BBC News|date=2013-08-26|year=2013|url=http://www.bbc.com/news/science-environment-23814524|ref=harv|accessdate='
        self.assertIn(e, o.cite)

    def test_bbc3(self):
        """1 author"""
        i = 'https://www.bbc.com/news/science-environment-23814524'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Gage|first=Suzi|title=Sea otter return boosts ailing seagrass in California|website=BBC News|date=2013-08-26|year=2013|url=http://www.bbc.com/news/science-environment-23814524|ref=harv|accessdate='
        self.assertIn(e, o.cite)
        
    def test_bbc4(self):
        """news.bbc.co.uk, 1 author"""
        i = 'http://news.bbc.co.uk/2/hi/programmes/newsnight/5178122.stm'
        o = urls.Citation(i)
        e = u"* {{cite web|last=Jones|first=Meirion|title=Malaria advice 'risks lives'|website=BBC NEWS|date=2006-07-13|year=2006|url=http://news.bbc.co.uk/2/hi/programmes/newsnight/5178122.stm|ref=harv|accessdate="
        self.assertIn(e, o.cite)

        
class NytTest(unittest.TestCase):

    def test_nyt1(self):
        """newstyle, 1 author"""
        i = 'http://www.nytimes.com/2014/05/30/business/international/on-the-internet-the-right-to-forget-vs-the-right-to-know.html?hp&_r=0'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Hakim|first=Danny|title=Right to Be Forgotten? Not That Easy|website=The New York Times|date=2014-05-29|year=2014|url=http://www.nytimes.com/2014/05/30/business/international/on-the-internet-the-right-to-forget-vs-the-right-to-know.html|ref=harv|accessdate='
        self.assertIn(e, o.cite)

    def test_nyt2(self):
        """newstyle, 2 authors"""
        i = 'http://www.nytimes.com/2014/05/31/sports/basketball/steven-a-ballmers-2-billion-play-for-clippers-is-a-big-bet-on-the-nba.html?hp'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Belson|first=Ken|last2=Sandomir|first2=Richard|title=$2 Billion for Clippers? In Time, It May Be a Steal for Steve Ballmer|website=The New York Times|date=2014-05-30|year=2014|url=http://www.nytimes.com/2014/05/31/sports/basketball/steven-a-ballmers-2-billion-play-for-clippers-is-a-big-bet-on-the-nba.html|ref=harv|accessdate='
        self.assertIn(e, o.cite)

    def test_nyt3(self):
        """oldstyle, 1 author"""
        i = 'http://www.nytimes.com/2007/12/25/world/africa/25kenya.html'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Gettleman|first=Jeffrey|title=Election Rules Complicate Kenya Race|website=The New York Times|date=2007-12-25|year=2007|url=http://www.nytimes.com/2007/12/25/world/africa/25kenya.html|ref=harv|accessdate='
        self.assertIn(e, o.cite)

    def test_nyt4(self):
        """newstyle, 2 authors, only byline"""
        i = 'http://dealbook.nytimes.com/2014/05/30/insider-trading-inquiry-includes-mickelson-and-icahn/'
        o = urls.Citation(i)
        e = u'* {{cite web|last=Goldstein|first=Matthew|last2=Protess|first2=Ben|title=Investor, Bettor, Golfer: Insider Trading Inquiry Includes Mickelson, Icahn and William T. Walters|website=DealBook|date=2014-05-30|year=2014|url=http://dealbook.nytimes.com/2014/05/30/insider-trading-inquiry-includes-mickelson-and-icahn/|ref=harv|accessdate='
        self.assertIn(e, o.cite)

    def test_nyt5(self):
        """special case for date format (not in usual meta tags)"""
        i = 'http://www.nytimes.com/2007/06/13/world/americas/13iht-whale.1.6123654.html'
        o = urls.Citation(i)
        e = u'* {{cite web|title=19th-century harpoon gives clue on whales|website=The New York Times|date=2007-06-13|year=2007|url=http://www.nytimes.com/2007/06/13/world/americas/13iht-whale.1.6123654.html|ref={{sfnref|The New York Times|2007}}|accessdate='
        self.assertIn(e, o.cite)

        
class Ensani(unittest.TestCase):

    def test_ens(self):
        """Get title by hometitle comparison."""
        i = 'http://www.ensani.ir/fa/content/326173/default.aspx'
        o = urls.Citation(i)
        e = u'* {{cite web|last=جلیلیان|first=شهرام|last2=نیا|first2=امیر علی|title=ورود کاسی ها به میان رودان و پیامدهای آن|website=پرتال جامع علوم انسانی|date=2014-05-20|year=2014|url=http://www.ensani.ir/fa/content/326173/default.aspx|ref=harv|accessdate='
        self.assertIn(e, o.cite)
        

if __name__ == '__main__':
    unittest.main()