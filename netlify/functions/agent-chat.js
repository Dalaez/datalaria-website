/**
 * Netlify Function: Agent Chat Proxy
 * 
 * Proxies requests to Algolia Agent Studio API to bypass CORS restrictions.
 * This enables the browser to communicate with the AI agent.
 */

const ALGOLIA_APP_ID = process.env.ALGOLIA_APP_ID || 'C4NV3SCYAM';
const ALGOLIA_SEARCH_KEY = process.env.ALGOLIA_SEARCH_API_KEY;
const ALGOLIA_AGENT_ID = process.env.ALGOLIA_AGENT_ID || 'f27a0952-b61a-4526-9c37-68e9a2a441d0';

exports.handler = async (event, context) => {
    // Only allow POST requests
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    try {
        const { query, conversationId, language } = JSON.parse(event.body);

        if (!query) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Query is required' })
            };
        }

        console.log(`[Agent Chat] Query: "${query}", Lang: ${language}`);

        // Call Algolia Agent Studio API
        const agentUrl = `https://${ALGOLIA_APP_ID}.algolia.net/1/agents/${ALGOLIA_AGENT_ID}/chat`;

        const response = await fetch(agentUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Algolia-API-Key': ALGOLIA_SEARCH_KEY,
                'X-Algolia-Application-Id': ALGOLIA_APP_ID,
                'X-Api-Version': '2025-01-01'
            },
            body: JSON.stringify({
                query: query,
                conversationId: conversationId || undefined,
                language: language || 'en'
            })
        });

        const data = await response.json();

        console.log(`[Agent Chat] Response status: ${response.status}`);

        if (!response.ok) {
            // If Agent API fails, fall back to search
            console.log('[Agent Chat] Agent API failed, falling back to search');
            return await fallbackToSearch(query, headers);
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                answer: data.answer || data.message,
                sources: data.sources || [],
                conversationId: data.conversationId
            })
        };

    } catch (error) {
        console.error('[Agent Chat] Error:', error);

        // Fall back to search on any error
        try {
            const { query } = JSON.parse(event.body);
            return await fallbackToSearch(query, headers);
        } catch (e) {
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ error: 'Internal server error' })
            };
        }
    }
};

/**
 * Fallback to Algolia Search when Agent API is unavailable
 */
async function fallbackToSearch(query, headers) {
    const searchUrl = `https://${ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/datalaria_posts/query`;

    const response = await fetch(searchUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Algolia-API-Key': ALGOLIA_SEARCH_KEY,
            'X-Algolia-Application-Id': ALGOLIA_APP_ID
        },
        body: JSON.stringify({
            query: query,
            hitsPerPage: 5,
            attributesToRetrieve: ['title', 'description', 'url', 'domain'],
            attributesToSnippet: ['content:80']
        })
    });

    const data = await response.json();

    if (data.hits && data.hits.length > 0) {
        // Build a natural response from search results
        const intro = 'Based on my knowledge base, here are relevant articles:';
        const articles = data.hits.map(h => ({
            title: h.title,
            url: h.url,
            snippet: h._snippetResult?.content?.value || h.description || ''
        }));

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                answer: intro,
                sources: articles,
                isSearchFallback: true
            })
        };
    }

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            answer: "I couldn't find relevant information. Try asking about S&OP, Autopilot, or data engineering.",
            sources: [],
            isSearchFallback: true
        })
    };
}
