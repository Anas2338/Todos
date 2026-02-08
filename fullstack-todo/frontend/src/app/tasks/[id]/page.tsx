'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import { Task } from '@/types/tasks';
import Button from '@/components/ui/button';
import LoadingSpinner from '@/components/common/loading-spinner';

// Helper function to safely format dates
const formatDate = (dateValue: string | Date | undefined): string => {
  if (!dateValue) {
    return 'Date not available';
  }

  // Handle empty string specifically
  if (typeof dateValue === 'string' && dateValue.trim() === '') {
    return 'Date not available';
  }

  let date: Date | null = null;

  if (typeof dateValue === 'string') {
    // If it's a string, try to parse it
    date = new Date(dateValue);
  } else if (dateValue instanceof Date) {
    // If it's already a Date object
    date = dateValue;
  } else {
    // If it's neither a string nor a Date object
    return 'Date not available';
  }

  // Check if the date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date';
  }

  // Format as locale date string
  return date.toLocaleString();
};

export default function TaskDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const { tasks, loading, error, fetchTasks, deleteTask, toggleTaskCompletion } = useTasks(user?.id || '');

  // Redirect to login if not authenticated, but only after auth loading is complete
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [authLoading, user, router]);

  // If user is not authenticated and not loading, show nothing or loading state
  if (!authLoading && !user) {
    return null; // or show a loading state while redirect happens
  }
  const [task, setTask] = useState<Task | null>(null);

  useEffect(() => {
    if (tasks.length > 0) {
      const foundTask = tasks.find(t => t.id === id);
      setTask(foundTask || null);
    }
  }, [tasks, id]);

  const handleToggleComplete = async () => {
    if (task && user) {
      try {
        // Toggle the task completion status using the useTasks hook
        await toggleTaskCompletion(task.id);
        // Fetch tasks to refresh the UI with the updated status
        await fetchTasks();
      } catch (error) {
        console.error('Error toggling task completion:', error);
        // Fetch tasks to ensure UI is up-to-date even if there was an error
        await fetchTasks();
      }
    }
  };

  const handleEdit = () => {
    router.push(`/tasks/${id}/edit`);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(id as string);
        router.push('/dashboard');
      } catch (error) {
        console.error('Error deleting task:', error);
        // Fetch tasks to ensure UI is up-to-date
        await fetchTasks();
        router.push('/dashboard');
      }
    }
  };

  const handleBack = () => {
    router.push('/dashboard');
  };

  if (loading && !task) {
    return (
      <div className="p-6">
        <div className="flex justify-center items-center h-64">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="rounded-md bg-red-50 p-4 mb-4">
          <div className="flex">
            <div className="shrink-0">
              <span className="text-red-400">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error loading task</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
        <Button onClick={handleBack}>Back to Dashboard</Button>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="p-6">
        <div className="rounded-md bg-red-50 p-4 mb-4">
          <div className="flex">
            <div className="shrink-0">
              <span className="text-red-400">⚠️</span>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Task not found</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>The requested task could not be found.</p>
              </div>
            </div>
          </div>
        </div>
        <Button onClick={handleBack}>Back to Dashboard</Button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="flex justify-between items-start mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Task Details</h1>
        <Button variant="secondary" onClick={handleBack}>
          Back to Dashboard
        </Button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <div className="flex items-center justify-between">
            <h3 className={`text-lg leading-6 font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            <div className="flex items-center space-x-2">
              <Button
                variant={task.completed ? 'outline' : 'primary'}
                size="sm"
                onClick={handleToggleComplete}
              >
                {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
              </Button>
              <Button variant="outline" size="sm" onClick={handleEdit}>
                Edit
              </Button>
              <Button variant="danger" size="sm" onClick={handleDelete}>
                Delete
              </Button>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
          <dl className="sm:divide-y sm:divide-gray-200">
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Description</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {task.description || 'No description provided'}
              </dd>
            </div>
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Status</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  task.completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
              </dd>
            </div>
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Created</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {formatDate(task.createdAt)}
              </dd>
            </div>
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Updated</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {formatDate(task.updatedAt)}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
}