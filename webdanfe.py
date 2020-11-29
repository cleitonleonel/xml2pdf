# -*- coding: utf-8 -*-
#
"""
Author: <Cleiton Leonel Creton>
E-mail: <cleiton.leonel@gmail.com>
versão: 0.0.1

ES-Brazil, 26/11/2020
"""

import requests

BASE_URL = 'https://www.webdanfe.com.br/'


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

    def send_request(self, method, url, **kwargs):
        """
        Envia a requisição de acordo com o método definido e os bytes do abjeto.

        :param method: GET ou POST.
        :param url: Link url da página a ser requisitada.
        :param kwargs: Argumentos passados diretamente para a lib requests.
        :return:
        """
        try:
            response = self.session.request(method, url, **kwargs)
        except ValueError:
            return None

        if response.status_code == 200:
            return response

        return False


class WebDanfeApi(Browser):

    def __init__(self):
        super().__init__()
        self.headers = self.headers()
        self.headers['Content-Type'] = 'application/json'

    def upload_xml(self, xml_file):
        """
        Faz o envio do xml para o site https://www.webdanfe.com.br/.

        :param xml_file: Caminho do arquivo xml.
        :return: Retorna os bytes do arquivo ou False, caso não encontre o pdf.
        """
        self.headers.pop('Content-Type', None)

        with open(xml_file, 'rb') as file:
            response = self.send_request('POST', BASE_URL + 'danfe/GeraDanfe.php',
                                         files={'arquivoXml': file}, headers=self.headers)
        if not response:
            return False

        return response

    def generate_xml(self, key):
        """
        Faz uma busca pelo xml referente via site https://www.webdanfe.com.br/.

        :param key: Chave da nota.
        :return: Retorna o conteúdo do objeto.
        """
        self.headers.pop('Content-Type', None)

        params = {
            'arquivoXml': '(binary)',
            'conteudoDoArquivo': '',
            'chaveNfe': key,
            'tipoBoleto': '1 - 16',
            'boletoAgencia': '',
            'boletoAgenciaDigito': '',
            'boletoConta': '',
            'boletoContaDigito': '',
        }
        response = self.send_request('POST', 'https://camellia.webdanfe.com.br/PegaNfe/Puxa.aspx', params=params, headers=self.headers)
        if not response:
            return False

        return response

    def get_pdf(self, response):
        """
        salva o arquivo do pdf.

        :return: Retorna o file path pdf.
        """

        chunk_size = 2000
        filename = response.headers.get("Content-Disposition").split("filename=")[1].replace('"', '')
        file_path = f'./pdf/{filename}'
        with open(file_path, 'wb') as pdf:
            for chunk in response.iter_content(chunk_size):
                pdf.write(chunk)

        return file_path


if __name__ == "__main__":
    wd = WebDanfeApi()
    response = wd.upload_xml('docs/32201034971421000181650010000014191914100001-nfce.xml')
    download = wd.get_pdf(response)
    # gera_xml = wd.generate_xml(key='32201034971421000181650010000014191914100001') #  Está obsoleta...
