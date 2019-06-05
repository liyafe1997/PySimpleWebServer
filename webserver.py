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
            if node.split('.')[-1] == "html" or node.split('.')[-1] == "htm":
                print "Html files, set header Content-Type=text/html"
                self.send_header('Content-type', 'text/html')
        except:
            pass
        self.end_headers()
        #--Process header
#------------------Web Services Start-----------------
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
            userid = str(requests["userid"][0])
            #queryString = "SELECT id FROM u_account WHERE userName="+str(username)
            #result = SQLike_Query(queryString)
            #print "SQLike Select USERNAME Result = "+result
            #userid=result.split('\n')[1].split('\t')[0]
            #print "UserID = "+userid
            queryString = "SELECT * FROM tblog WHERE userid="+userid
            result = SQLike_Query(queryString)

            jsonarray = []
            result = result.split('\n')[1:]
            print "SQLike Select articles Result = \n"
            print result
            for i in range(len(result)):
                #id,title,summary,releaseDate,clickHit,replyHit,content,typeId,keyWord,userid
                if len(result[i].split('\t')) == 10:
                    print "A line data:"
                    print result[i].split('\t')
                    articleID= result[i].split('\t')[0]
                    data={}
                    data['articleid'] = articleID
                    data['title']=result[i].split('\t')[1]
                    data['summary']=result[i].split('\t')[2]
                    data['releaseDate']=result[i].split('\t')[3]
                    data['clickHit']=result[i].split('\t')[4]
                    data['replyHit']=result[i].split('\t')[5]
                    data['content']=result[i].split('\t')[6]
                    data['typeId']=result[i].split('\t')[7]
                    data['keyWord']=result[i].split('\t')[8]
                    data['userid']=result[i].split('\t')[9]
                                            
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
                try:
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
                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())            
            else:
                print "New Blog Error: Username Or Password Wrong!"
                self.wfile.write(("failed").encode())
        elif node == "/list":
            queryString = "SELECT * FROM u_account"
            result = SQLike_Query(queryString)

            jsonarray = []
            result = result.split('\n')[1:]
            print "SQLike Select user list Result = \n"
            print result
            for i in range(len(result)):
                if len(result[i].split('\t')) == 8:
                    print "A line data:"
                    print result[i].split('\t')
                    userid= result[i].split('\t')[0]
                    data={}
                    data['userid'] = userid
                    data['username']=result[i].split('\t')[1]
                    data['nickname']=result[i].split('\t')[3]
                    data['sign']=result[i].split('\t')[4]
                    data['proFile']=result[i].split('\t')[5]
                    data['imageName']=result[i].split('\t')[6]
                    data['blogtypeid']=result[i].split('\t')[7]
                    jsonarray.append(data)
            jsondata = json.dumps(jsonarray)
            print "jsondata:"
            print jsondata
            self.wfile.write((jsondata).encode())
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
        #http://127.0.0.1:8081/getarticle?id=1
        elif node == "/getarticle":
            QueryString = "select * from tblog where id="+str(requests["id"][0])    
            article_contain = SQLike_Query(QueryString)
            article_contain = article_contain.split('\n')#return a list with 2 room,
            a_key = article_contain[0].split('\t')
            a_value = article_contain[1].split('\t')  
            dic = {}#store contain from db save as json format
            for i in range(0, len(a_value)):
                dic[a_key[i]] = a_value[i]
            self.wfile.write(json.dumps(dic).encode())
        elif node == "/getusernamebyuserid":
            QueryString = "select userName from u_account where id="+str(requests["id"][0])    
            result = SQLike_Query(QueryString)
            result=result.split('\n')[1].split('\t')[0]
            self.wfile.write(result.encode())

        #function 13: delete article by id
        #/deletearticle?adminuser=42432&adminpassword=fadsfads&articleid=1
        elif node == "/deletearticle":
            queryString = "SELECT password FROM m_account WHERE username="+str(requests["adminuser"][0])
            result = SQLike_Query(queryString)
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            #--verifing username password
            if result == requests["adminpassword"][0]: #password matched
                print "Delete blog admin succeed!"
                try:
                    print ("Delete tblog : "+SQLike_Query("DELETE tblog WHERE id="+str(requests["articleid"][0])))
                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())
            else:
                print "Comment Process Login failed"
                self.wfile.write(("failed").encode())
        #end of delect article
        
        #function 14: delete link by id
        #/deletelink?adminuser=42432&adminpassword=fadsfads&linkid=xxx
        elif node == "/deletelink":
            queryString = "SELECT password FROM m_account WHERE username="+str(requests["adminuser"][0])
            result = SQLike_Query(queryString)
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            #--verifing username password
            if result == requests["adminpassword"][0]: #password matched
                print "Delete blog admin succeed!"
                try:
                    print ("Delete tblog : "+SQLike_Query("DELETE f_link WHERE id="+str(requests["linkid"][0])))
                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())
            else:
                print "Comment Process Login failed"
                self.wfile.write(("failed").encode())
        #end of delete link

        #function 15:
        #/deletecomment?adminuser=42432&adminpassword=fadsfads&commentid=1
        #function 16:
        # /deletelink?adminuser=42432&adminpassword=fadsfads&linkid=1&linkname=xxx&linkurl=xxx&orderno=xxx
        elif node == "/deletecomment":
            queryString = "SELECT password FROM m_account WHERE username="+str(requests["adminuser"][0])
            result = SQLike_Query(queryString)
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            
            if requests["orderno"][0] == None:
                #--verifing username password
                if result == requests["adminpassword"][0]: #password matched
                    print "Delete blog admin succeed!"
                    try:
                        print ("Delete tblog : "+SQLike_Query("DELETE t_comment WHERE id="+str(requests["commentid"][0])))
                        self.wfile.write(("ok").encode())
                    except:
                        self.wfile.write(("failed").encode())
                else:
                    print "Comment Process Login failed"
                    self.wfile.write(("failed").encode())
            else:
                if result == requests["adminpassword"][0]: #password matched
                    print "Delete blog admin succeed!"
                    try:
                        #delete friendly link
                        print ("Delete tblog : "+SQLike_Query("DELETE t_comment WHERE id="+str(requests["commentid"][0])))
                        self.wfile.write(("ok").encode())
                    except:
                        self.wfile.write(("failed").encode())
                else:
                    print "Comment Process Login failed"
                    self.wfile.write(("failed").encode())
        #end of delete comment & friendly link

        
        elif node == "/keywordsearch":
            queryString = "SELECT id,title,typeId,releaseDate,clickHit FROM tblog WHERE keyWord="+str(requests["keyword"][0])  
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
        elif node == "/typenamesearch":
            queryString = "SELECT id,title,typeId,releaseDate,clickHit FROM tblog WHERE typeId="+str(requests["typeid"][0])  
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
        elif node =="/register":
            #get last user id
            queryString = "SELECT id FROM u_account"
            print queryString
            result = SQLike_Query(queryString)
            print "SQLike Result = "
            print result
            lines = result.split('\n')
            lines = [line for line in lines if line.strip()] # remove empty line
            lines= lines[1:]
            print lines
            newid = len(lines) + 1    
            print "New User ID = "+str(newid)
            #--get last user id

            #/register?username=xxx&password=123&nickname=xxx&sign=xxx&profile=xxx&imagename=xxx&blogtype=xxx
            try:
                #INSERT INTO u_account VALUES
                newid = str(newid)
                userName = str(requests["username"][0])
                password = str(requests["password"][0])
                nickName = str(requests["nickname"][0])
                sign = str(requests["sign"][0])
                profile = str(requests["profile"][0])
                imagename = str(requests["imagename"][0])
                blogtypeid = str(requests["blogtype"][0])
                #SQL colunm: id,title,summary,releaseDate,clickHit,replyHit,content,typeId,keyWord,userid
                result = SQLike_Query("INSERT INTO u_account VALUES ("+newid+","+userName+","+password+","+nickName+","+sign+","+profile+","+imagename+","+blogtypeid+")")
                print "New User Insert Result="
                print result
                self.wfile.write(("ok").encode())
            except:
                self.wfile.write(("failed").encode())

        #function 9
        #/blogmanage?username=xxx&password=123&nickname=xxx&sign=xxx&profile=xxx&imagename=xxx&blogtype=xxx
        elif node =="/blogmanage":
            #verifing username password
            queryString = "SELECT password FROM u_account WHERE userName="+str(requests["username"][0])
            print queryString
            result = SQLike_Query(queryString)
            
            print "SQLite Result : "+result
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            
            #--verifing username password
            if result == requests["password"][0]: #password matched

                #get user id
                queryString = "SELECT id FROM u_account WHERE userName="+str(requests["username"][0])
                print queryString
                result = SQLike_Query(queryString)
                result=result.split('\n')[1].split('\t')[0]
                print "SQLike Result = "
                print result
                userid = result
                #--get user id
                print "Modify blog owner info login succeed! userID="+userid 

                #/blogmanage?username=xxx&password=123&nickname=xxx&sign=xxx&profile=xxx&imagename=xxx&blogtype=xxx
                #id,userName,password,nickName,sign,proFile,imageName,blogtypeid
                try:
                    print ("UPDATE:"+SQLike_Query("UPDATE u_account SET nickName="+ str(requests["nickname"][0])+" WHERE id="+userid))
                    print ("UPDATE:"+SQLike_Query("UPDATE u_account SET sign="+ str(requests["sign"][0])+" WHERE id="+userid))
                    print ("UPDATE:"+SQLike_Query("UPDATE u_account SET proFile="+ str(requests["profile"][0])+" WHERE id="+userid))
                    print ("UPDATE:"+SQLike_Query("UPDATE u_account SET imageName="+ str(requests["imagename"][0])+" WHERE id="+userid))
                    print ("UPDATE:"+SQLike_Query("UPDATE u_account SET blogtypeid="+ str(requests["blogtype"][0])+" WHERE id="+userid))
                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())
            else:
                print "Modify blog owner info login failed!"
                self.wfile.write(("failed").encode())
        elif node =="/linkadd":
            #/linkadd?linkname=xxx&linkurl=xxx&orderno=3
            #get last link id
            queryString = "SELECT id FROM f_link"
            print queryString
            result = SQLike_Query(queryString)
            print "SQLike Result = "
            print result
            lines = result.split('\n')
            lines = [line for line in lines if line.strip()] # remove empty line
            lines= lines[1:] #remove the first line
            print lines
            newid = str(len(lines) + 1 )   
            print "New Link ID = "+str(newid)
            #--get last link id

            try:
                #INSERT INTO f_link VALUES
                newid = str(newid)
                linkName = str(requests["linkname"][0])
                linkUrl = str(requests["linkurl"][0])
                orderno = str(requests["orderno"][0])
                #SQL colunm: id,title,summary,releaseDate,clickHit,replyHit,content,typeId,keyWord,userid
                result = SQLike_Query("INSERT INTO f_link VALUES ("+newid+","+linkName+","+linkUrl+","+orderno+")")
                print "New Link Insert Result="
                print result
                self.wfile.write(("ok").encode()) 
            except:
                self.wfile.write(("failed").encode())

        elif node =="/comment":
        #verifing username password
            queryString = "SELECT password FROM u_account WHERE userName="+str(requests["username"][0])
            print queryString
            result = SQLike_Query(queryString)
            
            print "SQLite Result : "+result
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            
            #--verifing username password
            if result == requests["password"][0]: #password matched
                print "New blog login succeed!"
                #get last comment id
                queryString = "SELECT id FROM t_comment"
                print queryString
                result = SQLike_Query(queryString)
                print "SQLike Result = "
                print result
                lines = result.split('\n')
                lines = [line for line in lines if line.strip()] # remove empty line
                lines= lines[1:]
                print lines
                newid = str(len(lines) + 1)    
                print "New comment ID = "+ newid
                #--get last comment id
                
                #get user id
                queryString = "SELECT id FROM u_account WHERE userName="+str(requests["username"][0])
                print queryString
                result = SQLike_Query(queryString)
                result=result.split('\n')[1].split('\t')[0]
                print "SQLike Result = "
                print result
                userid = result
                #--get user id
                #/comment?username=xxx&password=xxx&content=xxx&articleid=xxx
                try:
                    #INSERT INTO tblog VALUES
                    commentid = newid
                    articleid = str(requests["articleid"][0])
                    content = str(requests["content"][0])
                    commentDate = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                    state = '0'
                    #SQL colunm: id,userid,articleid,content,commentDate,state
                    result = SQLike_Query("INSERT INTO t_comment VALUES ("+commentid+","+userid+","+articleid+","+content+","+commentDate+","+state+")")
                    print "New comment Insert Result="
                    print result
                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())
            else:
                print "Comment Process Login failed"
                self.wfile.write(("failed").encode())

        elif node == "/commentlist":
            userid = str(requests["articleid"][0])
            #queryString = "SELECT id FROM u_account WHERE userName="+str(username)
            #result = SQLike_Query(queryString)
            #print "SQLike Select USERNAME Result = "+result
            #userid=result.split('\n')[1].split('\t')[0]
            #print "UserID = "+userid
            queryString = "SELECT * FROM t_comment WHERE articleid="+userid
            result = SQLike_Query(queryString)

            jsonarray = []
            result = result.split('\n')[1:]
            print "SQLike Select comments Result = \n"
            print result
            for i in range(len(result)):
                if len(result[i].split('\t')) == 6:
                    print "A line data:"
                    print result[i].split('\t')
                    commentid= result[i].split('\t')[0]
                    data={}
                    data['commentid'] = commentid
                    data['userid']=result[i].split('\t')[1]
                    data['articleid']=result[i].split('\t')[2]
                    data['content']=result[i].split('\t')[3]
                    data['commentDate']=result[i].split('\t')[4]
                    data['state']=result[i].split('\t')[4]
                    jsonarray.append(data)
            jsondata = json.dumps(jsonarray)
            print "jsondata:"
            print jsondata
            self.wfile.write((jsondata).encode())
        elif node =="/deleteuser":
            #/deleteuser?adminuser=42432&adminpassword=fadsfads&userid=xxx

            #verifing username password
            queryString = "SELECT password FROM m_account WHERE username="+str(requests["adminuser"][0])
            print queryString
            result = SQLike_Query(queryString)
            
            print "SQLite Result : "+result
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            
            #--verifing username password
            if result == requests["adminpassword"][0]: #password matched
                print "Delete blog admin succeed!"

                try:
                    print ("Delete u_account : "+SQLike_Query("DELETE u_account WHERE id="+str(requests["userid"][0])))
                    print ("Delete tblog : "+SQLike_Query("DELETE tblog WHERE userid="+str(requests["userid"][0])))
                    print ("Delete t_comment : "+SQLike_Query("DELETE t_comment WHERE userid="+str(requests["userid"][0])))

                    self.wfile.write(("ok").encode())
                except:
                    self.wfile.write(("failed").encode())
            else:
                print "Comment Process Login failed"
                self.wfile.write(("failed").encode())
        elif node == "/adminlogin" :
            queryString = "SELECT password FROM m_account WHERE username="+str(requests["adminusername"][0])
            print queryString
            result = SQLike_Query(queryString)
            
            print "SQLite Result : "+result
            result=result.split('\n')[1].split('\t')[0] #Get the second line(first line is colonm) and the first data
            if result == requests["adminpassword"][0]:
                self.wfile.write(("ok").encode())
            else:
                self.wfile.write(("failed").encode())

#------------------Web Services End-----------------

#------------------Web Server Load File From File System Start-----------------
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
#------------------Web Server Load File From File System End-----------------

            


    def do_POST(self):
        form = cgi.FieldStorage   (
            fp = self.rfile,
            headers = self.headers,
            environ = {  'REQUEST_METHOD': 'POST'}
        )

        value = form.getvalue("key")

        #self._set_headers()
        self.wfile.write("")

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