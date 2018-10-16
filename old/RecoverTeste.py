#!/usr/bin/python
# -*- coding: utf-8 -*-


import json, requests, urllib3, sys, os
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

# Desabilita erros de request, caso exista
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
now = datetime.now()

# Gerar a data de modificação
string = str(now)
dataMod = string.replace(" ","_")

# Função que abre e salva os dados no arquivo
def createDir(path,data):
    fileJSON = open(path,'w')
    fileJSON.write(data)
    fileJSON.close()

# Função que cria a pasta no diretório caso não exista
def saveDumps(path,data,NameDir):
    if os.path.isdir('/tmp/'+NameDir):
        createDir(path,data)
    else:
        os.system('mkdir /tmp/'+NameDir)
        createDir(path,data)

# Função que envia requisições gerais
def sendRequest(param, path, NameDir):
    dirName = NameDir
    response = requests.get('https://labisilon-mgr.rede.tst:8080'+param, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        data = response.content
        saveDumps(path, data, dirName)
    else:
        print("404 not found")

# Função que envia e salva os dados do groupnet
def sendRequestIdGroupNet(id,NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/3/network/groupnets/'+id, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/groupnet')):
            data = response.content
            path = '/tmp/'+NameDir+'/groupnet/'+id+'.json'
            saveDumps(path, data, NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/groupnet')
            data = response.content
            path = '/tmp/'+NameDir+'/groupnet/'+id+'.json'
            saveDumps(path, data, NameDir)
    else:
        # Groupnet não encontrado
        print("404 not found")

# Função que envia e salva os dados da subnet
def sendRequestSubnets(id_groupnet, subnet,NameDir):
    if subnet == None:
        subnet == ""
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/3/network/groupnets/'+id_groupnet+'/subnets/'+subnet, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/subnet')):
            data = response.content
            path = '/tmp/'+NameDir+'/subnet/'+subnet+'.json'
            saveDumps(path, data, NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/subnet')
            data = response.content
            path = '/tmp/'+NameDir+'/subnet/'+subnet+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Subnet não encontrado
        print('')

# Função que envia e salva os dados das pools
def sendRequestPools(id_groupnet,subnet_name, pool,NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/3/network/groupnets/'+id_groupnet+'/subnets/'+subnet_name+'/pools/'+pool, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/pools')):
            data = response.content
            path = '/tmp/'+NameDir+'/pools/'+pool+'.json'
            saveDumps(path, data,NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/pools')
            data = response.content
            path = '/tmp/'+NameDir+'/pools/'+pool+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Pool não encontrada
        print('')

# Função que envia e salva os dados das Rules
def sendRequestRules(id_groupnet,subnet_name,pool,rule,NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/3/network/groupnets/'+id_groupnet+'/subnets/'+subnet_name+'/pools/'+pool+'/rules/'+rule, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/rules')):
            data = response.content
            path = '/tmp/'+NameDir+'/rules/'+rule+'.json'
            saveDumps(path, data,NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/rules')
            data = response.content
            path = '/tmp/'+NameDir+'/rules/'+rule+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Rule não encontrada
        print('')

#______________________________________________________________Avaliar essa parte do Script______________________________________________________________________________

# Função que envia e salva os dados das Zones
def sendRequestZone(zoneName, NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/3/zones/'+zoneName, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/zones')):
            data = response.content
            path = '/tmp/'+NameDir+'/zones/'+zoneName+'.json'
            saveDumps(path, data,NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/zones')
            data = response.content
            path = '/tmp/'+NameDir+'/zones/'+zoneName+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Zone não encontrada
        print('')

# Função que envia e salva os dados de determinada SMB
def sendRequestSMB(name, NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/1/protocols/smb/shares/'+name, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/smb_export')):
            data = response.content
            path = '/tmp/'+NameDir+'/smb_export/'+name+'.json'
            saveDumps(path, data,NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/smb_export')
            data = response.content
            path = '/tmp/'+NameDir+'/smb_export/'+name+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Zone não encontrada
        print('')

# Função que envia e salva os dados de determinada NFS
def sendRequestNFS(name, NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/4/protocols/nfs/exports/'+str(name), auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/nfs_export')):
            data = response.content
            path = '/tmp/'+NameDir+'/nfs_export/'+str(name)+'.json'
            saveDumps(path, data,NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/nfs_export')
            data = response.content
            path = '/tmp/'+NameDir+'/nfs_export/'+str(name)+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Zone não encontrada
        print('')

# Função que executa a Zone
def executeZone(NameDir):

    zones = '/tmp/'+NameDir+'/zone_informations.json'
    sendRequest('/platform/3/zones/', zones,NameDir)

    # Salvar no disco
    arquivojson = open('/tmp/'+NameDir+'/zone_informations.json','r')
    dadosJson = json.load(arquivojson)
    total = len(dadosJson['zones'][0]['id'])
    x = 0
    while x < total:
        namezone = dadosJson['zones'][x]['name']
        sendRequestZone(namezone,NameDir)
        x+=1

# Função que executa o export do SMB
def executeSMB(NameDir):
    smb = '/tmp/'+NameDir+'/smb_export.json'
    sendRequest('/platform/1/protocols/smb/shares', smb,NameDir)

    # Salvar no disco
    arquivojson = open('/tmp/'+NameDir+'/smb_export.json','r')
    dadosJson = json.load(arquivojson)
    total = dadosJson['total']
    x = 0
    while x < total:
        smb_name = dadosJson['shares'][x]['name']
        sendRequestSMB(smb_name,NameDir)
        x+=1

# Função que executa o export do NFS
def executeNFS(NameDir):
    nfs = '/tmp/'+NameDir+'/nfs_export.json'
    sendRequest('/platform/4/protocols/nfs/exports', nfs,NameDir)

    # Salvar no disco
    arquivojson = open('/tmp/'+NameDir+'/nfs_export.json','r')
    dadosJson = json.load(arquivojson)
    total = dadosJson['total']
    x = 0
    while x < total:
        nfs_name = dadosJson['exports'][x]['id']
        sendRequestNFS(nfs_name,NameDir)
        x+=1

def getSmbCurrentZone(zoneName, NameDir):
    response = requests.get('https://labisilon-mgr.rede.tst:8080/platform/4/protocols/smb/shares?zone='+zoneName, auth=('root', 'laboratory'), verify=False)
    if response.status_code == 200:
        if(os.path.isdir('/tmp/'+NameDir+'/currentZone')):
            data = response.content
            path = '/tmp/'+NameDir+'/currentZone/'+zoneName+'.json'
            saveDumps(path, data,NameDir)
        else:
            os.system('mkdir /tmp/'+NameDir+'/currentZone')
            data = response.content
            path = '/tmp/'+NameDir+'/currentZone/'+zoneName+'.json'
            saveDumps(path, data,NameDir)
    else:
        # Zone não encontrada
        print('')

def executeSmbCurrentZone(NameDir):
    zones = '/tmp/'+NameDir+'/zone_informations.json'
    sendRequest('/platform/3/zones/', zones,NameDir)

    arquivojson = open('/tmp/'+NameDir+'/zone_informations.json','r')
    dadosJson = json.load(arquivojson)
    total = len(dadosJson['zones'][0]['id'])
    x = 0
    while x < total:
        namezone = dadosJson['zones'][x]['name']
        getSmbCurrentZone(namezone,NameDir)
        x+=1

def execute(NameDir):
    
    # Informações Gerais
    groupnet = '/tmp/'+NameDir+'/general_informations.json'
    sendRequest('/platform/3/network/groupnets', groupnet,NameDir)

    # Ler Arquivo json com dados da groupnet
    arquivo_json = open('/tmp/'+NameDir+'/general_informations.json','r') 
    dados_json = json.load(arquivo_json)

    # Informações da zone
    executeZone(NameDir)

    # Informações do SMB
    executeSMB(NameDir)

    # Informações do NFS
    executeNFS(NameDir)

    # Informações current Access Zone
    executeSmbCurrentZone(NameDir)

    # Armazenar quantos groupnets existem para saber quantas vezes será iterado
    total = dados_json['total']
    x = 0
    while x < total:

        # Pegar o id do groupNet
        id_groupnet = dados_json['groupnets'][x]['id']  

        # Gera o arquivo com as informações de cada groupnet
        sendRequestIdGroupNet(id_groupnet,NameDir)

        # Ler subnets
        arquivo_json2 = open("/tmp/"+NameDir+"/groupnet/"+id_groupnet+".json")
        dados_json2 = json.load(arquivo_json2)
        subnet_empty = dados_json2['groupnets'][0]['subnets']

        #Validar se groupnet tem subnet
        a = 0
        while a < len(subnet_empty):

            # Pegar o nome das subnets
            subnet_name = dados_json2['groupnets'][0]['subnets'][a]

            # Gera o arquivo com as informação de cada subnet
            sendRequestSubnets(id_groupnet,subnet_name,NameDir)

            # Ler pools
            arquivo_json3 = open("/tmp/"+NameDir+"/subnet/"+subnet_name+".json")
            dados_json3 = json.load(arquivo_json3)
            pool_empty = dados_json3['subnets'][0]['pools']

            # Validação de pools, caso não exista
            y = 0
            while y < len(pool_empty):

                # Pegar o nome da pool
                name_pool = dados_json3['subnets'][0]['pools'][y]

                # Gera o arquivo com as informações de cada pool
                sendRequestPools(id_groupnet,subnet_name,name_pool,NameDir)

                # Ler Rules
                arquivo_json4 = open("/tmp/"+NameDir+"/pools/"+name_pool+".json")
                dados_json4 = json.load(arquivo_json4)
                rule_empty = dados_json4['pools'][0]['rules']

                # Validação de rules, caso não exista
                z = 0

                while z < len(rule_empty):

                    # Pega o nome da rule
                    name_rule = dados_json4['pools'][0]['rules'][z]

                    # Gera o arquivo com as informações das rules
                    sendRequestRules(id_groupnet,subnet_name,name_pool,name_rule,NameDir)
                    z+=1
                y+=1
            a+=1
        x+=1


# Remover arquivos
def removeFiles():
    os.system('rm -rf /tmp/backup/general_informations.json')
    os.system('rm -rf /tmp/backup/nfs_export.json')
    os.system('rm -rf /tmp/backup/smb_export.json')
    os.system('rm -rf /tmp/backup/zone_informations.json')

def verify():

    groupnet = '/tmp/backup/general_informations.json'
    sendRequest('/platform/3/network/groupnets', groupnet, 'backup')

    # Armazena o arquivo zone_informations dentro da pasta backup para fazer comparação
    zones = '/tmp/backup/zone_informations.json'
    sendRequest('/platform/3/zones', zones, 'backup')

    # Armazena o arquivo smb_export dentro da pasta backup para fazer comparação
    smbE = '/tmp/backup/smb_export.json'
    sendRequest('/platform/4/protocols/smb/shares', smbE, 'backup')

    # Armazena o arquivo nfs_ export dentro da pasta backup para fazer comparação
    nfsE = '/tmp/backup/nfs_export.json'
    sendRequest('/platform/4/protocols/nfs/exports', nfsE, 'backup')

    # Pega o arquivo antigo e compara com o novo para verificar se houve alteração (general_informations)
    arquivo_json_last = open('/tmp/dumps/general_informations.json','r') 
    dados_json_last = json.load(arquivo_json_last)
    arquivo_json_new = open('/tmp/backup/general_informations.json','r') 
    dados_json_new = json.load(arquivo_json_new)

    # Pega o arquivo antigo e compara com o novo para verificar se houve alteração (zone_informations)
    arquivo_json_lastZone = open('/tmp/dumps/zone_informations.json','r') 
    dados_json_lastZone = json.load(arquivo_json_lastZone)
    arquivo_json_newZone = open('/tmp/backup/zone_informations.json','r') 
    dados_json_newZone = json.load(arquivo_json_newZone)

    # Pega o arquivo antigo e compara com o novo para verificar se houve alteração (smb_export)
    arquivo_json_lastSmb = open('/tmp/dumps/smb_export.json','r') 
    dados_json_lastSmb = json.load(arquivo_json_lastSmb)
    arquivo_json_newSmb = open('/tmp/backup/smb_export.json','r') 
    dados_json_newSmb = json.load(arquivo_json_newSmb)

    # Pega o arquivo antigo e compara com o novo para verificar se houve alteração (nfs_export)
    arquivo_json_lastNfs = open('/tmp/dumps/nfs_export.json','r') 
    dados_json_lastNfs = json.load(arquivo_json_lastNfs)
    arquivo_json_newNfs = open('/tmp/backup/nfs_export.json','r') 
    dados_json_newNfs = json.load(arquivo_json_newNfs)

    if dados_json_last == dados_json_new:
        print('Não foram feitas alterações')
    else:
        if dados_json_last == dados_json_new:
            print('Modificações encontradas')
            execute('backup'+dataMod)
        else:
            print('Não precisa de modificação')


if os.path.isdir('/tmp/dumps'):
    if os.path.isdir('/tmp/backup'):
        verify()      
    else:
        # Cria a pasta
        os.system('mkdir /tmp/backup')
        verify()
else:
    print('Primeira vez')
    execute('dumps')
    
#dados_json_lastZone == dados_json_newZone or dados_json_lastSmb == dados_json_newSmb or dados_json_lastNfs == dados_json_newNfs