#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from nfce import html
from pychromepdf import ChromePDF
import os
import sys
import json
import xmltodict

BASE_DIR = os.getcwd()

if sys.platform.startswith('win32'):
    system = 'Windows'
    PATH_TO_CHROME_EXE = r'C:\Program~1\Google\Chrome\Application\chrome.exe'
elif sys.platform.startswith('linux'):
    system = 'Linux'
    PATH_TO_CHROME_EXE = '/usr/bin/google-chrome-stable'


class Template(object):

    def __init__(self, data):
        self.data = data
        self.itens_total = None

    def logo(self):
        return f'{BASE_DIR}/images/nf-e-nota-fiscal-eletronica.png'

    def emit(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["emit"]

    def itens(self):
        data = self.data["nfeProc"]["NFe"]["infNFe"]["det"]
        list_itens = []
        if isinstance(data, list):
            self.itens_total = len(data)
            for item in data:
                dict_itens = self.mount_dict(item)
                list_itens.append(dict_itens)
        else:
            self.itens_total = 1
            list_itens.append(self.mount_dict(data))
        return list_itens

    def info_nfe(self):
        return self.data["nfeProc"]["protNFe"]["infProt"]

    def info_itens(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]

    def fiscal(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["ide"]

    def impost(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"]

    def protocol(self):
        return self.data["nfeProc"]["protNFe"]["infProt"]["nProt"]

    def codes(self):
        return self.data["nfeProc"]["NFe"]["infNFeSupl"]

    def payments(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"]

    def additional_info(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["infAdic"]

    def footer(self):
        return {}

    def mount_dict(self, item):
        dict_itens = {}
        dict_itens['code'] = item['prod']['cProd']
        dict_itens['description'] = item['prod']['xProd']
        dict_itens['quantity'] = item['prod']['qCom']
        dict_itens['unity'] = item['prod']['uCom']
        dict_itens['price'] = item['prod']['vUnTrib']
        dict_itens['total_price'] = item['prod']['vProd']
        return dict_itens


def get_data(file_path):
    with open(file_path, 'rb') as xml:
        data = json.dumps(xmltodict.parse(xml))
    return json.loads(data)


def mount_table(itens):
    new_itens = []

    table_itens = """
        <tr>
          <td>%(code)s</td>
          <td class="tdRight">%(description)s</td>
          <td>%(quantity)s</td>
          <td class="tRight">%(unity)s</td>
          <td class="tRight">%(price)s</td>
          <td class="tRight">%(total_price)s</td>
        </tr>               
    """

    for item in itens:
        new_itens.append(table_itens % item)
    return ''.join(new_itens)


def initialize(filename=None):
    dict_data = get_data(filename)
    result = False
    #print(dict_data)

    tp = Template(dict_data)

    # print(tp.info_nfe())
    # print(tp.payments())
    # print(tp.fiscal())
    # print(tp.codes())
    # print(tp.impost())
    # print(tp.itens())
    # print(tp.info_itens())
    # print(tp.emit())
    # print(tp.footer())
    # print(tp.logo())

    file_name = tp.info_nfe()["chNFe"]

    """
    items = [
        {
            "code": '00002',
            "description": 'produto teste',
            "quantity": '1',
            "unity": 'PC',
            "price": '10.00',
            "total_price": '10.00'
        },
        {
            "code": '00003',
            "description": 'produto teste2',
            "quantity": '2',
            "unity": 'KG',
            "price": '13.00',
            "total_price": '26.00'
        }
    ]    """

    url_logo = f'{BASE_DIR}/images/nf-e-nota-fiscal-eletronica.png'
    payment_type = "Dinheiro" if tp.payments()["tPag"] == "01" else "Crédito"

    dict_details = {"url_logo": url_logo,
                    "nl_company_cnpj_cpf": tp.emit()["CNPJ"],
                    "ds_company_issuer_name": tp.emit()["xNome"],
                    "ds_company_complement": tp.emit()["enderEmit"]["xCpl"],
                    "ds_company_address": tp.emit()["enderEmit"]["xLgr"],
                    "ds_company_neighborhood": tp.emit()["enderEmit"]["xBairro"],
                    "ds_company_number": tp.emit()["enderEmit"]["nro"],
                    "ds_company_city_name": tp.emit()["enderEmit"]["xMun"],
                    "ds_company_uf": tp.emit()["enderEmit"]["UF"],
                    "ds_company_zip_code": tp.emit()["enderEmit"]["CEP"],
                    "ds_company_fone": tp.emit()["enderEmit"]["fone"],
                    "table_items": mount_table(tp.itens()),
                    # "qtd_unit_itens": dict_data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["qCom"],
                    "qtd_itens": tp.itens_total,  # dict_data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["indTot"],
                    "tot_product": tp.impost()["vProd"],
                    "vl_discount": tp.impost()["vDesc"],
                    "vl_shipping": tp.impost()["vFrete"],
                    "vl_total": tp.impost()["vNF"],
                    "payment_forms": payment_type,
                    "payment_return_forms": tp.payments()["vPag"],
                    "url_sefaz": tp.codes()["urlChave"],
                    "ds_danfe": '',
                    "consumer": '',
                    "nl_invoice": tp.fiscal()["cNF"],
                    "ds_invoice_serie": tp.fiscal()["serie"],
                    "dt_invoice_issue": tp.fiscal()["dhEmi"],
                    "ds_protocol": tp.info_nfe()["nProt"],
                    "dt_hr_invoice_issue": tp.fiscal()["dhEmi"],
                    "QRCODE": tp.codes()["qrCode"],
                    # "QRCODE": 'https://generator.qrcodefacil.com/qrcodes/static-eee4e1f2a0e3cd369c7053a88a745622.svg',
                    "state_fiscal_message": '',
                    "approximate_tax": '',
                    "additional_information": tp.additional_info()["infCpl"],
                    }

    # print(dict_details)

    html_bytestring = html % dict_details

    with open(f'templates/{file_name}.html', 'w') as html_file:
        html_file.write(html % dict_details)

    cpdf = ChromePDF(PATH_TO_CHROME_EXE, sandbox=False)

    with open(f'{BASE_DIR}/pdf/{file_name}.pdf', 'w') as output_file:

        if system == 'Windows':
            if cpdf.page_to_pdf(f'{BASE_DIR}/{html_file.name}', output_file):
                result = True
        else:
            if cpdf.html_to_pdf(html_bytestring, output_file):
                result = True

        if not result:
            print("Error generating pdf")
            return False

        print("Successfully generated the pdf: {}".format(output_file.name))
        # os.system(f'cat {output_file.name} | lpr -P POS80')


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        file_path = args[1]
        initialize(file_path)
