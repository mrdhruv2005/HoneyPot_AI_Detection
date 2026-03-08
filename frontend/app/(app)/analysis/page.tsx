"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

export default function AnalysisPage() {
    return (
        <div className="flex flex-col gap-4 p-4">
            <h2 className="text-3xl font-bold tracking-tight glow-text">Risk Analysis</h2>
            <Card className="border-white/10 bg-card/50 backdrop-blur-sm">
                <CardHeader>
                    <CardTitle>Attack Vector Analysis</CardTitle>
                    <CardDescription>Breakdown of potential threats</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span>Phishing Probablity</span>
                                <span>88%</span>
                            </div>
                            <Progress value={88} className="bg-primary/20 [&>div]:bg-red-500" />
                        </div>
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span>Social Engineering</span>
                                <span>64%</span>
                            </div>
                            <Progress value={64} className="bg-primary/20 [&>div]:bg-orange-500" />
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
