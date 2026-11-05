from django.http import HttpResponseBadRequest
from django.shortcuts import render

from .forms import FORMULARIOS
from .qr import imagen_qr_base64, payload_desde_formulario


def generador_qr_index(request):
    tipo = 'url'
    return render(request, 'index.html', {
        'tipo': tipo,
        'form': FORMULARIOS[tipo](),
        'qr_base64': None,
    })


def campos_qr(request):
    tipo = request.GET.get('tipo', 'url')
    formulario = FORMULARIOS.get(tipo)
    if formulario is None:
        return HttpResponseBadRequest('Tipo de QR no válido.')

    return render(request, 'partials/campos_qr.html', {
        'tipo': tipo,
        'form': formulario(),
    })


def generar_qr(request):
    tipo = request.POST.get('tipo')
    formulario = FORMULARIOS.get(tipo)
    if formulario is None:
        return HttpResponseBadRequest('Tipo de QR no válido.')

    form = formulario(request.POST)
    qr_base64 = None
    caption = 'Revisa los campos marcados e inténtalo de nuevo.'

    if form.is_valid():
        contenido = payload_desde_formulario(tipo, form.cleaned_data)
        qr_base64 = imagen_qr_base64(contenido)
        caption = 'Tu código QR está listo para descargar.'

    contexto = {
        'tipo': tipo,
        'form': form,
        'qr_base64': qr_base64,
        'caption': caption,
    }

    if request.headers.get('HX-Request', '').lower() == 'true':
        return render(request, 'partials/qr_resultado.html', contexto)

    return render(request, 'index.html', contexto)