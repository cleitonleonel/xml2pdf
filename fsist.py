# -*- coding: utf-8 -*-
#
"""
Author: <Cleiton Leonel Creton>
E-mail: <cleiton.leonel@gmail.com>
versão: 0.0.1

ES-Brazil, 26/11/2020
"""


import io
import json
import zipfile
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.fsist.com.br/'


class Browser(object):

    def __init__(self):
        self.response = None
        self.session = requests.Session()
        self.soup_parser = {'features': 'html5lib'}

    def headers(self):
        """
        Define o header padrão para o Browser
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0)'
                          ' Gecko/20100101 Firefox/72.0',
        }
        return headers

    def send_request(self, method, url, soup_cnf=False, **kwargs):
        """
        Envia a requisição de acordo com o método definido e retorna o código-fonte da página.

        :param method: GET ou POST.
        :param url: Link url da página a ser requisitada.
        :param soup_cnf: True ou False, define o uso ou não de Beaultifulsoup.
        :param kwargs: Argumentos passados diretamente para a lib requests.
        :return:
        """
        try:
            response = self.session.request(method, url, **kwargs)
        except ValueError:
            return None
        if response.status_code == 200:
            if soup_cnf:
                try:
                    return self.format_html(response.text)
                except ValueError:
                    return []

        return response

    def format_html(self, response):
        soup = BeautifulSoup(response, **self.soup_parser)
        return soup


class FSistApi(Browser):

    def __init__(self):
        super().__init__()
        self.id = None
        self.arq = None
        self.type = None
        self.content = None
        self.current_key = None
        self.current_json = {}
        self.headers = self.headers()
        self.headers['Content-Type'] = 'application/json'

    def upload_xml(self, xml_file, soup_cnf):
        """
        Faz o envio do xml para o site https://www.fsist.com.br/.

        :param xml_file: Caminho do arquivo xml.
        :param soup_cnf: Define o uso ou não de Beaultifulsoup.
        :return: Retorna o código-fonte da página ou False, caso não encontre o pdf.
        """
        self.headers.pop('Content-Type', None)
        params = {
            't': 'gerarpdf'
        }
        with open(xml_file, 'rb') as file:
            response = self.send_request('POST', BASE_URL + '/comandos.aspx', soup_cnf,
                                         files={'file': file}, params=params, headers=self.headers)
        if not response:
            return False

        result = response.find("compactando")

        self.current_json = json.loads(result.text)

        self.current_key = self.current_json['itens'][0]['chave']
        self.id = self.current_json['id']
        self.arq = self.current_json['Arquivo']
        self.type = 'gerarpdfdownload'

        return self.current_json

    def get_pdf(self, download=True):
        """
        Faz a requisição para download do pdf.

        :return: Retorna os bytes do arquivo zip que contém o arquivo ou arquivos pdf.
        """
        params = {
            't': self.type,
            'id': self.id,
            'arq': self.arq
        }
        response = self.send_request('GET', BASE_URL + 'comandos.aspx',
                                     params=params, headers=self.headers)

        if not response:
            return False

        if download:
            return self.extract(response)

        return response.content

    def extract(self, response):
        """
        Extrai e salva o pdf ou pdfs na pasta padrão.

        :param response: Recebe o response com os bytes do arquivo zip.
        :return: Retorna sucesso o falha para o download do arquivo.
        """
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as temp_zip:
                for zipinfo in temp_zip.infolist():
                    if self.current_key in zipinfo.filename:
                        filename = zipinfo.filename
                        temp_zip.extract(filename, path='./pdf')
                        return True
        except ValueError:
            return False


if __name__ == "__main__":
    fs = FSistApi()
    data = fs.upload_xml('docs/35080599999090910270550010000000015180051273-nfe.xml', soup_cnf=True)  # Por padrão usa-se bs4 para fazer o parse no código-fonte, soup_cnf=False irá retornar o response puro.
    download = fs.get_pdf()  # Download automático, para alterar definir "fs.get_pdf(download=False)"
