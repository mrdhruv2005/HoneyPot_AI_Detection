"use client"

import { useState, useRef, useEffect } from "react"
import { useChatStore } from "@/lib/store"
import { Send, Shield, Database } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function ChatPage() {
    const { messages, addMessage, riskScore, setRiskScore, intelligence, updateIntelligence } = useChatStore()
    const [input, setInput] = useState("")
    const scrollRef = useRef<HTMLDivElement>(null)

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight
        }
    }, [messages])

    // Fetch History on Mount
    useEffect(() => {
        const fetchHistory = async () => {
            // Logic to persist session ID across reloads (e.g. from URL or LocalStorage)
            // For now, we regenerate session daily, so we try to fetch that.
            // Ideally, the user should be able to select sessions from a list.
            // Using a static session ID for simpler testing of persistence for now:
            const sessionId = "live-session-" + new Date().getDate();

            const { getHistory } = await import("@/lib/api");
            const data = await getHistory(sessionId);

            if (data && data.history) {
                // Convert backend history format to frontend message format if needed
                // Backend: {sender: 'user'|'scammer', text: '...', timestamp: '...'}
                // Frontend: {id: '...', role: 'agent'|'scammer', content: '...', timestamp: '...'}

                const loadedMessages = data.history.map((msg: any) => ({
                    id: crypto.randomUUID(),
                    role: msg.sender === 'user' ? 'agent' : 'scammer', // Map 'user' backend -> 'agent' frontend role
                    content: msg.text,
                    timestamp: msg.timestamp
                }));

                // Avoid duplicates if store already has them (simple check)
                if (messages.length === 0 && loadedMessages.length > 0) {
                    loadedMessages.forEach((m: any) => addMessage(m));
                }

                if (data.intelligence) {
                    updateIntelligence(data.intelligence);
                }
            }
        }
        fetchHistory()
    }, [])

    const handleSend = async () => {
        if (!input.trim()) return

        // 1. User Message
        const timestamp = new Date().toISOString()
        const newMessage = {
            id: crypto.randomUUID(),
            role: 'scammer' as const,
            content: input,
            timestamp
        }

        addMessage(newMessage)
        setInput("")

        // 2. Set Analyzing State
        // TODO: Add isAnalyzing to store to show typing indicator

        // 3. Call Backend
        try {
            // Import dynamically
            const { streamMessage } = await import("@/lib/api");

            // Create placeholder for agent message
            const agentMsgId = crypto.randomUUID()
            const agentMsg = {
                id: agentMsgId,
                role: 'agent' as const,
                content: "", // Start empty
                timestamp: new Date().toISOString()
            }
            addMessage(agentMsg)

            // Stream chunks
            await streamMessage(
                {
                    sessionId: "live-session-" + new Date().getDate(),
                    message: {
                        sender: "scammer",
                        text: newMessage.content,
                        timestamp: newMessage.timestamp
                    },
                    conversationHistory: messages
                        .filter(m => m.role !== 'system' && m.id !== agentMsgId) // Don't send the empty placeholder back
                        .map(m => ({
                            sender: m.role === 'agent' ? 'user' : 'scammer',
                            text: m.content,
                            timestamp: m.timestamp
                        })),
                    metadata: { channel: "SMS", language: "en-US", locale: "IN" }
                },
                (token) => {
                    // Update the last message (which is our placeholder) with new content
                    useChatStore.setState(state => ({
                        messages: state.messages.map(m =>
                            m.id === agentMsgId ? { ...m, content: m.content + token } : m
                        )
                    }))
                },
                (metadata) => {
                    // Update store with metadata
                    setRiskScore(metadata.riskScore)
                    if (metadata.extractedIntelligence) {
                        updateIntelligence(metadata.extractedIntelligence)
                    }
                },
                () => {
                    console.log("Stream Complete")
                },
                () => {
                    // Error Fallback
                    const errorMsg = {
                        id: crypto.randomUUID(),
                        role: 'system' as const,
                        content: "Error connecting to Intelligence Core. Using offline protocols.",
                        timestamp: new Date().toISOString()
                    }
                    addMessage(errorMsg)
                }
            )

        } catch (error) {
            console.error("Backend Error:", error)
        }
    }

    // Removed simulateAIResponse


    return (
        <div className="flex h-[calc(100vh-2rem)] gap-4">
            {/* Left: Chat Area */}
            <Card className="flex-1 flex flex-col border-white/10 bg-card/50 backdrop-blur-sm">
                <CardHeader className="py-4 border-b border-white/5">
                    <CardTitle className="flex items-center gap-2 text-lg">
                        <Shield className="size-5 text-primary" /> Active Engagement Session
                    </CardTitle>
                    <CardDescription>Live interaction with conversation simulator</CardDescription>
                </CardHeader>

                <div className="flex-1 p-0 overflow-hidden relative">
                    <div ref={scrollRef} className="h-full overflow-y-auto p-4 space-y-4">
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={`flex ${msg.role === 'scammer' ? 'justify-end' :
                                    msg.role === 'system' ? 'justify-center' : 'justify-start'
                                    }`}
                            >
                                <div
                                    className={`max-w-[80%] rounded-xl px-4 py-3 text-sm ${msg.role === 'scammer'
                                        ? 'bg-primary text-primary-foreground rounded-br-none'
                                        : msg.role === 'system'
                                            ? 'bg-muted/50 text-muted-foreground text-xs py-1'
                                            : 'bg-muted/30 border border-white/5 rounded-bl-none'
                                        }`}
                                >
                                    {msg.role !== 'system' && (
                                        <div className="text-[10px] opacity-50 mb-1 uppercase tracking-wider font-bold">
                                            {msg.role === 'scammer' ? 'Me' : 'User'}
                                        </div>
                                    )}
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="p-4 border-t border-white/5 bg-background/20">
                    <div className="flex gap-2">
                        <Input
                            placeholder="Paste suspicious message or type response..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            className="border-white/10 bg-black/20 focus-visible:ring-primary"
                        />
                        <Button onClick={handleSend} size="icon" className="bg-primary hover:bg-primary/90">
                            <Send className="size-4" />
                        </Button>
                    </div>
                </div>
            </Card>

            {/* Right: Intelligence Panel */}
            <div className="w-80 flex flex-col gap-4">
                {/* Risk Score Card */}
                <Card className="border-white/10 bg-card/50 backdrop-blur-sm">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Risk Probability</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-end justify-between mb-2">
                            <span className="text-4xl font-bold text-white">{riskScore}%</span>
                            <span className={`text-sm font-medium ${riskScore > 40 ? 'text-destructive' : 'text-emerald-500'}`}>
                                {riskScore > 40 ? 'CRITICAL' : 'SAFE'}
                            </span>
                        </div>
                        <Progress value={riskScore} className={`h-2 ${riskScore > 40 ? 'bg-destructive/20 [&>div]:bg-destructive' : 'bg-primary/20'}`} />
                    </CardContent>
                </Card>

                {/* Extracted Intel Tabs */}
                <Card className="flex-1 border-white/10 bg-card/50 backdrop-blur-sm flex flex-col">
                    <Tabs defaultValue="entities" className="flex-1 w-full flex flex-col">
                        <div className="px-4 pt-4">
                            <TabsList className="w-full bg-black/20">
                                <TabsTrigger value="entities" className="flex-1">Entities</TabsTrigger>
                                <TabsTrigger value="metadata" className="flex-1">Metadata</TabsTrigger>
                            </TabsList>
                        </div>

                        <TabsContent value="entities" className="flex-1 p-4 space-y-4">
                            <div className="space-y-3">
                                <h4 className="text-xs font-semibold text-muted-foreground uppercase flex items-center gap-2">
                                    <Database className="size-3" /> Extracted Intelligence
                                </h4>

                                {intelligence.bankAccounts.length === 0 && intelligence.upiIds.length === 0 && intelligence.suspiciousKeywords.length === 0 && (
                                    <div className="text-sm text-muted-foreground italic text-center py-6">
                                        No entities extracted yet.
                                    </div>
                                )}

                                {intelligence.suspiciousKeywords.length > 0 && (
                                    <div className="space-y-2">
                                        <span className="text-xs text-muted-foreground">Keywords</span>
                                        <div className="flex flex-wrap gap-2">
                                            {intelligence.suspiciousKeywords.map((k, i) => (
                                                <Badge key={i} variant="outline" className="border-primary/50 bg-primary/10 text-primary-foreground">{k}</Badge>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {intelligence.upiIds.length > 0 && (
                                    <div className="space-y-2">
                                        <span className="text-xs text-muted-foreground">UPI IDs</span>
                                        <div className="space-y-1">
                                            {intelligence.upiIds.map((k, i) => (
                                                <div key={i} className="text-sm bg-black/20 p-2 rounded border border-white/5">{k}</div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </TabsContent>

                        <TabsContent value="metadata" className="p-4">
                            <div className="space-y-2 text-sm text-muted-foreground">
                                <div className="flex justify-between">
                                    <span>Protocol</span>
                                    <span className="text-foreground">SMS</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Region</span>
                                    <span className="text-foreground">IN (India)</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Language</span>
                                    <span className="text-foreground">en-US</span>
                                </div>
                            </div>
                        </TabsContent>
                    </Tabs>
                </Card>
            </div>
        </div>
    )
}
