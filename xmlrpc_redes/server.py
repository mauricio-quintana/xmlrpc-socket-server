import socket
import threading
import xml.etree.ElementTree as ET

class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.methods = {}  

    def add_method(self, func):
        self.methods[func.__name__] = func

    def serve(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.address, self.port))
        sock.listen(20)
        print(f"Servidor escuchando en {self.address}:{self.port}")

        while True:
            conn, addr = sock.accept()
            threading.Thread(target=self.atender, args=(conn,)).start()
        sock.close()

    def atender(self, conn): 

        def construir_respuesta(headers,body):
            if not body.lstrip().startswith('<?xml version="1.0"?>'):
                return construir_fault(1, "Error parseo de XML")
            try:
                root = ET.fromstring(body)
            except ET.ParseError:
                return construir_fault(1, "Error parseo de XML")
            except Exception:
                return construir_fault(1, "Error parseo de XML")
            
            method_name = root.find('methodName')
            if method_name is None or method_name.text is None:
                return construir_fault(1, "Error parseo de XML")
            
            method_name = method_name.text

            if method_name not in self.methods:
                return construir_fault(2, "No existe el método invocado")

            params = []
            try:
                for p in root.findall('params/param'):
                    value_elem = list(p.find('value'))[0]  
                    if value_elem.tag in ['i4', 'int']:
                        params.append(int(value_elem.text))
                    elif value_elem.tag == 'string':
                        params.append(value_elem.text)
                    else:
                        return construir_fault(1, "Error parseo de XML")
            except Exception:
                return construir_fault(1, "Error parseo de XML")
            
            try:
                resultado_proc = self.methods[method_name](*params)
            except TypeError:
                return construir_fault(3, "Error en parámetros del método invocado")
            except ValueError:
                return construir_fault(3, "Error en parámetros del método invocado")
            except Exception:
                return construir_fault(4, "Error interno en la ejecución del método")

            return construir_respuesta_valida(resultado_proc,method_name)
        
        def construir_fault(fault_code,fault_string):
            
#NOOOO MODIFICAR IDENTACION
            body = f"""<?xml version="1.0"?>
<methodResponse>
    <fault>
        <value>
            <struct>
                <member>
                    <name>faultCode</name>
                    <value><int>{fault_code}</int></value>
                    </member>
                <member>
                    <name>faultString</name>
                    <value><string>{fault_string}</string></value>
                    </member>
                </struct>
            </value>
        </fault>
    </methodResponse>"""
            return construir_headers(body)
        
        def construir_respuesta_valida(resultado, method):
            if isinstance(resultado, int):
                mensaje =  f"<param><value><i4>{resultado}</i4></value></param>"
            else:
                mensaje =  f"<param><value><string>{resultado}</string></value></param>" 

#NOOOO MODIFICAR IDENTACION
            body = f"""<?xml version="1.0"?>
<methodResponse>
    <params>
        {mensaje}
    </params>
</methodResponse>"""
            
            return construir_headers(body)
        
        def construir_headers(body):
            return (
                "HTTP/1.1 200 OK\r\n"
                "Connection: close\r\n" 
                f"Content-Length: {len(body)}\r\n"
                "Content-Type: text/xml\r\n"
                "\r\n"
                f"{body}"
                )
        
        def construir_bad_request(body):
            return (
                "HTTP/1.1 400 Bad Request\r\n"
                "Connection: close\r\n" 
                f"Content-Length: {len(body)}\r\n"
                "Content-Type: text/xml\r\n"
                "\r\n"
                f"{body}"
                )

        def send_aux(respuesta,s):
            mensaje_enviar = respuesta.encode()
            total_enviados = 0
            while total_enviados < len(mensaje_enviar):
                try:
                    enviados = s.send(mensaje_enviar[total_enviados:])
                except Exception:
                    return
                if enviados == 0:
                    return
                total_enviados += enviados
            
        conn.settimeout(60)
        buffer = ""
        while "\r\n\r\n" not in buffer:
            try:
                data = conn.recv(1024)                
                if not data:
                    conn.close()
                    return
                buffer += data.decode()
            except socket.timeout:
                respuesta = construir_bad_request("")
                send_aux(respuesta,conn)
                conn.close()
                return
            except socket.error:
                respuesta = construir_bad_request("")
                send_aux(respuesta,conn)
                conn.close()
                return
            except Exception:
                conn.close()
                return

        headers, resto = buffer.split("\r\n\r\n", 1)
        
        primera_linea = headers.split("\r\n")[0]
        es_post = primera_linea.split(" ")[0]
        headers_lower = headers.lower()          
        if es_post != "POST" or "user-agent:"  not in headers_lower or "host:"  not in headers_lower or "content-length:"  not in headers_lower or "content-type:"  not in headers_lower:
            respuesta = construir_bad_request("")
            send_aux(respuesta,conn)
            conn.close()
            return
       
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                try:
                    largo = line.split(":")[1].strip()
                    content_length = int(largo)
                except ValueError:  #IndexError es porque no hay nada y ValueError es porque no se puede convertir a entero
                    respuesta = construir_bad_request("")
                    send_aux(respuesta,conn)
                    conn.close()
                    return
                except IndexError:
                    respuesta = construir_bad_request("")
                    send_aux(respuesta,conn)
                    conn.close()
                    return
                except Exception:
                    respuesta = construir_bad_request("")
                    send_aux(respuesta,conn)
                    conn.close()
                    return

        #print(content_length)
        body = resto.encode()
        while len(body) < content_length:
            try:
                data = conn.recv(1024)
            except (socket.timeout,socket.error):
                respuesta = construir_bad_request("")
                send_aux(respuesta,conn)
                conn.close()
                return
            except Exception:
                conn.close()
                return
            if not data:
                conn.close()
                return
            body += data
        
        if len(body)!=content_length:
            respuesta = construir_bad_request("")
            send_aux(respuesta,conn)
            conn.close()
            return
        body = body.decode()
        
        respuesta = construir_respuesta(headers,body)
        send_aux(respuesta,conn)
        
        conn.close()