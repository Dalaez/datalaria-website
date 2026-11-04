// netlify/functions/subscribe.js

const ALLOWED_LISTS = ['newsletter', 'helix'];

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type, Accept',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Content-Type': 'application/json'
};

exports.handler = async (event) => {
  // 1. Manejar preflight OPTIONS para CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: corsHeaders,
      body: ''
    };
  }

  // 2. Validar que el método sea POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: corsHeaders,
      body: JSON.stringify({ success: false, error: 'Method Not Allowed' })
    };
  }

  try {
    // 3. Extraer y validar el cuerpo de la solicitud
    let data;
    try {
      data = typeof event.body === 'string' ? JSON.parse(event.body) : (event.body || {});
    } catch (e) {
      return {
        statusCode: 400,
        headers: corsHeaders,
        body: JSON.stringify({ success: false, error: 'Cuerpo de solicitud inválido (JSON malformado).' })
      };
    }

    const { email, name, language, list } = data;

    // 4. Validar datos esenciales
    if (!email || !email.includes('@') || !name) {
      return {
        statusCode: 400,
        headers: corsHeaders,
        body: JSON.stringify({ success: false, error: 'Nombre y correo válido son obligatorios.' })
      };
    }

    // 5. Obtener la clave API desde las variables de entorno de Netlify
    const apiKey = process.env.BREVO_API_KEY;
    if (!apiKey) {
      console.error('Error Crítico: La variable de entorno BREVO_API_KEY no está configurada.');
      return {
        statusCode: 500,
        headers: corsHeaders,
        body: JSON.stringify({ success: false, error: 'Error de configuración en el servidor.' })
      };
    }

    // 6. Lógica para separar Nombre y Apellido
    const nameParts = (name || '').trim().split(/\s+/);
    const firstName = nameParts[0] || '';
    const lastName = nameParts.slice(1).join(' ') || '';

    // 7. Lógica para seleccionar la lista por idioma y lista blanca ('newsletter' | 'helix')
    const contactLanguage = (language || 'es').toLowerCase() === 'en' ? 'en' : 'es';
    const targetList = ALLOWED_LISTS.includes(list) ? list : 'newsletter';

    let listId;
    if (targetList === 'helix') {
      listId = contactLanguage === 'es'
        ? Number(process.env.BREVO_HELIX_LIST_ES || 5)
        : Number(process.env.BREVO_HELIX_LIST_EN || 6);
    } else {
      listId = contactLanguage === 'es' ? 3 : 4;
    }

    // 8. Construir el payload para la API de Brevo
    const payload = {
      email: email.trim().toLowerCase(),
      attributes: {
        FIRSTNAME: firstName,
        LASTNAME: lastName,
        LANGUAGE: contactLanguage.toUpperCase() === 'EN' ? 'en' : 'es',
      },
      listIds: [listId],
      updateEnabled: true,
    };

    // 9. Realizar la llamada a la API de Brevo
    const response = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'api-key': apiKey,
      },
      body: JSON.stringify(payload),
    });

    // 10. Manejar respuestas exitosas (201 Created o 204 No Content)
    if (response.ok || response.status === 201 || response.status === 204) {
      return {
        statusCode: 200,
        headers: corsHeaders,
        body: JSON.stringify({ success: true, message: 'Suscripción exitosa', list: targetList, listId: listId })
      };
    }

    // 11. Manejo de errores específicos (ej. duplicados)
    let errorData = {};
    try {
      errorData = await response.json();
    } catch (e) {
      errorData = { message: `HTTP ${response.status}` };
    }

    if (response.status === 400 && (errorData.code === 'duplicate_parameter' || (errorData.message && errorData.message.toLowerCase().includes('already exist')))) {
      return {
        statusCode: 200,
        headers: corsHeaders,
        body: JSON.stringify({ success: true, message: 'Contacto ya registrado y actualizado', list: targetList, listId: listId })
      };
    }

    console.error('Error desde la API de Brevo:', JSON.stringify(errorData, null, 2));
    return {
      statusCode: response.status,
      headers: corsHeaders,
      body: JSON.stringify({ success: false, error: errorData.message || 'No se pudo procesar la suscripción.' })
    };

  } catch (error) {
    console.error('Error inesperado en la función subscribe:', error);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ success: false, error: 'Ocurrió un error interno en el servidor.' })
    };
  }
};
