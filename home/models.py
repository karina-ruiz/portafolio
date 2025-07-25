from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.images.models import Image
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

#  Página de inicio
class HomePage(Page):
    subtitulo = models.CharField(max_length=250, blank=True, help_text="Frase llamativa bajo el título")
    introduccion = RichTextField(blank=True)
    imagen_destacada = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_texto = models.CharField(max_length=50, blank=True, help_text="Texto del botón")
    cta_enlace = models.URLField(blank=True, help_text="Enlace del botón CTA")

    content_panels = Page.content_panels + [
        FieldPanel("subtitulo"),
        FieldPanel("introduccion"),
        FieldPanel("imagen_destacada"),  # 👈 corregido
        FieldPanel("cta_texto"),
        FieldPanel("cta_enlace"),
    ]


# Página "Sobre mí"
class AboutPage(Page):
    biografia = RichTextField(blank=True)
    años_experiencia = models.IntegerField(default=0)
    tecnologias_destacadas = models.CharField(max_length=200, help_text="Ej: Python, Django, React")
    imagen_perfil = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel("biografia"),
        FieldPanel("años_experiencia"),
        FieldPanel("tecnologias_destacadas"),
        FieldPanel("imagen_perfil"),  # 👈 corregido
    ]


#  Página de servicios
class ServiciosPage(Page):
    descripcion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("descripcion"),
        InlinePanel("servicios", label="Servicios"),
    ]

#  Ítems de servicios
class ServicioItem(Orderable):
    page = ParentalKey("ServiciosPage", on_delete=models.CASCADE, related_name="servicios")
    titulo = models.CharField(max_length=100)
    descripcion = RichTextField()
    icono = models.CharField(max_length=50, blank=True, help_text="Ej: bi-code-slash")
    enlace = models.URLField(blank=True, help_text="Enlace opcional a más info")

    panels = [
        FieldPanel("titulo"),
        FieldPanel("descripcion"),
        FieldPanel("icono"),
        FieldPanel("enlace"),
    ]


# Índice de proyectos
class ProyectosIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


# Proyecto individual
class ProyectoPage(Page):
    cliente = models.CharField(max_length=100)
    resumen = RichTextField()
    tecnologias = models.CharField(max_length=200)
    fecha = models.DateField(blank=True, null=True)
    imagen = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    enlace_demo = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("cliente"),
        FieldPanel("resumen"),
        FieldPanel("tecnologias"),
        FieldPanel("fecha"),
        FieldPanel("imagen"),  # 👈 corregido
        FieldPanel("enlace_demo"),
    ]


# Formulario de contacto
class FormField(AbstractFormField):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")


class ContactPage(AbstractEmailForm):
    gracias = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel("form_fields", label="Campos del formulario"),
        FieldPanel("gracias"),
    ]

    def get_landing_page_template(self, request=None):
        return "home/contact_page_landing.html"
