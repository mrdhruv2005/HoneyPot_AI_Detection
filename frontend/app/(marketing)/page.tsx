import Link from "next/link"
import { ShieldAlert, ArrowRight, Lock, Laptop } from "lucide-react"

export default function LandingPage() {
    return (
        <div className="flex min-h-screen flex-col">
            <header className="px-6 h-16 flex items-center border-b border-white/10 backdrop-blur-md sticky top-0 z-50">
                <div className="flex items-center gap-2 font-bold text-xl tracking-tighter">
                    <ShieldAlert className="size-6 text-primary" />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-white/60">CyberGuard</span>
                </div>
                <nav className="ml-auto flex gap-6 text-sm font-medium items-center">
                    <Link
                        href="/dashboard"
                        className="bg-primary/20 hover:bg-primary/30 text-primary border border-primary/50 px-4 py-2 rounded-md text-sm transition-all shadow-[0_0_15px_-5px_var(--color-primary)] inline-flex items-center justify-center"
                    >
                        Launch Dashboard
                    </Link>
                </nav>
            </header>

            <main className="flex-1">
                <section className="relative pt-32 pb-40 overflow-hidden">
                    <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-primary/10 via-background to-background pointer-events-none"></div>
                    <div className="container mx-auto px-6 relative z-10 text-center">
                        <div className="inline-flex items-center gap-2 rounded-full border border-white/5 bg-white/5 px-3 py-1 text-sm text-muted-foreground backdrop-blur-3xl mb-8">
                            <span className="flex size-2 rounded-full bg-emerald-500"></span>
                            System Online &bull; v2.0.4
                        </div>

                        <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-8 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/40">
                            Autonomous Scam <br />
                            <span className="text-primary glow-text">Intelligence</span>
                        </h1>

                        <p className="max-w-2xl mx-auto text-muted-foreground text-xl mb-12 leading-relaxed">
                            Deploy autonomous AI agents to engage scammers, waste their time, and extract actionable intelligence—bank accounts, UPI IDs, and phishing links.
                        </p>

                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                            <Link
                                href="/dashboard"
                                className="h-12 px-8 rounded-lg bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-all shadow-[0_0_20px_-5px_var(--color-primary)] flex items-center gap-2"
                            >
                                Get Started <ArrowRight className="size-4" />
                            </Link>
                        </div>
                    </div>

                    {/* Decorative Grid */}
                    <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] pointer-events-none opacity-20"></div>
                </section>

                <section className="py-24 border-t border-white/5 bg-black/20">
                    <div className="container mx-auto px-6">
                        <div className="grid md:grid-cols-3 gap-8">
                            {[
                                { icon: ShieldAlert, title: "Autonomous Engagement", desc: "AI personas that maintain believable, multi-turn conversations with scammers." },
                                { icon: Lock, title: "Zero-Risk Isolation", desc: "All interactions happen in a sandboxed environment. Your personal data is never exposed." },
                                { icon: Laptop, title: "Structured Intelligence", desc: "Automatically extracts and verifies bank details, UPI IDs, and URLs for reporting." },
                            ].map((item, i) => (
                                <div key={i} className="p-8 rounded-2xl border border-white/5 bg-white/5 hover:bg-white/10 transition-colors backdrop-blur-sm group">
                                    <div className="size-12 rounded-xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                        <item.icon className="size-6 text-primary" />
                                    </div>
                                    <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                                    <p className="text-muted-foreground leading-relaxed">{item.desc}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            </main>

            <footer className="py-8 border-t border-white/5 text-center text-sm text-muted-foreground">
                © 2026 CyberGuard. All rights reserved. Built for security professionals.
            </footer>
        </div>
    )
}
