from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, VARCHAR    #import used types
from sqlalchemy.orm import declarative_base, sessionmaker

from utils import fanymodules as fm    #my own "lib"

from datetime import datetime    #import day and hour

from colorama import init, Back, Style    #colors
init()


DATABASE_URL = "postgresql+psycopg2://postgres:cttdavi2602@localhost:5432/postgres"
# postgresql+psycopg2://usuario:senha@localhost:5432/your_database


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()



#------------------- MENU -------------------

def menu():
    print(f'{Back.CYAN}========== MENU =========={Style.RESET_ALL}')
    print('1 - registrar produto')
    print('2 - registrar venda')
    print('3 - retirar produto')
    print('4 - verificar estoque')
    print('5 - encerrar o programa')

    while True:
        try:
            choice = int(input(f'\nDigite a opção aqui (número): '))
            while choice not in (1, 2, 3, 4, 5):
                choice = int(input(f'{Back.YELLOW}Por favor, digite uma opção válida (1 | 2 | 3 | 4 | 5)!{Style.RESET_ALL} '))
            return choice
        except ValueError:
            print(f'{Back.YELLOW}Por favor, digite uma opção válida!{Style.RESET_ALL}')



#------------------- CLASSES -------------------

class StockTable(Base):   # class is mandatory with database
    __tablename__ = 'estoque'   # create table estoque
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    quantity = Column(Integer)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    profit_reais = Column(Float)
    profit_percent = Column(Float)
    date_of_purchase = Column(TIMESTAMP)

Base.metadata.create_all(engine)



class SalesTable(Base):   # class is mandatory with database
    __tablename__ = 'vendas'   # create table vendas
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    sale_price = Column(Float)
    sale_profit = Column(Float)
    profitsale_percent = Column(Float)
    quantity = Column(Integer)
    date_of_sale = Column(TIMESTAMP)

Base.metadata.create_all(engine)



class ExcludeTable(Base):   # class is mandatory with database
    __tablename__ = 'retirados'   # create table retirados
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    purchase_price = Column(Float)
    quantity = Column(Integer)
    reason = Column(String)
    date_of_exclude = Column(TIMESTAMP)

Base.metadata.create_all(engine)



#------------------- FUNÇÕES -------------------

def option_1():  # register product
    while True:
        
        while True:
            product = input(f'\nDigite o nome do novo produto: ').strip().title()   # product validation
            if product.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um nome de produto válido!{Style.RESET_ALL}')


        while True:
            product_type = input('Digite o tipo do produto: ').strip().title()  # type validation
            if product_type.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um tipo de produto válido!{Style.RESET_ALL}')


        size = input(f'Digite o tamanho do produto: ').strip().upper()  # size


        while True:
            try:
                quantity = int(input(f'Digite a quantidade de {product}: '))    # quantity validation
                if quantity < 1 or quantity > 120:
                    print(f'{Back.YELLOW}Por favor, digite uma quantidade válida (1 - 120)!{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Por favor, digite uma quantidade válida!{Style.RESET_ALL}')


        while True:
            try:
                purchase_price = float(input(f'Digite o preço de compra unitário de {product}: '))  # purchase_price validation
                if purchase_price < 0.1 or purchase_price > 1000:
                    print(f'{Back.YELLOW}Por favor, digite um preço válido (0.1 - 1000)!{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Por favor, digite um preço válido!{Style.RESET_ALL}')


        while True:
            try:
                sale_price = float(input(f'Digite o preço de venda unitário de {product}: '))   # sale_price validation
                if sale_price < 0.1 or sale_price > 1000:
                    print(f'{Back.YELLOW}Por favor, digite um preço válido (0.1 - 1000)!{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Por favor, digite um preço válido!{Style.RESET_ALL}')


        profit_reais = sale_price - purchase_price  # profit reais


        profit_percent = (sale_price - purchase_price) / sale_price * 100   # profit percent


        date_of_purchase = datetime.now()   # date


        session = Session()  #create session


        try:
            new_record = StockTable(product=product, product_type=product_type, size=size, quantity=quantity,
                                    purchase_price=purchase_price, sale_price=sale_price,
                                    profit_reais=profit_reais, profit_percent=profit_percent, date_of_purchase=date_of_purchase)
            
            session.add(new_record)
            session.commit()     # enter in PostgreSQL
            print(f'{Back.GREEN}Produto registrado com sucesso na tabela estoque!{Style.RESET_ALL}')
        except Exception as error:
            session.rollback()
            print(f'{Back.RED}ERRO: {error}{Style.RESET_ALL}')
            
        finally:
            session.close()


        if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
            break




