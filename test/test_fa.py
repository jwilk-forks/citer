#! /usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase, main

import config; config.LANG = 'fa'
# load .tests_cache
# noinspection PyUnresolvedReferences
import test

from lib.ketabir import ketabir_sfn_cit_ref
from lib.doi import doi_sfn_cit_ref
from lib.googlebooks import googlebooks_sfn_cit_ref
from lib.isbn_oclc import isbn_sfn_cit_ref
from lib.noormags import noormags_sfn_cit_ref
from lib.noorlib import noorlib_sfn_cit_ref
from lib.pubmed import pmid_sfn_cit_ref


class KetabirTest(TestCase):

    def test_ab1(self):
        """authors = 1, translators = 2, otheo = 1, isbn13"""
        self.assertEqual(
            '* {{یادکرد کتاب | نام خانوادگی=لانسکی |'
            ' نام=ویکی | ترجمه=فیروزه دالکی و مژگان امیرفروغی |'
            ' دیگران=کی وایت (تصويرگر) |'
            ' عنوان=101 راه برای اینکه پدر بهتری باشید |'
            ' ناشر=پیک ادبیات | مکان=تهران - تهران |'
            ' سال=۱۳۸۶ | ماه=۰۶ | شابک=978-964-8165-81-4 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1323394')[1])

    def test_ab2(self):
        """authors = 3, translators = 2, otheo = 0, isbn13"""
        self.assertEqual(
            '* {{یادکرد کتاب |'
            ' نام خانوادگی=کرسول | نام=جان | نام خانوادگی۲=پلانو‌کلارک |'
            ' نام۲=ویکی | ترجمه=عباس زارعی و محسن نیازی |'
            ' عنوان=روش‌های تحقیق تلفیقی |'
            ' ناشر=ثامن‌ الحجج‌(ع) | مکان=تهران - تهران | جلد=۱ |'
            ' سال=۱۳۸۷ | ماه=۰۳ | شابک=978-964-2823-35-2 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1369975')[1])

    def test_ab3(self):
        """authors = 2, translators = 0, otheo = 4, isbn13"""
        self.assertEqual(
            '* {{یادکرد کتاب | نام خانوادگی=فخررحیمی |'
            ' نام=علیرضا | نام خانوادگی۲=فخررحیمی |'
            ' نام۲=الهام | دیگران=آرش نادرپور'
            ' (مقدمه)، وحید شهبازیان (مقدمه)، رضا مقدم (مقدمه) '
            'و امیر جابری (مقدمه) | عنوان=آموزش گام'
            ' به گام پیکربندی مسیریابهای میکروتیک: آمادگی آزمون MTCNA '
            '| ناشر=نشرگستر | مکان=تهران - تهران |'
            ' سال=۱۳۹۱ | ماه=۰۳ | شابک=978-600-5883-43-5 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1676357')[1])

    def test_ab4(self):
        """authors = 3, translators = 0, otheo = 0, isbn13"""
        self.assertEqual(
            '* {{یادکرد کتاب | نام خانوادگی=کریمی |'
            ' نام=نجمه | نام خانوادگی۲=یزدخواستی |'
            ' نام۲=فروغ | نام خانوادگی۳=مختاری |'
            ' نام۳=صفورا | عنوان=11 سپتامبر ... آرماگدون |'
            ' ناشر=حدیث راه عشق | مکان=اصفهان - اصفهان |'
            ' سال=۱۳۸۶ | ماه=۰۶ | شابک=978-964-95633-4-3 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1324978')[1])

    def test_ab5(self):
        """Year is interesting here."""
        self.assertEqual(
            '* {{یادکرد کتاب | نام خانوادگی=یوسف‌نژاد |'
            ' نام=یوسف‌علی | عنوان=فراهنجاری در'
            ' مثنوی‌سرایی: بررسی قالب غزل - مثنوی در ادب فارسی |'
            ' ناشر=هنر رسانه اردی‌بهشت | مکان=تهران - تهران |'
            ' سال=۱۳۸۸ | ماه=۰۲ | شابک=978-964-2656-34-9 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1430801')[1])

    def test_ab6(self):
        """Month and year detection."""
        self.assertEqual(
            '* {{یادکرد کتاب |'
            ' نام خانوادگی=مونس | نام=حسین | ترجمه=حمیدرضا شیخی |'
            ' عنوان=تاریخ و تمدن مغرب | ناشر=سازمان‌ مطالعه '
            '‌و تدوین‌ کتب‌ علوم ‌انسانی ‌دانشگاهها (سمت) |'
            ' مکان=خراسان رضوی - مشهد | جلد=۱ |'
            ' سال=۱۳۹۰ | ماه=۱۱ | شابک=978-964-530-036-2 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1643445')[1])

    def test_ab7(self):
        """1 Editor."""
        self.assertEqual(
            '* {{یادکرد کتاب | نام خانوادگی=دیماتیو | نام=ام.رابین |'
            ' نام خانوادگی ویراستار=جباری | نام ویراستار=کریم |'
            ' ترجمه=محمد کاویانی | دیگران=کیانوش هاشمیان (زيرنظر) |'
            ' عنوان=روانشناسی سلامت به ضمیمه نگرشی بر منابع اسلامی |'
            ' ناشر=سازمان‌ مطالعه ‌و تدوین‌ کتب‌ علوم'
            ' ‌انسانی ‌دانشگاهها (سمت) | مکان=تهران - تهران | جلد=۱ |'
            ' سال=۱۳۸۸ | ماه=۰۸ | شابک=978-964-459-398-7 | زبان=fa}}',
            ketabir_sfn_cit_ref(
                'http://www.ketab.ir/bookview.aspx?bookid=1459372')[1])


