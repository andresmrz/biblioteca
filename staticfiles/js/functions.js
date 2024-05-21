/**
 * Muestra un popover con detalles de un libro específico.
 * @param {HTMLElement} objeto - Elemento HTML que dispara la función.
 * @param {string} url_editar - URL para editar el libro.
 * @param {string} url_prestar - URL para prestar el libro.
 * @param {string} titulo - Título del libro.
 * @param {string} autor - Autor del libro.
 * @param {number} anio_publicacion - Año de publicación del libro.
 * @param {number} cantidad_stock - Cantidad de libros en stock.
 */

function listaLibroVerDetalles(objeto, url_editar, url_prestar, titulo, autor, anio_publicacion, cantidad_stock)
{
    var rect = objeto.getBoundingClientRect();
    var top = rect.top + rect.height / 2 + window.scrollY;
    var left = rect.right + 10 + window.scrollX;

    var popover = document.getElementById('lista-libro-popover');

    popover.style.top = (top - 120) + 'px';
    popover.style.left = (left - 30) + 'px';
    popover.style.display = 'block';

    document.getElementById('lista-libro-detalles-titulo').innerHTML = '<b>Titulo: </b>' + titulo;
    document.getElementById('lista-libro-detalles-autor').innerHTML = '<b>Autor: </b>' + autor;
    document.getElementById('lista-libos-detalles-anio-publicacion').innerHTML = '<b>Año de publicación: </b>' + anio_publicacion;
    document.getElementById('lista-libro-detalles-cantidad-stock').innerHTML = '<b>Cantidad en stock: </b>' + cantidad_stock;

    if(document.getElementById('lista-libro-detalles-editar'))
    {
        document.getElementById('lista-libro-detalles-editar').href = url_editar;
    }

    if(document.getElementById('lista-libro-detalles-prestar'))
    {
        document.getElementById('lista-libro-detalles-prestar').href = url_prestar;
    }

    document.getElementById('lista-libro-eliminar').dataset.id = objeto.dataset.id;
}

/**
 * Elimina un libro de la base de datos.
 * @param {HTMLElement} objeto - Elemento HTML que representa el libro a eliminar.
 */

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

/**
 * Permite al usuario devolver un libro prestado.
 * @param {number} id - ID del libro a devolver.
 */

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
 
/**
 * Cierra un popover especificado.
 * @param {string} id - Identificador del popover a cerrar.
 */

function closePopover(id) 
{
    var popover = document.getElementById(id + '-' + 'popover');
    popover.style.display = 'none';
}

/**
 * Obtiene el valor de una cookie especificada.
 * @param {string} name - Nombre de la cookie deseada.
 * @returns {string|null} Valor de la cookie si se encuentra, null de lo contrario.
 */

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
