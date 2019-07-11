import csv
import datetime
import json

# TODO: Debería ser un switch con todas las opciones (tiene solo lo que yo uso)
def obtener_tipo_documento_texto(codigo):
    if codigo == '1':
        return 'Factura'
    elif codigo == '2':
        return 'Autofactura'
    elif codigo == '3':
        return 'Boleta de Venta'
    elif codigo == '4':
        return 'Nota de Crédito'
    elif codigo == '11':
        return 'Comprobante de Ingreso de Entidades Públicas, Religiosas o de Beneficio Público'
    else:
        return ''

# NOTE: Están todas las opciones
def obtener_tipo_egreso_texto(codigo):
    if codigo == 'gasto':
        return 'Gasto'
    elif codigo == 'inversion_actividad':
        return 'Inversiones Relacionadas a la Actividad Gravada'
    else:
        return 'Inversiones Personales y de familiares a Cargo'

# TODO: Debería ser un switch con todas las opciones (tiene solo llas que yo potencialmente usaría)
def obtener_sub_tipo_egreso_texto(codigo):
    if codigo == 'GPERS':
        return 'Gastos personales y de familiares a cargo realizados en el país'
    elif codigo == 'PREST':
        return 'Amortización o cancelación de préstamos obtenidos antes de ser contribuyente del IRP, así como sus intereses, comisiones y otros recargos'
    elif codigo == 'MEH':
        return 'Muebles, Equipos y Herramientas'
    elif codigo == 'INM':
        return 'Adquisición de inmuebles, construcción o mejoras de inmuebles'
    elif codigo == 'EDU':
        return 'Educación y/o Capacitación'
    elif codigo == 'GSTADM':
        return 'Intereses, comisiones y demás gastos administrativos'
    elif codigo == 'RECPOS':
        return 'Intereses, comisiones y otros recargos pagados por los préstamos obtenidos, con posterioridad a ser contribuyentes del IRP'
    elif codigo == 'CMPOF':
        return 'Compra de útiles de oficina, gastos de limpieza y mantenimiento'
    elif codigo == 'ACCIONES':
        return 'Compra de acciones o cuotas partes de sociedades constituidas en el país'
    elif codigo == 'SALUD':
        return 'Salud.'
    else:
        return 'Otros gastos realizados relacionados a la actividad gravada'

egresos = []
with open('IRP - Egresos.csv', newline='') as csvfile: # TODO: Pasar como parametro
    reader = csv.DictReader(csvfile)
    try:
        for idx, row in enumerate(reader):
            # print('Registro nro.: ', idx)
            # crear un item de ingreso por cada registro en el csv de Ingresos
            # Ejemplo item egreso
            # {
            #   "periodo": "2017",
            #   "tipo": "1",
            #   "relacionadoTipoIdentificacion": "RUC",
            #   "fecha": "2017-11-22",
            #   "id": 24,
            #   "importe": null,
            #   "ruc": "3893208",
            #   "egresoMontoTotal": 55455,
            #   "relacionadoNombres": "LA VIENESA S.A.",
            #   "relacionadoNumeroIdentificacion": "80025405",
            #   "timbradoCondicion": "contado",
            #   "timbradoDocumento": "010-002-0009859",
            #   "timbradoNumero": "12325328",
            #   "tipoEgreso": "gasto",
            #   "tipoEgresoTexto": "Gasto",
            #   "tipoTexto": "Factura",
            #   "subtipoEgreso": "GPERS",
            #   "subtipoEgresoTexto": "Gastos personales y de familiares a cargo realizados en el país"
            # }
            json_data = {}

            json_data['periodo'] = "2018" # TODO: Pasar como parametro
            json_data['tipo'] = row['tipo_documento']
            json_data['relacionadoTipoIdentificacion'] = row['tipo_identificacion']
            json_data['fecha'] = row['fecha']
            json_data['importe'] = None
            json_data['ruc'] = "3893208" # TODO: Pasar como parametro
            json_data['egresoMontoTotal'] = int(row['monto_total_egreso'])
            json_data['relacionadoNombres'] = row['razon_social']
            json_data['relacionadoNumeroIdentificacion'] = row['numero_identificacion']
            if row['tipo_documento'] == '1': # solo si es factura
                json_data['timbradoCondicion'] = row['condicion_venta']
            json_data['timbradoDocumento'] = row['numero_documento']
            if row['tipo_documento'] != '11': # entidad publica no requiere timbrado, solo nro de doc
                json_data['timbradoNumero'] = row['timbrado']
            json_data['tipoEgreso'] = row['tipo_egreso']
            json_data['tipoEgresoTexto'] = obtener_tipo_egreso_texto(row['tipo_egreso'])
            json_data['tipoTexto'] = obtener_tipo_documento_texto(row['tipo_documento'])
            json_data['subtipoEgreso'] = row['clasificacion_egreso']
            json_data['subtipoEgresoTexto'] = obtener_sub_tipo_egreso_texto(row['clasificacion_egreso'])
            # ingreso_data = json.dumps(json_data, ensure_ascii=False)
            # print(ingreso_data)
            egresos.append(json_data)
        print('Éxito: todos los registros fueron generados correctamente')
    except Exception as e:
        print(str(e))
        print('Error: ningún registro se procesará')

with open('base.json', 'r+') as f:
    data = json.load(f)
    updated_data = data
    updated_data['egresos'] = egresos

    with open('test-egresos.json', 'w') as outfile:
        json.dump(updated_data, outfile, ensure_ascii=False)
