# Taller caché

Para recordar, ¿qué es el caché?. Es un componente que se encarga de guardar solicitudes que hagamos para que en un futuro estás sean mucho más rápidas.

Por ejemplo, una solicitud que realizamos muchas veces, en temas de costo de las solicitudes se harían mucho más caras debido a la gran cantidad.

Su funcionamiento se basa en la siguiente lógica.

```py
Dada una URL, try encontrar la página in cache
if la página is in cache:
    return la página guardada en cache
else:
    generar la página
    guardar la página generada in cache (for next time)
    return la página generada
```

Entonces, cada vez que se realiza una query o solicitud a la página, esta misma se almacena para ser retornada directamente sin generar la información de nuevo.

#### Ventajas

-   Vuelve más rápida solicitudes pesadas.
    
-   Genera un dinamismo más fluido al no cargas innecesarias.
    

#### Desventajas

-   Genera muchos peso en la información almacenada.
    
-   Se tiene que seleccionar bien que información se va a almacenar.
    

Django permite hacer el cache de distintas querys, vistas, solicitudes. Para poder crear este sistema dentro de nuestra aplicación seguiremos los pasos a continuación.

## SetUp

Para poder crear nuestro caché necesitamos definir algunas cosas. Por ejemplo, donde se encontrará la información almacenada, puede ser dentro de una base de datos, en un archivo del sistema o directamente en la memoria. Esta es una decisión de suma importancia que impactará en el rendimiento de nuestra caché.

Para nuestra aplicación utilizaremos el basado en memoria.

### Memcached

Este es un server caché, enteramente basado en memoria. Es utilizado en app como Facebook o Wikipedia para reducir la cantidad de veces que se accede a la base de datos, he incrementa increíblemente el rendimiento de las páginas.

Para instalar Memcached dentro de nuestro entorno virtual, ejecutamos lo siguiente.

```shell
pip install python-memcached
```

Para que funciona, debemos instanciarlo en algún puerto, en este caso trabajará dentro del puerto 11211. Dentro de nuestro archivo `settings.py` añadimos las siguientes líneas.

```py
SESSIONS_ENGINE='django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

-   `BACKEND`: Define el tipo de caché que utilizaremos.
    
-   `LOCATION`: Define el servidor o servidores a utilizar.
    

Una ventaja de Memcached, es funciona en distintos servidores. Esto significa que puede tomar distintos servidores como uno solo. Añadiremos otro servidor para nuestro caché.

```py
SESSIONS_ENGINE='django.contrib.sessions.backends.cache'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": ["127.0.0.1:11211", "127.0.0.2:11212"],
    }
}
```

Con todo configurado, podemos añadir el caché a nuestras vistas.

## Caché en vistas

Si recordamos la sesión pasada realizamos la creación de un `ListView`, ahora a esa misma vista le añadiremos el caché.

```py
# ...
class BookList(ListView):
    model = Book
    template_name = "booklist.html"
```

Para las vistas de tipo clase, tenemos que definir el caché en el url. Se explicará posteriormente el motivo de `60 * 15`

```py
from django.views.decorators.cache import cache_page
urlpatterns = [
    path("", cache_page(60*15)(views.BookList.as_view()), name="BookList")
]
```

Pero también existe el caso de que sea en una vista de tipo función, para este caso el caché está definido de la siguiente forma.

```py
@cache_page(60 * 15)
def my_view(request):
    ...
```

Para este caso, toma un solo argumento, que es el `timeout`, que indica la cantidad de tiempo que permanecerá la vista en la caché.

`timeout` esta definido en segundos, por lo que en este caso estamos definiendo un tiempo de 15 minutos.

-   60 es 1 minuto y tenemos 15 veces 1 minuto.

## Caché en templates

También podemos ingresar a la caché algunos fragmentos de un template que nosotros indiquemos.

```html
{% load cache %}
{% cache 500 sidebar %}
    .. sidebar ..
{% endcache %}
```

Con `load cache`, tenemos acceso a la caché dentro de nuestro template. Luego, en los siguiente tags, caché recibe el `timeoout`.

## Sesiones en Django

En el taller de vista, pudimos hacer uso de lo que son sesiones, ahora lo exploraremos más a profundo.

Django ofrece soporte para las sesiones anónimas, con las sesiones podemos guardar y obtener información que nosotros mismos definamos.

Por ejemplo, creamos una nueva vista. En esta obtenemos un solo objeto.

```py
def select_book(request, id):
    book = Book.objects.filter(bookID = id)
    request.session["authors"] = book[0].authors
    context = {}
    context["book"] = book[0]
    return render(request, "oneBook.html", context)
```

Para este caso estamos definiendo dentro de nuestra sesión el autor del libro. Luego definiremos una vista que reciba y renderice únicamente el autor.

```py
def author(request, id):
    context = {}
    context["author"] = request.session["authors"]
    return render(request, "author.html", context)
```

Entonces, cuando se haga uso de esta vista, usaremos lo guardado en la sesión, esto nos evita agregar la información en el parámetro o realizar una nueva query a la base de datos para obtener la información.

Creamos nuestros templates.

-   `oneBook.html`

```html
{% extends 'base.html' %}

{% block content %}
<ul>

<li>{{book.title}}</li> 
<li><a href="{% url 'onlyAuthor' book.bookID%}">{{book.authors}}</a></li>
<li>{{book.average_rating}}</li>
<li>{{book.isbn}}</li>

</ul>
{% endblock %}
```

Generamos

-   `author.html`

```html
{% extends 'base.html' %}

{% block content %}
<ul>
<li>{{author}}</li>
</ul>
{% endblock %}
```

Con esto mostraremos únicamente el autor dentro de otra vista, sin realizar ninguna query a la base de datos y sin enviar la información como parámetro.

## Tarea

-   Implementar lo visto en el taller.
    
-   Añadir 2 servidores para el caché.
    
-   Añadir una nueva vista que obtenga los 10 primeros resultados del ListView, este debe tener un timeout de 10 minutos.
    
-   Añadir a la vista principal del ListView (`booklist.html`) un caché a todo el for dentro del template, este debe tener un timeout de 5 minutos.
    
-   Implementar un sistema entre la vista `selectBook` y `author`, que evite inconsistencia en la información si se modifica el url.
    
    -   Cuando se hace la ruta `book/<id>` y luego se pasa a `book/<id>/author` si se modifica el segundo url, por la sesión se mostraría la misma información. Generar un sistema que verifique que el author guardado en la sesión, sea el mismo al que le pertenece el id de la URL.
        
    -   Si no existe el id, renderizar `No existe el autor`.
        

### Opcional

Implementar los otros métodos de caché. Tanto el de base de datos y el de archivos.

Links:
[Diapositivas](https://docs.google.com/presentation/d/e/2PACX-1vSumcxHgirBr2y5dhb-gb3KYkDOZkZbVe6ycj4bKp7vP4q4ykdbidpTyh8gnu0TBDsd_97ThY-lc7KI/embed?start=false&loop=false&delayms=3000&slide=id.g1a360ea300c_0_2)

Videos:
[Teoria](https://www.youtube.com/watch?v=6mUF8mVHwHY&list=PLxI5H7lUXWhjV-yCSEuJXxsDmNESrvbw3&index=13&ab_channel=Silabuz)
[Practica](https://www.youtube.com/watch?v=Pt2bOKhPltM&list=PLxI5H7lUXWhjV-yCSEuJXxsDmNESrvbw3&index=14&ab_channel=Silabuz)
