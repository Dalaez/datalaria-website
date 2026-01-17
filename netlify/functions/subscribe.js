// Netlify Function: Subscribe to Brevo Newsletter
// POST /api/subscribe - Adds a contact to Brevo list

exports.handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, error: 'Method not allowed' })
    };
  }

  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  try {
    const { email, name } = JSON.parse(event.body);

    // Validate input
    if (!email || !email.includes('@')) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, error: 'Valid email is required' })
      };
    }

    // Get API key from environment variable
    const apiKey = process.env.BREVO_API_KEY;
    if (!apiKey) {
      console.error('BREVO_API_KEY environment variable not set');
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ success: false, error: 'Server configuration error' })
      };
    }

    // Split name into first and last name
    const nameParts = (name || '').trim().split(' ');
    const firstName = nameParts[0] || '';
    const lastName = nameParts.slice(1).join(' ') || '';

    // Brevo API request to create/update contact
    const response = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'api-key': apiKey
      },
      body: JSON.stringify({
        email: email,
        attributes: {
          FIRSTNAME: firstName,
          LASTNAME: lastName
        },
        listIds: [3], // List ID #3
        updateEnabled: true // Update if contact already exists
      })
    });

    // Handle Brevo response
    if (response.ok || response.status === 201 || response.status === 204) {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ success: true, message: 'Successfully subscribed!' })
      };
    }

    // Contact already exists (duplicate) - still a success
    if (response.status === 400) {
      const errorData = await response.json();
      if (errorData.code === 'duplicate_parameter') {
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({ success: true, message: 'Already subscribed!' })
        };
      }
      throw new Error(errorData.message || 'Subscription failed');
    }

    const errorData = await response.json();
    throw new Error(errorData.message || 'Subscription failed');

  } catch (error) {
    console.error('Newsletter subscription error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ success: false, error: error.message || 'An error occurred' })
    };
  }
};
