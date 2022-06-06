from crypt import methods
import requests
from urllib import response
from flask import Flask, redirect, render_template, request, redirect
from datetime import datetime, timedelta
import gspread

app = Flask(__name__)

gc = gspread.service_account('/Users/joseceronrodriguez/Desktop/xepelin/credencial.json')

sh = gc.open_by_key('1tdXg394erp-ELjWSj-lH4PO0i_JZK2iCGKrY_CyUbfY')

worksheet = sh.sheet1

class Registros:
    def __init__(self, idOp, Tasa, Email, row_idx):
        self.id = idOp
        self.tasa = Tasa
        self.email = Email
        self.row_idx = row_idx


@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    if not email or email != 'test.xepelin@gmail.com':
        return "error! bad email"

    pw = request.form['pw']
    if not pw or pw != "12345":
        return "error! wrong password"

    #worksheet.append_row()

    return redirect('/page')

@app.route('/', methods=['GET','POST'])
def index():
    print("hola")
    return render_template('index.html')

@app.route('/page')
def registro():
    registros = worksheet.get_all_records()
    headers = ['idOp','Tasa','Email']
    datos = []
    for idx, dato in enumerate(registros, start=2):
        row = [dato['idOp'],dato['Tasa'],dato['Email']]
        datos.append(row)

    return render_template('gsheet.html', datos = datos, headers= headers)

@app.route('/change', methods =['POST'])
def change_tasa():
    id_op = request.form['idOp']
    new_tasa= request.form['tasa']
    email = request.form['email']

    cell = worksheet.find(id_op)

    cell_row = cell.row
    cell_col_tasa = int(cell.col) + 1
    worksheet.update_cell(cell_row, cell_col_tasa, new_tasa)

    url = 'https://hooks.zapier.com/hooks/catch/6872019/oahrt5g/'
    data = {
        'idOp': id_op,
        'tasa': new_tasa,
        'email': email
    }

    response = requests.post(url, json = data)
    return "Se envio el correo"