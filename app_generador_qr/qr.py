import base64
import io
from urllib.parse import quote

import qrcode


def payload_desde_formulario(tipo, datos):
    if tipo == 'url':
        return datos['url']

    if tipo == 'texto':
        return datos['texto']

    if tipo == 'wifi':
        return (
            f"WIFI:T:{datos['seguridad']};"
            f"S:{datos['ssid']};"
            f"P:{datos.get('password', '')};;"
        )

    if tipo == 'vcard':
        vcard_lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{datos['apellidos']};{datos['nombre']};;;",
            f"FN:{datos['nombre']} {datos['apellidos']}",
            f"TEL;TYPE=CELL:{datos['telefono']}",
            f"EMAIL;TYPE=INTERNET:{datos['email']}"
        ]
        
        # Añadir campos opcionales si existen en los datos
        if datos.get('empresa'):
            vcard_lines.append(f"ORG:{datos['empresa']}")
        if datos.get('cargo'):
            vcard_lines.append(f"TITLE:{datos['cargo']}")
            
        vcard_lines.append("END:VCARD")
        
        # Unir todas las líneas con saltos de línea correctos
        return "\n".join(vcard_lines)        
    
    telefono = datos['telefono']
    mensaje = datos.get('mensaje') or ''
    if mensaje:
        return f'https://wa.me/{telefono}?text={quote(mensaje)}'
    return f'https://wa.me/{telefono}'


def imagen_qr_base64(contenido):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(contenido)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color='#1e1b2e', back_color='white')
    buffer = io.BytesIO()
    imagen.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('ascii')
