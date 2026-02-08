# Agentic AI Todo Application

This is a full-stack todo application with AI-powered chatbot integration for natural language task management.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **AI Chatbot**: Natural language interface for managing tasks
- **Authentication**: Secure user authentication and authorization
- **Responsive Design**: Works on desktop and mobile devices

## AI Chatbot Feature

The application includes an AI-powered chatbot that allows users to manage their tasks through natural language commands. The chatbot is integrated using OpenAI ChatKit and communicates with a backend service to process natural language commands for:

- Adding tasks: "Add a task to buy groceries by Friday"
- Viewing tasks: "Show me my tasks for today"
- Updating tasks: "Change the deadline for task X to tomorrow"
- Deleting tasks: "Delete task X"
- Marking tasks complete/incomplete: "Mark task 'Buy milk' as complete"

The chatbot interface appears as a modal that can be accessed from the main dashboard, providing a seamless experience alongside the traditional task list interface.

## Tech Stack

- **Frontend**: Next.js, React, TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **AI Integration**: OpenAI ChatKit
- **Backend**: Node.js, Express (or other specified backend)

## Setup

1. Clone the repository
2. Install dependencies: `npm install` or `yarn install`
3. Set up environment variables (see `.env.example`)
4. Run the development server: `npm run dev` or `yarn dev`

## Contributing

Please see the contributing guidelines in the `.specify` folder.

## License

MIT