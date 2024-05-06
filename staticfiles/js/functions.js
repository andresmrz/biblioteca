
function listaLibroVerDetalles(objeto, url_editar, url_prestar, titulo, autor, anio_publicacion, cantidad_stock)
{
    var rect = objeto.getBoundingClientRect();
    var top = rect.top + rect.height / 2 + window.scrollY;
    var left = rect.right + 10 + window.scrollX;

    var popover = document.getElementById('lista-libro-popover');

    popover.style.top = (top - 120) + 'px';
    popover.style.left = (left - 30) + 'px';
    popover.style.display = 'block';

    $('#lista-libro-detalles-titulo').html('<b>Titulo: </b>' + titulo);
    $('#lista-libro-detalles-autor').html('<b>Autor: </b>' + autor);
    $('#lista-libos-detalles-anio-publicacion').html('<b>Año de publicación: </b>' + anio_publicacion);
    $('#lista-libro-detalles-cantidad-stock').html('<b>Cantidad en stock: </b>' + cantidad_stock);

    document.getElementById('lista-libro-detalles-editar').href = url_editar;
    document.getElementById('lista-libro-detalles-prestar').href = url_prestar;
    document.getElementById('lista-libro-eliminar').dataset.id = objeto.dataset.id;
}

function eliminarLibro(objeto) 
{
    if(!confirm('¿Estás seguro de que quieres eliminar este libro?'))
    {
        return;  // No hacer nada si el usuario cancela la operación
    }
  
    fetch(`/api/libros/eliminar/${objeto.dataset.id}/`, 
    {
      method: 'DELETE',
      headers: 
      {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => 
    {
        if(response.ok)
        {
            alert('Libro eliminado correctamente.');
            window.location.href = '/libros/';  // Redirigir a la lista de libros
        }
        else
        {
            throw new Error('Algo salió mal al intentar eliminar el libro');
        }
    })
    .catch(error => 
    {
        console.error('Error:', error);
    });
}

function devolverLibro(id) 
{
    if(!confirm('¿Estás seguro de que quieres devolver este libro?'))
    {
        return;  // No hacer nada si el usuario cancela la operación
    }

    fetch('/api/libros/devolver/' + id + '/', 
    {
        method: 'PATCH',
        headers: 
        {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .then(response => 
    {
    if (response.ok)
    {
        return response.json();
    }
    else
    {
        throw new Error('Algo salió mal en la API');
    }
    })
    .then(data => 
    {
        console.log('Devolución realizada:', data);
        window.location.href = '/libros/historial/';;
    })
    .catch(error => 
    {
        console.error('Error al realizar la devolución:', error);
        alert(error.error || 'Un error ocurrió al realizar la devolución.');  // Muestra el mensaje de error al usuario
    });
}
  
function closePopover(id) 
{
    var popover = document.getElementById(id + '-' + 'popover');
    popover.style.display = 'none';
}

function getCookie(name) 
{
    let cookieValue = null;
    if(document.cookie && document.cookie !== '') 
    {
        const cookies = document.cookie.split(';');

        for(let i = 0; i < cookies.length; i++)
        {
            const cookie = cookies[i].trim();

            if(cookie.substring(0, name.length + 1) === (name + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }
    return cookieValue;
}
