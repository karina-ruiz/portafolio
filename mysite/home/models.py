from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


# --- HOMEPAGE ---
class HomePage(Page):
    subtitulo = models.CharField(max_length=255, blank=True)
    introduccion = RichTextField(blank=True)
    imagen_destacada = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_texto = models.CharField(max_length=100, blank=True, help_text="Texto del botón de llamada a la acción")
    cta_enlace = models.URLField(blank=True, help_text="URL del botón de llamada a la acción")

    content_panels = Page.content_panels + [
        FieldPanel('subtitulo'),
        FieldPanel('introduccion'),
        FieldPanel('imagen_destacada'),
        MultiFieldPanel([
            FieldPanel('cta_texto'),
            FieldPanel('cta_enlace'),
        ], heading="Llamado a la acción"),
    ]


# --- ABOUT PAGE ---
class AboutPage(Page):
    biografia = RichTextField(blank=True, help_text="Texto biográfico sobre tu experiencia y trayectoria")
    anios_experiencia = models.PositiveIntegerField(default=0, help_text="Años de experiencia profesional")
    tecnologias_destacadas = StreamField(
        [
            ('tecnologia', blocks.CharBlock(required=True, help_text="Nombre de la tecnología destacada")),
        ],
        use_json_field=True,
        blank=True,
        help_text="Lista de tecnologías que dominas o usas frecuentemente"
    )
    imagen_perfil = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagen de perfil profesional"
    )

    content_panels = Page.content_panels + [
        FieldPanel('biografia'),
        FieldPanel('anios_experiencia'),
        FieldPanel('tecnologias_destacadas'),
        FieldPanel('imagen_perfil'),
    ]


# --- SERVICIOS PAGE ---
class ServiciosPage(Page):
    descripcion = RichTextField(blank=True, help_text="Descripción general de los servicios")

    content_panels = Page.content_panels + [
        FieldPanel('descripcion'),
    ]

    subpage_types = ['home.ServiciosItem']


# --- SERVICIOS ITEM ---
class ServiciosItem(Page):
    titulo = models.CharField(max_length=255, help_text="Nombre del servicio")
    descripcion = models.TextField(help_text="Descripción del servicio")
    icono = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Ícono representativo del servicio"
    )
    enlace = models.URLField(blank=True, help_text="Enlace para más información (opcional)")

    content_panels = Page.content_panels + [
        FieldPanel('titulo'),
        FieldPanel('descripcion'),
        FieldPanel('icono'),
        FieldPanel('enlace'),
    ]

    parent_page_types = ['home.ServiciosPage']
    subpage_types = []


# --- PROYECTOS INDEX PAGE ---
class ProyectosIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        proyectos = ProyectoPage.objects.child_of(self).live().order_by('-fecha')
        context['proyectos'] = proyectos
        return context


# --- PROYECTO PAGE ---
class ProyectoPage(Page):
    cliente = models.CharField(max_length=255, blank=True, help_text="Nombre del cliente")
    resumen = RichTextField(blank=True, help_text="Resumen del proyecto")
    tecnologias = StreamField(
        [
            ('tecnologia', blocks.CharBlock(help_text="Tecnología usada")),
        ],
        use_json_field=True,
        blank=True,
        help_text="Lista de tecnologías usadas en este proyecto"
    )
    fecha = models.DateField(help_text="Fecha de realización o entrega")
    imagen = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagen destacada del proyecto"
    )
    enlace_demo = models.URLField(blank=True, help_text="Enlace a demo en vivo o repositorio")

    content_panels = Page.content_panels + [
        FieldPanel('cliente'),
        FieldPanel('resumen'),
        FieldPanel('tecnologias'),
        FieldPanel('fecha'),
        FieldPanel('imagen'),
        FieldPanel('enlace_demo'),
    ]

    parent_page_types = ['home.ProyectosIndexPage']
    subpage_types = []


# --- CONTACT PAGE ---
class ContactPage(AbstractEmailForm):
    gracias = RichTextField(blank=True, help_text="Mensaje de agradecimiento tras enviar formulario")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('gracias'),
        InlinePanel('form_fields', label="Campos del formulario"),
        MultiFieldPanel([
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('subject'),
        ], heading="Configuración de correo electrónico"),
    ]


class FormField(AbstractFormField):
    page = models.ForeignKey(
        ContactPage,
        on_delete=models.CASCADE,
        related_name='form_fields',
    )
