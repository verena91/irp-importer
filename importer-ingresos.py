import csv
import datetime
import json

# TODO: Debería ser un switch con todas las opciones (tiene solo lo que yo uso)
def obtener_tipo_documento_texto(codigo):
    if codigo == '1':
        return 'Factura'
    elif codigo == '4':
        return 'Nota de Crédito'
    else:
        return ''

# TODO: Debería ser un switch con todas las opciones (tiene solo lo que yo uso)
def obtener_tipo_ingreso_texto(codigo):
    if codigo == 'HPRSP':
        return 'Honorarios Profesionales y otras remuneraciones percibidas por servicios personales'
    else:
        return 'Dividendos y utilidades'

ingresos = []
with open('IRP - Ingresos.csv', newline='') as csvfile: # TODO: Pasar como parametro
    reader = csv.DictReader(csvfile)
    try:
        for idx, row in enumerate(reader):
            # print('Registro nro.: ', idx)
            # crear un item de ingreso por cada registro en el csv de Ingresos
            # Ejemplo item ingreso
            # {
            #   "tipo": "1",
            #   "periodo": "2017",
            #   "tipoTexto": "Factura",
            #   "fecha": "2017-11-04",
            #   "ruc": "3893208",
            #   "tipoIngreso": "OI",
            #   "tipoIngresoTexto": "Otros Ingresos Gravados o No Gravados por el IRP",
            #   "id": 1,
            #   "ingresoMontoGravado": 18181818,
            #   "ingresoMontoNoGravado": 0,
            #   "ingresoMontoTotal": 18181818,
            #   "timbradoCondicion": "contado",
            #   "timbradoDocumento": "001-002-0000032",
            #   "timbradoNumero": "11586889",
            #   "relacionadoTipoIdentificacion": "CEDULA",
            #   "relacionadoNumeroIdentificacion": "4698431",
            #   "relacionadoNombres": "RUTH BETHANIA LÓPEZ ESPINOZA"
            # }
            json_data = {}
            json_data['tipo'] = row['tipo_documento']
            json_data['periodo'] = "2018" # TODO: Pasar como parametro
            json_data['tipoTexto'] = obtener_tipo_documento_texto(row['tipo_documento'])
            json_data['fecha'] = row['fecha']
            json_data['ruc'] = "3893208" # TODO: Pasar como parametro
            json_data['tipoIngreso'] = row['tipo_ingreso']
            json_data['tipoIngresoTexto'] = obtener_tipo_ingreso_texto(row['tipo_ingreso'])
            json_data['ingresoMontoGravado'] = int(row['ingreso_gravado'])
            json_data['ingresoMontoNoGravado'] = int(row['ingreso_no_gravado'])
            json_data['ingresoMontoTotal'] = int(row['total'])
            if row['tipo_documento'] == '1': # solo si es factura
                json_data['timbradoCondicion'] = row['condicion_venta']
            json_data['timbradoDocumento'] = row['numero_documento']
            json_data['timbradoNumero'] = row['timbrado']
            json_data['relacionadoTipoIdentificacion'] = row['tipo_identificacion']
            json_data['relacionadoNumeroIdentificacion'] = row['numero_identificacion']
            json_data['relacionadoNombres'] = row['razon_social']
            # ingreso_data = json.dumps(json_data, ensure_ascii=False)
            # print(ingreso_data)
            ingresos.append(json_data)
        print('Éxito: todos los registros fueron generados correctamente')
    except Exception as e:
        print(str(e))
        print('Error: ningún registro se procesará')

with open('base.json', 'r+') as f:
    data = json.load(f)
    updated_data = data
    updated_data['ingresos'] = ingresos

    with open('test-ingresos.json', 'w') as outfile:
        json.dump(updated_data, outfile)
