from django.shortcuts import redirect,render,HttpResponse
from urllib.request import urlopen
import json 
from pprint import pprint
from operator import itemgetter


def index(request):
    #Información para el gráfico de arriendos
    rentsLabels = []
    rentsData = []
    rents = getCompaniesSortByProfits()

    for rent in rents:
        rentsLabels.append(rent['name'])
        rentsData.append(rent['profits'])
    #---------------------------------
    sumRentsAmount = 0
    for amoun in rentsData:
        sumRentsAmount += amoun

    totalRents = len(allRents())
    totalClients = len(getClientIds())
    totalCompanies = len(rentsLabels)

    context = {
            'totalRents'    : totalRents,
            'totalClients'  : totalClients,
            'sumRentsAmount': sumRentsAmount,
            'totalCompanies': totalCompanies,
            'rentsLabels'   : rentsLabels,
            'rentsData'     : rentsData, 
        }
    return render(request, 'home.html', context)



def clients(request):
    context = {
            'clients' : getClientIds(),
        }
    return render(request, 'clients/all_clients.html', context)



def companies(request):
    context = {
            'companies' : getCompanyIds(),
        }
    return render(request, 'companies/all_companies.html', context)



def rents(request):
    context = {
            'rents' : allRents(),
        }
    return render(request, 'rents/all_rents.html', context)



def allRents():
    rents = getRentIds()
    clients = getClientIds()
    companies = getCompanyIds()

    allRents = []

    for rent in rents:
        nameCompany = ''
        nameClient = ''
        totalCostRent = 0
        companyId = ''
        clientId = ''

        for company in companies:
            if rent['empresa'] == company['id']:
                nameCompany = company['name']
                companyId = company['id']

        for client in clients:
            if rent['cliente'] == client['id']:
                nameClient = client['name']
                clientId = client['id']

        totalCostRent = rent['dias'] * rent['costo_diario']
        allRents.append({
                                'id'       : rent['id'],
                                'company'  : nameCompany,
                                'companyId': companyId,
                                'client'   : nameClient,
                                'clientId' : clientId,
                                'cantDays' : rent['dias'],
                                'costDay'  : rent['costo_diario'],
                                'totalCostRent': totalCostRent
                            })
        nameCompany = ''
        nameClient = ''
        totalCostRent = 0
        companyId = ''
        clientId = ''

    return allRents



def funtionsResult(request, idFuntion):
    if idFuntion == 1:
        context = {
            'result' :  getClientIds(),
        }
        return render(request, 'funtionsResult/funtion1.html', context)
    elif idFuntion == 2:
        context = {
            'result' :  getClientByLastName(),
        }
        return render(request, 'funtionsResult/funtion2.html', context)
    elif idFuntion == 3:
        context = {
            'result' :  getClientsSortByRentExpenses(),
        }
        return render(request, 'funtionsResult/funtion3.html', context)
    elif idFuntion == 4:
        context = {
            'result' :  getCompanyClientsSortByName(),
        }
        return render(request, 'funtionsResult/funtion4.html', context)
    elif idFuntion == 5:
        return render(request, 'funtionsResult/funtion5.html')
    elif idFuntion == 6:
        context = {
            'result' :  getCompaniesSortByProfits(),
        }
        return render(request, 'funtionsResult/funtion6.html', context)
    elif idFuntion == 7:
        context = {
            'result' :  getCompaniesWithRentsOver1Week(),
        }
        return render(request, 'funtionsResult/funtion7.html', context)
    elif idFuntion == 8:
        context = {
            'result' :  getClientsWithLessExpense(),
        }
        return render(request, 'funtionsResult/funtion8.html', context)
    elif idFuntion == 9:
        context = {
            'result' :  newClientRanking(),
        }
        return render(request, 'funtionsResult/funtion9.html', context)


# ================= FUNCIONES ============================
#1.- Lista de clientes
def getClientIds():
    #Obtenemos los datos de los clientes
    url_client = 'http://localhost:8000/api/arriendo-autos/cliente/'
    response_client = urlopen(url_client)
    all_clients = json.loads(response_client.read())

    #pprint(all_clients)
    return  all_clients



def getCompanyIds():
    #Obtenemos los datos de las empresas
    url_company = 'http://localhost:8000/api/arriendo-autos/empresa/'
    response_company = urlopen(url_company)
    all_companies = json.loads(response_company.read())

    #pprint(all_companies)
    return  all_companies



def getRentIds():
    #Obtenemos los datos de los arriendos
    url_rent = 'http://localhost:8000/api/arriendo-autos/arriendo/'
    response_rent = urlopen(url_rent)
    all_rent = json.loads(response_rent.read())

    #pprint(all_rent)
    return  all_rent


#2.- Ids clientes ordenados por apellido
def getClientByLastName():
    clients = getClientIds()
    clientsLastName = []

    for client in clients:
        for i in client['name']:
            name = client['name'].split()
        clientsLastName.append({
            'id' : client['id'],
            'lastName' : name[1]
        })

    clientsOrderByLastName = sorted(clientsLastName, key=lambda x: x["lastName"])
    return clientsOrderByLastName



