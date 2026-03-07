from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, VARCHAR    # import used types
from sqlalchemy.orm import declarative_base, sessionmaker

import os   #clear screen

from utils import fanymodules as fm    # my own "lib"

from datetime import datetime    # import day and hour

from tabulate import tabulate   # print a beautiful table

from colorama import init, Back, Style    # colors
init()


DATABASE_URL = # postgresql+psycopg2://usuario:senha@localhost:5432/your_database


engine = create_engine(DATABASE_URL)   # connect with the database
Session = sessionmaker(bind=engine)
Base = declarative_base()



#------------------- MENU -------------------

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')    #clear screen


def menu():
    clear_screen()
    print(f'{Back.CYAN}========== M E N U =========={Style.RESET_ALL}')
    print('0 - encerrar programa')
    print('1 - registrar produto')
    print('2 - registrar venda')
    print('3 - retirar produto')
    print('4 - verificar peça no estoque')
    print('5 - verificar alertas')
    print('6 - verificar resultados')
    print('7 - verificar tabelas')


    while True:
        try:
            choice = int(input(f'\nDigite a opção aqui (número): '))
            while choice not in (0, 1, 2, 3, 4, 5, 6, 7):
                choice = int(input(f'{Back.YELLOW}Por favor, digite uma opção válida (0 | 1 | 2 | 3 | 4 | 5 | 6 | 7)!{Style.RESET_ALL} '))
            return choice
        except ValueError:
            print(f'{Back.YELLOW}Por favor, digite uma opção válida!{Style.RESET_ALL}')



#------------------- CLASSES -------------------

class StockTable(Base):   # class is mandatory with database
    __tablename__ = 'estoque'   # creating table estoque
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    quantity = Column(Integer)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    profit_reais = Column(Float)
    profit_percent = Column(Float)
    date = Column(TIMESTAMP)



class SalesTable(Base):   # class is mandatory with database
    __tablename__ = 'vendas'   # creating table vendas
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    quantity = Column(Integer)
    sale_unit_price = Column(Float)
    sale_total_price = Column(Float)
    sale_profit = Column(Float)
    profitsale_percent = Column(Float)
    date = Column(TIMESTAMP)



class ExcludeTable(Base):   # class is mandatory with database
    __tablename__ = 'retirados'   # creating table retirados
    id = Column(Integer, primary_key=True)
    product = Column(String)
    product_type = Column(String)
    size = Column(VARCHAR)
    unit_prejudice = Column(Float)
    total_prejudice = Column(Float)
    quantity = Column(Integer)
    reason = Column(String)
    date = Column(TIMESTAMP)


