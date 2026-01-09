# Todo Application with Tailwind CSS 4.1

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) and integrated with Tailwind CSS 4.1.

## Features

- **Next.js 16+** with App Router
- **Tailwind CSS 4.1** for styling with modern CSS features
- **TypeScript** for type safety
- **Responsive design** with mobile-first approach
- **Authentication** with login and registration
- **Task management** with CRUD operations
- **Modern component architecture** with reusable UI components

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn install
```

Next, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Tailwind CSS 4.1 Configuration

This project uses Tailwind CSS 4.1 with the new CSS-first configuration model. The configuration is split between:

- `src/app/globals.css` - Main CSS file that imports Tailwind
- `src/app/theme.css` - Theme configuration using the `@theme` directive
- `tailwind.config.ts` - Traditional Tailwind configuration (kept for compatibility)

### Key Changes in Tailwind CSS 4.1

- **CSS-first configuration**: Customization now happens directly in CSS using the `@theme` directive
- **Improved performance**: Up to 5x faster build times and 100x faster incremental builds
- **Modern color system**: Uses OKLCH color format for better perceptual uniformity
- **Enhanced container queries**: First-class support for container queries
- **Native CSS features**: Leverages modern CSS features like `color-mix()`, `@property`, and cascade layers

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── (auth)/          # Authentication pages (login, register)
│   │   ├── dashboard/       # Protected task dashboard
│   │   ├── tasks/           # Task management pages
│   │   │   ├── [id]/        # Individual task details
│   │   │   └── new/         # Create new task
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   └── globals.css      # Global styles with Tailwind import
│   ├── components/          # Reusable UI components
│   │   ├── auth/            # Authentication-specific components
│   │   ├── common/          # Common UI components
│   │   ├── providers/       # Context providers
│   │   ├── tasks/           # Task management components
│   │   └── ui/              # Base UI components
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility functions and API client
│   ├── types/               # TypeScript type definitions
│   └── tests/               # Frontend tests
├── docs/                    # Documentation
├── public/                  # Static assets
├── .env.example             # Environment variables example
├── next.config.js           # Next.js configuration
├── postcss.config.js        # PostCSS configuration with Tailwind
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies and scripts
```

## Environment Variables

Create a `.env.local` file in the frontend directory with the following:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Available Scripts

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm run start` - Start production server
- `npm run lint` - Run linting checks

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs) - Learn about Next.js features and API
- [Tailwind CSS 4.1 Documentation](https://tailwindcss.com/docs) - Learn about Tailwind CSS features
- [TypeScript Documentation](https://www.typescriptlang.org/docs/) - Learn about TypeScript
- [React Documentation](https://react.dev/learn/tutorial-tic-tac-toe) - Learn about React

## Deployment

The application can be deployed to platforms like Vercel, Netlify, or any Node.js hosting service. For detailed deployment instructions, refer to the [Next.js deployment documentation](https://nextjs.org/docs/deployment).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.