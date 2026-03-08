"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function IntelligencePage() {
    return (
        <div className="flex flex-col gap-4 p-4">
            <h2 className="text-3xl font-bold tracking-tight glow-text">Intelligence Database</h2>
            <Card className="border-white/10 bg-card/50 backdrop-blur-sm">
                <CardHeader>
                    <CardTitle>Extracted Entities</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow className="hover:bg-white/5 border-white/10">
                                <TableHead>Type</TableHead>
                                <TableHead>Value</TableHead>
                                <TableHead>Confidence</TableHead>
                                <TableHead>Session</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow className="hover:bg-white/5 border-white/10">
                                <TableCell>UPI ID</TableCell>
                                <TableCell className="font-mono">scammer@okhdfcbank</TableCell>
                                <TableCell>99.8%</TableCell>
                                <TableCell>#1024</TableCell>
                            </TableRow>
                            <TableRow className="hover:bg-white/5 border-white/10">
                                <TableCell>Phone</TableCell>
                                <TableCell className="font-mono">+91 98765 43210</TableCell>
                                <TableCell>100%</TableCell>
                                <TableCell>#1024</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    )
}
