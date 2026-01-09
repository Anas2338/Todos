# Quickstart Guide: Frontend Todo Application

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (assumed to be running on localhost:3000 or specified endpoint)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Set up environment variables**
   Create a `.env.local` file in the frontend directory with the following:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:3000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   ```

5. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

6. **Open the application**
   Visit `http://localhost:3001` (or your configured port) in your browser

## Development Commands

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm run start` - Start production server
- `npm run lint` - Run linting checks
- `npm run test` - Run unit and integration tests
- `npm run test:e2e` - Run end-to-end tests

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
│   │   └── page.tsx         # Home page
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utility functions and API client
│   ├── types/               # TypeScript type definitions
│   └── styles/              # Global styles
├── public/                  # Static assets
└── tests/                   # Frontend tests
```

## Key Features

1. **Authentication**: User registration and login with Better Auth
2. **Task Management**: Create, read, update, delete, and mark tasks as complete
3. **Responsive Design**: Works on desktop and mobile devices
4. **Error Handling**: Proper error states and user feedback
5. **Loading States**: Appropriate loading indicators during API calls

## API Integration

The frontend integrates with the backend API at the following endpoints:
- GET `/api/{user_id}/tasks` - Get all tasks for user
- POST `/api/{user_id}/tasks` - Create new task
- GET `/api/{user_id}/tasks/{id}` - Get specific task
- PUT `/api/{user_id}/tasks/{id}` - Update task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Update task completion status

## Testing

The application includes:
- Unit tests for individual components
- Integration tests for API interactions
- End-to-end tests for user flows

Run all tests with:
```bash
npm run test
```

## Environment Configuration

The application uses the following environment variables:

**Required:**
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Base URL for Better Auth

**Optional:**
- `NEXT_PUBLIC_APP_NAME` - Application name for display
- `NEXT_PUBLIC_DEFAULT_PAGE_SIZE` - Default number of tasks to load per page