from xmlrpc_redes.client import connect

def test_client():
    print("============================")
    print("Iniciando Pruebas Servidor 1")

    #host = "192.168.1.133"
    #host = "localhost"
    host = '150.150.0.2'
    puerto = 8080
    
    conn = connect(host,puerto)
    retorno = conn.concat("Hola"," mi nombre es Mauricio")
    assert retorno == "Hola mi nombre es Mauricio"
    print('Test 1 completado')

    conn = connect(host,puerto)
    retorno = conn.concat("345","23","657","HTTP")
    assert retorno == "34523657HTTP"
    print('Test 2 completado')

    conn = connect(host,puerto)
    retorno = conn.concat("Hola"," mi nombre es Mauricio",456,25)
    #print(retorno)
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 3 completado')

    conn = connect(host,puerto)
    retorno = conn.funcion_no_existente(5,2)
    assert retorno == "Fault_Code: 2 ; String_Code: No existe el método invocado"
    print('Test 4 completado')

    conn = connect(host,puerto)
    retorno = conn.suma(5,2)
    assert retorno == 7
    print('Test 5 completado')

    conn = connect(host,puerto)
    retorno = conn.suma(5,2,-7,10,9,-5)
    assert retorno == 14
    print('Test 6 completado')

    conn = connect(host,puerto)
    retorno = conn.suma(5,2,-7,"Hola",9,-5)
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 7 completado')

    conn = connect(host,puerto)
    mensaje = "Prueba"
    retorno = conn.echo(mensaje)
    assert retorno == mensaje
    print('Test 8 completado')

    conn = connect(host,puerto)
    retorno = conn.eco(mensaje)
    assert retorno == "Fault_Code: 2 ; String_Code: No existe el método invocado"
    print('Test 9 completado')

    conn = connect(host,puerto)
    mensaje = "Prueba"
    retorno = conn.echo(mensaje,mensaje)
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 10 completado')

    conn = connect(host,puerto)
    mensaje = "Prueba"
    retorno = conn.echo(mensaje)
    assert retorno == mensaje
    print('Test 11 completado')

    conn = connect(host,puerto)
    #mensaje = "a"*20000        
    mensaje = "aeri"
    retorno = conn.echo(mensaje)
    print(retorno)
    assert retorno == mensaje
    print('Test 12 completado')
  
    print("============================")
    print("Iniciando Pruebas Servidor 2")
    
    #host = "192.168.1.133"
    #host = "localhost"
    host = "100.100.0.2"
    puerto = 80

    conn = connect(host,puerto)
    retorno = conn.mayusculas("hola que tal")
    assert retorno == "HOLA QUE TAL"
    print('Test 1 completado')

    conn = connect(host,puerto)
    retorno = conn.mayusculas("hola Que tal","todo bien")
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 2 completado')

    conn = connect(host,puerto)
    retorno = conn.mayusculas()
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 3 completado')

    conn = connect(host,puerto)
    retorno = conn.contar_vocales("Hola, mi nombre es Mauricio")
    assert retorno == 11
    print('Test 4 completado')

    conn = connect(host,puerto)
    retorno = conn.contar_vocales("Hola, mi nombre es Mauricio", "aeri")
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 5 completado')

    conn = connect(host,puerto)
    retorno = conn.contar_voc("Hola, mi nombre es Mauricio", "aeri")
    assert retorno == "Fault_Code: 2 ; String_Code: No existe el método invocado"
    print('Test 6 completado')

    conn = connect(host,puerto)
    retorno = conn.contar_vocales()
    assert retorno == "Fault_Code: 3 ; String_Code: Error en parámetros del método invocado"
    print('Test 7 completado')




    conn1 = connect(host,puerto)
    #conn2 = connect(host,puerto)
    retorno1 = conn1.contar_vocales("Hola que tal como te va hoy en este increible dia")
    #retorno2 = conn2.contar_vocales("aeri")
    assert retorno1 == 19
    #assert retorno2 == 3
    print('Test 8 completado')

    conn = connect(host,puerto)
    retorno = conn.division(4,0)
    assert retorno == "Fault_Code: 4 ; String_Code: Error interno en la ejecución del método"
    print('Test 9 completado')

    conn = connect(host,puerto)
    retorno = conn.mayor_a_5("Todo Bien Por Aca",6)
    assert retorno == "TODO BIEN POR ACA"
    print('Test 10 completado')

    conn = connect(host,puerto)
    retorno = conn.saludar()
    assert retorno == "HOLA"
    print('Test 11 completado')


    
test_client()