Base.metadata.create_all(engine) # create all tables in database



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


        with Session() as session:  #create session

            existing_product = session.query(StockTable).filter_by(     # verify if product already exists using the variables below
                    product=product,
                    product_type=product_type,
                    size=size
                ).first()


            if existing_product:    # if product already exists, just update the quantity
                existing_product.quantity = existing_product.quantity + quantity
                session.commit()
                print(f'{Back.GREEN}Produto já em estoque! Quantidade atualizada para {existing_product.quantity}!{Style.RESET_ALL}')


            else:    # if not, create new register
                
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


                date = datetime.now()   # date
            
            
                try:
                    new_record = StockTable(product=product, product_type=product_type, size=size, quantity=quantity,
                                            purchase_price=purchase_price, sale_price=sale_price,
                                            profit_reais=profit_reais, profit_percent=profit_percent, date=date)
                        
                    session.add(new_record)
                    session.commit()     # enter in PostgreSQL
                    print(f'{Back.GREEN}Produto registrado com sucesso na tabela estoque!{Style.RESET_ALL}')
                    
                except Exception as error:
                    session.rollback()
                    print(f'{Back.RED}ERRO: {error}{Style.RESET_ALL}')
                


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
                sale_unit_price = float(input(f'Digite o preço vendido de {product}: '))     # sale_price validation
                if sale_unit_price < 1 or sale_unit_price > 1000:
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


        sale_total_price = sale_unit_price * quantity   #total sale price
        
        
        date = datetime.now()   # date


        with Session() as session:  #create session


            # search item in stock
            stock_item = session.query(StockTable).filter_by(
                product=product,
                product_type=product_type,
                size=size
                ).first()


            # check if exist
            if not stock_item:
                print(f'{Back.RED}ERRO: {product} {product_type} {size} NÃO existe no estoque.{Style.RESET_ALL}')

                if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                    break
                else:
                    continue


            # check if quantity is enough
            if stock_item.quantity < quantity:
                print(f'{Back.RED}ERRO: Você tentou vender {quantity}, mas só tem {stock_item.quantity} no estoque.{Style.RESET_ALL}')

                if fm.get_repeat_product() == 'não':    # verify if the program will repeat or no
                    break
                else:
                    continue


            sale_profit = sale_total_price - stock_item.purchase_price * quantity   # create sale_profit
            
            
            if sale_unit_price > stock_item.purchase_price:
                print(f'{Back.GREEN}lucro de: {sale_profit / quantity} reais por item {Style.RESET_ALL}')
                print(f'{Back.GREEN}lucro total de: {sale_profit} reais {Style.RESET_ALL}')
            else:
                print(f'{Back.RED}perda de: {sale_profit / quantity} reais por item {Style.RESET_ALL}')
                print(f'{Back.RED}perda total de: {sale_profit} reais {Style.RESET_ALL}')  
    

            profitsale_percent = (sale_unit_price - stock_item.purchase_price) / sale_unit_price * 100    # profit per product with percent 


            stock_item.quantity = stock_item.quantity - quantity    # update quantity


            if stock_item.quantity == 0:    # Remove if 0
                session.delete(stock_item)


            try:
                new_record = SalesTable(product=product, product_type=product_type, size=size, quantity=quantity, sale_unit_price=sale_unit_price,
                                        sale_total_price=sale_total_price,sale_profit=sale_profit, 
                                        profitsale_percent=profitsale_percent, date=date)
                
                session.add(new_record)
                session.commit()    # enter in PostgreSQL
                print(f'{Back.GREEN}Venda registrada com sucesso na tabela vendas!{Style.RESET_ALL}')
            except Exception as error:
                session.rollback()
                print(f'{Back.RED}ERRO: {error}{Style.RESET_ALL}')


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
        
        
        date = datetime.now()    # date
        
        
        with Session() as session:  #create session


            # search item in stock
            stock_item = session.query(StockTable).filter_by(
                product=product,
                product_type=product_type,
                size=size
                ).first()
            
            
            # check if exist
            if not stock_item:
                print(f'{Back.RED}ERRO: {product} {product_type} {size} NÃO existe no estoque.{Style.RESET_ALL}')
                
                if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                    break
                else:
                    continue


            # check if quantity is enough
            if stock_item.quantity < quantity:
                print(f'{Back.RED}ERRO: Você tentou retirar {quantity}, mas só tem {stock_item.quantity} no estoque.{Style.RESET_ALL}')
                
                if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
                    break
                else:
                    continue


            stock_item.quantity = stock_item.quantity - quantity    # update quantity
            
            
            total_prejudice = stock_item.purchase_price * quantity 
            unit_prejudice = total_prejudice / quantity     
            
            print(f'{Back.RED}perda de: {unit_prejudice} reais por item {Style.RESET_ALL}')
            print(f'{Back.RED}perda total de: {total_prejudice} reais {Style.RESET_ALL}') 
            
            
            if stock_item.quantity == 0:    # Remove if 0
                session.delete(stock_item)


            try:
                new_record = ExcludeTable(product=product, product_type=product_type, size=size, unit_prejudice=unit_prejudice,
                                        total_prejudice=total_prejudice, quantity=quantity,
                                        reason=reason, date=date)
                
                session.add(new_record)
                session.commit()    # enter in PostgreSQL
                print(f'{Back.GREEN}Produto registrado com sucesso na tabela retirados!{Style.RESET_ALL}')
            except Exception as error:
                session.rollback()
                print(f'{Back.RED}ERRO: {error}{Style.RESET_ALL}')


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


        with Session() as session:  #create session


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


        if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
            break   



def option_5():  # alerts 
    
    with Session() as session:  #create session
        
        stock_item = session.query(StockTable).all()  #stock_item = all in StockTable
            
        if stock_item:
            print(f'{Back.YELLOW}============= ALERTAS ============={Style.RESET_ALL}')
                
            for i in stock_item:
                if i.quantity < 5:
                    print(f'\n{Back.RED}O produto {i.product} {i.product_type} tamanho {i.size} só contem {i.quantity} unidades{Style.RESET_ALL}')
            
        else:
            print(f'\n{Back.GREEN}Não existem alertas no momento{Style.RESET_ALL}')
    
    
    