#3.- Clientes ordenados decrecientemente por la suma total de gasto en arriendo
def getClientsSortByRentExpenses():
    clients = getClientIds()
    rents =  getRentIds()
    clientsExpenses = []
    clientsSortByRentExpenses = []

    for client in clients:
        clientsExpenses.append({ 
                                "id" : client['id'],
                                "rut": client['rut'],
                                "name" : client['name'], 
                                "expenses" : 0
                                })

    for rent in rents:
        for client in clientsExpenses:
            if client['id'] == rent['cliente']:
                sum = rent['costo_diario'] * rent['dias']
                client['expenses'] += sum

    clientsExpensesDesc = sorted(clientsExpenses, key = itemgetter('expenses'), reverse=True)

    for client in clientsExpensesDesc:
        clientsSortByRentExpenses.append({
                                        "name" : client['name'], 
                                        "expenses" : client['expenses']  
                                        })                
    return clientsSortByRentExpenses



#4.- Diccionario empresas y sus clientes por rut ordenados por nombres
def getCompanyClientsSortByName():
    companies = getCompanyIds()
    rents =  getRentIds()
    clients = getClientIds()
    companyClientsSortByName = {}
    companyClients = []


    #Todas la empresas con los ids de sus clientes
    for company in companies:
        companyClients.append({
                                "id" : company['id'],
                                "name" : company['name'],
                                "clientsIdList" : [],
                                "clients" : [],
                                "clientsOrderByName" : []
                                })
        for rent in rents:
            for company in companyClients:
                if company['id'] == rent['empresa'] and not rent['cliente'] in company['clientsIdList']:
                    company['clientsIdList'].append(rent['cliente'])
                    

    #Se agregan todos los datos de los clientes
    for company in companyClients:
        for id in company['clientsIdList']:
            for client in clients:
                if client['id'] == id:
                    company['clients'].append(client)
    

    #Se agrega todos los cliente ordenados por nombre
    for company in companyClients:
        data = company['clients']
        OrderByName = sorted(data, key=lambda x: x["name"])
        company['clientsOrderByName'].append(OrderByName)

    #Se agregan al diccionario companyClientsSortByName 'nombre empresa' : [ruts]
    for company in companyClients:
        ruts = []
        itera = 0
        for client in company['clientsOrderByName'][itera]:
            ruts.append(client['rut'])
            itera = itera + 1
    
        companyClientsSortByName[company['name']] = ruts 
                                        
    return companyClientsSortByName


#5.-
def getClientsSortByAmount(id_empresa):
    return 'Función 5'


#Función n° 6 
def getCompaniesSortByProfits():
    companies = getCompanyIds()
    rents = getRentIds()
    companiesProfits = []

    for company in companies:
        companiesProfits.append({ 
                                "id" : company['id'],
                                "name" : company['name'], 
                                "profits" : 0
                                })

    for rent in rents:
        for company in companiesProfits:
            if company['id'] == rent['empresa']:
                sum = rent['costo_diario'] * rent['dias']
                company['profits'] += sum

    companiesSortByProfits = sorted(companiesProfits, key = itemgetter('profits'), reverse=False)
    return companiesSortByProfits


#Función n° 7 
def getCompaniesWithRentsOver1Week():
    companies = getCompanyIds()
    rents = getRentIds()
    RentsOver1Week = []
    CompaniesWithRentsOver1Week = {}

    for company in companies:
        RentsOver1Week.append({
                                "id" : company['id'],
                                "name" : company['name'], 
                                "rents" : 0
                            })

    for rent in rents:
        for company in RentsOver1Week:
            if company['id'] == rent['empresa'] and rent['dias'] >= 7:
                company['rents'] += 1

    for company in RentsOver1Week:
        CompaniesWithRentsOver1Week[company['name']] = company['rents']

    return CompaniesWithRentsOver1Week


#Función n° 8
def getClientsWithLessExpense():
    companies = getCompanyIds()
    rents = getRentIds()
    clientLessExpense = []
    clientsWithLessExpense = {}

    for company in companies:
        clientLessExpense.append({
                                'id' : company['id'],
                                'name' : company['name'],
                                'clients' : [] 
                                })
    #Todos los arriendos por empresa
    for rent in rents:
        for company in clientLessExpense: 
            if company['id'] == rent['empresa'] and not next((x for x in company['clients'] if x["id"] == rent['cliente']), None):
                company['clients'].append({
                                        'id' : rent['cliente'],
                                        'expense' : 0
                                        })
                nombre = company['name']                        
                print(f'Compañia : {nombre}')
                for client in company['clients']: 
                    if rent['cliente'] == client['id']:
                        sum = rent['costo_diario'] * rent['dias']
                        client['expense'] += sum
                    pprint(f'cliente : { client} ')        
                    
    return clientLessExpense



#9.-
def newClientRanking():
    pass