def option_2():  # register sale
    while True:
        
        while True:
            product = input(f'\nDigite o nome do produto vendido: ').strip().title()    # product validation
            if product.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um nome de produto válido!{Style.RESET_ALL}')


        while True:
            product_type = input('Digite o tipo do produto: ').strip().title()  # product type validation
            if product_type.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um tipo de produto válido!{Style.RESET_ALL}')


        size = input(f'Digite o tamanho do produto: ').strip().upper()  # size


        while True:
            try:
                sale_price = float(input(f'Digite o preço vendido de {product}: '))     # sale_price validation
                if sale_price < 1 or sale_price > 1000:
                    print(f'{Back.YELLOW}Por favor, digite um preço válido (1 - 1000)!{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Por favor, digite um preço válido!{Style.RESET_ALL}')


        while True:
            try:
                quantity = int(input(f'Digite a quantidade de {product}: '))    # quantity validation
                if quantity < 1 or quantity > 120:
                    print(f'{Back.YELLOW}Por favor, digite uma quantidade válida (1 - 120)!{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Por favor, digite uma quantidade válida!{Style.RESET_ALL}')


        date_of_sale = datetime.now()   # date


        session = Session()  #create session


        # search item in stock
        stock_item = session.query(StockTable).filter_by(
            product=product,
            product_type=product_type,
            size=size
            ).first()


        # check if exist
        if not stock_item:
            print(f'{Back.RED}ERRO: {product} {product_type} {size} NÃO existe no estoque.{Style.RESET_ALL}')
            session.close()

            if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                break
            else:
                continue


        # check if quantity is enough
        if stock_item.quantity < quantity:
            print(f'{Back.RED}ERRO: Você tentou vender {quantity}, mas só tem {stock_item.quantity} no estoque.{Style.RESET_ALL}')
            session.close()

            if fm.get_repeat_product() == 'não':    # verify if the program will repeat or no
                break
            else:
                continue


        sale_profit = sale_price - stock_item.purchase_price    # create sale_profit
        
        if sale_price > stock_item.purchase_price:
            print(f'{Back.GREEN}lucro de: {sale_profit} reais por item {Style.RESET_ALL}') 
            print(f'{Back.GREEN}lucro total de: {sale_profit * quantity} reais {Style.RESET_ALL}')   
        else:
            print(f'{Back.RED}perda de: {sale_profit} reais por item {Style.RESET_ALL}')
            print(f'{Back.RED}perda total de: {sale_profit * quantity} reais {Style.RESET_ALL}')  
   

        profitsale_percent = (sale_price - stock_item.purchase_price) / sale_price * 100    # profit per product with percent 


        stock_item.quantity = stock_item.quantity - quantity    # update quantity


        if stock_item.quantity == 0:    # Remove if 0
            session.delete(stock_item)


        try:
            new_record = SalesTable(product=product, product_type=product_type, size=size, sale_price=sale_price,
                                    sale_profit=sale_profit, profitsale_percent=profitsale_percent, quantity=quantity,
                                    date_of_sale=date_of_sale)
            
            session.add(new_record)
            session.commit()    # enter in PostgreSQL
            print(f'{Back.GREEN}Venda registrada com sucesso na tabela vendas!{Style.RESET_ALL}')
        except Exception as error:
            session.rollback()
            print(f'{Back.RED}ERRO: {error}{Style.RESET_ALL}')
            
        finally:
            session.close()


        if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
            break