class GooglebookTest(TestCase):

    def test_gb1(self):
        self.assertIn(
            '* {{یادکرد کتاب | نام خانوادگی=Arms |'
            ' نام=W.Y. | عنوان=Digital Libraries | ناشر=MIT Press |'
            ' سری=Digital libraries and electronic publishing |'
            ' سال=2001 | شابک=978-0-262-26134-0 |'
            ' پیوند=https://books.google.com/books?id=pzmt3pcBuGYC&pg=PR11 |'
            ' زبان=en | تاریخ بازبینی=',
            googlebooks_sfn_cit_ref(
                'http://books.google.com/books?'
                'id=pzmt3pcBuGYC&pg=PR11&lpg=PP1&dq=digital+library'
            )[1],
        )

    def test_gb2(self):
        """a book with more than 4 authors (10 authors)"""
        o = googlebooks_sfn_cit_ref(
            'http://books.google.com/books?id='
            'U46IzqYLZvAC&pg=PT57#v=onepage&q&f=false')
        self.assertIn(
            '&lt;ref&gt;'
            '{{پک | Anderson | DeBolt | Featherstone | Gunther | 2010'
            ' | ک=InterACT with Web Standards: A'
            ' holistic approach to web design | زبان=en | ص=57}}'
            '\u200f&lt;/ref&gt;',
            o[0],
        )
        self.assertIn(
            '* {{یادکرد کتاب |'
            ' نام خانوادگی=Anderson |'
            ' نام=E. |'
            ' نام خانوادگی۲=DeBolt | نام۲=V. |'
            ' نام خانوادگی۳=Featherstone |'
            ' نام۳=D. | نام خانوادگی۴=Gunther |'
            ' نام۴=L. |'
            ' نام خانوادگی۵=Jacobs | نام۵=D.R. | نام خانوادگی۶=Mills |'
            ' نام۶=C. |'
            ' نام خانوادگی۷=Schmitt | نام۷=C. | نام خانوادگی۸=Sims |'
            ' نام۸=G. |'
            ' نام خانوادگی۹=Walter | نام۹=A. |'
            ' نام خانوادگی۱۰=Jensen-Inman |'
            ' نام۱۰=L. |'
            ' عنوان=InterACT with Web Standards:'
            ' A holistic approach to web design |'
            ' ناشر=Pearson Education |'
            ' سری=Voices That Matter | سال=2010 |'
            ' شابک=978-0-13-270490-8 |'
            ' پیوند=https://books.google.com/books?id=U46IzqYLZvAC&pg=PT57 |'
            ' زبان=en |'
            ' تاریخ بازبینی=',
            o[1],
        )

    def test_gb3(self):
        """Non-ascii characters in title"""
        o = googlebooks_sfn_cit_ref(
            'http://books.google.com/books?'
            'id=icMEAAAAQBAJ&pg=PA588&dq=%22a+Delimiter+is%22&hl='
            'en&sa=X&ei=oNKSUrKeDovItAbO_4CoBA&ved=0CC4Q6AEwAA#v='
            'onepage&q=%22a%20Delimiter%20is%22&f=false'
        )
        self.assertIn(
            '&lt;ref&gt;'
            '{{پک | Farrell | 2009 '
            '| ک=Microsoft Visual C# 2008 Comprehensive: '
            'An Introduction to Object-Oriented Programming |'
            ' زبان=en | ص=588}}'
            '\u200f&lt;/ref&gt;',
            o[0],
        )
        self.assertIn(
            '* {{یادکرد کتاب | نام خانوادگی=Farrell |'
            ' نام=J. | عنوان=Microsoft Visual C# 2008 Comprehensive: '
            'An Introduction to Object-Oriented Programming |'
            ' ناشر=Cengage Learning | سال=2009 | شابک=978-1-111-78619-9 |'
            ' پیوند=https://books.google.com/books?id=icMEAAAAQBAJ&pg=PA588 |'
            ' زبان=en | تاریخ بازبینی=',
            o[1],
        )

    def test_gb4(self):
        """Non-ascii characters in author's name."""
        o = googlebooks_sfn_cit_ref(
            'http://books.google.com/books?id='
            'i8nZjjo_9ikC&pg=PA229&dq=%22legal+translation+is%22&hl=en&sa='
            'X&ei=hEuYUr_mOsnKswb49oDQCA&ved=0CC4Q6AEwAA#v=onepage&q='
            '%22legal%20translation%20is%22&f=false'
        )
        self.assertIn(
            '&lt;ref&gt;{{پک | Šarčević | 1997 '
            '| ک=New Approach to Legal Translation |'
            ' زبان=en | ص=229}}'
            '\u200f&lt;/ref&gt;',
            o[0],
        )
        self.assertIn(
            '* {{یادکرد کتاب | نام خانوادگی=Šarčević |'
            ' نام=S. |'
            ' عنوان=New Approach to Legal Translation |'
            ' ناشر=Springer Netherlands |'
            ' سال=1997 |'
            ' شابک=978-90-411-0401-4 |'
            ' پیوند=https://books.google.com/books?id=i8nZjjo_9ikC&pg=PA229 |'
            ' زبان=en |'
            ' تاریخ بازبینی=',
            o[1],
        )


