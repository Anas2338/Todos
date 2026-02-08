// Type definitions for todo-related entities

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date | null;
  priority: 'low' | 'medium' | 'high';
  userId: string;
}

export interface TodoState {
  todos: Todo[];
  loading: boolean;
  error: string | null;
}

export interface TodoOperation {
  operation: 'create' | 'update' | 'delete' | 'toggleComplete';
  todoId?: string;
  data: {
    title?: string;
    description?: string;
    completed?: boolean;
    dueDate?: Date | null;
    priority?: 'low' | 'medium' | 'high';
  };
}