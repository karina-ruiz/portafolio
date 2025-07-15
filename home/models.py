from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


 
class HomePage(Page):
    introduccion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduccion"),
    ]



class ServiciosPage(Page):
    descripcion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("descripcion"),
        InlinePanel("servicios", label="Servicios"), 
    ]


# 🔹 Submodelo: Ítems individuales de servicio dentro de ServiciosPage
class ServicioItem(Orderable):
    page = ParentalKey("ServiciosPage", on_delete=models.CASCADE, related_name="servicios")
    titulo = models.CharField(max_length=100)
    descripcion = RichTextField()
    icono = models.CharField(max_length=50, blank=True)  
    panels = [
        FieldPanel("titulo"),
        FieldPanel("descripcion"),
        FieldPanel("icono"),
    ]



class ProyectosIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]



class ProyectoPage(Page):
    cliente = models.CharField(max_length=100)
    resumen = RichTextField()
    tecnologias = models.CharField(max_length=200, help_text="Ej: Django, React, PostgreSQL")

    content_panels = Page.content_panels + [
        FieldPanel("cliente"),
        FieldPanel("resumen"),
        FieldPanel("tecnologias"),
    ]



class AboutPage(Page):
    biografia = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("biografia"),
    ]



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
