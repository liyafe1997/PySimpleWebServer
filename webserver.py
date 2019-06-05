import os
import cgi
import urlparse
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import time


global sqlikesock

def ReadFile(filename):
    file_object = open(filename, "rb")
    try:
        fileContent = file_object.read()
    finally:
        file_object.close()
    return fileContent


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        requests = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        #http://127.0.0.1:8081/432432?user=bbb&ccc=ddd
        node = self.path.split('?')
        node = node[0]
        print "Request node = "+str(node)
        print "Request para = "+str(requests)

        #Process header
        self.send_response(200)
        try:
            if node.split('.')[-1] == ".html" or node.split('.')[-1] == ".htm":
                self.send_header('Content-type', 'text/html')
        except:
            pass
        self.end_headers()
        #--Process header
        if node == "/login" :
            queryString = "SELECT password FROM u_account WHERE userName="+str(requests["username"][0])
            print queryString
            result = SQLike_Query(queryString)
            
            print "SQLite Result : "+result
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            if result == requests["password"][0]:
                self.wfile.write(("ok").encode())
            else:
                self.wfile.write(("failed").encode())
        elif node == "/listarticle":
            username = str(requests["username"][0])
            queryString = "SELECT id FROM u_account WHERE userName="+str(username)
            result = SQLike_Query(queryString)
            print "SQLike Select USERNAME Result = "+result
            userid=result.split('\n')[1].split('\t')[0]
            print "UserID = "+userid
            queryString = "SELECT id,title,typeId,releaseDate,clickHit FROM tblog WHERE userid="+userid
            result = SQLike_Query(queryString)

            jsonarray = []
            result = result.split('\n')[1:]
            print "SQLike Select articles Result = \n"
            print result
            for i in range(len(result)):
                if len(result[i].split('\t')) == 6:
                    print "A line data:"
                    print result[i].split('\t')
                    articleID= result[i].split('\t')[0]
                    data={}
                    data['articleid'] = articleID
                    data['title']=result[i].split('\t')[1]
                    data['typeId']=result[i].split('\t')[2]
                    data['releaseDate']=result[i].split('\t')[3]
                    data['clickHit']=result[i].split('\t')[4]
                    jsonarray.append(data)
            jsondata = json.dumps(jsonarray)
            print "jsondata:"
            print jsondata
            self.wfile.write((jsondata).encode())
        elif node == "/newblog":
            #verifing username password
            queryString = "SELECT password FROM u_account WHERE userName="+str(requests["username"][0])
            print queryString
            result = SQLike_Query(queryString)
            
            print "SQLite Result : "+result
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            
            #--verifing username password
            if result == requests["password"][0]: #password matched
                print "New blog login succeed!"
                #get last artilce id
                queryString = "SELECT id FROM tblog"
                print queryString
                result = SQLike_Query(queryString)
                print "SQLike Result = "
                print result
                lines = result.split('\n')
                lines = [line for line in lines if line.strip()] # remove empty line
                lines= lines[1:]
                print lines
                newid = len(lines) + 1    
                print "New Article ID = "+str(newid)
                #--get last article id
                queryString = "SELECT id FROM u_account WHERE userName="+str(requests["username"][0])
                print queryString
                result = SQLike_Query(queryString)
                print "SQLike Result = "
                print result
                userid=str(result.split('\n')[1].split('\t')[0])
                
                #get userid
                #--get userid
#username=aaa&password=bbb&blogtitle=xxx&blogcontent=xxx&blogTypeid=123&summary=dfasfdafasd&keyword=fadfad

                #INSERT INTO tblog VALUES
                articleid = str(newid)
                title = str(requests["blogtitle"][0])
                summary = str(requests["summary"][0])
                releaseDate = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                clickHit = '0'
                replyHit = '0'
                content = str(requests["blogcontent"][0])
                typeID = str(requests["blogTypeid"][0])
                keyWord = str(requests["keyword"][0])
                userid = userid
                #SQL colunm: id,title,summary,releaseDate,clickHit,replyHit,content,typeId,keyWord,userid
                result = SQLike_Query("INSERT INTO tblog VALUES ("+articleid+","+title+","+summary+","+releaseDate+","+clickHit+","+replyHit+","+content+","+typeID+","+keyWord+","+userid+")")
                print "New Blog Insert Result="
                print result
            else:
                print "New Blog Error: Username Or Password Wrong!"
        elif node == "/list" : 
            queryString = "SELECT nickName FROM u_account"
            user_id = "SELECT id From u_account"
            result = SQLike_Query(queryString)
            id_result= SQLike_Query(user_id)
            print result
            result = result.split('\t\n')
            id_result = id_result.split('\t\n')
            print result
            print id_result
            jsonarray =[]
            for i in range(1, len(result)-1):
                d = {} 
                d["nickname"] = result[i]
                d["userid"] = id_result[i]
                jsonarray.append(d)
            jsondata = json.dumps(jsonarray)
            self.wfile.write(jsondata.encode())
        elif node == "/listblogtype":
            print "List blog types"
            queryString = "SELECT * FROM t_blogtype"
            result = SQLike_Query(queryString)
            print "SQLike Select t_blogtype Result = "
            print result
            jsonarray = []
            lines = result.split('\n')
            lines = [line for line in lines if line.strip()] # remove empty line
            result = lines[1:]
            print "SQLike Select articles Result = \n"
            print result
            for i in range(len(result)):
                print "A line data:\n"
                print result[i].split('\t')
                blogtypeID= result[i].split('\t')[0]
                data={}
                data['typeid'] = blogtypeID
                data['typename']=result[i].split('\t')[1]
                data['typedescribe']=result[i].split('\t')[2]
                jsonarray.append(data)
            jsondata = json.dumps(jsonarray)
            print "jsondata:"
            print jsondata
            self.wfile.write((jsondata).encode())
        elif node == "/":
            try:
                filecontent = ReadFile(os.path.split(os.path.abspath(__file__))[0]+"/WEBCONTENT/index.html")
                self.wfile.write(filecontent)
                print "Return file: "+node
            except:
                print "File not found: "+node
                self.wfile.write("<html><title>404 Not Found</title>404 Error<br>File /index.html Not Found.</html>")
        else :
            try:
                filecontent = ReadFile(os.path.split(os.path.abspath(__file__))[0]+"/WEBCONTENT"+node)
                self.wfile.write(filecontent)
                print "Return file: "+node
            except:
                print "File not found: "+node
                self.wfile.write("<html><title>404 Not Found</title>404 Error<br>File " + node +" Not Found.</html>")


            


    def do_POST(self):
        form = cgi.FieldStorage   (
            fp = self.rfile,
            headers = self.headers,
            environ = {  'REQUEST_METHOD': 'POST'}
        )

        value = form.getvalue("key")

        self._set_headers()
        self.wfile.write(value.encode())

def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Fucking http server is started.")
    httpd.serve_forever()

def SQLike_Query(cmdstring):
    global sqlikesock
    sqlikesock.send(cmdstring)
    data = sqlikesock.recv(1024)
    return data

if __name__ == "__main__":
    global sqlikesock
    from sys import argv
    sqlikesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sqlikesock.connect(('127.0.0.1', 1667))
        print "SQLike Server Connected!"
    except:
        print "Failed to Connect SQLike DB Server"
    
    run(HTTPServer,S,8081)