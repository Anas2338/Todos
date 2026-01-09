import { useState, useEffect } from 'react';
import { Task, CreateTaskData, UpdateTaskData } from '@/types/tasks';
import { taskApi } from '@/lib/api/tasks';

interface UseTasksReturn {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  forceRefresh: () => void;
  createTask: (data: CreateTaskData) => Promise<Task>;
  updateTask: (taskId: string, data: UpdateTaskData) => Promise<Task>;
  deleteTask: (taskId: string) => Promise<void>;
  toggleTaskCompletion: (taskId: string) => Promise<Task>;
}

export const useTasks = (userId: string): UseTasksReturn => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTasks = await taskApi.getAll(userId);
      // Defensive check: ensure fetchedTasks is an array before setting state
      const tasksArray = Array.isArray(fetchedTasks) ? fetchedTasks : [];
      setTasks(tasksArray);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (data: CreateTaskData) => {
    try {
      setLoading(true);
      const newTask = await taskApi.create(userId, data);
      setTasks(prev => {
        // Defensive check: ensure prev is an array
        const currentTasks = Array.isArray(prev) ? prev : [];
        return [...currentTasks, newTask];
      });
      // Return the new task to indicate success
      return newTask;
    } catch (err) {
      const errorMessage = (err as Error).message;
      setError(errorMessage);
      // Re-throw the error so callers can handle it
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (taskId: string, data: UpdateTaskData) => {
    try {
      setLoading(true);
      const updatedTask = await taskApi.update(userId, taskId, data);
      setTasks(prev => {
        // Defensive check: ensure prev is an array
        const currentTasks = Array.isArray(prev) ? prev : [];
        return currentTasks.map(task => task.id === taskId ? updatedTask : task);
      });
      return updatedTask;
    } catch (err) {
      const errorMessage = (err as Error).message;
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (taskId: string) => {
    try {
      setLoading(true);

      // Validate parameters before calling API
      if (!userId || typeof userId !== 'string' || userId.trim() === '') {
        throw new Error('Invalid user ID provided for deleting task');
      }
      if (!taskId || typeof taskId !== 'string' || taskId.trim() === '') {
        throw new Error('Invalid task ID provided for deleting task');
      }

      await taskApi.delete(userId, taskId);
      setTasks(prev => {
        // Defensive check: ensure prev is an array
        const currentTasks = Array.isArray(prev) ? prev : [];
        return currentTasks.filter(task => task.id !== taskId);
      });
    } catch (err) {
      const errorMessage = (err as Error).message;
      console.error('Error deleting task:', err);
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: string) => {
    try {
      const task = tasks.find(t => t.id === taskId);
      if (!task) {
        throw new Error('Task not found');
      }

      setLoading(true);
      const updatedTask = await taskApi.toggleComplete(userId, taskId, !task.completed);
      setTasks(prev => {
        // Defensive check: ensure prev is an array
        const currentTasks = Array.isArray(prev) ? prev : [];
        return currentTasks.map(task => task.id === taskId ? updatedTask : task);
      });
      return updatedTask;
    } catch (err) {
      const errorMessage = (err as Error).message;
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks on initial load
  useEffect(() => {
    if (userId && typeof userId === 'string' && userId.trim() !== '') {
      fetchTasks();
    }
  }, [userId]);

  const forceRefresh = () => {
    if (userId && typeof userId === 'string' && userId.trim() !== '') {
      fetchTasks();
    }
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    forceRefresh,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};