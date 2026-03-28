import socket
import xml.etree.ElementTree as ET

class Client:
    def __init__(self, host, port):
        self.destino_host = host
        self.destino_port = port
        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((host, port))
        except (socket.timeout, socket.error, OSError):
            print("No se pudo conectar al servidor")
        


    def __getattr__(self, name):
        def envio(*args):
            def construir_solicitud(host, method_name, args):
                params_xml = ""
                for arg in args:
                    if isinstance(arg, int):
                        params_xml += f"<param><value><i4>{arg}</i4></value></param>"
                    elif isinstance(arg, str):
                        params_xml += f"<param><value><string>{arg}</string></value></param>"
                    else:
                        raise Exception()

                body = f"""<?xml version="1.0"?> 
<methodCall>
    <methodName>{method_name}</methodName>
    <params>
        {params_xml}
    </params>
</methodCall>"""

                return construir_headers(body,host)

            def construir_headers(body,host):
                return (
                    "POST / HTTP/1.1\r\n"
                    "User-Agent: xmlrpc_redes/1.0\r\n"
                    f"Host: {host}\r\n"
                    "Content-Type: text/xml\r\n"
                    f"Content-length: {len(body)}\r\n"
                    "\r\n"
                    f"{body}"
                    )
            
            def parseo(cuerpo):
                
                root = ET.fromstring(cuerpo)
                
                # Si hay fault
                fault_elem = root.find(".//fault")
                if fault_elem is not None:
                    for member in fault_elem.findall(".//member"):
                        name_elem = member.find("name")
                        value_elem = member.find("value")
                        if name_elem is not None and value_elem is not None:
                            if name_elem.text == "faultCode":
                                fault_code = value_elem.find("int").text                        
                            elif name_elem.text == "faultString":
                                fault_string = value_elem.find("string").text
                    return f"Fault_Code: {fault_code} ; String_Code: {fault_string}"
                
                # Si no hay fault, parseamos parámetro
                param_elem = root.find(".//param")
                if param_elem is not None:
                    value_elem = param_elem.find("value")
                    if value_elem is not None:
                        child = list(value_elem)[0]
                        tag = child.tag
                        if tag in ("i4", "int"):
                            return int(child.text)
                        elif tag == "string":
                            return child.text
                        else:
                            valor = child.text
                        return valor              
                return None 
            
            
            self.cliente.settimeout(60)
            try:
                xml_request = construir_solicitud(self.destino_host, name , args)
            except Exception:
                self.cliente.close()
                print("Parametros no soportados")
                return
            
            mensaje_enviar = xml_request.encode()
            
            #enviamos request
            total_enviados = 0
            while total_enviados < len(mensaje_enviar):
                try:
                    enviados = self.cliente.send(mensaje_enviar[total_enviados:])
                except Exception:
                    self.cliente.close()
                    print("El servidor cerro la conexion")
                    return
                if enviados == 0:
                    self.cliente.close()
                    print("El servidor cerro la conexion")
                    return
                total_enviados += enviados

            #Recibimos datos
            buffer = ""
            while "\r\n\r\n" not in buffer:
                try:
                    data = self.cliente.recv(1024)
                except Exception:
                    self.cliente.close()
                    print("El servidor cerro la conexion")
                    return
                if not data:
                    self.cliente.close()
                    print("El servidor cerro la conexion")
                    return
                buffer += data.decode()

            headers, resto = buffer.split("\r\n\r\n", 1)
            
            headers_lower = headers.lower()   

            #controlamos headers
            if "200 ok" not in headers_lower or  "connection: close"  not in headers_lower or "content-length:"  not in headers_lower or "content-type:"  not in headers_lower:
                self.cliente.close()
                if("bad request" in headers_lower):
                    print("Error al enviar el request, se cierra la conexion")
                else:
                    print("Error al parsear el HTTP, se cierra la conexion")                   
                return
            

            for line in headers.split("\r\n"):
                if line.lower().startswith("content-length:"):
                    try:
                        largo = line.split(":")[1].strip()
                        content_length = int(largo)
                    except Exception:
                        self.cliente.close()
                        print("Error al parsear el HTTP, se cierra la conexion")                         
                        return
            

            #recibimos el resto del body
            body = resto.encode()
            while len(body) < content_length:
                try:
                    data = self.cliente.recv(1024)
                except Exception:
                    self.cliente.close()
                    print("El servidor cerro la conexion")
                    return
                if not data:
                    self.cliente.close()
                    print("El servidor cerro la conexion")
                    return
                body += data
            body = body.decode()


            
            if not body.lstrip().startswith('<?xml version="1.0"?>'):
                self.cliente.close()
                print("Error al parsear el XML, se cierra la conexion")
                return

            #se parsea y se controla el xml
            try:
                retorno = parseo(body)
            except Exception:
                self.cliente.close()
                print("Error al parsear el XML, se cierra la conexion")
                return
            
            self.cliente.close()

            return retorno
        return envio

def connect(host, port):
    return Client(host, port)

