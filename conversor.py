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

    @staticmethod
    def logo():
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
        return self.data["nfeProc"]["NFe"]["infNFe"]["pag"]

    def additional_info(self):
        return self.data["nfeProc"]["NFe"]["infNFe"]["infAdic"]

    @staticmethod
    def footer():
        return {}

    @staticmethod
    def mount_dict(item):
        dict_itens = {'code': item['prod']['cProd'], 'description': item['prod']['xProd'],
                      'quantity': item['prod']['qCom'], 'unity': item['prod']['uCom'], 'price': item['prod']['vUnTrib'],
                      'total_price': item['prod']['vProd']}
        return dict_itens


def get_data(filepath):
    with open(filepath, 'rb') as xml:
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


def get_card(banner):
    cards = {
        '01': 'Visa',
        '02': 'MasterCard',
        '03': 'American Express',
        '04': 'SoroCred',
        '05': 'Diners',
        '06': 'Elo',
        '07': 'HiperCard',
        '08': 'Aura',
        '09': 'Cabal',
        '10': 'Alelo',
        '11': 'BanesCard',
        '12': 'CalCard',
        '13': 'CredZ',
        '14': 'Discover',
        '15': 'GoodCard',
        '16': 'Gre3nCard',
        '17': 'Hiper',
        '18': 'JcB',
        '19': 'Mais',
        '20': 'MaxVan',
        '21': 'PoliCard',
        '22': 'RedeCompras',
        '23': 'Sodexo',
        '24': 'ValeCard',
        '25': 'VeroCheque',
        '26': 'VR',
        '27': 'Ticket',
        '99': 'Outros'
    }

    return cards.get(banner, 'Outros')


def get_payment_type(pay):
    payments_type = {
        '01': 'Dinheiro',
        '02': 'Cheque',
        '03': 'Cartão de Crédito',
        '04': 'Cartão de Débito',
        '05': 'Crédito Loja',
        '10': 'Vale Alimentação',
        '11': 'Vale Refeição',
        '12': 'Vale Presente',
        '13': 'Vale Combustível',
        '15': 'Boleto Bancário',
        '16': 'Deposito Bancário',
        '17': 'PIX',
        '18': 'Transf/Cart.Digital',
        '19': 'Crédito Virtual'
    }

    return payments_type.get(pay, 'Outros')


def get_payments(payments):
    new_payments = []

    table_payments = """
        <tr>
            <td class="last">
                %(payment_forms)s
            </td>
        </tr>               
    """

    for payment in payments["detPag"]:
        if "card" in payment:
            html_str = f'{get_payment_type(payment["tPag"])} {get_card(payment["card"]["tBand"])}<span class="td-text' \
                       f'-right">{payment["vPag"]}</span> '
        else:
            html_str = f'{get_payment_type(payment["tPag"])}<span class="td-text-right">{payment["vPag"]}</span>'
        new_payments.append(table_payments % {'payment_forms': html_str})

    payment_change = ""
    if payments["vTroco"] != '0,00':
        payment_change = f"""
        <tr>
            <td class="last">
                TROCO :<span class="td-text-right">{payments["vTroco"]}</span>
            </td>
        </tr>
        """

    return ''.join(new_payments) + payment_change


def initialize(filename=None):
    dict_data = get_data(filename)
    result = False

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

    url_logo = f'{BASE_DIR}/images/nf-e-nota-fiscal-eletronica.png'
    payments = tp.payments()

    dict_details = {"url_logo": url_logo,
                    "nl_company_cnpj_cpf": tp.emit()["CNPJ"],
                    "ds_company_issuer_name": tp.emit()["xNome"],
                    "ds_company_complement": tp.emit()["enderEmit"].get("xCpl", ""),
                    "ds_company_address": tp.emit()["enderEmit"]["xLgr"],
                    "ds_company_neighborhood": tp.emit()["enderEmit"]["xBairro"],
                    "ds_company_number": tp.emit()["enderEmit"].get("nro", ""),
                    "ds_company_city_name": tp.emit()["enderEmit"]["xMun"],
                    "ds_company_uf": tp.emit()["enderEmit"]["UF"],
                    "ds_company_zip_code": tp.emit()["enderEmit"]["CEP"],
                    "ds_company_fone": tp.emit()["enderEmit"].get("fone", ""),
                    "table_items": mount_table(tp.itens()),
                    # "qtd_unit_itens": dict_data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["qCom"],
                    "qtd_itens": tp.itens_total,  # dict_data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["indTot"],
                    "tot_product": tp.impost()["vProd"],
                    "vl_discount": tp.impost()["vDesc"],
                    "vl_shipping": tp.impost()["vFrete"],
                    "vl_total": tp.impost()["vNF"],
                    "payments": get_payments(payments),
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
