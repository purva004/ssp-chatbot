"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export function MarkdownRenderer({ content, className }: MarkdownRendererProps) {
  return (
    <div className={cn("whitespace-pre-wrap break-words", className)}>
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}