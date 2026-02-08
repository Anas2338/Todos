// State management for traditional todo UI to maintain isolation from chat UI

import { useReducer, useEffect } from 'react';
import { Todo } from '@/types/todo';
import { todoSyncService } from '../services/api/todoSyncService';

// Define the traditional todo state interface
interface TraditionalTodoState {
  todos: Todo[];
  loading: boolean;
  error: string | null;
  filter: 'all' | 'active' | 'completed';
}

// Actions that can be performed on todos
type TodoAction =
  | { type: 'SET_TODOS'; payload: Todo[] }
  | { type: 'ADD_TODO'; payload: Todo }
  | { type: 'UPDATE_TODO'; payload: Todo }
  | { type: 'DELETE_TODO'; payload: string }
  | { type: 'TOGGLE_TODO'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_FILTER'; payload: 'all' | 'active' | 'completed' }
  | { type: 'CLEAR_ERROR' };

// Reducer function for traditional todo state
const todoReducer = (state: TraditionalTodoState, action: TodoAction): TraditionalTodoState => {
  switch (action.type) {
    case 'SET_TODOS':
      return { ...state, todos: action.payload, loading: false };
    case 'ADD_TODO':
      return { ...state, todos: [...state.todos, action.payload] };
    case 'UPDATE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id ? action.payload : todo
        ),
      };
    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload),
      };
    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
        ),
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    case 'SET_FILTER':
      return { ...state, filter: action.payload };
    default:
      return state;
  }
};

// Hook for traditional todo state management
export const useTraditionalTodoState = (userId: string) => {
  const [state, dispatch] = useReducer(todoReducer, {
    todos: [],
    loading: false,
    error: null,
    filter: 'all',
  });

  // Subscribe to sync changes when component mounts
  useEffect(() => {
    const unsubscribe = todoSyncService.subscribe((todos) => {
      // Update traditional UI todos when sync events occur
      dispatch({ type: 'SET_TODOS', payload: todos });
    });

    // Subscribe to change events to handle specific updates
    const unsubscribeChanges = todoSyncService.subscribeToChanges((event) => {
      switch (event.type) {
        case 'created':
          if (event.source !== 'traditional') {
            const todo = event.todo as Todo;
            dispatch({ type: 'ADD_TODO', payload: todo });
          }
          break;
        case 'updated':
          if (event.source !== 'traditional') {
            const todo = event.todo as Todo;
            dispatch({ type: 'UPDATE_TODO', payload: todo });
          }
          break;
        case 'deleted':
          if (event.source !== 'traditional') {
            const todoId = event.todo as string;
            dispatch({ type: 'DELETE_TODO', payload: todoId });
          }
          break;
      }
    });

    // Cleanup subscriptions on unmount
    return () => {
      unsubscribe();
      unsubscribeChanges();
    };
  }, []);

  // Function to add a new todo
  const addTodo = async (title: string, description?: string, dueDate?: Date, priority?: 'low' | 'medium' | 'high') => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const newTodo: Todo = {
        id: `todo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        title,
        description: description || '',
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date(),
        dueDate: dueDate || null,
        priority: priority || 'medium',
        userId,
      };

      dispatch({ type: 'ADD_TODO', payload: newTodo });

      // Sync this change to chat UI and other sources
      await todoSyncService.syncTodosToChat({ created: [newTodo] });

      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to add todo';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Function to update a todo
  const updateTodo = async (id: string, updates: Partial<Todo>) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const todoToUpdate = state.todos.find(todo => todo.id === id);
      if (!todoToUpdate) {
        throw new Error('Todo not found');
      }

      const updatedTodo: Todo = {
        ...todoToUpdate,
        ...updates,
        updatedAt: new Date(),
      };

      dispatch({ type: 'UPDATE_TODO', payload: updatedTodo });

      // Sync this change to chat UI and other sources
      await todoSyncService.syncTodosToChat({ updated: [updatedTodo] });

      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update todo';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Function to toggle todo completion
  const toggleTodo = async (id: string) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const todoToToggle = state.todos.find(todo => todo.id === id);
      if (!todoToToggle) {
        throw new Error('Todo not found');
      }

      const updatedTodo: Todo = {
        ...todoToToggle,
        completed: !todoToToggle.completed,
        updatedAt: new Date(),
      };

      dispatch({ type: 'UPDATE_TODO', payload: updatedTodo });

      // Sync this change to chat UI and other sources
      await todoSyncService.syncTodosToChat({ updated: [updatedTodo] });

      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to toggle todo';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Function to delete a todo
  const deleteTodo = async (id: string) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      dispatch({ type: 'DELETE_TODO', payload: id });

      // Sync this change to chat UI and other sources
      await todoSyncService.syncTodosToChat({ deleted: [id] });

      dispatch({ type: 'SET_LOADING', payload: false });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete todo';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Function to clear error
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  // Filter todos based on current filter
  const filteredTodos = state.todos.filter(todo => {
    if (state.filter === 'active') return !todo.completed;
    if (state.filter === 'completed') return todo.completed;
    return true; // 'all' filter
  });

  return {
    todos: filteredTodos,
    loading: state.loading,
    error: state.error,
    filter: state.filter,
    addTodo,
    updateTodo,
    toggleTodo,
    deleteTodo,
    setFilter: (filter: 'all' | 'active' | 'completed') => dispatch({ type: 'SET_FILTER', payload: filter }),
    clearError,
  };
};