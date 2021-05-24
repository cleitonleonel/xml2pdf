# -*- coding: utf-8 -*-
#
html = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <style type="text/css">
        #page-content {
            background: white;
            width: 80mm;
            font-family: Arial,Helvetica Neue,Helvetica,sans-serif;
        }

        @page {
            size: 80mm 210mm; /*{{ order.total_height }}*/
            /*margin: 2mm;*/
            margin-left: 4mm;
            margin-right: 4mm;
            padding: 0;
        }

        /* print */
        /*@page {
            margin-left: 4mm;
            margin-right: 4mm;
            padding: 0;
        }*/

        @media print {
            * {
                padding-left: 0 !important;
                padding-right: 0 !important;
            }

            .areaNfce {
                border: none !important;
            }
        }

        /* geral */
        * {
            padding: 0;
            margin: 0;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            min-width: 58mm;
            max-width: 80mm;
        }

        .areaNfce {
            min-width: 58mm;
            margin: 4px auto;
            border: 1px solid #c5c6c1;
            padding: 0 8px 0 8px;
        }

        .areaNfce table {
            width: 100%%;
            margin-top: 5px;
        }

        .areaNfce table thead {
            float: left;
            width: 100%%;
            min-height: 50px;
        }

        .areaNfce table tr td {
            text-align: left;
            font-size: 12px;
            color: #000;
            vertical-align: top;
        }

        /* mainNfce */
        .areaNfce table.mainNfce {
            border-top: none;
        }

        .mainNfce .titMain {
            display: block;
            font-size: 10px;
        }

        .areaNfce table.mainNfce tr td {
            text-align: left;
        }


        .areaNfce table.mainNfce tr td .logo img {
            height: 47px;
            width: 47px;
            padding-right: 4px;
        }

        .areaNfce table.detailSale {
            margin-top: 10px;
            table-layout: fixed;
        }

        .areaNfce table.detailSale tr td {
            text-align: left;
            padding: 5px;
            font-weight: bolder;
            letter-spacing: 0px;
        }

        .areaNfce table.detailSale tr td:first-child {
            border-left: none;
        }

        .areaNfce table.detailSale tr td:last-child {
            text-align: right;
            width: 60px;
            vertical-align: bottom;
        }

        .detailSale td {
            display: inline;
        }

        .formPayment tr td {
            font-size: 10px !important;
        }

        .formPayment .tdRight {
            margin-left: 100px;
        }

        .formPayment .mRight {
            margin-left: 34px;
        }


        /* formPayment */
        .valuePayment .paymentText {
            margin-top: 10px;
            font-size: 12px;
            font-weight: 300;
        }

        .formPayment .tRight {
            text-align: right;
        }

        .valuePayment td.paymentText span {
            text-align: right;
        }

        .formPayment .lColor {
            font-size: 12px;
            color: #808080;
            font-weight: 300;
        }

        .descQt .qtde {
            margin-top: 10px;
            font-size: 12px;
            color: #808080;
            font-weight: 300;
        }

        .descQt .qtde.last {
            color: #000;
            margin-bottom: 10px;
            display: block;
        }

        .descQt td.qtde span {
            text-align: right;
            display: inline;
            float: right;
        }


        /* explanations */
        .areaNfce table.explanations tr td {
            text-align: center;
        }

        .contingencia {
            background: #808080;
            border: 1px solid #d4d4d4;
        }

        .contingencia div {
            background: #fff;
            width: 216px;
            margin: 0 auto;
            padding: 10px;
        }

        .explanations .contingencia h1 {
            font-size: 15px;
        }
        /* postTax */
        .areaNfce table.postTax tr td {
            text-align: center;
        }

        .postTax .text {
            font-weight: bold;
            color: #000;
            font-size: 10px;
        }

        .postTax a {
            text-decoration: none;
            color: #000;
            display: block;
            text-align: center;
        }
        /* User */
        .areaNfce table.user tr td {
            text-align: center;
        }

        /* Barcode */

        .barcode td {
            vertical-align: top !important;
        }

        .barcode .info-consumer {
            text-align: center;
        }

        /*.barcode .section-info-small { display: none; }*/

        .barcode .section-info {
            width: 100%%;
        }

        .barcode .section-info .info-consumer .lColor {
            font-size: 12px;
            color: #808080;
            font-weight: 300;
            text-transform: none;
        }

        .barcode .section-info .info-consumer h5 {
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
        }

        .barcode .section-info .info-consumer p {
            line-height: 15px;
            font-family: 'Arial', Helvetica, sans-serif;
            font-size: 12px;
            margin-bottom: 4px;
        }

        .qrCode {
            /*width: 25mm;
            min-height: 25mm;*/
            margin: 0 auto;
            text-align: center;
        }

        /* footer */
        .nfceFooter p {
            font-size: 12px !important;
            color: #000 !important;
            font-weight: 300;
            font-family: 'Arial', Helvetica, sans-serif;
        }

        .nfceFooter p span {
            display: block;
            text-align: center;
        }

        .table-contingencia {
            border-top: 1px solid #000;
            border-bottom: 1px solid #000;
            /*background: white url(data:image/png;charset=utf-8;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAICAYAAADA+m62AAAAGklEQVQoU2NkYGCQZCACMBKhBqyENgoHuxsBNlAAO7Z6FzgAAAAASUVORK5CYII=);*/
            position: relative;
        }

        .table-contingencia .aviso-contingencia {
            background-color: white;
            text-align: center;
            width: 100%%;
            margin: 0 auto;
            padding: 5px;
        }

        .table-contingencia .aviso-contingencia h5 {
            font-size: 14px;
            font-weight: bold;
            margin: 0;
            padding: 0;
            text-transform: uppercase;
        }

        .table-contingencia .aviso-contingencia p {
            font-size: 12px;
        }

        .td-text-right {
            float: right;
            text-align: right;
        }

        @media print {
            .table-contingencia {
                overflow: hidden;
            }

            .table-contingencia:before {
                position: absolute;
                width: 100%%;
                height: 100%%;
                z-index: 2;
                /*content: url('data:image/gif;charset=utf-8;base64,R0lGODlhIANkAIAAAObm5v///yH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS4zLWMwMTEgNjYuMTQ1NjYxLCAyMDEyLzAyLzA2LTE0OjU2OjI3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M2IChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5QUY0REVDMTAwMzIxMUU3OUQwRUM3OTJEQjVBMjMyQyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo5QUY0REVDMjAwMzIxMUU3OUQwRUM3OTJEQjVBMjMyQyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjlBRjRERUJGMDAzMjExRTc5RDBFQzc5MkRCNUEyMzJDIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjlBRjRERUMwMDAzMjExRTc5RDBFQzc5MkRCNUEyMzJDIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+Af/+/fz7+vn49/b19PPy8fDv7u3s6+rp6Ofm5eTj4uHg397d3Nva2djX1tXU09LR0M/OzczLysnIx8bFxMPCwcC/vr28u7q5uLe2tbSzsrGwr66trKuqqainpqWko6KhoJ+enZybmpmYl5aVlJOSkZCPjo2Mi4qJiIeGhYSDgoGAf359fHt6eXh3dnV0c3JxcG9ubWxramloZ2ZlZGNiYWBfXl1cW1pZWFdWVVRTUlFQT05NTEtKSUhHRkVEQ0JBQD8+PTw7Ojk4NzY1NDMyMTAvLi0sKyopKCcmJSQjIiEgHx4dHBsaGRgXFhUUExIREA8ODQwLCgkIBwYFBAMCAQAAIfkEAAAAAAAsAAAAACADZAAAAv+Ej6nL7Q+jnLTai7PevPsPhuJIluaJpuqKBe4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNF7Pm9Lr9js/r9/y+/w8YyBJHWGh4iJiouMjY6PgIGSk5SVlpeYmZqbnJ2emJKRgqOkpaanqKmqq6avrp+gobKztLW2t7i5uru8vb6/sLHCz8xFpsfIycrLzM3Lw8DB0tPU1dbX2Nna29zd3t/Q1e6zxOXm5+jp6u3hre7v4OHy8/T19vf4+fr79fue7/DzCgwIEEmfE7iDChwoUMGzp8CDGixIkUC1q8iDGjxo3/HCFQ/AgypMiRJEuaPIkypUp9HVu6fAkzpkxRK2vavIkzp86dPHv6/FlyptChRIsaPdoAqNKlTJs6fQo1qtSpVJUgvYo1q9at56p6/Qo2rNixZMuaPRuLq9q1bNu6zYM2rty5dOvavYs3r9e3fPv6/Qv4gd7BhAsbPow4seLF4gI7fgw5clHGlCtbvow5s+bNnGNI/gw6tGiAnUubPo06terVrBmOfg07tuxUrWvbvo07t+7dvBnN/g08uPBBvYsbP448ufLlyIc7fw49+gTm1Ktbv449u/aq0rt7/y58u/jx5MubP4/+Hfj17NtDTg8/vvz59OvbV+Q+v/79W+/7XP8PYIACDkggDvwdiGCCLxXIYIMOPghhhLgpSGGFFpImYYYabshhhx6GdWGIIo6ozIcmnohiiiqu2BCJLr4II00szkhjjTbeiKMuMe7IY4905AhkkEIOSWSRahQAADs=');*/
            }

            .table-contingencia .aviso-contingencia {
                position: relative;
                z-index: 10;
            }
        }
    </style>
  </head>

  <body>
    <div class="areaNfce">
      <table class="mainNfce">
        <thead>
        <tr>
          <td id="companyLogo">
            <div class="logo">
              <img src="%(url_logo)s" />
            </div>
          </td>
          <td class="titMain">
            <p>
              <span class="label">CNPJ: %(nl_company_cnpj_cpf)s </span><br><span style="">%(ds_company_issuer_name)s</span>
            </p>
            <p>%(ds_company_address)s, %(ds_company_neighborhood)s, %(ds_company_complement)s, %(ds_company_number)s, %(ds_company_city_name)s, %(ds_company_uf)s</p>
            <p>CEP: %(ds_company_zip_code)s</p>
            <p>TEL: %(ds_company_fone)s</p>
            <!--<p>Documento Auxiliar da Nota Fiscal de Consumidor Eletrônica</p>-->
          </td>
        </tr>
        </thead>
      </table>

      <table class="table-contingencia">
        <tr>
          <td>
            <div class="aviso-contingencia">
              <!--<h5>Emitida em Contingencia</h5>
              <p>Pendente de autorização</p>-->
              
              <p style="font-weight: bold">Documento Auxiliar da Nota Fiscal de Consumidor Eletrônica</p>
            </div>
          </td>
        </tr>
      </table>

      <table class="formPayment" style="border-bottom: 1px solid #000;">
      
        <tr>
          <td><strong>Código</strong></td>
          <td><strong>Descrição</strong></td>
          <td class="tdRight"><strong>Qtde</strong></td>
          <td class="tdRight"><strong>UN</strong></td>
          <td class="tRight"><strong>Vl Unit.</strong></td>
          <td class="tRight"><strong>Vl Total</strong></td>
        </tr>
        %(table_items)s
      </table>

      <table class="descQt" style="border-bottom: 1px solid #000;">
        <!--<tr>
          <td>Itens unitários<span class="td-text-right">[(qtd_unit_itens)]</span></td>
        </tr>-->
        <tr>
          <td>Qtde total de itens <span class="td-text-right">%(qtd_itens)s</span></td>
        </tr>
        <tr>
          <td>Valor total R$ <span class="td-text-right">%(tot_product)s</span></td>
        </tr>
        <tr id="discount">
          <td>Desconto R$ <span class="td-text-right">%(vl_discount)s</span></td>
        </tr>
        <tr id="shipping">
          <td class="last">Frete R$ <span class="td-text-right">%(vl_shipping)s</span></td>
        </tr>
        <tr>
          <td class="last"><strong>Valor a Pagar R$ <span class="td-text-right">%(vl_total)s</span></strong></td>
        </tr>
      </table>

      <table class="valuePayment" style="border-bottom: 1px solid #000;">
        <tr>
          <td>FORMA PGTO. <span class="td-text-right">VALOR PAGO R$</span></td>
        </tr>
        %(payments)s

      </table>

      <table class="postTax" style="border-bottom: 1px solid #000;">
        <tr>
          <td><span id="url_consulta" class="text">Consulte pela Chave de Acesso em <br><a style="color: blue" href="">%(url_sefaz)s</a></span></td>
        </tr>
        <tr>
          <td>%(ds_danfe)s</td>
        </tr>
      </table>

      <table>
        <tr>
          <td>
            <div class="qrCode">
              <img width="110px" src="%(QRCODE)s" />
            </div>
          </td>
        </tr>
      </table>

      <table class="barcode">
        <tr class="section-info">
          <td style="text-align: center" class="info-consumer">
            <p><strong>Consumidor</strong> %(consumer)s</p>
            <p style="font-size: 10px"><strong>NFCe nº %(nl_invoice)s Série %(ds_invoice_serie)s %(dt_invoice_issue)s</strong></p>
            <p><strong>Via consumidor</strong></p>
            <p><strong>Protocolo de autorização:</strong>%(ds_protocol)s</p>
            <p><strong>Data de autorização:</strong>%(dt_hr_invoice_issue)s</p>
            
            <!--<div class="contingency-text">
              <h5>Emitida em Contingencia</h5>
              <p>Pendente de autorização</p>
            </div>-->

            <!--<div id="qrCode" class="qrCode">
                <img src="%(QRCODE)s" />
            </div>-->
            
          </td>
        </tr>
      </table>

      <table class="nfceFooter" id="stateFiscalMessage">
        <tr>
          <td><p style="text-align: center">%(state_fiscal_message)s</p></td>
        </tr>
      </table>

      <table class="nfceFooter">
        <tr>
          <td><p style="text-align: center">%(approximate_tax)s</p></td>
        </tr>
      </table>

      <table class="nfceFooter">
        <tr>
          <td><p style="text-align: left; font-size: 10px">%(additional_information)s</p></td>
        </tr>
      </table>

      <table class="nfceFooter">
        <tr>
          <td style="text-align: center; font-size: 10px"><strong>Empresa de Software www.empresa.com</strong></td>
        </tr>
      </table>
    </div>
  </body>
</html>
"""