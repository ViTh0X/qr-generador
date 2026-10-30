from django import forms


WIDGET_ATTRS = {
    'class': 'form-control',
}


class QrUrlForm(forms.Form):
    url = forms.URLField(
        label='URL del sitio',
        widget=forms.URLInput(attrs={
            **WIDGET_ATTRS,
            'placeholder': 'https://tusitio.com',
            'autocomplete': 'url',
        }),
    )


class QrTextoForm(forms.Form):
    texto = forms.CharField(
        label='Texto',
        widget=forms.Textarea(attrs={
            **WIDGET_ATTRS,
            'rows': 4,
            'placeholder': 'Escribe el mensaje que quieres compartir',
        }),
    )


class QrWifiForm(forms.Form):
    ssid = forms.CharField(
        label='Nombre de la red (SSID)',
        widget=forms.TextInput(attrs={
            **WIDGET_ATTRS,
            'placeholder': 'Mi WiFi',
            'autocomplete': 'off',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={
            **WIDGET_ATTRS,
            'placeholder': '••••••••',
            'autocomplete': 'off',
        }),
    )
    seguridad = forms.ChoiceField(
        label='Seguridad',
        choices=(
            ('WPA', 'WPA / WPA2'),
            ('WEP', 'WEP'),
            ('nopass', 'Sin contraseña'),
        ),
        widget=forms.Select(attrs=WIDGET_ATTRS),
    )

    def clean(self):
        data = super().clean()
        if data.get('seguridad') != 'nopass' and not data.get('password'):
            self.add_error('password', 'Ingresa la contraseña de la red.')
        return data


class QrWhatsappForm(forms.Form):
    telefono = forms.CharField(
        label='Número con código de país',
        widget=forms.TextInput(attrs={
            **WIDGET_ATTRS,
            'placeholder': '573001234567',
        }),
    )
    mensaje = forms.CharField(
        label='Mensaje (opcional)',
        required=False,
        widget=forms.Textarea(attrs={
            **WIDGET_ATTRS,
            'rows': 3,
            'placeholder': 'Hola, quiero más información',
        }),
    )

    def clean_telefono(self):
        digitos = ''.join(caracter for caracter in self.cleaned_data['telefono'] if caracter.isdigit())
        if len(digitos) < 8:
            raise forms.ValidationError('Ingresa el número con código de país.')
        return digitos

class QRVCardForm(forms.Form):
    # Campos de Nombre
    nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Juan'})
    )
    apellidos = forms.CharField(        
        label="Apellidos",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Pérez Gómez'})
    )
    
    # Campos de Contacto
    telefono = forms.CharField(        
        label="Teléfono Móvil",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. +34600000000'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'Ej. juan.perez@email.com'})
    )
    
    # Campos Laborales (Opcionales)
    empresa = forms.CharField(    
        required=False, 
        label="Empresa",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Mi Empresa S.A.'})
    )
    cargo = forms.CharField(        
        required=False, 
        label="Cargo o Puesto",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Gerente de Ventas'})
    )


FORMULARIOS = {
    'url': QrUrlForm,
    'vcard':QRVCardForm,
    'texto': QrTextoForm,
    'wifi': QrWifiForm,
    'whatsapp': QrWhatsappForm,
}