class NoormagsTest(TestCase):

    def test_nm2(self):
        self.assertIn(
            '* {{یادکرد ژورنال |'
            ' عنوان=زندگی نامه علمی دکتر کاووس حسن لی |'
            ' ژورنال=شعر | شماره=62 | سال=1387 | صفحه=17–19 |'
            ' پیوند=https://www.noormags.ir/view/fa/articlepage/454096 |'
            ' زبان=fa | تاریخ بازبینی=',
            noormags_sfn_cit_ref(
                'http://www.noormags.com/view/fa/ArticlePage/454096'
            )[1],
        )


class NoorlibTest(TestCase):

    def test_nl1(self):
        i = 'http://www.noorlib.ir/View/fa/Book/BookView/Image/3232'
        o = noorlib_sfn_cit_ref(i)
        e = (
            '* {{یادکرد کتاب '
            '| نام خانوادگی=ابن اثیر '
            '| نام=علی بن محمد '
            '| عنوان=الكامل في التاريخ '
            '| ناشر=دار صادر '
            '| مکان=بیروت - لبنان '
            '| سری=الكامل في التاريخ '
            '| جلد=13 '
            '| پیوند=https://www.noorlib.ir/View/fa/Book/BookView/Image/3232 '
            '| زبان=عربی '
            '| تاریخ بازبینی='
        )
        self.assertIn(e, o[1])


