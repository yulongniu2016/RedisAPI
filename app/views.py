from django.shortcuts import render
from django.http import HttpResponse
from django_redis import get_redis_connection
import json

# Create your views here.
def redisget(request):
    conn = get_redis_connection('default')
    print(conn.hget('kkk','age'))
    key = conn.get('beijing')
    return HttpResponse(key)
def scan_list(request):
    conn = get_redis_connection('default')
    print(conn.keys(pattern='10*'))
    keycount = 0
    scanlist = []
    for item in conn.keys(pattern='10*'):
        #print(item,conn.get(item))
        #scanlist.append({'ip':item})
        scanlist.append({'ip':item, 'ver':conn.get(item)})
        print(scanlist)
        keycount += 1
        print("keycount is: ",keycount) 
    #return HttpResponse(200)
    return render(request, 'scan_list.html', {'scanlist': scanlist})

def redisset(request):
    # Receive data that web explore method to update date
    # http usage: http://xxx.xxx.xxx.xxx:port/redisset/?name=xxx&value=xxx
    if request.method == 'GET':
        print("---> It's GET")
        name = request.GET.get('name')
        values = request.GET.get('value')
        print("--->name: ",name)
        print("--->value: ",values)
      
        conn = get_redis_connection('default')
        conn.set(name,values)

        #return HttpResponse(200)

    # Receive data that curl command update with JSON method on Linux's shell
    if request.method == 'POST':

        # It's use curl command to update data with JSON on Linux's shell
        # shell usage: curl -H "Content-Type: application/json" -X POST -d '{"name":"neimeng","value":"huhehaote"}' http://10.199.89.212:7000/redisset/
        #print("---> use curl command with JSON")
        #print("--->request.body: ", request.body)
        #receive_data = json.loads(request.body.decode('utf-8'))
        #print("--->receive_data ", receive_data)
        #name = receive_data['name']
        #values = receive_data['value']

        # It's use curl command to update data with POST on Linux's shell
        # shell usage: curl -d "name=xxx&value=xxx" http://xxx.xxx.xxx.xxx:port/redisset/
        print("---> use curl command with POST")
        name = request.POST.get('name')
        values = request.POST.get('value')
 
        print("--->name: ",name)
        print("--->value: ",values)

        # set data to redis
        conn = get_redis_connection('default')
        conn.set(name,values)

        return HttpResponse(200)
