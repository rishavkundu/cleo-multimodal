import React from 'react'

import { cn } from '@/lib/utils'
import { ExternalLink } from '@/components/external-link'

export function FooterText({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p
      className={cn(
        'px-2 text-center text-xs leading-normal text-muted-foreground',
        className
      )}
      {...props}
    >
      Leon Assistant built with{' '}
      <ExternalLink href="https://anthropic.com">Anthropic</ExternalLink> by{' '}
      <ExternalLink href="https://rishavkundu.com">
        Rishav Kundu
      </ExternalLink>
      .
    </p>
  )
}
