'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import { Task } from '@/types/tasks';
import TaskForm from '@/components/tasks/task-form';
import Button from '@/components/ui/button';
import LoadingSpinner from '@/components/common/loading-spinner';

export default function EditTaskPage() {
  const { id } = useParams();
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const { tasks, loading, error, updateTask, deleteTask } = useTasks(user?.id || '');

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

  const handleSubmit = async (updatedData: { title: string; description?: string }) => {
    if (task && user) {
      await updateTask(task.id, updatedData);
      router.push(`/tasks/${id}`);
    }
  };

  const handleCancel = () => {
    router.push(`/tasks/${id}`);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(id as string);
        router.push('/dashboard');
      } catch (error) {
        console.error('Error deleting task:', error);
        // Navigate back to task details on error
        router.push(`/tasks/${id}`);
      }
    }
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
        <Button onClick={() => router.push('/dashboard')}>Back to Dashboard</Button>
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
        <Button onClick={() => router.push('/dashboard')}>Back to Dashboard</Button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Edit Task</h1>
        <Button variant="danger" size="sm" onClick={handleDelete}>
          Delete Task
        </Button>
      </div>
      <TaskForm
        task={task}
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        submitButtonText="Update Task"
      />
    </div>
  );
}