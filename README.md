# _xml2pdf_

Simple script convert xml to pdf online from https://www.fsist.com.br/.

```
from xml2pdf import FSistApi

fs = FSistApi()
data = fs.upload_xml('docs/35080599999090910270550010000000015180051273-nfe.xml', soup_cnf=True)
fs.get_pdf()

```