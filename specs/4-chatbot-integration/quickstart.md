# Quickstart: Chatbot Frontend Integration

## Development Setup

### Prerequisites
- Node.js 18.x or higher
- pnpm package manager (preferred) or npm/yarn
- Access to Phase III backend chat endpoint
- Existing Todo application frontend codebase

### Installation
1. Clone the repository and navigate to the frontend directory:
```bash
cd fullstack-todo/frontend
```

2. Install dependencies:
```bash
pnpm install
# or
npm install
```

3. Copy the environment template and configure your backend API endpoint:
```bash
cp .env.example .env.local
```
Then update the `NEXT_PUBLIC_CHAT_API_URL` variable to point to your Phase III backend chat endpoint.

### Running the Development Server
```bash
npm run dev
# or
pnpm dev
```

The application will be available at `http://localhost:3000`

## Key Components

### Chat Components Structure
```
src/
├── components/
│   └── chatbot/
│       ├── ChatModal.tsx          # Main modal container
│       ├── ChatInterface.tsx      # Chat UI container
│       ├── MessageList.tsx        # Displays chat messages
│       └── MessageInput.tsx       # Input field for user messages
├── hooks/
│   └── useChatBot.ts             # Chat state and API interactions
├── services/
│   └── chatApi.ts                # API client for chat backend
└── types/
    └── chat.ts                   # Type definitions
```

## Integration Points

### Adding Chat to Existing Pages
To add chat functionality to any page, wrap your component with the ChatProvider and use the ChatModal component:

```tsx
import { ChatProvider } from '@/providers/ChatProvider';
import { ChatModal } from '@/components/chatbot/ChatModal';

export default function MyPage() {
  return (
    <ChatProvider>
      <div className="page-content">
        {/* Your existing page content */}
      </div>
      <ChatModal />
    </ChatProvider>
  );
}
```

### Authentication Integration
The chat interface respects the existing Better Auth authentication. Make sure to protect routes using the existing authentication patterns:

```tsx
import { useAuth } from '@/hooks/useAuth';

export default function ProtectedPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>Please sign in to access chat</div>;

  return (
    <ChatProvider>
      {/* Your protected content */}
      <ChatModal />
    </ChatProvider>
  );
}
```

## API Service Usage

The chat API service handles communication with the backend:

```ts
import { sendChatMessage, getConversationHistory } from '@/services/chatApi';

// Send a message
const response = await sendChatMessage({
  message: "Add a task to buy groceries",
  conversationId: currentConversationId
});

// Get conversation history
const conversation = await getConversationHistory(conversationId);
```

## Environment Variables
- `NEXT_PUBLIC_CHAT_API_URL` - Base URL for the chat backend API
- `NEXT_PUBLIC_AUTH_ENABLED` - Toggle for authentication checks (defaults to true)