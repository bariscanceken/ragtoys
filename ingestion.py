from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from bs4 import BeautifulSoup
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
path_text = os.path.join(base_dir, 'tabulates.txt')

load_dotenv()

urls = [# ok "https://www.ktu.edu.tr/oidb",
        "https://www.ktu.edu.tr/oidb/sikcasorulansorular",
        "http://www.mevzuat.gov.tr/Metin.Aspx?MevzuatKod=8.5.23952&MevzuatIliski=0&sourceXmlSearch=karadeniz",
        "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=42551&MevzuatTur=8&MevzuatTertip=5",
        "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=39819&MevzuatTur=8&MevzuatTertip=5",
        "https://www.resmigazete.gov.tr/eskiler/2012/10/20121011-6.htm",
        "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=34564&MevzuatTur=8&MevzuatTertip=5",
        "https://www.mevzuat.gov.tr/Metin.Aspx?MevzuatKod=8.5.33904&MevzuatIliski=0&sourceXmlSearch=",
        "http://www.mevzuat.gov.tr/Metin.Aspx?MevzuatKod=8.5.16680&MevzuatIliski=0&sourceXmlSearch=",
        "http://www.mevzuat.gov.tr/Metin.Aspx?MevzuatKod=7.5.13948&MevzuatIliski=0&sourceXmlSearch=yatay%20ge%C3%A7i%C5%9F",
        "http://www.mevzuat.gov.tr/Metin.Aspx?MevzuatKod=7.5.8315&MevzuatIliski=0&sourceXmlSearch=MESLEK%20Y%DCKSEKOKULLARI%20VE%20A%C7IK%D6%D0RET%DDM%20%D6N%20L%DDSANS%20PROGRAMLARI",
#        "https://kms.kaysis.gov.tr/Home/Goster/190840",
#        "https://kms.kaysis.gov.tr/Home/Goster/172996",
#        "https://kms.kaysis.gov.tr/Home/Goster/62675",
#        "https://kms.kaysis.gov.tr/Home/Goster/62629",
        "http://www.ktu.edu.tr/dosyalar/oidb_LmmYS.pdf"
#        "https://kms.kaysis.gov.tr/Home/Goster/172995",
#        "https://www.ktu.edu.tr/dosyalar/08_00_00_82343.pdf",
#        "https://kms.kaysis.gov.tr/Home/Goster/62683",
#        "https://kms.kaysis.gov.tr/Home/Goster/173003",
#        "https://kms.kaysis.gov.tr/Home/Goster/173002",
#        "https://kms.kaysis.gov.tr/Home/Goster/173004",
#        "https://kms.kaysis.gov.tr/Home/Goster/172998",
#        "https://kms.kaysis.gov.tr/Home/Goster/183753",
#        "https://www.ktu.edu.tr/dosyalar/oidb_396fb.pdf",
#        "https://www.ktu.edu.tr/dosyalar/sbe_b44e6.pdf" ,
#        "https://kms.kaysis.gov.tr/Home/Goster/172994" ,
        "https://www.ktu.edu.tr/oidb/iletisim" ,
        "https://www.ktu.edu.tr/oidb/hakkimizda" ,
        "https://www.ktu.edu.tr/oidb/hakkimizda/tab1",
        "https://www.ktu.edu.tr/oidb/personel" ,
        "https://www.ktu.edu.tr/oidb/hakkimizda/tab2",
        "https://www.ktu.edu.tr/oidb/birimlerimiz",
        "https://www.ktu.edu.tr/oidb/komisyonlar" ,
        "https://www.ktu.edu.tr/kvkb/aydinlatmametni",
        "https://www.ktu.edu.tr/oidb/form/qdEDpvjn",
        "https://www.ktu.edu.tr/oidb/akademiktakvim"
        "https://www.ktu.edu.tr/tr/katalog",
        "https://www.ktu.edu.tr/oidb/akademik-birimler",
        "https://www.ktu.edu.tr/oidb/programlarimiz",
        "https://www.ktu.edu.tr/yonetim/akreditasyonvebelgelendirme",
        "https://www.ktu.edu.tr/oidb/ciftanadalyandal",
        "https://www.ktu.edu.tr/oidb/engelsiz-birim",
        "https://dy2.ktu.edu.tr/donemDersleri/",
        "https://www.ktu.edu.tr/kariyer",
#        #"https://www.ktu.edu.tr/dosyalar/oidb_62d5e.pdf",
        "https://www.ktu.edu.tr/sks/ogrencikulupleri",
        "https://www.ktu.edu.tr/omer",
        "https://www.ktu.edu.tr/oidb/pedagojikformasyon",
        "https://www.ktu.edu.tr/sem",
        "https://www.ktu.edu.tr/oidb/sikcasorulansorular",
        "https://www.ktu.edu.tr/usec",
        "https://www.ktu.edu.tr/uzem",
        "https://www.ktu.edu.tr/oidb/yataygecis",
        "https://www.ktu.edu.tr/oidb/bizeyazin",
        "https://bys.ktu.edu.tr/BYS/bys.aspx?giris=3",
        "https://www.ktu.edu.tr/mezun/diplomansanagelsin",
        "https://roundcube.ktu.edu.tr/hesk/",
        "https://dersprogrami.ktu.edu.tr/",
        "https://derseyazilim.ktu.edu.tr/",
        "https://harc.ktu.edu.tr/",
        "https://www.ktu.edu.tr/bilgiislem/eduroam",
        "https://kampuskart.ktu.edu.tr/User/Login",
        "https://www.ktu.edu.tr/oidb/form/ogrenci-isleri-daire-baskanligi-ogrenci-memnuniyet-anketi-2025",
        "https://www.ktu.edu.tr/sks/iskur-genclik-programi",
        "https://www.ktu.edu.tr/oidb/mezun-bilgi-sistemi",
#        #"https://www.ktu.edu.tr/dosyalar/genelsekreterlik_c9137.pdf",
        "https://www.ktu.edu.tr/sks/staj",
        "https://uek.ktu.edu.tr/ogrenci.html",
        "https://www.ktu.edu.tr/oidb/uluslararasiogrenci",
#        #"https://www.ktu.edu.tr/dosyalar/oisa_eW0ne.pdf",
        "https://aday.ktu.edu.tr/",
        "https://yokatlas.yok.gov.tr/",
        "https://www.ktu.edu.tr/oidb/diger-universite-ve-kurumlarin-duyurulari",
        "https://mbs.ktu.edu.tr/Login/Index?ReturnUrl=%2F",
        "https://www.ktu.edu.tr/mezun/diplomansanagelsin",
        "https://www.ktu.edu.tr/oidb/tabanpuanlaristatistik",
        "https://www.ktu.edu.tr/oidb/yillaragoreogrencisayilari",
        "https://www.ktu.edu.tr/oidb/mezunogrencisayilari",
        "https://www.ktu.edu.tr/oidb/yksdolulukoranlari",
        "https://www.ktu.edu.tr/dio",
        "https://www.ktu.edu.tr/digk",
        "https://www.ktu.edu.tr/mezun",
        "https://www.ktu.edu.tr/uoik",
        "https://www.ktu.edu.tr/usec",
        "https://www.ktu.edu.tr/ylsy",
        
]

docs = [WebBaseLoader(url, requests_kwargs={"verify": False, "headers": {"User-Agent": "Mozilla/5.0"}}).load() for url in urls]

docs_list = [
    BeautifulSoup(doc.page_content, "html.parser").get_text(separator=" ", strip=True).split()
    for sublist in docs
    for doc in sublist
]

if __name__ == "__main__":
    for text in docs_list:
        with open(path_text, 'a', encoding='utf-8') as dosya:
            dosya.write(" ".join(text) + "\n")