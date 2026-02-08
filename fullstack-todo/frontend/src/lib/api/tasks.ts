import { Task, CreateTaskData, UpdateTaskData } from '@/types/tasks';
import apiClient from './client';

// Helper function to transform API response to Task interface
const transformTaskResponse = (apiTask: any): Task => {
  // Safely create date objects, falling back to current time if parsing fails
  const createdAt = new Date(apiTask.created_at);
  const updatedAt = new Date(apiTask.updated_at);

  return {
    id: apiTask.id,
    title: apiTask.title,
    description: apiTask.description,
    completed: apiTask.completed,
    userId: apiTask.user_id,
    createdAt: isNaN(createdAt.getTime()) ? new Date() : createdAt,
    updatedAt: isNaN(updatedAt.getTime()) ? new Date() : updatedAt,
  };
};

// Helper function to transform API response array to Task array
const transformTaskResponseArray = (apiResponse: any): Task[] => {
  if (!apiResponse || !apiResponse.tasks || !Array.isArray(apiResponse.tasks)) {
    return [];
  }

  return apiResponse.tasks.map(transformTaskResponse);
};

export const taskApi = {
  // Get all tasks for the authenticated user
  async getAll(userId: string): Promise<Task[]> {
    if (!userId || typeof userId !== 'string' || userId.trim() === '') {
      throw new Error('Invalid user ID provided for fetching tasks');
    }
    const response = await apiClient.get<any>(`/api/${userId}/tasks`);
    return transformTaskResponseArray(response);
  },

  // Get a specific task by ID
  async getById(userId: string, taskId: string): Promise<Task> {
    if (!userId || typeof userId !== 'string' || userId.trim() === '') {
      throw new Error('Invalid user ID provided for fetching task');
    }
    if (!taskId || typeof taskId !== 'string' || taskId.trim() === '') {
      throw new Error('Invalid task ID provided for fetching task');
    }
    const apiTask = await apiClient.get<any>(`/api/${userId}/tasks/${taskId}`);
    return transformTaskResponse(apiTask);
  },

  // Create a new task
  async create(userId: string, data: CreateTaskData): Promise<Task> {
    if (!userId || typeof userId !== 'string' || userId.trim() === '') {
      throw new Error('Invalid user ID provided for creating task');
    }
    const apiTask = await apiClient.post<any>(`/api/${userId}/tasks`, data);
    return transformTaskResponse(apiTask);
  },

  // Update a task
  async update(userId: string, taskId: string, data: UpdateTaskData): Promise<Task> {
    if (!userId || typeof userId !== 'string' || userId.trim() === '') {
      throw new Error('Invalid user ID provided for updating task');
    }
    if (!taskId || typeof taskId !== 'string' || taskId.trim() === '') {
      throw new Error('Invalid task ID provided for updating task');
    }
    const apiTask = await apiClient.put<any>(`/api/${userId}/tasks/${taskId}`, data);
    return transformTaskResponse(apiTask);
  },

  // Delete a task
  async delete(userId: string, taskId: string): Promise<void> {
    if (!userId || typeof userId !== 'string' || userId.trim() === '') {
      console.error('Invalid user ID provided for deleting task:', userId);
      throw new Error('Invalid user ID provided for deleting task');
    }
    if (!taskId || typeof taskId !== 'string' || taskId.trim() === '') {
      console.error('Invalid task ID provided for deleting task:', taskId);
      throw new Error('Invalid task ID provided for deleting task');
    }
    try {
      await apiClient.delete<void>(`/api/${userId}/tasks/${taskId}`);
    } catch (error) {
      console.error('DELETE request failed:', error);
      throw error;
    }
  },

  // Toggle task completion status
  async toggleComplete(userId: string, taskId: string, completed: boolean): Promise<Task> {
    if (!userId || typeof userId !== 'string' || userId.trim() === '') {
      throw new Error('Invalid user ID provided for toggling task completion');
    }
    if (!taskId || typeof taskId !== 'string' || taskId.trim() === '') {
      throw new Error('Invalid task ID provided for toggling task completion');
    }
    const apiTask = await apiClient.patch<any>(`/api/${userId}/tasks/${taskId}/complete`, { completed });
    return transformTaskResponse(apiTask);
  },
};