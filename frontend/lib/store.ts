import { create } from 'zustand'

export type Message = {
    id: string
    role: 'user' | 'agent' | 'scammer' | 'system'
    content: string
    timestamp: string
}

export type ExtractedIntelligence = {
    bankAccounts: string[]
    upiIds: string[]
    phishingLinks: string[]
    phoneNumbers: string[]
    suspiciousKeywords: string[]
}

interface ChatState {
    messages: Message[]
    riskScore: number
    isAnalyzing: boolean
    intelligence: ExtractedIntelligence

    addMessage: (message: Message) => void
    setRiskScore: (score: number) => void
    setIsAnalyzing: (isAnalyzing: boolean) => void
    updateIntelligence: (data: Partial<ExtractedIntelligence>) => void
    resetChat: () => void
}

export const useChatStore = create<ChatState>((set) => ({
    messages: [
        {
            id: '1',
            role: 'system',
            content: 'System initialized. Waiting for suspicious content...',
            timestamp: '2024-01-01T00:00:00.000Z'
        }
    ],
    riskScore: 0,
    isAnalyzing: false,
    intelligence: {
        bankAccounts: [],
        upiIds: [],
        phishingLinks: [],
        phoneNumbers: [],
        suspiciousKeywords: []
    },

    addMessage: (message) => set((state) => ({
        messages: [...state.messages, message]
    })),

    setRiskScore: (score) => set({ riskScore: score }),

    setIsAnalyzing: (isAnalyzing) => set({ isAnalyzing }),

    updateIntelligence: (data) => set((state) => ({
        intelligence: { ...state.intelligence, ...data }
    })),

    resetChat: () => set({
        messages: [],
        riskScore: 0,
        intelligence: {
            bankAccounts: [],
            upiIds: [],
            phishingLinks: [],
            phoneNumbers: [],
            suspiciousKeywords: []
        }
    })
}))
