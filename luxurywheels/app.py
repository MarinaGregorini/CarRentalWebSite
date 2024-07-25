from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database.migration import *
from validar_pagamento import validar_dados_pagamento
from clear_cookies import clear_cookies

app = Flask(__name__)
app.secret_key = 'p`x=^h}v_$~ri~f-'

login_manager = LoginManager()
login_manager.init_app(app)

DATABASE_PATH = 'database/luxuryWheels.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():

    tipos_veiculos = session.query(TipoVeiculo).all()
    marcas = session.query(Marca).all()
    categorias = session.query(Categoria).all()
    transmissoes = session.query(Transmissao).all()
    tipos_motores = session.query(TipoMotor).all()

    response = make_response(render_template(
    'search.html',
    tipos_veiculos=tipos_veiculos,
    marcas=marcas,
    categorias=categorias,
    transmissoes=transmissoes,
    tipos_motores=tipos_motores
))

    response = clear_cookies(response)

    return response

@app.route('/resultado_da_pesquisa', methods=['POST'])
def resultado_da_pesquisa():

    tipo_veiculo_id = request.form.getlist('tipoVeiculo')
    tipo_veiculo_id_int = list(map(int, tipo_veiculo_id))

    transmissao_id = request.form.getlist('transmissao')
    transmissao_id_int = list(map(int, transmissao_id))

    tipo_motor_id = request.form.getlist('tipo_motor')
    tipo_motor_id_int = list(map(int, tipo_motor_id))

    marca_id = request.form.getlist('marca')
    marca_id_int = list(map(int, marca_id))

    categoria_id = request.form.getlist('categoria')
    categoria_id_int = list(map(int, categoria_id))

    diaria = request.form.get('diaria')
    passageiros = request.form.getlist('lugares')
    levantamento = request.form.get('levantamento')
    devolucao = request.form.get('devolucao')

    levantamento = datetime.strptime(levantamento, '%Y-%m-%dT%H:%M')
    devolucao = datetime.strptime(devolucao, '%Y-%m-%dT%H:%M')

    if levantamento < datetime.now():
        flash('A data de levantamento não pode ser anterior à data atual')
        response = redirect(url_for('home'))
        return response

    if devolucao < levantamento:
        flash('A data de devolução não pode ser anterior à data de levantamento')
        response = redirect(url_for('home'))
        return response

    diferenca_em_horas = (devolucao - levantamento).total_seconds() / 3600

    dias_reserva = int(diferenca_em_horas // 24)

    if diferenca_em_horas % 24 > 0:

        dias_reserva += 1

    query = session.query(Veiculos)

    if tipo_veiculo_id:

        query = query.join(TipoVeiculo).filter(Veiculos.tipo_veiculo_id.in_(tipo_veiculo_id_int))

    if marca_id:

        query = query.join(Marca).filter(Veiculos.marca_id.in_(marca_id_int))

    if categoria_id:

        query = query.join(Categoria).filter(Veiculos.categoria_id.in_(categoria_id_int))

    if transmissao_id:

        query = query.join(Transmissao).filter(Veiculos.transmissao_id.in_(transmissao_id_int))

    if tipo_motor_id:

        query = query.join(TipoMotor).filter(Veiculos.tipo_motor_id.in_(tipo_motor_id_int))

    for opcao in passageiros:

        if opcao=='lugares1_4':

            query = query.filter(Veiculos.passageiros.between(1, 4))

        elif opcao=='lugares5_6':

            query = query.filter(Veiculos.passageiros.between(5, 6))

        elif opcao=='lugares7+':

            query = query.filter(Veiculos.passageiros.between(7, 9))

    if diaria:

        query = query.filter(Veiculos.diaria <= float(diaria))

    subquery = session.query(Reservas.veiculo_id).filter(
        or_(
            and_(Reservas.data_inicio <= levantamento, Reservas.data_final >= levantamento),
            and_(Reservas.data_inicio <= devolucao, Reservas.data_final >= devolucao),
            and_(Reservas.data_inicio >= levantamento, Reservas.data_final <= devolucao)
        )
    ).subquery()

    query = query.filter(~Veiculos.id.in_(select(subquery.c.veiculo_id)))

    query = query.filter(Veiculos.prox_revisao > devolucao)

    validacao_devolucao = devolucao - timedelta(days=365)
    query = query.filter(Veiculos.inspecao >= validacao_devolucao)

    resultados = query.all()

    response = make_response(
        render_template(
            'results.html',
            resultados=resultados,
            dias_reserva=dias_reserva
        )
    )

    response.set_cookie('levantamento', levantamento.strftime('%Y-%m-%dT%H:%M'))
    response.set_cookie('devolucao', devolucao.strftime('%Y-%m-%dT%H:%M'))

    return response

@app.route('/set-cookies', methods=['POST'])
def set_cookies():

    veiculo_id = request.form.get('veiculo_id')
    valor_total = request.form.get('valor_total')

    if current_user.is_authenticated:

        response = make_response(redirect(url_for('pagamento')))
        response.set_cookie('veiculo_id', veiculo_id)
        response.set_cookie('valor_total', valor_total)

        return response

    response = make_response(redirect(url_for('login', next=url_for('pagamento'))))
    response.set_cookie('veiculo_id', veiculo_id)
    response.set_cookie('valor_total', valor_total)

    return response

@login_manager.user_loader
def load_user(user_id):

    response = session.get(Clientes, int(user_id))

    return response

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET' or request.method == 'POST' and 'email' not in request.form:

        next_page = request.args.get('next')

        if next_page:

            response = make_response(render_template('login.html'))
            response.set_cookie('next_page', next_page)

            return response

        response = render_template('login.html')

        return response

    if request.method == 'POST' and 'email' in request.form:

        email = request.form.get('email')
        senha = request.form.get('senha')

        cliente = session.query(Clientes).filter_by(email=email).first()

        if cliente and cliente.check_password(senha):

            login_user(cliente)

            next_page = request.cookies.get('next_page')

            if next_page:

                response = make_response(redirect(next_page))
                response.delete_cookie('next_page')

                return response

            response = redirect(url_for('home'))

            return response

        flash('E-mail ou senha incorretos')

        response = redirect(url_for('login'))

        return response

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')

        cliente_existente = session.query(Clientes).filter_by(email=email).first()

        if cliente_existente:

            flash('Este email já está registrado. Faça login ou use outro email.')

            response = render_template('registro.html')

            return response

        novo_cliente = Clientes(nome=nome, email=email, telefone=telefone)
        novo_cliente.set_password(senha)

        session.add(novo_cliente)
        session.commit()

        response = redirect(url_for('login'))

        return response

    response = render_template('registro.html')

    return response

@app.route('/logout')
@login_required
def logout():

    logout_user()

    response = redirect(url_for('home'))

    return response

@app.route('/pagamento', methods=['GET', 'POST'])
@login_required
def pagamento():

    valor_total = request.cookies.get('valor_total')
    veiculo_id = request.cookies.get('veiculo_id')

    veiculo = session.get(Veiculos, int(veiculo_id))

    if request.method == 'POST' and 'nome_cartao' in request.form:

        nome_cartao = request.form.get('nome_cartao')
        numero_cartao = request.form.get('numero_cartao')
        id_cartao = numero_cartao[-4:]
        validade = request.form.get('validade')
        cvv = request.form.get('cvv')

        if validar_dados_pagamento(numero_cartao, validade, cvv):

            pagamento_realizado = Pagamentos(
            nome_cartao=nome_cartao,
            numero_cartao=id_cartao,
            valor_reserva=valor_total,
            pagamento_realizado=True
            )

            session.add(pagamento_realizado)
            session.commit()

            cliente_id = current_user.id

            levantamento = request.cookies.get('levantamento')
            devolucao = request.cookies.get('devolucao')

            levantamento = datetime.strptime(levantamento, '%Y-%m-%dT%H:%M')
            devolucao = datetime.strptime(devolucao, '%Y-%m-%dT%H:%M')

            reserva = Reservas(
            veiculo_id=veiculo_id,
            cliente_id=cliente_id,
            data_inicio=levantamento,
            data_final=devolucao,
            pagamento_id=pagamento_realizado.id
            )

            session.add(reserva)
            session.commit()

            reserva_id = reserva.id
            pagamento_id = reserva.pagamento_id

            response = make_response(
                render_template(
                    'confirmacao_reserva.html',
                    veiculo=veiculo,
                    valor_total=valor_total,
                    reserva_id=reserva_id,
                    levantamento=levantamento,
                    devolucao=devolucao
                )
            )

            response.set_cookie('reserva_id', str(reserva_id))
            response.set_cookie('pagamento_id', str(pagamento_id))

            return response

        flash('Dados de pagamento inválidos. Por favor, tente novamente.')

        response = render_template('pagamento.html', veiculo=veiculo, valor_total=valor_total)

        return response

    response = render_template('pagamento.html', veiculo=veiculo, valor_total=valor_total)

    return response

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():

    if current_user.is_authenticated:

        todas_reservas = (
            session.query(Reservas)
            .filter_by(cliente_id=current_user.id)
            .order_by(Reservas.data_inicio)
            .all()
        )

        veiculos = {
            reserva.veiculo_id: session.get(Veiculos, reserva.veiculo_id)
            for reserva in todas_reservas
        }

        pagamentos = {
            reserva.pagamento_id: session.get(Pagamentos, reserva.pagamento_id)
            for reserva in todas_reservas
        }

        data_atual = date.today()

        reserva_atual = None
        outras_reservas = []

        for reserva in todas_reservas:

            data_inicio = reserva.data_inicio.date()
            data_final = reserva.data_final.date()

            if data_final < data_atual:

                session.delete(reserva)

            elif data_inicio <= data_atual <= data_final:

                reserva_atual = reserva

            else:

                outras_reservas.append(reserva)

        response = render_template(
            'reservations.html',
            reserva_atual=reserva_atual,
            outras_reservas=outras_reservas,
            veiculos=veiculos,
            pagamentos=pagamentos
        )

        return response

    response = redirect(url_for('login', next=url_for('reservas')))

    return response

@app.route('/alterar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def alterar_reserva(reserva_id):

    reserva = session.get(Reservas, reserva_id)
    veiculo = reserva.veiculo

    if request.method == 'POST':

        nova_data_inicio = request.form.get('data_inicio')
        nova_data_final = request.form.get('data_final')

        nova_data_inicio = datetime.strptime(nova_data_inicio, '%Y-%m-%dT%H:%M')
        nova_data_final = datetime.strptime(nova_data_final, '%Y-%m-%dT%H:%M')

        if nova_data_inicio < datetime.now():

            flash('A data de levantamento não pode ser anterior à data atual')

            response = redirect(url_for('alterar_reserva', reserva_id=reserva_id))

            return response

        if nova_data_final < nova_data_inicio:

            flash('A data de devolução não pode ser anterior à data de levantamento')

            response = redirect(url_for('alterar_reserva', reserva_id=reserva_id))

            return response

        validacao_devolucao = nova_data_final - timedelta(days=365)

        veiculo_disponivel = session.query(Veiculos).filter(
            and_(
                Veiculos.id == veiculo.id,
                ~exists().where(
                    and_(
                        Reservas.veiculo_id == Veiculos.id,
                        Reservas.data_inicio < nova_data_final,
                        Reservas.data_final > nova_data_inicio
                    )
                ),
                Veiculos.prox_revisao > nova_data_final,
                Veiculos.inspecao > validacao_devolucao
            )
        ).first()

        if not veiculo_disponivel:

            flash('O veículo não está disponível para as novas datas selecionadas')

            response = redirect(url_for('alterar_reserva', reserva_id=reserva_id))
            return response

        num_dias = (nova_data_final - nova_data_inicio).days + 1
        diaria = reserva.veiculo.diaria

        novo_valor_reserva = num_dias * diaria

        reserva.data_inicio = nova_data_inicio
        reserva.data_final = nova_data_final
        reserva.pagamento.valor_reserva = novo_valor_reserva

        session.commit()

        flash('Datas da reserva alteradas com sucesso!')

        response = redirect(url_for('reservas'))

        return response

    response = render_template('alterar_reserva.html', reserva=reserva)

    return response

@app.route('/cancelar_reserva/<int:reserva_id>', methods=['POST'])
@login_required
def cancelar_reserva(reserva_id):

    reserva = session.get(Reservas, reserva_id)

    session.delete(reserva)
    session.commit()

    flash('Reserva cancelada com sucesso!')

    response = redirect(url_for('reservas'))

    return response

if __name__ == '__main__':
    app.run(debug=True)
