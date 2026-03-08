"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function SettingsPage() {
    return (
        <div className="flex flex-col gap-4 p-4">
            <h2 className="text-3xl font-bold tracking-tight glow-text">System Configuration</h2>
            <Card className="border-white/10 bg-card/50 backdrop-blur-sm">
                <CardHeader>
                    <CardTitle>Agent Persona</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground text-sm mb-4">Configure how the autonomous agent behaves during engagement.</p>
                    <Button variant="outline">Edit Persona Prompts <span className="ml-2 text-xs text-muted-foreground">(ongoing)</span></Button>
                </CardContent>
            </Card>
        </div>
    )
}
