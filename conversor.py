#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from nfce import html
from pychromepdf import ChromePDF
import os
import json
import xmltodict

BASE_DIR = os.getcwd()
PATH_TO_CHROME_EXE = '/usr/bin/google-chrome-stable'


def get_data(file_path):
    with open(file_path, 'rb') as xml:
        data = json.dumps(xmltodict.parse(xml))
    return json.loads(data)


def mount_table(items):
    new_items = []

    table_items = """
        <tr>
          <td>%(code)s</td>
          <td class="tdRight">%(description)s</td>
          <td>%(quantity)s</td>
          <td class="tRight">%(unity)s</td>
          <td class="tRight">%(price)s</td>
          <td class="tRight">%(total_price)s</td>
        </tr>               
    """

    for item in items:
        new_items.append(table_items % item)

    return ''.join(new_items)


def main():
    dict_data = get_data("docs/32201034971421000181650010000014191914100001-nfce.xml")
    file_name = dict_data["nfeProc"]["protNFe"]["infProt"]["chNFe"]

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
    ]

    url_logo = f'{BASE_DIR}/images/nf-e-nota-fiscal-eletronica.png'
    payment_type = "Dinheiro" if dict_data["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"]["tPag"] == "01" else "Crédito"

    dict_details = {"url_logo": url_logo,
                    "nl_company_cnpj_cpf": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["CNPJ"],
                    "ds_company_issuer_name": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["xNome"],
                    "ds_company_complement": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xCpl"],
                    "ds_company_address": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xLgr"],
                    "ds_company_neighborhood": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xBairro"],
                    "ds_company_number": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["nro"],
                    "ds_company_city_name": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["xMun"],
                    "ds_company_uf": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["UF"],
                    "ds_company_zip_code": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["CEP"],
                    "ds_company_fone": dict_data["nfeProc"]["NFe"]["infNFe"]["emit"]["enderEmit"]["fone"],
                    "table_items": mount_table(items),
                    "qtd_unit_itens": dict_data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["qCom"],
                    "qtd_itens": dict_data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["indTot"],
                    "tot_product": dict_data["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"]["vProd"],
                    "vl_discount": dict_data["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"]["vDesc"],
                    "vl_shipping": dict_data["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"]["vFrete"],
                    "vl_total": dict_data["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"]["vNF"],
                    "payment_forms": payment_type,
                    "payment_return_forms": dict_data["nfeProc"]["NFe"]["infNFe"]["pag"]["detPag"]["vPag"],
                    "url_sefaz": dict_data["nfeProc"]["NFe"]["infNFeSupl"]["urlChave"],
                    "ds_danfe": '',
                    "consumer": '',
                    "nl_invoice": dict_data["nfeProc"]["NFe"]["infNFe"]["ide"]["cNF"],
                    "ds_invoice_serie": dict_data["nfeProc"]["NFe"]["infNFe"]["ide"]["serie"],
                    "dt_invoice_issue": dict_data["nfeProc"]["NFe"]["infNFe"]["ide"]["dhEmi"],
                    "ds_protocol": dict_data["nfeProc"]["protNFe"]["infProt"]["nProt"],
                    "dt_hr_invoice_issue": dict_data["nfeProc"]["NFe"]["infNFe"]["ide"]["dhEmi"],
                    # "QRCODE": dict_data["nfeProc"]["NFe"]["infNFeSupl"]["qrCode"],
                    "QRCODE": 'https://generator.qrcodefacil.com/qrcodes/static-eee4e1f2a0e3cd369c7053a88a745622.svg',
                    "state_fiscal_message": '',
                    "approximate_tax": '',
                    "additional_information": dict_data["nfeProc"]["NFe"]["infNFe"]["infAdic"]["infCpl"],
                    }

    # print(dict_details)

    html_bytestring = html % dict_details

    with open(f'templates/{file_name}.html', 'w') as html_file:
        html_file.write(html % dict_details)

    cpdf = ChromePDF(PATH_TO_CHROME_EXE, sandbox=False)

    with open(f'pdf/{file_name}.pdf', 'w') as output_file:
        if cpdf.html_to_pdf(html_bytestring, output_file):
            print("Successfully generated the pdf: {}".format(output_file.name))
        else:
            print("Error generating pdf")


if __name__ == '__main__':
    main()