def option_3():  # delete product
    while True:
        
        while True:
            product = input(f'\nDigite o produto que deseja retirar: ').strip().title()    # product validation
            if product.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um nome de produto válido!{Style.RESET_ALL}')


        while True:
            product_type = input('Digite o tipo do produto: ').strip().title()  # product type validation
            if product_type.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um tipo de produto válido!{Style.RESET_ALL}')


        size = input(f'Digite o tamanho do produto: ').strip().upper()    # size


        while True:
            try:
                quantity = int(input(f'Digite a quantidade de {product}: '))    # quantity validation
                if quantity < 1 or quantity > 100:
                    print(f'{Back.YELLOW}Por favor, digite uma quantidade válida (1 - 100)!{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Por favor, digite uma quantidade válida!{Style.RESET_ALL}')


        reason = input('Digite o motivo da retirada: ').strip().capitalize()    # reason
        
        
        date_of_exclude = datetime.now()    # date
        
        
        session = Session()  #create session


        # search item in stock
        stock_item = session.query(StockTable).filter_by(
            product=product,
            product_type=product_type,
            size=size
            ).first()
        
        
        # check if exist
        if not stock_item:
            print(f'{Back.RED}ERRO: {product} {product_type} {size} NÃO existe no estoque.{Style.RESET_ALL}')
            session.close()
            
            if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                break
            else:
                continue


        # check if quantity is enough
        if stock_item.quantity < quantity:
            print(f'{Back.RED}ERRO: Você tentou retirar {quantity}, mas só tem {stock_item.quantity} no estoque.{Style.RESET_ALL}')
            session.close()
            
            if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                break
            else:
                continue


        stock_item.quantity = stock_item.quantity - quantity    # update quantity
        
        
        purchase_price = stock_item.purchase_price      # pick up purchase price
        print(f'{Back.RED}perda de: {purchase_price} reais por item {Style.RESET_ALL}')
        print(f'{Back.RED}perda total de: {purchase_price * quantity} reais {Style.RESET_ALL}') 


        if stock_item.quantity == 0:    # Remove if 0
            session.delete(stock_item)


        try:
            new_record = ExcludeTable(product=product, product_type=product_type, size=size,
                                      purchase_price=purchase_price, quantity=quantity,
                                      reason=reason, date_of_exclude=date_of_exclude)
            
            session.add(new_record)
            session.commit()    # enter in PostgreSQL
            print(f'{Back.GREEN}Produto registrado com sucesso na tabela retirados!{Style.RESET_ALL}')
        except Exception as error:
            session.rollback()
            print(f'{Back.RED}ERRO: {error}{Style.RESET_ALL}')

        finally:
            session.close()


        if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                break
        else:
            continue



def option_4():  # check item
    while True:

        while True:
            product = input(f'\nDigite o nome do produto que deseja verificar: ').strip().title()   # product validation
            if product.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um nome de produto válido!{Style.RESET_ALL}')


        while True:
            product_type = input('Digite o tipo do produto a ser verificado: ').strip().title()    # product_type validation
            if product_type.replace(' ', '').isalpha():
                break
            else:
                print(f'{Back.YELLOW}Por favor, digite um tipo de produto válido!{Style.RESET_ALL}')


        size = input(f'Digite o tamanho do produto a ser verificado: ').strip().upper()    # size


        session = Session()  #create session


        # search item in stock
        stock_item = session.query(StockTable).filter_by(
            product=product,
            product_type=product_type,
            size=size
            ).first()


        # if exist
        if stock_item:
            print(f'{Back.GREEN}{product} {product_type} {size} existe no estoque com {stock_item.quantity} peças.{Style.RESET_ALL}')


        # if not exist
        else:
            print(f'{Back.RED}{product} {product_type} {size} NÃO existe no estoque.{Style.RESET_ALL}')
        session.close()
        
        
        if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
            break



#------------------- MAIN LOOP -------------------

while True:
    choice = menu()

    if choice == 1:   # register product 
        option_1()

    elif choice == 2:   # register sale  
        option_2()

    elif choice == 3:   # register exclusion
        option_3()

    elif choice == 4:   # check if product in StockTable
        option_4()


    else:
        print(f'\n{Back.WHITE}======= PROGRAMA ENCERRADO ======={Style.RESET_ALL}')
        break


    rep = input(f'\nVocê quer retornar ao menu? (sim/não): ').strip().lower()  # verify if the program will repeat or no
    while rep not in ('sim', 'não'):
        rep = input(f'{Back.YELLOW}Por favor, digite uma opção válida (sim/não): {Style.RESET_ALL}').strip().lower()

    if rep == 'não':
        print(f'\n{Back.WHITE}======= PROGRAMA ENCERRADO ======={Style.RESET_ALL}')
        break 