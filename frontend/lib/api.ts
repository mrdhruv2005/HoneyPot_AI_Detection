import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor for API keys/Auth tokens
// Interceptor for API keys/Auth tokens
api.interceptors.request.use((config) => {
    // No auth token needed for public access
    return config;
});

// Define types based on backend schemas
export interface ConversationItem {
    sender: string;
    text: string;
    timestamp: string;
}

export interface ProcessRequest {
    sessionId: string;
    message: {
        sender: string;
        text: string;
        timestamp: string;
    };
    conversationHistory: ConversationItem[];
    metadata?: {
        channel: string;
        language: string;
        locale: string;
    };
}

export const processMessage = async (payload: ProcessRequest) => {
    // Hardcoded API Key for Demo (In production, use secure proxy or user key)
    const config = {
        headers: {
            'X-API-Key': 'secret-key'
        }
    };
    const response = await api.post('/api/v1/process', payload, config);
    return response.data;
}

export const streamMessage = async (
    payload: any,
    onToken: (token: string) => void,
    onMetadata: (metadata: any) => void,
    onComplete: () => void,
    onError: () => void
) => {
    // We cannot use Axios for SSE easily, using fetch-event-source or native EventSource is harder for POST.
    // However, fetch-event-source library is best.
    // For simplicity without new deps, we'll use native fetch and read the body reader.

    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/v1/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Stream failed");

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        if (!reader) throw new Error("No reader");

        // SSE Parser (simplified)
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            console.log("RAW STREAM CHUNK:", chunk); // DEBUG
            buffer += chunk;

            // Safer splitting for double newlines (standard SSE), handling various newline formats
            const parts = buffer.split(/\r\n\r\n|\n\n/);
            buffer = parts.pop() || ''; // Keep partial last chunk

            for (const part of parts) {
                const lines = part.split(/\r\n|\n/);
                let eventType = null;
                let data = '';

                for (const line of lines) {
                    if (line.startsWith('event: ')) {
                        eventType = line.substring(7).trim();
                    } else if (line.startsWith('data: ')) {
                        // Append data, handling multi-line data if necessary
                        // IMPORTANT: Do NOT trim the data content, as it removes spaces from tokens like " beta"
                        const content = line.substring(6);
                        data += (data ? '\n' : '') + content;
                    }
                }

                // Debug log to confirm parsing success
                console.log("Parsed SSE Event:", eventType, data);

                if (eventType === 'token') {
                    onToken(data);
                } else if (eventType === 'metadata') {
                    try {
                        onMetadata(JSON.parse(data));
                    } catch (e) {
                        console.error("Metadata parse error", e);
                    }
                } else if (eventType === 'end') {
                    onComplete();
                    return;
                }
            }
        }
    } catch (e) {
        console.error("Stream Error", e);
        onError();
    }
}

export const getDashboardStats = async () => {
    try {
        const response = await api.get('/api/v1/stats');
        return response.data;
    } catch (error) {
        console.error("Failed to fetch dashboard stats", error);
        return null;
    }
}

export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch (error) {
        console.error("Health check failed", error);
        return { status: "offline" };
    }
}

export const getHistory = async (sessionId: string) => {
    try {
        const response = await api.get(`/api/v1/history?sessionId=${sessionId}`);
        return response.data;
    } catch (error) {
        console.error("Failed to fetch history", error);
        return null;
    }
}

export default api;
