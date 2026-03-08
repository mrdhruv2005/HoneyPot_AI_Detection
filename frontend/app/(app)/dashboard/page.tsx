
"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Shield, MessageSquare, Database, Activity, Loader2 } from "lucide-react"
import { DashboardCharts } from "@/components/dashboard-charts"
import { getDashboardStats } from "@/lib/api"
import { Skeleton } from "@/components/ui/skeleton"

export default function DashboardPage() {
    const [isLoading, setIsLoading] = useState(true)
    const [stats, setStats] = useState({
        totalMessages: 0,
        scamsDetected: 0,
        bankAccountsExtracted: 0,
        upiIdsExtracted: 0,
        phishingLinksExtracted: 0,
        phoneNumbersExtracted: 0,
        activityData: [] as any[],
        extractionData: [] as any[],
        recentActivity: [] as any[]
    })

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const data = await getDashboardStats()
                if (data) {
                    const extractionData = [
                        { name: "Bank Accts", value: data.bankAccountsExtracted || 0 },
                        { name: "UPI IDs", value: data.upiIdsExtracted || 0 },
                        { name: "URLs", value: data.phishingLinksExtracted || 0 },
                        { name: "Phones", value: data.phoneNumbersExtracted || 0 },
                    ]

                    setStats({
                        totalMessages: data.totalMessages || 0,
                        scamsDetected: data.scamsDetected || 0,
                        bankAccountsExtracted: data.bankAccountsExtracted || 0,
                        upiIdsExtracted: data.upiIdsExtracted || 0,
                        phishingLinksExtracted: data.phishingLinksExtracted || 0,
                        phoneNumbersExtracted: data.phoneNumbersExtracted || 0,
                        activityData: data.activityData || [],
                        extractionData,
                        recentActivity: data.recentActivity || []
                    })
                }
            } catch (error) {
                console.error("Fetch stats failed", error)
            } finally {
                setIsLoading(false)
            }
        }

        fetchStats()
        // Poll every 5 seconds for live updates
        const interval = setInterval(fetchStats, 5000)
        return () => clearInterval(interval)
    }, [])

    const detectionRate = stats.totalMessages > 0
        ? ((stats.scamsDetected / stats.totalMessages) * 100).toFixed(1)
        : "0.0"

    // Loading Skeleton View
    if (isLoading) {
        return (
            <div className="flex flex-col gap-4 p-4">
                <div className="flex items-center gap-2">
                    <Skeleton className="h-8 w-48 bg-white/10" />
                    <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {[...Array(6)].map((_, i) => (
                        <Card key={i} className="bg-card/50 backdrop-blur-sm border-white/5">
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <Skeleton className="h-4 w-24 bg-white/10" />
                                <Skeleton className="h-4 w-4 rounded-full bg-white/10" />
                            </CardHeader>
                            <CardContent>
                                <Skeleton className="h-8 w-16 mb-2 bg-white/10" />
                                <Skeleton className="h-3 w-32 bg-white/10" />
                            </CardContent>
                        </Card>
                    ))}
                </div>

                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                    <Skeleton className="col-span-4 h-[350px] bg-white/5 rounded-xl" />
                    <Skeleton className="col-span-3 h-[350px] bg-white/5 rounded-xl" />
                </div>
            </div>
        )
    }

    return (
        <div className="flex flex-col gap-4 p-4 animate-in fade-in duration-500">
            <h2 className="text-3xl font-bold tracking-tight glow-text">Command Center</h2>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Messages</CardTitle>
                        <MessageSquare className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats.totalMessages}</div>
                        <p className="text-xs text-muted-foreground">
                            Processed in real-time
                        </p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Scams Detected</CardTitle>
                        <Shield className="h-4 w-4 text-destructive" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-destructive">{stats.scamsDetected}</div>
                        <p className="text-xs text-muted-foreground">
                            {detectionRate}% threat detection rate
                        </p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Bank Accounts</CardTitle>
                        <Database className="h-4 w-4 text-emerald-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-emerald-500">{stats.bankAccountsExtracted}</div>
                        <p className="text-xs text-muted-foreground">
                            Accounts extracted
                        </p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">UPI IDs</CardTitle>
                        <Database className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-blue-500">{stats.upiIdsExtracted}</div>
                        <p className="text-xs text-muted-foreground">
                            UPI IDs extracted
                        </p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Phishing Links</CardTitle>
                        <Database className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-orange-500">{stats.phishingLinksExtracted}</div>
                        <p className="text-xs text-muted-foreground">
                            Malicious URLs found
                        </p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Phone Numbers</CardTitle>
                        <Database className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-purple-500">{stats.phoneNumbersExtracted}</div>
                        <p className="text-xs text-muted-foreground">
                            Phone numbers extracted
                        </p>
                    </CardContent>
                </Card>
            </div>

            <DashboardCharts activityData={stats.activityData} extractionData={stats.extractionData} />

            {/* Recent Activity Table Stub */}
            <Card className="flex-1 bg-card/50 backdrop-blur-sm border-white/5">
                <CardHeader>
                    <CardTitle>Recent Intelligent Agents</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {stats.recentActivity && stats.recentActivity.length > 0 ? (
                            stats.recentActivity.map((activity: any, i: number) => (
                                <div key={i} className="flex items-center justify-between border-b border-white/5 pb-2 last:border-0">
                                    <div className="flex items-center gap-4">
                                        <div className="size-8 rounded-full bg-primary/20 flex items-center justify-center text-xs font-bold text-primary">
                                            A{i + 1}
                                        </div>
                                        <div>
                                            <div className="font-medium text-sm truncate max-w-[200px]" title={activity.snippet}>
                                                {activity.snippet}
                                            </div>
                                            <div className="text-xs text-muted-foreground">
                                                Session #{activity.sessionId.slice(-4)}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <div className={`px-2 py-0.5 rounded text-[10px] border font-mono ${activity.status === 'SCAM'
                                            ? 'bg-destructive/20 text-destructive border-destructive/20'
                                            : 'bg-emerald-500/20 text-emerald-500 border-emerald-500/20'
                                            }`}>
                                            {activity.status}
                                        </div>
                                        <div className="text-xs text-muted-foreground">
                                            {new Date(activity.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="text-center text-sm text-muted-foreground py-4">
                                No recent activity
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

