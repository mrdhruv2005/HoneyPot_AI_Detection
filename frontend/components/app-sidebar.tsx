"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import {
  ShieldAlert,
  MessageSquare,
  LayoutDashboard,
  Settings,
  Database,
  ChevronsUpDown,
  LogOut,
  Plus
} from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
} from "@/components/ui/sidebar"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  // No handlers needed for guest mode

  return (
    <Sidebar collapsible="icon" {...props} className="border-r border-white/10 bg-sidebar">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="/">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <ShieldAlert className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Agentic Honey-pot system</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu>
          <div className="px-3 py-2 text-xs font-medium text-muted-foreground">Platform</div>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip="Dashboard">
              <a href="/dashboard">
                <LayoutDashboard />
                <span>Dashboard</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip="Chat">
              <a href="/chat">
                <MessageSquare />
                <span>Chat</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>

        </SidebarMenu>
        <SidebarSeparator className="mx-2 my-2 bg-white/5" />
        <SidebarMenu>
          <div className="px-3 py-2 text-xs font-medium text-muted-foreground">Configuration</div>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip="Settings">
              <a href="/settings">
                <Settings />
                <span>Settings</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarContent>
      <SidebarRail />
    </Sidebar >
  )
}
