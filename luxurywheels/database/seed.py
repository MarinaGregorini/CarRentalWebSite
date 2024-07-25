from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from migration import *

DATABASE_PATH = 'database/luxuryWheels.db'
engine = create_engine(f'sqlite:///{DATABASE_PATH}')

Session = sessionmaker(bind=engine)
session = Session()

tipo_veiculo = [
    TipoVeiculo(nome='Carro'),
    TipoVeiculo(nome='Moto'),
]

marca = [
    Marca(nome='Fiat'),
    Marca(nome='Peugeot'),
    Marca(nome='Ford'),
    Marca(nome='Mini'),
    Marca(nome='Volkswagen'),
    Marca(nome='Audi'),
    Marca(nome='Tesla'),
    Marca(nome='Citröen'),
    Marca(nome='Mercedes Benz'),
    Marca(nome='Honda'),
    Marca(nome='BMW')
]

modelo = [
    Modelo(nome='500'),
    Modelo(nome='208'),
    Modelo(nome='Focus'),
    Modelo(nome='ID 3'),
    Modelo(nome='Kuga'),
    Modelo(nome='A3 Sportback'),
    Modelo(nome='Model 3'),
    Modelo(nome='Cooper Cabrio'),
    Modelo(nome='C4 Picasso Space Tour'),
    Modelo(nome='V-Class Long'),
    Modelo(nome='PCX 125'),
    Modelo(nome='C 400 GT'),
    Modelo(nome='R1250 GS')
]

categoria = [
    Categoria(nome='Mini'),
    Categoria(nome='Compacto'),
    Categoria(nome='SUV'),
    Categoria(nome='Premium'),
    Categoria(nome='Conversível'),
    Categoria(nome='Grande'),
    Categoria(nome='Standard'),
    Categoria(nome='Oversize'),
]

transmissao = [
    Transmissao(nome='Manual'),
    Transmissao(nome='Automática'),
]

tipo_motor = [
    TipoMotor(nome='Elétrico'),
    TipoMotor(nome='Combustão')
]

veiculos = [
    Veiculos(
        marca_id=1,
        tipo_veiculo_id=1,
        modelo_id=1,
        categoria_id=1,
        transmissao_id=1,
        tipo_motor_id=2,
        passageiros=4,
        diaria=32.20,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/fiat500.png'
    ),
    Veiculos(
        marca_id=2,
        tipo_veiculo_id=1,
        modelo_id=2,
        categoria_id=2,
        transmissao_id=1,
        tipo_motor_id=1,
        passageiros=5,
        diaria=33.50,
        ult_revisao=date(2023, 8, 1),
        prox_revisao=date(2024, 8, 1),
        inspecao=date(2023, 10, 1),
        imagem_url='img/peugeot208.png'
    ),
    Veiculos(
        marca_id=3,
        tipo_veiculo_id=1,
        modelo_id=3,
        categoria_id=2,
        transmissao_id=1,
        tipo_motor_id=2,
        passageiros=5,
        diaria=38.450,
        ult_revisao=date(2024, 2, 1),
        prox_revisao=date(2025, 2, 1),
        inspecao=date(2023, 7, 1),
        imagem_url='img/fordfocus.png'
    ),
    Veiculos(
        marca_id=5,
        tipo_veiculo_id=1,
        modelo_id=4,
        categoria_id=2,
        transmissao_id=2,
        tipo_motor_id=1,
        passageiros=5,
        diaria=43.20,
        ult_revisao=date(2024, 2, 1),
        prox_revisao=date(2025, 2, 1),
        inspecao=date(2024, 6, 1),
        imagem_url='img/volkswagenid3.png'
    ),
    Veiculos(
        marca_id=3,
        tipo_veiculo_id=1,
        modelo_id=5,
        categoria_id=3,
        transmissao_id=1,
        tipo_motor_id=2,
        passageiros=5,
        diaria=60.11,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/fordkuga.png'
    ),
    Veiculos(
        marca_id=6,
        tipo_veiculo_id=1,
        modelo_id=6,
        categoria_id=4,
        transmissao_id=1,
        tipo_motor_id=2,
        passageiros=5,
        diaria=65.99,
        ult_revisao=date(2024, 6, 1),
        prox_revisao=date(2025, 6, 1),
        inspecao=date(2023, 8, 1),
        imagem_url='img/audia3.png'
    ),
    Veiculos(
        marca_id=7,
        tipo_veiculo_id=1,
        modelo_id=7,
        categoria_id=4,
        transmissao_id=2,
        tipo_motor_id=1,
        passageiros=5,
        diaria=68.70,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/teslamodel3.png'
    ),
    Veiculos(
        marca_id=4,
        tipo_veiculo_id=1,
        modelo_id=8,
        categoria_id=5,
        transmissao_id=2,
        tipo_motor_id=2,
        passageiros=4,
        diaria=72.32,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/minicooper.png'
    ),
    Veiculos(
        marca_id=8,
        tipo_veiculo_id=1,
        modelo_id=9,
        categoria_id=6,
        transmissao_id=1,
        tipo_motor_id=2,
        passageiros=7,
        diaria=291.55,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/citroenc4.png'
    ),
    Veiculos(
        marca_id=9,
        tipo_veiculo_id=1,
        modelo_id=10,
        categoria_id=4,
        transmissao_id=2,
        tipo_motor_id=2,
        passageiros=8,
        diaria=396.97,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/mercedesbenzclass.png'
    ),
    Veiculos(
        marca_id=10,
        tipo_veiculo_id=2,
        modelo_id=11,
        categoria_id=7,
        transmissao_id=1,
        tipo_motor_id=2,
        passageiros=2,
        diaria=26.65,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/hondapcx125.png'
    ),
    Veiculos(
        marca_id=11,
        tipo_veiculo_id=2,
        modelo_id=12,
        categoria_id=7,
        transmissao_id=2,
        tipo_motor_id=1,
        passageiros=2,
        diaria=41.80,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/bmwc400gt.png'
    ),
    Veiculos(
        marca_id=11,
        tipo_veiculo_id=2,
        modelo_id=13,
        categoria_id=8,
        transmissao_id=2,
        tipo_motor_id=2,
        passageiros=2,
        diaria=84.55,
        ult_revisao=date(2024, 5, 1),
        prox_revisao=date(2025, 5, 1),
        inspecao=date(2023, 12, 1),
        imagem_url='img/bmwr1250gs.png'
    )
]

session.add_all(tipo_veiculo)
session.add_all(marca)
session.add_all(modelo)
session.add_all(categoria)
session.add_all(transmissao)
session.add_all(tipo_motor)
session.add_all(veiculos)
session.commit()
session.close()