class DoiTest(TestCase):

    def test_di1(self):
        self.maxDiff = None
        # Note: Language detection is wrong, it should be en
        self.assertIn(
            "* {{یادکرد ژورنال | نام خانوادگی=Atkins |"
            " نام=Joshua H. | نام خانوادگی۲=Gershell | نام۲=Leland J. |"
            " عنوان=Selective anticancer drugs |"
            " ژورنال=Nature Reviews Drug Discovery |"
            " ناشر=Springer Nature | جلد=1 | شماره=7 |"
            " سال=2002 | ماه=7 | issn=1474-1776 | doi=10.1038/nrd842 |"
            " صفحه=491–492 |"
            " زبان=da}}",
            doi_sfn_cit_ref('http://dx.doi.org/10.1038/nrd842')[1],
        )


class IsbnTest(TestCase):

    def test_is1(self):
        """not found in ketabir"""
        self.assertIn(
            '* {{یادکرد کتاب | نام خانوادگی=Adkins | نام=Roy |'
            ' عنوان=The war for all the oceans : '
            'from Nelson at the Nile to Napoleon at Waterloo |'
            ' ناشر=Abacus | مکان=London | سال=2007 |'
            ' شابک=978-0-349-11916-8 '
            '| oclc=137313052 '
            '| زبان=en}}',
            isbn_sfn_cit_ref('9780349119168', pure=True)[1])

    def test_is2(self):
        """not found in ottobib"""
        self.assertEqual(
            '* {{یادکرد کتاب | دیگران=بدیل‌بن‌علی خاقانی'
            ' (شاعر)، جهانگیر منصور (به‌اهتمام) '
            'و محمدحسن فروزانفر (مقدمه) |'
            ' عنوان=دیوان خاقانی شروانی |'
            ' ناشر=موسسه انتشارات نگاه | مکان=تهران - تهران |'
            ' سال=۱۳۹۶ | ماه=۰۵ | شابک=978-964-6736-71-9 | زبان=fa}}',
            isbn_sfn_cit_ref('978-964-6736-71-9', pure=True)[1]
        )

    def test_is3(self):
        """exists in both"""
        self.assertEqual(
            '* {{یادکرد کتاب |'
            ' دیگران=سهراب سپهری (شاعر) و سحر معصومی (به‌اهتمام) |'
            ' عنوان=راز گل سرخ: نقد و گزیده شعرهای سهراب سپهری |'
            ' ناشر=موسسه انتشارات نگاه | مکان=تهران - تهران |'
            ' سال=۱۳۸۱ | ماه=۰۶ | شابک=964-6736-34-3 | oclc=53446327 '
            '| زبان=fa}}',
            isbn_sfn_cit_ref('964-6736-34-3 ')[1],
        )

    def test_is4(self):
        """unpure isbn10"""
        self.assertEqual(
            '* {{یادکرد کتاب | نام خانوادگی=حافظ |'
            ' نام=شمس‌الدین‌محمد | دیگران=رضا نظرزاده (به‌اهتمام) |'
            ' عنوان=دیوان کامل حافظ همراه با فالنامه |'
            ' ناشر=دیوان | مکان=قم - قم |'
            ' سال=۱۳۸۵ | ماه=۰۹ | شابک=964-92962-6-3 | زبان=fa}}',
            isbn_sfn_cit_ref('choghondar 964-92962-6-3 شلغم')[1]
        )

    def test_2letter_langcode(self):
        """Test that 3letter language code is converted to a 2-letter one."""
        # Todo: The fawiki template mixes persian and chinese characters...
        self.assertIn(
            '* {{یادکرد ژورنال | نام خانوادگی=Huang | نام=Y '
            '| نام خانوادگی۲=Lu | نام۲=J | نام خانوادگی۳=Shen '
            '| نام۳=Y | نام خانوادگی۴=Lu | نام۴=J '
            '| عنوان=&amp;#91;The protective effects of total flavonoids from '
            'Lycium Barbarum L. on lipid peroxidation of liver mitochondria '
            'and red blood cell in rats&amp;#93;. '
            '| ژورنال=Wei sheng yan jiu = Journal of hygiene research '
            '| جلد=28 | شماره=2 | تاریخ=1999-03-30 | issn=1000-8020 '
            '| pmid=11938998 | صفحه=115–6 | زبان=zh}}',
            pmid_sfn_cit_ref('11938998')[1],
        )


if __name__ == '__main__':
    main()