def option_6():  # results
    while True:
        
        while True:
            try:
                # taking start date
                start = input('Digite a data inicial (DD/MM/YYYY): ').strip()
                start_date = datetime.strptime(start, '%d/%m/%Y')  # converts to datetime
                break
            except ValueError:
                print(f'{Back.YELLOW}Data inválida! Use o formato DD/MM/YYYY.{Style.RESET_ALL}')


        while True:
            try:
                # taking final date
                end = input('Digite a data final (DD/MM/YYYY): ').strip()
                end_date = datetime.strptime(end, "%d/%m/%Y")  # convert to datetime

                # validation if final date is after start date
                if end_date < start_date:
                    print(f'{Back.YELLOW}A data final deve ser igual ou posterior a data inicial.{Style.RESET_ALL}')
                    continue
                break
            except ValueError:
                print(f'{Back.YELLOW}Data inválida! Use o formato DD/MM/YYYY.{Style.RESET_ALL}')


        with Session() as session:  # create session
        
        
            # taking sales in the period
            sales = session.query(SalesTable).filter(
                SalesTable.date >= start_date,
                SalesTable.date <= end_date
            ).all()
            
            
            # taking exclude in the period
            prejudice = session.query(ExcludeTable).filter(
                ExcludeTable.date >= start_date,
                ExcludeTable.date <= end_date
            ).all()

            
            if not sales:
                print(f'{Back.RED}Não há vendas nesse período.{Style.RESET_ALL}')
            else:
                # calculate profit
                total_profit = sum(s.sale_profit for s in sales)    # sum of all sale_profit in SalesTable
                total_prejudice_value = sum(p.total_prejudice for p in prejudice)   # sum of all total_prejudice in ExcludeTable
                
                total_profit = total_profit - total_prejudice_value
                
                total_sale = sum(s.sale_total_price for s in sales)
                
                
                print(f'{Back.GREEN}Total vendido nesse período: R${total_sale:.2f}{Style.RESET_ALL}')
                print(f'{Back.RED}Perda total com produtos retirados nesse período: R${total_prejudice_value:.2f}{Style.RESET_ALL}')
                print(f'{Back.GREEN}Lucro total nesse período: R${total_profit:.2f}{Style.RESET_ALL}')
            
                
        if fm.get_repeat_product() == 'não':   # verify if the program will repeat or no
            break   



def option_7():  # tables
    while True:
        
        table_choice = input('Qual tabela você deseja ver (estoque, vendas, retirados): ').strip().lower()
        while table_choice not in ('estoque', 'retirados', 'vendas'):
            table_choice = input(f'{Back.YELLOW}insira uma opção de tabela válida para vizualização: {Style.RESET_ALL}')
            
            
        with Session() as session:  # create session
            
            
            # table choice
            if table_choice == 'estoque':
                table_class = StockTable
                
            elif table_choice == 'vendas':
                table_class = SalesTable
                
            else:
                table_class = ExcludeTable
                
            
            while True:
                try:
                    # taking start date
                    start = input('Digite a data inicial (DD/MM/YYYY): ').strip()
                    start_date = datetime.strptime(start, '%d/%m/%Y')  # convert to datetime
                    break
                except ValueError:
                    print(f'{Back.YELLOW}Data inválida! Use o formato DD/MM/YYYY.{Style.RESET_ALL}')


            while True:
                try:
                    # taking final date
                    end = input('Digite a data final (DD/MM/YYYY): ').strip()
                    end_date = datetime.strptime(end, "%d/%m/%Y")  # convert to datetime

                    # validation if final date is after start date
                    if end_date < start_date:
                        print(f'{Back.YELLOW}A data final deve ser igual ou posterior a data inicial.{Style.RESET_ALL}')
                        continue
                    break
                except ValueError:
                    print(f'{Back.YELLOW}Data inválida! Use o formato DD/MM/YYYY.{Style.RESET_ALL}')
                
                
            records_period = session.query(table_class).filter(
                table_class.date >= start_date,
                table_class.date <= end_date
                ).all()
            
            
            if not records_period:
                print(f'\n{Back.YELLOW}Nenhum registro encontrado na tabela {table_class.__tablename__} nesse período!{Style.RESET_ALL}')
                if fm.get_repeat_product() == 'sim':   # verify if the program will repeat or no   
                    continue
                else:
                    return


            print(f'\n{Back.CYAN}================== TABELA {table_class.__tablename__.upper()} =================={Style.RESET_ALL}')
            print(f'{start_date} <-----> {end_date}')
            
            
            # take Columns name
            columns = table_class.__table__.columns.keys()  # __table__ is a entire table in SQLAlchemy and columns.keys() return a list with columns name
            
            
            # create data list
            table_data = []


            for r in records_period:
                row = []  # create empty list

                for col in columns:  # go through each column name
                    value = getattr(r, col)  # get the value of that column
                    row.append(value)  # add the value to the row
                    
                table_data.append(row)  # add the row to the table data

            # showing the table
            print(tabulate(table_data, headers=columns, tablefmt="fancy_grid"))
            
            
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
        
    elif choice == 5:   # check alerts
        option_5()
        
    elif choice == 6:   # check results
        option_6()
        
    elif choice == 7:   # check tables
        option_7()


    else:
        print(f'\n{Back.WHITE}======= PROGRAMA ENCERRADO ======={Style.RESET_ALL}')
        break


    rep = input(f'\nVocê quer retornar ao menu? (sim/não): ').strip().lower()  # verify if the program will repeat or no
    while rep not in ('sim', 'não'):
        rep = input(f'{Back.YELLOW}Por favor, digite uma opção válida (sim/não): {Style.RESET_ALL}').strip().lower()

    if rep == 'não':
        print(f'\n{Back.WHITE}======= PROGRAMA ENCERRADO ======={Style.RESET_ALL}')

        break
