"use client"
import { Area, AreaChart, CartesianGrid, XAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export interface DashboardChartsProps {
    activityData: any[]; // Using any to match recharts flexibility, or define strict type
    extractionData: any[];
}

export function DashboardCharts({ activityData, extractionData }: DashboardChartsProps) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                <CardHeader>
                    <CardTitle>Real-time Detection Volume</CardTitle>
                    <CardDescription>24-hour analysis trend</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={activityData} accessibilityLayer>
                                <defs>
                                    <linearGradient id="colorScams" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="time" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: 'var(--color-card)', borderColor: 'rgba(255,255,255,0.1)', color: 'white' }}
                                />
                                <Area type="monotone" dataKey="scams" stroke="var(--color-primary)" fillOpacity={1} fill="url(#colorScams)" />
                                <Area type="monotone" dataKey="safe" stroke="var(--color-secondary-foreground)" fillOpacity={0.1} fill="var(--color-secondary)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>

            <Card className="bg-card/50 backdrop-blur-sm border-white/5">
                <CardHeader>
                    <CardTitle>Intelligence Extraction</CardTitle>
                    <CardDescription>Entities harvested by autonomous agents</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={extractionData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                                <XAxis type="number" stroke="rgba(255,255,255,0.3)" fontSize={12} />
                                <Tooltip
                                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                    contentStyle={{ backgroundColor: 'var(--color-card)', borderColor: 'rgba(255,255,255,0.1)', color: 'white' }}
                                />
                                <Bar dataKey="value" fill="var(--color-accent)" radius={[0, 4, 4, 0]} barSize={32} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
