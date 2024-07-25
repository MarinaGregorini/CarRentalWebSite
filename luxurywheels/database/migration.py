from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
Base = declarative_base()

class TipoVeiculo(Base):

    __tablename__ = 'tipo_veiculo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)

class Marca(Base):

    __tablename__ = 'marca'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)

class Modelo(Base):

    __tablename__ = 'modelo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)

class Categoria(Base):

    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)

class Transmissao(Base):

    __tablename__ = 'transmissao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)

class TipoMotor(Base):

    __tablename__ = 'tipo_motor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False, unique=True)

class Veiculos(Base):

    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_veiculo_id = Column(Integer, ForeignKey('tipo_veiculo.id'), nullable=False)
    marca_id = Column(Integer, ForeignKey('marca.id'), nullable=False)
    modelo_id = Column(Integer, ForeignKey('modelo.id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    transmissao_id = Column(Integer, ForeignKey('transmissao.id'), nullable=False)
    tipo_motor_id = Column(Integer, ForeignKey('tipo_motor.id'), nullable=False)
    passageiros = Column(Integer, nullable=False)
    diaria = Column(DECIMAL(6, 2), nullable=False)
    ult_revisao = Column(Date, nullable=False)
    prox_revisao = Column(Date, nullable=False)
    inspecao = Column(Date, nullable=False)
    imagem_url = Column(String(200), nullable=False)

    reservas = relationship('Reservas', backref='veiculo')
    tipo_veiculo = relationship('TipoVeiculo', backref='veiculos')
    marca = relationship('Marca', backref='veiculos')
    modelo = relationship('Modelo', backref='veiculos')
    categoria = relationship('Categoria', backref='veiculos')
    transmissao = relationship('Transmissao', backref='veiculos')
    tipo_motor = relationship('TipoMotor', backref='veiculos')

class Clientes(Base):

    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(20), nullable=True)
    senha = Column(String(50), nullable=False)

    reservas = relationship('Reservas', backref='cliente')

    def set_password(self, senha):

        self.senha = generate_password_hash(senha)

    def check_password(self, senha):

        return check_password_hash(self.senha, senha)

    def is_authenticated(self):

        return True

    def is_active(self):

        return True

    def is_anonymous(self):

        return True

    def get_id(self):

        return str(self.id)

class Pagamentos(Base):

    __tablename__ = 'pagamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_cartao = Column(String(100), nullable=False)
    nome_cartao = Column(String(100), nullable=False)
    valor_reserva = Column(DECIMAL(10, 2), nullable=False)
    pagamento_realizado = Column(Boolean, nullable=False, default=False)

    reservas = relationship('Reservas', backref='pagamento')

class Reservas(Base):

    __tablename__ = 'reservas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'), nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data_inicio = Column(DateTime, nullable=False)
    data_final = Column(DateTime, nullable=False)
    pagamento_id = Column(Integer, ForeignKey('pagamentos.id'), nullable=True)


DATABASE_PATH = 'database/luxuryWheels.db'
engine = create_engine(f'sqlite:///{DATABASE_PATH}')

Base.metadata.create_all(engine)
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()
