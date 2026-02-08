// Custom hook for managing MCP tool integration in ChatKit

import { useState, useCallback } from 'react';
import { Todo, TodoOperation } from '../types/todo';
import { chatService } from '../services/api/chatService';
import useToolStatus from './useToolStatus';

const useMCPIntegration = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Use the tool status hook to track MCP operations
  const { startToolCall, completeToolCall, failToolCall, updateToolStatus } = useToolStatus();

  const executeMCPTool = useCallback(async (operation: TodoOperation) => {
    setLoading(true);
    setError(null);

    try {
      // Create a unique tool call ID
      const toolCallId = `tool-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

      // Start tracking the tool call
      startToolCall(toolCallId, operation.operation);

      // Simulate MCP tool execution
      // In a real implementation, this would call the actual MCP tools
      const result = await simulateMCPCall(operation);

      // Update tool status to executing
      updateToolStatus(toolCallId, 'executing');

      // Process the result based on operation type
      const processedTodos = processOperationResult(operation, result.todosAffected);

      // Update local state with new todos
      setTodos(processedTodos);

      // Mark tool call as completed
      completeToolCall(toolCallId, result);

      return { success: true, todos: processedTodos, result };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'MCP tool execution failed';
      setError(errorMessage);

      // Mark tool call as failed
      failToolCall('last-tool-call', { error: errorMessage });

      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [startToolCall, updateToolStatus, completeToolCall, failToolCall]);

  const simulateMCPCall = async (operation: TodoOperation): Promise<{ todosAffected: Todo[] }> => {
    // This is a simulation - in real implementation, this would call the actual MCP tools
    // through the backend API

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // For demo purposes, return mock data
    const mockTodos: Todo[] = [
      {
        id: 'mock-todo-1',
        title: operation.data.title || 'Sample todo',
        description: operation.data.description || '',
        completed: operation.data.completed ?? false,
        createdAt: new Date(),
        updatedAt: new Date(),
        dueDate: operation.data.dueDate || null,
        priority: operation.data.priority || 'medium',
        userId: 'mock-user-id'
      }
    ];

    return { todosAffected: mockTodos };
  };

  const processOperationResult = (operation: TodoOperation, affectedTodos: Todo[]): Todo[] => {
    let updatedTodos = [...todos];

    switch (operation.operation) {
      case 'create':
        if (affectedTodos.length > 0) {
          updatedTodos = [...updatedTodos, ...affectedTodos];
        }
        break;

      case 'update':
        if (operation.todoId) {
          updatedTodos = updatedTodos.map(todo =>
            todo.id === operation.todoId ? { ...todo, ...operation.data } : todo
          );
        }
        break;

      case 'delete':
        if (operation.todoId) {
          updatedTodos = updatedTodos.filter(todo => todo.id !== operation.todoId);
        }
        break;

      case 'toggleComplete':
        if (operation.todoId) {
          updatedTodos = updatedTodos.map(todo =>
            todo.id === operation.todoId ? { ...todo, completed: !todo.completed } : todo
          );
        }
        break;
    }

    return updatedTodos;
  };

  const createTodo = useCallback(async (title: string, description?: string, dueDate?: Date, priority?: 'low' | 'medium' | 'high') => {
    const operation: TodoOperation = {
      operation: 'create',
      data: {
        title,
        description,
        dueDate,
        priority: priority || 'medium'
      }
    };

    return executeMCPTool(operation);
  }, [executeMCPTool]);

  const updateTodo = useCallback(async (todoId: string, updates: Partial<Todo>) => {
    const operation: TodoOperation = {
      operation: 'update',
      todoId,
      data: {
        title: updates.title,
        description: updates.description,
        completed: updates.completed,
        dueDate: updates.dueDate,
        priority: updates.priority
      }
    };

    return executeMCPTool(operation);
  }, [executeMCPTool]);

  const deleteTodo = useCallback(async (todoId: string) => {
    const operation: TodoOperation = {
      operation: 'delete',
      todoId,
      data: {}
    };

    return executeMCPTool(operation);
  }, [executeMCPTool]);

  const toggleTodoComplete = useCallback(async (todoId: string) => {
    const operation: TodoOperation = {
      operation: 'toggleComplete',
      todoId,
      data: {}
    };

    return executeMCPTool(operation);
  }, [executeMCPTool]);

  const fetchTodos = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // In a real implementation, this would fetch todos from the backend
      // For now, we'll just return the local state
      return { success: true, todos };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch todos';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [todos]);

  return {
    todos,
    loading,
    error,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodoComplete,
    fetchTodos,
    executeMCPTool,
  };
};

export default useMCPIntegration;