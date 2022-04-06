
from FileManager import FileManager
fileManager = FileManager()

def login():
    login_file = "login.html"

    header = "HTTP/1.1 200 OK\n\n"
    return header + fileManager.read_file(login_file)

def form_page():
    mainpage_file = "mainpage.html"

    header = header = 'HTTP/1.1 200 OK\n\n'
    return header + fileManager.read_file(mainpage_file)

def error_page():
    header = 'HTTP/1.1 404 Not Found\n\n'
    response = '''
    <html>
        <body>
            <header>
                <h1 style="text-align: left; margin-top: 5%; color: red">Error 404</h1>
                <h3 style="text-align: left;"> The requested URL was not found on this server</h3>
            </header>
        </body>
    </html>
    '''
    return header + response

def bad_request_page():
    header = 'HTTP/1.1 400 Bad Request Error\n\n'
    response = '''
    <html>
        <body>
            <header>
                <h1 style="text-align: left; margin-top: 5%; color: red">Error 400</h1>
                <h3 style="text-align: left;"> Malformed or illegal request </h3>
            </header>
        </body>
    </html>
    '''
    return header + response

def saved_data_page():
    header = "HTTP/1.1 200 OK\n\n"
    response = '''
    <html>
        <body>
            <header>
                <h1 style=" font-size: 50px; text-align: center; margin-top: 5%; color: #5cb85c ">Datos almacenados correctamente</h1>
            </header>
            </form>
        </body>
    </html>
    '''
    return header + response